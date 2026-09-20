# Skid results

* Complete: 18/18
* Potentially deterministic: 12
* Non-deterministic: 5
* Inconclusive: 1

[Processor and settings](profile.md) · [Input events](events.txt)

Skid is extra event occurrences before the Linux process stop.

| Event | Min skid | Max skid | Average skid | Skid determinism |
|---|---:|---:|---:|---|
| [`br_inst_retired.near_call:u`](workers/cpu3/event-0004.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`br_inst_retired.near_return:u`](workers/cpu4/event-0005.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.128b_packed_double:u`](workers/cpu7/event-0008.log) | 3 | 3 | 3.00 | Potentially deterministic |
| [`fp_arith_inst_retired.128b_packed_single:u`](workers/cpu8/event-0009.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.4_flops:u`](workers/cpu9/event-0010.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.8_flops:u`](workers/cpu10/event-0011.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar:u`](workers/cpu11/event-0012.log) | 9 | 9 | 9.00 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar_double:u`](workers/cpu12/event-0013.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar_single:u`](workers/cpu13/event-0014.log) | 9 | 9 | 9.00 | Potentially deterministic |
| [`fp_arith_inst_retired.vector:u`](workers/cpu14/event-0015.log) | 10 | 10 | 10.00 | Potentially deterministic |
| [`inst_retired.nop:u`](workers/cpu16/event-0017.log) | 48 | 48 | 48.00 | Potentially deterministic |
| [`mem_inst_retired.lock_loads:u`](workers/cpu17/event-0018.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`br_inst_retired.cond:u`](workers/cpu0/event-0001.log) | 20 | 21 | 20.70 | Non-deterministic |
| [`br_inst_retired.cond_ntaken:u`](workers/cpu1/event-0002.log) | 9 | 11 | 9.40 | Non-deterministic |
| [`br_inst_retired.conditional:u`](workers/cpu2/event-0003.log) | 20 | 21 | 20.80 | Non-deterministic |
| [`br_inst_retired.near_taken:u`](workers/cpu5/event-0006.log) | 8 | 11 | 9.60 | Non-deterministic |
| [`br_inst_retired.not_taken:u`](workers/cpu6/event-0007.log) | 9 | 11 | 9.70 | Non-deterministic |
| [`fp_assist.any:u`](workers/cpu15/event-0016.log) | — | — | — | Inconclusive |

## Measurement notes

| Event | Note |
|---|---|
| [`fp_assist.any:u`](workers/cpu15/event-0016.log) | too few events to choose an overflow period (count: 3; need at least 4) |
