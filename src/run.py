#!/usr/bin/env python3
"""check whether each event returns the same count across repeated runs."""

from collections import Counter
import fcntl
import json
import multiprocessing
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

from machine import identify, select_cores, smt_disabled
from messages import Parser, message
from worker import defer_interrupts, interrupt, run_worker, signal_group


BASE = Path(__file__).resolve().parents[1]


def arguments():
    parser = Parser(description=__doc__)
    parser.add_argument('--cores', type=int, help='worker cores (default: all minus one)')
    parser.add_argument('--rounds', type=int, default=5, help='maximum rounds per event (default: 5)')
    parser.add_argument('--events', type=Path, help='one plain event name per line')
    parser.add_argument('--output', type=Path, help='custom output directory; never overwritten')
    parser.add_argument('--benchmark', type=Path,
                        default=BASE.parent / 'deterministic/static/binaries/retired_instr.all.x86_64')
    parser.add_argument('--timeout', type=float, default=120,
                        help='seconds allowed per measurement (default: 120)')
    args = parser.parse_args()
    if args.rounds < 2:
        parser.error('--rounds must be at least 2')
    if not 0 < args.timeout < float('inf'):
        parser.error('--timeout must be finite and positive')
    return args


def read_events(path):
    if not path.is_file():
        raise ValueError(f'event list not found: {path}; '
                         'capture one with src/perf-list-events.py and pass it with --events')
    events = path.read_text().splitlines()
    if not events or len(set(events)) != len(events):
        raise ValueError('event list must be nonempty and contain no duplicates')
    if any(not re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]*', event) for event in events):
        raise ValueError('use one plain event name per line, without modifiers or whitespace')
    return events


def output_directory(requested):
    requested = requested.absolute()
    requested.parent.mkdir(parents=True, exist_ok=True)
    candidate = requested
    suffix = 1
    while True:
        try:
            candidate.mkdir()
            break
        except FileExistsError:
            suffix += 1
            candidate = requested.with_name(f'{requested.name}-{suffix}')
    if suffix > 1:
        message('~', f'output exists; using {candidate}')
    return candidate


def atomic_write(path, text):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(text)
    temporary.replace(path)


def collect(output):
    rows = []
    for path in sorted(output.glob('workers/cpu*/results.jsonl')):
        for line in path.read_text().splitlines(keepends=True):
            if line.endswith('\n'):
                rows.append(json.loads(line))
    return rows


def report(output, total, started, state):
    rows = collect(output)
    counts = Counter(row['status'] for row in rows)
    elapsed = time.monotonic() - started
    progress = (f'{state}: {len(rows)}/{total} ({len(rows) / total:.1%}); '
                f'remaining: {total - len(rows)}; elapsed: {elapsed:.0f}s\n')
    progress += '; '.join(f'{name}: {number}' for name, number in sorted(counts.items())) + '\n'
    atomic_write(output / 'progress.txt', progress)
    text = ['# Event results', '', f'* {state}: {len(rows)}/{total}',
            f'* Potentially deterministic: {counts["Potentially deterministic"]}',
            f'* Non-deterministic: {counts["Non-deterministic"]}',
            f'* Zero-only: {counts["Zero-only"]}', '',
            '[Processor and settings](profile.md) · [Input events](events.txt)', '']
    sections = [('Determinism', ['Potentially deterministic', 'Non-deterministic']),
                ('Zero-only (inconclusive)', ['Zero-only']), ('Measurement errors', ['Error'])]
    for title, statuses in sections:
        selected = sorted((row for row in rows if row['status'] in statuses),
                          key=lambda row: (statuses.index(row['status']), row['event']))
        if not selected:
            continue
        text += [f'## {title}', '', '| Event | Runs | Determinism |', '|---|---:|---|']
        for row in selected:
            text.append(f'| [`{row["event"]}`]({row["log"]}) | {row["runs"]} | {row["status"]} |')
        text.append('')
    atomic_write(output / 'results.md', '\n'.join(text))
    return rows


