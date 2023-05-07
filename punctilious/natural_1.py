import core
core.Axiom.echo_init = True
core.Theory.echo_statement = True

theory = core.Theory(dashed_name='natural-numbers-theory')

axiom_1 = theory.append_axiom(text='0 is a natural number.', citation='Tao, 2006, p. 19')

natural_numbers = theory.append_objct(sym='ℕ', dashed_name='natural-numbers')
s_02 = theory.append_formula_statement(tup=(core.class_membership, natural_numbers, core.class_nature), justification=core.Justification(core.justification_methods.axiom_encoding, axiom_1))

zero = theory.append_objct(sym='0', dashed_name='zero')
s_03 = theory.append_formula_statement(tup=(core.class_membership, zero, natural_numbers), justification=core.Justification(core.justification_methods.axiom_encoding, axiom_1))

n = theory.append_variable(sym='n', dashed_name='n')
m = theory.append_variable(sym='m', dashed_name='m')

equal = theory.append_relation(sym='=', dashed_name='equality-operator', formula_str_fun=core.formula_str_funs.infix)
successor = theory.append_relation(sym='++', dashed_name='successor-operator', formula_str_fun=core.formula_str_funs.condensed_unary_postfix)
#add = core.Objct('+', formula_str_fun=core.FormulaStringFunctions.infix)
#less_or_equal = core.Objct('≤', formula_str_fun=core.FormulaStringFunctions.infix, alt_nam_dic={'long name': 'less or equal to'})

#phi1 = core.Formula(n1)
#phi2 = core.Formula((nadd, n1, n2))
#phi3 = core.Formula((nleq, phi1, phi2))