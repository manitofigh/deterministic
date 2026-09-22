# Event results

* Complete: 256/256
* Potentially deterministic: 18
* Non-deterministic: 195
* Zero-only: 43

[Processor and settings](profile.md) · [Input events](events.txt)

## Determinism

| Event | Runs | Determinism |
|---|---:|---|
| [`assists.fp:u`](workers/cpu4/event-0068.log) | 100 | Potentially deterministic |
| [`br_inst_retired.cond:u`](workers/cpu21/event-0148.log) | 100 | Potentially deterministic |
| [`br_inst_retired.cond_ntaken:u`](workers/cpu22/event-0149.log) | 100 | Potentially deterministic |
| [`br_inst_retired.cond_taken:u`](workers/cpu23/event-0150.log) | 100 | Potentially deterministic |
| [`br_inst_retired.indirect:u`](workers/cpu25/event-0152.log) | 100 | Potentially deterministic |
| [`br_inst_retired.near_call:u`](workers/cpu26/event-0153.log) | 100 | Potentially deterministic |
| [`br_inst_retired.near_return:u`](workers/cpu27/event-0154.log) | 100 | Potentially deterministic |
| [`br_inst_retired.near_taken:u`](workers/cpu28/event-0155.log) | 100 | Potentially deterministic |
| [`fp_arith_inst_retired.128b_packed_double:u`](workers/cpu5/event-0069.log) | 100 | Potentially deterministic |
| [`fp_arith_inst_retired.128b_packed_single:u`](workers/cpu6/event-0070.log) | 100 | Potentially deterministic |
| [`fp_arith_inst_retired.4_flops:u`](workers/cpu9/event-0073.log) | 100 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar:u`](workers/cpu13/event-0077.log) | 100 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar_double:u`](workers/cpu14/event-0078.log) | 100 | Potentially deterministic |
| [`fp_arith_inst_retired.scalar_single:u`](workers/cpu15/event-0079.log) | 100 | Potentially deterministic |
| [`fp_arith_inst_retired.vector:u`](workers/cpu16/event-0080.log) | 100 | Potentially deterministic |
| [`inst_retired.nop:u`](workers/cpu60/event-0187.log) | 100 | Potentially deterministic |
| [`mem_inst_retired.lock_loads:u`](workers/cpu37/event-0038.log) | 100 | Potentially deterministic |
| [`misc_retired.pause_inst:u`](workers/cpu14/event-0204.log) | 100 | Potentially deterministic |
| [`arith.divider_active:u`](workers/cpu17/event-0144.log) | 2 | Non-deterministic |
| [`arith.fp_divider_active:u`](workers/cpu18/event-0145.log) | 2 | Non-deterministic |
| [`assists.any:u`](workers/cpu19/event-0146.log) | 74 | Non-deterministic |
| [`baclears.any:u`](workers/cpu17/event-0081.log) | 2 | Non-deterministic |
| [`br_inst_retired.all_branches:u`](workers/cpu20/event-0147.log) | 2 | Non-deterministic |
| [`br_inst_retired.far_branch:u`](workers/cpu24/event-0151.log) | 2 | Non-deterministic |
| [`br_misp_retired.all_branches:u`](workers/cpu29/event-0156.log) | 2 | Non-deterministic |
| [`br_misp_retired.cond:u`](workers/cpu30/event-0157.log) | 2 | Non-deterministic |
| [`br_misp_retired.cond_ntaken:u`](workers/cpu31/event-0158.log) | 2 | Non-deterministic |
| [`br_misp_retired.cond_taken:u`](workers/cpu32/event-0159.log) | 2 | Non-deterministic |
| [`br_misp_retired.indirect:u`](workers/cpu33/event-0160.log) | 16 | Non-deterministic |
| [`br_misp_retired.indirect_call:u`](workers/cpu34/event-0161.log) | 91 | Non-deterministic |
| [`br_misp_retired.near_taken:u`](workers/cpu35/event-0162.log) | 2 | Non-deterministic |
| [`branch-instructions:u`](workers/cpu53/event-0117.log) | 2 | Non-deterministic |
| [`branch-load-misses:u`](workers/cpu38/event-0102.log) | 2 | Non-deterministic |
| [`branch-loads:u`](workers/cpu39/event-0103.log) | 2 | Non-deterministic |
| [`branch-misses:u`](workers/cpu54/event-0118.log) | 2 | Non-deterministic |
| [`branches:u`](workers/cpu55/event-0119.log) | 2 | Non-deterministic |
| [`bus-cycles:u`](workers/cpu56/event-0120.log) | 2 | Non-deterministic |
| [`cache-misses:u`](workers/cpu57/event-0121.log) | 2 | Non-deterministic |
| [`cache-references:u`](workers/cpu58/event-0122.log) | 2 | Non-deterministic |
| [`core_power.lvl0_turbo_license:u`](workers/cpu14/event-0141.log) | 2 | Non-deterministic |
| [`core_snoop_response.i_fwd_fe:u`](workers/cpu2/event-0003.log) | 2 | Non-deterministic |
| [`core_snoop_response.i_fwd_m:u`](workers/cpu3/event-0004.log) | 2 | Non-deterministic |
| [`core_snoop_response.i_hit_fse:u`](workers/cpu4/event-0005.log) | 2 | Non-deterministic |
| [`core_snoop_response.miss:u`](workers/cpu5/event-0006.log) | 2 | Non-deterministic |
| [`core_snoop_response.s_fwd_fe:u`](workers/cpu6/event-0007.log) | 2 | Non-deterministic |
| [`core_snoop_response.s_hit_fse:u`](workers/cpu8/event-0009.log) | 2 | Non-deterministic |
| [`cpu-cycles:u`](workers/cpu59/event-0123.log) | 2 | Non-deterministic |
| [`cpu_clk_unhalted.distributed:u`](workers/cpu37/event-0164.log) | 2 | Non-deterministic |
| [`cpu_clk_unhalted.one_thread_active:u`](workers/cpu38/event-0165.log) | 2 | Non-deterministic |
| [`cpu_clk_unhalted.ref_distributed:u`](workers/cpu39/event-0166.log) | 2 | Non-deterministic |
| [`cpu_clk_unhalted.ref_tsc:u`](workers/cpu40/event-0167.log) | 2 | Non-deterministic |
| [`cpu_clk_unhalted.ref_xclk:u`](workers/cpu41/event-0168.log) | 2 | Non-deterministic |
| [`cpu_clk_unhalted.thread:u`](workers/cpu42/event-0169.log) | 2 | Non-deterministic |
| [`cpu_clk_unhalted.thread_p:u`](workers/cpu43/event-0170.log) | 2 | Non-deterministic |
| [`cycle_activity.cycles_l1d_miss:u`](workers/cpu44/event-0171.log) | 2 | Non-deterministic |
| [`cycle_activity.cycles_l2_miss:u`](workers/cpu45/event-0172.log) | 2 | Non-deterministic |
| [`cycle_activity.cycles_mem_any:u`](workers/cpu46/event-0173.log) | 2 | Non-deterministic |
| [`cycle_activity.stalls_l1d_miss:u`](workers/cpu47/event-0174.log) | 2 | Non-deterministic |
| [`cycle_activity.stalls_l2_miss:u`](workers/cpu48/event-0175.log) | 2 | Non-deterministic |
| [`cycle_activity.stalls_l3_miss:u`](workers/cpu0/event-0127.log) | 2 | Non-deterministic |
| [`cycle_activity.stalls_mem_any:u`](workers/cpu49/event-0176.log) | 2 | Non-deterministic |
| [`cycle_activity.stalls_total:u`](workers/cpu50/event-0177.log) | 2 | Non-deterministic |
| [`cycles:u`](workers/cpu60/event-0124.log) | 2 | Non-deterministic |
| [`decode.lcp:u`](workers/cpu18/event-0082.log) | 2 | Non-deterministic |
| [`dsb2mite_switches.count:u`](workers/cpu19/event-0083.log) | 2 | Non-deterministic |
| [`dsb2mite_switches.penalty_cycles:u`](workers/cpu20/event-0084.log) | 2 | Non-deterministic |
| [`dtlb-load-misses:u`](workers/cpu40/event-0104.log) | 2 | Non-deterministic |
| [`dtlb-loads:u`](workers/cpu41/event-0105.log) | 2 | Non-deterministic |
| [`dtlb-store-misses:u`](workers/cpu42/event-0106.log) | 3 | Non-deterministic |
| [`dtlb-stores:u`](workers/cpu43/event-0107.log) | 13 | Non-deterministic |
| [`dtlb_load_misses.stlb_hit:u`](workers/cpu47/event-0237.log) | 2 | Non-deterministic |
| [`dtlb_load_misses.walk_active:u`](workers/cpu48/event-0238.log) | 2 | Non-deterministic |
| [`dtlb_load_misses.walk_completed:u`](workers/cpu49/event-0239.log) | 4 | Non-deterministic |
| [`dtlb_load_misses.walk_completed_4k:u`](workers/cpu52/event-0242.log) | 3 | Non-deterministic |
| [`dtlb_load_misses.walk_pending:u`](workers/cpu53/event-0243.log) | 2 | Non-deterministic |
| [`dtlb_store_misses.stlb_hit:u`](workers/cpu54/event-0244.log) | 2 | Non-deterministic |
| [`dtlb_store_misses.walk_active:u`](workers/cpu55/event-0245.log) | 2 | Non-deterministic |
| [`dtlb_store_misses.walk_completed:u`](workers/cpu56/event-0246.log) | 2 | Non-deterministic |
| [`dtlb_store_misses.walk_completed_4k:u`](workers/cpu59/event-0249.log) | 2 | Non-deterministic |
| [`dtlb_store_misses.walk_pending:u`](workers/cpu60/event-0250.log) | 2 | Non-deterministic |
| [`exe_activity.1_ports_util:u`](workers/cpu51/event-0178.log) | 2 | Non-deterministic |
| [`exe_activity.2_ports_util:u`](workers/cpu52/event-0179.log) | 2 | Non-deterministic |
| [`exe_activity.3_ports_util:u`](workers/cpu53/event-0180.log) | 2 | Non-deterministic |
| [`exe_activity.4_ports_util:u`](workers/cpu54/event-0181.log) | 2 | Non-deterministic |
| [`exe_activity.bound_on_stores:u`](workers/cpu55/event-0182.log) | 2 | Non-deterministic |
| [`icache_16b.ifdata_stall:u`](workers/cpu21/event-0085.log) | 2 | Non-deterministic |
| [`icache_64b.iftag_hit:u`](workers/cpu22/event-0086.log) | 2 | Non-deterministic |
| [`icache_64b.iftag_miss:u`](workers/cpu23/event-0087.log) | 2 | Non-deterministic |
| [`icache_64b.iftag_stall:u`](workers/cpu24/event-0088.log) | 2 | Non-deterministic |
| [`icache_data.stalls:u`](workers/cpu25/event-0089.log) | 2 | Non-deterministic |
| [`icache_tag.stalls:u`](workers/cpu26/event-0090.log) | 2 | Non-deterministic |
| [`idq.dsb_cycles_any:u`](workers/cpu27/event-0091.log) | 2 | Non-deterministic |
| [`idq.dsb_cycles_ok:u`](workers/cpu28/event-0092.log) | 2 | Non-deterministic |
| [`idq.dsb_uops:u`](workers/cpu29/event-0093.log) | 2 | Non-deterministic |
| [`idq.mite_cycles_any:u`](workers/cpu30/event-0094.log) | 2 | Non-deterministic |
| [`idq.mite_cycles_ok:u`](workers/cpu31/event-0095.log) | 2 | Non-deterministic |
| [`idq.mite_uops:u`](workers/cpu32/event-0096.log) | 2 | Non-deterministic |
| [`idq.ms_switches:u`](workers/cpu33/event-0097.log) | 2 | Non-deterministic |
| [`idq.ms_uops:u`](workers/cpu34/event-0098.log) | 2 | Non-deterministic |
| [`idq_uops_not_delivered.core:u`](workers/cpu35/event-0099.log) | 2 | Non-deterministic |
| [`idq_uops_not_delivered.cycles_0_uops_deliv.core:u`](workers/cpu36/event-0100.log) | 2 | Non-deterministic |
| [`idq_uops_not_delivered.cycles_fe_was_ok:u`](workers/cpu37/event-0101.log) | 2 | Non-deterministic |
| [`ild_stall.lcp:u`](workers/cpu56/event-0183.log) | 2 | Non-deterministic |
| [`inst_decoded.decoders:u`](workers/cpu57/event-0184.log) | 2 | Non-deterministic |
| [`inst_retired.any:u`](workers/cpu58/event-0185.log) | 2 | Non-deterministic |
| [`inst_retired.any_p:u`](workers/cpu59/event-0186.log) | 2 | Non-deterministic |
| [`inst_retired.prec_dist:u`](workers/cpu61/event-0188.log) | 2 | Non-deterministic |
| [`instructions:u`](workers/cpu61/event-0125.log) | 2 | Non-deterministic |
| [`int_misc.all_recovery_cycles:u`](workers/cpu62/event-0189.log) | 2 | Non-deterministic |
| [`int_misc.clear_resteer_cycles:u`](workers/cpu0/event-0190.log) | 2 | Non-deterministic |
| [`int_misc.clears_count:u`](workers/cpu1/event-0191.log) | 2 | Non-deterministic |
| [`int_misc.recovery_cycles:u`](workers/cpu2/event-0192.log) | 2 | Non-deterministic |
| [`int_misc.uop_dropping:u`](workers/cpu3/event-0193.log) | 2 | Non-deterministic |
| [`itlb-load-misses:u`](workers/cpu44/event-0108.log) | 2 | Non-deterministic |
| [`itlb_misses.stlb_hit:u`](workers/cpu61/event-0251.log) | 2 | Non-deterministic |
| [`itlb_misses.walk_active:u`](workers/cpu62/event-0252.log) | 2 | Non-deterministic |
| [`itlb_misses.walk_completed:u`](workers/cpu0/event-0253.log) | 2 | Non-deterministic |
| [`itlb_misses.walk_completed_4k:u`](workers/cpu2/event-0255.log) | 2 | Non-deterministic |
| [`itlb_misses.walk_pending:u`](workers/cpu3/event-0256.log) | 2 | Non-deterministic |
| [`l1-dcache-load-misses:u`](workers/cpu45/event-0109.log) | 2 | Non-deterministic |
| [`l1-dcache-loads:u`](workers/cpu46/event-0110.log) | 2 | Non-deterministic |
| [`l1-dcache-stores:u`](workers/cpu47/event-0111.log) | 87 | Non-deterministic |
| [`l1-icache-load-misses:u`](workers/cpu48/event-0112.log) | 2 | Non-deterministic |
| [`l1d.replacement:u`](workers/cpu9/event-0010.log) | 2 | Non-deterministic |
| [`l1d_pend_miss.fb_full:u`](workers/cpu10/event-0011.log) | 2 | Non-deterministic |
| [`l1d_pend_miss.fb_full_periods:u`](workers/cpu11/event-0012.log) | 2 | Non-deterministic |
| [`l1d_pend_miss.l2_stall:u`](workers/cpu12/event-0013.log) | 2 | Non-deterministic |
| [`l1d_pend_miss.pending:u`](workers/cpu13/event-0014.log) | 2 | Non-deterministic |
| [`l1d_pend_miss.pending_cycles:u`](workers/cpu14/event-0015.log) | 2 | Non-deterministic |
| [`l2_lines_in.all:u`](workers/cpu15/event-0016.log) | 2 | Non-deterministic |
| [`l2_lines_out.non_silent:u`](workers/cpu16/event-0017.log) | 2 | Non-deterministic |
| [`l2_lines_out.silent:u`](workers/cpu17/event-0018.log) | 2 | Non-deterministic |
| [`l2_lines_out.useless_hwpf:u`](workers/cpu18/event-0019.log) | 2 | Non-deterministic |
| [`l2_rqsts.all_code_rd:u`](workers/cpu19/event-0020.log) | 2 | Non-deterministic |
| [`l2_rqsts.all_demand_data_rd:u`](workers/cpu20/event-0021.log) | 2 | Non-deterministic |
| [`l2_rqsts.all_demand_miss:u`](workers/cpu21/event-0022.log) | 2 | Non-deterministic |
| [`l2_rqsts.all_rfo:u`](workers/cpu22/event-0023.log) | 2 | Non-deterministic |
| [`l2_rqsts.code_rd_hit:u`](workers/cpu23/event-0024.log) | 2 | Non-deterministic |
| [`l2_rqsts.code_rd_miss:u`](workers/cpu24/event-0025.log) | 2 | Non-deterministic |
| [`l2_rqsts.demand_data_rd_hit:u`](workers/cpu25/event-0026.log) | 2 | Non-deterministic |
| [`l2_rqsts.demand_data_rd_miss:u`](workers/cpu26/event-0027.log) | 2 | Non-deterministic |
| [`l2_rqsts.rfo_hit:u`](workers/cpu27/event-0028.log) | 2 | Non-deterministic |
| [`l2_rqsts.rfo_miss:u`](workers/cpu28/event-0029.log) | 2 | Non-deterministic |
| [`l2_rqsts.swpf_miss:u`](workers/cpu30/event-0031.log) | 6 | Non-deterministic |
| [`l2_trans.l2_wb:u`](workers/cpu31/event-0032.log) | 2 | Non-deterministic |
| [`ld_blocks.store_forward:u`](workers/cpu5/event-0195.log) | 2 | Non-deterministic |
| [`ld_blocks_partial.address_alias:u`](workers/cpu6/event-0196.log) | 2 | Non-deterministic |
| [`llc-load-misses:u`](workers/cpu49/event-0113.log) | 2 | Non-deterministic |
| [`llc-loads:u`](workers/cpu50/event-0114.log) | 2 | Non-deterministic |
| [`llc-store-misses:u`](workers/cpu51/event-0115.log) | 2 | Non-deterministic |
| [`llc-stores:u`](workers/cpu52/event-0116.log) | 2 | Non-deterministic |
| [`load_hit_prefetch.swpf:u`](workers/cpu7/event-0197.log) | 16 | Non-deterministic |
| [`longest_lat_cache.miss:u`](workers/cpu32/event-0033.log) | 2 | Non-deterministic |
| [`longest_lat_cache.reference:u`](workers/cpu33/event-0034.log) | 2 | Non-deterministic |
| [`machine_clears.count:u`](workers/cpu11/event-0201.log) | 2 | Non-deterministic |
| [`machine_clears.memory_ordering:u`](workers/cpu1/event-0128.log) | 2 | Non-deterministic |
| [`machine_clears.smc:u`](workers/cpu12/event-0202.log) | 2 | Non-deterministic |
| [`mem-stores:u`](workers/cpu0/event-0001.log) | 11 | Non-deterministic |
| [`mem_inst_retired.all_loads:u`](workers/cpu34/event-0035.log) | 2 | Non-deterministic |
| [`mem_inst_retired.all_stores:u`](workers/cpu35/event-0036.log) | 73 | Non-deterministic |
| [`mem_inst_retired.any:u`](workers/cpu36/event-0037.log) | 2 | Non-deterministic |
| [`mem_inst_retired.split_loads:u`](workers/cpu38/event-0039.log) | 2 | Non-deterministic |
| [`mem_inst_retired.split_stores:u`](workers/cpu39/event-0040.log) | 2 | Non-deterministic |
| [`mem_inst_retired.stlb_miss_loads:u`](workers/cpu40/event-0041.log) | 16 | Non-deterministic |
| [`mem_inst_retired.stlb_miss_stores:u`](workers/cpu41/event-0042.log) | 6 | Non-deterministic |
| [`mem_load_l3_hit_retired.xsnp_fwd:u`](workers/cpu42/event-0043.log) | 17 | Non-deterministic |
| [`mem_load_l3_hit_retired.xsnp_none:u`](workers/cpu45/event-0046.log) | 2 | Non-deterministic |
| [`mem_load_l3_miss_retired.local_dram:u`](workers/cpu46/event-0047.log) | 2 | Non-deterministic |
| [`mem_load_retired.fb_hit:u`](workers/cpu52/event-0053.log) | 2 | Non-deterministic |
| [`mem_load_retired.l1_hit:u`](workers/cpu53/event-0054.log) | 2 | Non-deterministic |
| [`mem_load_retired.l1_miss:u`](workers/cpu54/event-0055.log) | 2 | Non-deterministic |
| [`mem_load_retired.l2_hit:u`](workers/cpu55/event-0056.log) | 2 | Non-deterministic |
| [`mem_load_retired.l2_miss:u`](workers/cpu56/event-0057.log) | 2 | Non-deterministic |
| [`mem_load_retired.l3_hit:u`](workers/cpu57/event-0058.log) | 2 | Non-deterministic |
| [`mem_load_retired.l3_miss:u`](workers/cpu58/event-0059.log) | 2 | Non-deterministic |
| [`ref-cycles:u`](workers/cpu62/event-0126.log) | 2 | Non-deterministic |
| [`resource_stalls.sb:u`](workers/cpu15/event-0205.log) | 2 | Non-deterministic |
| [`resource_stalls.scoreboard:u`](workers/cpu16/event-0206.log) | 2 | Non-deterministic |
| [`rs_events.empty_cycles:u`](workers/cpu17/event-0207.log) | 2 | Non-deterministic |
| [`rs_events.empty_end:u`](workers/cpu18/event-0208.log) | 2 | Non-deterministic |
| [`slots:u`](workers/cpu1/event-0002.log) | 2 | Non-deterministic |
| [`sq_misc.sq_full:u`](workers/cpu61/event-0062.log) | 37 | Non-deterministic |
| [`sw_prefetch_access.any:u`](workers/cpu62/event-0063.log) | 2 | Non-deterministic |
| [`sw_prefetch_access.nta:u`](workers/cpu0/event-0064.log) | 2 | Non-deterministic |
| [`sw_prefetch_access.t0:u`](workers/cpu2/event-0066.log) | 2 | Non-deterministic |
| [`sw_prefetch_access.t1_t2:u`](workers/cpu3/event-0067.log) | 2 | Non-deterministic |
| [`topdown.backend_bound_slots:u`](workers/cpu19/event-0209.log) | 2 | Non-deterministic |
| [`topdown.slots:u`](workers/cpu20/event-0210.log) | 2 | Non-deterministic |
| [`topdown.slots_p:u`](workers/cpu21/event-0211.log) | 2 | Non-deterministic |
| [`uops_decoded.dec0:u`](workers/cpu22/event-0212.log) | 2 | Non-deterministic |
| [`uops_dispatched.port_0:u`](workers/cpu23/event-0213.log) | 2 | Non-deterministic |
| [`uops_dispatched.port_1:u`](workers/cpu24/event-0214.log) | 2 | Non-deterministic |
| [`uops_dispatched.port_2_3:u`](workers/cpu25/event-0215.log) | 2 | Non-deterministic |
| [`uops_dispatched.port_4_9:u`](workers/cpu26/event-0216.log) | 2 | Non-deterministic |
| [`uops_dispatched.port_5:u`](workers/cpu27/event-0217.log) | 2 | Non-deterministic |
| [`uops_dispatched.port_6:u`](workers/cpu28/event-0218.log) | 2 | Non-deterministic |
| [`uops_dispatched.port_7_8:u`](workers/cpu29/event-0219.log) | 2 | Non-deterministic |
| [`uops_executed.core_cycles_ge_1:u`](workers/cpu30/event-0220.log) | 2 | Non-deterministic |
| [`uops_executed.core_cycles_ge_2:u`](workers/cpu31/event-0221.log) | 2 | Non-deterministic |
| [`uops_executed.core_cycles_ge_3:u`](workers/cpu32/event-0222.log) | 2 | Non-deterministic |
| [`uops_executed.core_cycles_ge_4:u`](workers/cpu33/event-0223.log) | 2 | Non-deterministic |
| [`uops_executed.cycles_ge_1:u`](workers/cpu34/event-0224.log) | 2 | Non-deterministic |
| [`uops_executed.cycles_ge_2:u`](workers/cpu35/event-0225.log) | 2 | Non-deterministic |
| [`uops_executed.cycles_ge_3:u`](workers/cpu36/event-0226.log) | 2 | Non-deterministic |
| [`uops_executed.cycles_ge_4:u`](workers/cpu37/event-0227.log) | 2 | Non-deterministic |
| [`uops_executed.stall_cycles:u`](workers/cpu38/event-0228.log) | 2 | Non-deterministic |
| [`uops_executed.thread:u`](workers/cpu39/event-0229.log) | 2 | Non-deterministic |
| [`uops_executed.x87:u`](workers/cpu40/event-0230.log) | 2 | Non-deterministic |
| [`uops_issued.any:u`](workers/cpu41/event-0231.log) | 2 | Non-deterministic |
| [`uops_issued.stall_cycles:u`](workers/cpu42/event-0232.log) | 2 | Non-deterministic |
| [`uops_retired.slots:u`](workers/cpu44/event-0234.log) | 2 | Non-deterministic |
| [`uops_retired.stall_cycles:u`](workers/cpu45/event-0235.log) | 2 | Non-deterministic |
| [`uops_retired.total_cycles:u`](workers/cpu46/event-0236.log) | 2 | Non-deterministic |

