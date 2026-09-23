#!/usr/bin/env python3
"""Run the branch-sled matrix in one dated experiment directory."""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / 'src'))
from permissions import user_owned_outputs

SETUP_ITERATIONS = 3125
SETUP_BRANCH_COUNT = SETUP_ITERATIONS * 32  # 31 repeated branches and one loop branch
SLED_PASSES = 2000
WIDTHS = (64, 256, 1024)
TAKEN = (0, 1)
MONTHS = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')


def thresholds(width):
    threshold_after_16_sled_passes = SETUP_BRANCH_COUNT + 16 * (width + 1) + 1
    return (
        SETUP_BRANCH_COUNT + 1,
        SETUP_BRANCH_COUNT + 2,
        SETUP_BRANCH_COUNT + 8,
        SETUP_BRANCH_COUNT + 32,
        threshold_after_16_sled_passes,
        threshold_after_16_sled_passes + width // 2,
        threshold_after_16_sled_passes + width - 1,
    )


def new_experiment_directory():
    parent = HERE / 'results'
    parent.mkdir(exist_ok=True)

    while True:
        now = datetime.now().astimezone()
        name = f'{MONTHS[now.month - 1]}-{now:%d-%Y-%H:%M:%S}'
        candidate = parent / name

        try:
            candidate.mkdir()
            return candidate, now
        except FileExistsError:
            time.sleep(1)


def result_row(case, directory, exit_code):
    paths = sorted(directory.glob('workers/cpu*/results.jsonl'))
    rows = [
        json.loads(line)
        for path in paths
        for line in path.read_text().splitlines(keepends=True)
        if line.endswith('\n')
    ]
    measurements = [
        measurement
        for row in rows
        for measurement in row.get('measurements', [])
        if 'skid' in measurement
    ]
    skids = [measurement['skid'] for measurement in measurements]

    return {
        'case': case,
        'exit_code': exit_code,
        'successes': len(skids),
        'min': min(skids) if skids else None,
        'max': max(skids) if skids else None,
        'average': sum(skids) / len(skids) if skids else None,
        'peak': max(measurements, key=lambda item: item['skid']) if skids else None,
        'report': f'{case}/results.md' if (directory / 'results.md').is_file() else f'{case}/runner.log',
    }


def write_report(root, started, rounds, core, rows):
    lines = [
        '# Branch sled skid experiment',
        '',
        f'- Started: {started.isoformat(timespec="seconds")}',
        '- Event: `br_inst_retired.cond:u`',
        f'- Worker CPU: {core}',
        f'- Rounds per series: {rounds}',
        f'- Sled passes: {SLED_PASSES}',
        '',
        '| Branches per pass | Taken | Overflow | Successful | Min | Max | Average | Series |',
        '|---:|---:|---:|---:|---:|---:|---:|---|',
    ]

    for row in rows:
        width, taken, threshold = row['case'].split('-')
        minimum = '—' if row['min'] is None else str(row['min'])
        maximum = '—' if row['max'] is None else str(row['max'])
        average = '—' if row['average'] is None else f'{row["average"]:.2f}'
        lines.append(
            f'| {width[1:]} | {"yes" if taken == "t1" else "no"} | {threshold[1:]} '
            f'| {row["successes"]}/{rounds} | {minimum} | {maximum} '
            f'| {average} | [{row["case"]}]({row["report"]}) |'
        )

    peaks = [row for row in rows if row['peak']]

    if peaks:
        winner = max(peaks, key=lambda row: row['max'])
        peak = winner['peak']
        lines += [
            '',
            f'Largest observed skid: **{winner["max"]}** extra branches in '
            f'[{winner["case"]}]({winner["report"]}), round {peak["round"]}, '
            f'stop IP `{peak["ip"]}`.',
        ]

    if any(row['exit_code'] or row['successes'] != rounds for row in rows):
        lines += ['', 'Some series failed or had incomplete rounds; inspect their series links.']

    report = root / 'results.md'
    temporary = root / 'results.md.tmp'
    temporary.write_text('\n'.join(lines) + '\n')
    temporary.replace(report)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rounds', type=int, default=100, help='rounds per series (default: 100)')
    parser.add_argument('--pin-core', type=int, default=0, help='worker CPU (default: 0)')
    args = parser.parse_args()

    if args.rounds < 2:
        parser.error('--rounds must be at least 2')

    if args.pin_core < 0:
        parser.error('--pin-core must be nonnegative')

    if os.geteuid() != 0:
        parser.error('run with sudo to access performance counters')

    root, started = new_experiment_directory()
    rows = []

    with user_owned_outputs([root, HERE / 'build']):
        try:
            for taken in TAKEN:
                for width in WIDTHS:
                    subprocess.run(
                        [
                            'make', '-C', str(HERE),
                            f'SETUP_ITERATIONS={SETUP_ITERATIONS}',
                            f'SLED_PASSES={SLED_PASSES}', f'BRANCHES_PER_SLED_PASS={width}',
                            f'REPEATED_BRANCHES_TAKEN={taken}',
                        ],
                        check=True,
                        stdout=subprocess.DEVNULL,
                    )
                    binary = HERE / 'build' / f'branch-sled-setup{SETUP_ITERATIONS}-passes{SLED_PASSES}-branches{width}-taken{taken}'

                    for threshold in thresholds(width):
                        case = f'b{width}-t{taken}-n{threshold}'
                        command = [
                            sys.executable, str(REPO / 'src/run.py'),
                            '--mode', 'skid', '--event', 'br_inst_retired.cond',
                            '--benchmark', str(binary), '--overflow', str(threshold),
                            '--rounds', str(args.rounds), '--cores', '1',
                            '--start-core', str(args.pin_core), '--output', str(root),
                        ]
                        existing = set(root.iterdir())
                        try:
                            result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
                        except KeyboardInterrupt:
                            result = None

                        output = result.stdout + result.stderr if result else 'Sweep interrupted during this series.\n'
                        match = re.search(r'^Results: (.+)$', result.stdout, re.MULTILINE) if result else None
                        directory = root / case

                        if match and Path(match.group(1)).is_dir():
                            Path(match.group(1)).rename(directory)
                        else:
                            # An interrupted runner may have created its dated output before printing Results.
                            created = [path for path in root.iterdir() if path.is_dir() and path not in existing]
                            if len(created) == 1:
                                created[0].rename(directory)
                            else:
                                directory.mkdir()

                        (directory / 'runner.log').write_text(output)
                        row = result_row(case, directory, result.returncode if result else 130)
                        rows.append(row)
                        print(f'{case} max skid: {row["max"] if row["max"] is not None else "n/a"}', flush=True)
                        write_report(root, started, args.rounds, args.pin_core, rows)
                        if result is None:
                            raise KeyboardInterrupt
        finally:
            write_report(root, started, args.rounds, args.pin_core, rows)

    print(f'Results: {root / "results.md"}')
    return int(any(row['exit_code'] or row['successes'] != args.rounds for row in rows))


if __name__ == '__main__':
    sys.exit(main())
