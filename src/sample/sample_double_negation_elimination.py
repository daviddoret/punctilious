import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
o2 = u.o.declare()
r1 = u.r.declare(arity=2, signal_proposition=True)
axiom = u.declare_axiom(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
t1 = u.t(echo=True)
theory_axiom = t1.include_axiom(a=axiom)
not_not_p = t1.i.axiom_interpretation.infer_formula_statement(axiom=theory_axiom,
    formula=u.r.lnot(u.r.lnot(r1(o1, o2))))

# And finally, use the double-negation-elimination inference-rule:
proposition_of_interest = t1.i.double_negation_elimination.infer_formula_statement(
    not_not_p=not_not_p, subtitle='The proposition of interest')
