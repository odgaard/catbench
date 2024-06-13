from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace
from interopt.parameter import IntExponential, Constraint

from catbench.benchmarks.rise import rise_objectives, rise_metrics, rise_fidelity_params

def get_scal_definition():
    data_size = 33554432
    return ProblemDefinition(
        'scal', SearchSpace(
            params=[
                IntExponential(name='tuned_ls1', bounds=(1, 1024),      default=1,      base=2),
                IntExponential(name='tuned_gs0', bounds=(1, 1024),      default=8,      base=2),
                IntExponential(name='tuned_s0',  bounds=(1, data_size), default=2048,   base=2),
                IntExponential(name='tuned_vec', bounds=(2, 16),        default=2,      base=2),
                IntExponential(name='tuned_gs1', bounds=(1, 1024),      default=128,    base=2),
                IntExponential(name='tuned_ls0', bounds=(1, 1024),      default=8,      base=2),
                IntExponential(name='tuned_s1',  bounds=(1, data_size), default=16,     base=2),
            ],
            constraints = [Constraint(
                constraint=constraint_string,
                dependent_params=dependent_params) for constraint_string, dependent_params in [
                ('tuned_gs0 % tuned_ls0 == 0', ['tuned_gs0', 'tuned_ls0']),
                ('tuned_gs1 % tuned_ls1 == 0', ['tuned_gs1', 'tuned_ls1']),
                ('tuned_ls0 * tuned_ls1 <= 1024', ['tuned_ls0', 'tuned_ls1']),
                ('(tuned_s0 % (tuned_s1 * tuned_vec) == 0) and ((tuned_s0 * (1 / (tuned_s1 * tuned_vec))) >= 1) and ((tuned_s0 * tuned_s1 * (1 / (tuned_s1 * tuned_vec))) >= 1) and ((tuned_s0 * tuned_s1) >= 0) and ((tuned_s0 * tuned_s1) % (tuned_s1 * tuned_vec) == 0) and ((tuned_s0 * tuned_s1 * tuned_vec * (1 / (tuned_s1 * tuned_vec))) >= 1)', ['tuned_s0', 'tuned_s1', 'tuned_vec']),
                (f'{data_size} * tuned_s1 * tuned_vec * (1 / (tuned_s1 * tuned_vec)) >= 1', ['tuned_s1', 'tuned_vec']),
            ]],
            metrics=rise_metrics,
            objectives=rise_objectives,
            fidelity_params=rise_fidelity_params
        )
    )
