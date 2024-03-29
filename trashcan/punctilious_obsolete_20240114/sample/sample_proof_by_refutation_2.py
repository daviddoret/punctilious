import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.register()
o2 = u.o.register()
f = u.c1.register(arity=1, symbol='f')
t1 = u.t.register(echo=True)
axiom = u.a.register(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with inconsistent propositions
theory_axiom = t1.include_axiom(axiom)
f_o1_eq_f_02 = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=(f(o1) | u.c1.eq | f(o2)),
    lock=False)
with u.with_variable('x') as x, u.with_variable('y') as y:
    implication = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom,
        p=(f(x) | u.c1.eq | f(y)) | u.c1.implies | (x | u.c1.neq | y), lock=True)
t1.stabilize()

# Pose the inequality hypothesis
h = t1.pose_hypothesis(hypothesis_formula=o1 | u.c1.eq | o2, subtitle='We pose the positive hypothesis')
substitution = h.child_theory.i.variable_substitution.infer_formula_statement(p=implication, phi=u.c1.tupl(o1, o2))
inequality = h.child_theory.i.modus_ponens.infer_formula_statement(p_implies_q=substitution, p=f_o1_eq_f_02)

# Prove hypothesis inconsistency
h_inconsistency = t1.i.inconsistency_introduction_2.infer_formula_statement(x_equal_y=h.child_statement,
    x_unequal_y=inequality, t=h.child_theory, subtitle='The proposition of interest')

# And finally, use the proof-by-contradiction-2 inference-rule:
proposition_of_interest = t1.i.proof_by_refutation_2.infer_formula_statement(h=h, inc_h=h_inconsistency,
    subtitle='The proposition of interest')
