#!/usr/bin/env python3
"""check whether each event returns the same count across repeated runs"""

from collections import Counter
from datetime import datetime
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
import tempfile
import time

# avoid root-owned bytecode files when running with sudo
sys.dont_write_bytecode = True

from machine import identify, select_cores, smt_disabled
from messages import Parser, message
from permissions import user_owned_outputs
import skid
from worker import defer_interrupts, interrupt, run_worker, signal_group

BASE = Path(__file__).resolve().parents[1]
MONTHS = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')


def arguments():
    parser = Parser(description=__doc__)
    parser.add_argument(
        '--mode',
        choices=('count', 'skid'),
        default='count',
        help='count determinism or overflow skid (default: count)',
    )
    parser.add_argument(
        '--cores', type=int, help='worker cores (default: all minus one; one with --event)'
    )
    parser.add_argument(
        '--start-core', type=int, help='first worker CPU number (default: lowest available)'
    )
    parser.add_argument('--rounds', type=int, default=10, help='rounds per event (default: 10)')

    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--events', type=Path, help='one plain event name per line')
    selection.add_argument('--event', help='one event name, optionally ending in :u')
    selection.add_argument(
        '--from-results',
        type=Path,
        help='count results for skid (default: latest matching CPU run)',
    )

    parser.add_argument(
        '--overflow',
        dest='overflow_threshold',
        type=int,
        help='skid overflow threshold (default: select from a preliminary count)',
    )
    parser.add_argument('--output', type=Path, help='save a dated run under this directory')
    parser.add_argument(
        '--benchmark',
        type=Path,
        default=BASE.parent / 'deterministic/static/binaries/retired_instr.all.x86_64',
    )
    parser.add_argument(
        '--timeout', type=float, default=120, help='seconds allowed per measurement (default: 120)'
    )

    args = parser.parse_args()

    if args.event:
        args.event = args.event.removesuffix(':u')

        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]*', args.event):
            parser.error('--event requires one plain event name, optionally ending in :u')

    if args.mode != 'skid' and (args.from_results or args.overflow_threshold is not None):
        parser.error('--from-results and --overflow require --mode skid')

    if args.overflow_threshold is not None and not 2 <= args.overflow_threshold <= 2147483647:
        parser.error('--overflow must be between 2 and 2147483647')

    if args.start_core is not None and args.start_core < 0:
        parser.error('--start-core must be nonnegative')

    if args.rounds < 2:
        parser.error('--rounds must be at least 2')

    if not 0 < args.timeout < float('inf'):
        parser.error('--timeout must be finite and positive')

    return args


def find_count_results(info):
    name = f'{info["slug"]}-step{info["stepping"]}'
    directory = BASE / 'results/counts' / info['microarch'] / name

    return latest_count_results(directory)


def latest_count_results(directory):
    matches = []

    if directory.is_dir():
        for path in directory.iterdir():
            try:
                month, rest = path.name.split('-', 1)
                date = datetime.strptime(rest, '%d-%Y-%H:%M:%S')
                date = date.replace(month=MONTHS.index(month) + 1)
            except ValueError:
                continue

            if path.is_dir():
                matches.append((date, path))

    for date, path in sorted(matches, reverse=True):
        if skid.has_count_results(path):
            return path

    raise ValueError(
        f'no dated count runs found in {directory}; '
        'pass --from-results PATH, --events PATH, or --event NAME'
    )


def read_events(path):
    if not path.is_file():
        raise ValueError(
            f'event list not found: {path}; '
            'capture one with src/perf-list-events.py and pass it with --events'
        )

    events = path.read_text().splitlines()

    if not events or len(set(events)) != len(events):
        raise ValueError('event list must be nonempty and contain no duplicates')

    if any(not re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]*', event) for event in events):
        raise ValueError('use one plain event name per line, without modifiers or whitespace')

    return events


def output_directory(requested):
    requested = requested.absolute()
    parents = []

    for parent in requested.parents:
        if parent.exists():
            break

        parents.append(parent)

    if not requested.exists():
        parents.append(requested)

    with user_owned_outputs(parents):
        requested.mkdir(parents=True, exist_ok=True)

    while True:
        now = datetime.now()
        stamp = f'{MONTHS[now.month - 1]}-{now:%d-%Y-%H:%M:%S}'
        candidate = requested / stamp

        try:
            candidate.mkdir()
            return candidate
        except FileExistsError:
            message('~', f'run already exists at {candidate}; waiting for the next second')
            time.sleep(1)


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


