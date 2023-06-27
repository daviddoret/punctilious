from unittest import TestCase
import punctilious as pu
import random_data


class TestFormula(TestCase):
    def test_formula(self):
        pu.configuration.text_format = pu.text_formats.plaintext
        pu.configuration.echo_default = None
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(1)
        r2 = u.r.declare(2)
        phi1 = u.f(r1, o1)
        self.assertEqual('r1(o1)', str(phi1.repr_formula()))
        self.assertEqual('r1(o1)', str(phi1.repr_formula(text_format=pu.text_formats.plaintext)))
        self.assertEqual('r₁(𝑜₁)', str(phi1.repr_formula(text_format=pu.text_formats.unicode)))
        self.assertEqual(
            r'\mathnormal{r}_{1}(\mathit{o}_{1})',
            str(phi1.repr_formula(text_format=pu.text_formats.latex_math)))
