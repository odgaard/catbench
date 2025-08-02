# API Reference

## Core Functions

### `catbench.benchmark()`

Creates a benchmark instance for the specified benchmark type.

```python
benchmark(name, dataset=None, server_addresses=None, port=50051)
```

**Parameters:**
- `name` (str): The benchmark name (e.g., 'spmm', 'asum', 'mm')
- `dataset` (str, optional): Dataset to use:
  - Surrogate mode: dataset name (e.g., '2630', 'titanv', 'rtxtitan')
  - Tabular mode: 'test' or path to CSV file
  - Hardware mode: 'hardware_run' or 'cluster_run'
- `server_addresses` (list, optional): List of server addresses for hardware benchmarking
- `port` (int, optional): Port for gRPC communication (default: 50051)

**Returns:**
- Benchmark instance with a `query()` method

**Example:**
```python
import catbench as cb

# Surrogate benchmark
bench = cb.benchmark('spmm')

# Hardware benchmark
bench = cb.benchmark('spmm', dataset='hardware_run', 
                    server_addresses=['192.168.1.100'])
```

## Benchmark Instance Methods

### `benchmark.query()`

Executes a benchmark with the given configuration.

```python
query(configuration, fidelity_settings)
```

**Parameters:**
- `configuration` (dict): Benchmark-specific parameters
- `fidelity_settings` (dict): Execution settings

**Returns:**
- dict: Results containing 'compute_time' and 'energy' (if available)

## Fidelity Settings

Control the execution and measurement accuracy:

### TACO Benchmarks
```python
fidelity_settings = {
    "iterations": 15,           # Number of iterations
    "repeats": 5,              # Number of measurements
    "wait_after_run": 1,       # Seconds to wait after run
    "wait_between_repeats": 1  # Seconds between repeats
}
```

### RISE Benchmarks
```python
fidelity_settings = {
    "iterations": 100,    # Number of iterations
    "timeouts": 60000    # Timeout in milliseconds
}
```

## Benchmark Parameters

### SpMM (Sparse Matrix-Matrix Multiplication)
```python
configuration = {
    'chunk_size': int,           # Loop tiling size
    'unroll_factor': int,        # Loop unrolling factor
    'omp_chunk_size': int,       # OpenMP chunk size
    'omp_num_threads': int,      # Number of OpenMP threads
    'omp_scheduling_type': int,  # 0: static, 1: dynamic
    'omp_monotonic': int,        # 0 or 1
    'omp_dynamic': int,          # 0 or 1
    'permutation': str           # Loop permutation (e.g., '(0,1,2,3,4)')
}
```

### ASUM (Absolute Sum)
```python
configuration = {
    "tuned_sp0": int,     # Split factor 0
    "tuned_gs0": int,     # Group size 0
    "tuned_stride": int,  # Memory stride
    "tuned_sp1": int,     # Split factor 1
    "tuned_ls0": int      # Local size 0
}
```

### MM (Matrix Multiplication)
```python
configuration = {
    "tuned_tile_i": int,      # Tile size for i dimension
    "tuned_tile_j": int,      # Tile size for j dimension
    "tuned_tile_k": int,      # Tile size for k dimension
    "tuned_reg_tile_i": int,  # Register tile i
    "tuned_reg_tile_j": int,  # Register tile j
    "tuned_wg_i": int,        # Work group i
    "tuned_wg_j": int         # Work group j
}
```

## Server Management

### Running a gRPC Server

For hardware benchmarking, start a gRPC server:

```bash
# TACO benchmarks
docker run --network host --privileged -it \
    sisef/catbench-taco:0.0.1 -o SpMM

# RISE benchmarks with GPU
docker run --network host --privileged --gpus all -it \
    sisef/catbench-rise:0.0.1 asumTuning
```

### Cluster Mode

Start the CATBench server manager:

```bash
python -m catbench --benchmark spmm --dataset cluster \
    --servers server1.com server2.com server3.com
```

Connect from client:
```python
benchmark = cb.benchmark("spmm", dataset="cluster_run", 
                        port=50050, 
                        server_addresses=["manager.server.com"])
```

## Error Handling

```python
try:
    result = benchmark.query(config, fidelity)
except Exception as e:
    print(f"Benchmark failed: {e}")
```

## Available Benchmarks

### TACO Suite
- `spmm` - Sparse Matrix-Matrix Multiplication
- `spmv` - Sparse Matrix-Vector Multiplication
- `mttkrp` - Matricized Tensor Times Khatri-Rao Product
- `sddmm` - Sampled Dense-Dense Matrix Multiplication
- `ttv` - Tensor-Times-Vector

### RISE Suite
- `asum` - Absolute Sum
- `mm` - Matrix Multiplication
- `scal` - Scalar Multiplication
- `harris` - Harris Corner Detection
- `kmeans` - K-means Clustering
- `stencil` - Stencil Operations
- `carl` - Carl Benchmark
- `intersect` - Set Intersection