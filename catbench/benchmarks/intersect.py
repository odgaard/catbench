from interopt.definition import ProblemDefinition
from interopt.search_space import SearchSpace, Metric, Objective
from interopt.parameter import Integer


intersect_metrics = [Metric(f'cycle_error_test{i}', i, True) for i in range(10)]
intersect_objectives = [Objective(f'cycle_error_test{i}', intersect_metrics[i], True) for i in range(10)]

max_cycles = 500

intersect_params = [
    Integer(name='startup_delay',       bounds=(1, max_cycles), default=0),
    Integer(name='stop_latency',        bounds=(1, max_cycles), default=0),
    Integer(name='output_latency',      bounds=(1, max_cycles), default=18),
    Integer(name='sequential_interval', bounds=(1, max_cycles), default=1),
    Integer(name='val_stop_delay',      bounds=(1, max_cycles), default=0),
    Integer(name='val_advance_delay',   bounds=(1, max_cycles), default=0),
]

def get_intersect_definition():
    return ProblemDefinition(name='intersect',
        search_space=SearchSpace(
            params=intersect_params,
            metrics=intersect_metrics,
            objectives=intersect_objectives,
            constraints=[],
        )
    )
