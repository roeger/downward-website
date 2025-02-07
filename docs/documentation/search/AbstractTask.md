

## Cost-adapted task 

A cost-adapting transformation of the root task.

    adapt_costs(cost_type=normal)

* *cost_type* ({normal, one, plusone}): Operator cost adjustment type. No matter what this setting is, axioms will always be considered as actions of cost 0 by the heuristics that treat axioms as actions.
    * `normal`: all actions are accounted for with their real cost
    * `one`: all actions are accounted for as unit cost
    * `plusone`: all actions are accounted for as their real cost + 1 (except if all actions have original cost 1, in which case cost 1 is used). This is the behaviour known for the heuristics of the LAMA planner. This is intended to be used by the heuristics, not search algorithms, but is supported for both.

## no_transform 

    no_transform()
