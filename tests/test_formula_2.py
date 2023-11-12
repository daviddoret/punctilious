from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestTheoreticalObjct(TestCase):
    def test_list_theoretical_objcts_recursively(self):
        u = pu.UniverseOfDiscourse()
        t = u.declare_theory()
        r1 = u.c1.declare(1)
        self.assertEqual({r1}, set(r1.iterate_theoretical_objcts_references()))
        r2 = u.c1.declare(2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        a = u.a.declare(random_data.random_sentence())
        ap = t.include_axiom(a)
        f1 = u.declare_compound_formula(r1, o1)
        self.assertEqual({f1, r1, o1}, set(f1.iterate_theoretical_objcts_references()))
        f2 = u.declare_compound_formula(r1, o3)
        f3 = u.declare_compound_formula(r2, f1, f2)
        self.assertEqual({f1, f2, f3, r1, r2, o1, o3}, set(f3.iterate_theoretical_objcts_references()))

    def test_list_connectives_recursively(self):
        u = pu.UniverseOfDiscourse()
        t = u.declare_theory()
        r1 = u.c1.declare(1)
        self.assertEqual({r1}, set(r1.iterate_connectives()))
        r2 = u.c1.declare(2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        a = u.a.declare(random_data.random_sentence())
        ap = t.include_axiom(a)
        f1 = u.declare_compound_formula(r1, o1)
        self.assertEqual({r1}, set(f1.iterate_connectives()))
        f2 = u.declare_compound_formula(r1, o3)
        f3 = u.declare_compound_formula(r2, f1, f2)
        self.assertEqual({r1, r2}, set(f3.iterate_connectives()))

    def test_get_variable_ordered_set_1(self):
        u = pu.UniverseOfDiscourse()
        r = u.c1.declare(2)
        with u.with_variable('x') as x, u.with_variable('y') as y, u.with_variable('z') as z, u.with_variable(
            'a') as a, u.with_variable('b') as b, u.with_variable('c') as c:
            phi1 = u.declare_compound_formula(r, b,
                u.declare_compound_formula(r, z, u.declare_compound_formula(x, y, u.declare_compound_formula(a, a, z))),
                echo=True)
            oset1 = pu.get_formula_unique_variable_ordered_set(u=u, phi=phi1)
            self.assertEqual((b, z, x, y, a), oset1)
            phi2 = u.declare_compound_formula(r, a,
                u.declare_compound_formula(y, y, u.declare_compound_formula(z, b, u.declare_compound_formula(r, c, z))),
                echo=True)
            oset2 = pu.get_formula_unique_variable_ordered_set(u=u, phi=phi2)
            self.assertEqual((a, y, z, b, c), oset2)
