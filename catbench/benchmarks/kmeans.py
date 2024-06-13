from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace
from interopt.parameter import IntExponential, Constraint
from catbench.benchmarks.rise import rise_metrics, rise_objectives, rise_fidelity_params


def get_kmeans_definition():
    return ProblemDefinition(
        'kmeans', SearchSpace(
            params=[
                IntExponential(name='tuned_gs0', bounds=(1, 1024),  default=256,    base=2),
                IntExponential(name='tuned_gs1', bounds=(1, 1024),  default=1024,   base=2),
                IntExponential(name='tuned_ls0', bounds=(1, 1024),  default=1,      base=2),
                IntExponential(name='tuned_ls1', bounds=(1, 1024),  default=8,      base=2),
            ],
            constraints = [Constraint(constraint=constraint_string, dependent_params=dependent_params) for constraint_string, dependent_params in [
                ('tuned_gs0 % tuned_ls0 == 0', ['tuned_gs0', 'tuned_ls0']),
                ('tuned_gs1 % tuned_ls1 == 0', ['tuned_gs1', 'tuned_ls1']),
                ('tuned_ls0 * tuned_ls1 <= 1024', ['tuned_ls0', 'tuned_ls1'])
            ]],
            metrics=rise_metrics,
            objectives=rise_objectives,
            fidelity_params=rise_fidelity_params
        )
    )
