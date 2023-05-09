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

        relation_3 = theory.append_relation(sym='▱', dashed_name='empty-parallelogram', formula_str_fun=core.formula_str_funs.infix)
        relation_4 = theory.append_relation(sym='◻', dashed_name='empty-square', formula_str_fun=core.formula_str_funs.infix)

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
        self.assertTrue(phi_1.str(str_fun=core.formula_str_funs.formal) == '(▼)', msg='formal representation of leaf free-formula')
        phi_1b = theory.assure_free_formula(phi=(object_1))
        self.assertTrue(phi_1 is phi_1b, msg='unicity of leaf free-formula')
        self.assertTrue(core.formula_variable_equivalence(phi_1, phi_1), msg='formula variable-equivalence')
        self.assertTrue(core.formula_variable_equivalence(phi_1, phi_1b), msg='formula variable-equivalence')

        phi_2 = theory.assure_free_formula(phi=(relation_1, object_1, object_2))
        self.assertTrue(phi_2.str(str_fun=core.formula_str_funs.formal) == '((⬨), (▼), (●))')
        self.assertFalse(core.formula_variable_equivalence(phi_1, phi_2), msg='formula variable-equivalence')

        phi_3 = theory.assure_free_formula(phi=(relation_2, object_2, object_1))
        phi_4 = theory.assure_free_formula(phi=(relation_3, phi_2, phi_3))
        phi_4b = theory.assure_free_formula(phi=(relation_3, (relation_1, object_1, object_2), (relation_2, object_2, object_1)))
        self.assertTrue(phi_4 is phi_4b, msg='unicity of non-leaf free-formula')
        self.assertTrue(core.formula_variable_equivalence(phi_4, phi_4b), msg='formula variable-equivalence')

        # Anti-variable equality and anti-variable inequality of free-formula

        self.assertTrue(core.formula_equality_by_variable_symbols(
            phi=(object_1),
            psi=(object_1)),
            msg='anti-variable-equality of leaf free-formula')
        self.assertFalse(core.formula_equality_by_variable_symbols(
            phi=(object_1),
            psi=(object_2)),
            msg='anti-variable-inequality of leaf free-formula')
        self.assertTrue(core.formula_equality_by_variable_symbols(
            phi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_2, object_1)),
            psi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_2, object_1))),
            msg='anti-variable-equality of non-leaf free-formula')
        self.assertFalse(core.formula_equality_by_variable_symbols(
            phi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_2, object_1)),
            psi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_1, object_2))),
            msg='anti-variable-inequality of non-leaf free-formula')

        # Formula with variables
        phi_10 = theory.assure_free_formula((relation_1, variable_big_x, object_1))
        phi_11 = theory.assure_free_formula((relation_1, variable_big_y, object_1))
        phi_12 = theory.assure_free_formula((relation_1, object_1, variable_big_y))
        self.assertTrue(core.formula_variable_equivalence(phi_10, phi_11))
        self.assertFalse(core.formula_variable_equivalence(phi_10, phi_12))

        print('phi-20: formula-variable-equivalence')

        phi_20_tup = (relation_1, variable_big_x, (relation_1, variable_big_x, variable_big_y))
        self.assertEqual(str(core.formula_component_count(phi_20_tup)), '{⬨: 2, 𝓧: 2, 𝓨: 1}')
        phi_21_tup = (relation_1, variable_big_b, (relation_1, variable_big_b, variable_big_a))
        self.assertEqual(str(core.formula_component_count(phi_21_tup)), '{⬨: 2, 𝓑: 2, 𝓐: 1}')
        self.assertTrue(core.formula_variable_equivalence(phi_20_tup, phi_20_tup))
        self.assertFalse(core.formula_variable_equivalence(phi_20_tup, phi_11))

        print('phi-30: variable extraction')

        phi_30_input = theory.assure_free_formula((relation_1, object_1))  # , object_2, variable_big_z))
        self.assertEqual(str(core.formula_component_count(phi_30_input)), '{⬨: 1, ▼: 1}')  # , ●: 1, 𝓩: 1}')
        phi_30_mask = theory.assure_free_formula((relation_1, variable_big_x))  # , variable_big_y, variable_big_z))
        self.assertEqual(str(core.formula_component_count(phi_30_mask)), '{⬨: 1, 𝓧: 1}')  # , ●: 1, 𝓩: 1}')
        phi_30_map_variable_set = frozenset([variable_big_x])  # , variable_big_y])

        # Step 1: confirm compatibility of the mask with the input,
        #   considering a set of variables V. And retrieve the variable values.
        compatibility, var_values = core.extract_variable_values_from_formula(phi=phi_30_input, mask=phi_30_mask, variable_set=phi_30_map_variable_set)
        self.assertTrue(compatibility, msg='compatibility of mask with input formula')
        print(var_values)

        # Step 2: create a new formula as a copy of the template,
        #   where variables are replaced by their values.
        phi_30_template = theory.assure_free_formula((relation_2, variable_big_y, variable_big_x))
        compatibility, phi_30_output = core.transform_formula(phi=phi_30_input, mask=phi_30_mask, variable_set=phi_30_map_variable_set, template=phi_30_template)

        print('phi-40: component substitutions')

        phi_40_a = theory.assure_free_formula((relation_1, object_1, variable_big_x, object_2, relation_2 ,object_1 ,variable_big_x, variable_big_y, variable_big_z))
        self.assertEqual('((⬨), (▼), (𝓧), (●), (⬭), (▼), (𝓧), (𝓨), (𝓩))', phi_40_a.str())
        phi_40_b = core.substitute_formula_components(phi=phi_40_a, substitutions={object_1: object_2})
        REPRENDRE ICI LE MECANISME DE SUBSTITUTION SIMPLE
        print(phi_40_b)
        pass
