import core

theory = core.Theory(dashed_name='test-environment-1-theory')

object_1_dashed_name = 'filled-downward-triangle'
object_1_sym = '▼'
object_1 = theory.append_objct(sym=object_1_sym, dashed_name=object_1_dashed_name)

object_2_dashed_name = 'filled-circle'
object_2_sym = '●'
object_2 = theory.append_objct(sym=object_2_sym, dashed_name=object_2_dashed_name)

relation_1_sym = '⬨'
relation_1_dashed_name = 'empty-lozenge'
relation_1 = theory.append_relation(sym=relation_1_sym, dashed_name=relation_1_dashed_name,
                                    formula_str_fun=core.formula_str_funs.infix)
relation_2_sym = '⬭'
relation_2_dashed_name = 'empty-horizontal-ellipse'
relation_2 = theory.append_relation(sym=relation_2_sym, dashed_name=relation_2_dashed_name,
                                    formula_str_fun=core.formula_str_funs.function)

variable_1_sym = '𝓧'
variable_1_dashed_name = 'big-x'
variable_1 = theory.append_variable(sym=variable_1_sym, dashed_name=variable_1_dashed_name)
variable_2_sym = '𝓨'
variable_2_dashed_name = 'big-y'
variable_2 = theory.append_variable(sym=variable_2_sym, dashed_name=variable_2_dashed_name)

phi_1 = theory.assure_free_formula(phi=object_1)
phi_1b = theory.assure_free_formula(phi=(object_1))

phi_2 = theory.assure_free_formula(phi=(relation_1, object_1, object_2))
print('hello')