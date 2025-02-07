# Profiling

## Profiling Running Time

Here is an example of how to run the `callgrind` tool of `valgrind`
to profile the search component.

To set up, run the translator component:

    ./fast-downward.py --translate PROBLEM.PDDL

To profile, run the search component manually under `valgrind`
(substitute the appropriate build and search options):

    valgrind --tool=callgrind --callgrind-out-file=callgrind.out \
        --dump-instr=yes --collect-jumps=yes \
        ./builds/release/bin/downward --search "astar(blind())" < output.sas

To browse the profiling results:

    # either this:
    kcachegrind callgrind.out

    # or this:
    qcachegrind callgrind.out

See section ["Installing QCacheGrind"](#installing-qcachegrind) below if you have neither KCacheGrind nor
QCacheGrind installed.

## Profiling Cache Misses

Here is an example of how to run the \`cachegrind\` tool of \`valgrind\`
to profile the CPU cache behaviour of the search component.

To set up, run the translator component:

    ./fast-downward.py --translate PROBLEM.PDDL

To profile, run the search component manually under \`valgrind\`
(substitute the appropriate build and search options):

    valgrind --tool=cachegrind --cachegrind-out-file=cachegrind.out \
        ./builds/release/bin/downward --search "astar(blind())" < output.sas

To browse the profiling results:

    # either this:
    kcachegrind cachegrind.out

    # or this:
    qcachegrind cachegrind.out

See section \"Installing [QCacheGrind](QCacheGrind "wikilink")\" below
if you have neither [KCacheGrind](KCacheGrind "wikilink") nor
[QCacheGrind](QCacheGrind "wikilink") installed.

## Profiling Memory Usage

Here is an example of how to run the `massif` tool of `valgrind` to
profile memory usage of the search component.

To set up, run the translator component:

    ./fast-downward.py --translate PROBLEM.PDDL

Note that `massif` only works for dynamically linked binaries. Recent
versions of Fast Downward use dynamic linking by default.

    ./build.py release

To profile, run the search component manually under `valgrind`
(substitute the appropriate search options):

    valgrind --tool=massif --massif-out-file=massif.out \
        ./builds/release/bin/downward --search "astar(blind())" < output.sas

To browse the profiling results:

    sudo apt install massif-visualizer
    massif-visualizer massif.out

## Profiling Python

Here is an example of how to profile CPU usage of the translator with
`cprofile` and `snakeviz`.

To create profile, run the translator under `cprofile`:

    python -m cProfile -o translator.prof ./translate.py DOMAIN.PDDL PROBLEM.PDDL

To browse the profiling results:

    pip install snakeviz
    snakeviz translator.prof

## Installing QCacheGrind

QCacheGrind is KCacheGrind without the KDE bindings and is part of the same
source archive as KCacheGrind. You may want to try it if you would rather not
install all the KDE dependencies that KCacheGrind brings in.

To download and build QCacheGrind:

    sudo apt-get install qt5-default graphviz
    # Download December 2016 release. Alternatively, check
    # https://github.com/KDE/kcachegrind/releases for something more recent.
    wget https://github.com/KDE/kcachegrind/archive/v16.12.0.tar.gz
    tar xvzf v16.12.0.tar.gz
    cd kcachegrind-16.12.0
    qmake && make -j4

Then copy the executable `qcachegrind/qcachegrind` to your preferred
place, for example:

    cp qcachegrind/qcachegrind ~/bin/

All other files can be deleted. Alternatively, for a system-wide install
that includes metadata for the desktop:

    sudo install -m 755 qcachegrind/qcachegrind /usr/local/bin/
    sudo install -m 644 qcachegrind/qcachegrind.desktop \
         /usr/local/share/applications/
    sudo install -m 644 kcachegrind/hi32-app-kcachegrind.png \
        /usr/local/share/icons/hicolor/32x32/apps/kcachegrind.png
    sudo install -m 644 kcachegrind/hi48-app-kcachegrind.png \
        /usr/local/share/icons/hicolor/48x48/apps/kcachegrind.png
