from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace
from interopt.parameter import IntExponential, Constraint

from catbench.benchmarks.rise import rise_metrics, rise_objectives, rise_fidelity_params

def get_mm_definition():
    return ProblemDefinition(
        'mm', SearchSpace(
            params=[
                IntExponential(name='tuned_v3',  bounds=(4, 1024),  default=8,      base=2),
                IntExponential(name='tuned_v4',  bounds=(1, 1024),  default=16,     base=2),
                IntExponential(name='tuned_v5',  bounds=(4, 1024),  default=16,     base=2),
                IntExponential(name='tuned_v6',  bounds=(4, 1024),  default=64,     base=2),
                IntExponential(name='tuned_v7',  bounds=(4, 1024),  default=8,      base=2),
                IntExponential(name='tuned_v8',  bounds=(1, 1024),  default=16,     base=2),
                IntExponential(name='tuned_ls0', bounds=(1, 1024),  default=32,     base=2),
                IntExponential(name='tuned_ls1', bounds=(1, 1024),  default=16,     base=2),
                IntExponential(name='tuned_gs0', bounds=(1, 1024),  default=1024,   base=2),
                IntExponential(name='tuned_gs1', bounds=(1, 1024),  default=16,     base=2),
            ],
            constraints = [Constraint(constraint=constraint_string, dependent_params=dependent_params) for constraint_string, dependent_params in [
                ('tuned_v7 % tuned_v3 == 0', ['tuned_v7', 'tuned_v3']),
                ('tuned_v5 % tuned_v4 == 0', ['tuned_v5', 'tuned_v4']),
                ('tuned_v5 * tuned_v8 % tuned_v6 == 0', ['tuned_v5', 'tuned_v8', 'tuned_v6']),
                ('tuned_gs0 % tuned_ls0 == 0', ['tuned_gs0', 'tuned_ls0']),
                ('(tuned_gs1 % tuned_ls1 == 0) and (tuned_ls0 * tuned_ls1 <= 1024)', ['tuned_gs1', 'tuned_ls1', 'tuned_ls0']),
                ('49152 - tuned_v5 * 1 * 4 - tuned_v5 * 1 * 4 - 4 * 1 * 1 >= 0', ['tuned_v5']),
                ('49152 - tuned_v5 * tuned_v7 * 4 - tuned_v5 * 1 * 4 - 4 * tuned_v7 * 1 >= 0', ['tuned_v5', 'tuned_v7']),
                ('49152 - tuned_v5 * tuned_v7 * 4 - tuned_v5 * tuned_v8 * 4 - 4 * tuned_v7 * tuned_v8 >= 0', ['tuned_v5', 'tuned_v7', 'tuned_v8']),
            ]],
            metrics=rise_metrics,
            objectives=rise_objectives,
            fidelity_params=rise_fidelity_params
        )
    )
