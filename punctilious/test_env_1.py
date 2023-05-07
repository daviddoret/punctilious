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
        self.assertTrue(object_1.cat == core.cats.objct)

        object_2_dashed_name = 'filled-circle'
        object_2_sym = '●'
        object_2 = theory.append_objct(sym=object_2_sym, dashed_name=object_2_dashed_name)
        self.assertTrue(object_2.sym == object_2_sym)
        self.assertTrue(object_2.dashed_name == object_2_dashed_name)
        self.assertTrue(object_2.cat == core.cats.objct)

        relation_1_sym = '⬨'
        relation_1_dashed_name = 'empty-lozenge'
        relation_1 = theory.append_relation(sym=relation_1_sym, dashed_name=relation_1_dashed_name,
                                            formula_str_fun=core.formula_str_funs.infix)
        self.assertTrue(relation_1.sym == relation_1_sym)
        self.assertTrue(relation_1.dashed_name == relation_1_dashed_name)
        self.assertTrue(relation_1.cat == core.cats.relation)

        relation_2_sym = '⬭'
        relation_2_dashed_name = 'empty-horizontal-ellipse'
        relation_2 = theory.append_relation(sym=relation_2_sym, dashed_name=relation_2_dashed_name,
                                            formula_str_fun=core.formula_str_funs.function)
        self.assertTrue(relation_2.sym == relation_2_sym)
        self.assertTrue(relation_2.dashed_name == relation_2_dashed_name)
        self.assertTrue(relation_2.cat == core.cats.relation)

        relation_3 = theory.append_relation(sym='▱', dashed_name='empty-parallelogram', formula_str_fun=core.formula_str_funs.infix)
        relation_4 = theory.append_relation(sym='◻', dashed_name='empty-square', formula_str_fun=core.formula_str_funs.infix)

        variable_1_sym = '𝓧'
        variable_1_dashed_name = 'big-x'
        variable_1 = theory.append_variable(sym=variable_1_sym, dashed_name=variable_1_dashed_name)
        self.assertTrue(variable_1.sym == variable_1_sym)
        self.assertTrue(variable_1.dashed_name == variable_1_dashed_name)
        self.assertTrue(variable_1.cat == core.cats.variable)

        variable_2_sym = '𝓨'
        variable_2_dashed_name = 'big-y'
        variable_2 = theory.append_variable(sym=variable_2_sym, dashed_name=variable_2_dashed_name)
        self.assertTrue(variable_2.sym == variable_2_sym)
        self.assertTrue(variable_2.dashed_name == variable_2_dashed_name)
        self.assertTrue(variable_2.cat == core.cats.variable)

        phi_1 = theory.assure_free_formula(phi=object_1)
        self.assertTrue(phi_1.str(str_fun=core.formula_str_funs.formal) == '(▼)')
        phi_1b = theory.assure_free_formula(phi=(object_1))
        self.assertTrue(phi_1 is phi_1b, msg='unicity of leaf free-formula')

        phi_2 = theory.assure_free_formula(phi=(relation_1, object_1, object_2))
        self.assertTrue(phi_2.str(str_fun=core.formula_str_funs.formal) == '((⬨), (▼), (●))')
        phi_3 = theory.assure_free_formula(phi=(relation_2, object_2, object_1))
        phi_4 = theory.assure_free_formula(phi=(relation_3, phi_2, phi_3))
        phi_4b = theory.assure_free_formula(phi=(relation_3, (relation_1, object_1, object_2), (relation_2, object_2, object_1)))
        self.assertTrue(phi_4 is phi_4b, msg='unicity of non-leaf free-formula')

        self.assertTrue(core.anti_variable_equal_to(
            phi=(object_1),
            psi=(object_1)),
            msg='anti-variable-equality of leaf free-formula')
        self.assertFalse(core.anti_variable_equal_to(
            phi=(object_1),
            psi=(object_2)),
            msg='anti-variable-inequality of leaf free-formula')
        self.assertTrue(core.anti_variable_equal_to(
            phi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_2, object_1)),
            psi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_2, object_1))),
            msg='anti-variable-equality of non-leaf free-formula')
        self.assertFalse(core.anti_variable_equal_to(
            phi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_2, object_1)),
            psi=(relation_1, (relation_2, object_1, object_2), (relation_3, object_1, object_2))),
            msg='anti-variable-inequality of non-leaf free-formula')
