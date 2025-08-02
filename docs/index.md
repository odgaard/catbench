# Welcome to CATBench

CATBench is a powerful benchmarking framework designed for evaluating computational performance and energy efficiency of compiler benchmarks.

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Get up and running with CATBench in minutes

    [:octicons-arrow-right-24: Getting started](getting-started.md)

-   :material-book-open-variant:{ .lg .middle } **User Guide**

    ---

    Learn about benchmarks, parameters, and best practices

    [:octicons-arrow-right-24: Read the guide](benchmarks.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete API documentation with examples

    [:octicons-arrow-right-24: API docs](api-reference.md)

-   :material-server:{ .lg .middle } **Deployment**

    ---

    Deploy on hardware, clusters, or containers

    [:octicons-arrow-right-24: Deploy CATBench](deployment.md)

</div>

## Overview

CATBench provides a unified interface for running benchmarks in three different modes:

!!! info "Execution Modes"

    === "Surrogate Benchmarking"
    
        Uses machine learning (CatBoost) models for fast performance prediction without requiring actual hardware.
        
        ```python
        benchmark = cb.benchmark('spmm')  # Default mode
        ```

    === "Tabular Benchmarking"
    
        Leverages precomputed data for reproducible results from CSV files.
        
        ```python
        benchmark = cb.benchmark('spmm', dataset='test')
        ```

    === "Hardware Benchmarking"
    
        Runs actual benchmarks on real hardware via gRPC for accurate measurements.
        
        ```python
        benchmark = cb.benchmark('spmm', dataset='hardware_run', 
                                server_addresses=['localhost'])
        ```

## Key Features

<div class="grid" markdown>

:material-speedometer:{ .lg } **Performance**
: Fast surrogate models for quick iteration

:material-chart-line:{ .lg } **Metrics**
: Measure execution time and energy consumption

:material-docker:{ .lg } **Containerized**
: Pre-built Docker images for easy deployment

:material-server-network:{ .lg } **Distributed**
: Built-in support for cluster deployments

</div>

## Quick Example

```python
import catbench as cb

# Create a benchmark instance
benchmark = cb.benchmark('spmm')

# Define configuration
query = {
    'chunk_size': 16, 
    'unroll_factor': 16,
    'omp_num_threads': 16,
    'omp_scheduling_type': 0,
    'omp_chunk_size': 2,
    'omp_monotonic': 0,
    'omp_dynamic': 0,
    'permutation': '(0, 1, 2, 3, 4)'
}

# Set fidelity parameters
fidelity = {
    "iterations": 15,
    "repeats": 5,
    "wait_after_run": 1,
    "wait_between_repeats": 1
}

# Run benchmark
result = benchmark.query(query, fidelity)
print(f"Execution time: {result['compute_time']:.2f} ms")
```

## Supported Benchmarks

=== "TACO Suite"

    Tensor Algebra Compiler benchmarks for sparse operations:
    
    - **SpMM** - Sparse Matrix-Matrix Multiplication
    - **SpMV** - Sparse Matrix-Vector Multiplication  
    - **MTTKRP** - Matricized Tensor Times Khatri-Rao Product
    - **SDDMM** - Sampled Dense-Dense Matrix Multiplication
    - **TTV** - Tensor-Times-Vector

=== "RISE Suite"

    GPU-focused benchmarks with parallel patterns:
    
    - **ASUM** - Absolute Sum
    - **MM** - Matrix Multiplication
    - **Scal** - Scalar Multiplication
    - **Harris** - Harris Corner Detection
    - **K-means** - Clustering Algorithm
    - **Stencil** - Stencil Operations

## Next Steps

<div class="grid cards" markdown>

-   :fontawesome-brands-python: **Install CATBench**

    ```bash
    pip install catbench
    ```

-   :material-test-tube: **Try Examples**

    Explore our [example gallery](examples.md) with ready-to-run code

-   :octicons-git-pull-request-24: **Contribute**

    Help improve CATBench - [contribution guide](contributing.md)

</div>