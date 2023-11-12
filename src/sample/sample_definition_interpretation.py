import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
r1 = u.c1.declare(2, signal_proposition=True)
r2 = u.c1.declare(1, signal_proposition=True)
definition = u.declare_definition(natural_language='Dummy definition for demonstration purposes')

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
t1 = u.declare_theory(echo=True)
theory_definition = t1.include_definition(d=definition)

# And finally, use the absorption inference-rule:
proposition_of_interest = t1.i.definition_interpretation.infer_formula_statement(d=theory_definition, x=r1(o1, o2),
    y=r2(o3), subtitle='The proposition of interest')