## Zero-only (inconclusive)

| Event | Runs | Determinism |
|---|---:|---|
| [`br_misp_retired.ret:u`](workers/cpu36/event-0163.log) | 100 | Zero-only |
| [`core_power.lvl1_turbo_license:u`](workers/cpu15/event-0142.log) | 100 | Zero-only |
| [`core_power.lvl2_turbo_license:u`](workers/cpu16/event-0143.log) | 100 | Zero-only |
| [`core_snoop_response.s_fwd_m:u`](workers/cpu7/event-0008.log) | 100 | Zero-only |
| [`dtlb_load_misses.walk_completed_1g:u`](workers/cpu50/event-0240.log) | 100 | Zero-only |
| [`dtlb_load_misses.walk_completed_2m_4m:u`](workers/cpu51/event-0241.log) | 100 | Zero-only |
| [`dtlb_store_misses.walk_completed_1g:u`](workers/cpu57/event-0247.log) | 100 | Zero-only |
| [`dtlb_store_misses.walk_completed_2m_4m:u`](workers/cpu58/event-0248.log) | 100 | Zero-only |
| [`fp_arith_inst_retired.256b_packed_double:u`](workers/cpu7/event-0071.log) | 100 | Zero-only |
| [`fp_arith_inst_retired.256b_packed_single:u`](workers/cpu8/event-0072.log) | 100 | Zero-only |
| [`fp_arith_inst_retired.512b_packed_double:u`](workers/cpu10/event-0074.log) | 100 | Zero-only |
| [`fp_arith_inst_retired.512b_packed_single:u`](workers/cpu11/event-0075.log) | 100 | Zero-only |
| [`fp_arith_inst_retired.8_flops:u`](workers/cpu12/event-0076.log) | 100 | Zero-only |
| [`itlb_misses.walk_completed_2m_4m:u`](workers/cpu1/event-0254.log) | 100 | Zero-only |
| [`l2_rqsts.swpf_hit:u`](workers/cpu29/event-0030.log) | 100 | Zero-only |
| [`ld_blocks.no_sr:u`](workers/cpu4/event-0194.log) | 100 | Zero-only |
| [`lsd.cycles_active:u`](workers/cpu8/event-0198.log) | 100 | Zero-only |
| [`lsd.cycles_ok:u`](workers/cpu9/event-0199.log) | 100 | Zero-only |
| [`lsd.uops:u`](workers/cpu10/event-0200.log) | 100 | Zero-only |
| [`mem_load_l3_hit_retired.xsnp_miss:u`](workers/cpu43/event-0044.log) | 100 | Zero-only |
| [`mem_load_l3_hit_retired.xsnp_no_fwd:u`](workers/cpu44/event-0045.log) | 100 | Zero-only |
| [`mem_load_l3_miss_retired.remote_dram:u`](workers/cpu47/event-0048.log) | 100 | Zero-only |
| [`mem_load_l3_miss_retired.remote_fwd:u`](workers/cpu48/event-0049.log) | 100 | Zero-only |
| [`mem_load_l3_miss_retired.remote_hitm:u`](workers/cpu49/event-0050.log) | 100 | Zero-only |
| [`mem_load_l3_miss_retired.remote_pmm:u`](workers/cpu50/event-0051.log) | 100 | Zero-only |
| [`mem_load_misc_retired.uc:u`](workers/cpu51/event-0052.log) | 100 | Zero-only |
| [`mem_load_retired.local_pmm:u`](workers/cpu59/event-0060.log) | 100 | Zero-only |
| [`misc_retired.lbr_inserts:u`](workers/cpu13/event-0203.log) | 100 | Zero-only |
| [`rtm_retired.aborted:u`](workers/cpu2/event-0129.log) | 100 | Zero-only |
| [`rtm_retired.aborted_events:u`](workers/cpu3/event-0130.log) | 100 | Zero-only |
| [`rtm_retired.aborted_mem:u`](workers/cpu4/event-0131.log) | 100 | Zero-only |
| [`rtm_retired.aborted_memtype:u`](workers/cpu5/event-0132.log) | 100 | Zero-only |
| [`rtm_retired.aborted_unfriendly:u`](workers/cpu6/event-0133.log) | 100 | Zero-only |
| [`rtm_retired.commit:u`](workers/cpu7/event-0134.log) | 100 | Zero-only |
| [`rtm_retired.start:u`](workers/cpu8/event-0135.log) | 100 | Zero-only |
| [`sq_misc.bus_lock:u`](workers/cpu60/event-0061.log) | 100 | Zero-only |
| [`sw_prefetch_access.prefetchw:u`](workers/cpu1/event-0065.log) | 100 | Zero-only |
| [`tx_exec.misc2:u`](workers/cpu9/event-0136.log) | 100 | Zero-only |
| [`tx_exec.misc3:u`](workers/cpu10/event-0137.log) | 100 | Zero-only |
| [`tx_mem.abort_capacity_read:u`](workers/cpu11/event-0138.log) | 100 | Zero-only |
| [`tx_mem.abort_capacity_write:u`](workers/cpu12/event-0139.log) | 100 | Zero-only |
| [`tx_mem.abort_conflict:u`](workers/cpu13/event-0140.log) | 100 | Zero-only |
| [`uops_issued.vector_width_mismatch:u`](workers/cpu43/event-0233.log) | 100 | Zero-only |
