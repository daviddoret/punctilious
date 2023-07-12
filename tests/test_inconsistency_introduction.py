from unittest import TestCase

import punctilious as pu
import random_data


class TestInconsistencyIntroduction(TestCase):
    def test_inconsistency_introduction(self):
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        p = t.i.axiom_interpretation.infer_statement(ap, u.f(r1, o1, o2), echo=True)
        not_p = t.i.axiom_interpretation.infer_statement(ap, u.f(u.r.lnot, u.f(r1, o1, o2)),
                                                         echo=True)
        inc = t.i.inconsistency_introduction.infer_statement(p, not_p, echo=True)
        self.assertEqual('𝐼𝑛𝑐(𝒯₁)', inc.rep_formula(text_format=pu.encodings.unicode))
        self.assertIs(pu.consistency_values.proved_inconsistent, t.consistency)
