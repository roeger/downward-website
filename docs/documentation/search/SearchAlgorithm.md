

## A* search (eager) 

A* is a special case of eager best first search that uses g+h as f-function. We break ties using the evaluator. Closed nodes are re-opened.

    astar(eval, lazy_evaluator=<none>, pruning=null(), cost_type=normal, bound=infinity, max_time=infinity, description="astar", verbosity=normal)

* *eval* ([Evaluator](Evaluator.md)): evaluator for h-value
* *lazy_evaluator* ([Evaluator](Evaluator.md)): An evaluator that re-evaluates a state before it is expanded.
* *pruning* ([PruningMethod](PruningMethod.md)): Pruning methods can prune or reorder the set of applicable operators in each state and thereby influence the number and order of successor states that are considered.
* *cost_type* ({normal, one, plusone}): Operator cost adjustment type. No matter what this setting is, axioms will always be considered as actions of cost 0 by the heuristics that treat axioms as actions.
    * `normal`: all actions are accounted for with their real cost
    * `one`: all actions are accounted for as unit cost
    * `plusone`: all actions are accounted for as their real cost + 1 (except if all actions have original cost 1, in which case cost 1 is used). This is the behaviour known for the heuristics of the LAMA planner. This is intended to be used by the heuristics, not search algorithms, but is supported for both.
* *bound* (int): exclusive depth bound on g-values. Cutoffs are always performed according to the real cost, regardless of the cost_type parameter
* *max_time* (double): maximum time in seconds the search is allowed to run for. The timeout is only checked after each complete search step (usually a node expansion), so the actual runtime can be arbitrarily longer. Therefore, this parameter should not be used for time-limiting experiments. Timed-out searches are treated as failed searches, just like incomplete search algorithms that exhaust their search space.
* *description* (string): description used to identify search algorithm in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**lazy_evaluator:** When a state s is taken out of the open list, the lazy evaluator h re-evaluates s. If h(s) changes (for example because h is path-dependent), s is not expanded, but instead reinserted into the open list. This option is currently only present for the A* algorithm.

### Equivalent statements using general eager search 

    --search astar(evaluator)

is equivalent to

    --evaluator h=evaluator
    --search eager(tiebreaking([sum([g(), h]), h], unsafe_pruning=false),
                   reopen_closed=true, f_eval=sum([g(), h]))

## Eager best-first search 

    eager(open, reopen_closed=false, f_eval=<none>, preferred=[], pruning=null(), cost_type=normal, bound=infinity, max_time=infinity, description="eager", verbosity=normal)

* *open* ([OpenList](OpenList.md)): open list
* *reopen_closed* (bool): reopen closed nodes
* *f_eval* ([Evaluator](Evaluator.md)): set evaluator for jump statistics. (Optional; if no evaluator is used, jump statistics will not be displayed.)
* *preferred* (list of [Evaluator](Evaluator.md)): use preferred operators of these evaluators
* *pruning* ([PruningMethod](PruningMethod.md)): Pruning methods can prune or reorder the set of applicable operators in each state and thereby influence the number and order of successor states that are considered.
* *cost_type* ({normal, one, plusone}): Operator cost adjustment type. No matter what this setting is, axioms will always be considered as actions of cost 0 by the heuristics that treat axioms as actions.
    * `normal`: all actions are accounted for with their real cost
    * `one`: all actions are accounted for as unit cost
    * `plusone`: all actions are accounted for as their real cost + 1 (except if all actions have original cost 1, in which case cost 1 is used). This is the behaviour known for the heuristics of the LAMA planner. This is intended to be used by the heuristics, not search algorithms, but is supported for both.
* *bound* (int): exclusive depth bound on g-values. Cutoffs are always performed according to the real cost, regardless of the cost_type parameter
* *max_time* (double): maximum time in seconds the search is allowed to run for. The timeout is only checked after each complete search step (usually a node expansion), so the actual runtime can be arbitrarily longer. Therefore, this parameter should not be used for time-limiting experiments. Timed-out searches are treated as failed searches, just like incomplete search algorithms that exhaust their search space.
* *description* (string): description used to identify search algorithm in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## Greedy search (eager) 

    eager_greedy(evals, preferred=[], boost=0, pruning=null(), cost_type=normal, bound=infinity, max_time=infinity, description="eager_greedy", verbosity=normal)

