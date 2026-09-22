# Skid results

* Complete: 23/23
* Potentially deterministic: 14
* Non-deterministic: 6
* Inconclusive: 3

[Processor and settings](profile.md) · [Input events](events.txt)

Skid is extra event occurrences before the Linux process stop.

| Event | Min skid | Max skid | Average skid | Skid determinism |
|---|---:|---:|---:|---|
| [`br_inst_retired.cond_taken:u`](workers/cpu3/event-0004.log) | 5 | 5 | 5.00 | Potentially deterministic |
| [`br_inst_retired.indirect:u`](workers/cpu4/event-0005.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`br_inst_retired.near_call:u`](workers/cpu5/event-0006.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`br_inst_retired.near_return:u`](workers/cpu6/event-0007.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.128b_packed_double:u`](workers/cpu9/event-0010.log) | 3 | 3 | 3.00 | Potentially deterministic |
| [`fp_arith_inst_retired.128b_packed_single:u`](workers/cpu10/event-0011.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.4_flops:u`](workers/cpu11/event-0012.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar_double:u`](workers/cpu13/event-0014.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar_single:u`](workers/cpu14/event-0015.log) | 10 | 10 | 10.00 | Potentially deterministic |
| [`fp_arith_inst_retired.vector:u`](workers/cpu15/event-0016.log) | 10 | 10 | 10.00 | Potentially deterministic |
| [`mem-stores:u`](workers/cpu18/event-0019.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`mem_inst_retired.all_stores:u`](workers/cpu19/event-0020.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`mem_inst_retired.stlb_miss_stores:u`](workers/cpu21/event-0022.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`misc_retired.pause_inst:u`](workers/cpu22/event-0023.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`br_inst_retired.cond:u`](workers/cpu1/event-0002.log) | 20 | 21 | 20.90 | Non-deterministic |
| [`br_inst_retired.cond_ntaken:u`](workers/cpu2/event-0003.log) | 9 | 15 | 13.75 | Non-deterministic |
| [`br_inst_retired.near_taken:u`](workers/cpu7/event-0008.log) | 10 | 12 | 11.45 | Non-deterministic |
| [`fp_arith_inst_retired.scalar:u`](workers/cpu12/event-0013.log) | 9 | 10 | 9.75 | Non-deterministic |
| [`inst_retired.nop:u`](workers/cpu16/event-0017.log) | 57 | 69 | 63.25 | Non-deterministic |
| [`mem_inst_retired.lock_loads:u`](workers/cpu20/event-0021.log) | 0 | 1 | 0.80 | Non-deterministic |
| [`assists.fp:u`](workers/cpu0/event-0001.log) | — | — | — | Inconclusive |
| [`dtlb-stores:u`](workers/cpu8/event-0009.log) | — | — | — | Inconclusive |
| [`l1-dcache-stores:u`](workers/cpu17/event-0018.log) | — | — | — | Inconclusive |

## Measurement notes

| Event | Note |
|---|---|
| [`assists.fp:u`](workers/cpu0/event-0001.log) | too few events to choose an overflow threshold (count: 3; need at least 4) |

## Measurement errors

Statistics use successful rounds only. Failed rounds are retained in the logs.

| Event | Successful rounds | Errors |
|---|---:|---:|
| [`l1-dcache-stores:u`](workers/cpu17/event-0018.log) | 0 | 1 |
| [`dtlb-stores:u`](workers/cpu8/event-0009.log) | 0 | 1 |
