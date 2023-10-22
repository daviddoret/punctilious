"""This sample script export all theory packages."""

import punctilious as pu
import theory as pu_theory

target_folder = '../../data/'

# pu.configuration.echo_default = False
# t = pu_theory.MGZ2021ClassicalLogicK0().t
# print('---------------------------')
# print(t.rep_article())

u = pu.create_universe_of_discourse()

a = u.o.declare()
b = u.o.declare()
c = u.o.declare()
d = u.o.declare()

with u.with_variable() as x, u.with_variable() as y:
    phi: pu.Formula = (a | u.r.implies | x) | u.r.iff | (y | u.r.land | b)
    print(phi)

with u.with_variable() as x, u.with_variable() as y:
    psi: pu.Formula = (x | u.r.implies | x) | u.r.iff | (y | u.r.land | b)
    print(psi)

v = frozenset(phi.v).union(psi.v)

print(phi.is_masked_formula_similar_to(phi=psi, mask=v))
print(psi.is_masked_formula_similar_to(phi=phi, mask=v))

pass
