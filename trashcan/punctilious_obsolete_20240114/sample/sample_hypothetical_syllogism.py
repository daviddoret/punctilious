import punctilious as pu

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.register()
o2 = u.o.register()
o3 = u.o.register()
r1 = u.c1.register(arity=2, signal_proposition=True)
r2 = u.c1.register(arity=1, signal_proposition=True)
axiom = u.a.register(natural_language='Dummy axiom for demonstration purposes')

# Elaborate a dummy theory with a set of propositions necessary for our demonstration
t1 = u.t.register(echo=True)
theory_axiom = t1.include_axiom(a=axiom)
p_implies_q = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=r1(o1, o2) | u.c1.implies | r2(o3),
    lock=False)
q_implies_r = t1.i.axiom_interpretation.infer_formula_statement(a=theory_axiom, p=r2(o3) | u.c1.implies | r1(o3, o1),
    lock=True)

# And finally, use the modus-ponens inference-rule:
proposition_of_interest = t1.i.hypothetical_syllogism.infer_formula_statement(p_implies_q=p_implies_q,
    q_implies_r=q_implies_r, subtitle='The proposition of interest')
