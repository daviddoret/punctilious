import core
import random_data

n1 = random_data.random_word()
n2 = random_data.random_word()
n3 = random_data.random_word()
n4 = random_data.random_word()
n5 = random_data.random_word()

t1 = core.Theory(dashed='test-theory-1')
a1 = core.Axiom(theory=t1, text=f'{n1} is a {n2}.')
core.AxiomStatement(theory=t1, axiom=a1)
a2 = core.Axiom(theory=t1, text=f'If a {n3} is {n4}, then it is {n5}.')
core.AxiomStatement(theory=t1, axiom=a2)
o1 = core.SimpleObjct(theory=t1, dashed=n1)
o2 = core.SimpleObjct(theory=t1, dashed=n2)
o3 = core.SimpleObjct(theory=t1, dashed=n3)
o4 = core.SimpleObjct(theory=t1, dashed=n4)
o5 = core.SimpleObjct(theory=t1, dashed=n5)
r1 = core.Relation(theory=t1, arity=2, formula_frmt=core.Formula.frmts.infix_operator, dashed='is', symbol='')
core.AxiomFormalization(theory=t1, axiom=a1, truth_object=core.Formula(theory=t1, relation=r1, parameters=(o1, o2)))
x = t1.repr_as_theory()
t1.prnt()

