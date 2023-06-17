import punctilious as pu

u = pu.UniverseOfDiscourse()
r1 = u.r.declare(1)
r2 = u.r.declare(2)
with u.v('x') as x, u.v('y') as y, u.v('z') as z:
    f = u.f(r2, z, u.f(r2, z, u.f(x, y, u.f(x, y, z))), echo=True)
    print(f.get_variable_ordered_set())
