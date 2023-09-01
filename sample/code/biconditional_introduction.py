import punctilious as pu

pu.configuration.echo_default = False
pu.configuration.echo_inferred_statement = True
pu.configuration.echo_axiom_inclusion = True
pu.configuration.echo_proof = True

# Create a universe-of-discourse with basic objects for the sake of this demonstration.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
r1 = u.r.declare(2, signal_proposition=True)
r2 = u.r.declare(1, signal_proposition=True)
axiom = u.declare_axiom(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
t1 = u.t(echo=True)
theory_axiom = t1.include_axiom(a=axiom)
phi1 = t1.i.axiom_interpretation.infer_statement(axiom=theory_axiom,
    formula=r1(o1, o2) | u.r.implies | r2(o3))
phi2 = t1.i.axiom_interpretation.infer_statement(axiom=theory_axiom,
    formula=r2(o3) | u.r.implies | r1(o1, o2))

# And finally, use the biconditional-introduction inference-rule:
pu.configuration.echo_proof = True
biconditional_inference = t1.i.bi.infer_statement(p_implies_q=phi1, q_implies_p=phi2)