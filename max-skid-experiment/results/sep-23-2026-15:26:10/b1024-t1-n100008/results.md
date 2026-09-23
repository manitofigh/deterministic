# Skid results

* Complete: 1/1
* Potentially deterministic: 0
* Non-deterministic: 1
* Inconclusive: 0

[Processor and settings](profile.md) · [Input events](events.txt)

Skid is extra event occurrences before the Linux process stop.

| Event | Min skid | Max skid | Average skid | Skid determinism |
|---|---:|---:|---:|---|
| [`br_inst_retired.cond:u`](workers/cpu0/event-0001.log) | 2 | 3 | 2.09 | Non-deterministic |
