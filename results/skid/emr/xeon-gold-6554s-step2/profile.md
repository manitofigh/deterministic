# Processor profile

- Processor: INTEL(R) XEON(R) GOLD 6554S
- Microarchitecture/event family: `emr`
- CPU family/model: 6/0xcf
- Stepping: 2
- Mode: skid
- Worker CPUs: [0]
- Reserved coordinator CPU: 71
- SMT: verified disabled or not supported
- Rounds: 10
- Events: 22
- Per-round timeout: 120 seconds
- Benchmark: `/home/mani/dev/Laplace/deterministic/static/binaries/retired_instr.all.x86_64`
- Input: `/home/mani/dev/Laplace/deterministic/results/emr/xeon-gold-6554s-step2`

Results describe this run, not all processors with the same name.

Skid is measured from counter enable at the exec stop to the overflow signal-delivery stop, before a user signal handler runs. Only benchmark user-space events are counted. This includes the Linux delivery path; it is not hardware interrupt latency alone.

Period: half the preliminary count, capped at 1000000. The selected period and counter encoding are saved for each event.
