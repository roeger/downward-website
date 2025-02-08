# Release Workflow

We have *regular releases* and *bugfix releases*. We use `20.06` as an example for a regular release and `22.06.1` as an example for a bugfix release.

Release steps:

 1. Set the variables used in the following steps as in this example for a regular release:
```
RELEASE=20.06
BRANCH=20.06
TAG=20.06.0
```
 Set them as in this example for a bugfix release:
```
RELEASE=22.06.1
BRANCH=22.06
TAG=22.06.1
```
 1. Regular releases only: make sure that you are on the commit on which you want to base the release.
 1. Bugfix releases only: check out the release branch and cherry-pick each commit with hash `HASH` that you want to include:
```
git checkout release-$BRANCH
git cherry-pick HASH
```
 1. Make sure that the list of contributors and copyright years in the `README.md` file are up to date.
 1. Make sure the changelog (see [ChangelogFormat](changelog-format.md)) is up to date and committed. In particular:
     1. Make sure the changelog includes the line giving the date of the release.
     1. Add a new section like `## Fast Downward 20.06` or `## Fast Downward 22.06.1` and gather all changes since the last release from the commit messages. Use an existing regular/bugfix release as an example.
 1. Make sure that the working directory is clean and that any last-minute changes from the above steps are committed.
 1. Update version number and create branches, tags and recipe files by running the `prepare-release.sh` script:
```
./misc/releases/prepare-release.sh $TAG
```
 1. Verify the following manually:
    1. The `fast-downward-$RELEASE.tar.gz` tarball created in the previous step contains the appropriate files.
    1. Branches and tags were created as expected. In a bugfix release, a tag like `22.06.1` should have been created on the existing release branch `22.06`.
    1. A new commit was created with the right recipe files and version changes.
 1. Push all changes.
```
git push --all
git push --tags
```
 1. Make sure that all Github actions are green on the release branch.
 1. Build the Docker image and push it to the Docker Hub. Note that we build the `20.06`/`22.06` Docker image, not `20.06.0`/`22.06.1`. Under normal conditions, Docker needs root rights. The actual push to Docker hub needs appropriate credentials. Malte has them; not sure anyone else does. (Please edit if you do.)
```
sudo ./misc/releases/push-docker.sh $BRANCH
```
 1. Build the Apptainer image:
```
apptainer pull fast-downward.sif docker://aibasel/downward:$BRANCH
```
 Note: Ubuntu (*.deb) packages for Apptainer are available here: <https://github.com/apptainer/apptainer/releases>. Tested with Apptainer 1.3.6.
 1. Test:
    * that we can build and successfully run the planner from the produced tarball
    * that we can successfully run the planner from the produced Apptainer image, including a configuration using SoPlex
    * that we can successfully run the planner from the produced Vagrantfile (automatically includes SoPlex; to also build the VM with CPLEX, you need an environment variable `DOWNWARD_LP_INSTALLERS` that points to a directory containing the CPLEX installer in the correct version)
 1. Regular releases only: create a Wiki page for the release. We suggest starting from a copy of the page for the [[Releases|last release]].
    1. Update the date and release version name.
    1. Update the changelog.
    1. Upload the tarball as an attachment to the page.
    1. Upload the Vagrant file created by the `prepare-release.sh` script as an attachment to the page.
    1. Create a link in [[Releases]] to the page of the new release.
 1. Bugfix releases only: update the Wiki page of the release (for bugfix release `22.06.1`, reuse the release page `22.06`). See the Wiki page for [[Releases/22.06|release 22.06]] for an example.
    1. Adjust the date and mention the bugfix release version name.
    1. Update the changelog.
    1. Update the name of the tarball (it should include the bugfix number) and upload the tarball as an attachment to the page. 
    1. Upload the Vagrant file created by the prepare-release.sh script as an attachment to the page.
 1. Create a new release on github:
    1. On <https://github.com/aibasel/downward/releases> click on `Draft a new release`.
    1. Set `Tag` to `release-$TAG`, `Release Title` to `$RELEASE`, and `Description` to `For information about this release, please visit the [Fast Downward wiki](https://www.fast-downward.org/Releases/$BRANCH)`.
    1. Click on `Publish Release`.
 1. Send an announcement e-mail to the Fast Downward list including changelog information.
 1. Send the same announcement as a message in the Fast Downward Discord server.

