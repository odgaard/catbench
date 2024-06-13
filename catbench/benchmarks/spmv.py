from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace
from interopt.parameter import IntExponential, Constraint

from catbench.benchmarks.taco import taco_metrics, taco_objectives, taco_common_parameters, taco_fidelity_params

def get_spmv_definition():
    return ProblemDefinition(
        'SpMV', SearchSpace(
            params=[
                IntExponential(name='chunk_size',       bounds=(1, 1024),   default=16, base=2),
                IntExponential(name='chunk_size2',      bounds=(1, 64),     default=2,  base=2),
                IntExponential(name='chunk_size3',      bounds=(1, 64),     default=2,  base=2),
                IntExponential(name='omp_chunk_size',   bounds=(1, 256),    default=2,  base=2)
            ] + taco_common_parameters,
            constraints=[Constraint
                         (constraint=constraint_string,
                          dependent_params=dependent_params) for constraint_string, dependent_params in [
                ('permutation[4] == 4', ['permutation']),
            ]],
            metrics=taco_metrics,
            objectives=taco_objectives,
            fidelity_params=taco_fidelity_params
        )
    )
