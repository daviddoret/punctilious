import punctilious as pu

u = pu.UniverseOfDiscourse()
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
r1 = u.c1.declare(signal_proposition=True)
r2 = u.c1.declare(signal_proposition=True)
r3 = u.c1.declare()

phi1: pu.CompoundFormula = o1 | r2 | o2
print(phi1)
_, phi1, _ = pu.verify_formula(u=u, input_value=phi1)
print(phi1)

with u.with_variable(symbol='x') as x:
    phi2: pu.CompoundFormula = o1 | r2 | x
print(phi2)
_, phi2, _ = pu.verify_formula(u=u, input_value=phi2)
print(phi2)

with u.with_variable(symbol='x') as x:
    phi3: pu.CompoundFormula = o1 | r2 | x
print(phi3)
_, phi3, _ = pu.verify_formula(u=u, input_value=phi3)
print(phi3)

_, phi4, _ = pu.verify_formula(u=u, input_value=phi3, form=phi2)
print(phi4)
