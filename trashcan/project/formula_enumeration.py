from __future__ import annotations


def get_composite_definitional_name(a: Proposition, b: Proposition) -> str:
    pair = [a, b]
    pair = sorted(pair)
    return f'({pair[0]}, {pair[1]})'


class Proposition:
    index_counter: int = 0

    def __init__(self):
        self.i = Proposition._get_p_index()

    def __lt__(self, other):
        # return self.i < other.i
        if self == other:
            return False
        if isinstance(self, AtomicProposition):
            if isinstance(other, AtomicProposition):
                return self.i < other.i
            elif isinstance(other, CompositeProposition):
                if self == other.a:
                    # if component a is equal,
                    # the atomic formula comes first.
                    return True
                else:
                    return self < other.a
            else:
                raise Exception('ooops')
        elif isinstance(self, CompositeProposition):
            if isinstance(other, AtomicProposition):
                return self.i < other.i
            elif isinstance(other, CompositeProposition):
                if self.a == other.a:
                    return self.b < other.b
                else:
                    return self.a < other.a
            else:
                raise Exception('ooops')
        else:
            raise Exception('ooops')

    def __gt__(self, other):
        if self == other:
            return False
        else:
            return not self < other

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.definitional_name)

    def __str__(self):
        return self.definitional_name

    def __repr__(self):
        return self.definitional_name

    @property
    def denoting_name(self) -> str:
        if isinstance(self, AtomicProposition):
            return f'a{self.i}'
        elif isinstance(self, CompositeProposition):
            return f'p{self.i}'
        else:
            raise Exception('ooops')

    @property
    def definitional_name(self) -> str:
        if isinstance(self, AtomicProposition):
            return self.denoting_name
        elif isinstance(self, CompositeProposition):
            return get_composite_definitional_name(a=self.a, b=self.b)
        else:
            raise Exception('ooops')

    @staticmethod
    def _get_p_index() -> int:
        AtomicProposition.index_counter = AtomicProposition.index_counter + 1
        return AtomicProposition.index_counter


class AtomicProposition(Proposition):

    def __init__(self):
        super().__init__()
        print(f'Let {self.denoting_name} be an atomic proposition.')


class CompositeProposition(Proposition):
    def __init__(self, a: Proposition, b: Proposition):
        super().__init__()
        pair = [a, b]
        pair = sorted(pair)
        self.a = pair[0]
        self.b = pair[1]  # print(f'Let {self.denoting_name} := {self.definitional_name}.')


def complete_missing_pairs(s: set):
    s_complement = set()
    for a in s:
        for b in s:
            definitional_name = get_composite_definitional_name(a=a, b=b)
            if definitional_name not in s and definitional_name not in s_complement:
                q = CompositeProposition(a=a, b=b)
                s_complement.add(q)
    print(f'Complement: {len(s_complement)}')
    return s.union(s_complement)


n: int = 0
atomic_proposition_max: int = 5
develop_enumeration: bool = True
a = set()
s = set()
while develop_enumeration:
    n = n + 1
    print('_____')
    print(f'n = {n}')
    print(f's{n} = s{n - 1} ∪ a{n}')
    p = AtomicProposition()
    a = a.union({p})
    s = s.union({p})
    print(f'|a{n}| = {len(a)}')
    print(f'|s{n}| = {len(s)}')
    # print(f'Complete the missing pairs')
    s = complete_missing_pairs(s=s)
    if n >= atomic_proposition_max:
        develop_enumeration = False
    # print(f's := {sorted(s)}')
    print(f'|s{n}| = {len(s)}')
    print(f'|c{n}| = |s{n}| - |a{n}| = {len(s) - len(a)}')
    # print(f's = {sorted(s)}')
    pass
