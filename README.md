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
| `--cores N` | Number of physical cores used by workers. Default: all available physical cores minus one. The coordinator stays on a separate core. |
| `--start-core N` | First worker CPU number. For example, `--cores 10 --start-core 10` selects CPUs 10 through 19. Unavailable ranges are rejected. |
| `--rounds N` | Default: 10, minimum: 2. Counting stops when counts differ; skid mode runs every round. |
| `--output PATH` | By default, the name is chosen based on the arch/uarch running on. Don't worry, existing dirs are not overwritten due to multiple runs on the same machine. |
| `--events PATH` | Would be generated if non-existent; one can however provide their own list of events by putting each event on a separate line. |
| `--event NAME` | Test one event, optionally ending in `:u`. |
| `--from-results PATH` | In skid mode, select potentially deterministic events from a previous count run. Default: detect count results for this CPU. |
| `--period N` | In skid mode, request overflow after N events. Default: half a preliminary count, capped at 1,000,000. Allowed range: 2 through 2,147,483,647. |
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

By default, output goes under `results/<microarch>/<processor-model>-step<stepping>/`. 
Your existing directories would not be overwritten; more runs on the same machine appends `-2`, then `-3`, etc to the dir name.

Based on the arch/uarch that the script is ran on, the results are written under its relevant dir name. 
There, you can see a beautifully-put-together results.md` containing the table of results. 
The event names link to logs containing the assigned CPU, benchmark stderr, parsed counts and the final result. Benchmark stdout is discarded. The runs column says how many rounds we actually attempted, including the round that first differed or failed.

| result | meaning |
|---|---|
| potentially deterministic | every requested round returned the same nonzero count. |
| non-deterministic | a successful round returned a different count. no more rounds are needed. |
| zero-only | every round returned zero. this doesn't show that the event can track progress. |
| error | the command failed, timed out, or didn't give a usable count. |

The potentially deterministic events come first, then the non-deterministic ones. zero-only events and errors have separate sections. 

## Measuring skid

Skid mode requests an interrupt partway through the benchmark, then measures how
many extra events occurred before Linux stopped the process. These are event
counts, not necessarily instructions or CPU cycles. The measurement includes
Linux's signal-delivery path. It uses ordinary overflow interrupts, not Precise
Event-Based Sampling (PEBS).

With no event source, skid mode looks under `results/<microarch>/` for this
processor model and stepping. It uses the matching count run with the highest
numbered suffix (`-2`, `-3`, etc.) that contains worker results, and prints the
selected directory. If none exists, provide an event source explicitly.
If the selected run has no potentially deterministic events, it reports an error.

```bash
# automatically find count results for this CPU
sudo python3 src/run.py --mode skid

# potentially deterministic events from a previous count run
sudo python3 src/run.py --mode skid --from-results results/emr/xeon-gold-6554s-step2

# a custom list, regardless of any previous classification
sudo python3 src/run.py --mode skid --events my-events.txt

# one event with an explicit overflow period
sudo python3 src/run.py --mode skid --event br_inst_retired.near_taken --period 1000000
```

Skid mode needs `cc` and Linux C development headers in addition to Python and
`perf`; install them using your distribution's package manager. The runner builds
the helper automatically. There are no additional Python packages to install.
On a machine where simultaneous multithreading (SMT) is already disabled and
performance-counter access is permitted, skid mode can also run without sudo.

By default, a preliminary run chooses a period separately for each event. If the
benchmark produces fewer than four events, the automatic selection reports an
error. Use `--period` to select a threshold explicitly; a benchmark that finishes
before its overflow notification is reported as a failed measurement.

Each round starts a fresh benchmark. Counting begins at the executable's entry,
and the process stops at the overflow signal before a user-space signal handler
runs. The saved count minus the requested period is the skid. Only user-space
events in that process are counted. All 10 rounds run even when their skids differ.

Results go under `results/skid/<microarch>/<processor-model>-step<stepping>/`.
Existing runs are preserved by appending `-2`, `-3`, etc. `--output` overrides the
location. Files created by sudo are assigned to the invoking user during cleanup,
including partial results from interrupted runs.

The report shows:

| Event | Min skid | Max skid | Average skid | Skid determinism |
|---|---:|---:|---:|---|
| example event | 10 | 10 | 10.00 | Potentially deterministic |

Each event links to its rounds, including the period, count at stop, skid, and
stopped instruction address. Matching skid values, including zero, are potentially
deterministic only when every requested round succeeds. Differing values are
non-deterministic. Incomplete measurements with no observed difference are
inconclusive. Errors are listed separately, and statistics use successful rounds
only. The maximum is the largest observed value, not a guaranteed upper bound.

A zero skid means no additional occurrences of that event were counted. The
process may still have executed instructions that do not contribute to it.
