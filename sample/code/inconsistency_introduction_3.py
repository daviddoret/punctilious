import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this demonstration.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
t1 = u.t(echo=True)
axiom = u.declare_axiom(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with inconsistent propositions
theory_axiom = t1.include_axiom(axiom)
p_neq_p = t1.i.axiom_interpretation.infer_statement(theory_axiom, (o1 | u.r.neq | o1))
t1.stabilize()

# Use a distinct theory T2 to demonstrate the inconsistency of T1
# because T1 could not prove its own inconsistency because it is inconsistent!
t2 = u.t(echo=True)

# And finally, use the inconsistency-introduction-3 inference-rule:
proposition_of_interest = t2.i.inconsistency_introduction_3.infer_statement(p_neq_p=p_neq_p,
    inconsistent_theory=t1, subtitle='The proposition of interest')
