import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.register()
o2 = u.o.register()
o3 = u.o.register()
r1 = u.c1.register(2, signal_proposition=True)
r2 = u.c1.register(1, signal_proposition=True)
axiom = u.a.register(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
t1 = u.t.register(echo=True)
theory_axiom = t1.include_axiom(a=axiom)
phi1 = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=r1(o1, o2) | u.c1.implies | r2(o3),
    lock=False)
phi2 = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=r2(o3) | u.c1.implies | r1(o1, o2),
    lock=True)

# And finally, use the biconditional-introduction inference-rule:
biconditional_inference = t1.i.bi.infer_formula_statement(p_implies_q=phi1, q_implies_p=phi2,
    subtitle='The proposition of interest')
