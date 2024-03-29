"""This sample script export all theory packages."""

import punctilious as pu
import theory as pu_theory

target_folder = '../../data/'

# pu.configuration.echo_default = False
# t = pu_theory.MGZ2021ClassicalLogicK0().t
# print('---------------------------')
# print(t.rep_article())

u = pu.create_universe_of_discourse()

a = u.o.register()
b = u.o.register()
c = u.o.register()
d = u.o.register()

with u.with_variable() as x, u.with_variable() as y:
    phi: pu.CompoundFormula = (a | u.c1.implies | x) | u.c1.iff | (y | u.c1.land | b)
    print(phi)

with u.with_variable() as x, u.with_variable() as y:
    psi: pu.CompoundFormula = (x | u.c1.implies | x) | u.c1.iff | (y | u.c1.land | b)
    print(psi)

v = frozenset(phi.get_unique_variable_ordered_set).union(psi.get_unique_variable_ordered_set)

print(phi.is_masked_formula_similar_to(phi=psi, mask=v))
print(psi.is_masked_formula_similar_to(phi=phi, mask=v))

pass
