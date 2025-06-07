from __future__ import annotations
import typing
import collections
import util


def data_validate_restricted_growth_function_sequence(
        o: FlexibleRestrictedGrowthFunctionSequence) -> RestrictedGrowthFunctionSequence:
    if isinstance(o, RestrictedGrowthFunctionSequence):
        return o
    if isinstance(o, collections.abc.Iterable):
        return RestrictedGrowthFunctionSequence(*o)
    if isinstance(o, collections.abc.Generator):
        return RestrictedGrowthFunctionSequence(*o)
    raise util.PunctiliousException('RestrictedGrowthFunctionSequence data validation failure', o=o)


def data_validate_restricted_growth_function_sequence_elements(
        o: FlexibleRestrictedGrowthFunctionSequence) -> FlexibleRestrictedGrowthFunctionSequence:
    if isinstance(o, RestrictedGrowthFunctionSequence):
        # data validation is assured by the class logic.
        return o
    if isinstance(o, collections.abc.Iterable) or isinstance(o, collections.abc.Generator):
        o = tuple(o)
        o = tuple(int(n) for n in o)
        for i, n in enumerate(o):
            if i > 0 and n > max(o[0:i]) + 1:
                raise util.PunctiliousException('RestrictedGrowthFunctionSequence elements data validation failure',
                                                o=o, i=i, n=n)
        return o
    raise util.PunctiliousException('RestrictedGrowthFunctionSequence elements data validation failure', o=o)


_restricted_growth_function_sequence_cache = dict()  # cache mechanism assuring that unique rpts are only instantiated once.


def retrieve_restricted_growth_function_sequence_from_cache(i: RestrictedGrowthFunctionSequence):
    """cache mechanism assuring that unique rpts are only instantiated once."""
    global _abstract_formula_cache
    if hash(i) in _restricted_growth_function_sequence_cache.keys():
        return _restricted_growth_function_sequence_cache[hash(i)]
    else:
        _restricted_growth_function_sequence_cache[hash(i)] = i
        return i


class RestrictedGrowthFunctionSequence(tuple):
    """

    Definition:
    A `RestrictedGrowthFunctionSequence` is a finite sequence of natural numbers such that:
        - n_1 = 1
        - with i > 1, n_i = 1 + max(n_1, n_2, ..., n_(i-1))
    """

    def __init__(self, *s):
        super(RestrictedGrowthFunctionSequence, self).__init__()

    def __new__(cls, *s):
        s: tuple[int] = data_validate_restricted_growth_function_sequence_elements(s)
        s: tuple[int] = super(RestrictedGrowthFunctionSequence, cls).__new__(cls, s)
        s: tuple[int] = retrieve_restricted_growth_function_sequence_from_cache(s)
        return s

    @property
    def length(self) -> int:
        """The `length` of a finite sequence is the number of elements in the sequence."""
        return len(self)


FlexibleRestrictedGrowthFunctionSequence = typing.Union[
    RestrictedGrowthFunctionSequence, tuple[int], collections.abc.Iterator, collections.abc.Generator, None]
