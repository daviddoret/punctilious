from unittest import TestCase

import punctilious as p
import random_data


class TestInconsistencyIntroduction(TestCase):
    def test_inconsistency_introduction(self):
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t(
            'testing-theory',
            include_inconsistency_introduction_inference_rule=True)
        a = u.axiom('The arbitrary axiom of testing.')
        ap = t.postulate_axiom(a)
        phi1 = t.dai(u.f(r1, o1, o2), ap=ap)
        phi2 = t.dai(u.f(u.r.lnot, u.f(r1, o1, o2)), ap=ap)
        with self.assertWarns(p.InconsistencyWarning):
            phi3 = t.ii(phi1, phi2)
        self.assertEqual('Inc(testing-theory)', phi3.repr())
