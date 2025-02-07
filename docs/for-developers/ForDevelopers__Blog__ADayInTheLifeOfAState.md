1.  1.  page was renamed from
        [ForDevelopers](ForDevelopers "wikilink")/Blog/A Day in the Life
        of a State

# Blog Entry (22.01.2021): A Day in the Life of a State {#blog_entry_22.01.2021_a_day_in_the_life_of_a_state}

As part of issue348, we looked at how states are used in an A\* search
with the LM-cut heuristic, when they created, accessed, copied etc. The
code version we are looking at is code written for the issue but most of
the story currently applies to the main code base as well.

### Popping the State from the Open List {#popping_the_state_from_the_open_list}

We start in

    EagerSearch::step

where a

    StateID

is popped from the open list. Here, a

    State

is created by calling

    State s = state_registry.lookup_state(id);

Inside

    StateRegistry::lookup_state

, we look up the packed buffer and ask the task proxy to create a state
for it

    const [[PackedStateBin]] *buffer = state_data_pool[id.value];
    return task_proxy.create_state(this, id, buffer);

The function

    TaskProxy::create_state

calls the constructor of

    State

that just stores all relevant information (task, registry, ID, buffer,
and a

    state_packer

to access the packed buffer). All of these are light-weight assignments,
no unpacking or initialization of heavy objects is done. The unpacked
data is initialized to an empty vector (variant 1) or a null pointer
(variant 2). Variant 1 needs a dynamic allocation here because all state
data is behind a shared pointer, while variant 2 that only uses a share
pointer for the unpacked data does not (the shared pointer is
initialized to

    nullptr

). The code in the main branch returns a

    GlobalState

here which behaves similar to variant 2 but doesn\'t have the null
pointer to unpacked data.

Back in

    EagerSearch::step

, we now have the created state and use it to get a search node:

    node.emplace(search_space.get_node(s));

This internally copies the state into the search node. As our states are
light-weight, this only means that we have to copy some (shared)
pointers. The exact number is different for variant 1 (1 pointer + 1
shared pointer) and variant 2 (4 pointers, 2 integers, 1 shared
pointer).

### Lazy Evaluators and Statistics {#lazy_evaluators_and_statistics}

The search next creates an

    EvaluationContext

that also internally stores a copy of the state. If a lazy evaluator (a
heuristic where the value can change between the time a state is
inserted in the open list and the time it is expanded) is used, this
evaluation context is then used to check for dead ends. This will first
access the

    heuristic_cache

(a

    PerStateInformation

) using the state. Access only requires the registry and the ID of the
state and does not access the state\'s values. Through the check

    OpenList::is_dead_end

this can also lead to an evaluation of the heuristic (see below). Note
that this evaluates the state that is expanded, not the successors (that
happens later). While this is only necessary with a lazy evaluator, the

    EvaluationContext

for it is actually created in any case. This is because it is used in

    update_f_value_statistics

to print lines such as

    [t=0.0486119s, 46128 KB] f = 12, 23878 evaluated, 14354 expanded

This additional evaluation would not be necessary if we don\'t care
about the statistics line and the part of the code is marked as a hack
but because heuristic values are cached, the overhead is not terrible.

### Applicable and Preferred Operators {#applicable_and_preferred_operators}

Backtracking to

    EagerSearch::step

, the search keeps popping states from the open list until a
non-dead-end is found. For this, the search then gets the state from the
search node (a copy in the main branch but a const reference in the
issue to avoid reference-counting the shared pointers). This state is
then used to ask for applicable operators. The successor generator
classes access the state to compute applicable operators. So far, there
is no explicit unpacking of the state here, so unless the state was
unpacked by a lazy evaluator above, the successor generator works on the
packed data. If the lazy evaluator did unpack the state, this is shared
with the state in the search node because we used references instead of
copying (with a copy, we would benefit from the copy in variant 1 but
not in variant 2).

Next up are the pruning methods that are called with a const reference
of the state. They are not used in the config we are looking at but they
get the state as a const reference, so the same comment about sharing
the unpacked data applies here (the values could be unpacked or packed
depending on the lazy evaluator).

We now create another

    EvaluationContext

for the state in the search to check for preferred operators. This will
evaluate the heuristic again but this time the value hopefully comes
from the heuristic cache within the heuristic (it cannot come from the
cache in the evaluation context because the context is new). If the
heuristic value is cached, the state does not have to be converted along
the task transformation and we only need a lookup in a

    PerStateInformation

.

### Generating Successor States {#generating_successor_states}

