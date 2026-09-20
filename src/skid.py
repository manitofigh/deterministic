"""measure event-count overshoot at a process's overflow signal stop"""

import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import traceback

from worker import interrupt, measure

HARDWARE_EVENTS = {
    'cycles': 0,
    'cpu-cycles': 0,
    'instructions': 1,
    'cache-references': 2,
    'cache-misses': 3,
    'branches': 4,
    'branch-instructions': 4,
    'branch-misses': 5,
    'bus-cycles': 6,
    'stalled-cycles-frontend': 7,
    'stalled-cycles-backend': 8,
    'ref-cycles': 9,
}
CACHE_EVENTS = {
    'L1-dcache': 0,
    'L1-icache': 1,
    'LLC': 2,
    'dTLB': 3,
    'iTLB': 4,
    'branch': 5,
    'node': 6,
}


def candidates(directory):
    selected = set()
    paths = sorted(directory.glob('workers/cpu*/results.jsonl'))

    if not paths:
        raise ValueError(f'no worker results found in {directory}')

    for path in paths:
        for line in path.read_text().splitlines():
            row = json.loads(line)

            if 'skids' in row:
                raise ValueError('--from-results requires count-determinism results')

            if row['status'] == 'Potentially deterministic':
                selected.add(row['event'].removesuffix(':u'))

    if not selected:
        raise ValueError('no potentially deterministic events in the selected run')

    return sorted(selected)


def encode_event(event, records):
    if event in HARDWARE_EVENTS:
        return (0, HARDWARE_EVENTS[event], 0, 0)

    for cache, cache_id in CACHE_EVENTS.items():
        for operation, operation_id in (('load', 0), ('store', 1), ('prefetch', 2)):
            for suffix, result_id in (('s', 0), ('-misses', 1)):
                if event == f'{cache}-{operation}{suffix}':
                    return (3, cache_id | operation_id << 8 | result_id << 16, 0, 0)

    device = Path('/sys/bus/event_source/devices/cpu')
    alias = device / 'events' / event

    if alias.is_file():
        encoding = alias.read_text().strip()
    else:
        encodings = {
            row['Encoding']
            for row in records
            if row.get('EventName') == event
            and row.get('Unit') in ('cpu', 'default_core')
            and row.get('Encoding')
        }

        if len(encodings) != 1:
            raise ValueError(f'expected one core counter encoding for {event}')

        full = encodings.pop()
        unit, separator, fields = full.partition('/')

        if unit not in ('cpu', 'default_core') or not separator or not fields.endswith('/'):
            raise ValueError(f'unsupported encoding for {event}: {full}')

        encoding = fields[:-1]

    config = {'config': 0, 'config1': 0, 'config2': 0}

    for field in encoding.split(','):
        key, separator, value = field.partition('=')

        if key in ('period', 'name'):
            continue

        number = int(value, 0) if separator else 1
        format_path = device / 'format' / key

        if not format_path.is_file():
            raise ValueError(f'unsupported counter field {key} for {event}')

        register, positions = format_path.read_text().strip().split(':')
        bits = []

        for position in positions.split(','):
            bounds = position.split('-')
            bits.extend(range(int(bounds[0]), int(bounds[-1]) + 1))

        if register not in config or number < 0 or number >= 1 << len(bits):
            raise ValueError(f'invalid counter field {field} for {event}')

        for source, target in enumerate(bits):
            config[register] |= ((number >> source) & 1) << target

    return (
        int((device / 'type').read_text()),
        config['config'],
        config['config1'],
        config['config2'],
    )


