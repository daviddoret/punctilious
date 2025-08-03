from __future__ import annotations
import functools
import typing
import punctilious.util as util
import punctilious.binary_relation_library as brl
import punctilious.ternary_boolean_library as tbl


# Relation classes


class IsEqualTo(brl.BinaryRelation):
    r"""The equality binary-relation for 0-based natural numbers.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}_0, = )`.

    """

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: DyckWord = DyckWord.from_any(x)
        y: DyckWord = DyckWord.from_any(y)
        return str(x) == str(y)


class LexicographicOrder(brl.BinaryRelation):
    r"""The lexicographic relation order for Dyck words.

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
    def least_element(cls) -> object:
        return DyckWord("()")

    @classmethod
    def rank(cls, x: object) -> int:
        """
        Given a primitive Dyck word s (a well‐formed parenthesis string
        that only returns to balance 0 at the very end), return its 0-based
        rank in the sequence:
          semilength=1: "()"
          semilength=2: "(())"
          semilength=3: "((()))", "(()())"
          semilength=4: "(((())))", "((()()))", "((())())", "(()(()))", "(()()())"
          ...
        within each semilength, listed in lex order with '(' < ')'.
        """
        x: DyckWord = DyckWord.from_any(x)
        L = len(x)
        if L % 2 != 0 or L < 2:
            raise ValueError("input must be a primitive Dyck word of even length ≥2")
        k = L // 2
        # check basic primitive‐Dyck structure
        bal = 0
        for i, ch in enumerate(x):
            if ch == '(':
                bal += 1
            elif ch == ')':
                bal -= 1
            else:
                raise ValueError("invalid character")
            if bal < 0 or (bal == 0 and i != L - 1):
                raise ValueError("not primitive Dyck")
        if bal != 0:
            raise ValueError("not a Dyck word")

        # 1) Compute Catalan numbers C0..C_{k-1}
        catalan = [1]  # C0 = 1
        for i in range(1, k):
            # C_i = C_{i-1} * 2*(2i-1)/(i+1)
            c = catalan[-1] * 2 * (2 * i - 1) // (i + 1)
            catalan.append(c)

        # Number of primitives of semilength j is C_{j-1}, so
        # all primitives of smaller semilengths occupy
        # sum_{j=1..k-1} C_{j-1} = sum_{i=0..k-2} C_i
        prev_count = sum(catalan[0:k - 1])  # = 0 when k=1

        # 2) Extract the inner Dyck word of semilength m = k-1
        m = k - 1
        inner = x[1:-1]  # length = 2m

        # 3) Build DP_rem[r][b] = # of ways to complete a Dyck path
        #    of remaining length r starting from balance b.
        N = 2 * m
        DP_rem = [[0] * (m + 2) for _ in range(N + 1)]
        DP_rem[0][0] = 1
        for length in range(1, N + 1):
            for b in range(m + 1):
                cnt = 0
                # place '(' => balance b+1
                if b + 1 <= m:
                    cnt += DP_rem[length - 1][b + 1]
                # place ')' => balance b-1
                if b > 0:
                    cnt += DP_rem[length - 1][b - 1]
                DP_rem[length][b] = cnt

        # 4) Rank the inner Dyck word in lex order
        r = 0
        bal = 0
        for pos, ch in enumerate(inner):
            rem = N - pos - 1
            # how many completions if we put '(' here?
            cnt_open = DP_rem[rem][bal + 1] if bal + 1 <= m else 0
            if ch == '(':
                bal += 1
            else:  # ch == ')'
                # skip over all the words that start with '(' here
                r += cnt_open
                bal -= 1

        return prev_count + r

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: DyckWord = DyckWord.from_any(x)
        y: DyckWord = DyckWord.from_any(y)
        return cls.rank(x) < cls.rank(y)

    @classmethod
    def successor(cls, x: object) -> object:
        x: DyckWord = DyckWord.from_any(x)
        n: int = cls.rank(x)
        n_prime = n + 1
        y: DyckWord = cls.unrank(n_prime)
        return y

    @classmethod
    def unrank(cls, n: int) -> object:
        """
        Return the n-th primitive Dyck word (0-based) in the ordering:
          semilength = 1,2,3,...
          within each semilength k, lex order of all primitives of size k.

        A Dyck word is primitive if it never returns to zero height except at the very end.

        There are Catalan(k-1) primitives of semilength k, namely "(" + (any Dyck of semilength k-1) + ")".

        Example of the sequence for n=0..8:
          0 -> "()"
          1 -> "(())"
          2 -> "((()))"
          3 -> "(()())"
          4 -> "(((())))"
          5 -> "((()()))"
          6 -> "((())())"
          7 -> "(()(()))"
          8 -> "(()()())"
        """
        if n < 0:
            raise ValueError("n must be non-negative")

        # Step 1: build Catalan numbers C0, C1, C2, ...
        # and their cumulative sums until we exceed n.
        # Primitives of semilength k are counted by C_{k-1}.
        catalan = [1]  # C0 = 1
        cum = [1]  # sum_{i=0..0} C_i = 1
        idx = 0
        while cum[idx] <= n:
            j = idx + 1
            # C_j = C_{j-1} * 2*(2j-1)/(j+1)
            c = catalan[idx] * 2 * (2 * j - 1) // (j + 1)
            catalan.append(c)
            cum.append(cum[idx] + c)
            idx += 1

        # Now cum[idx] > n, so semilength k = idx+1,
        # and within that block our local rank is
        #   r = n - sum_{i=0..idx-1} C_i
        k = idx + 1
        prev_sum = cum[idx - 1] if idx >= 1 else 0
        r = n - prev_sum

        # A primitive of semilength k is "(" + (Dyck of semilength k-1) + ")"
        m = k - 1  # semilength of the inner Dyck word

        # Step 2: unrank the r-th (0-based) Dyck word of semilength m
        # in pure lex order, using a small DP table.
        total_length = 2 * m
        # ways_to_complete_path[len][bal] = # of ways to complete a path of
        # total remaining length len from balance=bal back to 0
        # without ever dipping below 0.
        ways_to_complete_path = [[0] * (m + 2) for _ in range(total_length + 1)]
        ways_to_complete_path[0][0] = 1
        for length in range(1, total_length + 1):
            for balance in range(m + 1):
                cnt = 0
                # place "(" -> bal+1
                if balance + 1 <= m:
                    cnt += ways_to_complete_path[length - 1][balance + 1]
                # place ")" -> bal-1
                if balance > 0:
                    cnt += ways_to_complete_path[length - 1][balance - 1]
                ways_to_complete_path[length][balance] = cnt

        if not (0 <= r < ways_to_complete_path[total_length][0]):
            raise ValueError("internal rank out of range")

        # Now walk the word
        balance = 0
        inner = []
        for pos in range(total_length):
            rem = total_length - pos - 1
            # how many completions if we put "(" here?
            cnt_open = ways_to_complete_path[rem][balance + 1] if balance + 1 <= m else 0
            if r < cnt_open:
                inner.append('(')
                balance += 1
            else:
                r -= cnt_open
                inner.append(')')
                balance -= 1

        raw_string = "(" + "".join(inner) + ")"
        return DyckWord(raw_string)


# Relations

is_equal_to = IsEqualTo  # The canonical equality relation for natural-number-0 elements.
lexicographic_order = LexicographicOrder  # The canonical is-strictly-less-than relation for natural-number-0 elements.


# Functions

def data_validate_dyck_work(s: str) -> bool:
    """
    Check if a given string is a valid Dyck word.

    A Dyck word is a balanced string of parentheses where:
    1. It contains only '(' and ')' characters
    2. It is balanced (equal number of opening and closing parentheses)
    3. It is properly nested (no closing parenthesis appears before its corresponding opening)

    Args:
        s: The input string to validate

    Returns:
        bool: True if the string is a Dyck word, False otherwise
    """
    s = str(s)

    if len(s) == 0:
        raise util.PunctiliousException("The empty string is not recognized as a valid Dyck word.")

    balance = 0

    for char in s:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        else:
            # If any character is not a parenthesis, it's not a Dyck word
            return False

        # If balance ever goes negative, it's not properly nested
        if balance < 0:
            return False

    # The total balance should be zero for a valid Dyck word
    return balance == 0


# Main class

class DyckWord(brl.ClassWithOrder, str):
    r"""A Dyck word.

    Bibliography
    ---------------

    - https://en.wikipedia.org/wiki/Dyck_language
    - https://blogs.ams.org/visualinsight/2015/07/15/dyck-words/

    """

    _HASH_SEED: int = 10160073242389361000  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    def __hash__(self):
        return hash((DyckWord, DyckWord._HASH_SEED, str(self),))

    def __new__(cls, x):
        x = str(x)
        if not data_validate_dyck_work(x):
            raise util.PunctiliousException("`x` cannot be interpreted as a Dyck word.", x=x)
        return super().__new__(cls, x)

    def __str__(self):
        return str.__str__(self)

    @classmethod
    def from_any(cls, o: object) -> DyckWord:
        r"""Declares a Dyck word from a Python object that can be interpreted as a dyck-word.

        :param o: A Python object.
        :return: A Dyck word.
        """
        if isinstance(o, DyckWord):
            return o
        else:
            o: str = str(o)
            return DyckWord(o)

    @functools.cached_property
    def characters_number(self) -> int:
        return len(self)

    @util.readonly_class_property
    def is_equal_to_relation(self) -> typing.Type[brl.BinaryRelation]:
        return IsEqualTo

    @util.readonly_class_property
    def is_strictly_less_than_relation(self) -> typing.Type[brl.BinaryRelation]:
        return LexicographicOrder

    @util.readonly_class_property
    def least_element(cls) -> DyckWord:
        return cls.is_strictly_less_than_relation.least_element


# Flexible types to facilitate data validation

FlexibleDyckWord = typing.Union[
    DyckWord, str]

# Aliases

DW = DyckWord  # An alias for Dyck word