Once this is done, the search loops over the applicable operators to
generate the successors.

    State succ_state = state_registry.get_successor_state(s, op);

The method

    StateRegistry::get_successor_state

may unpack the data but it also uses the packed data. To avoid an
unnecessary copy of the packed data we create the successor state
directly in the place where it will eventually live

    state_data_pool.push_back(predecessor.get_buffer());
    PackedStateBin *buffer = state_data_pool[state_data_pool.size() - 1];

We noticed that evaluating axioms and operator preconditions is faster
on unpacked data and for tasks with axioms this makes it worth unpacking
the state just to have the unpacked state available. So in tasks with
axioms, we unpack, copy out the values as an int vector, evaluate
effects and axioms, and then pack all values again. We can then return a
state that already has unpacked data available by moving the unpacked
data into the newly created state:

        if (task_properties::has_axioms(task_proxy)) {
            predecessor.unpack();
            vector<int> new_values = predecessor.get_values();
            for (EffectProxy effect : op.get_effects()) {
                if (does_fire(effect, predecessor)) {
                    [[FactPair]] effect_pair = effect.get_fact().get_pair();
                    new_values[effect_pair.var] = effect_pair.value;
                }
            }
            axiom_evaluator.evaluate(new_values);
            for (size_t i = 0; i < new_values.size(); ++i) {
                state_packer.set(buffer, i, new_values[i]);
            }
            StateID id = insert_id_or_pop_state();
            return task_proxy.create_state(this, id, buffer, move(new_values));
        }

In tasks without axioms this is usually not worth the additional dynamic
allocation and the overhead of copying the data in and out of the packed
representation. In such tasks, the successor state is built directly on
the packed representation. The resulting state does not have unpacked
data available and will create this only when needed.

    ... else {
            for (EffectProxy effect : op.get_effects()) {
                if (does_fire(effect, predecessor)) {
                    [[FactPair]] effect_pair = effect.get_fact().get_pair();
                    state_packer.set(buffer, effect_pair.var, effect_pair.value);
                }
            }
            StateID id = insert_id_or_pop_state();
            return task_proxy.create_state(this, id, buffer);
        }
    }

### Evaluating Successor States {#evaluating_successor_states}

Back in the search, we create another search node and evaluation context
for the successor which again implies copies of the state. At this point
we notify heuristics about the transition from the parent state to the
successor but LM-cut doesn\'t use this information. The only heuristic
that does (LM-count) uses the state only to access a per-state
information.

We then insert the successor state in the open list. A\* uses a
tie-breaking open list, so inserting a state is done in

    TieBreakingOpenList<Entry>::do_insertion

. This will ask the evaluation context to get the heuristic value (

    EvaluationContext::get_evaluator_value_or_infinity

) which calls

    EvaluationContext::get_result

.

### Heuristic Evaluation {#heuristic_evaluation}

The first time

    EvaluationContext::get_result

is called for each evaluation context, the value will not be cached and
we have to ask the evaluator to compute it (

    Evaluator::compute_result

). This uses the evaluation context to evaluate the heuristic. In A\*
with LM-cut, this goes through different evaluators (

    GEvaluator

for the g value,

    CombiningEvaluator

for g+h) but it eventually ends up in the base class implementation

    Heuristic::compute_result

. This method will take the state from the evaluation context as a const
reference. It will then check the evaluation cache inside the heuristic
and (if the value is not found there) call

    LandmarkCutHeuristic::compute_heuristic

.

The LM-cut heuristic then creates a local copy of the state and uses the
task transformation on it:

    State state = convert_ancestor_state(ancestor_state);

This will unpack the state, copy out its values as a

    vector<int>

, then allow the task transformation to modify the vector and create a
new state from the modified data. This new state is then not packed and
only contains the unpacked data.

    ancestor_state.unpack();
    std::vector<int> state_values = ancestor_state.get_values();
    task->convert_state_values(state_values, ancestor_task_proxy.task);
    return create_state(std::move(state_values));

The state is a local variable in

    LandmarkCutHeuristic::compute_heuristic

but it is passed by value to

    LandmarkCutLandmarks::compute_landmarks

(this should be a const reference). After the heuristic computation, the
local state (for the task of LM-cut) is destroyed but the state passed
to

    LandmarkCutHeuristic::compute_heuristic

(for the task of the search) remains unpacked, i.e., it has both packed
and unpacked data available. Since

    Heuristic::compute_result

uses a const reference instead of a copy, this is the state in the
evaluation context.
