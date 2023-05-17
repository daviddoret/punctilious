import core
import random_data

n1 = random_data.random_word()
n2 = random_data.random_word()
n3 = random_data.random_word()
n4 = random_data.random_word()
n5 = random_data.random_word()

t1 = core.Theory(symbol=f'{n1}-theory', capitalizable=True)
a1 = core.Axiom(theory=t1, axiom_text=f'{n1.capitalize()} is a {n2}.', capitalizable=True)
a2 = core.Axiom(theory=t1, axiom_text=f'If a 𝒙 is a {n2}, then 𝒙 is a {n3}.', capitalizable=True)
o1 = core.SimpleObjct(theory=t1, symbol=n1, capitalizable=True)
o2 = core.SimpleObjct(theory=t1, symbol=n2, capitalizable=True)
o3 = core.SimpleObjct(theory=t1, symbol=n3, capitalizable=True)
r1 = core.Relation(theory=t1, arity=2, formula_rep=core.Formula.reps.infix_operator, symbol='is-a')
core.DirectAxiomInferenceStatement(theory=t1, axiom=a1, valid_proposition=core.Formula(theory=t1, relation=r1, parameters=(o1, o2)))
x_is_a_o2 = core.Formula(theory=t1, relation=r1, parameters=(core.FreeVariablePlaceholder(symbol='𝒙'), o2))
x_is_a_o3 = core.Formula(theory=t1, relation=r1, parameters=(core.FreeVariablePlaceholder(symbol='𝒙'), o3))
implication_1 = core.Formula(theory=t1, relation=core._implies, parameters=(x_is_a_o2, x_is_a_o3))
core.DirectAxiomInferenceStatement(theory=t1, axiom=a1, valid_proposition=core.Formula(theory=t1, relation=core._implies, parameters=(o1, o2)))
core.ModusPonensStatement(theory=t1, )

t1.prnt()

