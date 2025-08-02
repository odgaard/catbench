# Deployment Guide

This guide covers deploying CATBench for hardware benchmarking, including single-node and cluster setups.

## Prerequisites

### System Requirements
- Linux operating system (tested on Ubuntu 20.04+, CentOS 7+)
- Docker installed and running
- Python 3.7 or higher

### Hardware Requirements
- For CPU benchmarks: Modern multi-core processor
- For GPU benchmarks: NVIDIA GPU with CUDA support
- For energy measurements: Intel CPU with RAPL support

## Single Node Deployment

### 1. Install CATBench

```bash
pip install catbench
```

### 2. Start gRPC Server

#### For TACO Benchmarks (CPU)

```bash
# SpMM benchmark
docker run --network host --privileged -it \
    sisef/catbench-taco:0.0.1 -o SpMM

# SpMV benchmark
docker run --network host --privileged -it \
    sisef/catbench-taco:0.0.1 -o SpMV

# Multiple benchmarks
docker run --network host --privileged -it \
    sisef/catbench-taco:0.0.1 -o SpMM SpMV MTTKRP
```

#### For RISE Benchmarks (GPU)

```bash
# Ensure NVIDIA Docker runtime is installed
docker run --network host --privileged --gpus all -it \
    sisef/catbench-rise:0.0.1 asumTuning

# Other RISE benchmarks
docker run --network host --privileged --gpus all -it \
    sisef/catbench-rise:0.0.1 mmTuning

docker run --network host --privileged --gpus all -it \
    sisef/catbench-rise:0.0.1 harrisTuning
```

### 3. Enable Energy Measurements

For CPU energy measurements via Intel RAPL:

```bash
# Make RAPL interface readable (requires sudo)
sudo chmod -R a+r /sys/class/powercap/intel-rapl

# Or add to system startup
echo 'chmod -R a+r /sys/class/powercap/intel-rapl' | \
    sudo tee /etc/rc.local
```

### 4. Test Connection

```python
import catbench as cb

# Test local connection
benchmark = cb.benchmark('spmm', 
                        dataset='hardware_run',
                        server_addresses=['localhost'])

config = {
    'chunk_size': 16,
    'unroll_factor': 2,
    'omp_chunk_size': 1,
    'omp_num_threads': 4,
    'omp_scheduling_type': 0,
    'omp_monotonic': 0,
    'omp_dynamic': 0,
    'permutation': '(0, 1, 2, 3, 4)'
}

result = benchmark.query(config, {"iterations": 5, "repeats": 2})
print(f"Connection successful! Time: {result['compute_time']} ms")
```

## Cluster Deployment

### 1. Deploy Worker Nodes

On each worker machine:

```bash
# TACO worker
docker run -d --name catbench-worker \
    --network host --privileged \
    --restart unless-stopped \
    sisef/catbench-taco:0.0.1 -o SpMM SpMV MTTKRP

# RISE worker (GPU nodes)
docker run -d --name catbench-worker \
    --network host --privileged --gpus all \
    --restart unless-stopped \
    sisef/catbench-rise:0.0.1 mmTuning
```

### 2. Start Cluster Manager

On the manager node:

```bash
# Start cluster manager
python -m catbench \
    --benchmark spmm \
    --dataset cluster \
    --servers worker1.domain.com worker2.domain.com worker3.domain.com \
    --port 50050
```

### 3. Configure Firewall

Ensure ports are open:
- Worker nodes: 50051 (default gRPC port)
- Manager node: 50050 (cluster manager port)

```bash
# Example for Ubuntu/Debian
sudo ufw allow 50050/tcp
sudo ufw allow 50051/tcp

# Example for CentOS/RHEL
sudo firewall-cmd --permanent --add-port=50050/tcp
sudo firewall-cmd --permanent --add-port=50051/tcp
sudo firewall-cmd --reload
```

### 4. Client Configuration

```python
import catbench as cb

# Connect to cluster manager
benchmark = cb.benchmark('spmm',
                        dataset='cluster_run',
                        port=50050,
                        server_addresses=['manager.cluster.com'])

# Queries are automatically distributed
result = benchmark.query(config, fidelity)
```

## Docker Deployment Options

### Custom Docker Images

Create a Dockerfile for custom configurations:

