from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace
from interopt.parameter import IntExponential, Constraint

from catbench.benchmarks.taco import taco_metrics, taco_objectives, taco_common_parameters, taco_fidelity_params

def get_sddmm_definition():
    return ProblemDefinition(
        'SDDMM', SearchSpace(
            params=[
                IntExponential(name='chunk_size',       bounds=(1, 256),    default=16, base=2),
                IntExponential(name='unroll_factor',    bounds=(1, 64),     default=2,  base=2),
                IntExponential(name='omp_chunk_size',   bounds=(1, 256),    default=2,  base=2),
            ] + taco_common_parameters,
            constraints=[Constraint(
                constraint=constraint_string,
                dependent_params=dependent_params) for constraint_string, dependent_params in [
                ('omp_num_threads % 2 == 0', ['omp_num_threads']),
                ('unroll_factor < chunk_size', ['unroll_factor', 'chunk_size']),
                ('((permutation[2] < permutation[4]) and (permutation[0] < permutation[2]) and (permutation[1] < permutation[2])) or \
                    ((permutation[4] < permutation[2]) and (permutation[0] < permutation[4]) and (permutation[1] < permutation[4]))', ['permutation'])
            ]],
            metrics=taco_metrics,
            objectives=taco_objectives,
            fidelity_params=taco_fidelity_params
        )
    )
