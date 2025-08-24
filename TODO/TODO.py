r"""

in all @classmethod MyClass.from_blablabla(cls, ...): use cls properly (like in RPTL),
to ensure these methods will return the correct type when called from classes inheriting from MyClass.

in syntactic structures, implement a solution to have consistent root_labels. then
assure that is_blablabla_equivalent methods are equivalent to is_lrpt_equivalent method.,

rename parameter n to root_label in from_blablabla methods.

Review comments "The main element ... is not an information". This is wrong.

review from_XXX methods to assure we include n=self.root_label in it when applicable.

review methods is_well_formed to factor in the root_label. probably by passing it as a parameter.

is there a way to design SyntacticSet (and other similar structures) in such a way
as to preserve the python types of its elements? For example to support a set of ordered pairs?

check that __init__ does nothing on input arguments. because immutable objects are
not modified by __new__. consider removing __init__ and creating properties in __new__ instead.

implement cls.sort() following the same approach as in RPTL in all foundational classes.

"""
