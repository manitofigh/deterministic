# Skid results

* Complete: 18/18
* Potentially deterministic: 0
* Non-deterministic: 0
* Inconclusive: 18

[Processor and settings](profile.md) · [Input events](events.txt)

Skid is extra event occurrences before the Linux process stop.

| Event | Min skid | Max skid | Average skid | Skid determinism |
|---|---:|---:|---:|---|
| [`br_inst_retired.cond:u`](workers/cpu0/event-0001.log) | — | — | — | Inconclusive |
| [`br_inst_retired.cond_ntaken:u`](workers/cpu1/event-0002.log) | — | — | — | Inconclusive |
| [`br_inst_retired.conditional:u`](workers/cpu2/event-0003.log) | — | — | — | Inconclusive |
| [`br_inst_retired.near_call:u`](workers/cpu3/event-0004.log) | — | — | — | Inconclusive |
| [`br_inst_retired.near_return:u`](workers/cpu4/event-0005.log) | — | — | — | Inconclusive |
| [`br_inst_retired.near_taken:u`](workers/cpu5/event-0006.log) | — | — | — | Inconclusive |
| [`br_inst_retired.not_taken:u`](workers/cpu6/event-0007.log) | — | — | — | Inconclusive |
| [`fp_arith_inst_retired.128b_packed_double:u`](workers/cpu7/event-0008.log) | — | — | — | Inconclusive |
| [`fp_arith_inst_retired.128b_packed_single:u`](workers/cpu8/event-0009.log) | — | — | — | Inconclusive |
| [`fp_arith_inst_retired.4_flops:u`](workers/cpu9/event-0010.log) | — | — | — | Inconclusive |
| [`fp_arith_inst_retired.8_flops:u`](workers/cpu10/event-0011.log) | — | — | — | Inconclusive |
| [`fp_arith_inst_retired.scalar:u`](workers/cpu11/event-0012.log) | — | — | — | Inconclusive |
| [`fp_arith_inst_retired.scalar_double:u`](workers/cpu12/event-0013.log) | — | — | — | Inconclusive |
| [`fp_arith_inst_retired.scalar_single:u`](workers/cpu13/event-0014.log) | — | — | — | Inconclusive |
| [`fp_arith_inst_retired.vector:u`](workers/cpu14/event-0015.log) | — | — | — | Inconclusive |
| [`fp_assist.any:u`](workers/cpu15/event-0016.log) | — | — | — | Inconclusive |
| [`inst_retired.nop:u`](workers/cpu16/event-0017.log) | — | — | — | Inconclusive |
| [`mem_inst_retired.lock_loads:u`](workers/cpu17/event-0018.log) | — | — | — | Inconclusive |

## Measurement errors

Statistics use successful rounds only. Failed rounds are retained in the logs.

| Event | Successful rounds | Errors |
|---|---:|---:|
| [`br_inst_retired.cond:u`](workers/cpu0/event-0001.log) | 0 | 1 |
| [`br_inst_retired.cond_ntaken:u`](workers/cpu1/event-0002.log) | 0 | 1 |
| [`fp_arith_inst_retired.8_flops:u`](workers/cpu10/event-0011.log) | 0 | 1 |
| [`fp_arith_inst_retired.scalar:u`](workers/cpu11/event-0012.log) | 0 | 1 |
| [`fp_arith_inst_retired.scalar_double:u`](workers/cpu12/event-0013.log) | 0 | 1 |
| [`fp_arith_inst_retired.scalar_single:u`](workers/cpu13/event-0014.log) | 0 | 1 |
| [`fp_arith_inst_retired.vector:u`](workers/cpu14/event-0015.log) | 0 | 1 |
| [`fp_assist.any:u`](workers/cpu15/event-0016.log) | 0 | 1 |
| [`inst_retired.nop:u`](workers/cpu16/event-0017.log) | 0 | 1 |
| [`mem_inst_retired.lock_loads:u`](workers/cpu17/event-0018.log) | 0 | 1 |
| [`br_inst_retired.conditional:u`](workers/cpu2/event-0003.log) | 0 | 1 |
| [`br_inst_retired.near_call:u`](workers/cpu3/event-0004.log) | 0 | 1 |
| [`br_inst_retired.near_return:u`](workers/cpu4/event-0005.log) | 0 | 1 |
| [`br_inst_retired.near_taken:u`](workers/cpu5/event-0006.log) | 0 | 1 |
| [`br_inst_retired.not_taken:u`](workers/cpu6/event-0007.log) | 0 | 1 |
| [`fp_arith_inst_retired.128b_packed_double:u`](workers/cpu7/event-0008.log) | 0 | 1 |
| [`fp_arith_inst_retired.128b_packed_single:u`](workers/cpu8/event-0009.log) | 0 | 1 |
| [`fp_arith_inst_retired.4_flops:u`](workers/cpu9/event-0010.log) | 0 | 1 |