def experiment(args, info, events, cpus, reserve):
    requested = args.output or (BASE / 'results' / info['microarch'] /
                                f'{info["slug"]}-step{info["stepping"]}')
    output = output_directory(requested)
    (output / 'events.txt').write_text('\n'.join(events) + '\n')
    profile = (f'# Processor profile\n\n'
               f'- Processor: {info["model"]}\n'
               f'- Microarchitecture/event family: `{info["microarch"]}`\n'
               f'- CPU family/model: {info["family"]}/0x{info["model_id"]:02x}\n'
               f'- Stepping: {info["stepping"]}\n'
               f'- Worker CPUs: {cpus}\n- Reserved coordinator CPU: {reserve}\n'
               f'- SMT: verified disabled or not supported\n'
               f'- Maximum rounds: {args.rounds}\n- Events: {len(events)}\n'
               f'- Per-round timeout: {args.timeout:g} seconds\n'
               f'- Benchmark: `{args.benchmark}`\n'
               f'- Input: `{args.events}`\n\n'
               'Results describe this run, not all processors with the same name.\n')
    (output / 'profile.md').write_text(profile)
    print(f'Results: {output}\nWorkers: {cpus}; coordinator: {reserve}', flush=True)
    workers = []
    started, state = time.monotonic(), 'Running'
    try:
        indexed = list(enumerate(events, 1))
        for position, cpu in enumerate(cpus):
            assigned = indexed[position::len(cpus)]
            if not assigned:
                continue
            folder = output / 'workers' / f'cpu{cpu}'
            folder.mkdir(parents=True)
            (folder / 'events.txt').write_text(''.join(event + '\n' for _, event in assigned))
            worker = multiprocessing.get_context('fork').Process(
                target=run_worker,
                args=(cpu, assigned, folder, args.benchmark, args.rounds, args.timeout))
            with defer_interrupts():
                worker.start()
                workers.append(worker)
        while any(worker.is_alive() for worker in workers):
            report(output, len(events), started, state)
            if any(worker.exitcode not in (None, 0) for worker in workers):
                raise RuntimeError('a worker failed; inspect its event logs')
            time.sleep(1)
        state = 'Complete' if all(worker.exitcode == 0 for worker in workers) else 'Failed'
    except BaseException:
        state = 'Interrupted or failed'
        raise
    finally:
        # stop the workers and benchmarks before turning SMT back on.
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        for worker in workers:
            if worker.is_alive():
                worker.terminate()
        for worker in workers:
            worker.join(timeout=10)
            if worker.is_alive():
                worker.kill()
                worker.join()
        for pid_path in output.glob('workers/cpu*/perf.pid'):
            signal_group(int(pid_path.read_text()), signal.SIGKILL)
            pid_path.unlink()
        rows = report(output, len(events), started, state)
        print((output / 'progress.txt').read_text(), end='', flush=True)
    failed = (state != 'Complete' or len(rows) != len(events)
              or any(row['status'] == 'Error' for row in rows))
    message('-' if failed else '+',
            f'run finished with errors; see {output / "results.md"}' if failed else
            f'run complete; see {output / "results.md"}')
    return int(failed)


def main():
    args = arguments()
    if os.geteuid() != 0:
        raise ValueError('run with sudo python3 src/run.py')
    if shutil.which('perf') is None:
        raise ValueError('perf is missing; install it using your distribution package manager')
    args.benchmark = args.benchmark.resolve()
    if not args.benchmark.is_file() or not os.access(args.benchmark, os.X_OK):
        raise ValueError(f'benchmark is not executable: {args.benchmark}')
    info = identify()
    args.events = (args.events or BASE / 'events/intel' / info['microarch'] / 'events.txt').resolve()
    signal.signal(signal.SIGTERM, interrupt)
    signal.signal(signal.SIGINT, interrupt)
    allowed = os.sched_getaffinity(0)
    # otherwise, another run could turn SMT back on while this one is still running.
    with open('/run/lock/deterministic-events.lock', 'w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError('another deterministic event experiment is running') from error
        if not args.events.exists():
            message('~', f'event list missing; capturing it to {args.events}')
            result = subprocess.run([sys.executable, str(BASE / 'src/perf-list-events.py'),
                                     '--output', str(args.events)])
            if result.returncode:
                raise RuntimeError('could not generate the event list; no workers started')
        events = read_events(args.events)
        with smt_disabled():
            cpus, reserve = select_cores(allowed, args.cores)
            try:
                os.sched_setaffinity(0, {reserve})
                return experiment(args, info, events, cpus, reserve)
            finally:
                os.sched_setaffinity(0, allowed)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        message('~', 'interrupted; partial results retained')
        sys.exit(130)
    except (OSError, ValueError, RuntimeError) as error:
        message('-', str(error))
        sys.exit(1)
