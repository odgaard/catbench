# Examples and Tutorials

This page contains practical examples for using CATBench in various scenarios.

## Basic Examples

### Example 1: Simple SpMM Benchmark

```python
import catbench as cb

# Create a SpMM benchmark with default settings
benchmark = cb.benchmark('spmm')

# Basic configuration
config = {
    'chunk_size': 16,
    'unroll_factor': 4,
    'omp_chunk_size': 2,
    'omp_num_threads': 8,
    'omp_scheduling_type': 0,  # static scheduling
    'omp_monotonic': 0,
    'omp_dynamic': 0,
    'permutation': '(0, 1, 2, 3, 4)'
}

# Run with default fidelity
fidelity = {
    "iterations": 10,
    "repeats": 3,
    "wait_after_run": 1,
    "wait_between_repeats": 1
}

result = benchmark.query(config, fidelity)
print(f"Execution time: {result['compute_time']:.2f} ms")
```

### Example 2: Parameter Sweep

```python
import catbench as cb
import itertools

benchmark = cb.benchmark('spmm', dataset='2630')

# Define parameter ranges
chunk_sizes = [8, 16, 32]
num_threads = [4, 8, 16]
unroll_factors = [1, 2, 4]

# Base configuration
base_config = {
    'omp_chunk_size': 2,
    'omp_scheduling_type': 0,
    'omp_monotonic': 0,
    'omp_dynamic': 0,
    'permutation': '(0, 1, 2, 3, 4)'
}

fidelity = {
    "iterations": 5,
    "repeats": 3,
    "wait_after_run": 0.5,
    "wait_between_repeats": 0.5
}

# Run parameter sweep
results = []
for cs, nt, uf in itertools.product(chunk_sizes, num_threads, unroll_factors):
    config = {
        **base_config,
        'chunk_size': cs,
        'omp_num_threads': nt,
        'unroll_factor': uf
    }
    
    try:
        result = benchmark.query(config, fidelity)
        results.append({
            'config': config,
            'time': result['compute_time']
        })
        print(f"CS={cs}, NT={nt}, UF={uf}: {result['compute_time']:.2f} ms")
    except Exception as e:
        print(f"Failed for configuration: {config}")

# Find best configuration
best = min(results, key=lambda x: x['time'])
print(f"\nBest configuration: {best['config']}")
print(f"Best time: {best['time']:.2f} ms")
```

## Advanced Examples

### Example 3: Hardware Benchmarking with Energy Measurement

```python
import catbench as cb

# Connect to hardware server
benchmark = cb.benchmark('spmm', 
                        dataset='hardware_run',
                        server_addresses=['192.168.1.100'])

config = {
    'chunk_size': 32,
    'unroll_factor': 4,
    'omp_chunk_size': 1,
    'omp_num_threads': 16,
    'omp_scheduling_type': 1,  # dynamic scheduling
    'omp_monotonic': 0,
    'omp_dynamic': 1,
    'permutation': '(1, 0, 4, 3, 2)'
}

# Higher fidelity for hardware measurements
fidelity = {
    "iterations": 50,
    "repeats": 10,
    "wait_after_run": 2,
    "wait_between_repeats": 2
}

result = benchmark.query(config, fidelity)
print(f"Execution time: {result['compute_time']:.2f} ms")
print(f"Energy consumption: {result['energy']:.2f} J")
print(f"Power: {result['energy'] / (result['compute_time'] / 1000):.2f} W")
```

### Example 4: RISE Benchmark - Matrix Multiplication

```python
import catbench as cb

# Create MM benchmark
benchmark = cb.benchmark('mm', dataset='rtxtitan')

# GPU-specific configuration
config = {
    "tuned_tile_i": 32,
    "tuned_tile_j": 32,
    "tuned_tile_k": 16,
    "tuned_reg_tile_i": 4,
    "tuned_reg_tile_j": 4,
    "tuned_wg_i": 256,
    "tuned_wg_j": 256
}

# RISE fidelity settings
fidelity = {
    "iterations": 100,
    "timeouts": 60000
}

result = benchmark.query(config, fidelity)
print(f"GPU kernel execution time: {result['compute_time']:.2f} ms")
```

### Example 5: Cluster Deployment

