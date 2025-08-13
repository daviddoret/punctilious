from __future__ import annotations
import itertools
import typing
import collections
import functools
import math
from functools import lru_cache

# punctilious libraries
import punctilious.util as util
import punctilious.binary_relation_library as brl
import punctilious.natural_number_0_library as nn0l
import punctilious.prime_number_library as pnl
import punctilious.ternary_boolean_library as tbl
import punctilious.special_values_library as spl
import punctilious.cantor_pairing_library as cpl


# Relation orders

class LexicographicOrder(brl.BinaryRelation):
    r"""The lexicographic order of (0-based) natural numbers.

    Mathematical definition
    -------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_m)` and :math:`T = (t_0, t_1, \ldots, t_n)`
    be two finite sequences of (1-based) natural numbers with :math:`s_i, t_j \in \mathbb{N}^+`.

    We say that :math:`S \prec T` under lexicographic-order if and only if:

    :math:`\exists k \leq \min(m,n)` such that :math:`s_i = t_i` for all :math:`i < k` and :math:`s_k < t_k`

    or:

    :math:`m < n` and :math:`s_i = t_i` for all :math:`i = 1, \ldots, m`

    Quotes
    -------

    "(Lexicographic order.) Let S be well-ordered by ≺, and for n > 0 let Tn
    be the set of all n-tuples (x1, x2, ..., xn) of elements xj in S.
    Define (x1, x2, ..., xn) ≺ (y1, y2, ..., yn) if there is some k, 1 ≤ k ≤ n,
    such that xj = yj for 1 ≤ j < k, but xk ≺ yk in S." [Knuth 1997, p. 20]

    "Here the relation (an, ..., a1) < (bn, ..., b1) denotes lexicographic ordering from left to right;
    that is, there is an index j such that ak = bk for n ≥ k > j, but aj < bj." [Knuth 1998, p. 6]

    Bibliography
    --------------

    - Knuth, Donald Ervin. The Art of Computer Programming - Volume 1 - Fundamental Algorithms - Third Edition. 1997.
    - Knuth, Donald Ervin. The Art of Computer Programming - Volume 3 - Sorting and Searching - Second Edition. 1998.


    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        There is no bijection between the lexicographic order of sequences and the natural numbers.

        The sequence of sequences (0),(1),(2),... is infinite.
        The sequence of sequences (0,0),(0,1),(0,2),... is infinite.
        The sequence of sequences (1,0),(1,1),(1,2),... is infinite.

        More generally, take any sequence S. There exists an infinite ascending sequence
        which consists in incrementing its last element infinitely.


        """
        return tbl.TernaryBoolean.FALSE

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        if x.is_equal_to(y):
            return False
        else:
            minimum_length: int = min(x.length, y.length)
            i: int
            for i in range(minimum_length):
                if x[i] < y[i]:
                    return True
                elif x[i] > y[i]:
                    return False
            # All compared elements are equal.
            if len(x) < len(y):
                # Shorter sequence is less
                return True
            else:
                return False


