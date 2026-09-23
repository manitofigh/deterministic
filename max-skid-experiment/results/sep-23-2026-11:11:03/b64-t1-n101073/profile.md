# Processor profile

- Started: 2026-09-23T11:12:07-04:00
- Processor: Intel(R) Xeon(R) Gold 6338N CPU @ 2.20GHz
- Microarchitecture/event family: `icx`
- CPU family/model: 6/0x6a
- Stepping: 6
- Mode: skid
- Worker CPUs: [0]
- Reserved coordinator CPU: 63
- SMT: verified disabled or not supported
- Rounds: 100
- Events: 1
- Per-round timeout: 120 seconds
- Benchmark: `/home/mani/dev/Laplace/deterministic/max-skid-experiment/build/branch-sled-p3125-l65536-b64-t1`
- Input: `br_inst_retired.cond`

Results describe this run, not all processors with the same name.

Skid is measured from counter enable at the exec stop to the overflow signal-delivery stop, before a user signal handler runs. Only benchmark user-space events are counted. This includes the Linux delivery path; it is not hardware interrupt latency alone.

Overflow threshold: 101073. The selected overflow threshold and counter encoding are saved for each event.
