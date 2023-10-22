import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.create_universe_of_discourse(echo=True)
a1 = u.declare_axiom(natural_language='Dummy axiom to establish some ground propositions.')
o1 = u.o.declare()
o2 = u.o.declare()
o3 = u.o.declare()
f = u.r.declare(arity=2, symbol='f', signal_proposition=True)
t1 = u.t(echo=True)

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
a = t1.include_axiom(a=a1)
pu.configuration.echo_proof = False
t1.i.axiom_interpretation.infer_formula_statement(a=a, p=f(o1, o2), lock=False)
t1.i.axiom_interpretation.infer_formula_statement(a=a, p=f(o2, o3), lock=False)
with u.with_variable('x') as x, u.with_variable('y') as y, u.with_variable('z') as z:
    implication = t1.i.axiom_interpretation.infer_formula_statement(a=a,
        p=(f(x, y) | u.r.land | f(y, z)) | u.r.implies | f(x, z), lock=True)
t1.stabilize()

# Pose the negation hypothesis
h = t1.pose_hypothesis(hypothesis_formula=u.r.lnot(f(o1, o3)),
    subtitle='We pose the negation hypothesis')

for i in h.child_theory.iterate_statements_in_theory_chain():
    print(i)

conjunction_introduction = h.child_theory.i.conjunction_introduction.infer_formula_statement(
    p=f(o1, o2), q=f(o2, o3))
variable_substitution = h.child_theory.i.variable_substitution.infer_formula_statement(
    p=implication, phi=u.r.tupl(o1, o2, o3))
modus_ponens = h.child_theory.i.modus_ponens.infer_formula_statement(
    p_implies_q=variable_substitution, p=conjunction_introduction)

# Prove hypothesis inconsistency
pu.configuration.echo_proof = True
h_inconsistency = t1.i.inconsistency_introduction_1.infer_formula_statement(p=modus_ponens,
    not_p=h.child_statement, t=h.child_theory, subtitle='Proof of the hypothesis inconsistency')

# And finally, use the proof-by-contradiction-1 inference-rule:
proposition_of_interest = t1.i.proof_by_contradiction_1.infer_formula_statement(h=h,
    inc_h=h_inconsistency, subtitle='The proposition of interest')
