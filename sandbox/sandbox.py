import punctilious as pu

l = pu.pl1.PL1()

pa = l.propositional_variables.declare_proposition_variable()

s = pu.ts.to_string(o=pa, protocol=pu.ts.protocols.unicode_limited, treatment=pu.fl1.treatments.symbolic_representation)

pb = l.propositional_variables.declare_proposition_variable()
phi = l.compound_formulas.declare_binary_formula(connective=l.connectives.conditional, term_1=pa, term_2=pb)

s = pu.ts.to_string(o=phi, protocol=pu.ts.protocols.unicode_limited,
    treatment=pu.fl1.treatments.symbolic_representation)

pass
