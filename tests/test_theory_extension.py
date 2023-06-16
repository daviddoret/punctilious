from unittest import TestCase
import punctilious as p
import random_data


class TestTheory(TestCase):
    def test_get_theory_chain(self):
        p.configuration.echo_default = True
        u = p.UniverseOfDiscourse()
        t1 = u.t()
        self.assertEqual({t1}, set(t1.iterate_theory_chain()))
        t2a = u.t(extended_theory=t1)
        t2b = u.t(extended_theory=t1)
        self.assertEqual({t1, t2a}, set(t2a.iterate_theory_chain()))
        self.assertEqual({t1, t2b}, set(t2b.iterate_theory_chain()))
        t3 = u.t(extended_theory=t2a)
        self.assertEqual({t1, t2a, t3}, set(t3.iterate_theory_chain()))

    def test_list_theoretical_objcts_recursively(self):
        p.configuration.echo_default = False
        u = p.UniverseOfDiscourse()
        t1 = u.t()
        self.assertEqual({t1}, set(t1.iterate_theoretical_objcts_references()))
        r1 = u.r.declare(2, signal_proposition=True)
        self.assertEqual({t1}, set(t1.iterate_theoretical_objcts_references()))
        r2 = u.r.declare(2, signal_proposition=True)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        f1 = u.f(r1, o1, o2)
        f2 = u.f(r1, o2, o3)
        f3 = u.f(r2, o3, f1)
        a1 = u.axiom(random_data.random_sentence())
        ap1 = t1.postulate_axiom(a1)
        t1.dai(f1, ap1)
        return None
        self.assertEqual({t1, r1, o1}, set(t1.iterate_theoretical_objcts_references()))
        limit = t1.dai(f2, ap1)
        t1.dai(f3, ap1)
        t2a = u.t(extended_theory=t1, extended_theory_limit=limit)
        t2b = u.t(extended_theory=t1)
        self.assertEqual({t1, t2a}, set(t2a.iterate_theoretical_objcts_references()))
        self.assertEqual({t1, t2b}, set(t2b.iterate_theoretical_objcts_references()))
        t2a.dai(f2, ap1)
        a2 = u._inference_rule(random_data.random_sentence())
        ap2 = t2a.postulate_axiom(a2)
        t2a.dai(f3, ap2)
        t3 = u.t(extended_theory=t2a)
        self.assertEqual({t1, t2a, t3}, set(t3.iterate_theoretical_objcts_references()))
