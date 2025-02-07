Back to [developer page](ForDevelopers "wikilink").

# Recommended development environment {#recommended_development_environment}

The requirements for compiling Fast Downward are listed in [the build
instructions](https://github.com/aibasel/downward/blob/main/BUILD.md "wikilink").
Our automated tests have additional dependencies that can be installed
as follows:

    apt-get install clang-tidy-16 python3.8 python3.10 python3-pip valgrind wget
    python3 -m pip install tox

For running the autodoc script you\'ll need to install txt2tags via

    python3 -m pip install -r misc/autodoc/requirements.txt

.

We recommend using Ubuntu 22.04 or 24.04 for Fast Downward development
since these versions are also used by the core developers and they allow
installing many dependencies via the package manager.

**Important**: We want the code to compile without warnings, but in
favour of user-friendliness we did not add the -Werror flag to the build
script. Make sure that you compile your code with the -Werror flag, for
example by adding

    export CXXFLAGS+=-Werror

to your bashrc. Note that you should build the binary from scratch after
this (i.e. remove the builds directory if it exists), since it will not
recompile files unless they have been changed.

## Installing clang-tidy-16 on Ubuntu 22.04 {#installing_clang_tidy_16_on_ubuntu_22.04}

We use clang-tidy-16 for our style checks which cannot be installed
through apt on Ubuntu 22.04. To install it manually, follow these steps:

1.  Download \`clang+llvm-16.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz\`
    from
    <https://github.com/llvm/llvm-project/releases/tag/llvmorg-16.0.0>
    (yes, 18.04 is correct even for Ubuntu 22.04).

`` 2. Unpack the downloaded file to any directory you like, say `~/local/opt/llvm16`. ``\
`` 3. Somewhere in your PATH, set two symlinks called `clang-tidy-16` to `~/local/opt/llvm16/bin/clang-tidy` and `run-clang-tidy-16` to `~/local/opt/llvm16/bin/run-clang-tidy`. ``\
`` 4. Install dependencies: `sudo apt install libtinfo5 libstdc++-12-dev`. ``\
`` 5. Try to run `clang-tidy-16`. If you get errors about missing shared libraries, install the missing dependencies. ``

## Running tests {#running_tests}

To run all tests under all locally-available Python versions, run
\`\`\`tox\`\`\` in the \`\`\`misc/\`\`\` directory. The command creates
Python virtual environments under \`\`\`misc/.tox\`\`\`. The directory
uses \~50 MB and is not shown by \`\`\`git status\`\`\`. You can safely
delete the directory after the tests have been run. To run a subset of
tests, e.g., only the style checks, use \`\`\`tox -e style\`\`\` (see
\`\`\`misc/tox.ini\`\`\` for other test environments). Many of the tests
that tox executes are Bash/Python scripts or pytest modules, which you
can also run individually. To check a pytest module, execute
\`\`\`pytest my_module.py\`\`\`.
