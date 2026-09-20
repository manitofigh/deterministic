# Event results

* Running: 132/303
* Potentially deterministic: 8
* Non-deterministic: 94
* Zero-only: 30

[Processor and settings](profile.md) · [Input events](events.txt)

## Determinism

| Event | Runs | Determinism |
|---|---:|---|
| [`fp_arith_inst_retired.128b_packed_single:u`](workers/cpu8/event-0085.log) | 1000 | Potentially deterministic |
| [`fp_arith_inst_retired.8_flops:u`](workers/cpu14/event-0091.log) | 1000 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar:u`](workers/cpu15/event-0092.log) | 1000 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar_double:u`](workers/cpu16/event-0093.log) | 1000 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar_single:u`](workers/cpu17/event-0094.log) | 1000 | Potentially deterministic |
| [`fp_arith_inst_retired.vector:u`](workers/cpu18/event-0095.log) | 1000 | Potentially deterministic |
| [`fp_assist.any:u`](workers/cpu0/event-0096.log) | 1000 | Potentially deterministic |
| [`mem_inst_retired.lock_loads:u`](workers/cpu0/event-0058.log) | 1000 | Potentially deterministic |
| [`baclears.any:u`](workers/cpu1/event-0097.log) | 2 | Non-deterministic |
| [`br_inst_retired.all_branches:u`](workers/cpu1/event-0173.log) | 2 | Non-deterministic |
| [`branch-instructions:u`](workers/cpu0/event-0001.log) | 2 | Non-deterministic |
| [`branch-misses:u`](workers/cpu1/event-0002.log) | 2 | Non-deterministic |
| [`bus-cycles:u`](workers/cpu2/event-0003.log) | 2 | Non-deterministic |
| [`cache-misses:u`](workers/cpu3/event-0004.log) | 2 | Non-deterministic |
| [`cache-references:u`](workers/cpu4/event-0005.log) | 2 | Non-deterministic |
| [`cpu-cycles:u`](workers/cpu5/event-0006.log) | 2 | Non-deterministic |
| [`cpu_clk_unhalted.one_thread_active:u`](workers/cpu1/event-0192.log) | 2 | Non-deterministic |
| [`cycle_activity.stalls_l3_miss:u`](workers/cpu13/event-0128.log) | 2 | Non-deterministic |
| [`decode.lcp:u`](workers/cpu2/event-0098.log) | 2 | Non-deterministic |
| [`dsb2mite_switches.count:u`](workers/cpu3/event-0099.log) | 2 | Non-deterministic |
| [`dsb2mite_switches.penalty_cycles:u`](workers/cpu4/event-0100.log) | 2 | Non-deterministic |
| [`dtlb_load_misses.miss_causes_a_walk:u`](workers/cpu1/event-0268.log) | 2 | Non-deterministic |
| [`exe_activity.bound_on_stores:u`](workers/cpu1/event-0211.log) | 2 | Non-deterministic |
| [`icache_16b.ifdata_stall:u`](workers/cpu5/event-0101.log) | 2 | Non-deterministic |
| [`icache_64b.iftag_hit:u`](workers/cpu6/event-0102.log) | 2 | Non-deterministic |
| [`icache_64b.iftag_stall:u`](workers/cpu8/event-0104.log) | 2 | Non-deterministic |
| [`icache_tag.stalls:u`](workers/cpu9/event-0105.log) | 2 | Non-deterministic |
| [`idq.all_mite_cycles_any_uops:u`](workers/cpu13/event-0109.log) | 2 | Non-deterministic |
| [`idq.dsb_cycles:u`](workers/cpu14/event-0110.log) | 2 | Non-deterministic |
| [`idq.dsb_cycles_any:u`](workers/cpu15/event-0111.log) | 2 | Non-deterministic |
| [`idq.dsb_cycles_ok:u`](workers/cpu16/event-0112.log) | 2 | Non-deterministic |
| [`idq.dsb_uops:u`](workers/cpu17/event-0113.log) | 2 | Non-deterministic |
| [`idq.mite_cycles:u`](workers/cpu18/event-0114.log) | 2 | Non-deterministic |
| [`idq.mite_uops:u`](workers/cpu0/event-0115.log) | 2 | Non-deterministic |
| [`idq.ms_cycles:u`](workers/cpu1/event-0116.log) | 2 | Non-deterministic |
| [`idq.ms_dsb_cycles:u`](workers/cpu2/event-0117.log) | 2 | Non-deterministic |
| [`idq.ms_mite_uops:u`](workers/cpu3/event-0118.log) | 2 | Non-deterministic |
| [`idq.ms_switches:u`](workers/cpu4/event-0119.log) | 2 | Non-deterministic |
| [`idq.ms_uops:u`](workers/cpu5/event-0120.log) | 2 | Non-deterministic |
| [`idq_uops_not_delivered.core:u`](workers/cpu6/event-0121.log) | 2 | Non-deterministic |
| [`idq_uops_not_delivered.cycles_fe_was_ok:u`](workers/cpu8/event-0123.log) | 2 | Non-deterministic |
| [`idq_uops_not_delivered.cycles_le_1_uop_deliv.core:u`](workers/cpu9/event-0124.log) | 2 | Non-deterministic |
| [`instructions:u`](workers/cpu13/event-0014.log) | 2 | Non-deterministic |
| [`itlb_misses.walk_completed:u`](workers/cpu1/event-0287.log) | 2 | Non-deterministic |
| [`l1d.replacement:u`](workers/cpu7/event-0027.log) | 2 | Non-deterministic |
| [`l1d_pend_miss.fb_full:u`](workers/cpu8/event-0028.log) | 2 | Non-deterministic |
| [`l1d_pend_miss.pending:u`](workers/cpu9/event-0029.log) | 2 | Non-deterministic |
| [`l1d_pend_miss.pending_cycles:u`](workers/cpu10/event-0030.log) | 2 | Non-deterministic |
| [`l1d_pend_miss.pending_cycles_any:u`](workers/cpu11/event-0031.log) | 2 | Non-deterministic |
| [`l2_lines_in.all:u`](workers/cpu12/event-0032.log) | 2 | Non-deterministic |
| [`l2_lines_out.non_silent:u`](workers/cpu13/event-0033.log) | 2 | Non-deterministic |
| [`l2_lines_out.silent:u`](workers/cpu14/event-0034.log) | 2 | Non-deterministic |
| [`l2_lines_out.useless_hwpf:u`](workers/cpu15/event-0035.log) | 2 | Non-deterministic |
| [`l2_rqsts.all_code_rd:u`](workers/cpu16/event-0036.log) | 2 | Non-deterministic |
| [`l2_rqsts.all_demand_data_rd:u`](workers/cpu17/event-0037.log) | 2 | Non-deterministic |
| [`l2_rqsts.all_demand_miss:u`](workers/cpu18/event-0038.log) | 2 | Non-deterministic |
| [`l2_rqsts.all_demand_references:u`](workers/cpu0/event-0039.log) | 2 | Non-deterministic |
| [`l2_rqsts.all_pf:u`](workers/cpu1/event-0040.log) | 2 | Non-deterministic |
| [`l2_rqsts.all_rfo:u`](workers/cpu2/event-0041.log) | 2 | Non-deterministic |
| [`l2_rqsts.code_rd_hit:u`](workers/cpu3/event-0042.log) | 2 | Non-deterministic |
| [`l2_rqsts.code_rd_miss:u`](workers/cpu4/event-0043.log) | 2 | Non-deterministic |
| [`l2_rqsts.demand_data_rd_hit:u`](workers/cpu5/event-0044.log) | 2 | Non-deterministic |
| [`l2_rqsts.demand_data_rd_miss:u`](workers/cpu6/event-0045.log) | 2 | Non-deterministic |
| [`l2_rqsts.miss:u`](workers/cpu7/event-0046.log) | 2 | Non-deterministic |
| [`l2_rqsts.pf_hit:u`](workers/cpu8/event-0047.log) | 2 | Non-deterministic |
| [`l2_rqsts.pf_miss:u`](workers/cpu9/event-0048.log) | 2 | Non-deterministic |
| [`l2_rqsts.references:u`](workers/cpu10/event-0049.log) | 2 | Non-deterministic |
| [`l2_rqsts.rfo_hit:u`](workers/cpu11/event-0050.log) | 2 | Non-deterministic |
| [`l2_rqsts.rfo_miss:u`](workers/cpu12/event-0051.log) | 2 | Non-deterministic |
| [`l2_trans.l2_wb:u`](workers/cpu13/event-0052.log) | 2 | Non-deterministic |
| [`longest_lat_cache.miss:u`](workers/cpu14/event-0053.log) | 2 | Non-deterministic |
| [`longest_lat_cache.reference:u`](workers/cpu15/event-0054.log) | 2 | Non-deterministic |
| [`machine_clears.count:u`](workers/cpu1/event-0230.log) | 2 | Non-deterministic |
| [`machine_clears.memory_ordering:u`](workers/cpu3/event-0137.log) | 2 | Non-deterministic |
| [`mem-stores:u`](workers/cpu14/event-0015.log) | 2 | Non-deterministic |
| [`mem_inst_retired.all_loads:u`](workers/cpu16/event-0055.log) | 2 | Non-deterministic |
| [`mem_inst_retired.all_stores:u`](workers/cpu17/event-0056.log) | 103 | Non-deterministic |
| [`mem_inst_retired.any:u`](workers/cpu18/event-0057.log) | 2 | Non-deterministic |
| [`mem_inst_retired.split_loads:u`](workers/cpu1/event-0059.log) | 2 | Non-deterministic |
| [`mem_inst_retired.split_stores:u`](workers/cpu2/event-0060.log) | 2 | Non-deterministic |
| [`mem_inst_retired.stlb_miss_loads:u`](workers/cpu3/event-0061.log) | 2 | Non-deterministic |
| [`mem_inst_retired.stlb_miss_stores:u`](workers/cpu4/event-0062.log) | 5 | Non-deterministic |
| [`mem_load_l3_hit_retired.xsnp_hitm:u`](workers/cpu6/event-0064.log) | 3 | Non-deterministic |
| [`mem_load_l3_hit_retired.xsnp_none:u`](workers/cpu8/event-0066.log) | 2 | Non-deterministic |
| [`mem_load_l3_miss_retired.local_dram:u`](workers/cpu9/event-0067.log) | 2 | Non-deterministic |
| [`mem_load_retired.fb_hit:u`](workers/cpu14/event-0072.log) | 2 | Non-deterministic |
| [`mem_load_retired.l1_hit:u`](workers/cpu15/event-0073.log) | 2 | Non-deterministic |
| [`mem_load_retired.l1_miss:u`](workers/cpu16/event-0074.log) | 2 | Non-deterministic |
| [`mem_load_retired.l2_hit:u`](workers/cpu17/event-0075.log) | 2 | Non-deterministic |
| [`mem_load_retired.l2_miss:u`](workers/cpu18/event-0076.log) | 2 | Non-deterministic |
| [`mem_load_retired.l3_hit:u`](workers/cpu0/event-0077.log) | 3 | Non-deterministic |
| [`mem_load_retired.l3_miss:u`](workers/cpu1/event-0078.log) | 2 | Non-deterministic |
| [`ref-cycles:u`](workers/cpu15/event-0016.log) | 2 | Non-deterministic |
| [`sw_prefetch_access.nta:u`](workers/cpu3/event-0080.log) | 3 | Non-deterministic |
| [`sw_prefetch_access.t0:u`](workers/cpu5/event-0082.log) | 2 | Non-deterministic |
| [`sw_prefetch_access.t1_t2:u`](workers/cpu6/event-0083.log) | 2 | Non-deterministic |
| [`topdown-fetch-bubbles:u`](workers/cpu16/event-0017.log) | 2 | Non-deterministic |
| [`topdown-recovery-bubbles:u`](workers/cpu17/event-0018.log) | 2 | Non-deterministic |
| [`topdown-slots-issued:u`](workers/cpu18/event-0019.log) | 2 | Non-deterministic |
| [`topdown-slots-retired:u`](workers/cpu0/event-0020.log) | 2 | Non-deterministic |
| [`topdown-total-slots:u`](workers/cpu1/event-0021.log) | 2 | Non-deterministic |
| [`uops_executed.core_cycles_ge_2:u`](workers/cpu1/event-0249.log) | 2 | Non-deterministic |

## Zero-only (inconclusive)

| Event | Runs | Determinism |
|---|---:|---|
| [`cycles-ct:u`](workers/cpu6/event-0007.log) | 1000 | Zero-only |
| [`cycles-t:u`](workers/cpu7/event-0008.log) | 1000 | Zero-only |
| [`el-abort:u`](workers/cpu8/event-0009.log) | 1000 | Zero-only |
| [`el-capacity:u`](workers/cpu9/event-0010.log) | 1000 | Zero-only |
| [`el-commit:u`](workers/cpu10/event-0011.log) | 1000 | Zero-only |
| [`el-conflict:u`](workers/cpu11/event-0012.log) | 1000 | Zero-only |
| [`el-start:u`](workers/cpu12/event-0013.log) | 1000 | Zero-only |
| [`fp_arith_inst_retired.256b_packed_double:u`](workers/cpu9/event-0086.log) | 1000 | Zero-only |
| [`fp_arith_inst_retired.512b_packed_single:u`](workers/cpu13/event-0090.log) | 1000 | Zero-only |
| [`hle_retired.aborted:u`](workers/cpu14/event-0129.log) | 1000 | Zero-only |
| [`hle_retired.aborted_events:u`](workers/cpu15/event-0130.log) | 1000 | Zero-only |
| [`hle_retired.aborted_mem:u`](workers/cpu16/event-0131.log) | 1000 | Zero-only |
| [`hle_retired.aborted_memtype:u`](workers/cpu17/event-0132.log) | 1000 | Zero-only |
| [`hle_retired.aborted_timer:u`](workers/cpu18/event-0133.log) | 1000 | Zero-only |
| [`hle_retired.commit:u`](workers/cpu1/event-0135.log) | 1000 | Zero-only |
| [`mem_load_l3_hit_retired.xsnp_hit:u`](workers/cpu5/event-0063.log) | 1000 | Zero-only |
| [`mem_load_l3_hit_retired.xsnp_miss:u`](workers/cpu7/event-0065.log) | 1000 | Zero-only |
| [`mem_load_l3_miss_retired.remote_dram:u`](workers/cpu10/event-0068.log) | 1000 | Zero-only |
| [`mem_load_l3_miss_retired.remote_fwd:u`](workers/cpu11/event-0069.log) | 1000 | Zero-only |
| [`mem_load_l3_miss_retired.remote_hitm:u`](workers/cpu12/event-0070.log) | 1000 | Zero-only |
| [`mem_load_misc_retired.uc:u`](workers/cpu13/event-0071.log) | 1000 | Zero-only |
| [`sq_misc.split_lock:u`](workers/cpu2/event-0079.log) | 1000 | Zero-only |
| [`sw_prefetch_access.prefetchw:u`](workers/cpu4/event-0081.log) | 1000 | Zero-only |
| [`tx-abort:u`](workers/cpu2/event-0022.log) | 1000 | Zero-only |
| [`tx-capacity:u`](workers/cpu3/event-0023.log) | 1000 | Zero-only |
| [`tx-commit:u`](workers/cpu4/event-0024.log) | 1000 | Zero-only |
| [`tx-conflict:u`](workers/cpu5/event-0025.log) | 1000 | Zero-only |
| [`tx-start:u`](workers/cpu6/event-0026.log) | 1000 | Zero-only |
| [`tx_mem.abort_hle_elision_buffer_not_empty:u`](workers/cpu1/event-0154.log) | 1000 | Zero-only |
| [`tx_mem.abort_hle_store_to_elided_lock:u`](workers/cpu3/event-0156.log) | 1000 | Zero-only |
