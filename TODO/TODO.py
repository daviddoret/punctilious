r"""

in all @classmethod MyClass.from_blablabla(cls, ...): use cls properly (like in RPTL),
to ensure these methods will return the correct type when called from classes inheriting from MyClass.

in syntactic structures: implement a generic is_equivalent_to method that drops
useless information. for example, the main element of tuples is not an information
that is considered in tuples equivalence.

in syntactic structures: consider transforming the underlying LRPT by effectively
dropping useless information. For example in ordered pairs, subtrees > 2 are dropped,
same for maps, etc. but put some more thinking into this first.



"""
