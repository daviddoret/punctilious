from unittest import TestCase
import punctilious as p
import random_data


class TestModusPonens(TestCase):
    def test_modus_ponens(self):
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        o4 = u.o()
        r1 = u.r(2, signal_proposition=True)
        t = u.t('modus-ponens-test-theory',
                include_modus_ponens_inference_rule=True)
        t.include_modus_ponens_inference_rule()
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        with u.v() as x, u.v() as y, u.v() as z:
            implication = t.dai(
                u.f(
                    u.implies,
                    u.f(u.land, u.f(r1, x, y), u.f(r1, y, z)),
                    u.f(r1, x, z)),
                ap=ap)
        phi1 = t.dai(u.f(r1, o1, o2), ap=ap)
        phi2 = t.dai(u.f(r1, o2, o3), ap=ap)
        phi1_and_phi2 = t.ci(phi1, phi2)
        conclusion_1 = t.infer_by_modus_ponens(
            conditional=implication,
            antecedent=phi1_and_phi2)
        self.assertEqual('◆(ℴ₁, ℴ₃)', conclusion_1.valid_proposition.repr_as_formula())
