import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
o4 = u.o.declare()
axiom = u.declare_axiom(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
t1 = u.declare_theory(echo=True)
theory_axiom = t1.include_axiom(a=axiom)
phi1 = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=o1 | u.c1.implies | o2, lock=False)
phi2 = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=o3 | u.c1.implies | o4, lock=False)
phi3 = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=u.c1.lnot(o2) | u.c1.lor | u.c1.lnot(o4),
    lock=True)

# And finally, use the conjunction-introduction inference-rule:
proposition_of_interest = t1.i.destructive_dilemma.infer_formula_statement(p_implies_q=phi1, r_implies_s=phi2,
    not_q_or_not_s=phi3, subtitle='The proposition of interest')
