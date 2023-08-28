from unittest import TestCase
import punctilious as pu
import random_data


class TestBiconditionalEliminationLeft(TestCase):
    def test_bel(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(arity=2, nameset='r', signal_proposition=True)
        r2 = u.r.declare(arity=1, nameset='r', signal_proposition=True)
        t = u.t()
        a1 = u.declare_axiom(random_data.random_sentence())
        a2 = t.include_axiom(a1)
        p1 = t.i.axiom_interpretation.infer_statement(a2,
            u.f(u.r.biconditional, u.f(r1, o1, o2), u.f(r2, o3)))
        self.assertEqual('(r1(o1, o2) <==> r2(o3))', p1.rep_formula(pu.encodings.plaintext))
        p2_bel = t.i.bel.infer_statement(p_iff_q=p1, echo=True)
        self.assertEqual('(r1(o1, o2) ==> r2(o3))', p2_bel.rep_formula(pu.encodings.plaintext))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ⟹ 𝑟₂(𝑜₃))', p2_bel.rep_formula(pu.encodings.unicode))
