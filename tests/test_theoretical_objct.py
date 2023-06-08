from unittest import TestCase
import punctilious as p
import random_data


class TestTheoreticalObjct(TestCase):
    def test_list_theoretical_objcts_recursively(self):
        u = p.UniverseOfDiscourse()
        t = u.t()
        r1 = u.r(1)
        self.assertEqual({r1}, set(r1.iterate_theoretical_objcts()))
        r2 = u.r(2)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        a = u.axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        f1 = u.f(r1, o1)
        self.assertEqual({f1, r1, o1}, set(f1.iterate_theoretical_objcts()))
        f2 = u.f(r1, o3)
        f3 = u.f(r2, f1, f2)
        self.assertEqual({f1, f2, f3, r1, r2, o1, o3}, set(f3.iterate_theoretical_objcts()))

    def test_list_relations_recursively(self):
        u = p.UniverseOfDiscourse()
        t = u.t()
        r1 = u.r(1)
        self.assertEqual({r1}, set(r1.iterate_relations()))
        r2 = u.r(2)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        a = u.axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        f1 = u.f(r1, o1)
        self.assertEqual({r1}, set(f1.iterate_relations()))
        f2 = u.f(r1, o3)
        f3 = u.f(r2, f1, f2)
        self.assertEqual({r1, r2}, set(f3.iterate_relations()))
