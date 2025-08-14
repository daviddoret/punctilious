def sequence_length_at_index(index: int) -> int:
    """
    Return the length of the `index`-th finite sequence (0-based)
    when all finite sequences of nonnegative integers are ordered by:
      1) total weight = (sum of entries + length),
      2) length,
      3) lexicographic order.

    The empty sequence is at index 0 and has length 0.
    """

    if index == 0:
        return 0

    # 1) Determine the weight layer this index falls into.
    # For n >= 1, indices [2^(weight-1), 2^weight - 1] all share the same weight.
    weight = index.bit_length()  # weight = floor(log2(index)) + 1
    choose_param = weight - 1  # We'll use m = weight - 1 in binomial coefficients C(m, k)

    # 2) Position inside the weight layer (0-based)
    start_of_layer = 1 << (weight - 1)  # 2^(weight-1)
    offset_in_layer = index - start_of_layer

    # 3) Within a fixed weight layer, lengths appear in runs:
    #    length = 1 repeated C(m,0) times, length = 2 repeated C(m,1) times, ..., up to length = weight repeated C(m,m) times.
    #    We walk these runs until the cumulative count exceeds offset_in_layer.
    cumulative_count = 0
    combinations_in_run = 1  # C(m, 0) = 1

    for length in range(1, weight + 1):
        cumulative_count += combinations_in_run
        if offset_in_layer < cumulative_count:
            return length
        # Update C(m, k) -> C(m, k+1) without recomputing from scratch
        combinations_in_run = combinations_in_run * (choose_param - (length - 1)) // length

    # Should never happen
    raise RuntimeError("Index could not be placed in any length run")


l = []
for n in range(128):
    l.append(sequence_length_at_index(n))
l = tuple(l)
print(l)
