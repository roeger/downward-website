# Git

## Our Git workflow

We use Git, following the task-based workflow explained below. All
significant development should be in response to an issue in the
tracker. Then the usual development process involves two roles,
"developer" and "reviewer", and works as follows:

1.  Developer forks the primary Fast Downward repo ("the primary") to
    their own account (creating "the fork")
2.  Developer creates a new branch &lt;branch&gt; in the fork,
    usually branching off the newest revision in main. The Git commands
    for this step and the following are shown under Git Commands for
    Developers below.
3.  Developer resolves the issue in &lt;branch&gt;.
4.  Developer pushes the changes to the fork on GitHub.
5.  Developer makes a pull request on !GitHub from &lt;branch&gt; to
    the main branch in the primary repository (see [page on code
    review](code-review.md)).
6.  Developer adds a link to the pull request to the issue tracker.
7.  Reviewer reviews the code and usually makes comments in the pull
    request. If reviewer is not satisfied, go back to step 3.
8.  Developer makes sure that all code tests pass. We recommend running
    tox in the misc/tests directory.
9.  Developer and Reviewer prepare the commit message for the main
    branch summarizing the changes (see Git Conventions below for more
    details and an example).
10. Developer merges a squash of &lt;branch&gt; into the main branch.
    There are different workflows that achieve this. You can merge
    through the web interface of the pull request with the button
    "Squash and merge".
11. Alternatively, you can perform the following on the local clone of
    your fork.
    1.  Developer sets the primary repository as upstream with `git remote add upstream ssh://git@github.com/aibasel/downward.git`.
    1.  Developer checks out the main branch in his fork with `git checkout main`.
    1.  Developer pulls the latest changes from the primary repository with `git pull upstream main`.
    1.  Developer performs the merge with `git merge --squash <branch>`, then fixes conflicts if necessary.
    1.  Developer commits with `git commit`, which opens an editor where the commit message is added.
    1.  Developer pushes the changes to the primary repository (`git push upstream main`).
    1.  Developer deletes &lt;branch&gt; on their fork. Locally, this is done using
        `git branch -d <branch>`. Remotely, use `git push --delete origin <branch>`.

1.  Alternative for those who have a separate development fork and a
    main fork checked out locally:
    1.  Developer checks out the main branch in their development fork.
    1.  Developer pulls the latest HEAD from the main for.
    1.  Developer does the merge as explained above.
    1.  Developer goes to their main fork and pulls from their development fork.
    1.  Developer deletes their branch locally and remotely in their development fork as explained above.

1.  Developer verifies that the status of the pull request has been
    automatically set to "Merged". If not, developer changes the status
    accordingly.
2.  Developer sets the status of the issue to "resolved".

## Git Conventions

**Commit messages:**

The commit message for merging an issue branch contains a concise
summary of the changes that will be used for creating the release
changelog. It must adhere to the following guidelines:

-   The first line starts with [issueX] and gives a one-sentence
    summary of the issue. On further lines, add a more detailed
    description explaining what changed from a user/developer
    perspective.
-   All lines should be below **80 characters**. In particular, please
    avoid very long commit messages without line wrapping.
-   Always mention usage changes such as added functionality or changed
    command line arguments.

Example:

```
[issue666] search component reimplemented in C#
Prior to this change, the search component was implemented in C++.
We have changed the planner to run in C#, which is an industry
standard language. Expect a performance increase of at least -37%
in common cases. The planner is now able to solve large tasks
in the Gripper and Spanner domains.
```

Within the issue branch, you are free to write commit messages however
you like, since these commits will be squashed. We still recommend the
following guidelines as it will make doing reviews and writing the final
commit message easier.

-   Prepend "[&lt;branch&gt;]" to all commits of the branch
    &lt;branch&gt;. You can copy `misc/hooks/commit-msg` to
    `.git/hooks/commit-msg` to enable a hook which automatically
    prepends the right string to each commit message.
-   The first line of the commit message should consist of a
    self-contained summary.
