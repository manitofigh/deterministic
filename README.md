# Finding Deterministic PMU Events

The goal is to find PMU events that behave deterministically. That is, if we run a
program 1000x and record a hardware event `abc`, the final recorded count on `abc` must
always be the same, given the same program.

This script runs the same core asm program repeatedly and checks whether each event returns the
same count. The default is 10 rounds per event; counting stops as soon as two counts differ.
Some events only prove non-deterministic when testing 100+ rounds.

The core asm tests are from [Vince Weaver's original deterministic repo](https://github.com/deater/deterministic).

**Support**: Currently for Intel processors only.

## Running

```bash
sudo python3 src/run.py
```

Run on a Linux machine. Also, python 3.9+ and `perf` are needed; install them using your distribution package manager if missing.

build the benchmark with `make -C static binaries/retired_instr.all.x86_64`. that needs `make` and the GNU assembler/linker.
If you place the binary elsewhere, you can provide its path using `--benchmark static/binaries/retired_instr.all.x86_64`.

### Options
All of these are optional.
| option | what it does |
|---|---|
| `--mode count\|skid` | Count determinism or overflow skid. Default: count. |
| `--cores N` | Number of physical cores used by workers. Default: all available physical cores minus one, or one worker with `--event`. The coordinator stays on a separate core. |
| `--start-core N` | First worker CPU number. For example, `--cores 10 --start-core 10` selects CPUs 10 through 19. Unavailable ranges are rejected. |
| `--rounds N` | Default: 10, minimum: 2. Counting stops when counts differ; skid mode runs every round. |
| `--output PATH` | Save a dated run under this directory. Without it, a single-event skid check only prints to the terminal. Other runs use the default results layout. |
| `--events PATH` | Would be generated if non-existent; one can however provide their own list of events by putting each event on a separate line. |
| `--event NAME` | Test one event, optionally ending in `:u`. |
| `--from-results PATH` | In skid mode, select potentially deterministic events from a previous count run. Default: detect count results for this CPU. |
| `--overflow N` | In skid mode, request overflow after N events. Default: half a preliminary count, capped at 1,000,000. Allowed range: 2 through 2,147,483,647. |
| `--benchmark PATH` | Uses the executable by Weaver et al. by default. |
| `--timeout SECONDS` | Stops a measurement that takes too long. Default is 120s / round. |

Also, relative paths you provide are relative to where you run the command.
The default event list, benchmark and results directory are located relative to this project, so the python script also works when called from another directory.

## Few things

* The script disables SMT and restores it once done (if it was enabled)
* The script uses `all_available_physical_cores - 1` by default and
distributes one worker thread per physical core, each with its own list
of events to test. If you don't care about the process ending faster and
want more available cores instead, you can limit this using `--cores 1`.
* What is marked "Potentially deterministic", is not necessarily deterministic,
and thus the key word "_potentially_". There is truly no way to know if some
hardware counter is deterministic. Hardware determinism, in this case, is
simply the trust gained through dozens/hundreds/thousands/millions of tests,
without anything ever differing in result.
* CPU names use Intel's [perfmon mapping](https://github.com/intel/perfmon/blob/main/mapfile.csv).
The code recognizes skx, clx, icx, spr, emr, gnr, srf and cwf. On another supported CPU family,
the runner captures its list if missing. you can also provide an explicit `--events` file
(if you have a specific list of events you want to test for determinism).
* The list of events that are useful for analysis are automatically extracted based on `perf list`'s output
on the running machine. If you have a specific list of events, just place them in a `events.txt` file
and the script would automatically use that instead.

## Reading the results

Count results go under `results/counts/<microarch>/<processor-model>-step<stepping>/<date>/`.
Skid results use the same layout under `results/skid/`.
Each processor has one directory, with a separate dated folder for each run:

```text
results/
  counts/emr/xeon-gold-6554s-step2/sep-20-2026-18:01:54/
  skid/emr/xeon-gold-6554s-step2/sep-20-2026-18:05:12/
```

Dates use local time, lowercase English month names, and a 24-hour clock.
If a folder already exists for the current second, the runner warns and waits for
the next second. Existing runs are never overwritten. Migrated older runs use
file timestamps where their original start time was not recorded; their profiles
explain this.

Based on the arch/uarch that the script is ran on, the results are written under its relevant dir name.
There, you can see a beautifully-put-together `results.md` file containing the table of results.
The event names link to logs containing the assigned CPU, benchmark stderr, parsed counts and the final result. Benchmark stdout is discarded. The runs column says how many rounds we actually attempted, including the round that first differed or failed.

| result | meaning |
|---|---|
| potentially deterministic | every requested round returned the same nonzero count. |
| non-deterministic | a successful round returned a different count. no more rounds are needed. |
| zero-only | every round returned zero (could be that the necessary instructions to increment those events were not even used in the asm benchmark)|
| error | the command failed, timed out, or didn't provide a count. |

The potentially deterministic events are placed on the top rows, and then the non-deterministic ones.
Zero-only events and errors have their own separate sections in the very bottom of the `results.md` file.

## Measuring skid

Give `--overflow N` to request a counter overflow after N events. The helper
starts counting when the benchmark begins, waits for the overflow signal to
stop it, then reads the counter. **Skid = count at stop - N.** The counter
tracks the benchmark's user-space events. With `br_inst_retired.cond`, skid
counts extra retired conditional branches.

```bash
sudo python3 src/run.py --mode skid --event br_inst_retired.cond --overflow 100000 --rounds 100
```

Skid mode also needs `cc` and Linux C headers to build its counter helper.

By default, the script finds the newest count run for this CPU and tests its
potentially deterministic events. It counts the whole benchmark once to
choose a threshold for each event. Use `--event NAME`, `--events PATH`, or
`--from-results PATH` to choose the events yourself. Use `--overflow N` to
choose the threshold.

Each round starts a new benchmark. Skid mode runs every requested round. It
reports the minimum, maximum, and average skid. Two different skids make the
result "Non-deterministic". If every requested round succeeds with the same
skid, the result is "Potentially deterministic". The remaining cases are
"Inconclusive".

A single `--event` check prints to the terminal. Add `--output PATH` to save it
under `PATH/<date>/`. Other skid runs use
`results/skid/<microarch>/<processor-model>-step<stepping>/<date>/`. The saved
report links to each round's threshold, count, skid, and stopped instruction
address. A zero skid means no further events of that type were counted; the
benchmark may still have run for more cycles. The maximum records the largest
skid seen in that run. Further runs may exceed it.

## Max skid experiment

The branch sled places the overflow at known conditional branches, then gives
the CPU more branches to retire before the process stops. The sweep tests
three sled widths, taken and untaken branches, and seven overflow thresholds.

```bash
bash max-skid-experiment/run-sweep.sh --rounds 100
```

In `b64-t0-n100001`, `b64` means 64 repeated branches per sled pass, `t0`
means those branches are untaken, and `n100001` is the requested overflow
threshold of 100,001 retired conditional branches. `t1` means taken branches.
Each sled pass also retires one loop branch.

The worker uses CPU 0 by default. Use `--pin-core N` to select another CPU.
Each run saves a summary at `max-skid-experiment/results/<date>/results.md`,
with links to the individual tests. See the
[experiment README](max-skid-experiment/README.md) for the assembly and the
small branch-count check.
