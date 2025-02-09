# CMake

## How to add new files to the planner

New source code files can be added to the planner by adding them to
`src/search/CMakeLists.txt`.

We group our files into CMake libraries that can be enabled/disabled in
a [custom build](#custom-builds). Libraries can have dependencies on other
libraries. This dependency graph is used to enable all libraries needed for
a manual build. For example, if a manual build only enables the library
`potentials`, the library `lp_solver` will be compiled as well because the
code for potential heuristics requires an LP solver.

For details of how to define CMake libraries, see the documentation in
`src/search/CMakeLists.txt`.

## Custom Builds

The `build.py` script only creates a directory, calls `cmake` once to generate
a build system, and a second time to execute the build.
To do these steps manually, run:

``` bash
cmake -S src -B builds/mycustombuild
cmake --build builds/mycustombuild
```

where `CMAKE_OPTIONS` are the options used to configure the build (see below).
Without options, this results in the `release` build. (Use `--build
mycustombuild` in the `fast-downward.py` script to select this build when
running the planner.)

You can use a CMake GUI to set up all available options. To do so, on Unix-like
systems replace the call to `cmake` by `ccmake` (`sudo apt install
cmake-curses-gui`). On Windows, open the CMake GUI and enter the paths there.

Possible options to configure the build include:

-   `-DLIBRARY_BLIND_SEARCH_HEURISTIC_ENABLED=False`

     Switch off the blind heuristic.
     See `src/search/CMakeLists.txt` for other libraries.

-   `-DCMAKE_BUILD_TYPE=DEBUG`

    The only other build type is: `RELEASE` (default)

-   `-DCMAKE_C_COMPILER=/usr/bin/clang`,
    `-DCMAKE_CXX_COMPILER=/usr/bin/clang++`

    Force the use of `clang`/`clang++` (adjust paths as necessary).

You can also generate makefiles for other build systems (such as ninja)
or generate project files for most IDEs:

-   `-GNinja`

    Use `ninja` instead of `make` in step 4.

-   `-G"NMake Makefiles"`

    Windows command line compile. Open the x86 developer shell for your compiler and then use `nmake` instead of `make` in step 4.

-   `-G"Visual Studio 15 2017"`

    This should generate a solution for Visual Studio 2017. Run this command in the command prompt with the environment variables loaded (i.e., execute the vsvarsall script).`

-   `-G"XCode"`

    This should generate a project file for XCode.

-   Run `cmake` without parameters to see which generators are available on
    your system.

You can also change the compiler/linker and their options by setting the
environment variables `CC`, `CXX`, `LINKER` and `CXXFLAGS`.  These variables
need to be set before running `./build.py` or executing `cmake` manually, so
one drawback is that you cannot save such settings as build configurations in
`build_config.py`. If you want to change these settings for an existing build,
you must manually remove the build directory before rerunning `./build.py`.

Examples:

-   To compile with `clang` use:

    ```bash
    CC=clang CXX=clang++ cmake ../../src
    ```

-   Use full paths if the compiler is not found on the `PATH`, e.g., to force
    using the GNU compiler on macOS using HomeBrew:

    !!! note
        Note that the following path is for GCC 4.8 which we no longer support. If you know the relevant path for a HomeBrew version of GCC 10 or newer, please let us know.

    ``` bash
    CXX=/usr/local/Cellar/gcc48/4.8.3/bin/g++-4.8 CC=/usr/local/Cellar/gcc48/4.8.3/bin/g++-4.8 LINKER=/opt/local/bin/g++-mp-4.8 cmake ../../src
    ```

-   The next example creates a build with the GNU compiler using MacPorts:
    
    !!! note
        Note that the following path is for GCC 4.8 which we no longer support. If you know the relevant path for a !MacPorts version of GCC 10 or newer, please let us know.

    ``` bash
    CXX=/opt/local/bin/g++-mp-4.8 CC=/opt/local/bin/gcc-mp-4.8 LINKER=/opt/local/bin/g++-mp-4.8 cmake ../../src
    ```

-   To abort compilation when the compiler emits a warning, set
    `CXXFLAGS="-Werror"`.
-   To force a 32-bit build on a 64-bit platform, set `CXXFLAGS="-m32"`. We
    recommend disabling the LP solver with 32-bit builds.

If you use a configuration often, it might make sense to add an alias
for it in `build_configs.py`.

Fast Downward automatically includes an LP Solver in the build if it is needed
and the solver is detected on the system. If you want to explicitly build
without LP solvers that are installed on your system, use `./build.py
release_no_lp`, or a [custom build](#custom-builds) with the option
`-DUSE_LP=NO`.

If you don't want to permanently modify your environment, you can also
set these variables directly when calling CMake.

## CMake tips and tricks

### Compiling an individual source file

This is useful, for example, if you are working on fixing compiler
errors in a given source file and want to get at the related error
messages quickly, without first going through a lot of other files that
a full build would produce.

    cd <REPOSITORY_ROOT>
    # Make sure Makefiles are up to date; can cancel build once compilation starts.
    ./build.py

    # Can substitute a different build in the following step as desired.
    cd builds/debug32/search

    # Sustitute compilation target as desired.
    make heuristics/lm_cut_heuristic.cc.o

The last line is perhaps a bit confusing because the generated object
file end up in a completely different place than the specified path
suggests. On a current Linux system, tab-completion for the make target
should work. If it does not, this may be a sign that `build.py` needs
to be run.
