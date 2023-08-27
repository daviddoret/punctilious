import punctilious as pu

pu.configuration.echo_default = False
pu.configuration.echo_inferred_statement = True
pu.configuration.echo_axiom_inclusion = True
pu.configuration.echo_proof = True

u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
o2 = u.o.declare()
r1 = u.r.declare(2, signal_proposition=True)
t1 = u.t(echo=True)
axiom = u.declare_axiom(natural_language='Dummy axiom for demonstration purposes')
theory_axiom = t1.include_axiom(axiom)
p = t1.i.axiom_interpretation.infer_statement(theory_axiom, r1(o1, o2))
not_p = t1.i.axiom_interpretation.infer_statement(theory_axiom, u.r.lnot(r1(o1, o2)))
t1.stabilize()
# Use a distinct theory T2 to demonstrate the inconsistency of T1,
# otherwise the demonstration will immediately become invalid,
# because T1 is inconsistent!
t2 = u.t()
pu.configuration.echo_proof = True
inc = t2.i.inconsistency_introduction_1.infer_statement(p=p, not_p=not_p, inconsistent_theory=t1)
