def generate_sequences(n):
    if n == 1:
        yield (1,)
    else:
        for first_number in range(n + 1, 0, -1):
            if first_number == n:
                yield (first_number,)
            else:
                for s in generate_sequences(n - first_number):
                    yield (first_number,) + s


def get_tree(x):
    """Recursively append an empty tuple to every tuple in the structure."""
    if not isinstance(x, tuple):
        return x  # Base case: not a tuple, return as is

    # Recursively process each element
    processed_elements = tuple(append_empty_tuple_recursively(e) for e in x)

    # Return a new tuple with the empty tuple appended
    return processed_elements + ((),)


x1 = append_empty_tuple_recursively(tuple())
print(x1)
x2 = append_empty_tuple_recursively(x1)
print(x2)
