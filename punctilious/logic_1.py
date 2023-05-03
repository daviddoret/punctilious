import core
core.Formula.echo = True

proposition = core.Objct('proposition')
ltrue = core.Objct('true')
lfalse = core.Objct('false')
leq = core.Objct('=', alt_nam_dic={'long name': 'logical equality'}, parent_formula_default_str_fun=core.FormulaStringFunctions.infix)
lneq = core.Objct('≠', parent_formula_default_str_fun=core.FormulaStringFunctions.infix)
lnot = core.Objct('¬', parent_formula_default_str_fun=core.FormulaStringFunctions.function)
liif = core.Objct('⟺', parent_formula_default_str_fun=core.FormulaStringFunctions.infix)
lor = core.Objct('∨', parent_formula_default_str_fun=core.FormulaStringFunctions.infix)
land = core.Objct('∧', parent_formula_default_str_fun=core.FormulaStringFunctions.infix)

f1 = core.Formula((leq, ltrue, ltrue))
f2 = core.Formula((leq, lfalse, lfalse))
f3 = core.Formula((lneq, ltrue, lfalse))
f4 = core.Formula((lneq, lfalse, ltrue))
f5 = core.Formula((lnot, ltrue))
f6 = core.Formula((lnot, lfalse))
f7 = core.Formula((leq, f5, lfalse))
f8 = core.Formula((leq, f6, ltrue))

vp = core.Variable('p')
f9 = core.Formula((core.is_of_class, vp, proposition))
f10 = core.Formula((leq, vp, ltrue))
f11 = core.Formula((leq, vp, lfalse))
f12 = core.Formula((lor, f10, f11))
#f13: (p is a proposition) ⟺ ((p = true) ∨ (p = false))
f13 = core.Formula((liif, f9, f12))

# statement: q = false
# from f13, it follows that q is a proposition
vq = core.Variable('q')
f14 = core.Formula((leq, vq, lfalse))

theory = []
print(f14)
print(f13.formula_tup[2])
if f14.is_variable_equal_to(f13.formula_tup[1]):
    print('variable equal')
    print('add implication to theory if it is not already there')
    # variable_mapping

