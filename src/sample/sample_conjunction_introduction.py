import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
r1 = u.c1.declare(arity=2, signal_proposition=True)
r2 = u.c1.declare(arity=1, signal_proposition=True)
axiom = u.a.declare(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
t1 = u.t.declare(echo=True)
theory_axiom = t1.include_axiom(a=axiom)
phi1 = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=r1(o1, o2), lock=False)
phi2 = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=r2(o3), lock=True)

# And finally, use the conjunction-introduction inference-rule:
proposition_of_interest = t1.i.conjunction_introduction.infer_formula_statement(p=phi1, q=phi2,
    subtitle='The proposition of interest')
