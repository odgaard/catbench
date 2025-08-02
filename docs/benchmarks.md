# Available Benchmarks

CATBench includes two main benchmark suites: TACO (Tensor Algebra Compiler) and RISE (Rewrite-based Intrinsically Parallel Intermediate Language).

## TACO Benchmarks

TACO benchmarks focus on sparse tensor operations commonly used in scientific computing and machine learning.

### SpMM - Sparse Matrix-Matrix Multiplication

Computes C = A × B where A is sparse and B is dense.

**Parameters:**
- `chunk_size` (int): Loop tiling chunk size [1-128]
- `unroll_factor` (int): Loop unrolling factor [1-16]
- `omp_chunk_size` (int): OpenMP chunk size [1-16]
- `omp_num_threads` (int): Number of OpenMP threads [1-max_threads]
- `omp_scheduling_type` (int): 0=static, 1=dynamic
- `omp_monotonic` (int): Monotonic scheduling flag [0,1]
- `omp_dynamic` (int): Dynamic adjustment flag [0,1]
- `permutation` (str): Loop order permutation, e.g., "(0,1,2,3,4)"

**Available Datasets:** 2630, titanv, test

### SpMV - Sparse Matrix-Vector Multiplication

Computes y = A × x where A is sparse.

**Parameters:**
- `chunk_size` (int): Loop chunk size
- `omp_num_threads` (int): Number of threads
- `omp_scheduling_type` (int): Scheduling policy
- `parallel_method` (str): Parallelization strategy

**Available Datasets:** 2630, titanv, test

### MTTKRP - Matricized Tensor Times Khatri-Rao Product

Performs tensor decomposition operations.

**Parameters:**
- `chunk_size` (int): Tiling size
- `unroll_factor` (int): Unrolling factor
- `omp_num_threads` (int): Thread count
- `mode` (int): Tensor mode [0-2]
- `permutation` (str): Loop permutation

**Available Datasets:** 2630, test

### SDDMM - Sampled Dense-Dense Matrix Multiplication

Computes S ⊙ (A × B) where S is a sparse sampling matrix.

**Parameters:**
- `chunk_size` (int): Chunk size
- `unroll_factor` (int): Unroll factor
- `omp_num_threads` (int): Threads
- `permutation` (str): Loop order

**Available Datasets:** 2630, test

### TTV - Tensor-Times-Vector

Multiplies a tensor by vectors along specified modes.

**Parameters:**
- `chunk_size` (int): Tiling parameter
- `omp_num_threads` (int): Thread count
- `mode_order` (str): Mode processing order

**Available Datasets:** 2630, test

## RISE Benchmarks

RISE benchmarks target GPU computation patterns with a focus on parallelization strategies.

### ASUM - Absolute Sum

Computes the sum of absolute values of array elements.

**Parameters:**
- `tuned_sp0` (int): Split factor 0 [powers of 2]
- `tuned_gs0` (int): Group size 0 [powers of 2]
- `tuned_stride` (int): Memory access stride
- `tuned_sp1` (int): Split factor 1 [powers of 2]
- `tuned_ls0` (int): Local size 0 [powers of 2]

**Available Datasets:** rtxtitan, titanv, test

### MM - Matrix Multiplication

Dense matrix multiplication C = A × B.

**Parameters:**
- `tuned_tile_i` (int): I-dimension tile size [8,16,32,64]
- `tuned_tile_j` (int): J-dimension tile size [8,16,32,64]
- `tuned_tile_k` (int): K-dimension tile size [8,16,32]
- `tuned_reg_tile_i` (int): Register tile I [1,2,4,8]
- `tuned_reg_tile_j` (int): Register tile J [1,2,4,8]
- `tuned_wg_i` (int): Work group I size [64,128,256]
- `tuned_wg_j` (int): Work group J size [64,128,256]

**Available Datasets:** rtxtitan, titanv, test

### Scal - Scalar Multiplication

Multiplies array elements by a scalar value.

**Parameters:**
- `tuned_gs0` (int): Group size
- `tuned_ls0` (int): Local size
- `tuned_vec_width` (int): Vectorization width [1,2,4,8]

**Available Datasets:** rtxtitan, test

### Harris - Harris Corner Detection

Image processing algorithm for corner detection.

**Parameters:**
- `tuned_tile_x` (int): X-dimension tile
- `tuned_tile_y` (int): Y-dimension tile
- `tuned_load_overlap` (int): Overlap loading strategy
- `tuned_pad` (int): Padding size

**Available Datasets:** rtxtitan, test

### K-means - K-means Clustering

Clustering algorithm for data analysis.

**Parameters:**
- `tuned_features_tile` (int): Feature tiling
- `tuned_points_tile` (int): Points tiling
- `tuned_clusters` (int): Number of clusters
- `tuned_local_points` (int): Local points size

**Available Datasets:** rtxtitan, test

### Stencil - Stencil Operations

Structured grid computations common in scientific simulations.

**Parameters:**
- `tuned_tile_x` (int): X tile size
- `tuned_tile_y` (int): Y tile size
- `tuned_tile_z` (int): Z tile size
- `tuned_load_method` (str): Loading strategy

**Available Datasets:** rtxtitan, test

## Benchmark Selection Guide

### When to use TACO benchmarks:
- Evaluating sparse linear algebra performance
- CPU-focused optimizations
- OpenMP parallelization studies
- Compiler optimization research

### When to use RISE benchmarks:
- GPU performance evaluation
- Parallel pattern optimization
- Memory access pattern studies
- Heterogeneous computing research

## Performance Metrics

All benchmarks return at minimum:
- `compute_time` (float): Execution time in milliseconds

Hardware benchmarks additionally return:
- `energy` (float): Energy consumption in Joules (if available)

## Dataset Information

### Default Datasets
- TACO benchmarks: `2630` (Intel Xeon E5-2630 v3)
- RISE benchmarks: `rtxtitan` (NVIDIA RTX Titan)

### Test Datasets
- Small datasets for quick testing: use `test` as dataset parameter
- Located in `datasets/` directory

### Hardware Datasets
- `hardware_run`: Direct hardware execution
- `cluster_run`: Distributed cluster execution

## Custom Benchmarks

To add custom benchmarks, create a new file in `catbench/benchmarks/` following the existing pattern:

```python
class MyBenchmark:
    def __init__(self):
        self.name = "mybench"
        self.parameters = {
            'param1': {'type': int, 'range': [1, 100]},
            'param2': {'type': str, 'values': ['a', 'b', 'c']}
        }
    
    def validate_config(self, config):
        # Validate parameter values
        pass
    
    def format_query(self, config, fidelity):
        # Format for execution
        pass
```