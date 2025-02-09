# 29.01.2021: A Deeper Look at States

In issue348 we changed one of our most fundamental classes - the
representation of states. In this blog post, we want to explain the
details of the state class, some design choices, and how to efficiently
work with states.

## The State Class

States internally store the following data (reordered slightly to match
the order of discussion here):

``` c++
class State {
    const AbstractTask *task;
    int num_variables;

    mutable std::shared_ptr<std::vector<int>> values;

    const StateRegistry *registry;
    StateID id;
    const PackedStateBin *buffer;
    const int_packer::IntPacker *state_packer;
}
```

#### General Data

Every state belongs to a task, which is stored internally as a pointer
to an `AbstractTask`. This class is a private implementation detail and not
accessible outside, so through the public interface (`State::get_task()`), the
task is available only as a `TaskProxy`.

Next up is the number of variables. We store this in each state for
faster access but this might not be necessary and will possibly
disappear in the future.

#### Unpacked Data

Finally, the next two blocks are related to the actual data of the
states. Our states can have data associated with them in two ways. The
most straight-forward way is a vector of integers where position *i*
contains the value of variable *i*. We store this data behind a shared
pointer, so states remain light-weight and cheap to copy. The use of
`mutable` is probably surprising but we will discuss this later.

#### Packed Data

The alternative to a vector is packed data where values of multiple
variables can be represented in one byte (for example, 8 boolean state
variables fit into a single byte). This packed representation is used
internally by the `StateRegistry` which stores states for long term storage.
The idea is that `State` objects usually do not live too long (say only for one
expansion) and we never store a large amount of them. When storing millions of
states, the overhead of storing an additional pointer for each of them becomes
very noticeable. This concerns explicit elements such as `const
AbstractTask *task` but also the pointers hidden inside the `vector` class.
This is why we store only packed data in a very compact way in the registry for
such states. The state class then offers a nice public-facing interface to this
data. Such states store their data in a registry (identified by `registry`) at
a specific position (identified by `id`). To avoid looking up the position of
the data every time, the state also stores the memory position of the actual
data (pointed to by `buffer`). Finally, the `state_packer` encapsulates the bit
magic that is required to access the value of a variable from the packed
representation.

## Three Kinds of States

As we have two kinds of possible data representations, there are three
kinds of states: those that have only unpacked data, those that have
only packed data, and those that have both (the fourth case of a state
without data doesn't require an object).

States derived from a registry (registered states) always have packed data
available but can be unpacked (with `State::unpack`) to have both kinds of data
available. Unpacking the data requires accessing every packed value once but
afterwards, accessing the unpacked data is faster than accessing the packed
data. This makes sense in cases where many values of the state need to be
accessed multiple times.  Calling `state::unpack` on state that is already
unpacked is allowed and cheap.

States that are created without a registry (unregistered states) never
have packed data available and always use unpacked data only.

The subscript operator (`State::operator[]`) automatically uses the fastest way
available to access the data and unifies the interface to all three kinds of
states.

## Immutable States through Mutable Pointers

Our states are meant to be *immutable* in the sense that a given state object
will not change its identity but you can assign a new state to a `State`
variable. A variable representing the state [1,2,3] cannot be changed to
represent the state [1,1,1] except by assignment. Technically, this means
that all methods of the class are `const` except for the (copy and move)
assignment operators.  The method `State::unpack` seems to contradict this
paradigm because it modifies the pointer `values`. We use the (maybe somewhat
controversial) keyword `mutable` on the pointer to still allow the method to be
considered `const`. The argument for this is that unpacking the data does not
change the logical identity of the state. If it represents [1,2,3] before the
operation, it still does so after unpacking.

## Working with States

In this section, we want to go over the most important steps for working
with `State` objects.

#### Constructing States

Registered states can be created with `StateRegistry::get_initial_state` and
`StateRegistry::get_successor_state`. As these are the only ways to create
registered states, such states are always reachable and always use duplicate
detection (each state is represented in the registry at most once and creating
a state along two paths will yield states with the same IDs).

Unregistered states can be created in a similar way with
`TaskProxy::get_initial_state` and `State::get_unregistered_successor`. In
addition, they can also be created from arbitrary values using
`TaskProxy::create_state`.

The other two overloads of `TaskProxy::create_state` (the ones involving
pointers to packed data) should only be used by the `StateRegistry` and should
otherwise be considered private.

#### Passing States Around

States are relatively light-weight, copying them only copies a handful
of pointers and possibly updates the reference count of the shared
pointer. But even if this copy is cheap, it is not free. We recommend
passing states around by `const` reference where possible but copying them
should not kill performance unless this happens in a very tight loop.

#### Accessing States

In most circumstances, accessing state values with `State::operator[]` should
be the right thing. If many values are requested from a registered state, it
might pay off to call `State::unpack` first but this should be profiled. Also
note that within heuristics all states are already unpacked at the moment.

In extreme circumstances where performance is absolutely critical,
`State::get_unpacked_values` can be used after unpacking the state to get
a reference to the internal vector. Passing this vector to a function instead
of the state saves one level of indirection when accessing the data and one
`if` statement during the access. In very tight loops this can make
a difference but this should only be done after identifying the issue with
a profile.

#### Comparing and Hashing States

Two states are considered equal if they contain the same values.
However, mixing registered and unregistered states or registered states
from different registries is likely unintentional and thus comparing
them is considered an error. We currently have no use case where such a
comparison would be necessary. If you do, contact us.

We provide a hash function (`feed(HashState &hash_state, const State &state)`)
for our implementation of hash maps (`utils::HashMap`) and hash sets
(`utils::HashSet`). This function is meant for hashing unregistered states.
Hashing registered states is considered an error for two reasons: first it is
not possible to implement an efficient hash function that computes the same
value for logically equal packed and unpacked states without unpacking the
packed state. Second, when hashing registered states, it is much more efficient
to hash their IDs instead of the state data, so we consider hashing the state
data a performance bug.

#### How Not to Use a State

Certain usage patters of a state are considered errors and will stop the
planner with a critical error. In the future, these tests may disappear
(leading to silent corruption) in release builds for performance
reasons, which is already the case for many other similar checks in the
planner. So we recommend thoroughly testing your code with debug builds,
switching to the more efficient release builds once you trust your code.

1.  Accessing packed data through `State::get_buffer` is an error on
    unregistered states (they do not have a buffer). You can use `if
    (s.get_registry())` to check if the state is registered.
2.  Accessing unpacked data through `State::get_unpacked_values()` is an error
    if the state has no unpacked data. We never implicitly
    unpack a state as this is an expensive operation. Call `s.unpack();` if you
    work with states where you are unsure if they have
    unpacked data available.
3.  Creating unregistered successor states through
    `State::get_unregistered_successor` also requires access to unpacked data
    and thus leads to an error if the state doesn't have it available.
4.  As described above, hashing a registered state is considered an
    error.
