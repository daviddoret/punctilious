from unittest import TestCase

import punctilious as pu
import random_data


class TestInconsistencyIntroduction2(TestCase):
    def test_inconsistency_introduction_2(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        t1 = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t1.include_axiom(a)
        p_eq_q = t1.i.axiom_interpretation.infer_statement(ap, u.f(u.r.eq, o1, o2))
        p_neq_q = t1.i.axiom_interpretation.infer_statement(ap, u.f(u.r.neq, o1, o2))
        t2 = u.t()
        inc = t2.i.inconsistency_introduction_1.infer_statement(p_eq_q=p_eq_q, p_neq_q=p_neq_q)
        self.assertEqual('𝐼𝑛𝑐(𝒯₁)', inc.rep_formula(encoding=pu.encodings.unicode))
        self.assertIs(pu.consistency_values.proved_inconsistent, t1.consistency)
