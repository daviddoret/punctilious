import punctilious as pu

pu.configuration.encoding = pu.encodings.plaintext

# Create a universe-of-discourse with basic objects for the sake of this example.
u = pu.UniverseOfDiscourse(echo=True)
o1 = u.o.register()
o2 = u.o.register()
o3 = u.o.register()
r1 = u.c1.register(2, signal_proposition=True)
r2 = u.c1.register(1, signal_proposition=True)

c1 = u.c3.register(value=o1, echo=True)
c2 = u.c3.register(value=o2 | r1 | o3, echo=True)

with u.with_variable(symbol='x') as x, u.with_variable('y') as y:
    c3 = u.c3.register(value=x | r1 | y, echo=True)

c4 = u.c3.register(value=o3, symbol='C', auto_index=False, echo=True)

# And finally, use the absorption inference-rule:
# proposition_of_interest = t1.i.absorption.infer_formula_statement(p_implies_q=p_implies_q,
#    subtitle='The proposition of interest')
