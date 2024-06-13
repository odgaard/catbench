from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace
from interopt.parameter import IntExponential, Constraint

from catbench.benchmarks.taco import taco_metrics, taco_objectives, taco_common_parameters, taco_fidelity_params

def get_mttkrp_definition():
    return ProblemDefinition(
        'MTTKRP', SearchSpace(
            params=[
                IntExponential(name='chunk_size',       bounds=(1, 1024),   default=None, base=2),
                IntExponential(name='unroll_factor',    bounds=(1, 1024),   default=None, base=2),
                IntExponential(name='omp_chunk_size',   bounds=(1, 256),    default=None, base=2),
            ] + taco_common_parameters,
            constraints=[Constraint(constraint=constraint_string, dependent_params=dependent_params) for constraint_string, dependent_params in [
                ('unroll_factor < chunk_size', ['unroll_factor', 'chunk_size']),
            ]],
            metrics=taco_metrics,
            objectives=taco_objectives,
            fidelity_params=taco_fidelity_params
        )
    )
