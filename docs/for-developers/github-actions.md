# GitHub Actions

GitHub Actions is the continuous integration tool of GitHub. Actions
are setup using so-called workflows, where each workflow possibly
consists of different jobs. Actions can be triggered by events on the
repository such as pushes, pull request and others. Any file found in

    REPOSITORY/.github/workflows

which ends on

    .yml

automatically defines a workflow. If you want to enable or disable
GitHub Actions, change your repository settings on GitHub via
`Settings->Actions`.

Currently, we have implemented some basic GitHub Actions. All of them
are triggered by pushing commits to the main repository and by pushing
to pull requests opened against the main repository.

The first workflow runs on MacOS and uses the default compilers. It
executes the driver, translator, and the standard config tests, i.e. it
runs `tox -e driver,translator,search`. Another workflow runs on
multiple Windows and Visual Studio Enterprise versions. This workflow
runs the translator and search tests (once the current version of VAL
accepts the plans of Fast Downward, we want to add the driver tests).
There is a workflow for Ubuntu that runs different combinations of
different versions of Ubuntu, Python and compilers. On this workflow we
execute the driver, translator, and search tests. Furthermore, there is
a workflow to ensure the code quality. This workflow checks the style
and clang-tidy tests. Our final workflow is only executed on pushes to
the main branch of the

    aibasel/downward

repository and updates the documentation.

## LP Solvers

!!! note

    For CPLEX you have to acquire a license.


!!! warning

    Do not publish the installer of CPLEX. This is not be covered by the license.

On both Ubuntu versions, we compile and test with CPLEX and SOPLEX. On
both Windows versions, we compile and test with CPLEX. Due to licensing,
CPLEX cannot be tested automatically on a fork (see issues
[issue970](http://issues.fast-downward.org/issue970 "wikilink") and
[issue971](http://issues.fast-downward.org/issue971 "wikilink")). If you
want to run a test for CPLEX, then you have to acquire a license (CPLEX
provides a free academic license). The GitHub Actions have to download
the installer (for CPLEX). Thus, you have to upload it to a server of
your choice and set its URL as a GitHub secret. In your GitHub
repository go to \`Settings-\>Secrets\` and add a secret. GitHub
Actions state that they censor secrets in the console output. The
following secrets can be defined:

-   CPLEX2211_LINUX_URL: Enables CPLEX 22.11 on the Ubuntu workflow
-   CPLEX2211_WINDOWS_URL: Enables CPLEX 22.11 on the Windows workflow

For the main repository, the secrets are set up, which means that
commits on the main repo always trigger builds with LP solvers. For
commits pushed to pull requests, the secrets need to be set up on the
fork the pull request was opened from. If they are not set up, the
builds will not use LP solvers. If you need help with the secrets,
contact Silvan.

## Tested Versions

[Requirements](../requirements) defines the policy for the version we want
test, but keep in mind that we cannot be up to date with every version release.
For the currently tested versions, see "Tested software versions" at the
[repository](https://github.com/aibasel/downward/).
