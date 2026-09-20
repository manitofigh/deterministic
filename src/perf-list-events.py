"""capture perf's event list and keep candidates for user-only counting."""

from collections import Counter
import csv
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

# avoid root-owned bytecode files when running with sudo.
sys.dont_write_bytecode = True

from machine import identify
from messages import Parser, message
from permissions import user_owned_outputs


SPECIAL = {
    'mem-loads': 'needs load-latency sampling setup',
    'rob_misc_events.lbr_inserts': 'needs LBR recording enabled',
    'cpu_clk_unhalted.ring0_trans': 'counts transitions into the kernel',
    'hw_interrupts.received': 'counts external interrupts',
    'tlb_flush.dtlb_thread': 'counts privileged TLB flushes',
    'tlb_flush.stlb_any': 'counts privileged TLB flushes',
    'itlb.itlb_flush': 'counts TLB flushes',
}
EXCLUDED_TYPES = {
    'Software event', 'Tracepoint event', 'Tool event',
    'Raw hardware event descriptor', 'Hardware breakpoint',
    'Raw event descriptor', 'Hwmon event',
}
CORE_TYPES = {'Hardware event', 'Hardware cache event', 'Kernel PMU event'}


def classify(event):
    name = event.get('EventName', '')
    kind = event.get('EventType', '')
    unit = event.get('Unit', '')
    description = ' '.join(event.get(key, '') for key in
                           ('BriefDescription', 'PublicDescription')).lower()
    encoding = event.get('Encoding', '').lower()
    if not name and event.get('MetricName'):
        return 'excluded', 'derived metric'
    if not name or not kind:
        raise ValueError(f'cannot classify record: {event}')
    if kind in EXCLUDED_TYPES:
        return 'excluded', kind.lower()
    if kind not in CORE_TYPES:
        raise ValueError(f'unknown event type for {name}: {kind}')
    if unit.startswith('uncore') or name.lower().startswith(('unc_', 'uncore_')):
        return 'excluded', 'uncore event'
    if unit not in ('', 'cpu', 'default_core'):
        return 'excluded', f'outside the supported core PMU: {unit}'
    if kind == 'Kernel PMU event' and not unit:
        raise ValueError(f'missing PMU name for {name}')
    if name.lower().startswith(('offcore', 'ocr.')) or 'offcore_rsp=' in encoding:
        return 'excluded', 'offcore event'
    if str(event.get('Deprecated', '0')).lower() in ('1', 'true'):
        return 'excluded', 'deprecated event'
    if name.startswith('topdown-'):
        return 'deferred', 'requires an event group led by slots'
    if name.startswith(('LLC-', 'node-')):
        return 'deferred', 'check whether this alias maps to offcore activity'
    if 'must be precise' in description:
        return 'deferred', 'requires precise sampling'
    if name.startswith('frontend_retired.') or 'frontend=' in encoding:
        return 'deferred', 'needs frontend filtering setup'
    if 'ldlat=' in encoding:
        return 'deferred', 'needs load-latency sampling setup'
    if name in SPECIAL:
        return 'deferred', SPECIAL[name]
    if name.startswith('ept.'):
        return 'deferred', 'counts guest address translation activity'
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]*', name):
        return 'deferred', 'needs syntax beyond a plain name followed by :u'
    return 'included', 'core event'


def select(records):
    if not isinstance(records, list) or not records:
        raise ValueError('expected a nonempty JSON list from perf')
    rows = {}
    for event in records:
        if not isinstance(event, dict):
            raise ValueError('expected an event object in the perf JSON list')
        status, reason = classify(event)
        name = event.get('EventName') or event['MetricName']
        key = ('event' if event.get('EventName') else 'metric', name)
        row = (name, status, reason)
        if key in rows and rows[key] != row:
            raise ValueError(f'conflicting definitions for {name}')
        rows[key] = row
    if not any(row[1] == 'included' for row in rows.values()):
        raise ValueError('no usable core events found')
    return list(rows.values())


def main():
    parser = Parser(description=__doc__)
    parser.add_argument('--output', type=Path, help='event file (default: events/intel/<microarch>/events.txt)')
    parser.add_argument('--input', type=Path, help='read saved perf JSON instead of capturing it')
    args = parser.parse_args()
    if args.output is None:
        args.output = (Path(__file__).resolve().parents[1] / 'events/intel' /
                       identify()['microarch'] / 'events.txt')
    args.output = args.output.resolve()
    if args.output.exists():
        raise ValueError(f'event list already exists: {args.output}')
    outputs = [args.output] + [args.output.with_suffix(suffix) for suffix in (
        '.perf-list.json', '.perf-list.stderr', '.deferred.txt',
        '.exclusions.tsv', '.summary.txt')]
    with user_owned_outputs(outputs):
        args.output.parent.mkdir(parents=True, exist_ok=True)
        raw_path = args.output.with_suffix('.perf-list.json')
        stderr_path = args.output.with_suffix('.perf-list.stderr')
        if args.input:
            raw = args.input.read_text()
            raw_path.write_text(raw)
        else:
            result = subprocess.run(['perf', 'list', '--json'], capture_output=True, text=True,
                                    env={**os.environ, 'LC_ALL': 'C', 'PERF_PAGER': 'cat'},
                                    timeout=60)
            raw = result.stdout
            stderr_path.write_text(result.stderr)
            raw_path.write_text(raw)
            if result.returncode or result.stderr.strip():
                raise ValueError(f'perf list failed or reported a problem; see '
                                 f'{stderr_path}; '
                                 'use sudo and a perf version that supports --json')
        rows = select(json.loads(raw))
        args.output.with_suffix('.deferred.txt').write_text(
            ''.join(name + '\n' for name, choice, _ in rows if choice == 'deferred'))
        with args.output.with_suffix('.exclusions.tsv').open('w') as file:
            writer = csv.writer(file, delimiter='\t', lineterminator='\n')
            writer.writerow(['name', 'status', 'reason'])
            writer.writerows(row for row in rows if row[1] != 'included')
        counts = Counter(row[1] for row in rows)
        summary = f'{len(rows)} unique entries: ' + ', '.join(
            f'{counts[status]} {status}' for status in ('included', 'excluded', 'deferred'))
        args.output.with_suffix('.summary.txt').write_text(summary + '\n')
        # don't let the runner read a list that is only partly written.
        with tempfile.NamedTemporaryFile(mode='w', dir=args.output.parent, delete=False) as file:
            temporary = Path(file.name)
            try:
                file.write(''.join(name + '\n' for name, choice, _ in rows if choice == 'included'))
                file.close()
                os.link(temporary, args.output)
            finally:
                temporary.unlink()
    message('+', f'{summary}; saved to {args.output}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        message('~', 'interrupted; the capture may be incomplete')
        sys.exit(130)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        message('-', str(error))
        sys.exit(1)