```dockerfile
FROM sisef/catbench-taco:0.0.1

# Add custom dependencies
RUN apt-get update && apt-get install -y \
    custom-package

# Set environment variables
ENV OMP_NUM_THREADS=16
ENV RAPL_ENERGY_METER=1

# Custom entrypoint
ENTRYPOINT ["python", "-m", "catbench.server"]
CMD ["-o", "SpMM", "SpMV"]
```

### Docker Compose

For multi-container deployment:

```yaml
version: '3.8'

services:
  catbench-manager:
    image: catbench/manager:latest
    ports:
      - "50050:50050"
    environment:
      - WORKER_ADDRESSES=worker1:50051,worker2:50051
    command: ["--benchmark", "spmm", "--dataset", "cluster"]

  worker1:
    image: sisef/catbench-taco:0.0.1
    privileged: true
    network_mode: host
    command: ["-o", "SpMM", "SpMV"]

  worker2:
    image: sisef/catbench-rise:0.0.1
    privileged: true
    network_mode: host
    runtime: nvidia
    command: ["mmTuning"]
```

## Production Considerations

### 1. Resource Limits

Set Docker resource constraints:

```bash
docker run -d \
    --cpus="8" \
    --memory="16g" \
    --memory-swap="16g" \
    sisef/catbench-taco:0.0.1
```

### 2. Monitoring

Monitor server health:

```python
# Health check endpoint
import requests

response = requests.get('http://worker1:50051/health')
if response.status_code == 200:
    print("Worker healthy")
```

### 3. Logging

Configure logging:

```bash
# Docker logs
docker logs catbench-worker

# Persistent logging
docker run -d \
    -v /var/log/catbench:/logs \
    -e LOG_LEVEL=INFO \
    -e LOG_FILE=/logs/catbench.log \
    sisef/catbench-taco:0.0.1
```

### 4. Security

#### Network Isolation
```bash
# Create dedicated network
docker network create catbench-net

# Run containers on isolated network
docker run -d --network catbench-net ...
```

#### TLS/SSL (if supported)
```python
# Configure secure connection
benchmark = cb.benchmark('spmm',
                        dataset='hardware_run',
                        server_addresses=['worker1:50051'],
                        use_tls=True,
                        cert_path='/path/to/cert.pem')
```

## Troubleshooting

### Common Issues

1. **Container fails to start**
   ```bash
   # Check logs
   docker logs catbench-worker
   
   # Common fix: RAPL permissions
   sudo chmod -R a+r /sys/class/powercap/intel-rapl
   ```

2. **Connection refused**
   ```bash
   # Check if container is running
   docker ps
   
   # Test port connectivity
   telnet localhost 50051
   ```

3. **GPU not available**
   ```bash
   # Install NVIDIA Docker runtime
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
       sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-docker2
   sudo systemctl restart docker
   ```

4. **Performance issues**
   ```bash
   # Disable CPU frequency scaling
   sudo cpupower frequency-set -g performance
   
   # Set CPU affinity
   docker run -d --cpuset-cpus="0-7" ...
   ```

### Diagnostics Script

```bash
#!/bin/bash
# catbench-diagnostics.sh

echo "=== System Information ==="
uname -a
lscpu | grep "Model name"
nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo "No GPU found"

echo -e "\n=== Docker Status ==="
docker --version
docker ps --filter "ancestor=sisef/catbench"

echo -e "\n=== RAPL Permissions ==="
ls -la /sys/class/powercap/intel-rapl/

echo -e "\n=== Network Connectivity ==="
for port in 50050 50051; do
    timeout 1 bash -c "cat < /dev/null > /dev/tcp/localhost/$port" && \
        echo "Port $port: OPEN" || echo "Port $port: CLOSED"
done

echo -e "\n=== Container Logs (last 10 lines) ==="
docker logs --tail 10 catbench-worker 2>&1
```

## Best Practices

1. **Isolation**: Run benchmarks on dedicated hardware when possible
2. **Consistency**: Disable CPU frequency scaling and turbo boost
3. **Monitoring**: Track system metrics during benchmarks
4. **Automation**: Use configuration management (Ansible, Puppet) for cluster deployment
5. **Backup**: Save benchmark results and configurations regularly