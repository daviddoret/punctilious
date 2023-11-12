import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
o2 = u.o.declare()
t1 = u.declare_theory(echo=True)
axiom = u.a.declare(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with inconsistent propositions
theory_axiom = t1.include_axiom(axiom)
x_equal_y = t1.i.axiom_interpretation.infer_formula_statement(theory_axiom, (o1 | u.c1.equal | o2), lock=False)
x_unequal_y = t1.i.axiom_interpretation.infer_formula_statement(theory_axiom, (o1 | u.c1.unequal | o2), lock=True)
t1.stabilize()

# Use a distinct theory T2 to demonstrate the inconsistency of T1
# because T1 could not prove its own inconsistency because it is inconsistent!
t2 = u.declare_theory(echo=True)

# And finally, use the inconsistency-introduction-2 inference-rule:
proposition_of_interest = t2.i.inconsistency_introduction_2.infer_formula_statement(x_equal_y=x_equal_y,
    x_unequal_y=x_unequal_y, t=t1, subtitle='The proposition of interest')
