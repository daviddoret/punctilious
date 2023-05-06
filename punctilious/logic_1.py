import core

core.FormulaStatement.echo = False
core.Theory.echo_statement = True
theory = core.Theory(dashed_name='propositional-logic-theory')

axiom_1 = theory.append_axiom(text='Truth is true')

ltrue = core.ObjctObsolete(sym='𝚃', dashed_name='truth')
phi_02 = core.FormulaStatement((ltrue))
theory.append_formula_statement(tup=phi_02,
                                justification=core.Justification(method=core.justification_methods.statement_derivation, justifying_statement=axiom_1))

proposition_class = core.ObjctObsolete(sym='proposition-class', dashed_name='proposition-class')
phi_01 = core.FormulaStatement((core.class_membership, proposition_class, core.class_nature))

lfalse = core.ObjctObsolete(sym='𝙵', dashed_name='falsum')
leq = core.ObjctObsolete(sym='=', dashed_name='equality-connective',
                         parent_formula_default_str_fun=core.FormulaStringFunctions.infix)
lneq = core.ObjctObsolete(sym='≠', dashed_name='inequality-connective',
                          parent_formula_default_str_fun=core.FormulaStringFunctions.infix)
lnot = core.ObjctObsolete(sym='¬', dashed_name='negation-connective',
                          parent_formula_default_str_fun=core.FormulaStringFunctions.function)
limplies = core.ObjctObsolete(sym='→', dashed_name='material-implication-connective',
                              parent_formula_default_str_fun=core.FormulaStringFunctions.infix)
liif = core.ObjctObsolete(sym='⟺', dashed_name='biconditional-connective',
                          parent_formula_default_str_fun=core.FormulaStringFunctions.infix)
lor = core.ObjctObsolete(sym='∨', dashed_name='disjunction-connective',
                         parent_formula_default_str_fun=core.FormulaStringFunctions.infix)
land = core.ObjctObsolete(sym='∧', dashed_name='conjunction-connective',
                          parent_formula_default_str_fun=core.FormulaStringFunctions.infix)

f1 = core.FormulaStatement((leq, ltrue, ltrue))
f2 = core.FormulaStatement((leq, lfalse, lfalse))
f3 = core.FormulaStatement((lneq, ltrue, lfalse))
f4 = core.FormulaStatement((lneq, lfalse, ltrue))
f5 = core.FormulaStatement((lnot, ltrue))
f6 = core.FormulaStatement((lnot, lfalse))
f7 = core.FormulaStatement((leq, f5, lfalse))
f8 = core.FormulaStatement((leq, f6, ltrue))

vp = core.Variable('p')
f9 = core.FormulaStatement((core.class_membership, vp, proposition_class))
f10 = core.FormulaStatement((leq, vp, ltrue))
f11 = core.FormulaStatement((leq, vp, lfalse))
f12 = core.FormulaStatement((lor, f10, f11))
# f13: (p is a proposition) ⟺ ((p = true) ∨ (p = false))
f13 = core.FormulaStatement((liif, f9, f12))

# statement: q = false
# from f13, it follows that q is a proposition
vq = core.Variable('q')
f14 = core.FormulaStatement((leq, vq, lfalse))

theory = []
print(f14)
print(f13.content[2])
if f14.is_variable_equal_to(f13.content[1]):
    print('variable equal')
    print('add implication to theory if it is not already there')
    # variable_mapping
