import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
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
    formula=r1(o1, o2) | u.r.biconditional | r2(o3))

# And finally, use the biconditional-elimination-1 inference-rule:
proposition_of_interest = t1.i.biconditional_elimination_1.infer_statement(p_iff_q=phi1,
    subtitle='The proposition of interest', echo=True)
