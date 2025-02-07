# Using uncrustify to fix code layout

We use `uncrustify`
with a Fast Downward configuration file (`.uncrustify.cfg` in the repository
root) to enforce some of our formatting conventions.  If a source file is
properly formatted, applying `uncrustify` should be an idempotent operation
(i.e., result in an identical file).  This is important so that we can verify
our style rules automatically, at least for those rules which`uncrustify`
can handle.

Not all aspects of source layout are handled by `uncrustify`, so please still
pay attention to our [whitespace](../whitespace) rules and other [coding
conventions](../coding-conventions).

## Installing uncrustify

Please note that we require a specific uncrustify version. On Ubuntu 22.04,
22.10 and 23.04, you get this uncrustify version by calling `sudo apt install
uncrustify` , so on these Ubuntu versions you don't need the steps below.

```
wget https://github.com/uncrustify/uncrustify/archive/uncrustify-0.72.0.tar.gz
tar -xzvf uncrustify-0.72.0.tar.gz
cd uncrustify-uncrustify-0.72.0
mkdir build
cd build
cmake ../
make -j4
sudo cp uncrustify /usr/local/bin  # Add binary to a directory on PATH.
```

## Running uncrustify

To check the formatting of all C++ files, use
`./misc/style/run-uncrustify.py`. To actually edit the files that need
to be uncrustified, use `./misc/style/run-uncrustify.py \--modify`.
This script is also part of our tox tests:

```
sudo apt install tox
cd misc/
tox -e fix-style
```

To check the style of Python and C++ files, you can use `tox -e style`.
