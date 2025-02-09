## Implementation Details

### State related classes

Some implementation detail on the state related classes is described in
<attachment:state-classes.pdf> (source file: <attachment:state-classes.odg>).

### Per State Information

Use `PerStateInformation<Entry>` to store an `Entry` object for each state. We
already discussed how to handle some special cases but not all of them are
implemented yet (we will do so once we need them).

**Temporary states/samples:** Use a temporary state registry to create
the samples. `PerStateInformation<Entry>` is already able to handle states
from different registries. Once the temporary registry is destroyed, all
information stored for its states
is also destroyed.

**Create states from scratch:** If states should be created that do not
correspond to the initial state or the successor of an existing states,
the state registry has to be extended. Add a method that allows to add a
buffer (i.e. a `state_var_t *`) and handle it just like states in the
`get_successor_state()` method.

**Store information for only a few states**: If information is needed
for only some of the created states, consider using two registries: one
for all states that require additional information and one for all other
states. If this is not possible, create a new class similar to
`PerStateInformation<Entry>` that uses a `hash_map<StateID, Entry>` instead of
a `SegmentedVector<Entry>` for storage. Support for multiple state registries
should be handled like it is done in `PerStateInformation<Entry>`.

**States without duplicate checks:** Depending on the use case it can
make sense to either work directly with buffers (i.e.  `state_var_t *`) or
create a new state registry class that omits the duplicate check.
