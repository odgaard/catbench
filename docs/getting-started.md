# Getting Started with CATBench

This guide will help you get up and running with CATBench quickly.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install from PyPI

```bash
pip install catbench
```

### Install from Source

```bash
git clone https://github.com/odgaard/catbench.git
cd catbench
pip install -r requirements.txt
pip install -e .
```

## Basic Usage

### 1. Import CATBench

```python
import catbench as cb
```

### 2. Create a Benchmark Instance

Choose your benchmark mode:

#### Surrogate Mode (Default)
```python
# Uses machine learning models for fast prediction
benchmark = cb.benchmark('spmm')

# Specify a dataset (default is '2630' for TACO benchmarks)
benchmark = cb.benchmark('spmm', dataset='2630')
```

#### Tabular Mode
```python
# Uses precomputed data from CSV files
benchmark = cb.benchmark('spmm', dataset='test')
```

#### Hardware Mode
```python
# Runs on actual hardware via gRPC
benchmark = cb.benchmark('spmm', dataset='hardware_run', 
                        server_addresses=['localhost'])
```

### 3. Define Query Parameters

Each benchmark type has specific parameters. For example, SpMM:

```python
query = {
    'chunk_size': 16,
    'unroll_factor': 16,
    'omp_chunk_size': 2,
    'omp_num_threads': 16,
    'omp_scheduling_type': 0,
    'omp_monotonic': 0,
    'omp_dynamic': 0,
    'permutation': '(1, 0, 4, 3, 2)'
}
```

### 4. Set Fidelity Settings

Control the accuracy vs. speed trade-off:

```python
fidelity_settings = {
    "iterations": 15,        # Number of iterations per measurement
    "repeats": 5,           # Number of repeat measurements
    "wait_after_run": 1,    # Seconds to wait after each run
    "wait_between_repeats": 1  # Seconds between repeats
}
```

### 5. Run the Benchmark

```python
result = benchmark.query(query, fidelity_settings)
print(f"Execution time: {result['compute_time']} ms")
print(f"Energy consumption: {result['energy']} J")
```

## Complete Example

```python
import catbench as cb

# Create benchmark instance
benchmark = cb.benchmark('spmm', dataset='2630')

# Define configuration
query = {
    'chunk_size': 32,
    'unroll_factor': 2,
    'omp_chunk_size': 1,
    'omp_num_threads': 10,
    'omp_scheduling_type': 1,
    'omp_monotonic': 0,
    'omp_dynamic': 0,
    'permutation': '(0, 1, 2, 3, 4)'
}

fidelity = {
    "iterations": 15,
    "repeats": 5,
    "wait_after_run": 1,
    "wait_between_repeats": 1
}

# Run benchmark
result = benchmark.query(query, fidelity)

# Print results
print(f"Configuration: {query}")
print(f"Compute time: {result['compute_time']:.2f} ms")
print(f"Energy: {result['energy']:.2f} J")
```

## Next Steps

- Explore [available benchmarks](benchmarks.md) and their parameters
- Learn about [hardware setup](deployment.md) for real benchmarking
- Check out more [examples](examples.md)
- Read the [API reference](api-reference.md) for detailed documentation