```python
import catbench as cb
import time

# Connect to cluster manager
benchmark = cb.benchmark('spmm', 
                        dataset='cluster_run',
                        port=50050,
                        server_addresses=['cluster.manager.com'])

# Multiple configurations to run in parallel
configs = [
    {
        'chunk_size': cs,
        'unroll_factor': uf,
        'omp_chunk_size': 2,
        'omp_num_threads': 16,
        'omp_scheduling_type': 0,
        'omp_monotonic': 0,
        'omp_dynamic': 0,
        'permutation': '(0, 1, 2, 3, 4)'
    }
    for cs in [8, 16, 32, 64]
    for uf in [1, 2, 4, 8]
]

fidelity = {
    "iterations": 20,
    "repeats": 5,
    "wait_after_run": 1,
    "wait_between_repeats": 1
}

# Submit all jobs
print(f"Submitting {len(configs)} configurations to cluster...")
results = []
for i, config in enumerate(configs):
    try:
        result = benchmark.query(config, fidelity)
        results.append((config, result))
        print(f"Job {i+1}/{len(configs)} completed")
    except Exception as e:
        print(f"Job {i+1} failed: {e}")

# Analyze results
best_time = float('inf')
best_config = None
for config, result in results:
    if result['compute_time'] < best_time:
        best_time = result['compute_time']
        best_config = config

print(f"\nBest configuration found:")
print(f"Configuration: {best_config}")
print(f"Time: {best_time:.2f} ms")
```

### Example 6: Using Tabular Data

```python
import catbench as cb
import pandas as pd

# Load from existing CSV data
benchmark = cb.benchmark('spmm', dataset='test')

# Or specify custom CSV path
# benchmark = cb.benchmark('spmm', dataset='path/to/data.csv')

config = {
    'chunk_size': 16,
    'unroll_factor': 2,
    'omp_chunk_size': 1,
    'omp_num_threads': 8,
    'omp_scheduling_type': 0,
    'omp_monotonic': 0,
    'omp_dynamic': 0,
    'permutation': '(0, 1, 2, 3, 4)'
}

# Fidelity is ignored for tabular data
fidelity = {}

result = benchmark.query(config, fidelity)
print(f"Tabular result: {result['compute_time']:.2f} ms")
```

## Optimization Examples

### Example 7: Bayesian Optimization

```python
import catbench as cb
from skopt import gp_minimize
from skopt.space import Integer, Categorical

benchmark = cb.benchmark('spmm')

# Define search space
space = [
    Integer(8, 64, name='chunk_size'),
    Integer(1, 8, name='unroll_factor'),
    Integer(1, 4, name='omp_chunk_size'),
    Integer(4, 32, name='omp_num_threads'),
    Categorical([0, 1], name='omp_scheduling_type')
]

# Fixed parameters
fixed_params = {
    'omp_monotonic': 0,
    'omp_dynamic': 0,
    'permutation': '(0, 1, 2, 3, 4)'
}

fidelity = {
    "iterations": 10,
    "repeats": 3,
    "wait_after_run": 1,
    "wait_between_repeats": 1
}

def objective(params):
    config = {
        'chunk_size': params[0],
        'unroll_factor': params[1],
        'omp_chunk_size': params[2],
        'omp_num_threads': params[3],
        'omp_scheduling_type': params[4],
        **fixed_params
    }
    
    try:
        result = benchmark.query(config, fidelity)
        return result['compute_time']
    except:
        return float('inf')

# Run Bayesian optimization
result = gp_minimize(objective, space, n_calls=50, random_state=42)

print(f"Best parameters found:")
print(f"Chunk size: {result.x[0]}")
print(f"Unroll factor: {result.x[1]}")
print(f"OMP chunk size: {result.x[2]}")
print(f"OMP threads: {result.x[3]}")
print(f"Scheduling type: {result.x[4]}")
print(f"Best time: {result.fun:.2f} ms")
```

## Tips and Best Practices

1. **Start with Surrogate Mode**: Use surrogate benchmarks for initial exploration and parameter tuning
2. **Validate with Hardware**: Always validate promising configurations on actual hardware
3. **Use Appropriate Fidelity**: Balance accuracy vs. execution time based on your needs
4. **Handle Errors Gracefully**: Always wrap benchmark calls in try-except blocks
5. **Log Results**: Save results to files for later analysis
6. **Monitor Resources**: When using hardware mode, monitor CPU/GPU utilization

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure gRPC server is running and accessible
2. **Energy Measurements Unavailable**: Check RAPL permissions (see deployment guide)
3. **Timeout Errors**: Increase timeout values in fidelity settings
4. **Invalid Configuration**: Check parameter ranges for each benchmark type