class LengthFirstLexicographicSecondOrder(brl.BinaryRelation):
    r"""The length-first-lexicographic-second order of (0-based) natural numbers.

    Mathematical definition
    -------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_m)` and :math:`T = (t_0, t_1, \ldots, t_n)`
    be two finite sequences of (1-based) natural numbers with :math:`s_i, t_j \in \mathbb{N}^+`.

    We say that :math:`S \prec T` under sum-lexicographic-order if and only if:

    :math:`|{S}| < |{T}|`

    or:

    :math:`|{S}| = |{T}| \land \exists k \leq \min(m,n)` such that :math:`s_i = t_i` for all :math:`i < k` and :math:`s_k < t_k`

    or:

    :math:`|{S}| = |{T}| \land m < n` and :math:`s_i = t_i` for all :math:`i = 1, \ldots, m`

    Note
    ------

    In the context of labeled rooted plane trees,
    "length-first" orders may look better suited to design orders of labeled rooted plane trees,
    because labeled rooted plane trees require the linkage of two orders:

    - rooted plane trees,
    - sequences of (0-based) natural numbers.

    In effect, for a labeled rooted plane tree to be well-formed,
    the size of the rooted plane trees must be equal
    to the length of the (0-based) natural number sequence.

    But the problem with length-first orders is that they are not well-founded,
    as by definition they have infinite chains, such as:
    (0),(1),(2),(3),...

    In effect, as there are countably infinite sequences of size n,
    length-first orders cannot be well-founded.

    See also
    ----------

    - :class:`LexicographicOrder`


    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @classmethod
    def rank(cls, x: object) -> int | typing.Literal[spl.SpecialValues.NOT_AVAILABLE]:
        # TODO: IMPLEMENT THIS
        pass

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        if x.is_equal_to(y):
            return False
        elif x.length < y.length:
            return True
        elif y.length < x.length:
            return False
        else:
            minimum_length: int = min(x.length, y.length)
            i: int
            for i in range(minimum_length):
                if x[i] < y[i]:
                    return True
                elif x[i] > y[i]:
                    return False
            # All compared elements are equal.
            if len(x) < len(y):
                # Shorter sequence is less
                return True
            else:
                return False

    @classmethod
    def unrank(cls, n: int) -> object:
        pass
    # TODO: IMPLEMENT THIS


class SumFirstLexicographicSecondOrder(brl.BinaryRelation):
    r"""The sum-first-lexicographic-second order of (0-based) natural numbers.

    Mathematical definition
    -------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_m)` and :math:`T = (t_0, t_1, \ldots, t_n)`
    be two finite sequences of (1-based) natural numbers with :math:`s_i, t_j \in \mathbb{N}^+`.

    We say that :math:`S \prec T` under sum-lexicographic-order if and only if:

    :math:`\sum{S} < \sum{T}`

    or:

    :math:`\sum{S} = \sum{T} \land \exists k \leq \min(m,n)` such that :math:`s_i = t_i` for all :math:`i < k` and :math:`s_k < t_k`

    or:

    :math:`\sum{S} = \sum{T} \land m < n` and :math:`s_i = t_i` for all :math:`i = 1, \ldots, m`

    See also
    ----------

    - :class:`LexicographicOrder`


    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Observe that (1), (0,1), (0,0,1), (0,0,0,1), ... is an infinite sequence of sequences of sum 1.

        More generally, take any non empty sequence S. There are infinite sequences of sum |S| created by inserting 0 elements between its elements.

        """
        return tbl.TernaryBoolean.FALSE

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        if x.is_equal_to(y):
            return False
        elif sum(x) < sum(y):
            return True
        elif sum(y) < sum(x):
            return False
        else:
            minimum_length: int = min(x.length, y.length)
            i: int
            for i in range(minimum_length):
                if x[i] < y[i]:
                    return True
                elif x[i] > y[i]:
                    return False
            # All compared elements are equal.
            if len(x) < len(y):
                # Shorter sequence is less
                return True
            else:
                return False


class AdjustedSumFirstLengthSecondLexicographicThirdOrder(brl.BinaryRelation):
    r"""The adjusted sum-first, length-second, lexicographic-third order of (0-based) natural numbers.

    Mathematical definition
    -------------------------

    TODO: REWRITE COMPLETELY

    Let :math:`S = (s_0, s_1, \ldots, s_m)` and :math:`T = (t_0, t_1, \ldots, t_n)`
    be two finite sequences of (0-based) natural numbers with :math:`s_i, t_j \in \mathbb{N}^+`.

    First we adjust S and T by incrementing all their elements by 1.
    This adjustment solves the problem of having infinitely many sequences with the same sum,
    such as (1),(0,1),(0,0,1),(0,0,0,1),...

    So we pose:
    :math:`S\prime = S + 1 = (s_0 + 1, s_1 + 1, ..., s_n + 1)`
    :math:`T\prime = T + 1 = (t_0 + 1, t_1 + 1, ..., t_n + 1)`

    We say that :math:`S \prec T` under adjusted-sum-lexicographic-order if and only if:

    :math:`\sum{S\prime} < \sum{T\prime}`

    or:

    :math:`\sum{S\prime} = \sum{T\prime} \land \exists k \leq \min(m,n)` such that :math:`s_i = t_i` for all :math:`i < k` and :math:`s_k < t_k`

    or:

    :math:`\sum{S\prime} = \sum{T\prime} \land m < n` and :math:`s_i = t_i` for all :math:`i = 1, \ldots, m`

    Note
    -------

    This order has immense advantages:

    - it grows slowly (given the Punctilious use case),
    - it allows very length sequences with small numbers of natural numbers,
    - both its ranking, unranking, and successor algorithms are efficient.

    For these reasons, it is elected as the canonical (i.e. default) order.

    See also
    ----------

    - :class:`SumFirstLexicographicSecondOrder`
    - :class:`LexicographicOrder`

    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        TODO: Provide proof here

        """
        return tbl.TernaryBoolean.TRUE

    @util.readonly_class_property
    def least_element(cls) -> NaturalNumber0Sequence:
        r"""Returns the least element of this order.

        The least element of the adjusted-sum-first, length-second, lexicographic-last order
        is the empty sequence: :math:`()`.

        :return:
        """
        return NaturalNumber0Sequence()

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)

        # first criteria: sum
        if cls.get_adjusted_sum(x) < cls.get_adjusted_sum(y):
            return True
        elif cls.get_adjusted_sum(y) < cls.get_adjusted_sum(x):
            return False
        else:
            # adjusted sums are equal.
            # second criteria: length
            if x.length < y.length:
                return True
            elif y.length < x.length:
                return False
            else:

                # third and final criteria: lexicographic order
                # both the sums and lengths of x and y are equal.
                i: int
                for i in range(x.length):
                    if x[i] > y[i]:
                        return True
                    elif x[i] < y[i]:
                        return False

                # x and y are necessarily equal
                return False

    @classmethod
    def rank(cls, x: FlexibleNaturalNumber0Sequence) -> int:
        r"""Returns the rank of sequence `s` under adjusted-sum-first-length-second-lexicographic-last order.


        Sample
        -------

        Let x = (2,4,3,1).

        We need to compute the cumulative sum of the following combinations:

        - all sequences of adjusted sum < 14
        - all sequences of adjusted sum = 14 and prefix:
          - (0, *)
          - (1, *)
          - (2, 0, *)
          - (2, 1, *)
          - (2, 2, *)
          - (2, 3, *)
          - (2, 4, 0, *)
          - (2, 4, 1, *)
          - (2, 4, 2, *)
          - (2, 4, 3, 0)
        - + 1 (the current sequence)

        """
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        adjusted_sum: int = cls.get_adjusted_sum(x)

        # special case: the empty sequence
        if x == cls.least_element:
            return 0

        cumulative_rank: int = 0

        # sum the cardinalities of all adjusted sum classes
        # that have strictly smaller adjusted sum than x.
        # note that:
        # 1) the intersection of these classes is the empty set,
        # 2) by the definition of this order, all sequences in these classes are less than x.
        for s in range(0, adjusted_sum):
            cumulative_rank += cls.get_adjusted_sum_class_rank_cardinality(s)

        # sum the cardinalities of all adjusted sum classes and length
        # that have equal adjusted sum to x,
        # and smaller length than x.
        # note that:
        # 1) the intersection of these classes is the empty set,
        # 2) all classes processed in the precedent step are less than all sequences in these classes,
        # 3) by the definition of this order, all sequences in these classes are less than x.
        for l in range(1, x.length):
            cumulative_rank += cls.get_adjusted_sum_and_length_class_rank_cardinality(adjusted_sum, l)

        # we are now left with the "adjusted sum and length" class of which x is an element.
        # we need to count the number of sequences that are less than x within this class.
        # the only transformation that is allowed to stay within this is class is to
        # keep the length of the sequence equal,
        # and change the values of the sequence elements in such a way as to keep the adjusted sum equal.
        # the first sequence of the class is:
        # (s0 => 0, 0, 0, 0, ..., 0) with adjusted sum = |S| + s0 - 1
        # the last sequence of the class is:
        # (0, 0, 0, 0, ..., sn) with adjusted sum = |S| + sn - 1
        #
        # a naive an inefficient implementation is to loop through sequences
        # from the first of the class to x.
        # of course, this is very inefficient for large sequences.
        current_sequence: tuple[int, ...] = (adjusted_sum - x.length,) + (0,) * (x.length - 1)
        while not current_sequence == x:
            current_sequence = cls.successor(current_sequence)
            cumulative_rank += 1

        # the number of sequences between the first sequence of the class and x may be very large.
        # so
        return cumulative_rank

    @classmethod
    def successor(cls, x: FlexibleNaturalNumber0Sequence) -> NaturalNumber0Sequence:
        r"""Returns the successor of sequence `x`
        given the "adjusted sum first, length second, lexigraphic last" order relation.

        :param x: A (0-based) natural number sequence.
        :return: A (0-based) natural number sequence.
        """
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)

        if x == cls.least_element:
            # the successor of the empty sequence is (0).
            return NaturalNumber0Sequence(0, )

        # Try to find a successor within the adjusted sum and length class.
        # Loop from the before-last element to the first.
        if x.length > 1:  # A minimum of two elements are needed to push values to the right withing equal length class.
            index: int
            for index in range(x.length - 2, -1, -1):
                value: int = x[index]
                if value > 0:
                    # Move one unit from position i to position i+1,
                    # and pack the entire tail sum to i+1 to keep the result as large
                    # as possible under the new prefix (i.e., immediate next in reverse-lex order).
                    tail_sum = 1 + sum(x[index + 1:])  # the 1 we moved plus existing tail
                    out = list(x)
                    out[index] -= 1
                    out[index + 1] = tail_sum
                    for j in range(index + 2, x.length):
                        out[j] = 0
                    return NaturalNumber0Sequence(*out)

        # A solution could not be found within this adjusted sum and length class.
        # I.e.: the sequence is of the form: (0, 0, 0, ..., s_n >= 0).

        # Try to find a successor within the adjusted sum class.
        # Loop from the last element to the first.
        last_value: int = x[-1]
        if last_value > 0:
            # The sequence is of the form (0, 0, 0, ..., s_n > 0).
            first_value = last_value - 1  # Decrement the last element of the sequence and position it at the beginning.
            suffix: tuple[int, ...] = (0,) * x.length
            s: tuple[int, ...] = (first_value,) + suffix
            s: NaturalNumber0Sequence = NaturalNumber0Sequence(*s)
            return s

        # A solution could not be found within this adjusted sum class.
        # I.e.: the sequence is of the form: (0, 0, 0, ..., 0).

        # Find the successor in the next adjusted sum class
        new_adjusted_sum: int = cls.get_adjusted_sum(x) + 1
        s: tuple[int, ...] = (new_adjusted_sum - 1,)
        s: NaturalNumber0Sequence = NaturalNumber0Sequence(*s)
        return s

    @classmethod
    def unrank(cls, n: int) -> NaturalNumber0Sequence:
        n: int = int(n)

        # special case
        if n == 0:
            # the empty sequence
            return cls.least_element

        # find the adjusted sum class
        adjusted_sum_class: int = 0
        loop: bool = True
        while loop:
            cumulative_cardinality: int = cls.get_cumulative_adjusted_sum_class_rank_cardinality(adjusted_sum_class)
            if cumulative_cardinality > n:
                loop = False
            else:
                adjusted_sum_class += 1

        # find the adjusted sum and length class
        length_class: int = 0
        loop: bool = True
        cumulative_cardinality: int = 0
        while loop:
            cumulative_cardinality += cls.get_adjusted_sum_and_length_class_rank_cardinality(adjusted_sum_class,
                                                                                             length_class)
            if cumulative_cardinality > n:
                loop = False
            else:
                length_class += 1

        # declare the first sequence in this adjusted sum and length class
        s: tuple[int, ...] = (adjusted_sum_class - length_class + 1,) + (0,) * (length_class - 1)
        s: NaturalNumber0Sequence(*s)
        loop: bool = True
        while loop:
            if cls.rank(s) == n:
                return s
            else:
                s: NaturalNumber0Sequence = cls.successor(s)

    @classmethod
    def get_adjusted_sum(cls, x: FlexibleNaturalNumber0Sequence) -> int:
        r"""Returns the adjusted sum of sequence `x`.

        The adjusted sum is the sum of the sequence `x\prime` such that
        every element in `x\prime` is equal to the corresponding element
        in `x`, + 1.

        Equivalently, this is the sum of `x` + the length of `x`.

        :param x:
        :return:
        """
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        # Equivalent form:
        # return sum(x.scalar_addition(1))
        return sum(x) + x.length

    @classmethod
    @lru_cache(maxsize=256)
    def get_adjusted_sum_class_rank_cardinality(cls, s: int) -> int:
        r"""Returns the cardinality of the "adjusted sum" class.

        This is the number of combinations of sequences of 0-based natural numbers
        such that their adjusted sum = `s`.

        :param s: the adjusted sum of the sequence.
        :return: the cardinality of the class.
        """
        s: int = int(s)
        if s < 0:
            raise util.PunctiliousException("`s` is less than 0.")
        if s == 0:
            return 1  # the empty sequence
        else:
            return 2 ** (s - 1)

    @classmethod
    @lru_cache(maxsize=256)
    def get_adjusted_sum_and_length_class_rank_cardinality(cls, s: int, l: int) -> int:
        r"""

        From the second stars and bars theorem,
        we know that for any pair of positive integers n and k,
        the number of k-tuples of non-negative integers whose sum is n
        is equal to the number of multisets of size k − 1 taken from a set of size n + 1,
        or equivalently, the number of multisets of size n taken from a set of size k,
        and is given by :math:`()`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)

        :param s:
        :param l:
        :return:
        """
        s: int = int(s)
        l: int = int(l)
        if s == 0 and l == 0:
            return 1  # the empty sequence
        else:
            return util.combination(s - 1, l - 1)

    @classmethod
    @lru_cache(maxsize=256)
    def get_cumulative_adjusted_sum_class_rank_cardinality(cls, s: int) -> int:
        r"""Returns the cumulative cardinality of the "adjusted sum" class,
        union all the precedent classes.

        :param s: the adjusted sum of the sequence.
        :return: the cumulative cardinality of the class.
        """
        s: int = int(s)
        if s < 0:
            raise util.PunctiliousException("s < 0")
        c: int = cls.get_adjusted_sum_class_rank_cardinality(s)
        if s == 0:
            return c
        else:
            return cls.get_cumulative_adjusted_sum_class_rank_cardinality(s - 1) + c


class GodelNumberEncodingOrder(brl.BinaryRelation):
    r"""The Godel-number-encoding relation order of (0-based) natural number sequences.

    Mathematical definition - xRy
    -------------------------------

    Let :math:`x = (s_0, s_1, \ldots, s_n)`
    be a finite sequences with :math:`s_i \in \mathbb{N}^+`.

    Let :math:`y = (t_0, t_1, \ldots, t_n)`
    be a finite sequences with :math:`t_i \in \mathbb{N}^+`.

    :math:`xRy` if and only if :math:`\mathrm{rank}(S) < \mathrm{rank}(T)`

    Mathematical definition - rank()
    ----------------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_n)`
    be a finite sequence with :math:`s_i \in \mathbb{N}^+`.

    Let :math:`p_0, p_1, \ldots, p_n` be the first :math:`n` prime numbers in ascending order.

    :math:`\mathrm{rank}(S) = p_0^{s_0} \cdot p_1^{s_1} \ldots p_n^{s_n}`

    Note
    ------

    The Gödel-number-encoding order has the following disadvantages:

    - it is not bijective with the natural numbers,
    - it grows very fast,
    - unranking requires factorization (but easy in practice because primes are taken in sequence).

    Note
    -----

    :math:`rank((1)) = 2^1 = 2`

    :math:`rank((1,0)) = 2^1 * 3^0 = 2`

    It follows that the Gödel-number-encoding order is not injective.

    It follows that the Gödel-number-encoding order is not bijective.

    It follows that the Gödel-number-encoding order is not isomorphic to (N, <).

    See the :class:`RefinedGodelNumberEncodingOrder` for an improved version of
    the Gödel-number-encoding order that is isomorphic to (N, <).

    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.FALSE

    @util.readonly_class_property
    def least_element(cls) -> NaturalNumber0Sequence:
        """

        The least element is the empty sequence.

        :return:
        """
        return NaturalNumber0Sequence()

    @classmethod
    def rank(cls, x: object) -> int:
        """

        0 should be mapped to the empty sequence ().
        1 should be mapped to sequence (0).

        :param x:
        :return:
        """
        x = NaturalNumber0Sequence.from_any(x)
        if x == cls.least_element:
            return 0
        else:
            n = 1
            p = 1
            for i, f in enumerate(x):
                p = pnl.get_next_prime(p)
                if i == len(x) - 1:
                    # this is the last factor
                    # Increment it to undo the encoding hack for leading zeroes.
                    f += 1
                n = n * p ** f
            return n - 1

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        n: int = cls.rank(x)
        m: int = cls.rank(y)
        return n < m

    @classmethod
    def successor(cls, x: object) -> object:
        n = cls.rank(x)
        n += 1
        y = cls.unrank(n)
        return y

    @classmethod
    def unrank(cls, n: int) -> object:
        n += 1  # Makes the ranks 0-based.
        if n == 1:
            return cls.least_element
        else:
            f = pnl.factorize(n)
            # Decrement the last element by 1.
            # This hack makes leading zeroes meaningful.
            s = util.decrement_last_element(f)
            return NaturalNumber0Sequence(*s)


