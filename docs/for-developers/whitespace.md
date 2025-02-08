# C++ whitespace guide 

As with our other coding conventions: when something is not specified
here and you're in doubt, follow the examples in the existing code.
We'll extend this page on an as-needed basis.

Some of the conventions discussed on this page are automatically taken
care of by `uncrustify`
(see [uncrustify](uncrustify.md)), but not all of them. In particular,
`uncrustify` will not break lines for you in most cases.

This page discusses aspects that are not handled by `uncrustify`
and/or aspects that are unclear and need further explanation.

## Basic style overview

We mostly follow the style from [The C Programming
Language](http://en.wikipedia.org/wiki/The_C_Programming_Language_%28book%29 "wikilink")
(cf. "K&R style" on <http://en.wikipedia.org/wiki/Indent_style>). If
you're an emacs user, setting your style to `stroustrup` should work
fine.

Some points on which we differ from K&R or where K&R does not specify a
rule:

 -   Line width is 72 characters if possible, 80 characters max.
 -   Indent with 4 spaces. There should be no tab characters in the
     file.
 -   Don't put the opening brace of a block on a line of its own.
     (K&R style makes an exception to the usual brace rule for
     function definitions; we don't.)
 -   For `if, while` statements etc. with only a single statement in the body,
     braces are optional. The single-line statement should always be on a new
     line. For constructs with several blocks (`if/else, try/catch`)
     either *all* blocks should have braces or *none*.

Examples of proper code (highlights brace style; spacing around
statements, function calls and pointers/references; breaking lines):

``` C++
    const int *MyClass::my_method(int &x, const FooBar *foo_bar) const {
        if (x < 0)
            return &x;
        foo_bar->dump();
        if (x >= 0) {
            x = foo_bar->get_value() + 4;
        } else {
            foo_bar->something_quite_long_with_lots_of_arguments(
                x, x + 3, foo_bar, true);
            cout << "Currently x has this value: " << x
                 << "; I hope this is alright." << endl;
        }
        return foo_bar->get_int_variable();
    }
```

## Breaking lines 

Lines that are too long (more than 72 or 80 characters; see above)
should be broken. Use "natural" places to break the lines; some rules
follow. Don't use a continuation character (`\`) unless necessary.

### Breaking function calls

Use one of these two ways to break function calls:

1. Break after opening parenthesis, indent following lines by four spaces.
2. Break after an argument, align after the opening parenthesis.

The first way is usually preferred.

```c++
int foobar1 = example_of_breaking_after_parenthesis(
    some_argument, foo + bar, baz, final_argument);
int foobar2 = example_of_breaking_after_argument(some_argument, foo + bar,
                                                 baz, final_argument);
```

### Breaking stream output

Break lines before `<<` or `>>` operators and align on these operators:

```c++
cout << "here's a lot of introductory text to make this a long line; x = " << x
     << ", y = " << y << endl;
```

### Breaking function definition heads

1. Prefer to keep everything on one line.
2.  If this is too long, break as for function calls above.
3.  If this is still too long, break after the return value type.

```c++
void MyClass::everything_fits_on_one_line_here(double &x, int y) {
    // Case 1 above.
}

int *MyLongerClassName::ooh_it_does_not_really_fit_any_more_here(
    double &x, int y) {
    // Case 2 above.
}

int *MyLongerClassName::ooh_it_does_not_really_fit_any_more_here(double &x,
                                                                 int y) {
    // Case 2 above, variant.
}

MyEvenQuiteAFewWordsLongerClassName::NestedClassWithALongName *
MyEvenQuiteAFewWordsLongerClassName::create_nested_class_with_a_long_name_instance(
    double &x, int y) {
    // Case 3 above.
}
```
