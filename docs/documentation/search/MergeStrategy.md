

This page describes the various merge strategies supported by the planner.

## Precomputed merge strategy 

This merge strategy has a precomputed merge tree. Note that this merge strategy does not take into account the current state of the factored transition system. This also means that this merge strategy relies on the factored transition system being synchronized with this merge tree, i.e. all merges are performed exactly as given by the merge tree.

    merge_precomputed(merge_tree, verbosity=normal)

* *merge_tree* ([MergeTree](MergeTree.md)): The precomputed merge tree.
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note:** An example of a precomputed merge startegy is a linear merge strategy, which can be obtained using:
```
merge_strategy=merge_precomputed(merge_tree=linear(<variable_order>))
```

## Merge strategy SSCs 

This merge strategy implements the algorithm described in the paper 

* Silvan Sievers, Martin Wehrle and Malte Helmert.<br />
 [An Analysis of Merge Strategies for Merge-and-Shrink Heuristics](https://ai.dmi.unibas.ch/papers/sievers-et-al-icaps2016.pdf).<br />
 In *Proceedings of the 26th International Conference on Planning and Scheduling (ICAPS 2016)*, pp. 2358-2366. AAAI Press, 2016.

In a nutshell, it computes the maximal SCCs of the causal graph, obtaining a partitioning of the task's variables. Every such partition is then merged individually, using the specified fallback merge strategy, considering the SCCs in a configurable order. Afterwards, all resulting composite abstractions are merged to form the final abstraction, again using the specified fallback merge strategy and the configurable order of the SCCs.

    merge_sccs(order_of_sccs=topological, merge_selector, verbosity=normal)

* *order_of_sccs* ({topological, reverse_topological, decreasing, increasing}): how the SCCs should be ordered
    * `topological`: according to the topological ordering of the directed graph where each obtained SCC is a 'supervertex'
    * `reverse_topological`: according to the reverse topological ordering of the directed graph where each obtained SCC is a 'supervertex'
    * `decreasing`: biggest SCCs first, using 'topological' as tie-breaker
    * `increasing`: smallest SCCs first, using 'topological' as tie-breaker
* *merge_selector* ([MergeSelector](MergeSelector.md)): the fallback merge strategy to use
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## Stateless merge strategy 

This merge strategy has a merge selector, which computes the next merge only depending on the current state of the factored transition system, not requiring any additional information.

    merge_stateless(merge_selector, verbosity=normal)

* *merge_selector* ([MergeSelector](MergeSelector.md)): The merge selector to be used.
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note:** Examples include the DFP merge strategy, which can be obtained using:
```
merge_strategy=merge_stateless(merge_selector=score_based_filtering(scoring_functions=[goal_relevance,dfp,total_order(<order_option>))]))
```
and the (dynamic/score-based) MIASM strategy, which can be obtained using:
```
merge_strategy=merge_stateless(merge_selector=score_based_filtering(scoring_functions=[sf_miasm(<shrinking_options>),total_order(<order_option>)]
```
