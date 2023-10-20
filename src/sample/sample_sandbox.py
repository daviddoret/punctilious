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

with u.v() as x, u.v() as y:
    phi: pu.Formula = (a | u.r.implies | x) | u.r.iff | (y | u.r.land | b)
    print(phi)

with u.v() as x, u.v() as y:
    psi: pu.Formula = (a | u.r.implies | x) | u.r.iff | (y | u.r.land | b)
    print(psi)

#  p = MGZ2021MinimalLogicM0()

print(phi.is_formula_syntactically_equivalent_to(phi=psi))

_, a2, _ = pu.verify_formula(u=u, input_value=a)

pass