class RefinedGodelNumberOrder(brl.BinaryRelation):
    r"""The refined Godel-number-encoding order of (0-based) natural number sequences.

    Mathematical definition - xRy
    -------------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_n)`
    be a finite sequences with :math:`s_i \in \mathbb{N}^+`.

    Let :math:`T = (t_0, t_1, \ldots, t_n)`
    be a finite sequences with :math:`t_i \in \mathbb{N}^+`.

    :math:`S < T` if and only if :math:`\mathrm{rank}(S) < \mathrm{rank}(T)`

    Mathematical definition - rank()
    ----------------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_n)`
    be a finite sequence with :math:`s_i \in \mathbb{N}^+`.

    Let :math:`p_0, p_1, \ldots, p_n` be the first :math:`n` prime numbers in ascending order.

    :math:`\mathrm{rank}(S) = p_0^{s_0} \cdot p_1^{s_1} \ldots p_n^{s_n}

    Note
    ------

    The Gödel-number-encoding order has the following disadvantages:

    - it grows much faster than lexicographic order given the use case of
      potentially long sequences with small distinct natural numbers.
    - intuitively, this is because its "space" is full of factors of
      prime numbers that are not effectively used (given the punctilious use case).
    - unranking requires factorization (but not so hard because primes are taken in sequence).

    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @util.readonly_class_property
    def least_element(cls) -> NaturalNumber0Sequence:
        """

        The least element is the empty sequence.

        :return:
        """
        return NaturalNumber0Sequence()

    @classmethod
    def rank(cls, x: object) -> int:
        """

        0 should be mapped to the empty sequence ().
        1 should be mapped to sequence (0).

        :param x:
        :return:
        """
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        if x == cls.least_element:
            return 0
        else:
            n: int = 1
            p: int = 1
            i: int
            exponent: int
            for i, exponent in enumerate(x):
                p = pnl.get_next_prime(p)
                if i == len(x) - 1:
                    # this is the last factor
                    # Increment it to undo the encoding hack for leading zeroes.
                    exponent += 1
                factor: int = p ** exponent
                n = n * factor
            return n - 1

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        n: int = cls.rank(x)
        m: int = cls.rank(y)
        return n < m

    @classmethod
    def successor(cls, x: object) -> object:
        n = cls.rank(x)
        n += 1
        y = cls.unrank(n)
        return y

    @classmethod
    def unrank(cls, n: int) -> object:
        n = int(n)
        n += 1  # Makes the ranks 0-based.
        if n == 1:
            return cls.least_element
        else:
            f: tuple[int, ...] = pnl.factorize(n)
            # Decrement the last element by 1.
            # This hack makes leading zeroes meaningful.
            s = util.decrement_last_element(f)
            return NaturalNumber0Sequence(*s)


class CombinedFixedLengthIntegersWithSentinelOrder(brl.BinaryRelation):
    r"""The combined fixed-length integers with sentinel order of (0-based) natural number sequence.

    See also
    ---------

    - :func:`util.combine_nbit_ints_with_sentinel`.
    - :func:`util.split_nbit_ints_with_sentinel`.

    Note
    ------

    The problem with the Gödel number approach is that it grows extremely fast.
    If we accept as a constraint that (0-based) natural number elements
    in the sequence have a maximal value of 2^n,
    such as 2^32, or 2^64 as is usual on many computer systems,
    then we can combine integer values using fixed-length bit representations.

    To solve the problem of leading zeroes, we can simply append a sentinel value of 1.

    Finally, we define rank(()) = 0.

    Then, this combined fixed-length integers order yields much smaller ranks
    as compared with orders based on the Gödel number approach,
    making them much easier to manipulate by a computer system.

    """

    _max_bits_constraints: int = 32  # The maximal number of bits allowed to represent elements in a (0-based) natural number sequence.

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        A bijection with (N, <) is impossible because many (0-based) natural numbers
        are missing from the ranks. To build on such missing value:
        - take any integer `x` whose lsb binary representation does not have a length of
          (fixed length) * n + 1.
        - note that by construction, all effective ranks have an lsb binary representation
          of length (fixed length) * n + 1 (the + 1 comes from the sentinel value).
        - conclude that `x` is a (0-based) natural number that cannot be mapped
          to a sequence of (0-based) natural numbers.

        For a practical example, take fixed length = 32 and tbe sequence (0).
        Its rank is 4,294,967,296.
        it follows that for all 0 < x < 4294967296, no unranking is possible.

        """
        return tbl.TernaryBoolean.FALSE

    @util.readonly_class_property
    def least_element(cls) -> NaturalNumber0Sequence:
        """

        The least element is the empty sequence.

        :return:
        """
        return NaturalNumber0Sequence()

    @classmethod
    def rank(cls, x: object) -> int:
        """

        0 is mapped to the empty sequence ().
        1 is mapped to sequence (0).

        :param x:
        :return:
        """
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        if x == cls.least_element:
            return 0  # by definition
        else:
            return util.combine_fixed_length_ints_with_sentinel(ints=x, fixed_length=cls._max_bits_constraints)

    @classmethod
    def relates(cls, x: FlexibleNaturalNumber0Sequence, y: FlexibleNaturalNumber0Sequence) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        n: int = cls.rank(x)
        m: int = cls.rank(y)
        return n < m

    @classmethod
    def successor(cls, x: FlexibleNaturalNumber0Sequence) -> NaturalNumber0Sequence:
        """

        Note
        -----

        To get the successor, we cannot use unrank(rank(x) + 1).
        This is because this order is not a bijection with N.
        Instead, we must increment the last element of the sequence,
        or if the last element has maximum value,
        set the last element to 0 and append a new element with value 0
        (leading zeroes are of course accepted).

        :param x:
        :return:
        """
        if x == cls.least_element:
            # this is the empty sequence
            return NaturalNumber0Sequence(0)  # the first non-empty sequence
        else:
            # the sequence is non-empty
            last_element: int = x[-1]
            if last_element == 2 ** cls._max_bits_constraints - 1:
                l = list(x)
                l[-1] = 0
                l.append(0)
                s: NaturalNumber0Sequence = NaturalNumber0Sequence(*l)
                return s
            else:
                l = list(x)
                last_element = last_element + 1
                l[-1] = last_element
                s: NaturalNumber0Sequence = NaturalNumber0Sequence(*l)
                return s

    @classmethod
    def unrank(cls, n: int) -> NaturalNumber0Sequence:
        n = int(n)
        if n == 0:
            return cls.least_element
        else:
            s: tuple[int, ...] = util.split_fixed_length_ints_with_sentinel(n=n, fixed_length=cls._max_bits_constraints)
            s: NaturalNumber0Sequence = NaturalNumber0Sequence(*s)
        return s