def prepare(events, output):
    compiler = shutil.which('cc')

    if compiler is None:
        raise ValueError('skid mode needs a C compiler; install cc using your package manager')

    source = Path(__file__).with_suffix('.c')
    helper = output / 'skid-helper'
    command = [
        compiler,
        '-O2',
        '-std=gnu11',
        '-Wall',
        '-Wextra',
        '-Werror',
        str(source),
        '-o',
        str(helper),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    (output / 'build.log').write_text(result.stdout + result.stderr)

    if result.returncode:
        raise ValueError(f'could not build skid helper; see {output / "build.log"}')

    result = subprocess.run(
        ['perf', 'list', '--json'],
        capture_output=True,
        text=True,
        env={**os.environ, 'LC_ALL': 'C', 'PERF_PAGER': 'cat'},
        timeout=60,
    )
    (output / 'perf-list.json').write_text(result.stdout)
    (output / 'perf-list.stderr').write_text(result.stderr)

    if result.returncode:
        raise ValueError('could not read counter encodings from perf list --json')

    records = json.loads(result.stdout)
    configs = {}

    for event in events:
        try:
            configs[event] = {'encoding': encode_event(event, records)}
        except ValueError as error:
            configs[event] = {'error': str(error)}

    (output / 'encodings.json').write_text(json.dumps(configs, indent=2) + '\n')

    return helper, configs


def trial(helper, encoding, overflow_threshold, benchmark, folder, log, timeout):
    raw_path = folder / 'perf.tmp'
    command = [
        str(helper),
        *map(str, encoding),
        str(overflow_threshold),
        str(raw_path),
        str(benchmark),
    ]
    code, raw, error = measure(command, raw_path, log, timeout)
    raw_path.unlink(missing_ok=True)

    if error:
        return {'error': error}

    try:
        result = json.loads(raw)
    except (ValueError, TypeError):
        return {'error': f'measurement helper exited with {code} without a valid result'}

    if code and not result.get('error'):
        return {'error': f'measurement helper exited with {code}'}

    return result


def test_event(
    index,
    event,
    cpu,
    folder,
    benchmark,
    rounds,
    timeout,
    counts_file,
    helper,
    config,
    requested_threshold,
):
    log_path = folder / f'event-{index:04d}.log'
    skids, measurements = [], []
    overflow_threshold = requested_threshold
    error = config.get('error')
    note = ''
    baseline = None

    with log_path.open('w', buffering=1) as log:
        log.write(f'event: {event}:u\ncpu: {cpu}\nround limit: {rounds}\n')

        if not error and overflow_threshold is None:
            log.write('\n--- preliminary count ---\n')
            baseline = trial(helper, config['encoding'], 0, benchmark, folder, log, timeout)
            error = baseline.get('error')

            if not error:
                total = baseline['count']
                log.write(f'count: {total}\n')

                if total < 4:
                    note = (
                        'too few events to choose an overflow threshold '
                        f'(count: {total}; need at least 4)'
                    )
                else:
                    overflow_threshold = min(1000000, total // 2)

        log.write(
            'overflow threshold: '
            f'{overflow_threshold if overflow_threshold is not None else "not selected"}\n'
        )

        if error:
            log.write(f'error: {error}\n')
        elif note:
            log.write(f'note: {note}\n')
        else:
            for number in range(1, rounds + 1):
                log.write(f'\n--- round {number} ---\n')
                result = trial(
                    helper, config['encoding'], overflow_threshold, benchmark, folder, log, timeout
                )
                result['round'] = number
                measurements.append(result)

                if result.get('error'):
                    log.write(f'error: {result["error"]}\n')
                else:
                    skids.append(result['skid'])
                    log.write(
                        f'count at stop: {result["count"]}\n'
                        f'skid: {result["skid"]}\n'
                        f'instruction pointer: {result["ip"]}\n'
                    )

                counts_file.write(
                    f'{event}:u\t{number}\t{overflow_threshold}\t'
                    f'{result.get("count", "INVALID")}\t'
                    f'{result.get("skid", "INVALID")}\t'
                    f'{result.get("ip", "")}\t{result.get("error", "")}\n'
                )

        failures = sum('error' in row for row in measurements)

        if len(set(skids)) > 1:
            status = 'Non-deterministic'
        elif len(skids) == rounds:
            status = 'Potentially deterministic'
        else:
            status = 'Inconclusive'

        log.write(f'\nresult: {status}\nsuccessful rounds: {len(skids)}/{rounds}\n')

    return dict(
        index=index,
        event=event + ':u',
        cpu=cpu,
        runs=len(measurements),
        status=status,
        overflow_threshold=overflow_threshold,
        skids=skids,
        measurements=measurements,
        baseline=baseline,
        errors=failures + bool(error),
        note=error or note,
        log=f'workers/cpu{cpu}/{log_path.name}',
    )


def run_worker(
    cpu, assigned, folder, benchmark, rounds, timeout, helper, configs, overflow_threshold
):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, interrupt)

    try:
        os.sched_setaffinity(0, {cpu})

        with (folder / 'counts.tsv').open('w', buffering=1) as counts:
            counts.write('event\tround\toverflow_threshold\tcount\tskid\tip\terror\n')

            with (folder / 'results.jsonl').open('w', buffering=1) as results:
                for index, event in assigned:
                    result = test_event(
                        index,
                        event,
                        cpu,
                        folder,
                        benchmark,
                        rounds,
                        timeout,
                        counts,
                        helper,
                        configs[event],
                        overflow_threshold,
                    )
                    results.write(json.dumps(result) + '\n')
    except KeyboardInterrupt:
        raise SystemExit(130)
    except Exception:
        (folder / 'worker.log').write_text(traceback.format_exc())
        raise SystemExit(1)


def report_rows(rows):
    order = ['Potentially deterministic', 'Non-deterministic', 'Inconclusive']
    text = [
        'Skid is extra event occurrences before the Linux process stop.',
        '',
        '| Event | Min skid | Max skid | Average skid | Skid determinism |',
        '|---|---:|---:|---:|---|',
    ]

    for row in sorted(rows, key=lambda row: (order.index(row['status']), row['event'])):
        skids = row['skids']
        low = min(skids) if skids else '—'
        high = max(skids) if skids else '—'
        average = f'{sum(skids) / len(skids):.2f}' if skids else '—'
        text.append(
            f'| [`{row["event"]}`]({row["log"]}) | {low} | {high} | '
            f'{average} | {row["status"]} |'
        )

    notes = [row for row in rows if row.get('note') and not row['errors']]

    if notes:
        text += ['', '## Measurement notes', '', '| Event | Note |', '|---|---|']

        for row in notes:
            text.append(f'| [`{row["event"]}`]({row["log"]}) | {row["note"]} |')

    errors = [row for row in rows if row['errors']]

    if errors:
        text += [
            '',
            '## Measurement errors',
            '',
            'Statistics use successful rounds only. Failed rounds are retained in the logs.',
            '',
            '| Event | Successful rounds | Errors |',
            '|---|---:|---:|',
        ]

        for row in errors:
            text.append(
                f'| [`{row["event"]}`]({row["log"]}) | ' f'{len(row["skids"])} | {row["errors"]} |'
            )

    text.append('')

    return text
