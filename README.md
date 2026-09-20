# Finding Deterministic PMU Events

The goal is to find PMU events that behave deterministically. That is, if we run a 
program 1000x and record a hardware event `abc`, the final count on that event would always stay 
the same, given the same program.

This script runs the same core asm program repeatedly and checks whether each event returns the 
same count. Five matching counts (the default number of `--rounds` to test) typically 
filter out 99% of the non-deterministic events in the first 2/3 rounds. Some events however, 
only prove non-deterministic when testing 100+ rounds.

The core asm tests are from [Vince Weaver's original deterministic repo](https://github.com/deater/deterministic).

**Support**: Currently for Intel processors only.

## Running

```bash
sudo python3 src/run.py
```

Run on a Linux machine. Also, python 3.9+ and `perf` are needed: install them using your distribution package manager if missing. 

build the benchmark with `make -C static binaries/retired_instr.all.x86_64`. that needs `make` and the GNU assembler/linker. 
If you place the binary elsewhere, you can provide its path using `--benchmark static/binaries/retired_instr.all.x86_64`.

Here are some other useful options:
```bash
sudo python3 src/run.py --cores 8 --rounds 10   # see 1. for explanation below
sudo python3 src/run.py --output results/my-run # see 2. for explanation below
sudo python3 src/run.py --events events/intel/skx/events.txt  # see 3. for explanation below
```

| option | what it does |
|---|---|
| `--cores N` | use N physical cores for workers. default: all available physical cores **minus one**. |
| `--rounds N` | at most N runs per event. default: 5; minimum: 2. stop as soon as counts differ. |
| `--output PATH` | choose the output directory. existing directories are never overwritten. |
| `--events PATH` | read one event name per line from this file. |
| `--benchmark PATH` | choose the executable to count events for. |
| `--timeout SECONDS` | stop a measurement that takes too long. default: 120 seconds per round. |

Also, relative paths you provide are relative to where you run the command. 
The default event list, benchmark and results directory are located relative to this project, so the python script also works when called from another directory.

## Few things

* The script disables SMT and restores it once done (if it was enabled)
* The script uses `all_available_physical_cores - 1` by default and 
distributes one worker thread per physical core, each with its own list 
of events to test. If you don't care about the process ending faster and 
want more available cores instead, you can limit this using `--core 1`.
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

## reading the results

by default, output goes under `results/<microarch>/<processor-model>-step<stepping>/`. 
Your existing directories would not be overwritten; more runs on the same machine appends `-2`, then `-3`, etc to the dir name.

Based on the arch/uarch that the script is ran on, the results are written under its relevant dir name. 
There, you can see a beautifully-put-together results.md` containing the table of results. 
The event names link to logs containing each command, the assigned CPU, raw perf output, benchmark stderr, parsed counts and the final result. benchmark stdout is discarded. the runs column says how many rounds we actually attempted, including the round that first differed or failed.

| result | meaning |
|---|---|
| potentially deterministic | every requested round returned the same nonzero count. |
| non-deterministic | a successful round returned a different count. no more rounds are needed. |
| zero-only | every round returned zero. this doesn't show that the event can track progress. |
| error | the command failed, timed out, or didn't give a usable count. |

The potentially deterministic events come first, then the non-deterministic ones. zero-only events and errors have separate sections. 
