# deterministic event experiments

we want to find events worth investigating as a clock for deterministic execution. this runs the same asm program repeatedly and checks whether each event returns the same count. five matching counts make an event worth looking at, but don't prove that it is deterministic for every program or that its interrupts arrive at an exact point.

## run it

```bash
cd ~/dev/Laplace/deterministic
sudo python3 src/run.py
```

we need linux, python 3.9+ and `perf`. install them using your distribution package manager if missing. there are no python packages to install, so no venv or separate setup script.

the asm tests are from [Vince Weaver's original deterministic repo](https://github.com/deater/deterministic), kept here under `static/`.

build the benchmark with `make -C static binaries/retired_instr.all.x86_64`. that needs `make` and the GNU assembler/linker. the default benchmark path works when this checkout is named `deterministic`; otherwise, pass `--benchmark static/binaries/retired_instr.all.x86_64`.

```bash
sudo python3 src/run.py --cores 8 --rounds 10
sudo python3 src/run.py --output results/my-run
sudo python3 src/run.py --events events/intel/skx/events.txt
```

| option | what it does |
|---|---|
| `--cores N` | use N physical cores for workers. default: all available physical cores minus one. |
| `--rounds N` | at most N runs per event. default: 5; minimum: 2. stop as soon as counts differ. |
| `--output PATH` | choose the output directory. existing directories are never overwritten. |
| `--events PATH` | read one event name per line from this file. |
| `--benchmark PATH` | choose the executable to count events for. |
| `--timeout SECONDS` | stop a measurement that takes too long. default: 120 seconds per round. |

relative paths you provide are relative to where you run the command. the default event list, benchmark and results directory are located relative to this project, so the python script also works when called from another directory.

## how it runs

first, disable simultaneous multithreading (SMT) if it's on. then pick one CPU per physical core, in increasing CPU number order. leave the last one for the python process that starts the workers and collects results.

split the event list across those workers in turn: event 1 goes to worker 1, event 2 to worker 2, and so on. each worker stays on its assigned CPU, and perf and the asm program inherit that setting. each event is assigned to one worker; we aren't testing every event on every core.

for each event, request `:u`, so only user execution is counted. save the perf output, compare the count with the first round, and stop immediately if it differs. otherwise, keep going until the requested number of rounds is done. `perf` sometimes leaves `:u` out of the printed event name; the command still requests it.

when the run finishes, restore SMT only if this run turned it off. ctrl-c stops the workers and their benchmark processes and keeps partial results. running again starts a new directory, it doesn't resume the partial run. a second runner is blocked while the first is active.

this needs a machine where we can control physical cores and SMT. detected VMs are rejected. reserving a core doesn't stop other programs or hardware interrupts from running on worker cores, and workers still share caches and memory. `kill -9` or a machine crash can't run cleanup, so those can leave processes or the SMT setting behind.

## the event list

`events/intel/skx/events.txt` has the 303 selected names exactly as listed, without line numbers, descriptions or `:u`. the runner adds `:u`. duplicate names, blank lines and extra whitespace are rejected.

the selection leaves out software counters, tracepoints, derived metrics, offcore events and system-wide counters. events needing special setup were set aside separately. ordinary cache, branch, load/store and other core events stay in the list, even if we don't expect them to be deterministic. optional support for precise event-based sampling (PEBS) alone wasn’t a reason to remove an event.

the runner first looks for `events/intel/<microarch>/events.txt`. if it's missing, it prints a warning, runs `perf-list-events.py` to create it, then reads the file and starts the workers. if capture or filtering fails, it stops with a red `[-]` error before starting workers. it never substitutes another CPU's list. a missing file passed with `--events` is generated at that path too.

you only need `sudo python3 src/run.py` for the full run, including capture when the list is missing. capture uses `LC_ALL=C perf list --json`, so your perf version must support `--json`. to generate the default list separately:

```bash
sudo python3 src/perf-list-events.py
```

CPU names use Intel's [perfmon mapping](https://github.com/intel/perfmon/blob/main/mapfile.csv). the code recognizes skx, clx, icx, spr, emr, gnr, srf and cwf. **only the skx event list is included here.** on another supported CPU family, the runner captures its list if missing. you can also provide an explicit `--events` file. passing the skx list on another CPU doesn't make it a complete list for that CPU.

## reading the results

by default, output goes under `results/<microarch>/<processor-model>-step<stepping>/`. existing directories are never overwritten; another run adds `-2`, then `-3`, etc.

open `results.md` for the table. the event names link to logs containing each command, the assigned CPU, raw perf output, benchmark stderr, parsed counts and the final result. benchmark stdout is discarded. the runs column says how many rounds we actually attempted, including the round that first differed or failed.

| result | what it means |
|---|---|
| potentially deterministic | every requested round returned the same nonzero count. |
| non-deterministic | a successful round returned a different count. no more rounds are needed. |
| zero-only | every round returned zero. this doesn't show that the event can track progress. |
| error | the command failed, timed out, or didn't give a usable count. |

the potentially deterministic events come first, then the non-deterministic ones. zero-only events and errors have separate sections. a counter must report that it ran for 100% of the measurement; perf rounds that percentage, so this doesn't rule out very small gaps.

## saved runs

the [completed run](results/skx/xeon-silver-4114-step4-2/results.md) covered all 303 events in 179 seconds using 19 workers: 24 potentially deterministic, 209 non-deterministic and 70 zero-only, with no errors.

the earlier `results/skx/xeon-silver-4114-step4/` is kept too. it has 12 parser errors from perf dropping `:u` in printed cache-event names. that was fixed before the `-2` run. use the `-2` results.
