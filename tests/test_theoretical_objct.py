from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestTheoreticalObjct(TestCase):
    def test_list_theoretical_objcts_recursively(self):
        u = pu.UniverseOfDiscourse()
        t = u.t()
        r1 = u.r.declare(1)
        self.assertEqual({r1}, set(r1.iterate_theoretical_objcts_references()))
        r2 = u.r.declare(2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        f1 = u.f(r1, o1)
        self.assertEqual({f1, r1, o1}, set(f1.iterate_theoretical_objcts_references()))
        f2 = u.f(r1, o3)
        f3 = u.f(r2, f1, f2)
        self.assertEqual({f1, f2, f3, r1, r2, o1, o3},
                         set(f3.iterate_theoretical_objcts_references()))

    def test_list_relations_recursively(self):
        u = pu.UniverseOfDiscourse()
        t = u.t()
        r1 = u.r.declare(1)
        self.assertEqual({r1}, set(r1.iterate_relations()))
        r2 = u.r.declare(2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        f1 = u.f(r1, o1)
        self.assertEqual({r1}, set(f1.iterate_relations()))
        f2 = u.f(r1, o3)
        f3 = u.f(r2, f1, f2)
        self.assertEqual({r1, r2}, set(f3.iterate_relations()))

    def test_get_variable_ordered_set_1(self):
        u = pu.UniverseOfDiscourse()
        r = u.r.declare(2)
        with u.v('x') as x, u.v('y') as y, u.v('z') as z, u.v('a') as a, u.v('b') as b, u.v(
                'c') as c:
            phi1 = u.f(r, b, u.f(r, z, u.f(x, y, u.f(a, a, z))), echo=True)
            oset1 = phi1.get_variable_ordered_set()
            self.assertEqual((b, z, x, y, a), oset1)
            phi2 = u.f(r, a, u.f(y, y, u.f(z, b, u.f(r, c, z))), echo=True)
            oset2 = phi2.get_variable_ordered_set()
            self.assertEqual((a, y, z, b, c), oset2)
