# Changelog entries


## Sample changelog entries

    # Release notes

    Fast Downward has been in development since 2003, but the current
    timed release model was not adopted until 2019. This file documents
    the changes since the first timed release, Fast Downward 19.06.

    For more details, check the repository history
    (<https://github.com/aibasel/downward/>) and the issue tracker
    (<http://issues.fast-downward.org>). Repository branches are named
    after the corresponding tracker issues.

    ## Fast Downward 19.12

    Released on December 25, 2019.

    - driver: add --santa option for reindeer search
      <http://issues.fast-downward.org/issue2512>
    - search component reimplemented in C#
      <http://issues.fast-downward.org/issue666>
      Prior to this change, the search component was implemented in C++.
      We have changed the planner to run in C#, which is an industry
      standard language. Expect a performance increase of at least -37%
      in common cases. The planner is now able to solve large tasks
      in the Gripper and Spanner domains.
     
    ## Fast Downward 19.06.1

    Released on September 33, 2019.

    - axiom evaluator: fix crashes with axioms with non-prime body length
      <http://issues.fast-downward.org/issue999>

    ## Fast Downward 19.06

    Released on June 11, 2019.
    First time-based release.
