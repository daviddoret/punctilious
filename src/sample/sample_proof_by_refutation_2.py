import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.declare()
o2 = u.o.declare()
f = u.r.declare(arity=1, symbol='f')
t1 = u.t(echo=True)
axiom = u.declare_axiom(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with inconsistent propositions
theory_axiom = t1.include_axiom(axiom)
f_o1_eq_f_02 = t1.i.axiom_interpretation.infer_formula_statement(theory_axiom,
    (f(o1) | u.r.eq | f(o2)))
with u.v('x') as x, u.v('y') as y:
    implication = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom,
        formula=(f(x) | u.r.eq | f(y)) | u.r.implies | (x | u.r.neq | y))
t1.stabilize()

# Pose the inequality hypothesis
h = t1.pose_hypothesis(hypothesis_formula=o1 | u.r.eq | o2,
    subtitle='We pose the positive hypothesis')
substitution = h.child_theory.i.variable_substitution.infer_formula_statement(p=implication,
    phi=u.r.tupl(o1, o2))
inequality = h.child_theory.i.modus_ponens.infer_formula_statement(p_implies_q=substitution,
    p=f_o1_eq_f_02)

# Use a distinct theory T2 to demonstrate the inconsistency of T1
# because T1 could not prove its own inconsistency because it is inconsistent!
t2 = u.t(echo=True)

# Prove hypothesis inconsistency
h_inconsistency = t2.i.inconsistency_introduction_2.infer_formula_statement(
    x_eq_y=h.child_statement, x_neq_y=inequality, inconsistent_theory=h.child_theory,
    subtitle='The proposition of interest')

# And finally, use the proof-by-contradiction-2 inference-rule:
proposition_of_interest = t1.i.proof_by_refutation_2.infer_formula_statement(x_eq_y_hypothesis=h,
    inc_hypothesis=h_inconsistency, subtitle='The proposition of interest')
