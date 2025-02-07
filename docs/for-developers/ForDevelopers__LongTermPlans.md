Back to [ForDevelopers](ForDevelopers "wikilink").

# Long-term plans (December 2022) {#long_term_plans_december_2022}

## Planner as a library {#planner_as_a_library}

-   easier application for many users
-   part of AIplan4EU
-   required changes:
    -   -   single process planner, no (intermediate) file writing,
            possibly via Python bindings of C++ modules
        -   solve component interaction problem
        -   get rid of the last global data structures (used in search)
        -   re-write translator in C++

## Integrate lifted techniques {#integrate_lifted_techniques}

-   promised as part of recently granted funding
-   requires making state representation and search techniques more
    general

## Large planner extensions {#large_planner_extensions}

-   need to discuss and decide which large features to implement or to
    abandon
-   examples:
    -   -   cost partitioning
        -   symmetries
        -   certificates

# Long-term plans (older - TODO: remove) {#long_term_plans_older___todo_remove}

-   state representation
    ([issue401](http://issues.fast-downward.org/issue401 "wikilink"))
-   life-time management of shared objects (e.g. CG) (related:
    [issue564](http://issues.fast-downward.org/issue564 "wikilink"))
-   rethink which shared objects can go together (e.g. when is it OK for
    a heuristic to use a different task than a search algorithm using
    it? When is it OK for a pattern selector to work with a different
    task? a landmark factory? an operator-counting constraint generator?
    etc.)

# Needs tender love and care {#needs_tender_love_and_care}

-   landmarks
-   option parser
-   search

# Items with action plans {#items_with_action_plans}

## Component creation and interaction {#component_creation_and_interaction}

Terminology and action plan:

-   component: e.g.
        FFHeuristic

    ,

        AlternationOpenList

    ,

        LandmarkFactorySasp
-   component builder: unpacks and stores options and creates components
-   plugin: creates a component builder, interacts with option parser

We implemented this action plan in a prototype (see
<http://issues.fast-downward.org/issue559>). It currently doesn\'t
include the following ideas, which we had during an offline discussion:

-   Use classes for plugins instead of
        _parse

    functions.
-   Plugin classes allow adding commandline options, call
        OptionParser::parse()

    , create component builders (and pass the Options object to their
    constructor).
-   if needed a common plugin base class could handle things like
        dry_run()

## Task Transformations {#task_transformations}

To fully support task transformations, we have to be aware of all
interactions between different levels. The main idea is to have a
hierarchy of task transformations with a

    RootTask

at the root and transformations as edges/children in this hierarchy. As
a first step, the search algorithms will always use the root task but
later we want to support transforming the task before giving it to the
search. Heuristics can transform the task they get from the search and
some of them explicitly wrap the task in some transformation (e.g.,
CEGAR uses

    DomainAbstractedTask

for the landmark decomposition). We thus have two interfaces that cross
levels in the hierarchy:

### Search-Heuristic interface {#search_heuristic_interface}

The search has to interact with the heuristic in the following way:

-   States from the search space of the search have to be translated
    down the hierarchy into states in the search space of the heuristic
    task.
    -   -   **Implementation:** The transformation is done inside the
            heuristic in
                Heuristic::convert_global_state

            by calling

                task_proxy.convert_ancestor_state(parent_state_data)

            where

                task_proxy

            is a proxy for the task used in the heuristic and

                parent_state_data

            is the data of the search state. The actual transformation
            is done in

                AbstractTask::convert_state_values

            which has to be implemented when designing a new task
            transformation. The default implementation in

                DelegatingTask

            passes the call to the parent to get a state of the parent
            task, then calls

                convert_state_values_from_parent

            to convert it to a local state. If any of the methods is not
            implemented or the input state is not from an ancestor state
            on the hierarchy, the call fails at the latest when reaching
            the root of the hierarchy.
        -   **Assumptions:** we assume that the task used in the
            heuristic is a descendant in the hierarchy from the task
            used in the search. If this is not the case, converting
            states will fail with an error.
-   Preferred operators identified by a heuristic have to be translated
    up the hierarchy to operators of the task used in the search.
    -   -   **Implementation:**
                Heuristic::set_preferred

            translates all operator IDs from local IDs to IDs of the
            root task before inserting them into the set of preferred
            operators that is handed to the search. This uses

                OperatorProxy::get_global_operator_id

            which is handled in

                AbstractTask::get_global_operator_id

            . Currently, none of our transformations touches the
            operators, so the call is forwarded to the root task where
            the function is the identity function, and then back down
            the hierarchy without change. Newly implemented task
            transformations that change the operator have to override
            the function with an actual translation.
        -   **Issues:** we currently do not support translating
            operators back up only part of the way in the hierarchy
            which would be needed if the search can work on a
            transformed task. We also currently do not support returning
            a set of operators that correspond to a single operator
            which might be useful if the task transformation combines
            several operators into one.
        -   **Assumptions:** we assume that the task used in the
            heuristic can identify a single operator of the root task
            that corresponds to a given operator. If this is not the
            case, the task transformation should abort in the method.
-   Transitions in the search space are passed on to path-dependent
    evaluators using the methods
        notify_initial_state

    and

        notify_state_transition

    . They are transitions (states and operators) of the search task and
    may have to be translated down the hierarchy. The only evaluator
    that currently uses it is the landmark count heuristic. Here, we
    have to either translate landmarks up the hierarchy (computing
    landmarks on a transformed task and translating the resulting set of
    landmarks into a set of landmarks for the search task) or we have to
    translate transitions of the search task down the hierarchy
    (computing landmarks on the transformed task, then checking if a new
    landmark is reached also in the transformed task).

    -   -   **Issues:** none of these alternatives is implemented and it
            is not clear which of them is better. Depending on whether
            the transformed task is larger (e.g., Pi\^m) or smaller
            (e.g., an abstraction) one or the other is what we want. At
            the time of this writing, task transformation are not
            correctly supported in the landmark code: the landmarks are
            computed on a transformed task but the transitions coming
            from the search are not translated, i.e., we treat the
            landmarks of the transformed task as landmarks of the search
            task. The transformation given to the landmark heuristic is
            wrapped in a
                CostAdaptedTask

            which in turn ignores the transformation. There are two
            independent issues here:

                CostAdaptedTask

            should not ignore its parameter (easy to fix now that

                is_unit_cost

            is no longer limited to the root task); and the landmark
            heuristic should either translate transitions or landmarks
            as described above.

### User-Search interface {#user_search_interface}

Currently, the search always uses the root task. If we want to change
this, we have to consider the interface between the search and the user
code. I currently only see one interaction there:

-   The plan returned by the search is a plan for the transformed task.
    We could offer methods to transform it back on demand.
