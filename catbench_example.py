import catbench as cb

q1 = {
    'chunk_size': 32, 'unroll_factor': 2,
    'omp_chunk_size': 1, 'omp_num_threads': 10,
    'omp_scheduling_type': 1,
    'omp_monotonic': 0, 'omp_dynamic': 0,
    'permutation': '(0, 1, 2, 3, 4)'
}

fids_taco = {
    "iterations": 15,
    "repeats": 5,
    "wait_after_run": 1,
    "wait_between_repeats": 1
}

def spmm_example():
    bench = cb.benchmark('SpMM', dataset="2630")
    result = bench.query(q1.copy(), fids_taco)
    print(result)


fids_rise = {
    "iterations": 100,
    "timeouts": 60000
}

q2 = {
    "tuned_sp0": 4096,
    "tuned_gs0": 16,
    "tuned_stride": 2,
    "tuned_sp1": 1024,
    "tuned_ls0": 16
}

def asum_example():
    bench = cb.benchmark('asum', dataset="test", server_addresses=["localhost"])
    result = bench.query(q2.copy(), fids_rise)
    print(result)

spmm_example()
#asum_example()
