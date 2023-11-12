import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.create_universe_of_discourse(echo=True)
a1 = u.declare_axiom(natural_language='Dummy axiom to establish some ground propositions.')
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
f = u.r.declare(arity=2, symbol='f', signal_proposition=True)
t1 = u.declare_theory(echo=True)

# Elaborate a dummy theory with a set of propositions necessary for our demonstration

# t theory derivation statements.
# these are predecessor statements that are contained in the h hypothesis.
a = t1.include_axiom(a=a1)
predecessor = t1.i.axiom_interpretation.infer_formula_statement(a=a, p=f(o2, o3), lock=False)
with u.with_variable('x') as x, u.with_variable('y') as y, u.with_variable('z') as z:
    implication = t1.i.axiom_interpretation.infer_formula_statement(a=a,
        p=(f(x, y) | u.r.land | f(y, z)) | u.r.implies | f(x, z), lock=True)
t1.stabilize()
t1.take_note(
    content='Until this point, statements are predecessors to the hypothesis, and they are contained in the (coming) h hypothesis.')

# Pose some hypothesis and infer some statement that we couldn't infer otherwise
# h theory derivation statements.
h = t1.pose_hypothesis(hypothesis_formula=f(o1, o2), subtitle='Pose some hypothesis')
conjunction_introduction = h.child_theory.i.conjunction_introduction.infer_formula_statement(p=f(o1, o2), q=f(o2, o3))
variable_substitution = h.child_theory.i.variable_substitution.infer_formula_statement(p=implication,
    phi=u.r.tupl(o1, o2, o3))
proposition_of_interest = h.child_theory.i.modus_ponens.infer_formula_statement(p_implies_q=variable_substitution,
    p=conjunction_introduction)
h.child_theory.take_note(content='Note that without the f(o1, o2) hypothesis, we could not infer f(o1, o3).')

t1.take_note(
    content='From this point on, statements are successors to the hypothesis, and they are not contained in the h hypothesis.')
successor = t1.i.double_negation_introduction.infer_formula_statement(p=f(o2, o3))
