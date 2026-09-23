#!/usr/bin/env python3
"""Summarize saved branch-sled runs and identify the largest observed skid."""

import argparse
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'experiment', nargs='?', type=Path,
        default=Path(__file__).resolve().parent / 'results',
        help='one dated experiment directory (default: all saved experiments)',
    )
    root = parser.parse_args().experiment
    rows = []

    for path in sorted(root.rglob('results.jsonl')):
        case = next(
            (parent.name for parent in path.parents if re.fullmatch(r'b\d+-t[01]-n\d+', parent.name)),
            path.parents[2].name,
        )

        for line in path.read_text().splitlines():
            row = json.loads(line)
            measurements = [item for item in row['measurements'] if 'skid' in item]

            if not measurements:
                print(f'{case}\t0/{row["runs"]}\tno successful rounds')
                continue

            skids = [item['skid'] for item in measurements]
            peak = max(measurements, key=lambda item: item['skid'])
            rows.append((peak['skid'], case, path, peak))
            print(
                f'{case}\t{len(skids)}/{row["runs"]}\t'
                f'min={min(skids)} max={max(skids)} '
                f'avg={sum(skids) / len(skids):.2f}'
            )

    if rows:
        maximum, case, path, measurement = max(rows, key=lambda item: item[0])
        print(
            f'Largest observed skid: {maximum} in {case}, '
            f'round {measurement["round"]}, stop IP {measurement["ip"]}\n'
            f'Result file: {path}'
        )
    else:
        print(f'No successful skid measurements under {root}')


if __name__ == '__main__':
    main()
