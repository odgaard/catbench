from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace, Metric, Objective
from interopt.parameter import Integer, Real


carl_metrics = [Metric(f'cycle_error_test{i}', i, True) for i in range(10)]
carl_objectives = [Objective(f'cycle_error_test{i}', carl_metrics[i], True) for i in range(10)]

max_cycles = 500

carl_params = [
    Integer(name='startup_delay',       bounds=(1, max_cycles), default=0),
    Real(name='data_load_factor',       bounds=(0.0, 2.0),      default=0.0),
    Integer(name='initial_delay',       bounds=(1, max_cycles), default=0),
    Integer(name='output_latency',      bounds=(1, max_cycles), default=18),
    Integer(name='sequential_interval', bounds=(1, max_cycles), default=1),
    Integer(name='miss_latency',        bounds=(1, max_cycles), default=0),
    Integer(name='row_size',            bounds=(1, 20),         default=4),
]

def get_carl_definition():
    return ProblemDefinition(name='carl',
        search_space=SearchSpace(
            params=carl_params,
            metrics=carl_metrics,
            objectives=carl_objectives,
            constraints=[],
        )
    )
