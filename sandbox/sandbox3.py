import punctilious as p
import random_data

u = p.UniverseOfDiscourse()
t = u.t(random_data.random_sentence())
r1 = u.r(1, signal_proposition=True)
r2 = u.r(2, signal_proposition=True)
o1 = u.o2.declare()
o2 = u.o2.declare()
o3 = u.o2.declare()
a = u.axiom(random_data.random_sentence())
ap = t.postulate_axiom(a)
f1 = u.f(r1, o1)
f2 = u.f(r1, o3)
f3 = u.f(r2, f1, f2)
dai1 = t.dai(f1, ap=ap)
dai2 = t.dai(f2, ap=ap)
dai3 = t.dai(f3, ap=ap)
print(t.repr_theory_report())
