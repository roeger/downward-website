

## Delete relaxation constraints from Imai and Fukunaga 

Operator-counting constraints based on the delete relaxation. By default the constraints encode an easy-to-compute relaxation of h^+^. With the right settings, these constraints can be used to compute the optimal delete-relaxation heuristic h^+^ (see example below). For details, see

* Tatsuya Imai and Alex Fukunaga.<br />
 [On a practical, integer-linear programming model for delete-freetasks and its use as a heuristic for cost-optimal planning](https://www.jair.org/index.php/jair/article/download/10972/26119/).<br />
 *Journal of Artificial Intelligence Research* 54:631-677. 2015.

    delete_relaxation_if_constraints(use_time_vars=false, use_integer_vars=false)

* *use_time_vars* (bool): use variables for time steps. With these additional variables the constraints enforce an order between the selected operators. Leaving this off (default) corresponds to the time relaxation by Imai and Fukunaga. Switching it on, can increase the heuristic value but will increase the size of the constraints which has a strong impact on runtime. Constraints involving time variables use a big-M encoding, so they are more useful if used with integer variables.
* *use_integer_vars* (bool): restrict auxiliary variables to integer values. These variables encode whether operators are used, facts are reached, which operator first achieves which fact, and in which order the operators are used. Restricting them to integers generally improves the heuristic value at the cost of increased runtime.

**Example:** To compute the optimal delete-relaxation heuristic h^+^, use
```
operatorcounting([delete_relaxation_if_constraints(use_time_vars=true, use_integer_vars=true)], use_integer_operator_counts=true))
```

**Note:** For best performance we recommend using the alternative formulation by Rankooh and Rintanen, accessible through the option ```delete_relaxation_rr_constraints```.

## Delete relaxation constraints from Rankooh and Rintanen 

Operator-counting constraints based on the delete relaxation. By default the constraints encode an easy-to-compute relaxation of h^+^. With the right settings, these constraints can be used to compute the optimal delete-relaxation heuristic h^+^ (see example below). For details, see

* Masood Feyzbakhsh Rankooh and Jussi Rintanen.<br />
 [Efficient Computation and Informative Estimation ofh+ by Integer and Linear Programming](https://ojs.aaai.org/index.php/ICAPS/article/view/19787/19546).<br />
 *Proceedings of the Thirty-Second International Conference on Automated Planning and Scheduling (ICAPS2022)* 32:71-79. 2022.

    delete_relaxation_rr_constraints(acyclicity_type=vertex_elimination, use_integer_vars=false)

* *acyclicity_type* ({time_labels, vertex_elimination, none}): The most relaxed version of this constraint only enforces that achievers of facts are picked in such a way that all goal facts have an achiever, and the preconditions all achievers are either true in the current state or have achievers themselves. In this version, cycles in the achiever relation can occur. Such cycles can be excluded with additional auxilliary varibles and constraints.
    * `time_labels`: introduces MIP variables that encode the time at which each fact is reached. Acyclicity is enforced with constraints that ensure that preconditions of actions are reached before their effects.
    * `vertex_elimination`: introduces binary variables based on vertex elimination. These variables encode that one fact has to be reached before another fact. Instead of adding such variables for every pair of states, they are only added for a subset sufficient to ensure acyclicity. Constraints enforce that preconditions of actions are reached before their effects and that the assignment encodes a valid order.
    * `none`: No acyclicity is enforced. The resulting heuristic is a relaxation of the delete-relaxation heuristic.
* *use_integer_vars* (bool): restrict auxiliary variables to integer values. These variables encode whether facts are reached, which operator first achieves which fact, and (depending on the acyclicity_type) in which order the operators are used. Restricting them to integers generally improves the heuristic value at the cost of increased runtime.

**Example:** To compute the optimal delete-relaxation heuristic h^+^, useinteger variables and some way of enforcing acyclicity (other than "none"). For example
```
operatorcounting([delete_relaxation_rr_constraints(acyclicity_type=vertex_elimination, use_integer_vars=true)], use_integer_operator_counts=true))
```

**Note:** While the delete-relaxation constraints by Imai and Fukunaga (accessible via option ```delete_relaxation_if_constraints```) serve a similar purpose to the constraints implemented here, we recommend using this formulation as it can generally be solved more efficiently, in particular in case of the h^+^ configuration, and some relaxations offer tighter bounds.

## LM-cut landmark constraints 

Computes a set of landmarks in each state using the LM-cut method. For each landmark L the constraint sum_{o in L} Count_o >= 1 is added to the operator-counting LP temporarily. After the heuristic value for the state is computed, all temporary constraints are removed again. For details, see

* Florian Pommerening, Gabriele Roeger, Malte Helmert and Blai Bonet.<br />
 [LP-based Heuristics for Cost-optimal Planning](http://www.aaai.org/ocs/index.php/ICAPS/ICAPS14/paper/view/7892/8031).<br />
 In *Proceedings of the Twenty-Fourth International Conference on Automated Planning and Scheduling (ICAPS 2014)*, pp. 226-234. AAAI Press, 2014.

* Blai Bonet.<br />
 [An admissible heuristic for SAS+ planning obtained from the state equation](http://ijcai.org/papers13/Papers/IJCAI13-335.pdf).<br />
 In *Proceedings of the Twenty-Third International Joint Conference on Artificial Intelligence (IJCAI 2013)*, pp. 2268-2274. AAAI Press, 2013.

    lmcut_constraints()

## Posthoc optimization constraints 

The generator will compute a PDB for each pattern and add the constraint h(s) <= sum_{o in relevant(h)} Count_o. For details, see

* Florian Pommerening, Gabriele Roeger and Malte Helmert.<br />
 [Getting the Most Out of Pattern Databases for Classical Planning](http://ijcai.org/papers13/Papers/IJCAI13-347.pdf).<br />
 In *Proceedings of the Twenty-Third International Joint Conference on Artificial Intelligence (IJCAI 2013)*, pp. 2357-2364. AAAI Press, 2013.

    pho_constraints(patterns=systematic(2))

* *patterns* ([PatternCollectionGenerator](PatternCollectionGenerator.md)): pattern generation method

## State equation constraints 

For each fact, a permanent constraint is added that considers the net change of the fact, i.e., the total number of times the fact is added minus the total number of times is removed. The bounds of each constraint depend on the current state and the goal state and are updated in each state. For details, see

* Menkes van den Briel, J. Benton, Subbarao Kambhampati and Thomas Vossen.<br />
 [An LP-based heuristic for optimal planning](http://link.springer.com/chapter/10.1007/978-3-540-74970-7_46).<br />
 In *Proceedings of the Thirteenth International Conference on Principles and Practice of Constraint Programming (CP 2007)*, pp. 651-665. Springer-Verlag, 2007.

* Blai Bonet.<br />
 [An admissible heuristic for SAS+ planning obtained from the state equation](http://ijcai.org/papers13/Papers/IJCAI13-335.pdf).<br />
 In *Proceedings of the Twenty-Third International Joint Conference on Artificial Intelligence (IJCAI 2013)*, pp. 2268-2274. AAAI Press, 2013.

* Florian Pommerening, Gabriele Roeger, Malte Helmert and Blai Bonet.<br />
 [LP-based Heuristics for Cost-optimal Planning](http://www.aaai.org/ocs/index.php/ICAPS/ICAPS14/paper/view/7892/8031).<br />
 In *Proceedings of the Twenty-Fourth International Conference on Automated Planning and Scheduling (ICAPS 2014)*, pp. 226-234. AAAI Press, 2014.

    state_equation_constraints(verbosity=normal)

* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output
