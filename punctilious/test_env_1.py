import core

theory = core.Theory(dashed_name='test-environment-1-theory')

object_1_dashed_name = 'black-downward-triangle'
object_1_sym = '▼'
object_1 = theory.append_objct(sym=object_1_sym, dashed_name=object_1_dashed_name)

object_2_dashed_name = 'black-circle'
object_2_sym = '●'
object_2 = theory.append_objct(sym=object_2_sym, dashed_name=object_2_dashed_name)

relation_1_sym = '⬨'
relation_1_dashed_name = 'white-lozenge'
relation_1 = theory.append_relation(sym=relation_1_sym, dashed_name=relation_1_dashed_name,
                                    formula_str_fun=core.formula_str_funs.infix)
relation_2_sym = '⬭'
relation_2_dashed_name = 'white-horizontal-ellipse'
relation_2 = theory.append_relation(sym=relation_2_sym, dashed_name=relation_2_dashed_name,
                                    formula_str_fun=core.formula_str_funs.function)

phi_1 = theory.assure_free_formula()