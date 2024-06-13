from interopt.search_space import Objective, Metric
from interopt.parameter import Integer, Categorical, Permutation, Real

taco_metrics=[
    Metric('compute_time',  index=0, singular=True),
    Metric('compute_times', index=1, singular=False),
    Metric('energy',        index=2, singular=True)
]

taco_objectives=[
    Objective(name='compute_time',  metric=taco_metrics[0], minimize=True),
    Objective(name='energy',        metric=taco_metrics[2], minimize=True)
]

max_threads = 20

taco_common_parameters = [
    Integer(    name='omp_num_threads',      bounds=(2, max_threads), default=16),
    Categorical(name='omp_scheduling_type',  categories=[0, 1, 2],    default=0),
    Categorical(name='omp_monotonic',        categories=[0, 1],       default=0),
    Categorical(name='omp_dynamic',          categories=[0, 1],       default=0),
    Permutation(name='permutation',          length=5,                default=(1, 0, 2, 3, 4))
]

taco_fidelity_params = [
    Integer(name='iterations',              bounds=(1, 500),    default=10),
    Integer(name='repeats',                 bounds=(1, 100),    default=5),
    Real(   name='wait_between_repeats',    bounds=(0, 1000),   default=0),
    Real(   name='wait_after_run',          bounds=(0, 1000),   default=10)
]
