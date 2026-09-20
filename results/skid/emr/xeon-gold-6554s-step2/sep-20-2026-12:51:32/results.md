# Skid results

* Interrupted or failed: 8/22
* Potentially deterministic: 6
* Non-deterministic: 2
* Inconclusive: 0

[Processor and settings](profile.md) · [Input events](events.txt)

Skid is extra event occurrences before the Linux process stop.

| Event | Min skid | Max skid | Average skid | Skid determinism |
|---|---:|---:|---:|---|
| [`br_inst_retired.cond:u`](workers/cpu0/event-0001.log) | 21 | 21 | 21.00 | Potentially deterministic |
| [`br_inst_retired.cond_taken:u`](workers/cpu0/event-0003.log) | 5 | 5 | 5.00 | Potentially deterministic |
| [`br_inst_retired.indirect:u`](workers/cpu0/event-0004.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`br_inst_retired.near_call:u`](workers/cpu0/event-0005.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`br_inst_retired.near_return:u`](workers/cpu0/event-0006.log) | 0 | 0 | 0.00 | Potentially deterministic |
| [`cpu_clk_unhalted.c0_wait:u`](workers/cpu0/event-0008.log) | 32 | 32 | 32.00 | Potentially deterministic |
| [`br_inst_retired.cond_ntaken:u`](workers/cpu0/event-0002.log) | 11 | 13 | 11.20 | Non-deterministic |
| [`br_inst_retired.near_taken:u`](workers/cpu0/event-0007.log) | 6 | 16 | 11.50 | Non-deterministic |
