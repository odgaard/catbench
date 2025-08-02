# CATBench: Benchmarking Framework

CATBench is a benchmarking framework designed for evaluating computational performance and energy efficiency of compiler benchmarks. It allows users to define and run benchmarks either on actual hardware via gRPC, using Catboost-based surrogate models, or using precomputed tabular data.

## Getting Started

To use CATBench, you need to define a benchmark instance and then run queries against it. The framework offers three primary modes of operation:

1. **Surrogate Benchmarking:** This mode trains and uses a Catboost-based surrogate model. It's faster and doesn't require actual hardware resources for computation. Suitable for quick analysis and testing.
2. **Tabular Benchmarking:** This mode uses precomputed data stored in a CSV format. It's useful for reproducing previous runs when you have the exact same software setup and seeds, but you e.g. don't have the hardware available.
2. **Hardware Benchmarking (gRPC):** This mode involves running the benchmark on actual hardware. It provides more real-world results but requires a setup with the necessary hardware resources and the gRPC service running.


# Basic example of surrogate benchmarking
```python
import catbench as cb

# For Surrogate Benchmarking
benchmark = cb.benchmark('spmm')
```

## Running Queries
After defining a benchmark instance, you can run queries against it:

```python
fidelity_setting = {
    "iterations": 15,
    "repeats": 5,
    "wait_after_run": 1,
    "wait_between_repeats": 1
}
query = {
    'chunk_size': 16, 'unroll_factor': 16, 
    'omp_chunk_size': 2, 'omp_num_threads': 16, 
    'omp_scheduling_type': 0, 'omp_monotonic': 0, 
    'omp_dynamic': 0, 'permutation': '(1, 0, 4, 3, 2)'
}

objectives_result = benchmark.query(query, fidelity_setting)
```

The example above uses the 2630 csv dataset from our paper and will automatically download it to train a surrogate model.
If you wish to use a different dataset it can be specified using e.g. "dataset=titanv". The default dataset for the RISE benchmarks is "rtxtitan".


# Hardware Benchmarking (gRPC)
```python
import catbench as cb

# For hardware benchmarking on local machine
hardware_benchmark = cb.benchmark("spmm", dataset="hardware_run", server_addresses=["localhost"])

# For hardware benchmarking on remote machine
hardware_benchmark = cb.benchmark("spmm", dataset="hardware_run", server_addresses=["192.168.1.100"])
```

### Setup gRPC server
Setup the gRPC server for the SpMM benchmark.
for the SpMM benchmark:


#### For TACO benchmarks
```bash
docker run --network host --privileged -it sisef/catbench-taco:0.0.1 -o SpMM
```

#### For RISE benchmarks
```bash
docker run --network host --privileged --gpus all -it sisef/catbench-rise:0.0.1 asumTuning
```

#### For CPU energy measurements
For CPU energy measurements the RAPL interface needs to be accessible. By default a user must have administrator privileges to read this file. The docker container might crash on startup with the following error:

```sh
terminate called after throwing an instance of 'std::runtime_error'
  what():  Failed to open file: /sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj
```

You would then need to run this command with sudo or ask you system administrator to make the RAPL file readable for your user.

```sh
sudo chmod -R a+r /sys/class/powercap/intel-rapl
```

# Cluster setup
For a cluster setup you simplify start the Docker containers on the machines that you want to use.
Then run the following command on a machine that will host the catbench server manager. The servers are the ip addresses or the domains of the servers you have started.
```sh
python3 -m catbench --benchmark spmm --dataset cluster --servers server1.mydomain.com server2.mydomain.com server3.mydomain.com
```

The server address for the catbench client should then forward requests to the machine that is running the catbench server manager.
By default the catbench server runs on port 50050, so the client needs to connect to this port, by passing `port=50050` as an argument to `cb.benchmark`.

```python
cluster_benchmark = cb.benchmark("spmm", dataset="cluster_run", port=50050, server_addresses=["your.catbench.server.com"])
```

You can then use the interface from the client as normal. The configurations are automatically sent and queued to run on any of the available servers.

