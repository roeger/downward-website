

This page describes the available merge trees that can be used to precompute a merge strategy, either for the entire task or a given subset of transition systems of a given factored transition system.
Merge trees are typically used in the merge strategy of type 'precomputed', but they can also be used as fallback merge strategies in 'combined' merge strategies.

## Linear merge trees 

These merge trees implement several linear merge orders, which are described in the paper:

* Malte Helmert, Patrik Haslum and Joerg Hoffmann.<br />
 [Flexible Abstraction Heuristics for Optimal Sequential Planning](https://ai.dmi.unibas.ch/papers/helmert-et-al-icaps2007.pdf).<br />
 In *Proceedings of the Seventeenth International Conference on Automated Planning and Scheduling (ICAPS 2007)*, pp. 176-183. AAAI Press, 2007.

    linear(variable_order=cg_goal_level, random_seed=-1, update_option=use_random)

* *variable_order* ({cg_goal_level, cg_goal_random, goal_cg_level, random, level, reverse_level}): the order in which atomic transition systems are merged
    * `cg_goal_level`: variables are prioritized first if they have an arc to a previously added variable, second if their goal value is defined and third according to their level in the causal graph
    * `cg_goal_random`: variables are prioritized first if they have an arc to a previously added variable, second if their goal value is defined and third randomly
    * `goal_cg_level`: variables are prioritized first if their goal value is defined, second if they have an arc to a previously added variable, and third according to their level in the causal graph
    * `random`: variables are ordered randomly
    * `level`: variables are ordered according to their level in the causal graph
    * `reverse_level`: variables are ordered reverse to their level in the causal graph
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
* *update_option* ({use_first, use_second, use_random}): When the merge tree is used within another merge strategy, how should it be updated when a merge different to a merge from the tree is performed.
    * `use_first`: the node representing the index that would have been merged earlier survives
    * `use_second`: the node representing the index that would have been merged later survives
    * `use_random`: a random node (of the above two) survives