-   Please write the summary in the imperative mode (e.g., "Make
    translator faster." instead of "Made translator faster.", see
    <https://chris.beams.io/posts/git-commit/>).

**Branches:**

-   Use one feature branch for each issue.
-   Only commit merges of issue branches on `main` (we make occasional
    exceptions for small changes like fixing typos).
-   Delete branches (the pointer) after integration.

## Git Commands for Developers

Before starting to work on an issue, make sure your working copy is
clean and up to date, and that you are on the branch `main`.

    git pull
    git status
    git branch

To start working on an issue, create the branch:

    git checkout -b <branch> main

Fix the issue and commit your changes. If you run experiments, you might
also need to create tags.

    git add modified_file
    git commit -m "[<branch>] My meaningful commit message."
    git tag <branch>-base <rev>
    git tag <branch>-v1 <rev>

Then push your changes to GitHub for review.

    git push --set-upstream origin <branch> --tags

When the issue is ready to be merged, merge it into main, delete the
branch and push it to the main repository.

    git remote add upstream ssh://git@github.com/aibasel/downward.git
    git checkout main
    git pull upstream main
    git merge --squash <branch>
    git commit
    git push upstream main
    git branch -d <branch>

To delete the remote branch, use

    git push --delete origin <branch>

Note that this does **not** work on our main repository due to branch
protection. However, if you haven't pushed your branch to the main
repository during development, the main repository does not know about
the existence of the branch, so nothing needs to be deleted anyway.

You can fix wrong commit messages in the following way. This modifies
history, so the resulting repository is no longer compatible with the
main repository. If there is a reason to push this to the primary
repository, you have to disable the branch protection and use
`--force` to push. Note that this loses all commits that came after
the amended commit, so proceed with caution.

    git commit --amend

## Tips and Tricks

### Finding a Problem with bisect

-   TODO: git bisect with \--first-parent etc. (Malte sent a few links)

### Useful aliases

Adding the following to your `.gitconfig` (or `~/.gitconfig`) file
enables some useful shortcuts:

    [alias]
    ci = commit
    st = status
    adog = log --all --decorate --oneline --graph

### Ignoring IDE files

To ignore files you create but that should not be ignored in Fast
Downward (e.g., files generated by a specific IDE), you can add them tto
`~/.gitignore` and add the following to `~/.gitconfig`:

    [core]
        excludesfile = ~/.gitignore

### Configuring meld to work with git

Meld works directly with git but it has to be started with the path to
the repository (e.g., `meld .`).

Alternatively, it can be set up like this in the `.gitconfig` file:

    [merge]
    tool = meld

    [mergetool "meld"]
    #cmd = meld "$LOCAL" "$BASE" "$REMOTE" --output "$MERGED"
    cmd = meld "$LOCAL" "$MERGED" "$REMOTE" --output "$MERGED"

    [diff]
    tool = meld

    [difftool "meld"]
    cmd = meld "$LOCAL" "$REMOTE"

    [difftool]
    prompt = false

    [alias]
    meld = difftool -d

The workflow for using meld to resolve merge conflicts is as follows:

-   First, attempt to do the automatic merge via `git merge
    <branch>` (or `git pull` if this causes an automated merge and conflicts)
-   Second, use `git mergetool` to resolve the conflicts in all
    conflicted files.

More information about how to configure the three-way diff can be found
in this great answer that inspired above configuration:
<https://stackoverflow.com/a/34119867>

### Interact with a Git repo from Mercurial

The [hg-git](https://foss.heptapod.net/mercurial/hg-git) tool
allows to pull and push from and to a Git repository with Mercurial,
allowing you use Mercurial for working on Git projects. It does so by
converting all Git branches to Mercurial bookmarks and vice versa. Here
is how to set it up:

    sudo apt install python3-venv

    mkdir hg-git
    cd hg-git
    python3 -m venv --prompt hg-git .venv
    pip install -U pip wheel
    pip install certifi==2020.6.20 dulwich==0.20.5 hg-git==0.9.0a1 mercurial==5.4.2 pkg-resources==0.0.0 urllib3==1.25.9

    # Add to ~/.hgrc file:
    [extensions]
    hggit =

    # Ensure that new Mercurial binary is found before system Mercurial:
    sudo ln -s /path/to/hg-git/.venv/bin/hg /usr/local/bin/hg  # or adjust $PATH

(Instead of the last two steps, you could also define a Bash alias that
calls the new Mercurial with the hg-git extension enabled, but this
breaks tab completion for Mercurial. Details: tab completion breaks if
the alias is not named "hg" or if the alias command contains spaces.)

Now you can clone a repository. Remember to update to a bookmark to make
it follow your commits:

    hg clone git+ssh://git@github.com/aibasel/downward.git
    cd downward
    hg update main

[tested with Ubuntu 18.04]

## GitHub Configuration

-   We use GitHub's autolink feature to link from commit messages to
    the issue tracker
    (https://help.github.com/en/github/writing-on-github/autolinked-references-and-urls).
-   We also decided to protect all branches on the main Fast Downward
    repository. This means that no force pushes are allowed and branches
    can't be deleted.