def report(output, total, started, state, mode='count'):
    rows = collect(output)
    counts = Counter(row['status'] for row in rows)
    elapsed = time.monotonic() - started
    progress = (
        f'{state}: {len(rows)}/{total} ({len(rows) / total:.1%}); '
        f'remaining: {total - len(rows)}; elapsed: {elapsed:.0f}s\n'
    )
    progress += '; '.join(f'{name}: {number}' for name, number in sorted(counts.items())) + '\n'
    atomic_write(output / 'progress.txt', progress)

    last_status = 'Inconclusive' if mode == 'skid' else 'Zero-only'
    text = [
        '# Skid results' if mode == 'skid' else '# Event results',
        '',
        f'* {state}: {len(rows)}/{total}',
        f'* Potentially deterministic: {counts["Potentially deterministic"]}',
        f'* Non-deterministic: {counts["Non-deterministic"]}',
        f'* {last_status}: {counts[last_status]}',
        '',
        '[Processor and settings](profile.md) · [Input events](events.txt)',
        '',
    ]

    if mode == 'skid':
        text.extend(skid.report_rows(rows))
        atomic_write(output / 'results.md', '\n'.join(text))

        return rows

    sections = [
        ('Determinism', ['Potentially deterministic', 'Non-deterministic']),
        ('Zero-only (inconclusive)', ['Zero-only']),
        ('Measurement errors', ['Error']),
    ]

    for title, statuses in sections:
        selected = sorted(
            (row for row in rows if row['status'] in statuses),
            key=lambda row: (statuses.index(row['status']), row['event']),
        )

        if not selected:
            continue

        text += [f'## {title}', '', '| Event | Runs | Determinism |', '|---|---:|---|']

        for row in selected:
            text.append(f'| [`{row["event"]}`]({row["log"]}) | {row["runs"]} | {row["status"]} |')

        text.append('')

    atomic_write(output / 'results.md', '\n'.join(text))

    return rows


def experiment(args, info, events, cpus, reserve):
    category = 'skid' if args.mode == 'skid' else 'counts'
    results_root = BASE / 'results' / category

    requested = args.output or (
        results_root / info['microarch'] / f'{info["slug"]}-step{info["stepping"]}'
    )
    output = output_directory(requested)
    started_at = datetime.now().astimezone().isoformat(timespec='seconds')

    with user_owned_outputs([output]):
        (output / 'events.txt').write_text('\n'.join(events) + '\n')
        helper, configs = None, None

        if args.mode == 'skid':
            helper, configs = skid.prepare(events, output)

        profile = (
            f'# Processor profile\n\n'
            f'- Started: {started_at}\n'
            f'- Processor: {info["model"]}\n'
            f'- Microarchitecture/event family: `{info["microarch"]}`\n'
            f'- CPU family/model: {info["family"]}/0x{info["model_id"]:02x}\n'
            f'- Stepping: {info["stepping"]}\n'
            f'- Mode: {args.mode}\n'
            f'- Worker CPUs: {cpus}\n- Reserved coordinator CPU: {reserve}\n'
            f'- SMT: verified disabled or not supported\n'
            f'- Rounds: {args.rounds}\n- Events: {len(events)}\n'
            f'- Per-round timeout: {args.timeout:g} seconds\n'
            f'- Benchmark: `{args.benchmark}`\n'
            f'- Input: `{args.from_results or args.event or args.events}`\n\n'
            'Results describe this run, not all processors with the same name.\n'
        )

        if args.mode == 'skid':
            profile += (
                '\nSkid is measured from counter enable at the exec stop to the overflow '
                'signal-delivery stop, before a user signal handler runs. '
                'Only benchmark user-space events are counted. '
                'This includes the Linux delivery path; it is not hardware interrupt latency alone.\n'
                f'\nOverflow threshold: {args.overflow_threshold or "half the preliminary count, capped at 1000000"}. '
                'The selected overflow threshold and counter encoding are saved for each event.\n'
            )

        (output / 'profile.md').write_text(profile)
        print(f'Results: {output}\nWorkers: {cpus}; coordinator: {reserve}', flush=True)
        workers = []
        started, state = time.monotonic(), 'Running'

        try:
            indexed = list(enumerate(events, 1))

            for position, cpu in enumerate(cpus):
                assigned = indexed[position :: len(cpus)]

                if not assigned:
                    continue

                folder = output / 'workers' / f'cpu{cpu}'
                folder.mkdir(parents=True)
                (folder / 'events.txt').write_text(''.join(event + '\n' for _, event in assigned))
                target = run_worker
                worker_args = (cpu, assigned, folder, args.benchmark, args.rounds, args.timeout)

                if args.mode == 'skid':
                    target = skid.run_worker
                    worker_args += (helper, configs, args.overflow_threshold, bool(args.event))

                worker = multiprocessing.get_context('fork').Process(
                    target=target, args=worker_args
                )

                with defer_interrupts():
                    worker.start()
                    workers.append(worker)

            while any(worker.is_alive() for worker in workers):
                report(output, len(events), started, state, args.mode)

                if any(worker.exitcode not in (None, 0) for worker in workers):
                    raise RuntimeError('a worker failed; inspect its event logs')

                time.sleep(1)

            if all(worker.exitcode == 0 for worker in workers):
                state = 'Complete'
            else:
                state = 'Failed'
        except BaseException:
            state = 'Interrupted or failed'
            raise
        finally:
            # stop the workers and benchmarks before turning SMT back on
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

            rows = report(output, len(events), started, state, args.mode)
            print((output / 'progress.txt').read_text(), end='', flush=True)

    failed = (
        state != 'Complete'
        or len(rows) != len(events)
        or any(row['status'] == 'Error' or row.get('errors', 0) for row in rows)
    )

    if failed:
        message('-', f'run finished with errors; see {output / "results.md"}')
    else:
        message('+', f'run complete; see {output / "results.md"}')

    return int(failed)


