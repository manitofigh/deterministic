import contextlib
import csv
from decimal import Decimal, InvalidOperation
import json
import os
from pathlib import Path
import signal
import subprocess
import traceback


def parse_count(text, event):
    rows = [row for row in csv.reader(text.splitlines(), delimiter=';')
            if len(row) >= 3 and row[2].strip() in (event, event.removesuffix(':u'))]
    if len(rows) != 1:
        raise ValueError('expected exactly one counter result')
    row = [field.strip() for field in rows[0]]
    if row[0] == '<not supported>':
        raise ValueError('event not supported')
    if len(row) < 5 or not row[0].isascii() or not row[0].isdigit():
        raise ValueError('counter did not produce an integer count')
    try:
        runtime, percent = Decimal(row[3]), Decimal(row[4])
        if not runtime.is_finite() or runtime <= 0 or percent != 100:
            raise ValueError('counter did not run for the full measurement')
    except InvalidOperation as error:
        raise ValueError('invalid counter runtime or running percentage') from error
    return int(row[0])


def interrupt(signum, frame):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    raise KeyboardInterrupt


@contextlib.contextmanager
def defer_interrupts():
    pending = []

    def remember(signum, frame):
        pending.append((signum, frame))

    previous = {}
    for signum in (signal.SIGINT, signal.SIGTERM):
        handler = signal.getsignal(signum)
        if handler != signal.SIG_IGN:
            previous[signum] = signal.signal(signum, remember)
    try:
        yield
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)
        if pending:
            interrupt(*pending[0])


def signal_group(pid, signum):
    try:
        os.killpg(pid, signum)
    except ProcessLookupError:
        pass


def measure(command, raw_path, log, timeout):
    raw_path.unlink(missing_ok=True)
    process = None
    pid_path = raw_path.with_suffix('.pid')
    try:
        # save the PID before handling a stop request so we can still kill perf.
        with defer_interrupts():
            process = subprocess.Popen(
                command, stdout=subprocess.DEVNULL, stderr=log,
                env={**os.environ, 'LC_ALL': 'C'}, start_new_session=True)
            pid_path.write_text(str(process.pid))
        returncode = process.wait(timeout=timeout)
        error = None
    except subprocess.TimeoutExpired:
        returncode, error = None, f'timeout after {timeout:g} seconds'
    finally:
        if process is not None and process.poll() is None:
            signal_group(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                signal_group(process.pid, signal.SIGKILL)
                process.wait()
        # perf can exit while the benchmark is still running.
        if process is not None:
            signal_group(process.pid, signal.SIGKILL)
        pid_path.unlink(missing_ok=True)
        raw = raw_path.read_text(errors='replace') if raw_path.exists() else ''
    return returncode, raw, error


def test_event(index, event, cpu, folder, benchmark, rounds, timeout, counts_file):
    event = event + ':u'
    log_path = folder / f'event-{index:04d}.log'
    counts = []
    status, note = 'Potentially deterministic', ''
    with log_path.open('w', buffering=1) as log:
        log.write(f'event: {event}\ncpu: {cpu}\nround limit: {rounds}\n')
        for number in range(1, rounds + 1):
            log.write(f'\n--- round {number} ---\n')
            raw_path = folder / 'perf.tmp'
            command = ['perf', 'stat', '--no-big-num', '--no-scale', '-x', ';',
                       '-o', str(raw_path), '-e', event, '--', str(benchmark)]
            returncode, raw, error = measure(command, raw_path, log, timeout)
            count = None
            if not error:
                try:
                    if returncode != 0:
                        raise ValueError(f'perf or benchmark exited with {returncode}')
                    count = parse_count(raw, event)
                except ValueError as problem:
                    error = str(problem)
            counts_file.write(f'{event}\t{number}\t{count if count is not None else "INVALID"}'
                              f'\t{returncode}\n')
            log.write(f'parsed count: {count}\nexit: {returncode}\n')
            if error:
                status, note = 'Error', error
                break
            counts.append(count)
            if count != counts[0]:
                status = 'Non-deterministic'
                break
        if status == 'Potentially deterministic' and counts[0] == 0:
            status, note = 'Zero-only', 'all rounds returned zero; inconclusive'
        log.write(f'\nresult: {status}\nrounds attempted: {number}\n{note}\n')
    raw_path.unlink(missing_ok=True)
    return dict(index=index, event=event, cpu=cpu, runs=number, status=status,
                counts=counts, note=note, log=f'workers/cpu{cpu}/{log_path.name}')


def run_worker(cpu, assigned, folder, benchmark, rounds, timeout):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, interrupt)
    folder = Path(folder)
    try:
        os.sched_setaffinity(0, {cpu})
        with (folder / 'counts.tsv').open('w', buffering=1) as counts:
            counts.write('event\tround\tcount\texit\n')
            with (folder / 'results.jsonl').open('w', buffering=1) as results:
                for index, event in assigned:
                    result = test_event(index, event, cpu, folder, benchmark,
                                        rounds, timeout, counts)
                    results.write(json.dumps(result) + '\n')
    except KeyboardInterrupt:
        raise SystemExit(130)
    except Exception:
        (folder / 'worker.log').write_text(traceback.format_exc())
        raise SystemExit(1)
