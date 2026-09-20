# Processor profile

- Processor: Intel(R) Xeon(R) Silver 4114 CPU @ 2.20GHz
- Microarchitecture/event family: `skx`
- CPU family/model: 6/0x55
- Stepping: 4
- Mode: skid
- Worker CPUs: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
- Reserved coordinator CPU: 19
- SMT: verified disabled or not supported
- Rounds: 10
- Events: 18
- Per-round timeout: 120 seconds
- Benchmark: `/users/moneytea/dev/Laplace/deterministic/static/binaries/retired_instr.all.x86_64`
- Original input path: `/users/moneytea/dev/Laplace/deterministic/results/skx/xeon-silver-4114-step4-3`
- Source count run: [results](../../../../counts/skx/xeon-silver-4114-step4/sep-20-2026-10:11:00/results.md)

Results describe this run, not all processors with the same name.

Skid is measured from counter enable at the exec stop to the overflow signal-delivery stop, before a user signal handler runs. Only benchmark user-space events are counted. This includes the Linux delivery path; it is not hardware interrupt latency alone.

Period: half the preliminary count, capped at 1000000. The selected period and counter encoding are saved for each event.

Migration: original folder `results/skid/skx/xeon-silver-4114-step4`. The dated folder uses the previous `profile.md` modification time (2026-09-20T14:27:40-04:00); the original experiment start time was not recorded.
