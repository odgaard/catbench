from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace
from interopt.parameter import IntExponential, Constraint
from catbench.benchmarks.rise import rise_metrics, rise_objectives, rise_fidelity_params

def get_asum_definition():
    return ProblemDefinition('asum', SearchSpace(
        params=[
            IntExponential(name='tuned_sp0',    bounds=(1, 16777216),   default=4096, base=2),
            IntExponential(name='tuned_gs0',    bounds=(1, 1024),       default=16,   base=2),
            IntExponential(name='tuned_stride', bounds=(1, 16777216),   default=2,    base=2),
            IntExponential(name='tuned_sp1',    bounds=(256, 16777216), default=1024, base=2),
            IntExponential(name='tuned_ls0',    bounds=(1, 1024),       default=16,   base=2)
        ],
        constraints = [Constraint(
            constraint=constraint_string,
            dependent_params=dependent_params) for constraint_string, dependent_params in [
            ('tuned_sp0 % tuned_sp1 == 0', ['tuned_sp0', 'tuned_sp1']),
            ('tuned_sp0 >= tuned_sp1', ['tuned_sp0', 'tuned_sp1']),
            ('tuned_sp0 >= tuned_sp1 * tuned_stride', ['tuned_sp0', 'tuned_sp1', 'tuned_stride']),
            ('tuned_gs0 % tuned_ls0 == 0', ['tuned_gs0', 'tuned_ls0'])
        ]],
        metrics=rise_metrics,
        objectives=rise_objectives,
        fidelity_params=rise_fidelity_params
    ))
