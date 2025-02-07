# Fast Downward Releases

Fast Downward uses time-based version numbers of the form \`YY.MM\`. For
example, Fast Downward 19.06 was originally released in June 2019. We
intend to follow a 6-monthly release cycle, but this is not set in
stone. Bugfix releases are numbered as \`19.06.1\`, \`19.06.2\` and so
on.

Fast Downward is research software, and we do not provide extensive
support for past releases. In particular, we generally do not backport
bug fixes. Bug fix releases are intended to be a rare exception to
address critical problems that can be backported with reasonable effort,
such as incompatibilities with new compiler versions. Bug fix releases
are generally limited to the latest release series.

## Releases since 2019

-   [Fast Downward 24.06](/24.06)
-   [Fast Downward 23.06](/23.06)
-   [Fast Downward 22.12](/22.12)
-   [Fast Downward 22.06](/22.06)
-   [Fast Downward 21.12](/21.12)
-   [Fast Downward 20.06](/20.06)
-   [Fast Downward 19.12](/19.12)
-   [Fast Downward 19.06](/19.06)

## Historical Releases

Fast Downward has been in development since 2003, but we only started
using the current release model in 2019. From 2008 onwards, various
versions of Fast Downward and related planners were released as part of
the [International Planning Competition
series](http://www.icaps-conference.org/index.php/Main/Competitions).

From 2003-2006, Fast Downward used no formal version control. From
2006-2010, the code was developed in a Subversion repository, from
2010-2020 in a Mercurial repository, and since July 2020 in a [Git
repository](https://github.com/aibasel/downward "wikilink"). The Git
repository includes history dating back to 2006, but the migrations to
Mercurial and to Git involved some pruning, in addition to differences
caused by the different data models of these version control systems. If
you need access to any of the historical code (pre-version-control era,
Subversion era, or Mercurial era), feel free to [contact us](mailto:
malte.helmert@unibas.ch).

Note that Mercurial repositories compatible with the legacy Mercurial
repository can be converted to Git repositories that are compatible with
our Git repository. If your repository branched off this Mercurial
repository, we recommend using [our conversion
script](https://github.com/aibasel/convert-downward).
