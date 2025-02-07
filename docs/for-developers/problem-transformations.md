# Problem transformations performed by the planner

Some developers have tried to adapt Fast Downward to other settings than
classical sequential planning, such as step-based classical planning
("parallel planning"), temporal planning, or variations of replanning,
planning under uncertainty, or other kinds of planning that involve
interleaving planning and execution.

If you intend to use the planner in this fashion, you need to be aware
that it implements certain optimizations that only apply to classical
sequential planning and to the given initial state and goal from the
PDDL file.

## Making the planner better for non-classical uses

If there is sufficient interest, we can try to make some of the
transformations below optional, so that interested parties can disable
them. In some cases, this is a lot of work, so we are very interested in
**hearing from you** (e.g. by email to the public Fast Downward mailing
list) if you think you would benefit from such changes.

## List of transformations

-   Following PDDL's add-after-delete semantics, if an action adds and
    deletes a fact at the same time, the translator can remove the
    delete effect. Similarly, if it adds something already implied by
    the precondition or effect condition, the add effect can be omitted.
    This transformation preserves the semantics of sequential planning,
    but not of parallel or temporal planning.
-   The translator can prune facts and actions that are not relaxed
    reachable from the initial state or that are not relevant to the
    goal in the sense that they never contribute to an irreducible plan.
    These transformations make it invalid to reuse a translated problem
    for a different initial state or goal. The pruning of
    goal-irrelevant facts and actions can be disabled by specifying the
    appropriate translator options. (Run the translator with option
    `--help` to see its available options.)

This list is very likely incomplete. Please contact us (by email or on
the [issue tracker](https://issues.fast-downward.org) if you think there may be
something that should be added here.
