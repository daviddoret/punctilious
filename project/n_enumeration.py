# import itertools
import math
import typing


def convert_powerset_element_to_string(s: frozenset[int]) -> str:
    """Convert an element s of the powerset of the natural numbers to a friendly looking string of the form: "{n1,
    n2, ... nm}".

    Note: the usage of the sorted function below is not strictly necessary because set elements are pre-ordered."""
    return '{' + ', '.join(map(str, sorted(s))) + '}'


def yield_finite_powerset_sub_element(i: int, n: int) -> typing.Generator[int, None, None]:
    """Yield the i-th element of the powerset of the set whose elements are the natural numbers ranging from 0 to n."""
    for j in range(0, n + 1):
        # Check if the j-th bit is set
        # in the binary representation of that natural number.
        if (i & (1 << j)) > 0:
            # The j-th bit was set,
            # it follows that j is the i-th element of the powerset.
            yield j


def yield_finite_powerset(n: int) -> typing.Generator[frozenset, None, None]:
    """Yield all the elements of the powerset of the set whose elements are the natural numbers ranging from 0 to n.

    Note: the order of the yielded elements is critical to the enumeration of the powerset of n."""
    powerset_cardinality: int = int(math.pow(2, n))
    i: int = 0

    # Loop through all natural numbers ranging from 0
    # to the cardinality of the powerset, non-inclusive.
    for i in range(0, powerset_cardinality):
        # The usage of frozensets is ideal because they
        # are... frozen and thus hashable.
        yield frozenset(yield_finite_powerset_sub_element(i=i, n=n))


print(list(yield_finite_powerset(n=0)))
print(list(yield_finite_powerset(n=1)))
print(list(yield_finite_powerset(n=2)))
print(list(yield_finite_powerset(n=3)))


# p3 = yield_finite_powerset(n=8)
# print(list(p3))

# Source of inspiration:
# https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
# https://www.geeksforgeeks.org/power-set/


def yield_powerset_of_n() -> typing.Generator[frozenset, None, None]:
    """Enumerate all elements of the powerset of the natural numbers."""
    n: int = 0  # A counter for the finite powersets.
    unique_index = set()  # A unique index to avoid re-yielding elements from the previous finite powersets.
    while True:
        # yield from yield_finite_powerset(n=n)
        for s in yield_finite_powerset(n=n):
            # Check if s has already been enumerated as part of a previous powerset.
            if s not in unique_index:
                # s was not enumerated so far, we may append it to the unique index and yield it.
                unique_index.add(s)
                yield s
        n = n + 1


def yield_powerset_of_n_with_mapping() -> typing.Generator[typing.Tuple[int, frozenset], None, None]:
    """Enumerate all elements of the powerset of the natural numbers,
    and explicitly yield the pairs (n, s) where n is the mapping in the natural numbers,
    and s is the element of the powerset."""
    i: int = 1  # A counter for the elements of the powerset.
    for s in yield_powerset_of_n():
        yield i, s
        i = i + 1


def yield_powerset_of_n_with_mapping_and_boundary(n: int) -> typing.Generator[typing.Tuple[int, frozenset], None, None]:
    """Enumerate all elements of the powerset of the natural numbers up to n-th element (inclusive)."""
    for i, s in yield_powerset_of_n_with_mapping():
        if i > n:
            return
        else:
            yield i, s


def print_powerset_of_n_with_mapping_and_boundary(n: int):
    for i, s in yield_powerset_of_n_with_mapping_and_boundary(n=n):
        print(f'{i} --> {convert_powerset_element_to_string(s=s)}')


print_powerset_of_n_with_mapping_and_boundary(n=17)


def get_powerset_of_n_enumeration_with_boundary(n: int):
    """A shortcut function to get a dictionary (mapping) of the n-th first consecutive natural numbers,
    with the n-th first elements of the powerset of N."""
    return {i: s for i, s in yield_powerset_of_n_with_mapping_and_boundary(n=n)}


print(get_powerset_of_n_enumeration_with_boundary(n=3))
