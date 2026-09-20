# Processor profile

- Processor: INTEL(R) XEON(R) GOLD 6554S
- Microarchitecture/event family: `emr`
- CPU family/model: 6/0xcf
- Stepping: 2
- Mode: skid
- Worker CPUs: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
- Reserved coordinator CPU: 71
- SMT: verified disabled or not supported
- Rounds: 10
- Events: 1
- Per-round timeout: 120 seconds
- Benchmark: `/home/mani/dev/Laplace/deterministic/static/binaries/retired_instr.all.x86_64`
- Input: `br_inst_retired.cond`

Results describe this run, not all processors with the same name.

Skid is measured from counter enable at the exec stop to the overflow signal-delivery stop, before a user signal handler runs. Only benchmark user-space events are counted. This includes the Linux delivery path; it is not hardware interrupt latency alone.

Overflow threshold: 520008. The selected overflow threshold and counter encoding are saved for each event.

Migration: original folder `results/skid/emr/xeon-gold-6554s-step2-3`. The dated folder uses the previous `profile.md` modification time (2026-09-20T17:57:31-04:00); the original experiment start time was not recorded.
