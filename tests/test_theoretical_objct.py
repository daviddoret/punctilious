from unittest import TestCase
import punctilious as p
import random_data


class TestTheoreticalObjct(TestCase):
    def test_list_theoretical_objcts_recursively(self):
        u = p.UniverseOfDiscourse()
        t = u.t()
        r1 = u.r(1)
        self.assertEqual({r1}, r1.list_theoretical_objcts_recursively())
        r2 = u.r(2)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        a = u.axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        f1 = u.f(r1, o1)
        self.assertEqual({f1, r1, o1}, f1.list_theoretical_objcts_recursively())
        f2 = u.f(r1, o3)
        f3 = u.f(r2, f1, f2)
        self.assertEqual({f1, f2, f3, r1, r2, o1, o3}, f3.list_theoretical_objcts_recursively())

    def test_list_relations_recursively(self):
        u = p.UniverseOfDiscourse()
        t = u.t()
        r1 = u.r(1)
        self.assertEqual({r1}, r1.list_relations_recursively())
        r2 = u.r(2)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        a = u.axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        f1 = u.f(r1, o1)
        self.assertEqual({r1}, f1.list_relations_recursively())
        f2 = u.f(r1, o3)
        f3 = u.f(r2, f1, f2)
        self.assertEqual({r1, r2}, f3.list_relations_recursively())
