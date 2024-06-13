from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace
from interopt.parameter import Integer, IntExponential, Constraint
from catbench.benchmarks.rise import rise_metrics, rise_objectives, rise_fidelity_params

def get_harris_definition():
    return ProblemDefinition(
        'harris', SearchSpace(
            params=[
                IntExponential(name='tuned_ls0', bounds=(1, 1024),  default=1,  base=2),
                IntExponential(name='tuned_ls1', bounds=(1, 1024),  default=1,  base=2),
                IntExponential(name='tuned_gs0', bounds=(1, 1024),  default=64, base=2),
                IntExponential(name='tuned_gs1', bounds=(1, 1024),  default=32, base=2),
                Integer(name='tuned_tileX',      bounds=(1, 1024),  default=38),
                Integer(name='tuned_tileY',      bounds=(1, 1024),  default=26),
                IntExponential(name='tuned_vec', bounds=(2, 4),     default=2,  base=2)
            ],
            constraints = [Constraint(
                constraint=constraint_string,
                dependent_params=dependent_params) for constraint_string, dependent_params in [
                ('tuned_gs0 % tuned_ls0 == 0', ['tuned_gs0', 'tuned_ls0']),
                ('tuned_gs1 % tuned_ls1 == 0', ['tuned_gs1', 'tuned_ls1']),
                ('(tuned_tileX + 4) % tuned_vec == 0', ['tuned_tileX', 'tuned_vec']), 
                ('(tuned_tileX * tuned_tileY) <= 1024', ['tuned_tileX', 'tuned_tileY']),
                ('(tuned_ls0 * tuned_ls1) <= 1024', ['tuned_ls0', 'tuned_ls1']),
                ('(tuned_tileX == 1) or (tuned_tileX % 2 == 0)', ['tuned_tileX']),
                ('(tuned_tileY == 1) or (tuned_tileY % 2 == 0)', ['tuned_tileY']),
                ('(tuned_tileY != 1) or ((tuned_tileX != 1024) and (tuned_tileX != 1022))', ['tuned_tileX', 'tuned_tileY']),
            ]],
            metrics=rise_metrics,
            objectives=rise_objectives,
            fidelity_params=rise_fidelity_params
        )
    )