class CantorTuplingWithSentinelValue(brl.BinaryRelation):
    r"""The Cantor "tupling" with sentinel value order of (0-based) natural number sequence.

    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        Every pair (n, 0) is mapped to the empty sequence ().

        """
        return tbl.TernaryBoolean.FALSE

    @util.readonly_class_property
    def least_element(cls) -> NaturalNumber0Sequence:
        """

        The least element is the empty sequence.

        :return:
        """
        return NaturalNumber0Sequence()

    @classmethod
    def rank(cls, x: FlexibleNaturalNumber0Sequence) -> int:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        n: int = cpl.cantor_tupling_with_sentinel_value(*x)
        return n

    @classmethod
    def relates(cls, x: FlexibleNaturalNumber0Sequence, y: FlexibleNaturalNumber0Sequence) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        n: int = cls.rank(x)
        m: int = cls.rank(y)
        return n < m

    @classmethod
    def successor(cls, x: FlexibleNaturalNumber0Sequence) -> NaturalNumber0Sequence:
        raise util.PunctiliousException("TO BE DEVELOPED")

    @classmethod
    def unrank(cls, n: int) -> NaturalNumber0Sequence:
        n = int(n)
        s: tuple[int, ...] = cpl.cantor_tupling_with_sentinel_value_inverse(n)
        return NaturalNumber0Sequence(*s)


