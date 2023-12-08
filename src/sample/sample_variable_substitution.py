import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.create_universe_of_discourse(echo=True)
a1 = u.a.declare(natural_language='Dummy axiom to establish some ground propositions.')
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
f = u.c1.declare(arity=2, symbol='f', signal_proposition=True)
t1 = u.t.declare(echo=True)

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
a = t1.include_axiom(a=a1)
t1.i.axiom_interpretation.infer_formula_statement(a=a, p=f(o1, o2), lock=False)
with u.with_variable('x') as x, u.with_variable('y') as y:
    implication = t1.i.axiom_interpretation.infer_formula_statement(a=a, p=f(x, y) | u.c1.implies | f(y, x), lock=True)
t1.stabilize()

proposition_of_interest = t1.i.variable_substitution.infer_formula_statement(p=implication, phi=u.c1.tupl(o1, o2))
