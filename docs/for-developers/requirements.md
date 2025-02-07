# Requirements

We use the following rules to decide which versions of operating
systems, compilers, Python and other tools we test:

-   Python: we test the default Python version of the two latest Ubuntu
    LTS releases.
-   GCC and Clang on Ubuntu: the latest GCC and Clang versions available
    via apt on the latest two Ubuntu LTS releases and the default GCC
    version in the latest Ubuntu LTS release.
-   Clang on macOS: we test the default AppleClang compiler on the
    latest two macOS versions available on GitHub actions.
-   MSVC on Windows: we test the default MSVC compiler that comes with
    the Visual Studio version on the latest two Windows versions
    available on GitHub actions.
-   LP solvers (CPLEX and SoPlex): we test one specific version. We
    only upgrade the tested version if the current version no longer
    works or someone wants to test a newer version instead.
-   CMake: we test the default CMake version that comes with the
    operating systems we test on GitHub Actions.

See the `README.md` file in the repository for what this means in
terms of concrete version numbers.
