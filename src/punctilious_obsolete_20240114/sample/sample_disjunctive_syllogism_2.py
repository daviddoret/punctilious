import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.register()
o2 = u.o.register()
o3 = u.o.register()
o4 = u.o.register()
axiom = u.a.register(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
t1 = u.t.register(echo=True)
theory_axiom = t1.include_axiom(a=axiom)
phi1 = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom,
    p=(o1 | u.c1.implies | o3) | u.c1.lor | (o1 | u.c1.implies | o4), lock=False)
phi2 = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=u.c1.lnot((o1 | u.c1.implies | o4)),
    lock=True)

# And finally, use the conjunction-introduction inference-rule:
proposition_of_interest = t1.i.disjunctive_syllogism_2.infer_formula_statement(p_or_q=phi1, not_q=phi2,
    subtitle='The proposition of interest')
