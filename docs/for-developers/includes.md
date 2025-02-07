# Include what you use

!!! warning
   
    This is outdated. The setup with clang 3.5 is no longer compatible with our
    C++20 setup. If we want to continue using IWYU, we'd have to update the setup.

You can use the include-what-you-use (IWYU) tool to check which includes
and forward definitions are missing/redundant. However, the tool outputs
many false positives, so each suggested change should be double-checked.

## Instructions

``` bash
# Make sure that clang-3.5 and the corresponding header files are installed.
sudo apt-get install clang-3.5 libclang-3.5-dev

# Install IWYU.
git clone https://github.com/include-what-you-use/include-what-you-use.git --branch clang_3.5
mkdir build
cd build
cmake -DLLVM_PATH=/usr/lib/llvm-3.5 ../
make
sudo mv include-what-you-use /usr/bin/

# Change into src/search.

# Check file:
include-what-you-use -g -std=c++11 -Wall -Wextra -pedantic -Werror -Iext -O3 -DNDEBUG -fomit-frame-pointer -c globals.cc -o .obj/globals.release.o
```

### Optionally use mapping file to suppress some warnings

``` bash
# File iwyu.imp:
[
   { include: ['"option_parser_util.h"', 'private', '"option_parser.h"', 'public'] },
   { include: ['<ext/alloc_traits.h>', 'private', '<vector>', 'public'] },
   { symbol: ["size_t", "private", "<vector>", "public"] },
   { symbol: ["assert", "private", "<cassert>", "public"] },
]

include-what-you-use -Xiwyu --mapping_file=iwyu.imp -g -std=c++11 -Wall -Wextra -pedantic -Werror -Iext -O3 -DNDEBUG -fomit-frame-pointer -c globals.cc -o .obj/globals.release.o
```
