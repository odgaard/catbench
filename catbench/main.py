from .benchmarks import *

from interopt import Study

# Similarly define SpMV, SDDMM, MTTKRP, and TTV classes
def benchmark(benchmark_name, enable_tabular=True, enable_model=True,
              dataset=None, enabled_objectives=None, enable_download=True,
              port=50051, server_addresses=None):
    definitions = {
        'spmm': get_spmm_definition(),
        'spmv': get_spmv_definition(),
        'sddmm': get_sddmm_definition(),
        'mttkrp': get_mttkrp_definition(),
        'ttv': get_ttv_definition(),
        'asum': get_asum_definition(),
        'harris': get_harris_definition(),
        'kmeans': get_kmeans_definition(),
        'mm': get_mm_definition(),
        'scal': get_scal_definition(),
        'stencil': get_stencil_definition(),
    }
    taco_tasks = ['spmm', 'spmv', 'sddmm', 'ttv', 'mttkrp']
    rise_tasks = ['asum', 'harris', 'kmeans', 'mm', 'scal', 'stencil']
    benchmark_name = benchmark_name.lower()

    if benchmark_name not in definitions:
        raise ValueError("Unknown benchmark name")

    if enabled_objectives is None:
        if benchmark_name in taco_tasks:
            enabled_objectives = ['compute_time']
        elif benchmark_name in rise_tasks:
            enabled_objectives = ['compute_time', 'energy']

    # If server_addresses is None, then run the benchmark locally
    if server_addresses is None:
        server_addresses = ["localhost"]
    # If server_addresses is not None, then it does not make sense to enable model
    else:
        enable_model = False

    if dataset is None:
        if benchmark_name in taco_tasks:
            dataset = '2630'
        elif benchmark_name in rise_tasks:
            dataset = 'rtxtitan'

    return Study(benchmark_name=benchmark_name, definition=definitions[benchmark_name],
                 enable_tabular=enable_tabular, enable_model=enable_model,
                 dataset=dataset, enable_download=enable_download,
                 enabled_objectives=enabled_objectives, port=port,
                 server_addresses=server_addresses)
