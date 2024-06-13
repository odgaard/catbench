from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace
from interopt.parameter import IntExponential, Constraint

from catbench.benchmarks.taco import taco_metrics, taco_objectives, taco_common_parameters, taco_fidelity_params

def get_ttv_definition():
    return ProblemDefinition(
        'TTV', SearchSpace(
            params=[
                IntExponential(name='chunk_size_i',     bounds=(2, 256),    default=16,     base=2),
                IntExponential(name='chunk_size_fpos',  bounds=(2, 256),    default=2,      base=2),
                IntExponential(name='chunk_size_k',     bounds=(2, 256),    default=2,      base=2),
                IntExponential(name='omp_chunk_size',   bounds=(1, 32),     default=2,      base=2),
            ] + taco_common_parameters,
            constraints = [Constraint(
                constraint=constraint_string,
                dependent_params=dependent_params) for constraint_string, dependent_params in [
                ("(permutation[0] == 4)"\
                " | ((permutation[0] == 0) & (permutation[1] == 1))"\
                " | ((permutation[0] == 1) & (permutation[1] == 0))"\
                " | ((permutation[0] == 0) & (permutation[1] == 4))"\
                " | ((permutation[0] == 1) & (permutation[1] == 4))", ['permutation']),
            ]],
            metrics=taco_metrics,
            objectives=taco_objectives,
            fidelity_params=taco_fidelity_params
        )
    )