* *evals* (list of [Evaluator](Evaluator.md)): evaluators
* *preferred* (list of [Evaluator](Evaluator.md)): use preferred operators of these evaluators
* *boost* (int): boost value for preferred operator open lists
* *pruning* ([PruningMethod](PruningMethod.md)): Pruning methods can prune or reorder the set of applicable operators in each state and thereby influence the number and order of successor states that are considered.
* *cost_type* ({normal, one, plusone}): Operator cost adjustment type. No matter what this setting is, axioms will always be considered as actions of cost 0 by the heuristics that treat axioms as actions.
    * `normal`: all actions are accounted for with their real cost
    * `one`: all actions are accounted for as unit cost
    * `plusone`: all actions are accounted for as their real cost + 1 (except if all actions have original cost 1, in which case cost 1 is used). This is the behaviour known for the heuristics of the LAMA planner. This is intended to be used by the heuristics, not search algorithms, but is supported for both.
* *bound* (int): exclusive depth bound on g-values. Cutoffs are always performed according to the real cost, regardless of the cost_type parameter
* *max_time* (double): maximum time in seconds the search is allowed to run for. The timeout is only checked after each complete search step (usually a node expansion), so the actual runtime can be arbitrarily longer. Therefore, this parameter should not be used for time-limiting experiments. Timed-out searches are treated as failed searches, just like incomplete search algorithms that exhaust their search space.
* *description* (string): description used to identify search algorithm in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Open list:** In most cases, eager greedy best first search uses an alternation open list with one queue for each evaluator. If preferred operator evaluators are used, it adds an extra queue for each of these evaluators that includes only the nodes that are generated with a preferred operator. If only one evaluator and no preferred operator evaluator is used, the search does not use an alternation open list but a standard open list with only one queue.

**Closed nodes:** Closed node are not re-opened

### Equivalent statements using general eager search 

    --evaluator h2=eval2
    --search eager_greedy([eval1, h2], preferred=[h2], boost=100)

is equivalent to

    --evaluator h1=eval1 --heuristic h2=eval2
    --search eager(alt([single(h1), single(h1, pref_only=true), single(h2), 
                        single(h2, pref_only=true)], boost=100),
                   preferred=[h2])

---

    --search eager_greedy([eval1, eval2])

is equivalent to

    --search eager(alt([single(eval1), single(eval2)]))

---

    --evaluator h1=eval1
    --search eager_greedy([h1], preferred=[h1])

is equivalent to

    --evaluator h1=eval1
    --search eager(alt([single(h1), single(h1, pref_only=true)]),
                   preferred=[h1])

---

    --search eager_greedy([eval1])

is equivalent to

    --search eager(single(eval1))

## Eager weighted A* search 

    eager_wastar(evals, preferred=[], reopen_closed=true, boost=0, w=1, pruning=null(), cost_type=normal, bound=infinity, max_time=infinity, description="eager_wastar", verbosity=normal)

* *evals* (list of [Evaluator](Evaluator.md)): evaluators
* *preferred* (list of [Evaluator](Evaluator.md)): use preferred operators of these evaluators
* *reopen_closed* (bool): reopen closed nodes
* *boost* (int): boost value for preferred operator open lists
* *w* (int): evaluator weight
* *pruning* ([PruningMethod](PruningMethod.md)): Pruning methods can prune or reorder the set of applicable operators in each state and thereby influence the number and order of successor states that are considered.
* *cost_type* ({normal, one, plusone}): Operator cost adjustment type. No matter what this setting is, axioms will always be considered as actions of cost 0 by the heuristics that treat axioms as actions.
    * `normal`: all actions are accounted for with their real cost
    * `one`: all actions are accounted for as unit cost
    * `plusone`: all actions are accounted for as their real cost + 1 (except if all actions have original cost 1, in which case cost 1 is used). This is the behaviour known for the heuristics of the LAMA planner. This is intended to be used by the heuristics, not search algorithms, but is supported for both.
* *bound* (int): exclusive depth bound on g-values. Cutoffs are always performed according to the real cost, regardless of the cost_type parameter
* *max_time* (double): maximum time in seconds the search is allowed to run for. The timeout is only checked after each complete search step (usually a node expansion), so the actual runtime can be arbitrarily longer. Therefore, this parameter should not be used for time-limiting experiments. Timed-out searches are treated as failed searches, just like incomplete search algorithms that exhaust their search space.
* *description* (string): description used to identify search algorithm in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Open lists and equivalent statements using general eager search:** See corresponding notes for "(Weighted) A* search (lazy)"

