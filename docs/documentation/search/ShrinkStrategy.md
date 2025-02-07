

This page describes the various shrink strategies supported by the planner.

## Bismulation based shrink strategy 

This shrink strategy implements the algorithm described in the paper:

* Raz Nissim, Joerg Hoffmann and Malte Helmert.<br />
 [Computing Perfect Heuristics in Polynomial Time: On Bisimulation and Merge-and-Shrink Abstractions in Optimal Planning.](https://ai.dmi.unibas.ch/papers/nissim-et-al-ijcai2011.pdf).<br />
 In *Proceedings of the Twenty-Second International Joint Conference on Artificial Intelligence (IJCAI 2011)*, pp. 1983-1990. AAAI Press, 2011.

    shrink_bisimulation(greedy=false, at_limit=return)

* *greedy* (bool): use greedy bisimulation
* *at_limit* ({return, use_up}): what to do when the size limit is hit
    * `return`: stop without refining the equivalence class further
    * `use_up`: continue refining the equivalence class until the size limit is hit

**shrink_bisimulation(greedy=true):** Combine this with the merge-and-shrink options max_states=infinity and threshold_before_merge=1 and with the linear merge strategy reverse_level to obtain the variant 'greedy bisimulation without size limit', called M&S-gop in the IJCAI 2011 paper. When we last ran experiments on interaction of shrink strategies with label reduction, this strategy performed best when used with label reduction before shrinking (and no label reduction before merging).

**shrink_bisimulation(greedy=false):** Combine this with the merge-and-shrink option max_states=N (where N is a numerical parameter for which sensible values include 1000, 10000, 50000, 100000 and 200000) and with the linear merge strategy reverse_level to obtain the variant 'exact bisimulation with a size limit', called DFP-bop in the IJCAI 2011 paper. When we last ran experiments on interaction of shrink strategies with label reduction, this strategy performed best when used with label reduction before shrinking (and no label reduction before merging).

## f-preserving shrink strategy 

This shrink strategy implements the algorithm described in the paper:

* Malte Helmert, Patrik Haslum and Joerg Hoffmann.<br />
 [Flexible Abstraction Heuristics for Optimal Sequential Planning](https://ai.dmi.unibas.ch/papers/helmert-et-al-icaps2007.pdf).<br />
 In *Proceedings of the Seventeenth International Conference on Automated Planning and Scheduling (ICAPS 2007)*, pp. 176-183. AAAI Press, 2007.

    shrink_fh(shrink_f=high, shrink_h=low, random_seed=-1)

* *shrink_f* ({high, low}): in which direction the f based shrink priority is ordered
    * `high`: prefer shrinking states with high value
    * `low`: prefer shrinking states with low value
* *shrink_h* ({high, low}): in which direction the h based shrink priority is ordered
    * `high`: prefer shrinking states with high value
    * `low`: prefer shrinking states with low value
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.

**Note:** The strategy first partitions all states according to their combination of f- and h-values. These partitions are then sorted, first according to their f-value, then according to their h-value (increasing or decreasing, depending on the chosen options). States sorted last are shrinked together until reaching max_states.

**shrink_fh():** Combine this with the merge-and-shrink option max_states=N (where N is a numerical parameter for which sensible values include 1000, 10000, 50000, 100000 and 200000) and the linear merge startegy cg_goal_level to obtain the variant 'f-preserving shrinking of transition systems', called HHH in the IJCAI 2011 paper. Also see bisimulation based shrink strategy. When we last ran experiments on interaction of shrink strategies with label reduction, this strategy performed best when used with label reduction before merging (and no label reduction before shrinking). We also recommend using full pruning with this shrink strategy, because both distances from the initial state and to the goal states must be computed anyway, and because the existence of only one dead state causes this shrink strategy to always use the map-based approach for partitioning states rather than the more efficient vector-based approach.

## Random 

    shrink_random(random_seed=-1)

* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
