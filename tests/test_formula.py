from unittest import TestCase
import punctilious as pu
import random_data


class TestFormula(TestCase):
    def test_formula(self):
        pu.configuration.encoding = pu.encodings.plaintext
        pu.configuration.echo_default = None
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(1)
        r2 = u.r.declare(2)
        phi1 = u.f(r1, o1)
        self.assertEqual('r1(o1)', str(phi1.rep_formula()))
        self.assertEqual('r1(o1)', str(phi1.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('𝑟₁(𝑜₁)', str(phi1.rep_formula(encoding=pu.encodings.unicode)))
        self.assertEqual(
            '\\mathit{r}_{1}\\left(\\mathit{o}_{1}\\right(',
            str(phi1.rep_formula(encoding=pu.encodings.latex_math)))
