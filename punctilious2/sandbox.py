import core
import random_data

n1 = random_data.random_word()
n2 = random_data.random_word()
n3 = random_data.random_word()
n4 = random_data.random_word()
n5 = random_data.random_word()

t1 = core.Theory(symbol='test-theory-1')
a1 = core.Axiom(theory=t1, symbol='axiom-1', capitalizable=True, text=f'{n1.capitalize()} is a {n2}.')
core.AxiomStatement(theory=t1, axiom=a1)
a2 = core.Axiom(theory=t1, symbol='axiom-2', capitalizable=True, text=f'If a {n3} is {n4}, then it is a {n5}.')
core.AxiomStatement(theory=t1, axiom=a2)
o1 = core.SimpleObjct(theory=t1, symbol=n1, capitalizable=True)
o2 = core.SimpleObjct(theory=t1, symbol=n2, capitalizable=True)
o3 = core.SimpleObjct(theory=t1, symbol=n3, capitalizable=True)
o4 = core.SimpleObjct(theory=t1, symbol=n4, capitalizable=True)
o5 = core.SimpleObjct(theory=t1, symbol=n5, capitalizable=True)
r1 = core.Relation(theory=t1, arity=2, formula_rep=core.Formula.reps.infix_operator, symbol='is')
core.AxiomFormalization(theory=t1, axiom=a1, truth_object=core.Formula(theory=t1, relation=r1, parameters=(o1, o2)))
print(t1.repr_as_theory())