**Note:** Eager weighted A* search uses an alternation open list while A* search uses a tie-breaking open list. Consequently, 

    --search eager_wastar([h()], w=1)

is **not** equivalent to

    --search astar(h())

## Lazy enforced hill-climbing 

    ehc(h, preferred_usage=prune_by_preferred, preferred=[], cost_type=normal, bound=infinity, max_time=infinity, description="ehc", verbosity=normal)

* *h* ([Evaluator](Evaluator.md)): heuristic
* *preferred_usage* ({prune_by_preferred, rank_preferred_first}): preferred operator usage
    * `prune_by_preferred`: prune successors achieved by non-preferred operators
    * `rank_preferred_first`: first insert successors achieved by preferred operators, then those by non-preferred operators
* *preferred* (list of [Evaluator](Evaluator.md)): use preferred operators of these evaluators
* *cost_type* ({normal, one, plusone}): Operator cost adjustment type. No matter what this setting is, axioms will always be considered as actions of cost 0 by the heuristics that treat axioms as actions.
    * `normal`: all actions are accounted for with their real cost
    * `one`: all actions are accounted for as unit cost
    * `plusone`: all actions are accounted for as their real cost + 1 (except if all actions have original cost 1, in which case cost 1 is used). This is the behaviour known for the heuristics of the LAMA planner. This is intended to be used by the heuristics, not search algorithms, but is supported for both.
* *bound* (int): exclusive depth bound on g-values. Cutoffs are always performed according to the real cost, regardless of the cost_type parameter
* *max_time* (double): maximum time in seconds the search is allowed to run for. The timeout is only checked after each complete search step (usually a node expansion), so the actual runtime can be arbitrarily longer. Therefore, this parameter should not be used for time-limiting experiments. Timed-out searches are treated as failed searches, just like incomplete search algorithms that exhaust their search space.
* *description* (string): description used to identify search algorithm in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

## Iterated search 

    iterated(algorithm_configs, pass_bound=true, repeat_last=false, continue_on_fail=false, continue_on_solve=true, cost_type=normal, bound=infinity, max_time=infinity, description="iterated", verbosity=normal)

* *algorithm_configs* (list of [SearchAlgorithm](SearchAlgorithm.md)): list of search algorithms for each phase
* *pass_bound* (bool): use the bound of iterated search as a bound for its component search algorithms, unless these already have a lower bound set. The iterated search bound is tightened whenever a component finds a cheaper plan.
* *repeat_last* (bool): repeat last phase of search
* *continue_on_fail* (bool): continue search after no solution found
* *continue_on_solve* (bool): continue search after solution found
* *cost_type* ({normal, one, plusone}): Operator cost adjustment type. No matter what this setting is, axioms will always be considered as actions of cost 0 by the heuristics that treat axioms as actions.
    * `normal`: all actions are accounted for with their real cost
    * `one`: all actions are accounted for as unit cost
    * `plusone`: all actions are accounted for as their real cost + 1 (except if all actions have original cost 1, in which case cost 1 is used). This is the behaviour known for the heuristics of the LAMA planner. This is intended to be used by the heuristics, not search algorithms, but is supported for both.
* *bound* (int): exclusive depth bound on g-values. Cutoffs are always performed according to the real cost, regardless of the cost_type parameter
* *max_time* (double): maximum time in seconds the search is allowed to run for. The timeout is only checked after each complete search step (usually a node expansion), so the actual runtime can be arbitrarily longer. Therefore, this parameter should not be used for time-limiting experiments. Timed-out searches are treated as failed searches, just like incomplete search algorithms that exhaust their search space.
* *description* (string): description used to identify search algorithm in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Note 1:** We don't cache heuristic values between search iterations at the moment. If you perform a LAMA-style iterative search, heuristic values and other per-state information will be computed multiple times.

**Note 2:** The configuration

    --search "iterated([lazy_wastar([ipdb()],w=10), lazy_wastar([ipdb()],w=5), lazy_wastar([ipdb()],w=3), lazy_wastar([ipdb()],w=2), lazy_wastar([ipdb()],w=1)])"

would perform the preprocessing phase of the ipdb heuristic 5 times (once before each iteration).

