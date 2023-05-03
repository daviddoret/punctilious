import core
core.Theory.echo_axiom = True
core.Theory.echo_statement = True

theory_1 = core.Theory(dashed_name='natural-numbers-theory')

axiom_2_1 = core.Axiom(text='0 is a natural number.', citation='Tao, 2006, p. 19')
s_01 = theory_1.add_statement(axiom_2_1, core.Justification(core.is_axiom))

natural_numbers = core.Objct('ℕ', alt_nam_dic={'long name': 'natural-numbers'})
phi_02 = core.Formula((core.is_of_class, natural_numbers, core.class_class))
s_02 = theory_1.add_statement(phi_02, core.Justification(core.axiom_encoding, s_01))

zero = core.Objct('0', alt_nam_dic={'long name': '0 (natural-number)'})
phi_03 = core.Formula((core.is_of_class, zero, natural_numbers))
s_03 = theory_1.add_statement(phi_03, core.Justification(core.axiom_encoding, s_01))

n = core.Variable('n')
m = core.Variable('m')

equal = core.Objct('=', parent_formula_default_str_fun=core.FormulaStringFunctions.infix, alt_nam_dic={'long name': 'equality of natural numbers'})
successor = core.Objct('++', parent_formula_default_str_fun=core.FormulaStringFunctions.condensed_unary_postfix, alt_nam_dic={'long name': 'natural number successor'})
#add = core.Objct('+', parent_formula_default_str_fun=core.FormulaStringFunctions.infix)
#less_or_equal = core.Objct('≤', parent_formula_default_str_fun=core.FormulaStringFunctions.infix, alt_nam_dic={'long name': 'less or equal to'})

#phi1 = core.Formula(n1)
#phi2 = core.Formula((nadd, n1, n2))
#phi3 = core.Formula((nleq, phi1, phi2))