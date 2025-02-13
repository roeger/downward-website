# C++ coding conventions and style guide

We try to maintain a consistent coding style because it makes reading
and modifying the code easier. Our coding conventions aren't
necessarily better than others (though we try to follow ones that make
sense and change those that don't), but the main utility of this is
consistency.

We're much stricter these days than we were, say, 10 years ago. The
reason for this is that a codebase with many contributors and large size
is much harder to maintain than a small one. So new code must pass
tougher tests than some of the existing code. (Of course, the existing
code should ideally be cleaned up more, too, but few people are
motivated to work on such tasks if there are other things to do that
seem more urgent.) Once code is in, it usually isn't changed for years
unless we discover a bug. So we really try to put a lot of effort on
making things as right as possible on the first try.

The following is not meant to be a complete description of our coding
conventions. When in doubt, follow the example of the existing code.

See also the information on how and where to put [whitespaces](cpp-whitespace.md).

### Language support

The translator runs on Python >= 3.6. The search code uses C++20 and
may use all language features supported by GCC 10, clang 12, MSVC 19.34,
and AppleClang 13.

### General recommendation

We generally follow the recommendations in the book [C++ Coding
Standards: 101 Rules, Guidelines, and Best
Practices](http://www.gotw.ca/publications/c++cs.htm) by Herb
Sutter and Andrei Alexandrescu. In the tracker or elsewhere, a mark of
the form **[SA ***x***]** is a reference to a rule in that book. For
example, **[SA 9]** refers to Sutter and Alexandrescu's rule 9:
"Don't pessimize prematurely".

### Comments

``` c++
// Write complete sentences ending with periods.

// Use imperative if possible: "Return the factorial." is better than "Returns the factorial.".

// Leave a space between the slashes and the comment.

// TODO: Use this format for todo items.

/*
  Use this style for comments spanning 
  multiple lines and strive to write 
  self-explanatory code that doesn't need 
  comments.
*/


/* For shorter multi-line comments (2-3 lines)
   this style is also fine. */
```

We generally prefer comments above the code (not next to it). If you
really want to put a short comment next to the code, leave **one** space
before and after the `//` slashes.

### Subdirectories, namespaces and CMake libraries

Subdirectories:

-   We don't use nested subdirectories (at least for now).
-   There are two types of subdirectories:
    -   *component subdirectories* correspond to a single component
        (e.g. one subdirectory for the PDB code, one for the
        landmarks code, one for the merge-and-shrink code)
    -   *grouping subdirectories* group together many components
        that are related and too small to deserve their individual
        subdirectories (e.g. one for all open list variants and one
        for all heuristics that don't need their own subdirectory)
-   Subdirectories follow the same naming conventions as filenames,
    methods and variables.
-   Subdirectory names should be kept short.

Namespaces:

-   We don't use nested namespaces (at least for now).
-   Every component (= CMake library) should correspond to a namespace.
    -   For components that have their own directory, the namespace
        name is derived from the directory name.
    -   For components that are too small for their own directory,
        the namespace name is derived from the main file name (or
        equivalently, the main class name).
-   Namespaces follow the same camel-case naming convention as classes.
-   We don't use `using namespace` for our own namespaces.

CMake libraries:

-   There's a 1:1 correspondence between namespaces and CMake
    libraries.

Examples:

-   Component directory `merge_and_shrink` contains the code the
    merge-and-shrink component in namespace `MergeAndShrink`.
-   The file `merge_and_shrink/transition_system.h` would be expected to
    contain the class `MergeAndShrink::TransitionSystem`.
-   Grouping directory `open_lists` contains the code for various open list
    components, for example an alternation open list.
-   The file `open_lists/alternation_open_list.h` would be expected to contain
    the class `AlternationOpenList::AlternationOpenList`.

Open questions:

-   We might introduce a namespace for the core code, i.e., the code
    that is necessary to build the planner. Right now it is in the
    global namespace.
-   We might eventually consider settling for shorter class names and/or
    filenames in cases where the directory name or namespace already
    provide the necessary context. For example, we might say
    `MergeAndShrink::Heuristic` instead of `MergeAndShrink::Heuristic`; we
    might say `AlternationOpenList::OpenList` or `Alternation::OpenList`
    instead of `AlternationOpenList`. (If you want to argue for this, this
    would need further discussion.)

### Header file guards

Macro names for header file guards follow this algorithm:

-   Take the filename, including subdirectory name if in a subdirectory.
-   Convert to uppercase.
-   Replace all `.` and `/` with `-`.

Example: `learning/state_space_sample.h` becomes
`LEARNING_STATE_SPACE_SAMPLE_H`.

Guard blocks should look like this:

``` c++
#ifndef LEARNING_STATE_SPACE_SAMPLE_H
#define LEARNING_STATE_SPACE_SAMPLE_H
// ...
#endif
```

That's all. In particular, don't add comments to the preprocessor
directives and don't add further underscores.

### Includes

Order includes in the following way: header corresponding to .cc file,
headers from the same directory, headers from the `src/search`
directory, headers from other directories, standard library includes,
and third-party library includes. If using the `using namespace std`
declaration, put it after all other includes. Order each group
alphabetically and separate the groups by empty lines. Add an empty line
between the last group and the remaining code. Here is a contrived
example:

``` c++
#include "pattern_generation_edelkamp.h"

#include "zero_one_pdbs_heuristic.h"

#include "../abstract_task.h"
#include "../causal_graph.h"

#include "../algorithms/ordered_set.h"
#include "../utils/timer.h"

#include <algorithm>
#include <cassert>
#include <vector>

#include <tree.hh>

using namespace std;

PatternGenerationEdelkamp::PatternGenerationEdelkamp(const Options &opts)
...
```

### Constructors, destructors and assignment operators

-   Add default destructor only for base classes (i.e., if other classes
    derive from them). The destructor should of course be virtual.
-   Explicitly remove copy constructor, i.e., declare it as `= delete`, for
    most types, especially those created by plug-ins and used polymorphically.
    Generally, we want to permit copy constructions only for cases where we've
    explicitly decided that it's useful.  Many of our objects are heavy-weight
    and should not be copied.

### Function signatures

-   Use `const` methods whenever appropriate.
-   Pass `string`s by const reference.
-   When overriding a virtual method, mention
   `virtual` again in the declaration and mark it as `override` (i.e., `virtual
    int foo() override;` rather than `int foo();`).
-   Mark function declarations in headers as `extern` (global functions).
-   Mark function declarations in .cc files `static` (local functions).

### const attributes

We generally don't make attributes of classes `const`. See the
![attached discussion](../files/const_discussion.txt){:download}
for the rationale behind this convention. (This is a convention that may
be changed if there is sufficient support, but while it is the way it
is, we should all follow the same style.) Exceptions include:

-   static constants like `static const int UNKNOWN = -1;`
    and enumeration values (all cases where we would currently use `ALL_CAPS`)
-   pointers and references to const (not really an exception
    because we do not mark the *pointers* as const, i.e., we would
    write `const Frobnicator *frobnicator;`, but not
    `const Frobnicator *frobnicator const;`.
-   attributes referring to plug-in parameters passed in through the
    option parser (This may seem a somewhat arbitrary convention,
    and perhaps it is, but for good or bad it does describe the one
    exception to the general rules that currently occurs commonly in
    the code.)

The same rules apply to function parameters and local variables.

### push_back vs. emplace_back

-   For a `vector<T>`, use `push_back` with arguments of type `T` or `T&&` to
    copy or move an already constructed object into the container, and use
    `emplace_back` in other cases, where the object can be directly constructed
    inside the container.

    -   Rationale:
        <https://stackoverflow.com/questions/26860749/efficiency-of-c11-push-back-with-stdmove-versus-emplace-back-for-already>
            and
            <https://stackoverflow.com/questions/10890653/why-would-i-ever-use-push-back-instead-of-emplace-back>

Examples:

``` c++
Foo x = ...; // construct a Foo

vector<Foo> foos;
foos.push_back(move(x));    // move the constructed Foo into the container
foos.emplace_back(44, 22);  // Foo has a constructor that takes two ints. Use emplace_back to directly construct the object inside the container.
```

### Anti-idioms

-   Don't write `NULL` or `0` for null pointers. Use `nullptr`.
-   Don't write `(ptr != nullptr)`.  Write `(ptr)`.
-   Don't write `(ptr == nullptr)`.  Write `(!ptr)`.
-   Don't write `(seq.size() == 0)`.  Write `(seq.empty())`.
-   Don't write `(seq.size() != 0)`.  Write `(!seq.empty())`.
-   Don't append underscores to constructor variables. Use the same
    name as the member variable (preferrable) or a different name.

### Passing and storing tasks

-   By default, pass `const TaskProxy &`.
-   Pass `const shared_ptr<AbstractTask> &` only in the following situations:

       -   the callee should participate in the ownership of the task
       -   the callee creates a delegating task based on the given task
           (even if it's only a temporary)

Conceptually, it's less clear that this is desirable, but with our
current design you cannot create a delegating task without (co-) owning
the task.

-   If the callee only needs access to a certain aspect of the task, it
    is preferable to make this explicit and only pass e.g.  `const
    OperatorsProxy &` or `const [[VariablesProxy]] &`.
-   If the task is needed after an object's construction, store a
    `TaskProxy` as a member variable.
-   Avoid storing large collections of proxies that carry redundant
    information. For example, a vector of 10000 `FactProxy` instances (of the
    same task) contains 10000 copies of the same abstract task pointer.
-   Avoid using proxies in performance-critical code.

### Exceptions

Derive custom exception classes from `utils::Exception`.

-   This rule does not apply to internal exceptions never seen by the
    user, such as `HillClimbingTimeout` in the PDB code.
-   The `print` method should write to `cerr`. See the existing
    examples of `utils::Exception` subclasses.
-   `utils::Exception` is intentionally not derived from
    `std::exception`. See [the attached
    file](https://www.fast-downward.org/ForDevelopers/CodingConventions?action=AttachFile&do=get&target=exception_discussion.txt)
    for some discussion.

### Miscellaneous

-   Prefer `template<typename T>` over `template<class T>`.
