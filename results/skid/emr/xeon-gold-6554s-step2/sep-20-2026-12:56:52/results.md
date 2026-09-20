# Skid results

* Complete: 22/22
* Potentially deterministic: 15
* Non-deterministic: 7
* Inconclusive: 0

[Processor and settings](profile.md) · [Input events](events.txt)

Skid is extra event occurrences before the Linux process stop.

| Event | Min skid | Max skid | Average skid | Skid determinism |
|---|---:|---:|---:|---|
| [`br_inst_retired.cond:u`](workers/cpu70/event-0001.log) | 21 | 21 | 21.00 | Potentially deterministic |
| [`br_inst_retired.cond_taken:u`](workers/cpu70/event-0003.log) | 5 | 5 | 5.00 | Potentially deterministic |
| [`br_inst_retired.indirect:u`](workers/cpu70/event-0004.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`br_inst_retired.near_call:u`](workers/cpu70/event-0005.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`br_inst_retired.near_return:u`](workers/cpu70/event-0006.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`cpu_clk_unhalted.c0_wait:u`](workers/cpu70/event-0008.log) | 32 | 32 | 32.00 | Potentially deterministic |
| [`cpu_clk_unhalted.pause:u`](workers/cpu70/event-0009.log) | 32 | 32 | 32.00 | Potentially deterministic |
| [`cpu_clk_unhalted.pause_inst:u`](workers/cpu70/event-0010.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.128b_packed_single:u`](workers/cpu70/event-0012.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.4_flops:u`](workers/cpu70/event-0013.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar_double:u`](workers/cpu70/event-0015.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`fp_arith_inst_retired.vector:u`](workers/cpu70/event-0017.log) | 10 | 10 | 10.00 | Potentially deterministic |
| [`int_vec_retired.128bit:u`](workers/cpu70/event-0019.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`int_vec_retired.add_128:u`](workers/cpu70/event-0020.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`misc2_retired.lfence:u`](workers/cpu70/event-0022.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`br_inst_retired.cond_ntaken:u`](workers/cpu70/event-0002.log) | 11 | 13 | 12.20 | Non-deterministic |
| [`br_inst_retired.near_taken:u`](workers/cpu70/event-0007.log) | 6 | 16 | 10.00 | Non-deterministic |
| [`fp_arith_inst_retired.128b_packed_double:u`](workers/cpu70/event-0011.log) | 1 | 3 | 2.80 | Non-deterministic |
| [`fp_arith_inst_retired.scalar:u`](workers/cpu70/event-0014.log) | 9 | 13 | 10.80 | Non-deterministic |
| [`fp_arith_inst_retired.scalar_single:u`](workers/cpu70/event-0016.log) | 10 | 12 | 10.40 | Non-deterministic |
| [`inst_retired.nop:u`](workers/cpu70/event-0018.log) | 57 | 69 | 63.20 | Non-deterministic |
| [`mem_inst_retired.lock_loads:u`](workers/cpu70/event-0021.log) | 0 | 1 | 0.90 | Non-deterministic |
