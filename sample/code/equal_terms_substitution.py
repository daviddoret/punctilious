import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this demonstration.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
r1 = u.r.declare(arity=2, signal_proposition=True)
r2 = u.r.declare(arity=1, signal_proposition=True)
axiom = u.declare_axiom(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
t1 = u.t(echo=True)
theory_axiom = t1.include_axiom(a=axiom)
proposition_x_equal_y = t1.i.axiom_interpretation.infer_statement(axiom=theory_axiom,
    formula=u.f(u.r.equal, u.f(r1, o1, o2), u.f(r2, o3)))
dummy_proposition = t1.i.axiom_interpretation.infer_statement(axiom=theory_axiom,
    formula=u.f(r1, u.f(r1, u.f(r1, u.f(r1, o1, o2), u.f(r1, o1, o2)), o2),
        u.f(r2, u.f(r1, o1, o2))))

# And finally, use the biconditional-introduction inference-rule:
proposition_of_interest = t1.i.ets.infer_statement(p=dummy_proposition,
    x_equal_y=proposition_x_equal_y)
