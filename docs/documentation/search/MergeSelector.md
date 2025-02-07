

This page describes the available merge selectors. They are used to compute the next merge purely based on the state of the given factored transition system. They are used in the merge strategy of type 'stateless', but they can also easily be used in different 'combined' merged strategies.

## Score based filtering merge selector 

This merge selector has a list of scoring functions, which are used iteratively to compute scores for merge candidates, keeping the best ones (with minimal scores) until only one is left.

    score_based_filtering(scoring_functions)

* *scoring_functions* (list of [MergeScoringFunction](MergeScoringFunction.md)): The list of scoring functions used to compute scores for candidates.
