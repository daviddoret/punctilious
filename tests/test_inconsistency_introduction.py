from unittest import TestCase

import punctilious as p
import random_data


class TestInconsistencyIntroduction(TestCase):
    def test_inconsistency_introduction(self):
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        r1 = u.r(2, signal_proposition=True)
        r2 = u.r(1, signal_proposition=True)
        t = u.t(
            'testing-theory',
            include_inconsistency_introduction_inference_rule=True)
        a = t.a('The arbitrary axiom of testing.')
        phi1 = t.dai(u.f(r1, o1, o2), a=a)
        phi2 = t.dai(u.f(u.nt, u.f(r1, o1, o2)), a=a)
        with self.assertWarns(p.InconsistencyWarning):
            phi3 = t.ii(phi1, phi2)
        self.assertEqual('Inc(testing-theory)', phi3.repr())
