# Code reviews with Github

You can prepare a code review by making a pull-request in your own Fast
Downward fork on Github.

-   Fork the official Github repository.
-   In the fork, prepare your issue or feature branch (e.g. issue123)
    according to [our Git workflow](../git).
-   In the fork, click "Pull requests" and click "New pull request",
    then select the `main` branch of **your repository** on the left
    and the `issue123` branch on the right.
-   Click "Create pull request".
-   Link to the pull request from the issue tracker.

## Compare arbitrary revisions

Compare any two revisions by following the steps above but using the
commit IDs of the commits you want to compare instead of the branch
names. It is not possible to create a pull request this way because
merging might not make sense for the selected commits but you'll be
able to see the code difference.
