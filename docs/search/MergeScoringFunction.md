

This page describes various merge scoring functions. A scoring function, given a list of merge candidates and a factored transition system, computes a score for each candidate based on this information and potentially some chosen options. Minimal scores are considered best. Scoring functions are currently only used within the score based filtering merge selector.

## DFP scoring 

This scoring function computes the 'DFP' score as described in the paper "Directed model checking with distance-preserving abstractions" by Draeger, Finkbeiner and Podelski (SPIN 2006), adapted to planning in the following paper:

* Silvan Sievers, Martin Wehrle and Malte Helmert.<br />
 [Generalized Label Reduction for Merge-and-Shrink Heuristics](https://ai.dmi.unibas.ch/papers/sievers-et-al-aaai2014.pdf).<br />
 In *Proceedings of the 28th AAAI Conference on Artificial Intelligence (AAAI 2014)*, pp. 2358-2366. AAAI Press, 2014.

    dfp()

**Note:** To obtain the configurations called DFP-B-50K described in the paper, use the following configuration of the merge-and-shrink heuristic and adapt the tie-breaking criteria of ```total_order``` as desired:
```
merge_and_shrink(merge_strategy=merge_stateless(merge_selector=score_based_filtering(scoring_functions=[goal_relevance,dfp,total_order(atomic_ts_order=reverse_level,product_ts_order=new_to_old,atomic_before_product=true)])),shrink_strategy=shrink_bisimulation(greedy=false),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50000,threshold_before_merge=1)
```

## Goal relevance scoring 

This scoring function assigns a merge candidate a value of 0 iff at least one of the two transition systems of the merge candidate is goal relevant in the sense that there is an abstract non-goal state. All other candidates get a score of positive infinity.

    goal_relevance()

## MIASM 

This scoring function favors merging transition systems such that in their product, there are many dead states, which can then be pruned without sacrificing information. In particular, the score it assigns to a product is the ratio of alive states to the total number of states. To compute this score, this class thus computes the product of all pairs of transition systems, potentially copying and shrinking the transition systems before if otherwise their product would exceed the specified size limits. A stateless merge strategy using this scoring function is called dyn-MIASM (nowadays also called sbMIASM for score-based MIASM) and is described in the following paper:

* Silvan Sievers, Martin Wehrle and Malte Helmert.<br />
 [An Analysis of Merge Strategies for Merge-and-Shrink Heuristics](https://ai.dmi.unibas.ch/papers/sievers-et-al-icaps2016.pdf).<br />
 In *Proceedings of the 26th International Conference on Planning and Scheduling (ICAPS 2016)*, pp. 2358-2366. AAAI Press, 2016.

    sf_miasm(shrink_strategy, max_states=-1, max_states_before_merge=-1, threshold_before_merge=-1, use_caching=true)

* *shrink_strategy* ([ShrinkStrategy](ShrinkStrategy.md)): We recommend setting this to match the shrink strategy configuration given to ```merge_and_shrink```, see note below.
* *max_states* (int [-1, infinity]): maximum transition system size allowed at any time point.
* *max_states_before_merge* (int [-1, infinity]): maximum transition system size allowed for two transition systems before being merged to form the synchronized product.
* *threshold_before_merge* (int [-1, infinity]): If a transition system, before being merged, surpasses this soft transition system size limit, the shrink strategy is called to possibly shrink the transition system.
* *use_caching* (bool): Cache scores for merge candidates. IMPORTANT! This only works under the assumption that the merge-and-shrink algorithm only uses exact label reduction and does not (non-exactly) shrink factors other than those being merged in the current iteration. In this setting, the MIASM score of a merge candidate is constant over merge-and-shrink iterations. If caching is enabled, only the scores for the new merge candidates need to be computed.

**Note:** To obtain the configurations called dyn-MIASM described in the paper, use the following configuration of the merge-and-shrink heuristic and adapt the tie-breaking criteria of ```total_order``` as desired:
```
merge_and_shrink(merge_strategy=merge_stateless(merge_selector=score_based_filtering(scoring_functions=[sf_miasm(shrink_strategy=shrink_bisimulation(greedy=false),max_states=50000,threshold_before_merge=1),total_order(atomic_ts_order=reverse_level,product_ts_order=new_to_old,atomic_before_product=true)])),shrink_strategy=shrink_bisimulation(greedy=false),label_reduction=exact(before_shrinking=true,before_merging=false),max_states=50000,threshold_before_merge=1)
```

**Note:** Unless you know what you are doing, we recommend using the same options related to shrinking for ```sf_miasm``` as for ```merge_and_shrink```, i.e. the options ```shrink_strategy```, ```max_states```, and ```threshold_before_merge``` should be set identically. Furthermore, as this scoring function maximizes the amount of possible pruning, merge-and-shrink should be configured to use full pruning, i.e. ```prune_unreachable_states=true``` and ```prune_irrelevant_states=true``` (the default).

## Single random 

This scoring function assigns exactly one merge candidate a score of 0, chosen randomly, and infinity to all others.

    single_random(random_seed=-1)

* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.

## Total order 

This scoring function computes a total order on the merge candidates, based on the specified options. The score for each merge candidate correponds to its position in the order. This scoring function is mainly intended as tie-breaking, and has been introduced in the following paper:

* Silvan Sievers, Martin Wehrle and Malte Helmert.<br />
 [An Analysis of Merge Strategies for Merge-and-Shrink Heuristics](https://ai.dmi.unibas.ch/papers/sievers-et-al-icaps2016.pdf).<br />
 In *Proceedings of the 26th International Conference on Automated Planning and Scheduling (ICAPS 2016)*, pp. 294-298. AAAI Press, 2016.

Furthermore, using the atomic_ts_order option, this scoring function, if used alone in a score based filtering merge selector, can be used to emulate the corresponding (precomputed) linear merge strategies reverse level/level (independently of the other options).

    total_order(atomic_ts_order=reverse_level, product_ts_order=new_to_old, atomic_before_product=false, random_seed=-1)

* *atomic_ts_order* ({reverse_level, level, random}): The order in which atomic transition systems are considered when considering pairs of potential merges.
    * `reverse_level`: the variable order of Fast Downward
    * `level`: opposite of reverse_level
    * `random`: a randomized order
* *product_ts_order* ({old_to_new, new_to_old, random}): The order in which product transition systems are considered when considering pairs of potential merges.
    * `old_to_new`: consider composite transition systems from oldest to most recent
    * `new_to_old`: opposite of old_to_new
    * `random`: a randomized order
* *atomic_before_product* (bool): Consider atomic transition systems before composite ones iff true.
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
