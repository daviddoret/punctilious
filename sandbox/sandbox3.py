import core

u = core.UniverseOfDiscourse()
o1 = u.o()
o2 = u.o()
o3 = u.o()
r1 = u.r(1)
r2 = u.r(2)
core.configuration.echo_default = True
core.configuration.echo_formula = None
u.f(r2, u.f(r1, o3), u.f(r2, o3, o1))
