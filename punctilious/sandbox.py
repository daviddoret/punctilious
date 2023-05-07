

class subformula:
    def __init__(self, internal_set):
        self.internal_set = internal_set

s1 = subformula(frozenset(['a','b','c']))
s2 = subformula(frozenset(['a','c','f']))
s3 = subformula(frozenset(['g','h']))
super_1 = tuple([s1, s2, s3])
super_set = frozenset().union(*[sub.internal_set for sub in super_1])
print(super_set)