To avoid this, use heuristic predefinition, which avoids duplicate preprocessing, as follows:

    "let(h,ipdb(),iterated([lazy_wastar([h],w=10), lazy_wastar([h],w=5), lazy_wastar([h],w=3), lazy_wastar([h],w=2), lazy_wastar([h],w=1)]))"

## Lazy best-first search 

    lazy(open, reopen_closed=false, preferred=[], randomize_successors=false, preferred_successors_first=false, random_seed=-1, cost_type=normal, bound=infinity, max_time=infinity, description="lazy", verbosity=normal)

* *open* ([OpenList](OpenList.md)): open list
* *reopen_closed* (bool): reopen closed nodes
* *preferred* (list of [Evaluator](Evaluator.md)): use preferred operators of these evaluators
* *randomize_successors* (bool): randomize the order in which successors are generated
* *preferred_successors_first* (bool): consider preferred operators first
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
* *cost_type* ({normal, one, plusone}): Operator cost adjustment type. No matter what this setting is, axioms will always be considered as actions of cost 0 by the heuristics that treat axioms as actions.
    * `normal`: all actions are accounted for with their real cost
    * `one`: all actions are accounted for as unit cost
    * `plusone`: all actions are accounted for as their real cost + 1 (except if all actions have original cost 1, in which case cost 1 is used). This is the behaviour known for the heuristics of the LAMA planner. This is intended to be used by the heuristics, not search algorithms, but is supported for both.
* *bound* (int): exclusive depth bound on g-values. Cutoffs are always performed according to the real cost, regardless of the cost_type parameter
* *max_time* (double): maximum time in seconds the search is allowed to run for. The timeout is only checked after each complete search step (usually a node expansion), so the actual runtime can be arbitrarily longer. Therefore, this parameter should not be used for time-limiting experiments. Timed-out searches are treated as failed searches, just like incomplete search algorithms that exhaust their search space.
* *description* (string): description used to identify search algorithm in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Successor ordering:** When using randomize_successors=true and preferred_successors_first=true, randomization happens before preferred operators are moved to the front.

## Greedy search (lazy) 

    lazy_greedy(evals, boost=1000, reopen_closed=false, preferred=[], randomize_successors=false, preferred_successors_first=false, random_seed=-1, cost_type=normal, bound=infinity, max_time=infinity, description="lazy_greedy", verbosity=normal)

* *evals* (list of [Evaluator](Evaluator.md)): evaluators
* *boost* (int): boost value for alternation queues that are restricted to preferred operator nodes
* *reopen_closed* (bool): reopen closed nodes
* *preferred* (list of [Evaluator](Evaluator.md)): use preferred operators of these evaluators
* *randomize_successors* (bool): randomize the order in which successors are generated
* *preferred_successors_first* (bool): consider preferred operators first
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
* *cost_type* ({normal, one, plusone}): Operator cost adjustment type. No matter what this setting is, axioms will always be considered as actions of cost 0 by the heuristics that treat axioms as actions.
    * `normal`: all actions are accounted for with their real cost
    * `one`: all actions are accounted for as unit cost
    * `plusone`: all actions are accounted for as their real cost + 1 (except if all actions have original cost 1, in which case cost 1 is used). This is the behaviour known for the heuristics of the LAMA planner. This is intended to be used by the heuristics, not search algorithms, but is supported for both.
* *bound* (int): exclusive depth bound on g-values. Cutoffs are always performed according to the real cost, regardless of the cost_type parameter
* *max_time* (double): maximum time in seconds the search is allowed to run for. The timeout is only checked after each complete search step (usually a node expansion), so the actual runtime can be arbitrarily longer. Therefore, this parameter should not be used for time-limiting experiments. Timed-out searches are treated as failed searches, just like incomplete search algorithms that exhaust their search space.
* *description* (string): description used to identify search algorithm in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Successor ordering:** When using randomize_successors=true and preferred_successors_first=true, randomization happens before preferred operators are moved to the front.

**Open lists:** In most cases, lazy greedy best first search uses an alternation open list with one queue for each evaluator. If preferred operator evaluators are used, it adds an extra queue for each of these evaluators that includes only the nodes that are generated with a preferred operator. If only one evaluator and no preferred operator evaluator is used, the search does not use an alternation open list but a standard open list with only one queue.

### Equivalent statements using general lazy search 

    --evaluator h2=eval2
    --search lazy_greedy([eval1, h2], preferred=[h2], boost=100)