class IsEqualTo(brl.BinaryRelation):
    r"""The equality binary-relation for 0-based natural numbers.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}_0, = )`.

    """

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        return x.is_natural_number_0_sequence_equivalent_to(y)


# General functions

def concatenate_natural_number_0_sequences(*s: FlexibleNaturalNumber0Sequence) -> NaturalNumber0Sequence:
    """Concatenates a collection of :class:`NaturalNumberSequence` elements, preserving order.

    :param s:
    :return:
    """
    s: tuple[int] = tuple(itertools.chain.from_iterable(
        t for t in s))
    return NaturalNumber0Sequence(*s)


# Classes


class NaturalNumber0Sequence(brl.ClassWithOrder, tuple):
    """A finite (computable) sequence of (0-based) natural numbers.

    Definition:
    An :class:`NaturalNumberSequence` is a finite sequence of natural numbers (n_0, n_1, ..., n_j) such that:
        - n_i >= 0 for 0 <= i <= j

    """

    def __add__(self, s):
        """Concatenates this :class:`NaturalNumberSequence` with another :class:`NaturalNumberSequence` `s`.
        Or performs a scalar addition if s is an integer.

        Note:
            This enables the usage of the python sum function, e.g.: sum(s0, s1, ...).

        :param s:
        :return:
        """
        if isinstance(s, int):
            return self.scalar_addition(n=s)
        elif isinstance(s, typing.Iterable):
            return concatenate_natural_number_0_sequences(self, s)
        else:
            raise util.PunctiliousException("Unsupported type.")

    def __hash__(self):
        return hash((NaturalNumber0Sequence, NaturalNumber0Sequence._HASH_SEED, *self.elements,))

    def __init__(self, *s):
        super(NaturalNumber0Sequence, self).__init__()

    def __new__(cls, *s):
        v: bool
        s: tuple[int] | None
        r: bool
        v, s = cls.data_validate_elements(s, raise_exception_on_validation_failure=True)
        s: tuple[int] = super(NaturalNumber0Sequence, cls).__new__(cls, s)
        s: tuple[int] = cls._from_cache(s)
        return s

    _HASH_SEED: int = 6807878777699371138  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    _cache: dict[
        int, NaturalNumber0Sequence] = dict()  # cache for NaturalNumberSequence.

    @classmethod
    def _compute_hash(cls, o: FlexibleNaturalNumber0Sequence) -> int:
        r"""Exposes the hashing logic as a static method.

        :param o: An object that is structurally compatible with a natural-number-sequence.
        :return: The hash of the natural-number-sequence that is structurally equivalent to `o`.
        """
        return hash((NaturalNumber0Sequence, cls._HASH_SEED, o.elements,))

    @classmethod
    def _from_cache(cls, o: FlexibleNaturalNumber0Sequence):
        r"""Cache mechanism used in the constructor."""
        hash_value: int = NaturalNumber0Sequence._compute_hash(o)
        if hash_value in cls._cache.keys():
            return cls._cache[hash_value]
        else:
            cls._cache[hash_value] = o
            return o

    def concatenate_with(self, x) -> NaturalNumber0Sequence:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        return concatenate_natural_number_0_sequences(self, x, )

    @util.readonly_class_property
    def is_equal_to_relation(self) -> typing.Type[brl.BinaryRelation]:
        return IsEqualTo

    @util.readonly_class_property
    def is_strictly_less_than_relation(self) -> typing.Type[brl.BinaryRelation]:
        # return RefinedGodelNumberOrder
        return AdjustedSumFirstLengthSecondLexicographicThirdOrder

    @util.readonly_class_property
    def least_element(cls) -> NaturalNumber0Sequence:
        return cls.is_strictly_less_than_relation.least_element

    @functools.cached_property
    def restricted_growth_function_sequence(self) -> NaturalNumber0Sequence:
        r"""Converts the natural-number-sequence `s` into a restricted-growth-function-sequence `t`,
        by applying canonical labeling.

        Notation:
        :math:`canonical(S)`

        Definition - Canonical Labeling:
        The canonical-labeling of a natural-numbers-sequence S is an RFG-sequence T such that:
         - the value of the first element of S is mapped to 1
         - whenever a new value x appears in S, it is mapped to max(t0, t1, ..., ti) + 1 where i is the index
           position of x in S

        Examples:
        (3,5,2,1) --> (1,2,3,4)
        (3,5,3,1,5,2) --> (1,2,1,3,2,4)

        :return:
        """
        if self.is_restricted_growth_function_sequence:
            return self
        else:
            mapping: dict[int, int] = dict()
            mapped_value: int = 0
            n: int
            for n in self:
                if n not in mapping.keys():
                    mapping[n] = mapped_value
                    mapped_value += 1
            s: tuple[int, ...] = tuple(mapping[n] for n in self)
            return NaturalNumber0Sequence(*s)

    def concatenate_with(self, *s: FlexibleNaturalNumber0Sequence) -> NaturalNumber0Sequence:
        r"""Concatenates this :class:`NaturalNumberSequence` with :class:`NaturalNumberSequence` `s`,
        or an iterable / generator of multiple :class:`NaturalNumberSequence` elements.

        Notation:
        :math:`S \mathbin{+\!\!+} T`

        Shortcuts:
        s1 + s2
        sum(s1, s2, ..., sn)

        :param s:
        :return:
        """
        return concatenate_natural_number_0_sequences(self, *s)

    @classmethod
    def data_validate_elements(
            cls,
            o: FlexibleNaturalNumber0Sequence, raise_exception_on_validation_failure: bool = True) -> \
            tuple[bool, FlexibleNaturalNumber0Sequence | None]:
        r"""Validates `o` as a collection of (0-based) natural number elements,
        applying implicit conversion as necessary.

        :param o: An object that may be interpreted as a :class:`NaturalNumberSequence`.
        :param raise_exception_on_validation_failure: Raises an exception if data validation fails.
        :return: a tuple (v, s) where v is True if data validation was successful, False otherwise,
            and s is the resulting natural-number sequence, or None if data validation failed.
        """
        if isinstance(o, NaturalNumber0Sequence):
            # data validation is assured by the class logic.
            return True, o
        if isinstance(o, collections.abc.Iterable) or isinstance(o, collections.abc.Generator):
            o: tuple[nn0l.NaturalNumber0, ...] = tuple(nn0l.NaturalNumber0.from_any(n) for n in o)
            return True, o
        if raise_exception_on_validation_failure:
            raise util.PunctiliousException("The type of `o` is not supported.", o_type=type(o), o=o)
        else:
            return False, None

    @property
    def elements(self) -> tuple[int, ...]:
        r"""Returns a tuple of the elements that compose this :class:`NaturalNumberSequence`, preserving order.

        :return: a tuple of the elements that compose this :class:`NaturalNumberSequence`, preserving order.
        """
        return tuple(super().__iter__())

    @classmethod
    def from_any(cls, o: object) -> NaturalNumber0Sequence:
        r"""Declares a natural-number-sequence from a Python object that can be interpreted as a natural-number-sequence.

        Note:
            This method is redundant with the default constructor.

        :param o: a Python object that can be interpreted as a natural-number-sequence.
        :return: a natural-number-sequence.
        """
        if isinstance(o, NaturalNumber0Sequence):
            return o
        if isinstance(o, collections.abc.Iterable):
            return NaturalNumber0Sequence(*o)
        if isinstance(o, collections.abc.Generator):
            return NaturalNumber0Sequence(*o)
        raise util.PunctiliousException('NaturalNumberSequence data validation failure', o=o)

    @property
    def im(self) -> tuple[int, ...]:
        r"""A shortcut for :attr:`NaturalNumberSequence.image`."""
        return self.image

    @functools.cached_property
    def image(self) -> tuple[int, ...]:
        r"""The :attr:`NaturalNumberSequence.image` is the set of values contained in the sequence,
        returned as a tuple of ascending and unique values.

        Notation:
        :math:`Im(S)`

        Note: a Python tuple is returned instead of a Python set. This is a design choice
            to force working with immutable objects.

        Note: the values are returned in ascending order.

        Shortcut: :attr:`NaturalNumberSequence.im`

        Definition:
            S := { s_0, s_1, ..., s_n }
            Im(S) := { s_i | 0 <= i <= n }

        :return: an ordered tuple of integers.
        """
        s: set[int] = set()
        for n in self.elements:
            s.add(n)
        s: tuple[int, ...] = tuple(s)
        s: tuple[int, ...] = tuple(sorted(s))
        return s

    @functools.cached_property
    def image_cardinality(self) -> int:
        r"""The :attr:`NaturalNumberSequence.image_cardinality` is the cardinality
         of the :attr:`NaturalNumberSequence.image`, i.e. the number of distinct values it contains.

        Notation:
        :math:`|Im(S)|`

        :return:
        """
        return len(self.image)

    def is_restricted_growth_function_equivalent_to(self, s) -> bool:
        r"""`True` if this natural number sequence canonical-natural-number-sequence-equivalent
        to the natural-number-sequence `s`, `False` otherwise.

        Notation:
        :math:`S ~_{canonical} T`

        Formal Definition:
        Two natural-number-sequences `s` and `t` are canonical-natural-number-sequence-equivalent
        if and only if their canonical-natural-number-sequence are natural-number-sequence-equivalent.

        """
        s: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(s)
        return self.restricted_growth_function_sequence.is_natural_number_0_sequence_equivalent_to(s)

    @functools.cached_property
    def is_increasing(self) -> bool:
        r"""Returns `True` if this sequence is increasing, `False` otherwise.

        Definition - Increasing sequence:
        A sequence :math:`S = (n_0, n1, \cdots, n_l)` is increasing
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, n_{i + 1} \ge n_i`.

        References:
         - Adams, Malcolm R. “An Introduction to Mathematical Analysis,” 2007.

        :return: `True` if this sequence is increasing, `False` otherwise.
        """
        return all(self.elements[i + 1] >= self.elements[i] for i in range(0, self.length - 1))

    @functools.cached_property
    def is_natural_number_sequence(self) -> bool:
        r"""

        Notation:
        :math:`\mathbb{N}\text{-sequence}(S)

        :return:
        """
        return True

    def is_natural_number_0_sequence_equivalent_to(self, s: FlexibleNaturalNumber0Sequence):
        r"""

        Notation:
        :math:`S ~_{\mathbb{N}\text{-sequence}} T`

        Formal definition:
        Two natural numbers-sequences s and t are natural-numbers-sequence-equivalent if and only if:
         - length(s) = length(t)
         - s_i = t_i for 0 <= i < length(s)

        :param s:
        :return:
        """
        s: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(s)
        return self.length == s.length and all(x == y for x, y in zip(self, s))

    @functools.cached_property
    def is_restricted_growth_function_sequence(self) -> bool:
        """`True` if this natural numbers sequence is also an RGF sequence, `False` otherwise.

        Formal Definition:
        A restricted-growth-function-sequence is a finite (computable) sequence
        of natural numbers (n_0, n_1, ..., n_i) such that:
            - n_0 = 1
            - n_j <= 1 + max(n_0, n_1, ..., n_(j-1)) for 0 < j <= i

        Synonyms:
         - RGFS
         - RGF sequence

        Note:
        Often RGF sequences have an initial value of 1 in the literature. We choose 0 here for consistency
        with the design choice of using 0-based indexes as the default indexing method in Python.

        """
        for i, n in enumerate(self):
            if i == 0 and n >= 1:
                return False
            if i > 0 and n > max(self.elements[0:i]) + 1:
                return False
        return True

    @functools.cached_property
    def is_strictly_increasing(self) -> bool:
        r"""Returns `True` if this sequence is strictly increasing, `False` otherwise.

        Definition - Strictly increasing sequence:
        A sequence :math:`S = (n_0, n1, \cdots, n_l)` is strictly increasing
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, n_{i + 1} > n_i`.

        References:
         - Adams, Malcolm R. “An Introduction to Mathematical Analysis,” 2007.

        :return: `True` if this sequence is strictly increasing, `False` otherwise.
        """
        return all(self.elements[i + 1] > self.elements[i] for i in range(0, self.length - 1))

    @functools.cached_property
    def length(self) -> int:
        """The `length` of a finite sequence is the number of elements in the sequence.

        Notation:
        :math:`|S|`

        """
        return len(self)

    @functools.cached_property
    def max_value(self) -> int:
        """The `max_value` of a `NaturalNumberSequence` is the maximum value of its elements.

        Notation:
        :math:`max(S)`

        """
        return max(self)

    def scalar_addition(self, n: int):
        r"""Returns the scalar addition of this sequence :math:`S` with `n`.

        Given a sequence` :math:`S`,
        and a natural number :math:`n`,
        returns a new sequence :math:`T` defined as
        :math:`(t_0 + n, t_1 + n, \cdots, t_i + n)`.

        :param n:
        :return:
        """
        n: int = int(n)
        t: tuple[int, ...] = tuple(x + n for x in self.elements)
        return NaturalNumber0Sequence(*t)

    @functools.cached_property
    def sum(self) -> int:
        return sum(x for x in self.elements)


# Flexible types to facilitate data validation

FlexibleNaturalNumber0Sequence = typing.Union[
    NaturalNumber0Sequence, tuple[int, ...], collections.abc.Iterator, collections.abc.Generator, None]

# Aliases and well-known objects

NN0S = NaturalNumber0Sequence  # An alias for NaturalNumberSequence
trivial_sequence = NaturalNumber0Sequence()  # An alias for the empty sequence ().
empty_sequence = NaturalNumber0Sequence()  # The empty sequence ().
is_equal_to = IsEqualTo  # The is-equal-to binary relation.
refined_godel_number_order = RefinedGodelNumberOrder
lexicographic_order = LexicographicOrder
length_first_lexicographic_second_order = LengthFirstLexicographicSecondOrder
sum_first_lexicographic_second_order = SumFirstLexicographicSecondOrder
godel_number_order = GodelNumberEncodingOrder
combined_fixed_length_integers_with_sentinel_order = CombinedFixedLengthIntegersWithSentinelOrder
