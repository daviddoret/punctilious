import punctilious as pu

l = pu.pl1.PropositionalLogic()

pa = l.propositional_variables.declare_proposition_variable()

s = pu.ts.to_string(o=pa, protocol=pu.ts.protocols.unicode_limited)

pb = l.propositional_variables.declare_proposition_variable()
phi = l.compound_formulas.declare_binary_formula(connective=l.connectives.material_implication, term_1=pa, term_2=pb)

s = pu.ts.to_string(o=phi, protocol=pu.ts.protocols.unicode_limited)

pass
