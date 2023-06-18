import punctilious as p
import random_data

u = p.UniverseOfDiscourse()
t = u.t(random_data.random_sentence())
r1 = u.r.declare(1, signal_proposition=True)
r2 = u.r.declare(2, signal_proposition=True)
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
a = u.axiom(random_data.random_sentence())
ap = t.postulate_axiom(a, echo=True)
"""
f1 = u.f(r1, o1)
f2 = u.f(r1, o3)
f3 = u.f(r2, f1, f2)
dai1 = t.dai(f1, ap=ap, header='a.b.c')
dai2 = t.dai(f2, ap=ap, header='4.5.6')
dai3 = t.dai(f3, ap=ap)
print(t.repr_theory_report())
"""