is equivalent to

    --evaluator h1=eval1 --heuristic h2=eval2
    --search lazy(alt([single(h1), single(h1, pref_only=true), single(h2),
                      single(h2, pref_only=true)], boost=100),
                  preferred=[h2])

---

    --search lazy_greedy([eval1, eval2], boost=100)

is equivalent to

    --search lazy(alt([single(eval1), single(eval2)], boost=100))

---

    --evaluator h1=eval1
    --search lazy_greedy([h1], preferred=[h1])

is equivalent to

    --evaluator h1=eval1
    --search lazy(alt([single(h1), single(h1, pref_only=true)], boost=1000),
                  preferred=[h1])

---

    --search lazy_greedy([eval1])

is equivalent to

    --search lazy(single(eval1))

## (Weighted) A* search (lazy) 

Weighted A* is a special case of lazy best first search.

    lazy_wastar(evals, preferred=[], reopen_closed=true, boost=1000, w=1, randomize_successors=false, preferred_successors_first=false, random_seed=-1, cost_type=normal, bound=infinity, max_time=infinity, description="lazy_wastar", verbosity=normal)

* *evals* (list of [Evaluator](Evaluator.md)): evaluators
* *preferred* (list of [Evaluator](Evaluator.md)): use preferred operators of these evaluators
* *reopen_closed* (bool): reopen closed nodes
* *boost* (int): boost value for preferred operator open lists
* *w* (int): evaluator weight
* *randomize_successors* (bool): randomize the order in which successors are generated
* *preferred_successors_first* (bool): consider preferred operators first
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
* *cost_type* ({normal, one, plusone}): Operator cost adjustment type. No matter what this setting is, axioms will always be considered as actions of cost 0 by the heuristics that treat axioms as actions.
    * `normal`: all actions are accounted for with their real cost
    * `one`: all actions are accounted for as unit cost
    * `plusone`: all actions are accounted for as their real cost + 1 (except if all actions have original cost 1, in which case cost 1 is used). This is the behaviour known for the heuristics of the LAMA planner. This is intended to be used by the heuristics, not search algorithms, but is supported for both.
* *bound* (int): exclusive depth bound on g-values. Cutoffs are always performed according to the real cost, regardless of the cost_type parameter
* *max_time* (double): maximum time in seconds the search is allowed to run for. The timeout is only checked after each complete search step (usually a node expansion), so the actual runtime can be arbitrarily longer. Therefore, this parameter should not be used for time-limiting experiments. Timed-out searches are treated as failed searches, just like incomplete search algorithms that exhaust their search space.
* *description* (string): description used to identify search algorithm in logs
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Successor ordering:** When using randomize_successors=true and preferred_successors_first=true, randomization happens before preferred operators are moved to the front.

**Open lists:** In the general case, it uses an alternation open list with one queue for each evaluator h that ranks the nodes by g + w * h. If preferred operator evaluators are used, it adds for each of the evaluators another such queue that only inserts nodes that are generated by preferred operators. In the special case with only one evaluator and no preferred operator evaluators, it uses a single queue that is ranked by g + w * h. 

### Equivalent statements using general lazy search 

    --evaluator h1=eval1
    --search lazy_wastar([h1, eval2], w=2, preferred=h1,
                         bound=100, boost=500)

is equivalent to

    --evaluator h1=eval1 --heuristic h2=eval2
    --search lazy(alt([single(sum([g(), weight(h1, 2)])),
                       single(sum([g(), weight(h1, 2)]), pref_only=true),
                       single(sum([g(), weight(h2, 2)])),
                       single(sum([g(), weight(h2, 2)]), pref_only=true)],
                      boost=500),
                  preferred=h1, reopen_closed=true, bound=100)

---

    --search lazy_wastar([eval1, eval2], w=2, bound=100)

is equivalent to

    --search lazy(alt([single(sum([g(), weight(eval1, 2)])),
                       single(sum([g(), weight(eval2, 2)]))],
                      boost=1000),
                  reopen_closed=true, bound=100)

---

    --search lazy_wastar([eval1, eval2], bound=100, boost=0)

is equivalent to

    --search lazy(alt([single(sum([g(), eval1])),
                       single(sum([g(), eval2]))])
                  reopen_closed=true, bound=100)

---

    --search lazy_wastar(eval1, w=2)

is equivalent to

    --search lazy(single(sum([g(), weight(eval1, 2)])), reopen_closed=true)
