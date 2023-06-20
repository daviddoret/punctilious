from unittest import TestCase

import punctilious as pu
import random_data


class TestInconsistencyIntroduction(TestCase):
    def test_inconsistency_introduction(self):
        u = pu.UniverseOfDiscourse('biconditional-elimination-left-universe')
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t('inconsistency-introduction-theory')
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        p = t.dai(u.f(r1, o1, o2), ap=ap)
        not_p = t.dai(u.f(u.r.lnot, u.f(r1, o1, o2)), ap=ap)
        inc = t.i.inconsistency_introduction.infer_statement(p, not_p, echo=True)
        # self.assertEqual('Inc(testing-theory)', phi3.repr())
        self.assertIs(pu.consistency_values.proved_inconsistent, t.consistency)
