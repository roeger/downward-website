

Prune or reorder applicable operators.

## Atom-centric stubborn sets 

Stubborn sets are a state pruning method which computes a subset of applicable actions in each state such that completeness and optimality of the overall search is preserved. Previous stubborn set implementations mainly track information about actions. In contrast, this implementation focuses on atomic propositions (atoms), which often speeds up the computation on IPC benchmarks. For details, see

* Gabriele Roeger, Malte Helmert, Jendrik Seipp and Silvan Sievers.<br />
 [An Atom-Centric Perspective on Stubborn Sets](https://ai.dmi.unibas.ch/papers/roeger-et-al-socs2020.pdf).<br />
 In *Proceedings of the 13th Annual Symposium on Combinatorial Search (SoCS 2020)*, pp. 57-65. AAAI Press, 2020.

    atom_centric_stubborn_sets(use_sibling_shortcut=true, atom_selection_strategy=quick_skip, verbosity=normal)

* *use_sibling_shortcut* (bool): use variable-based marking in addition to atom-based marking
* *atom_selection_strategy* ({fast_downward, quick_skip, static_small, dynamic_small}): Strategy for selecting unsatisfied atoms from action preconditions or the goal atoms. All strategies use the fast_downward strategy for breaking ties.
    * `fast_downward`: select the atom (v, d) with the variable v that comes first in the Fast Downward variable ordering (which is based on the causal graph)
    * `quick_skip`: if possible, select an unsatisfied atom whose producers are already marked
    * `static_small`: select the atom achieved by the fewest number of actions
    * `dynamic_small`: select the atom achieved by the fewest number of actions that are not yet part of the stubborn set
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note on verbosity parameter:** Setting verbosity to verbose or higher enables time measurements in each call to prune_operators for a given state. This induces a significant overhead, up to 30% in configurations like blind search with the no pruning method (`null`). We recommend using at most normal verbosity for running experiments.

## Limited pruning 

Limited pruning applies another pruning method and switches it off after a fixed number of expansions if the pruning ratio is below a given value. The pruning ratio is the sum of all pruned operators divided by the sum of all operators before pruning, considering all previous expansions.

    limited_pruning(pruning, min_required_pruning_ratio=0.2, expansions_before_checking_pruning_ratio=1000, verbosity=normal)

* *pruning* ([PruningMethod](PruningMethod.md)): the underlying pruning method to be applied
* *min_required_pruning_ratio* (double [0.0, 1.0]): disable pruning if the pruning ratio is lower than this value after 'expansions_before_checking_pruning_ratio' expansions
* *expansions_before_checking_pruning_ratio* (int [0, infinity]): number of expansions before deciding whether to disable pruning
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note on verbosity parameter:** Setting verbosity to verbose or higher enables time measurements in each call to prune_operators for a given state. This induces a significant overhead, up to 30% in configurations like blind search with the no pruning method (`null`). We recommend using at most normal verbosity for running experiments.

**Example:** To use atom centric stubborn sets and limit them, use
```
pruning=limited_pruning(pruning=atom_centric_stubborn_sets(),min_required_pruning_ratio=0.2,expansions_before_checking_pruning_ratio=1000)
```
in an eager search such as astar.

## No pruning 

This is a skeleton method that does not perform any pruning, i.e., all applicable operators are applied in all expanded states. 

    null(verbosity=normal)

* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note on verbosity parameter:** Setting verbosity to verbose or higher enables time measurements in each call to prune_operators for a given state. This induces a significant overhead, up to 30% in configurations like blind search with the no pruning method (`null`). We recommend using at most normal verbosity for running experiments.

## StubbornSetsEC 

Stubborn sets represent a state pruning method which computes a subset of applicable operators in each state such that completeness and optimality of the overall search is preserved. As stubborn sets rely on several design choices, there are different variants thereof. The variant 'StubbornSetsEC' resolves the design choices such that the resulting pruning method is guaranteed to strictly dominate the Expansion Core pruning method. For details, see

* Martin Wehrle, Malte Helmert, Yusra Alkhazraji and Robert Mattmueller.<br />
 [The Relative Pruning Power of Strong Stubborn Sets and Expansion Core](http://www.aaai.org/ocs/index.php/ICAPS/ICAPS13/paper/view/6053/6185).<br />
 In *Proceedings of the 23rd International Conference on Automated Planning and Scheduling (ICAPS 2013)*, pp. 251-259. AAAI Press, 2013.

    stubborn_sets_ec(verbosity=normal)

* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note on verbosity parameter:** Setting verbosity to verbose or higher enables time measurements in each call to prune_operators for a given state. This induces a significant overhead, up to 30% in configurations like blind search with the no pruning method (`null`). We recommend using at most normal verbosity for running experiments.

## Stubborn sets simple 

Stubborn sets represent a state pruning method which computes a subset of applicable operators in each state such that completeness and optimality of the overall search is preserved. As stubborn sets rely on several design choices, there are different variants thereof. This stubborn set variant resolves the design choices in a straight-forward way. For details, see the following papers: 

* Yusra Alkhazraji, Martin Wehrle, Robert Mattmueller and Malte Helmert.<br />
 [A Stubborn Set Algorithm for Optimal Planning](https://ai.dmi.unibas.ch/papers/alkhazraji-et-al-ecai2012.pdf).<br />
 In *Proceedings of the 20th European Conference on Artificial Intelligence (ECAI 2012)*, pp. 891-892. IOS Press, 2012.

* Martin Wehrle and Malte Helmert.<br />
 [Efficient Stubborn Sets: Generalized Algorithms and Selection Strategies](http://www.aaai.org/ocs/index.php/ICAPS/ICAPS14/paper/view/7922/8042).<br />
 In *Proceedings of the 24th International Conference on Automated Planning  and Scheduling (ICAPS 2014)*, pp. 323-331. AAAI Press, 2014.

    stubborn_sets_simple(verbosity=normal)

* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note on verbosity parameter:** Setting verbosity to verbose or higher enables time measurements in each call to prune_operators for a given state. This induces a significant overhead, up to 30% in configurations like blind search with the no pruning method (`null`). We recommend using at most normal verbosity for running experiments.
