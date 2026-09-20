import contextlib
import os
from pathlib import Path
import re


CPU_ROOT = Path('/sys/devices/system/cpu')
SERVER_MODELS = {
    0x6A: 'icx', 0x6C: 'icx', 0x8F: 'spr', 0xCF: 'emr',
    0xAD: 'gnr', 0xAE: 'gnr', 0xAF: 'srf', 0xDD: 'cwf',
}


def cpu_list(text):
    cpus = set()
    for part in text.strip().split(','):
        if not part:
            continue
        bounds = [int(value) for value in part.split('-')]
        cpus.update(range(bounds[0], bounds[-1] + 1))
    return cpus


def identify():
    records = []
    for block in Path('/proc/cpuinfo').read_text().strip().split('\n\n'):
        records.append(dict(line.split(':', 1) for line in block.splitlines()
                            if ':' in line))
    records = [{key.strip(): value.strip() for key, value in row.items()}
               for row in records]
    allowed = os.sched_getaffinity(0)
    rows = [row for row in records if int(row['processor']) in allowed]
    identities = {(row['vendor_id'], row['cpu family'], row['model'],
                   row['stepping'], row['model name']) for row in rows}
    if len(identities) != 1:
        raise ValueError('expected one homogeneous processor model')
    vendor, family, model, stepping, name = identities.pop()
    if vendor != 'GenuineIntel' or int(family) != 6:
        raise ValueError('this runner currently supports Intel family 6 servers')
    if any('hypervisor' in row.get('flags', '').split() for row in rows):
        raise ValueError('physical-core and host SMT control require bare metal')
    microarch = SERVER_MODELS.get(int(model))
    if int(model) == 0x55:
        microarch = 'skx' if int(stepping) <= 4 else 'clx'
    if not microarch:
        raise ValueError(f'no microarchitecture mapping for CPU model {model}')
    clean = re.sub(r'\(R\)|\(TM\)', '', name, flags=re.I)
    clean = re.sub(r'\bIntel\b|\bCPU\b|\bProcessor\b', '', clean, flags=re.I)
    slug = re.sub(r'[^a-z0-9]+', '-', clean.split('@')[0].lower()).strip('-')
    return dict(model=name, microarch=microarch, family=int(family),
                model_id=int(model), stepping=int(stepping), slug=slug)


@contextlib.contextmanager
def smt_disabled():
    control = CPU_ROOT / 'smt/control'
    original = control.read_text().strip() if control.exists() else None
    changed = original == 'on'
    try:
        if changed:
            control.write_text('off\n')
        active = CPU_ROOT / 'smt/active'
        if active.exists() and active.read_text().strip() != '0':
            raise ValueError('SMT is still active; refusing to run')
        yield
    finally:
        if changed:
            control.write_text('on\n')


def select_cores(allowed, requested, start=None):
    online = cpu_list((CPU_ROOT / 'online').read_text())
    cores = {}
    for cpu in sorted(online & allowed):
        topology = CPU_ROOT / f'cpu{cpu}/topology'
        siblings = cpu_list((topology / 'thread_siblings_list').read_text())
        if len(siblings & online) != 1:
            raise ValueError(f'CPU {cpu} still has an online SMT sibling')
        socket = int((topology / 'physical_package_id').read_text())
        core = int((topology / 'core_id').read_text())
        cores.setdefault((socket, core), cpu)
    cpus = sorted(cores.values())
    if len(cpus) < 2:
        raise ValueError('need two physical cores: a worker and a reserved core')
    available = cpus if start is None else [cpu for cpu in cpus if cpu >= start]
    maximum = min(len(available), len(cpus) - 1)
    if maximum == 0:
        raise ValueError(f'no available worker CPUs starting at {start}')
    count = requested if requested is not None else maximum
    if not 1 <= count <= maximum:
        raise ValueError(f'--cores must be between 1 and {maximum} for this selection')
    workers = available[:count] if start is None else list(range(start, start + count))
    missing = sorted(set(workers) - set(cpus))
    if missing:
        raise ValueError(f'requested worker CPUs are unavailable: {missing}')
    reserve = max(cpu for cpu in cpus if cpu not in workers)
    return workers, reserve
