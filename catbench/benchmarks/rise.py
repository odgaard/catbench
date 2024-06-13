from interopt.search_space import Objective, Metric
from interopt.parameter import Integer, Real

rise_metrics=[
    Metric('compute_time',  index=0, singular=True),
    Metric('cpuEnergy',     index=1, singular=True),
    Metric('energy',        index=2, singular=True)
]

rise_objectives=[
    Objective(name='compute_time',  metric=rise_metrics[0], minimize=True),
    Objective(name='cpuEnergy',     metric=rise_metrics[1], minimize=True),
    Objective(name='energy',        metric=rise_metrics[2], minimize=True)
],


rise_fidelity_params = [
    Integer(name='iterations',  bounds=(1, 500),    default=10),
    Real(name='timeouts',       bounds=(1, 60000),  default=60000),
]
