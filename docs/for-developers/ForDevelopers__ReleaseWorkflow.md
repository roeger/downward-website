Back to [developer page](ForDevelopers "wikilink").

# Release Workflow {#release_workflow}

Assuming we want to create the \`20.06\` release, these are the steps we
would follow:

1.  Make sure that all Github actions are green.
2.  Make sure that you are on the revision you want to release.
3.  Make sure that the list of contributors and copyright years in the
    \`README.md\` file are up to date.
4.  Make sure the changelog (see
    [../ChangelogFormat](../ChangelogFormat "wikilink")) is up to date
    and committed. In particular:

`    1. Make sure the changelog includes the line giving the date of the release. `\
`    1. Add a new section like `

    ## Fast Downward 20.06

and gather all changes since the last release from the commit messages.

1.  Make sure that the working directory is clean and that any
    last-minute changes done following the above steps are committed.
2.  Update version number and create branches, tags and recipe files by
    running the \`prepare-release.sh\` script.

```{=html}
<!-- -->
```
    ./misc/releases/prepare-release.sh 20.06.0
        

1.  Verify the following manually:

``    1. The `fast-downward-20.06.tar.gz` tarball created in the previous step contains the appropriate files. ``\
`   1. Branches and tags were created as expected.`\
`   1. A new commit was created with the right recipe files and version changes.`

1.  Push all changes.

```{=html}
<!-- -->
```
    git push --all
    git push --tags
        

1.  Build the Docker image and push it to the Docker Hub. Note that we
    build the \`20.06\` Docker image, not \`20.06.0\`. Under normal
    conditions, Docker needs root rights. The actual push to Docker hub
    needs appropriate credentials. Malte has them; not sure anyone else
    does. (Please edit if you do.)

```{=html}
<!-- -->
```
    sudo ./misc/releases/push-docker.sh 20.06
        

1.  Build the Apptainer (successor to Singularity) image:

```{=html}
<!-- -->
```
    apptainer pull fast-downward.sif docker://aibasel/downward:20.06
        

`Note: Ubuntu (*.deb) packages for Apptainer are available here: `[`https://github.com/apptainer/apptainer/releases`](https://github.com/apptainer/apptainer/releases)`. Tested with Apptainer 1.2.2. <`\
`>`

1.  Test, at minimum:

`   * that we can build and successfully run the planner from the produced tarball`\
`   * that we can successfully run the planner from the produced Apptainer image, including a configuration using Soplex`\
`   * that we can successfully run the planner from the produced Vagrantfile (to build the VM with LP solvers, you need an environment variable `

    DOWNWARD_LP_INSTALLERS

that points to a directory containing the CPLEX installer in the correct
version.)

1.  Create a Wiki page for the release. We suggest starting from a copy
    of the page for the [last release](Releases "wikilink").

`   1. Update the date and release version name.`\
`   1. Update the changelog.`\
`   1. Upload the tarball as an attachment to the page.`\
``    1. Upload the Vagrant file created by the `prepare-release.sh` script as an attachment to the page. ``\
`   1. Create a link in `[`Releases`](Releases "wikilink")` to the page of the new release.`

1.  Create a new release on github:

`   1. On `[`https://github.com/aibasel/downward/releases`](https://github.com/aibasel/downward/releases)` click on "Draft a new release"`\
``    1. Set `Tag` to `release-20.06.0`, `Release Title` to `20.06`, and `Description` to `For information about this release, please visit the [Fast Downward wiki](https://www.fast-downward.org/Releases/20.06)`. ``\
``    1. Click on `Publish Release` ``

1.  Send an announcement e-mail to the Fast Downward list including
    changelog information.
2.  Send the same announcement as a message in the Fast Downward Discord
    server.

## Bugfix Releases {#bugfix_releases}

/!\\ It has proven to be error-prone to keep this section in sync with
the previous one. The next time we do a bugfix release, we might
consider merging the two sections (but it is perhaps too much work to do
this preemptively, especially as we might want to simplify these
workflows anyway).

The bugfix release workflow is a little different than the workflow for
a new release, but it also has a lot in common. The major difference
comes from the fact that you need to manually select the issues / fixes
that you want to include in (and hence also those that you want to
exclude from) the bugfix release. For simplicity of reuse, we repeat all
steps here. All provided commands use bugfix 22.06.1 for release 22.06,
replace this accordingly for your bugfix release.

1.  Start by checking out the release branch

```{=html}
<!-- -->
```
    git checkout release-22.06
        

1.  For all issue branches that you want to include in the bugfix
    release, repeat the following steps, starting with the branch that
    was merged into main the earliest:

`  1. cherry-pick the merge commit with hash HASH of the issue branch XXXX with`\
`   `

    git cherry-pick HASH -m 1
        

`  1. fix any merge conflicts that might arise (if any merged branches are excluded from the bugfix release, this will likely happen for the first branch in CHANGES.md)`\
`  1. commit changes on release branch `\
`   `

    git commit -m "[release-22.06] Cherry-picked issueXXXX"
        

1.  Make sure that the list of contributors and copyright years in the
    \`README.md\` file are up to date.
2.  Make sure the changelog (see
    [../ChangelogFormat](../ChangelogFormat "wikilink")) is up to date
    and committed. In particular:

`    1. Make sure the changelog includes the line giving the date of the bugfix release. `\
`    1. Add a new section like `

    ## Fast Downward 20.06.1

and gather all changes since the last (bugfix) release from the commit
messages.

1.  Make sure that the working directory is clean and that any
    last-minute changes done following the above steps are commited.
2.  Update version number and create branches, tags and recipe files by
    running the \`prepare-release.sh\` script.

```{=html}
<!-- -->
```
    ./misc/releases/prepare-release.sh 22.06.1
        

1.  Verify the following manually:

``    1. The `fast-downward-22.06.1.tar.gz` tarball created in the previous step contains the appropriate files. ``\
``    1. A tag like `22.06.1` was created on the existing release branch `22.06` ``\
`   1. A new commit was created with the right recipe files and version changes.`

1.  Push all changes.

```{=html}
<!-- -->
```
    git push --all
    git push --tags
        

1.  Make sure that all Github actions are green. Note that this step
    comes much later than in the release workflow because you pushed a
    version of the planner that did not necessarily exist in the repo
    before (because some commits might have been excluded).
2.  Build the Docker image and push it to the Docker Hub. Note that we
    build the \`20.06\` Docker image, not \`20.06.0\`. Under normal
    conditions, Docker needs root rights, and the script needs an
    environment variable that points to a directory containing the
    !SoPlex archive in the correct version. The actual push to Docker
    hub needs appropriate credentials. Malte has them; not sure anyone
    else does. (Please edit if you do.)

```{=html}
<!-- -->
```
    sudo DOWNWARD_LP_INSTALLERS=/path/to/dir/with/installer/ ./misc/releases/push-docker.sh 20.06
        

1.  Build the Apptainer (successor to Singularity) image:

```{=html}
<!-- -->
```
    apptainer pull fast-downward.sif docker://aibasel/downward:20.06
        

`Note: Ubuntu (*.deb) packages for Apptainer are available here: `[`https://github.com/apptainer/apptainer/releases`](https://github.com/apptainer/apptainer/releases)`. Tested with Apptainer 1.2.2. <`\
`>`

1.  Test, at minimum:

`   * that we can build and successfully run the planner from the produced tarball`\
`   * that we can successfully run the planner from the produced Apptainer image, including a configuration using Soplex`\
`   * that we can successfully run the planner from the produced Vagrantfile`

1.  Update the Wiki page of the release (for a bugfix release such as
    \`22.06.1\`, we do not create a new wiki page, but reuse the major
    release page \`22.06\`). See the updated Wiki page for \[release
    22.06\](https://www.fast-downward.org/Releases/22.06) for an
    example.

`   1. Adjust the date and mention the bugfix release version name.`\
`   1. Update the changelog.`\
`   1. Update the name of the tarball (it should include the bugfix number) and upload the tarball as an attachment to the page. `\
`   1. Upload the Vagrant file created by the prepare-release.sh script as an attachment to the page.`

1.  Create a new release on github:

`   1. On `[`https://github.com/aibasel/downward/releases`](https://github.com/aibasel/downward/releases)` click on "Draft new release"`\
``    1. Set `Tag` to `release-22.06.1`, `Release Title` to `22.06.1`, and `Description` to `For information about this release, please visit the [Fast Downward wiki](https://www.fast-downward.org/Releases/22.06)`. ``\
``    1. Click on `Publish Release` ``

1.  Send an announcement e-mail to the Fast Downward list including
    changelog information.
2.  Send the same announcement as a message in the Fast Downward Discord
    server.
