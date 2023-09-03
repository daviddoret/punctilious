import punctilious as pu

pu.configuration.echo_default = False
pu.configuration.echo_inferred_statement = True
pu.configuration.echo_axiom_inclusion = True
pu.configuration.echo_proof = True

# Create a universe-of-discourse with basic objects for the sake of this demonstration.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
o2 = u.o.declare()
t1 = u.t(echo=True)
axiom = u.declare_axiom(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with inconsistent propositions
theory_axiom = t1.include_axiom(axiom)
p_eq_q = t1.i.axiom_interpretation.infer_statement(theory_axiom, (o1 | u.r.eq | o2))
p_neq_q = t1.i.axiom_interpretation.infer_statement(theory_axiom, (o1 | u.r.neq | o2))
t1.stabilize()

# Use a distinct theory T2 to demonstrate the inconsistency of T1
# because T1 could not prove its own inconsistency because it is inconsistent!
t2 = u.t(echo=True)
pu.configuration.echo_proof = True

# And finally, use the inconsistency-introduction-2 inference-rule:
inc_proof = t2.i.inconsistency_introduction_2.infer_statement(x_equal_y=p_eq_q, p_neq_q=p_neq_q,
    inconsistent_theory=t1)
