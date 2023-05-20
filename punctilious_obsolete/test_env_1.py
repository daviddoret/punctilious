from unittest import TestCase
import core


class TestPunctilious(TestCase):
    def test_env_1(self):
        theory = core.Theory(dashed_name='test-environment-1-theory')

        object_1_dashed_name = 'filled-downward-triangle'
        object_1_sym = '▼'
        object_1 = theory.append_objct(sym=object_1_sym, dashed_name=object_1_dashed_name)
        self.assertTrue(object_1.sym == object_1_sym)
        self.assertTrue(object_1.dashed_name == object_1_dashed_name)
        self.assertTrue(object_1.cat == core.cats.objct_decl)

        object_2_dashed_name = 'filled-circle'
        object_2_sym = '●'
        object_2 = theory.append_objct(sym=object_2_sym, dashed_name=object_2_dashed_name)
        self.assertTrue(object_2.sym == object_2_sym)
        self.assertTrue(object_2.dashed_name == object_2_dashed_name)
        self.assertTrue(object_2.cat == core.cats.objct_decl)

        object_3 = theory.append_objct(sym='◆', dashed_name='filled-diamond')
        object_4 = theory.append_objct(sym='▬', dashed_name='filled-rectangle')

        relation_1_sym = '⬨'
        relation_1_dashed_name = 'empty-lozenge'
        relation_1 = theory.append_relation(sym=relation_1_sym, dashed_name=relation_1_dashed_name,
                                            formula_str_fun=core.formula_str_funs.infix)
        self.assertTrue(relation_1.sym == relation_1_sym)
        self.assertTrue(relation_1.dashed_name == relation_1_dashed_name)
        self.assertTrue(relation_1.cat == core.cats.rel_decl)

        relation_2_sym = '⬭'
        relation_2_dashed_name = 'empty-horizontal-ellipse'
        relation_2 = theory.append_relation(sym=relation_2_sym, dashed_name=relation_2_dashed_name,
                                            formula_str_fun=core.formula_str_funs.function)
        self.assertTrue(relation_2.sym == relation_2_sym)
        self.assertTrue(relation_2.dashed_name == relation_2_dashed_name)
        self.assertTrue(relation_2.cat == core.cats.rel_decl)

        relation_3 = theory.append_relation(sym='▱', dashed_name='empty-parallelogram',
                                            formula_str_fun=core.formula_str_funs.infix)
        relation_4 = theory.append_relation(sym='◻', dashed_name='empty-square',
                                            formula_str_fun=core.formula_str_funs.infix)

        variable_big_x_sym = '𝓧'
        variable_big_x_dashed_name = 'big-x'
        variable_big_x = theory.append_variable(sym=variable_big_x_sym, dashed_name=variable_big_x_dashed_name)
        self.assertTrue(variable_big_x.sym == variable_big_x_sym)
        self.assertTrue(variable_big_x.dashed_name == variable_big_x_dashed_name)
        self.assertTrue(variable_big_x.cat == core.cats.var_decl)

        variable_big_y_sym = '𝓨'
        variable_big_y_dashed_name = 'big-y'
        variable_big_y = theory.append_variable(sym=variable_big_y_sym, dashed_name=variable_big_y_dashed_name)
        self.assertTrue(variable_big_y.sym == variable_big_y_sym)
        self.assertTrue(variable_big_y.dashed_name == variable_big_y_dashed_name)
        self.assertTrue(variable_big_y.cat == core.cats.var_decl)

        variable_big_z = theory.append_variable(sym='𝓩', dashed_name='big-z')
        variable_big_a = theory.append_variable(sym='𝓐', dashed_name='big-a')
        variable_big_b = theory.append_variable(sym='𝓑', dashed_name='big-b')
        variable_big_c = theory.append_variable(sym='𝓒', dashed_name='big-c')
        variable_big_d = theory.append_variable(sym='𝓓', dashed_name='big-d')

        phi_1 = theory.assure_free_formula(phi=object_1)
        self.assertEqual('(▼)', phi_1.repr(str_fun=core.formula_str_funs.formal),
                         msg='FreeFormula.str()')
        phi_1b = theory.assure_free_formula(phi=(object_1))
        self.assertIs(phi_1, phi_1b, msg='unicity of leaf free-formula')
        self.assertTrue(core.variable_equivalence(phi_1, phi_1), msg='formula_variable_equivalence()')
        self.assertTrue(core.variable_equivalence(phi_1, phi_1b), msg='formula_variable_equivalence()')
        phi_1c = core.substitute_subformula(phi=phi_1, substitutions={object_1: object_2})
        self.assertEqual('(●)', phi_1c.repr(str_fun=core.formula_str_funs.formal), msg='substitute_formula_components()')

        phi_2 = theory.assure_free_formula(phi=(relation_1, object_1, object_2))
        self.assertEqual('((⬨), (▼), (●))', phi_2.repr(str_fun=core.formula_str_funs.formal), msg='FreeFormula.str()')
        self.assertFalse(core.variable_equivalence(phi_1, phi_2), msg='formula_variable_equivalence()')
        phi_2a = core.substitute_subformula(phi=phi_2, substitutions={relation_1: relation_4, object_2: object_1})
        self.assertEqual('((◻), (▼), (▼))', phi_2a.repr(str_fun=core.formula_str_funs.formal), msg='substitute_formula_components()')

        phi_3 = theory.assure_free_formula(phi=(relation_2, object_2, object_1))
        phi_4 = theory.assure_free_formula(phi=(relation_3, phi_2, phi_3))
        phi_4b = theory.assure_free_formula(
            phi=(relation_3, (relation_1, object_1, object_2), (relation_2, object_2, object_1)))
        self.assertEqual('((▱), ((⬨), (▼), (●)), ((⬭), (●), (▼)))', phi_4b.repr(str_fun=core.formula_str_funs.formal), msg='FreeFormula.str()')
        self.assertTrue(phi_4 is phi_4b, msg='unicity of non-leaf free-formula')
        self.assertTrue(core.variable_equivalence(phi_4, phi_4b), msg='formula_variable_equivalence()')
        phi_4c = core.substitute_subformula(phi=phi_4b, substitutions={relation_1: relation_4, object_2: object_1, object_1: object_2})
        self.assertEqual('((▱), ((◻), (●), (▼)), ((⬭), (▼), (●)))', phi_4c.repr(str_fun=core.formula_str_funs.formal), msg='substitute_formula_components()')
        #self.assertEqual('((◻), (▼), (▼))', phi_2a.str(str_fun=core.formula_str_funs.formal), msg='substitute_formula_components')

        # Anti-variable equality and anti-variable inequality of free-formula

        self.assertTrue(core.name_equivalence(
            phi=(object_1),
            psi=(object_1)),
            msg='anti-variable-equality of leaf free-formula')
        self.assertFalse(core.name_equivalence(
            phi=(object_1),
            psi=(object_2)),
            msg='anti-variable-inequality of leaf free-formula')
        self.assertTrue(core.name_equivalence(
            phi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_2, object_1)),
            psi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_2, object_1))),
            msg='anti-variable-equality of non-leaf free-formula')
        self.assertFalse(core.name_equivalence(
            phi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_2, object_1)),
            psi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_1, object_2))),
            msg='anti-variable-inequality of non-leaf free-formula')

        # Formula with variables
        phi_10 = theory.assure_free_formula((relation_1, variable_big_x, object_1))
        phi_11 = theory.assure_free_formula((relation_1, variable_big_y, object_1))
        phi_12 = theory.assure_free_formula((relation_1, object_1, variable_big_y))
        self.assertTrue(core.variable_equivalence(phi_10, phi_11))
        self.assertFalse(core.variable_equivalence(phi_10, phi_12))

        print('phi-20: formula-variable-equivalence')

        phi_20_tup = (relation_1, variable_big_x, (relation_1, variable_big_x, variable_big_y))
        self.assertEqual(str(core.count_leafs(phi_20_tup)), '{⬨: 2, 𝓧: 2, 𝓨: 1}')
        phi_21_tup = (relation_1, variable_big_b, (relation_1, variable_big_b, variable_big_a))
        self.assertEqual(str(core.count_leafs(phi_21_tup)), '{⬨: 2, 𝓑: 2, 𝓐: 1}')
        self.assertTrue(core.variable_equivalence(phi_20_tup, phi_20_tup))
        self.assertFalse(core.variable_equivalence(phi_20_tup, phi_11))

        print('phi-30')

        phi_30_input = theory.assure_free_formula((relation_1, object_1))
        self.assertEqual(str(core.count_leafs(phi_30_input)), '{⬨: 1, ▼: 1}')
        phi_30_mask = theory.assure_free_formula((relation_1, variable_big_x))
        self.assertEqual(str(core.count_leafs(phi_30_mask)), '{⬨: 1, 𝓧: 1}')
        phi_30_map_variable_set = frozenset([variable_big_x])
        phi_30_compatibility, var_values = core.extract_variable_values(phi=phi_30_input, mask=phi_30_mask, variable_set=phi_30_map_variable_set)
        self.assertTrue(phi_30_compatibility, msg='extract_variable_values_from_formula(): compatibility')
        self.assertEqual('{𝓧: ▼}', str(var_values), msg='extract_variable_values_from_formula(): values')
        phi_30_template = theory.assure_free_formula((relation_2, variable_big_y, variable_big_x))
        phi_30_compatibility, phi_30_transformed = core.transform_formula(phi=phi_30_input, mask=phi_30_mask,
                                                              variable_set=phi_30_map_variable_set,
                                                              template=phi_30_template)
        self.assertTrue(phi_30_compatibility, msg='transform_formula()')
        self.assertEqual('((⬭), (𝓨), (▼))', str(phi_30_transformed), msg='transform_formula()')

        print('phi-40')

        phi_40_a = theory.assure_free_formula((relation_1, object_1, variable_big_x, object_2, relation_2, object_1,
                                               variable_big_x, variable_big_y, variable_big_z))
        self.assertEqual('((⬨), (▼), (𝓧), (●), (⬭), (▼), (𝓧), (𝓨), (𝓩))', phi_40_a.repr())
        phi_40_b = core.substitute_subformula(phi=phi_40_a, substitutions={object_1: object_2})
        self.assertEqual('((⬨), (●), (𝓧), (●), (⬭), (●), (𝓧), (𝓨), (𝓩))', phi_40_b.repr(), msg='substitute_formula_components()')
        pass
