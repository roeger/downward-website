

Factory for single patterns

## CEGAR 

This pattern generator uses the CEGAR algorithm restricted to a random single goal of the task to compute a pattern. See below for a description of the algorithm and some implementation notes. The original algorithm (called single CEGAR) is described in the paper 

* Alexander Rovner, Silvan Sievers and Malte Helmert.<br />
 [Counterexample-Guided Abstraction Refinement for Pattern Selection in Optimal Classical Planning](https://ai.dmi.unibas.ch/papers/rovner-et-al-icaps2019.pdf).<br />
 In *Proceedings of the 29th International Conference on Automated Planning and Scheduling (ICAPS 2019)*, pp. 362-367. AAAI Press, 2019.

    cegar_pattern(max_pdb_size=1000000, max_time=infinity, use_wildcard_plans=true, random_seed=-1, verbosity=normal)

* *max_pdb_size* (int [1, infinity]): maximum number of states in the final pattern database (possibly ignored by a singleton pattern consisting of a single goal variable)
* *max_time* (double [0.0, infinity]): maximum time in seconds for the pattern generation
* *use_wildcard_plans* (bool): if true, compute wildcard plans which are sequences of sets of operators that induce the same transition; otherwise compute regular plans which are sequences of single operators
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

### Short description of the CEGAR algorithm 

The CEGAR algorithm computes a pattern collection for a given planning task and a given (sub)set of its goals in a randomized order as follows. Starting from the pattern collection consisting of a singleton pattern for each goal variable, it repeatedly attempts to execute an optimal plan of each pattern in the concrete task, collects reasons why this is not possible (so-called flaws) and refines the pattern in question by adding a variable to it.
Further parameters allow blacklisting a (sub)set of the non-goal variables which are then never added to the collection, limiting PDB and collection size, setting a time limit and switching between computing regular or wildcard plans, where the latter are sequences of parallel operators inducing the same abstract transition.

### Implementation notes about the CEGAR algorithm 

The following describes differences of the implementation to the original implementation used and described in the paper.

Conceptually, there is one larger difference which concerns the computation of (regular or wildcard) plans for PDBs. The original implementation used an enforced hill-climbing (EHC) search with the PDB as the perfect heuristic, which ensured finding strongly optimal plans, i.e., optimal plans with a minimum number of zero-cost operators, in domains with zero-cost operators. The original implementation also slightly modified EHC to search for a best-improving successor, chosen uniformly at random among all best-improving successors.

In contrast, the current implementation computes a plan alongside the computation of the PDB itself. A modification to Dijkstra's algorithm for computing the PDB values stores, for each state, the operator leading to that state (in a regression search). This generating operator is updated only if the algorithm found a cheaper path to the state. After Dijkstra finishes, the plan computation starts at the initial state and iteratively follows the generating operator, computes all operators of the same cost inducing the same transition, until reaching a goal. This constitutes a wildcard plan. It is turned into a regular one by randomly picking a single operator for each transition. 

Note that this kind of plan extraction does not consider all successors of a state uniformly at random but rather uses the previously deterministically chosen generating operator to settle on one successor state, which is biased by the number of operators leading to the same successor from the given state. Further note that in the presence of zero-cost operators, this procedure does not guarantee that the computed plan is strongly optimal because it does not minimize the number of used zero-cost operators leading to the state when choosing a generating operator. Experiments have shown (issue1007) that this speeds up the computation significantly while not having a strongly negative effect on heuristic quality due to potentially computing worse plans.

Two further changes fix bugs of the original implementation to match the description in the paper. The first bug fix is to raise a flaw for all goal variables of the task if the plan for a PDB can be executed on the concrete task but does not lead to a goal state. Previously, such flaws would not have been raised because all goal variables are part of the collection from the start on and therefore not considered. This means that the original implementation accidentally disallowed merging patterns due to goal violation flaws. The second bug fix is to actually randomize the order of parallel operators in wildcard plan steps.

## greedy 

    greedy(max_states=1000000, verbosity=normal)

* *max_states* (int [1, infinity]): maximal number of abstract states in the pattern database.
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## manual_pattern 

    manual_pattern(pattern, verbosity=normal)

* *pattern* (list of int): list of variable numbers of the planning task that should be used as pattern.
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## Random Pattern 

This pattern generator implements the 'single randomized causal graph' algorithm described in experiments of the the paper

* Alexander Rovner, Silvan Sievers and Malte Helmert.<br />
 [Counterexample-Guided Abstraction Refinement for Pattern Selection in Optimal Classical Planning](https://ai.dmi.unibas.ch/papers/rovner-et-al-icaps2019.pdf).<br />
 In *Proceedings of the 29th International Conference on Automated Planning and Scheduling (ICAPS 2019)*, pp. 362-367. AAAI Press, 2019.

See below for a description of the algorithm and some implementation notes.

    random_pattern(max_pdb_size=1000000, max_time=infinity, bidirectional=true, random_seed=-1, verbosity=normal)

* *max_pdb_size* (int [1, infinity]): maximum number of states in the final pattern database (possibly ignored by a singleton pattern consisting of a single goal variable)
* *max_time* (double [0.0, infinity]): maximum time in seconds for the pattern generation
* *bidirectional* (bool): this option decides if the causal graph is considered to be directed or undirected selecting predecessors of already selected variables. If true (default), it is considered to be undirected (precondition-effect edges are bidirectional). If false, it is considered to be directed (a variable is a neighbor only if it is a predecessor.
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

### Short description of the random pattern algorithm 

The random pattern algorithm computes a pattern for a given planning task and a single goal of the task as follows. Starting with the given goal variable, the algorithm executes a random walk on the causal graph. In each iteration, it selects a random causal graph neighbor of the current variable. It terminates if no neighbor fits the pattern due to the size limit or if the time limit is reached.

### Implementation notes about the random pattern algorithm 

In the original implementation used in the paper, the algorithm selected a random neighbor and then checked if selecting it would violate the PDB size limit. If so, the algorithm would not select it and terminate. In the current implementation, the algorithm instead loops over all neighbors of the current variable in random order and selects the first one not violating the PDB size limit. If no such neighbor exists, the algorithm terminates.
