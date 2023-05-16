import core

t1 = core.Theory(dashed='test-theory-1')
a1 = core.Axiom(theory=t1, text='If a floo is wala, then it is pilipili.')
core.Statement(theory=t1, truth_object=a1)
a2 = core.Axiom(theory=t1, text='If a pilipili is egege, then it is tog.')
core.Statement(theory=t1, truth_object=a2)
o1 = core.SimpleObjct(theory=t1)
r1 = core.Relation(theory=t1, arity=2, formula_frmt=core.Formula.frmts.infix_operator, dashed='is', symbol='')
x = t1.repr_as_theory()
t1.prnt()

