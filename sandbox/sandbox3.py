import punctilious as p

u = p.UniverseOfDiscourse()
o1 = u.o()
o2 = u.o()
o3 = u.o()
r1 = u.r(1)
r2 = u.r(2)
p.configuration.echo_default = True
p.configuration.echo_formula = None
u.f(r2, u.f(r1, o3), u.f(r2, o3, o1))
