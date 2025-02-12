

A landmark factory specification is either a newly created instance or a landmark factory that has been defined previously. This page describes how one can specify a new landmark factory instance. For re-using landmark factories, see OptionSyntax#Landmark_Predefinitions.

This feature type can be bound to variables using `let(variable_name, variable_definition, expression)` where `expression` can use `variable_name`. Predefinitions using `--evaluator`, `--heuristic`, and `--landmarks` are automatically transformed into `let`-expressions but are deprecated.

## Exhaustive Landmarks 

Exhaustively checks for each fact if it is a landmark.This check is done using relaxed planning.

    lm_exhaust(only_causal_landmarks=false, verbosity=normal)

* *only_causal_landmarks* (bool): keep only causal landmarks
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **conditional_effects:** ignored, i.e. not supported

## h^m Landmarks 

The landmark generation method introduced by Keyder, Richter & Helmert (ECAI 2010).

    lm_hm(m=2, conjunctive_landmarks=true, use_orders=true, verbosity=normal)

* *m* (int): subset size (if unsure, use the default of 2)
* *conjunctive_landmarks* (bool): keep conjunctive landmarks
* *use_orders* (bool): use orders between landmarks
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **conditional_effects:** ignored, i.e. not supported

## Merged Landmarks 

Merges the landmarks and orderings from the parameter landmarks

    lm_merged(lm_factories, verbosity=normal)

* *lm_factories* (list of [LandmarkFactory](LandmarkFactory.md)): 
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Precedence:** Fact landmarks take precedence over disjunctive landmarks, orderings take precedence in the usual manner (gn > nat > reas > o_reas). 

**Note:** Does not currently support conjunctive landmarks

Supported language features:

* **conditional_effects:** supported if all components support them

## HPS Orders 

Adds reasonable orders described in the following paper

* Jörg Hoffmann, Julie Porteous and Laura Sebastia.<br />
 [Ordered Landmarks in Planning](https://jair.org/index.php/jair/article/view/10390/24882).<br />
 *Journal of Artificial Intelligence Research* 22:215-278. 2004.

    lm_reasonable_orders_hps(lm_factory, verbosity=normal)

* *lm_factory* ([LandmarkFactory](LandmarkFactory.md)): 
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

**Obedient-reasonable orders:** Hoffmann et al. (2004) suggest obedient-reasonable orders in addition to reasonable orders. Obedient-reasonable orders were later also used by the LAMA planner (Richter and Westphal, 2010). They are "reasonable orders" under the assumption that all (non-obedient) reasonable orders are actually "natural", i.e., every plan obeys the reasonable orders. We observed experimentally that obedient-reasonable orders have minimal effect on the performance of LAMA (Büchner et al., 2023) and decided to remove them in issue1089.

Supported language features:

* **conditional_effects:** supported if subcomponent supports them

## RHW Landmarks 

The landmark generation method introduced by Richter, Helmert and Westphal (AAAI 2008).

    lm_rhw(disjunctive_landmarks=true, use_orders=true, only_causal_landmarks=false, verbosity=normal)

* *disjunctive_landmarks* (bool): keep disjunctive landmarks
* *use_orders* (bool): use orders between landmarks
* *only_causal_landmarks* (bool): keep only causal landmarks
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **conditional_effects:** supported

## Zhu/Givan Landmarks 

The landmark generation method introduced by Zhu & Givan (ICAPS 2003 Doctoral Consortium).

    lm_zg(use_orders=true, verbosity=normal)

* *use_orders* (bool): use orders between landmarks
* *verbosity* ({silent, normal, verbose, debug}): Option to specify the verbosity level.
    * `silent`: only the most basic output
    * `normal`: relevant information to monitor progress
    * `verbose`: full output
    * `debug`: like verbose with additional debug output

Supported language features:

* **conditional_effects:** We think they are supported, but this is not 100% sure.
