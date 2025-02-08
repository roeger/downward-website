

An evaluator specification is either a newly created evaluator instance or an evaluator that has been defined previously. This page describes how one can specify a new evaluator instance. For re-using evaluators, see OptionSyntax#Evaluator_Predefinitions.

If the evaluator is a heuristic, definitions of *properties* in the descriptions below:

 * **admissible:** h(s) <= h*(s) for all states s
 * **consistent:** h(s) <= c(s, s') + h(s') for all states s connected to states s' by an action with cost c(s, s')
 * **safe:** h(s) = infinity is only true for states with h*(s) = infinity
 * **preferred operators:** this heuristic identifies preferred operators 

This feature type can be bound to variables using `let(variable_name, variable_definition, expression)` where `expression` can use `variable_name`. Predefinitions using `--evaluator`, `--heuristic`, and `--landmarks` are automatically transformed into `let`-expressions but are deprecated.

## Additive heuristic 

    add(axioms=approximate_negative_cycles, transform=no_transform(), cache_estimates=true, description="add", verbosity=normal)

* *axioms* ({approximate_negative, approximate_negative_cycles}): How to compute axioms that describe how the negated (=default) value of a derived variable can be achieved.
    * `approximate_negative`: Overapproximate negated axioms for all derived variables by setting an empty condition, indicating the default value can always be achieved for free.
    * `approximate_negative_cycles`: Overapproximate negated axioms for all derived variables which have cyclic dependencies by setting an empty condition, indicating the default value can always be achieved for free. For all other derived variables, the negated axioms are computed exactly. Note that this can potentially lead to a combinatorial explosion.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** supported
* **axioms:** supported

Properties:

* **admissible:** no
* **consistent:** no
* **safe:** yes
* **preferred operators:** yes

## Blind heuristic 

Returns cost of cheapest action for non-goal states, 0 for goal states

    blind(transform=no_transform(), cache_estimates=true, description="blind", verbosity=normal)

* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** supported
* **axioms:** supported

Properties:

* **admissible:** yes
* **consistent:** yes
* **safe:** yes
* **preferred operators:** no

## Context-enhanced additive heuristic 

    cea(axioms=approximate_negative_cycles, transform=no_transform(), cache_estimates=true, description="cea", verbosity=normal)

* *axioms* ({approximate_negative, approximate_negative_cycles}): How to compute axioms that describe how the negated (=default) value of a derived variable can be achieved.
    * `approximate_negative`: Overapproximate negated axioms for all derived variables by setting an empty condition, indicating the default value can always be achieved for free.
    * `approximate_negative_cycles`: Overapproximate negated axioms for all derived variables which have cyclic dependencies by setting an empty condition, indicating the default value can always be achieved for free. For all other derived variables, the negated axioms are computed exactly. Note that this can potentially lead to a combinatorial explosion.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** supported
* **axioms:** supported

Properties:

* **admissible:** no
* **consistent:** no
* **safe:** no
* **preferred operators:** yes

## Additive Cartesian CEGAR heuristic 

See the paper introducing counterexample-guided Cartesian abstraction refinement (CEGAR) for classical planning:

