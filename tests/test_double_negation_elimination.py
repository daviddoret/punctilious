from unittest import TestCase
import punctilious as pu
import random_data


class TestDoubleNegationElimination(TestCase):
    def test_dne(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi0 = (o1 | r1 | o2)
        phi67 = u.r.lnot((o1 | r1 | o2))
        phi99 = u.r.lnot(u.r.lnot((o1 | r1 | o2)))
        phi1 = t.i.axiom_interpretation.infer_statement(ap, u.r.lnot(u.r.lnot((o1 | r1 | o2))))
        self.assertEqual('not(not(r1(o1, o2)))', phi1.rep_formula(pu.encodings.plaintext))
        self.assertEqual('¬(¬(𝑟₁(𝑜₁, 𝑜₂)))', phi1.rep_formula(pu.encodings.unicode))
        phi2 = t.i.dne.infer_statement(not_not_p=u.r.lnot(u.r.lnot((o1 | r1 | o2))))
        self.assertTrue(phi2.is_formula_syntactically_equivalent_to(o1 | r1 | o2))
        self.assertEqual('r1(o1, o2)', phi2.rep_formula(pu.encodings.plaintext))
        self.assertEqual('𝑟₁(𝑜₁, 𝑜₂)', phi2.rep_formula(pu.encodings.unicode))