def console_experiment(args, cpu):
    with tempfile.TemporaryDirectory(prefix='deterministic-skid-') as temporary:
        helper, configs = skid.prepare([args.event], Path(temporary), save=False)
        worker = multiprocessing.get_context('fork').Process(
            target=skid.run_console,
            args=(
                cpu,
                args.event,
                args.benchmark,
                args.rounds,
                args.timeout,
                helper,
                configs[args.event],
                args.overflow_threshold,
            ),
        )

        try:
            with defer_interrupts():
                worker.start()

            while worker.is_alive():
                worker.join(timeout=1)

            return int(worker.exitcode != 0)
        finally:
            if worker.pid is not None:
                if worker.is_alive():
                    worker.terminate()

                worker.join(timeout=10)

                if worker.is_alive():
                    worker.kill()
                    worker.join()


def main():
    args = arguments()

    if os.geteuid() != 0 and args.mode != 'skid':
        raise ValueError('run with sudo python3 src/run.py')

    if shutil.which('perf') is None:
        raise ValueError('perf is missing; install it using your distribution package manager')

    args.benchmark = args.benchmark.resolve()

    if not args.benchmark.is_file() or not os.access(args.benchmark, os.X_OK):
        raise ValueError(f'benchmark is not executable: {args.benchmark}')

    info = identify()

    if args.mode == 'skid' and not (args.from_results or args.events or args.event):
        args.from_results = find_count_results(info)
        message('~', f'using detected count results: {args.from_results}')

    if args.from_results:
        args.from_results = args.from_results.resolve()

        if not (args.from_results / 'workers').is_dir():
            args.from_results = latest_count_results(args.from_results)
            message('~', f'using count results: {args.from_results}')
    elif not args.event:
        args.events = (
            args.events or BASE / 'events/intel' / info['microarch'] / 'events.txt'
        ).resolve()

    signal.signal(signal.SIGTERM, interrupt)
    signal.signal(signal.SIGINT, interrupt)
    allowed = os.sched_getaffinity(0)
    # otherwise, another run could turn SMT back on while this one is still running
    lock_fd = os.open('/run/lock/deterministic-events.lock', os.O_RDONLY | os.O_CREAT, 0o644)

    with os.fdopen(lock_fd, 'r') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError('another deterministic event experiment is running') from error

        if args.events and not args.events.exists():
            message('~', f'event list missing; capturing it to {args.events}')
            result = subprocess.run(
                [
                    sys.executable,
                    str(BASE / 'src/perf-list-events.py'),
                    '--output',
                    str(args.events),
                ]
            )

            if result.returncode:
                raise RuntimeError('could not generate the event list; no workers started')

        if args.from_results:
            events = skid.candidates(args.from_results)
        elif args.event:
            events = [args.event]
        else:
            events = read_events(args.events)

        with smt_disabled():
            core_count = args.cores

            if args.event and core_count is None:
                core_count = 1

            cpus, reserve = select_cores(allowed, core_count, args.start_core)

            try:
                os.sched_setaffinity(0, {reserve})

                if args.mode == 'skid' and args.event and args.output is None:
                    return console_experiment(args, cpus[0])

                return experiment(args, info, events, cpus, reserve)
            finally:
                os.sched_setaffinity(0, allowed)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        message('~', 'interrupted')
        sys.exit(130)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        message('-', str(error))
        sys.exit(1)