* Jendrik Seipp and Malte Helmert.<br />
 [Counterexample-guided Cartesian Abstraction Refinement](https://ai.dmi.unibas.ch/papers/seipp-helmert-icaps2013.pdf).<br />
 In *Proceedings of the 23rd International Conference on Automated Planning and Scheduling (ICAPS 2013)*, pp. 347-351. AAAI Press, 2013.

and the paper showing how to make the abstractions additive:

* Jendrik Seipp and Malte Helmert.<br />
 [Diverse and Additive Cartesian Abstraction Heuristics](https://ai.dmi.unibas.ch/papers/seipp-helmert-icaps2014.pdf).<br />
 In *Proceedings of the 24th International Conference on Automated Planning and Scheduling (ICAPS 2014)*, pp. 289-297. AAAI Press, 2014.

For more details on Cartesian CEGAR and saturated cost partitioning, see the journal paper

* Jendrik Seipp and Malte Helmert.<br />
 [Counterexample-Guided Cartesian Abstraction Refinement for Classical Planning](https://ai.dmi.unibas.ch/papers/seipp-helmert-jair2018.pdf).<br />
 *Journal of Artificial Intelligence Research* 62:535-577. 2018.

    cegar(subtasks=[landmarks(),goals()], max_states=infinity, max_transitions=1M, max_time=infinity, pick=max_refined, use_general_costs=true, random_seed=-1, transform=no_transform(), cache_estimates=true, description="cegar", verbosity=normal)

* *subtasks* (list of [SubtaskGenerator](SubtaskGenerator.md)): subtask generators
* *max_states* (int [1, infinity]): maximum sum of abstract states over all abstractions
* *max_transitions* (int [0, infinity]): maximum sum of real transitions (excluding self-loops) over  all abstractions
* *max_time* (double [0.0, infinity]): maximum time in seconds for building abstractions
* *pick* ({random, min_unwanted, max_unwanted, min_refined, max_refined, min_hadd, max_hadd}): how to choose on which variable to split the flaw state
    * `random`: select a random variable (among all eligible variables)
    * `min_unwanted`: select an eligible variable which has the least unwanted values (number of values of v that land in the abstract state whose h-value will probably be raised) in the flaw state
    * `max_unwanted`: select an eligible variable which has the most unwanted values (number of values of v that land in the abstract state whose h-value will probably be raised) in the flaw state
    * `min_refined`: select an eligible variable which is the least refined (-1 * (remaining_values(v) / original_domain_size(v))) in the flaw state
    * `max_refined`: select an eligible variable which is the most refined (-1 * (remaining_values(v) / original_domain_size(v))) in the flaw state
    * `min_hadd`: select an eligible variable with minimal h^add(s_0) value over all facts that need to be removed from the flaw state
    * `max_hadd`: select an eligible variable with maximal h^add(s_0) value over all facts that need to be removed from the flaw state
* *use_general_costs* (bool): allow negative costs in cost partitioning
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

Properties:

* **admissible:** yes
* **consistent:** yes
* **safe:** yes
* **preferred operators:** no

## Causal graph heuristic 

    cg(max_cache_size=1000000, axioms=approximate_negative_cycles, transform=no_transform(), cache_estimates=true, description="cg", verbosity=normal)

* *max_cache_size* (int [0, infinity]): maximum number of cached entries per variable (set to 0 to disable cache)
* *axioms* ({approximate_negative, approximate_negative_cycles}): How to compute axioms that describe how the negated (=default) value of a derived variable can be achieved.
    * `approximate_negative`: Overapproximate negated axioms for all derived variables by setting an empty condition, indicating the default value can always be achieved for free.
    * `approximate_negative_cycles`: Overapproximate negated axioms for all derived variables which have cyclic dependencies by setting an empty condition, indicating the default value can always be achieved for free. For all other derived variables, the negated axioms are computed exactly. Note that this can potentially lead to a combinatorial explosion.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** supported
* **axioms:** supported

Properties:

* **admissible:** no
* **consistent:** no
* **safe:** no
* **preferred operators:** yes

## FF heuristic 

    ff(axioms=approximate_negative_cycles, transform=no_transform(), cache_estimates=true, description="ff", verbosity=normal)

* *axioms* ({approximate_negative, approximate_negative_cycles}): How to compute axioms that describe how the negated (=default) value of a derived variable can be achieved.
    * `approximate_negative`: Overapproximate negated axioms for all derived variables by setting an empty condition, indicating the default value can always be achieved for free.
    * `approximate_negative_cycles`: Overapproximate negated axioms for all derived variables which have cyclic dependencies by setting an empty condition, indicating the default value can always be achieved for free. For all other derived variables, the negated axioms are computed exactly. Note that this can potentially lead to a combinatorial explosion.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** supported
* **axioms:** supported

Properties:

* **admissible:** no
* **consistent:** no
* **safe:** yes
* **preferred operators:** yes

## Goal count heuristic 

    goalcount(transform=no_transform(), cache_estimates=true, description="goalcount", verbosity=normal)

* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** ignored by design
* **conditional effects:** supported
* **axioms:** supported

Properties:

* **admissible:** no
* **consistent:** no
* **safe:** yes
* **preferred operators:** no

## h^m heuristic 

    hm(m=2, transform=no_transform(), cache_estimates=true, description="hm", verbosity=normal)

* *m* (int [1, infinity]): subset size
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** ignored
* **axioms:** ignored

Properties:

* **admissible:** yes for tasks without conditional effects or axioms
* **consistent:** yes for tasks without conditional effects or axioms
* **safe:** yes for tasks without conditional effects or axioms
* **preferred operators:** no

## Max heuristic 

    hmax(axioms=approximate_negative_cycles, transform=no_transform(), cache_estimates=true, description="hmax", verbosity=normal)

* *axioms* ({approximate_negative, approximate_negative_cycles}): How to compute axioms that describe how the negated (=default) value of a derived variable can be achieved.
    * `approximate_negative`: Overapproximate negated axioms for all derived variables by setting an empty condition, indicating the default value can always be achieved for free.
    * `approximate_negative_cycles`: Overapproximate negated axioms for all derived variables which have cyclic dependencies by setting an empty condition, indicating the default value can always be achieved for free. For all other derived variables, the negated axioms are computed exactly. Note that this can potentially lead to a combinatorial explosion.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** supported
* **axioms:** supported

Properties:

* **admissible:** yes for tasks without axioms
* **consistent:** yes for tasks without axioms
* **safe:** yes
* **preferred operators:** no

## Landmark cost partitioning heuristic 

Landmark progression is implemented according to the following paper:

* Clemens Büchner, Thomas Keller, Salomé Eriksson and Malte Helmert.<br />
 [Landmarks Progression in Heuristic Search](https://ai.dmi.unibas.ch/papers/buechner-et-al-icaps2023.pdf).<br />
 In *Proceedings of the Thirty-Third International Conference on Automated Planning and Scheduling (ICAPS 2023)*, pp. 70-79. AAAI Press, 2023.

    landmark_cost_partitioning(lm_factory, pref=false, prog_goal=true, prog_gn=true, prog_r=true, transform=no_transform(), cache_estimates=true, description="landmark_cost_partitioning", verbosity=normal, cost_partitioning=uniform, alm=true, lpsolver=cplex)

* *lm_factory* ([LandmarkFactory](LandmarkFactory.md)): the set of landmarks to use for this heuristic. The set of landmarks can be specified here, or predefined (see [LandmarkFactory](LandmarkFactory.md)).
* *pref* (bool): enable preferred operators (see note below)
* *prog_goal* (bool): Use goal progression.
* *prog_gn* (bool): Use greedy-necessary ordering progression.
* *prog_r* (bool): Use reasonable ordering progression.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output
* *cost_partitioning* ({optimal, uniform}): strategy for partitioning operator costs among landmarks
    * `optimal`: use optimal (LP-based) cost partitioning
    * `uniform`: partition operator costs uniformly among all landmarks achieved by that operator
* *alm* (bool): use action landmarks
* *lpsolver* ({cplex, soplex}): external solver that should be used to solve linear programs
    * `cplex`: commercial solver by IBM
    * `soplex`: open source solver by ZIB

**Note:** to use an LP solver, you must build the planner with LP support. See [build instructions](https://github.com/aibasel/downward/blob/main/BUILD.md).

**Usage with A*:** We recommend to add this heuristic as lazy_evaluator when using it in the A* algorithm. This way, the heuristic is recomputed before a state is expanded, leading to improved estimates that incorporate all knowledge gained from paths that were found after the state was inserted into the open list.

**Consistency:** The heuristic is consistent along single paths if it is set as lazy_evaluator; i.e. when expanding s then we have h(s) <= h(s')+cost(a) for all successors s' of s reached with a. But newly found paths to s can increase h(s), at which point the above inequality might not hold anymore.

**Optimal Cost Partitioning:** To use `cost_partitioning=optimal`, you must build the planner with LP support. See [build instructions](https://github.com/aibasel/downward/blob/main/BUILD.md).

**Preferred operators:** Preferred operators should not be used for optimal planning. See [Landmark sum heuristic](Evaluator.md#landmark_sum_heuristic) for more information on using preferred operators; the comments there also apply to this heuristic.

Supported language features:

* **action costs:** supported
* **conditional_effects:** supported if the [LandmarkFactory](LandmarkFactory.md) supports them; otherwise not supported
* **axioms:** not allowed

Properties:

* **preferred operators:** yes (if enabled; see `pref` option)
* **admissible:** yes
* **consistent:** no; see document note about consistency
* **safe:** yes

## Landmark sum heuristic 

Landmark progression is implemented according to the following paper:

* Clemens Büchner, Thomas Keller, Salomé Eriksson and Malte Helmert.<br />
 [Landmarks Progression in Heuristic Search](https://ai.dmi.unibas.ch/papers/buechner-et-al-icaps2023.pdf).<br />
 In *Proceedings of the Thirty-Third International Conference on Automated Planning and Scheduling (ICAPS 2023)*, pp. 70-79. AAAI Press, 2023.

    landmark_sum(lm_factory, pref=false, prog_goal=true, prog_gn=true, prog_r=true, transform=no_transform(), cache_estimates=true, description="landmark_sum_heuristic", verbosity=normal, axioms=approximate_negative_cycles)

* *lm_factory* ([LandmarkFactory](LandmarkFactory.md)): the set of landmarks to use for this heuristic. The set of landmarks can be specified here, or predefined (see [LandmarkFactory](LandmarkFactory.md)).
* *pref* (bool): enable preferred operators (see note below)
* *prog_goal* (bool): Use goal progression.
* *prog_gn* (bool): Use greedy-necessary ordering progression.
* *prog_r* (bool): Use reasonable ordering progression.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output
* *axioms* ({approximate_negative, approximate_negative_cycles}): How to compute axioms that describe how the negated (=default) value of a derived variable can be achieved.
    * `approximate_negative`: Overapproximate negated axioms for all derived variables by setting an empty condition, indicating the default value can always be achieved for free.
    * `approximate_negative_cycles`: Overapproximate negated axioms for all derived variables which have cyclic dependencies by setting an empty condition, indicating the default value can always be achieved for free. For all other derived variables, the negated axioms are computed exactly. Note that this can potentially lead to a combinatorial explosion.

**Note on performance for satisficing planning:** The cost of a landmark is based on the cost of the operators that achieve it. For satisficing search this can be counterproductive since it is often better to focus on distance from goal (i.e. length of the plan) rather than cost. In experiments we achieved the best performance using the option 'transform=adapt_costs(one)' to enforce unit costs.

**Preferred operators:** Computing preferred operators is *only enabled* when setting pref=true because it has a nontrivial runtime cost. Using the heuristic for preferred operators without setting pref=true has no effect.
Our implementation to compute preferred operators based on landmarks differs from the description in the literature (see reference above).The original implementation computes two kinds of preferred operators:

1. If there is an applicable operator that reaches a landmark, all such operators are preferred.
1. If no such operators exist, perform an FF-style relaxed exploration towards the nearest landmarks (according to the landmark orderings) and use the preferred operators of this exploration.

Our implementation only considers preferred operators of the first type and does not include the second type. The rationale for this change is that it reduces code complexity and helps more cleanly separate landmark-based and FF-based computations in LAMA-like planner configurations. In our experiments, only considering preferred operators of the first type reduces performance when using the heuristic and its preferred operators in isolation but improves performance when using this heuristic in conjunction with the FF heuristic, as in LAMA-like planner configurations.

Supported language features:

* **action costs:** supported
* **conditional_effects:** supported if the [LandmarkFactory](LandmarkFactory.md) supports them; otherwise ignored
* **axioms:** supported

Properties:

* **preferred operators:** yes (if enabled; see `pref` option)
* **admissible:** no
* **consistent:** no
* **safe:** yes except on tasks with conditional effects when using a [LandmarkFactory](LandmarkFactory.md) not supporting them

## Landmark-cut heuristic 

    lmcut(transform=no_transform(), cache_estimates=true, description="lmcut", verbosity=normal)

* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

Properties:

* **admissible:** yes
* **consistent:** no
* **safe:** yes
* **preferred operators:** no

## Merge-and-shrink heuristic 

This heuristic implements the algorithm described in the following paper:

* Silvan Sievers, Martin Wehrle and Malte Helmert.<br />
 [Generalized Label Reduction for Merge-and-Shrink Heuristics](https://ai.dmi.unibas.ch/papers/sievers-et-al-aaai2014.pdf).<br />
 In *Proceedings of the 28th AAAI Conference on Artificial Intelligence (AAAI 2014)*, pp. 2358-2366. AAAI Press, 2014.

For a more exhaustive description of merge-and-shrink, see the journal paper

* Silvan Sievers and Malte Helmert.<br />
 [Merge-and-Shrink: A Compositional Theory of Transformations of Factored Transition Systems](https://ai.dmi.unibas.ch/papers/sievers-helmert-jair2021.pdf).<br />
 *Journal of Artificial Intelligence Research* 71:781-883. 2021.

The following paper describes how to improve the DFP merge strategy with tie-breaking, and presents two new merge strategies (dyn-MIASM and SCC-DFP):

* Silvan Sievers, Martin Wehrle and Malte Helmert.<br />
 [An Analysis of Merge Strategies for Merge-and-Shrink Heuristics](https://ai.dmi.unibas.ch/papers/sievers-et-al-icaps2016.pdf).<br />
 In *Proceedings of the 26th International Conference on Automated Planning and Scheduling (ICAPS 2016)*, pp. 294-298. AAAI Press, 2016.

Details of the algorithms and the implementation are described in the paper

* Silvan Sievers.<br />
 [Merge-and-Shrink Heuristics for Classical Planning: Efficient Implementation and Partial Abstractions](https://ai.dmi.unibas.ch/papers/sievers-socs2018.pdf).<br />
 In *Proceedings of the 11th Annual Symposium on Combinatorial Search (SoCS 2018)*, pp. 90-98. AAAI Press, 2018.

    merge_and_shrink(merge_strategy, shrink_strategy, label_reduction=<none>, prune_unreachable_states=true, prune_irrelevant_states=true, max_states=-1, max_states_before_merge=-1, threshold_before_merge=-1, main_loop_max_time=infinity, transform=no_transform(), cache_estimates=true, description="merge_and_shrink", verbosity=normal)

* *merge_strategy* ([MergeStrategy](MergeStrategy.md)): See detailed documentation for merge strategies. We currently recommend SCC-DFP, which can be achieved using ```merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance,dfp,total_order]))```
* *shrink_strategy* ([ShrinkStrategy](ShrinkStrategy.md)): See detailed documentation for shrink strategies. We currently recommend non-greedy shrink_bisimulation, which can be achieved using ```shrink_strategy=shrink_bisimulation(greedy=false)```
* *label_reduction* ([LabelReduction](LabelReduction.md)): See detailed documentation for labels. There is currently only one 'option' to use label_reduction, which is ```label_reduction=exact``` Also note the interaction with shrink strategies.
* *prune_unreachable_states* (bool): If true, prune abstract states unreachable from the initial state.
* *prune_irrelevant_states* (bool): If true, prune abstract states from which no goal state can be reached.
* *max_states* (int [-1, infinity]): maximum transition system size allowed at any time point.
* *max_states_before_merge* (int [-1, infinity]): maximum transition system size allowed for two transition systems before being merged to form the synchronized product.
* *threshold_before_merge* (int [-1, infinity]): If a transition system, before being merged, surpasses this soft transition system size limit, the shrink strategy is called to possibly shrink the transition system.
* *main_loop_max_time* (double [0.0, infinity]): A limit in seconds on the runtime of the main loop of the algorithm. If the limit is exceeded, the algorithm terminates, potentially returning a factored transition system with several factors. Also note that the time limit is only checked between transformations of the main loop, but not during, so it can be exceeded if a transformation is runtime-intense.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note:** Conditional effects are supported directly. Note, however, that for tasks that are not factored (in the sense of the JACM 2014 merge-and-shrink paper), the atomic transition systems on which merge-and-shrink heuristics are based are nondeterministic, which can lead to poor heuristics even when only perfect shrinking is performed.

**Note:** When pruning unreachable states, admissibility and consistency is only guaranteed for reachable states and transitions between reachable states. While this does not impact regular A* search which will never encounter any unreachable state, it impacts techniques like symmetry-based pruning: a reachable state which is mapped to an unreachable symmetric state (which hence is pruned) would falsely be considered a dead-end and also be pruned, thus violating optimality of the search.

**Note:** When using a time limit on the main loop of the merge-and-shrink algorithm, the heuristic will compute the maximum over all heuristics induced by the remaining factors if terminating the merge-and-shrink algorithm early. Exception: if there is an unsolvable factor, it will be used as the exclusive heuristic since the problem is unsolvable.

**Note:** A currently recommended good configuration uses bisimulation based shrinking, the merge strategy SCC-DFP, and the appropriate label reduction setting (max_states has been altered to be between 10k and 200k in the literature). As merge-and-shrink heuristics can be expensive to compute, we also recommend limiting time by setting ```main_loop_max_time``` to a finite value. A sensible value would be half of the time allocated for the planner.
```
merge_and_shrink(shrink_strategy=shrink_bisimulation(greedy=false),merge_strategy=merge_sccs(order_of_sccs=topological,merge_selector=score_based_filtering(scoring_functions=[goal_relevance(),dfp(),total_order()])),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50k,threshold_before_merge=1)
```

Supported language features:

* **action costs:** supported
* **conditional effects:** supported (but see note)
* **axioms:** not supported

Properties:

* **admissible:** yes (but see note)
* **consistent:** yes (but see note)
* **safe:** yes
* **preferred operators:** no

## Operator-counting heuristic 

An operator-counting heuristic computes a linear program (LP) in each state. The LP has one variable Count_o for each operator o that represents how often the operator is used in a plan. Operator-counting constraints are linear constraints over these varaibles that are guaranteed to have a solution with Count_o = occurrences(o, pi) for every plan pi. Minimizing the total cost of operators subject to some operator-counting constraints is an admissible heuristic. For details, see

* Florian Pommerening, Gabriele Roeger, Malte Helmert and Blai Bonet.<br />
 [LP-based Heuristics for Cost-optimal Planning](http://www.aaai.org/ocs/index.php/ICAPS/ICAPS14/paper/view/7892/8031).<br />
 In *Proceedings of the Twenty-Fourth International Conference on Automated Planning and Scheduling (ICAPS 2014)*, pp. 226-234. AAAI Press, 2014.

    operatorcounting(constraint_generators, use_integer_operator_counts=false, lpsolver=cplex, transform=no_transform(), cache_estimates=true, description="operatorcounting", verbosity=normal)

* *constraint_generators* (list of [ConstraintGenerator](ConstraintGenerator.md)): methods that generate constraints over operator-counting variables
* *use_integer_operator_counts* (bool): restrict operator-counting variables to integer values. Computing the heuristic with integer variables can produce higher values but requires solving a MIP instead of an LP which is generally more computationally expensive. Turning this option on can thus drastically increase the runtime.
* *lpsolver* ({cplex, soplex}): external solver that should be used to solve linear programs
    * `cplex`: commercial solver by IBM
    * `soplex`: open source solver by ZIB
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note:** to use an LP solver, you must build the planner with LP support. See [build instructions](https://github.com/aibasel/downward/blob/main/BUILD.md).

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported (the heuristic supports them in theory, but none of the currently implemented constraint generators do)
* **axioms:** not supported (the heuristic supports them in theory, but none of the currently implemented constraint generators do)

Properties:

* **admissible:** yes
* **consistent:** yes, if all constraint generators represent consistent heuristics
* **safe:** yes
* **preferred operators:** no

# Basic Evaluators 

## Constant evaluator 

Returns a constant value.

    const(value=1, description="const", verbosity=normal)

* *value* (int [0, infinity]): the constant value
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## g-value evaluator 

Returns the g-value (path cost) of the search node.

    g(description="g", verbosity=normal)

* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## Max evaluator 

Calculates the maximum of the sub-evaluators.

    max(evals, description="max", verbosity=normal)

* *evals* (list of [Evaluator](Evaluator.md)): at least one evaluator
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## Preference evaluator 

Returns 0 if preferred is true and 1 otherwise.

    pref(description="pref", verbosity=normal)

* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## Sum evaluator 

Calculates the sum of the sub-evaluators.

    sum(evals, description="sum", verbosity=normal)

* *evals* (list of [Evaluator](Evaluator.md)): at least one evaluator
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## Weighted evaluator 

Multiplies the value of the evaluator with the given weight.

    weight(eval, weight, description="weight", verbosity=normal)

* *eval* ([Evaluator](Evaluator.md)): evaluator
* *weight* (int): weight
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

# Pattern Database Heuristics 

## Canonical PDB 

The canonical pattern database heuristic is calculated as follows. For a given pattern collection C, the value of the canonical heuristic function is the maximum over all maximal additive subsets A in C, where the value for one subset S in A is the sum of the heuristic values for all patterns in S for a given state.

    cpdbs(patterns=systematic(1), max_time_dominance_pruning=infinity, transform=no_transform(), cache_estimates=true, description="cpdbs", verbosity=normal)

* *patterns* ([PatternCollectionGenerator](PatternCollectionGenerator.md)): pattern generation method
* *max_time_dominance_pruning* (double [0.0, infinity]): The maximum time in seconds spent on dominance pruning. Using 0.0 turns off dominance pruning. Dominance pruning excludes patterns and additive subsets that will never contribute to the heuristic value because there are dominating subsets in the collection.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

Properties:

* **admissible:** yes
* **consistent:** yes
* **safe:** yes
* **preferred operators:** no

## iPDB 

This approach is a combination of using the [Canonical PDB](Evaluator.md#canonical_pdb) heuristic over patterns computed with the [hillclimbing](PatternCollectionGenerator.md#hillclimbing) algorithm for pattern generation. It is a short-hand for the command-line option ```cpdbs(hillclimbing())```. Both the heuristic and the pattern generation algorithm are described in the following paper:

* Patrik Haslum, Adi Botea, Malte Helmert, Blai Bonet and Sven Koenig.<br />
 [Domain-Independent Construction of Pattern Database Heuristics for Cost-Optimal Planning](https://ai.dmi.unibas.ch/papers/haslum-et-al-aaai07.pdf).<br />
 In *Proceedings of the 22nd AAAI Conference on Artificial Intelligence (AAAI 2007)*, pp. 1007-1012. AAAI Press, 2007.

For implementation notes, see:

* Silvan Sievers, Manuela Ortlieb and Malte Helmert.<br />
 [Efficient Implementation of Pattern Database Heuristics for Classical Planning](https://ai.dmi.unibas.ch/papers/sievers-et-al-socs2012.pdf).<br />
 In *Proceedings of the Fifth Annual Symposium on Combinatorial Search (SoCS 2012)*, pp. 105-111. AAAI Press, 2012.

See also [Canonical PDB](Evaluator.md#canonical_pdb) and [Hill climbing](PatternCollectionGenerator.md#hill_climbing) for more details.

    ipdb(pdb_max_size=2000000, collection_max_size=20000000, num_samples=1000, min_improvement=10, max_time=infinity, random_seed=-1, max_time_dominance_pruning=infinity, transform=no_transform(), cache_estimates=true, description="cpdbs", verbosity=normal)

* *pdb_max_size* (int [1, infinity]): maximal number of states per pattern database 
* *collection_max_size* (int [1, infinity]): maximal number of states in the pattern collection
* *num_samples* (int [1, infinity]): number of samples (random states) on which to evaluate each candidate pattern collection
* *min_improvement* (int [1, infinity]): minimum number of samples on which a candidate pattern collection must improve on the current one to be considered as the next pattern collection 
* *max_time* (double [0.0, infinity]): maximum time in seconds for improving the initial pattern collection via hill climbing. If set to 0, no hill climbing is performed at all. Note that this limit only affects hill climbing. Use max_time_dominance_pruning to limit the time spent for pruning dominated patterns.
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
* *max_time_dominance_pruning* (double [0.0, infinity]): The maximum time in seconds spent on dominance pruning. Using 0.0 turns off dominance pruning. Dominance pruning excludes patterns and additive subsets that will never contribute to the heuristic value because there are dominating subsets in the collection.
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note:** The pattern collection created by the algorithm will always contain all patterns consisting of a single goal variable, even if this violates the pdb_max_size or collection_max_size limits.

**Note:** This pattern generation method generates patterns optimized for use with the canonical pattern database heuristic.

### Implementation Notes 

The following will very briefly describe the algorithm and explain the differences between the original implementation from 2007 and the new one in Fast Downward.

The aim of the algorithm is to output a pattern collection for which the [Canonical PDB](Evaluator.md#canonical_pdb) yields the best heuristic estimates.

The algorithm is basically a local search (hill climbing) which searches the "pattern neighbourhood" (starting initially with a pattern for each goal variable) for improving the pattern collection. This is done as described in the section "pattern construction as search" in the paper, except for the corrected search neighbourhood discussed below. For evaluating the neighbourhood, the "counting approximation" as introduced in the paper was implemented. An important difference however consists in the fact that this implementation computes all pattern databases for each candidate pattern rather than using A* search to compute the heuristic values only for the sample states for each pattern.

Also the logic for sampling the search space differs a bit from the original implementation. The original implementation uses a random walk of a length which is binomially distributed with the mean at the estimated solution depth (estimation is done with the current pattern collection heuristic). In the Fast Downward implementation, also a random walk is used, where the length is the estimation of the number of solution steps, which is calculated by dividing the current heuristic estimate for the initial state by the average operator costs of the planning task (calculated only once and not updated during sampling!) to take non-unit cost problems into account. This yields a random walk of an expected lenght of np = 2 * estimated number of solution steps. If the random walk gets stuck, it is being restarted from the initial state, exactly as described in the original paper.

The section "avoiding redundant evaluations" describes how the search neighbourhood of patterns can be restricted to variables that are relevant to the variables already included in the pattern by analyzing causal graphs. There is a mistake in the paper that leads to some relevant neighbouring patterns being ignored. See the [errata](https://ai.dmi.unibas.ch/research/publications.html) for details. This mistake has been addressed in this implementation. The second approach described in the paper (statistical confidence interval) is not applicable to this implementation, as it doesn't use A* search but constructs the entire pattern databases for all candidate patterns anyway.
The search is ended if there is no more improvement (or the improvement is smaller than the minimal improvement which can be set as an option), however there is no limit of iterations of the local search. This is similar to the techniques used in the original implementation as described in the paper.

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

Properties:

* **admissible:** yes
* **consistent:** yes
* **safe:** yes
* **preferred operators:** no

## Pattern database heuristic 

Computes goal distance in state space abstractions based on projections. First used in domain-independent planning by:

* Stefan Edelkamp.<br />
 [Planning with Pattern Databases](https://aaai.org/papers/7280-ecp-01-2001/).<br />
 In *Proceedings of the Sixth European Conference on Planning (ECP 2001)*, pp. 84-90. AAAI Press, 2001.

For implementation notes, see:

* Silvan Sievers, Manuela Ortlieb and Malte Helmert.<br />
 [Efficient Implementation of Pattern Database Heuristics for Classical Planning](https://ai.dmi.unibas.ch/papers/sievers-et-al-socs2012.pdf).<br />
 In *Proceedings of the Fifth Annual Symposium on Combinatorial Search (SoCS 2012)*, pp. 105-111. AAAI Press, 2012.

    pdb(pattern=greedy(), transform=no_transform(), cache_estimates=true, description="pdb", verbosity=normal)

* *pattern* ([PatternGenerator](PatternGenerator.md)): pattern generation method
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

Properties:

* **admissible:** yes
* **consistent:** yes
* **safe:** yes
* **preferred operators:** no

## Zero-One PDB 

The zero/one pattern database heuristic is simply the sum of the heuristic values of all patterns in the pattern collection. In contrast to the canonical pattern database heuristic, there is no need to check for additive subsets, because the additivity of the patterns is guaranteed by action cost partitioning. This heuristic uses the most simple form of action cost partitioning, i.e. if an operator affects more than one pattern in the collection, its costs are entirely taken into account for one pattern (the first one which it affects) and set to zero for all other affected patterns.

    zopdbs(patterns=systematic(1), transform=no_transform(), cache_estimates=true, description="zopdbs", verbosity=normal)

* *patterns* ([PatternCollectionGenerator](PatternCollectionGenerator.md)): pattern generation method
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

Properties:

* **admissible:** yes
* **consistent:** yes
* **safe:** yes
* **preferred operators:** no

# Potential Heuristics 

## Potential heuristic optimized for all states 

The algorithm is based on

* Jendrik Seipp, Florian Pommerening and Malte Helmert.<br />
 [New Optimization Functions for Potential Heuristics](https://ai.dmi.unibas.ch/papers/seipp-et-al-icaps2015.pdf).<br />
 In *Proceedings of the 25th International Conference on Automated Planning and Scheduling (ICAPS 2015)*, pp. 193-201. AAAI Press, 2015.

    all_states_potential(max_potential=1e8, lpsolver=cplex, transform=no_transform(), cache_estimates=true, description="all_states_potential", verbosity=normal)

* *max_potential* (double [0.0, infinity]): Bound potentials by this number. Using the bound ```infinity``` disables the bounds. In some domains this makes the computation of weights unbounded in which case no weights can be extracted. Using very high weights can cause numerical instability in the LP solver, while using very low weights limits the choice of potential heuristics. For details, see the ICAPS paper cited above.
* *lpsolver* ({cplex, soplex}): external solver that should be used to solve linear programs
    * `cplex`: commercial solver by IBM
    * `soplex`: open source solver by ZIB
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note:** to use an LP solver, you must build the planner with LP support. See [build instructions](https://github.com/aibasel/downward/blob/main/BUILD.md).

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

Properties:

* **admissible:** yes
* **consistent:** yes
* **safe:** yes
* **preferred operators:** no

## Diverse potential heuristics 

The algorithm is based on

* Jendrik Seipp, Florian Pommerening and Malte Helmert.<br />
 [New Optimization Functions for Potential Heuristics](https://ai.dmi.unibas.ch/papers/seipp-et-al-icaps2015.pdf).<br />
 In *Proceedings of the 25th International Conference on Automated Planning and Scheduling (ICAPS 2015)*, pp. 193-201. AAAI Press, 2015.

    diverse_potentials(num_samples=1000, max_num_heuristics=infinity, max_potential=1e8, lpsolver=cplex, transform=no_transform(), cache_estimates=true, description="diverse_potentials", verbosity=normal, random_seed=-1)

* *num_samples* (int [0, infinity]): Number of states to sample
* *max_num_heuristics* (int [0, infinity]): maximum number of potential heuristics
* *max_potential* (double [0.0, infinity]): Bound potentials by this number. Using the bound ```infinity``` disables the bounds. In some domains this makes the computation of weights unbounded in which case no weights can be extracted. Using very high weights can cause numerical instability in the LP solver, while using very low weights limits the choice of potential heuristics. For details, see the ICAPS paper cited above.
* *lpsolver* ({cplex, soplex}): external solver that should be used to solve linear programs
    * `cplex`: commercial solver by IBM
    * `soplex`: open source solver by ZIB
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.

**Note:** to use an LP solver, you must build the planner with LP support. See [build instructions](https://github.com/aibasel/downward/blob/main/BUILD.md).

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

Properties:

* **admissible:** yes
* **consistent:** yes
* **safe:** yes
* **preferred operators:** no

## Potential heuristic optimized for initial state 

The algorithm is based on

* Jendrik Seipp, Florian Pommerening and Malte Helmert.<br />
 [New Optimization Functions for Potential Heuristics](https://ai.dmi.unibas.ch/papers/seipp-et-al-icaps2015.pdf).<br />
 In *Proceedings of the 25th International Conference on Automated Planning and Scheduling (ICAPS 2015)*, pp. 193-201. AAAI Press, 2015.

    initial_state_potential(max_potential=1e8, lpsolver=cplex, transform=no_transform(), cache_estimates=true, description="initial_state_potential", verbosity=normal)

* *max_potential* (double [0.0, infinity]): Bound potentials by this number. Using the bound ```infinity``` disables the bounds. In some domains this makes the computation of weights unbounded in which case no weights can be extracted. Using very high weights can cause numerical instability in the LP solver, while using very low weights limits the choice of potential heuristics. For details, see the ICAPS paper cited above.
* *lpsolver* ({cplex, soplex}): external solver that should be used to solve linear programs
    * `cplex`: commercial solver by IBM
    * `soplex`: open source solver by ZIB
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note:** to use an LP solver, you must build the planner with LP support. See [build instructions](https://github.com/aibasel/downward/blob/main/BUILD.md).

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

Properties:

* **admissible:** yes
* **consistent:** yes
* **safe:** yes
* **preferred operators:** no

## Sample-based potential heuristics 

Maximum over multiple potential heuristics optimized for samples. The algorithm is based on

* Jendrik Seipp, Florian Pommerening and Malte Helmert.<br />
 [New Optimization Functions for Potential Heuristics](https://ai.dmi.unibas.ch/papers/seipp-et-al-icaps2015.pdf).<br />
 In *Proceedings of the 25th International Conference on Automated Planning and Scheduling (ICAPS 2015)*, pp. 193-201. AAAI Press, 2015.

    sample_based_potentials(num_heuristics=1, num_samples=1000, max_potential=1e8, lpsolver=cplex, transform=no_transform(), cache_estimates=true, description="sample_based_potentials", verbosity=normal, random_seed=-1)

* *num_heuristics* (int [0, infinity]): number of potential heuristics
* *num_samples* (int [0, infinity]): Number of states to sample
* *max_potential* (double [0.0, infinity]): Bound potentials by this number. Using the bound ```infinity``` disables the bounds. In some domains this makes the computation of weights unbounded in which case no weights can be extracted. Using very high weights can cause numerical instability in the LP solver, while using very low weights limits the choice of potential heuristics. For details, see the ICAPS paper cited above.
* *lpsolver* ({cplex, soplex}): external solver that should be used to solve linear programs
    * `cplex`: commercial solver by IBM
    * `soplex`: open source solver by ZIB
* *transform* ([AbstractTask](AbstractTask.md)): Optional task transformation for the heuristic. Currently, adapt_costs() and no_transform() are available.
* *cache_estimates* (bool): cache heuristic estimates
* *description* (string): description used to identify evaluator in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.

**Note:** to use an LP solver, you must build the planner with LP support. See [build instructions](https://github.com/aibasel/downward/blob/main/BUILD.md).

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

Properties:

* **admissible:** yes
* **consistent:** yes
* **safe:** yes
* **preferred operators:** no
