

Factory for pattern collections

## combo 

    combo(max_states=1000000, verbosity=normal)

* *max_states* (int [1, infinity]): maximum abstraction size for combo strategy
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## Disjoint CEGAR 

This pattern collection generator uses the CEGAR algorithm to compute a pattern for the planning task. See below for a description of the algorithm and some implementation notes. The original algorithm (called single CEGAR) is described in the paper 

* Alexander Rovner, Silvan Sievers and Malte Helmert.<br />
 [Counterexample-Guided Abstraction Refinement for Pattern Selection in Optimal Classical Planning](https://ai.dmi.unibas.ch/papers/rovner-et-al-icaps2019.pdf).<br />
 In *Proceedings of the 29th International Conference on Automated Planning and Scheduling (ICAPS 2019)*, pp. 362-367. AAAI Press, 2019.

    disjoint_cegar(max_pdb_size=1000000, max_collection_size=10000000, max_time=infinity, use_wildcard_plans=true, random_seed=-1, verbosity=normal)

* *max_pdb_size* (int [1, infinity]): maximum number of states per pattern database (ignored for the initial collection consisting of a singleton pattern for each goal variable)
* *max_collection_size* (int [1, infinity]): maximum number of states in the pattern collection (ignored for the initial collection consisting of a singleton pattern for each goal variable)
* *max_time* (double [0.0, infinity]): maximum time in seconds for this pattern collection generator (ignored for computing the initial collection consisting of a singleton pattern for each goal variable)
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

## Genetic Algorithm Patterns 

The following paper describes the automated creation of pattern databases with a genetic algorithm. Pattern collections are initially created with a bin-packing algorithm. The genetic algorithm is used to optimize the pattern collections with an objective function that estimates the mean heuristic value of the the pattern collections. Pattern collections with higher mean heuristic estimates are more likely selected for the next generation.

* Stefan Edelkamp.<br />
 [Automated Creation of Pattern Database Search Heuristics](http://www.springerlink.com/content/20613345434608x1/).<br />
 In *Proceedings of the 4th Workshop on Model Checking and Artificial Intelligence (!MoChArt 2006)*, pp. 35-50. AAAI Press, 2007.

    genetic(pdb_max_size=50000, num_collections=5, num_episodes=30, mutation_probability=0.01, disjoint=false, random_seed=-1, verbosity=normal)

* *pdb_max_size* (int [1, infinity]): maximal number of states per pattern database 
* *num_collections* (int [1, infinity]): number of pattern collections to maintain in the genetic algorithm (population size)
* *num_episodes* (int [0, infinity]): number of episodes for the genetic algorithm
* *mutation_probability* (double [0.0, 1.0]): probability for flipping a bit in the genetic algorithm
* *disjoint* (bool): consider a pattern collection invalid (giving it very low fitness) if its patterns are not disjoint
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note:** This pattern generation method uses the zero/one pattern database heuristic.

### Implementation Notes 

The standard genetic algorithm procedure as described in the paper is implemented in Fast Downward. The implementation is close to the paper.

 * Initialization<br />In Fast Downward bin-packing with the next-fit strategy is used. A bin corresponds to a pattern which contains variables up to `pdb_max_size`. With this method each variable occurs exactly in one pattern of a collection. There are `num_collections` collections created.
 * Mutation<br />With probability `mutation_probability` a bit is flipped meaning that either a variable is added to a pattern or deleted from a pattern.
 * Recombination<br />Recombination isn't implemented in Fast Downward. In the paper recombination is described but not used.
 * Evaluation<br />For each pattern collection the mean heuristic value is computed. For a single pattern database the mean heuristic value is the sum of all pattern database entries divided through the number of entries. Entries with infinite heuristic values are ignored in this calculation. The sum of these individual mean heuristic values yield the mean heuristic value of the collection.
 * Selection<br />The higher the mean heuristic value of a pattern collection is, the more likely this pattern collection should be selected for the next generation. Therefore the mean heuristic values are normalized and converted into probabilities and Roulette Wheel Selection is used.

Supported language features:

* **action costs:** supported
* **conditional effects:** not supported
* **axioms:** not supported

## Hill climbing 

This algorithm uses hill climbing to generate patterns optimized for the [Canonical PDB](Evaluator.md#canonical_pdb) heuristic. It it described in the following paper:

* Patrik Haslum, Adi Botea, Malte Helmert, Blai Bonet and Sven Koenig.<br />
 [Domain-Independent Construction of Pattern Database Heuristics for Cost-Optimal Planning](https://ai.dmi.unibas.ch/papers/haslum-et-al-aaai07.pdf).<br />
 In *Proceedings of the 22nd AAAI Conference on Artificial Intelligence (AAAI 2007)*, pp. 1007-1012. AAAI Press, 2007.

For implementation notes, see:

* Silvan Sievers, Manuela Ortlieb and Malte Helmert.<br />
 [Efficient Implementation of Pattern Database Heuristics for Classical Planning](https://ai.dmi.unibas.ch/papers/sievers-et-al-socs2012.pdf).<br />
 In *Proceedings of the Fifth Annual Symposium on Combinatorial Search (SoCS 2012)*, pp. 105-111. AAAI Press, 2012.

    hillclimbing(pdb_max_size=2000000, collection_max_size=20000000, num_samples=1000, min_improvement=10, max_time=infinity, random_seed=-1, verbosity=normal)

* *pdb_max_size* (int [1, infinity]): maximal number of states per pattern database 
* *collection_max_size* (int [1, infinity]): maximal number of states in the pattern collection
* *num_samples* (int [1, infinity]): number of samples (random states) on which to evaluate each candidate pattern collection
* *min_improvement* (int [1, infinity]): minimum number of samples on which a candidate pattern collection must improve on the current one to be considered as the next pattern collection 
* *max_time* (double [0.0, infinity]): maximum time in seconds for improving the initial pattern collection via hill climbing. If set to 0, no hill climbing is performed at all. Note that this limit only affects hill climbing. Use max_time_dominance_pruning to limit the time spent for pruning dominated patterns.
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
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

## manual_patterns 

    manual_patterns(patterns, verbosity=normal)

* *patterns* (list of list of int): list of patterns (which are lists of variable numbers of the planning task).
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## Multiple CEGAR 

This pattern collection generator implements the multiple CEGAR algorithm described in the paper

* Alexander Rovner, Silvan Sievers and Malte Helmert.<br />
 [Counterexample-Guided Abstraction Refinement for Pattern Selection in Optimal Classical Planning](https://ai.dmi.unibas.ch/papers/rovner-et-al-icaps2019.pdf).<br />
 In *Proceedings of the 29th International Conference on Automated Planning and Scheduling (ICAPS 2019)*, pp. 362-367. AAAI Press, 2019.

It is an instantiation of the 'multiple algorithm framework'. To compute a pattern in each iteration, it uses the CEGAR algorithm restricted to a single goal variable. See below for descriptions of the algorithms.

    multiple_cegar(use_wildcard_plans=true, max_pdb_size=1M, max_collection_size=10M, pattern_generation_max_time=infinity, total_max_time=100.0, stagnation_limit=20.0, blacklist_trigger_percentage=0.75, enable_blacklist_on_stagnation=true, random_seed=-1, verbosity=normal)

* *use_wildcard_plans* (bool): if true, compute wildcard plans which are sequences of sets of operators that induce the same transition; otherwise compute regular plans which are sequences of single operators
* *max_pdb_size* (int [1, infinity]): maximum number of states for each pattern database, computed by compute_pattern (possibly ignored by singleton patterns consisting of a goal variable)
* *max_collection_size* (int [1, infinity]): maximum number of states in all pattern databases of the collection (possibly ignored, see max_pdb_size)
* *pattern_generation_max_time* (double [0.0, infinity]): maximum time in seconds for each call to the algorithm for computing a single pattern
* *total_max_time* (double [0.0, infinity]): maximum time in seconds for this pattern collection generator. It will always execute at least one iteration, i.e., call the algorithm for computing a single pattern at least once.
* *stagnation_limit* (double [1.0, infinity]): maximum time in seconds this pattern generator is allowed to run without generating a new pattern. It terminates prematurely if this limit is hit unless enable_blacklist_on_stagnation is enabled.
* *blacklist_trigger_percentage* (double [0.0, 1.0]): percentage of total_max_time after which blacklisting is enabled
* *enable_blacklist_on_stagnation* (bool): if true, blacklisting is enabled when stagnation_limit is hit for the first time (unless it was already enabled due to blacklist_trigger_percentage) and pattern generation is terminated when stagnation_limit is hit for the second time. If false, pattern generation is terminated already the first time stagnation_limit is hit.
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

### Short description of the 'multiple algorithm framework' 

This algorithm is a general framework for computing a pattern collection for a given planning task. It requires as input a method for computing a single pattern for the given task and a single goal of the task. The algorithm works as follows. It first stores the goals of the task in random order. Then, it repeatedly iterates over all goals and for each goal, it uses the given method for computing a single pattern. If the pattern is new (duplicate detection), it is kept for the final collection.
The algorithm runs until reaching a given time limit. Another parameter allows exiting early if no new patterns are found for a certain time ('stagnation'). Further parameters allow enabling blacklisting for the given pattern computation method after a certain time to force some diversification or to enable said blacklisting when stagnating.

### Implementation note about the 'multiple algorithm framework' 

A difference compared to the original implementation used in the paper is that the original implementation of stagnation in the multiple CEGAR/RCG algorithms started counting the time towards stagnation only after having generated a duplicate pattern. Now, time towards stagnation starts counting from the start and is reset to the current time only when having found a new pattern or when enabling blacklisting.

## Multiple Random Patterns 

This pattern collection generator implements the 'multiple randomized causal graph' (mRCG) algorithm described in experiments of the paper

* Alexander Rovner, Silvan Sievers and Malte Helmert.<br />
 [Counterexample-Guided Abstraction Refinement for Pattern Selection in Optimal Classical Planning](https://ai.dmi.unibas.ch/papers/rovner-et-al-icaps2019.pdf).<br />
 In *Proceedings of the 29th International Conference on Automated Planning and Scheduling (ICAPS 2019)*, pp. 362-367. AAAI Press, 2019.

It is an instantiation of the 'multiple algorithm framework'. To compute a pattern in each iteration, it uses the random pattern algorithm, called 'single randomized causal graph' (sRCG) in the paper. See below for descriptions of the algorithms.

    random_patterns(bidirectional=true, max_pdb_size=1M, max_collection_size=10M, pattern_generation_max_time=infinity, total_max_time=100.0, stagnation_limit=20.0, blacklist_trigger_percentage=0.75, enable_blacklist_on_stagnation=true, random_seed=-1, verbosity=normal)

* *bidirectional* (bool): this option decides if the causal graph is considered to be directed or undirected selecting predecessors of already selected variables. If true (default), it is considered to be undirected (precondition-effect edges are bidirectional). If false, it is considered to be directed (a variable is a neighbor only if it is a predecessor.
* *max_pdb_size* (int [1, infinity]): maximum number of states for each pattern database, computed by compute_pattern (possibly ignored by singleton patterns consisting of a goal variable)
* *max_collection_size* (int [1, infinity]): maximum number of states in all pattern databases of the collection (possibly ignored, see max_pdb_size)
* *pattern_generation_max_time* (double [0.0, infinity]): maximum time in seconds for each call to the algorithm for computing a single pattern
* *total_max_time* (double [0.0, infinity]): maximum time in seconds for this pattern collection generator. It will always execute at least one iteration, i.e., call the algorithm for computing a single pattern at least once.
* *stagnation_limit* (double [1.0, infinity]): maximum time in seconds this pattern generator is allowed to run without generating a new pattern. It terminates prematurely if this limit is hit unless enable_blacklist_on_stagnation is enabled.
* *blacklist_trigger_percentage* (double [0.0, 1.0]): percentage of total_max_time after which blacklisting is enabled
* *enable_blacklist_on_stagnation* (bool): if true, blacklisting is enabled when stagnation_limit is hit for the first time (unless it was already enabled due to blacklist_trigger_percentage) and pattern generation is terminated when stagnation_limit is hit for the second time. If false, pattern generation is terminated already the first time stagnation_limit is hit.
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

### Short description of the 'multiple algorithm framework' 

This algorithm is a general framework for computing a pattern collection for a given planning task. It requires as input a method for computing a single pattern for the given task and a single goal of the task. The algorithm works as follows. It first stores the goals of the task in random order. Then, it repeatedly iterates over all goals and for each goal, it uses the given method for computing a single pattern. If the pattern is new (duplicate detection), it is kept for the final collection.
The algorithm runs until reaching a given time limit. Another parameter allows exiting early if no new patterns are found for a certain time ('stagnation'). Further parameters allow enabling blacklisting for the given pattern computation method after a certain time to force some diversification or to enable said blacklisting when stagnating.

### Implementation note about the 'multiple algorithm framework' 

A difference compared to the original implementation used in the paper is that the original implementation of stagnation in the multiple CEGAR/RCG algorithms started counting the time towards stagnation only after having generated a duplicate pattern. Now, time towards stagnation starts counting from the start and is reset to the current time only when having found a new pattern or when enabling blacklisting.

## Systematically generated patterns 

Generates all (interesting) patterns with up to pattern_max_size variables. For details, see

* Florian Pommerening, Gabriele Roeger and Malte Helmert.<br />
 [Getting the Most Out of Pattern Databases for Classical Planning](https://ai.dmi.unibas.ch/papers/pommerening-et-al-ijcai2013.pdf).<br />
 In *Proceedings of the Twenty-Third International Joint Conference on Artificial Intelligence (IJCAI 2013)*, pp. 2357-2364. AAAI Press, 2013.

    systematic(pattern_max_size=1, only_interesting_patterns=true, verbosity=normal)

* *pattern_max_size* (int [1, infinity]): max number of variables per pattern
* *only_interesting_patterns* (bool): Only consider the union of two disjoint patterns if the union has more information than the individual patterns.
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output
