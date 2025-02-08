

Subtask generator (used by the CEGAR heuristic).

## goals 

    goals(order=hadd_down, random_seed=-1)

* *order* ({original, random, hadd_up, hadd_down}): ordering of goal or landmark facts
    * `original`: according to their (internal) variable index
    * `random`: according to a random permutation
    * `hadd_up`: according to their h^add value, lowest first
    * `hadd_down`: according to their h^add value, highest first 
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.

## landmarks 

    landmarks(order=hadd_down, random_seed=-1, combine_facts=true)

* *order* ({original, random, hadd_up, hadd_down}): ordering of goal or landmark facts
    * `original`: according to their (internal) variable index
    * `random`: according to a random permutation
    * `hadd_up`: according to their h^add value, lowest first
    * `hadd_down`: according to their h^add value, highest first 
* *random_seed* (int [-1, infinity]): Set to -1 (default) to use the global random number generator. Set to any other value to use a local random number generator with the given seed.
* *combine_facts* (bool): combine landmark facts with domain abstraction

## original 

    original(copies=1)

* *copies* (int [1, infinity]): number of task copies
