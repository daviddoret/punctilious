import core

t = core.Theory(dashed='natural-numbers-theory')

zero = core.SimpleObjct(theory=t, dashed='zero', symbol='0')
successor = core.Relation(theory=t, arity=1, dashed='successor', symbol='++')
phi1 = core.Formula(theory=t, relation=successor, parameters=zero)

