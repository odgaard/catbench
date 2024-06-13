import argparse

from catbench.main import benchmark
from interopt.runner.grpc_runner.server import Server

def main():
    parser = argparse.ArgumentParser(description="Run a benchmark")
    parser.add_argument('--benchmark', type=str,
                        help='Benchmark to use', default="spmm")
    parser.add_argument('--dataset', type=str,
                        help='Dataset to use', default="server")
    parser.add_argument('--servers', type=str, nargs='+',
                        help='List of servers to use for benchmarking',
                        default=["localhost"])
    parser.add_argument('--objectives', type=str, nargs='+',
                        help='List of objectives to use for benchmarking',
                        default=None)
    parser.add_argument('--enable_model', type=bool, default=False,
                        help='Enable surrogate model')
    parser.add_argument('--enable_tabular', type=bool, default=True,
                        help='Enable caching of datasets')
    parser.add_argument('--enable_download', type=bool, default=True,
                        help='Enable downloading of datasets')
    parser.add_argument('--interopt_port', type=int, default=50050,
                        help='Port to use for the server')

    args = parser.parse_args()

    study = benchmark(
        args.benchmark,
        enable_tabular=args.enable_tabular, enable_model=args.enable_model,
        enable_download=args.enable_download, dataset=args.dataset,
        enabled_objectives=args.objectives,  server_addresses=args.servers)

    server = Server(study, port=args.interopt_port)
    server.start()

if __name__ == "__main__":
    main()
