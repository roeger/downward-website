

This page describes the current single 'option' for label reduction.

## Exact generalized label reduction 

This class implements the exact generalized label reduction described in the following paper:

* Silvan Sievers, Martin Wehrle and Malte Helmert.<br />
 [Generalized Label Reduction for Merge-and-Shrink Heuristics](https://ai.dmi.unibas.ch/papers/sievers-et-al-aaai2014.pdf).<br />
 In *Proceedings of the 28th AAAI Conference on Artificial Intelligence (AAAI 2014)*, pp. 2358-2366. AAAI Press, 2014.

    exact(before_shrinking, before_merging, method=all_transition_systems_with_fixpoint, system_order=random, random_seed=-1)

* *before_shrinking* (bool): apply label reduction before shrinking
* *before_merging* (bool): apply label reduction before merging
* *method* ({two_transition_systems, all_transition_systems, all_transition_systems_with_fixpoint}): Label reduction method. See the AAAI14 paper by Sievers et al. for explanation of the default label reduction method and the 'combinable relation' .Also note that you must set at least one of the options reduce_labels_before_shrinking or reduce_labels_before_merging in order to use the chosen label reduction configuration.
    * `two_transition_systems`: compute the 'combinable relation' only for the two transition systems being merged next
    * `all_transition_systems`: compute the 'combinable relation' for labels once for every transition system and reduce labels
    * `all_transition_systems_with_fixpoint`: keep computing the 'combinable relation' for labels iteratively for all transition systems until no more labels can be reduced
* *system_order* ({regular, reverse, random}): Order of transition systems for the label reduction methods that iterate over the set of all transition systems. Only useful for the choices all_transition_systems and all_transition_systems_with_fixpoint for the option label_reduction_method.
    * `regular`: transition systems are considered in the order given in the planner input if atomic and in the order of their creation if composite.
    * `reverse`: inverse of regular
    * `random`: random order
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
