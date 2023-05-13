from unittest import TestCase
import core


def generate_test_theory():
    theory = core.Theory(dashed_name='test-theory')

    theory.append_objct(pyn='o1', sym='▼', dashed_name='filled-downward-triangle')
    theory.append_objct(pyn='o2', sym='●', dashed_name='filled-circle')
    theory.append_objct(pyn='o3', sym='◆', dashed_name='filled-diamond')
    theory.append_objct(pyn='o4', sym='▬', dashed_name='filled-rectangle')

    theory.append_relation(pyn='r1', sym='⬨', dashed_name='empty-lozenge', formula_str_fun=core.formula_str_funs.infix)
    theory.append_relation(pyn='r2', sym='⬭', dashed_name='empty-horizontal-ellipse',
                           formula_str_fun=core.formula_str_funs.function)
    theory.append_relation(pyn='r3', sym='▱', dashed_name='empty-parallelogram',
                           formula_str_fun=core.formula_str_funs.infix)
    theory.append_relation(pyn='r4', sym='◻', dashed_name='empty-square', formula_str_fun=core.formula_str_funs.infix)

    theory.append_variable(pyn='X', sym='𝓧', dashed_name='big-x')
    theory.append_variable(pyn='Y', sym='𝓨', dashed_name='big-y')
    theory.append_variable(pyn='Z', sym='𝓩', dashed_name='big-z')
    theory.append_variable(pyn='A', sym='𝓐', dashed_name='big-a')
    theory.append_variable(pyn='B', sym='𝓑', dashed_name='big-b')
    theory.append_variable(pyn='C', sym='𝓒', dashed_name='big-c')
    theory.append_variable(pyn='D', sym='𝓓', dashed_name='big-d')

    return theory


class Test(TestCase):
    def test_extract_subformula_by_flat_index(self):
        t = generate_test_theory()
        phi = t.assure_free_formula((t.r3, (t.r1, t.o1, t.o2), t.Y, (t.r2, t.o3, (t.r3, t.Z), t.X, t.Z), t.Y, t.o1))
        print(phi.str(str_fun=core.formula_str_funs.formal))
        print(core.extract_subformula_by_flat_index(phi=phi, n=4))


    def test_unpack(self):
        t = generate_test_theory()
        phi = t.assure_free_formula((t.r1, t.o1, t.o2))
        tup = core.unpack(phi)
        assert(isinstance(phi, core.FreeFormula))
        assert (isinstance(tup, tuple))


