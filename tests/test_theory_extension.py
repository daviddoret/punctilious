from unittest import TestCase
import punctilious as p
import random_data


class TestTheory(TestCase):
    def test_list_theory_extension(self):
        p.configuration.echo_default = True
        u = p.UniverseOfDiscourse()
        t1 = u.t()
        r1 = u.r(2, signal_proposition=True)
        r2 = u.r(2, signal_proposition=True)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        f1 = u.f(r1, o1, o2)
        f2 = u.f(r1, o2, o3)
        f3 = u.f(r2, o3, f1)
        a1 = u.axiom(random_data.random_sentence())
        ap1 = t1.postulate_axiom(a1)
        t1.dai(f1, ap1)
        t2 = u.t(extended_theory=t1)
        t2.dai(f2, ap1)
        a2 = u.axiom(random_data.random_sentence())
        ap2 = t2.postulate_axiom(a2)
        t2.dai(f3, ap2)
