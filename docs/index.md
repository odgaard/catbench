# CATBench Documentation

Welcome to the CATBench documentation! CATBench is a powerful benchmarking framework designed for evaluating computational performance and energy efficiency of compiler benchmarks.

## What is CATBench?

CATBench provides a unified interface for running benchmarks in three different modes:

- **Surrogate Benchmarking**: Uses machine learning (CatBoost) models for fast performance prediction
- **Tabular Benchmarking**: Leverages precomputed data for reproducible results
- **Hardware Benchmarking**: Runs actual benchmarks on real hardware via gRPC

## Key Features

- 🚀 **Multiple Execution Modes**: Choose between surrogate models, tabular data, or real hardware
- 📊 **Built-in Benchmarks**: Includes TACO and RISE benchmark suites
- 🔧 **Easy Integration**: Simple Python API for benchmark execution
- 📈 **Performance Metrics**: Measure both execution time and energy consumption
- 🌐 **Distributed Execution**: Support for cluster deployments via gRPC
- 🐳 **Docker Support**: Pre-built containers for easy deployment

## Quick Start

```python
import catbench as cb

# Create a benchmark instance
benchmark = cb.benchmark('spmm')

# Define query parameters
query = {
    'chunk_size': 16, 
    'unroll_factor': 16,
    'omp_num_threads': 16,
    # ... more parameters
}

# Run the benchmark
result = benchmark.query(query, fidelity_settings)
```

## Documentation Contents

- [Getting Started](getting-started.md) - Installation and basic usage
- [Benchmarks](benchmarks.md) - Available benchmark types and parameters
- [API Reference](api-reference.md) - Detailed API documentation
- [Examples](examples.md) - Code examples and tutorials
- [Deployment](deployment.md) - Hardware setup and cluster configuration
- [Contributing](contributing.md) - How to contribute to CATBench

## Supported Benchmarks

### TACO Benchmarks
- SpMM (Sparse Matrix-Matrix Multiplication)
- SpMV (Sparse Matrix-Vector Multiplication)
- MTTKRP (Matricized Tensor Times Khatri-Rao Product)
- SDDMM (Sampled Dense-Dense Matrix Multiplication)
- TTV (Tensor-Times-Vector)

### RISE Benchmarks
- ASUM (Absolute Sum)
- MM (Matrix Multiplication)
- Scal (Scalar Multiplication)
- Harris (Harris Corner Detection)
- K-means Clustering
- Stencil Operations

## License

CATBench is open-source software. See the [LICENSE](https://github.com/odgaard/catbench/blob/main/LICENSE) file for details.