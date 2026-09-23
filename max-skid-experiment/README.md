# Branch sled skid experiment

This benchmark asks for an overflow at a known conditional branch, then runs a
long sequence of conditional branches. It measures how many more branch events
the existing skid helper counts before Linux stops the process.

## Counted path

The executable has its own `_start` and exits with a syscall. The skid helper
starts its counter at the executable's entry. Each counted setup iteration executes
31 `jnz` instructions and one `jnz` at the end of the loop. The default 3,125
iterations therefore retire 100,000 conditional branches. The setup's
31 repeated `jnz` instructions are not taken. The loop's `jnz` is taken until
the final iteration. A `nop` between `test` and the first repeated `jnz`
keeps that pair from combining into one internal operation.

`first_sled_branch` is the first branch in the sled. `--overflow 100001`
requests overflow when it retires. By then the executable has retired about
206,256 instructions: two initial instructions, 66 instructions per counted setup
iteration, three instructions between the setup and the marked branch, and
the marked branch itself. This is an instruction count along the written path;
the stop instruction can be later. The disassembly places the marked branch
at `0x401073` in the default build.

Each sled pass has 64 conditional branches and one conditional loop
branch. The default 2,000 passes leave 129,999 possible conditional
branch events after the marked branch if the executable runs to completion.
That number is sled capacity, not a predicted or measured skid. The `REPEATED_BRANCHES_TAKEN`
build option changes only the 64 branches per sled pass: `0` makes them untaken, and `1`
makes them taken. The loop branch is taken until the last iteration.
An untaken sled branch executes its following `nop`; a taken branch skips it.
The comparison therefore covers both branch direction and that instruction
difference. It does not isolate execution-port behavior by itself.

The counted setup and sled are small loops so their instruction bytes can be reused
while the counter approaches overflow. The sled sizes in the sweep are 64, 256,
and 1,024 branches per pass. They let us check whether a longer run of
branches between loop exits changes the observed skid. The sweep tests the
first pass and positions after 16 complete sled passes, when those instruction
bytes have already executed.

## Build and run

From the `deterministic` directory:

```sh
make -C max-skid-experiment
taskset -c 0 max-skid-experiment/build/branch-sled-setup3125-passes2000-branches64-taken0
bash max-skid-experiment/run-sweep.sh --rounds 100
```

The `taskset` command checks that the executable exits normally on CPU 0. The
runner pins its worker to CPU 0 and keeps its coordinator on another core. The
saved run includes every round's count, skid, and stopped instruction pointer.
CPU 0 is the default. Pass `--pin-core N` to use a different CPU.

To check the 32-branch setup count independently, run the two small benchmarks
in `mini-test/`:

```sh
sudo bash max-skid-experiment/mini-test/run.sh
sudo bash max-skid-experiment/mini-test/run.sh --round 100
```

The script assembles one- and two-iteration versions and measures each ten times
by default. `--round N` (or `--rounds N`) changes the number of measurements.
It prints the event name, expected count, and average measured count for each.
The measured counts on this machine were 32 and 64.

The sweep prompts for `sudo` once. It saves one dated experiment directory:

```text
max-skid-experiment/results/sep-23-2026-11:30:00/
  results.md
  b64-t0-n100001/
    results.md
    workers/cpu0/results.jsonl
  b1024-t1-n116401/
    results.md
    workers/cpu0/results.jsonl
```

The root `results.md` lists every combination, its minimum, maximum, average,
successful rounds, and a link to the series report. Each series retains its
per-round counts, skid, and stop addresses. The sweep writes the root report
after each series, so an interrupted experiment still has a summary of its
completed series.

The earlier 42-series run reached a maximum observed skid of 63 extra branches
with an untaken sled. At threshold 100,032 in the 1,024-branch sled, 100 rounds
ranged from 3 to 63 extra branches. A 63-skid round stopped at `0x40118f`, the
`nop` immediately after the 95th sled branch. The requested overflow was the
32nd sled branch; 95 - 32 = 63.

The largest measured skid supports a margin for the tested event, processor,
kernel, and setup. It cannot establish a guaranteed bound for every workload.
The counter reports additional retired conditional branches; the stopped
instruction pointer helps check where the signal actually stopped the process.

## Design sources

- [`../static/src/retired_instr.x86_64.s`](../static/src/retired_instr.x86_64.s)
  uses a static `_start`, explicit branch loops, and a direct exit syscall.
- [Peter Cordes on branch execution ports](https://stackoverflow.com/questions/50984007/what-exactly-happens-when-a-skylake-cpu-mispredicts-a-branch)
  motivates comparing taken and untaken branches. The cited port details are
  for Skylake; this experiment measures the result on Ice Lake.
- [Peter Cordes on compare and branch fusion](https://stackoverflow.com/questions/33721204/test-whether-a-register-is-zero-with-cmp-reg-0-vs-or-reg-reg)
  motivates the `nop` between `test` and the first sled branch.
- [Intel's Ice Lake event definition](https://perfmon-events.intel.com/platforms/icelakex/core-events/core/)
  defines `BR_INST_RETIRED.COND` as retired conditional branches.
