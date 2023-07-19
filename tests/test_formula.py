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
        r1 = u.r.declare(arity=1, formula_rep=pu.Formula.function_call)
        r2 = u.r.declare(arity=1, formula_rep=pu.Formula.prefix)
        r3 = u.r.declare(arity=1, formula_rep=pu.Formula.postfix)
        r4 = u.r.declare(arity=2, formula_rep=pu.Formula.function_call)
        phi1 = u.f(r1, o1)
        phi2 = u.f(r2, o1)
        phi3 = u.f(r3, o1)
        phi4 = u.f(r4, o1, o2)
        self.assertEqual('r1(o1)', str(phi1.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('𝑟₁(𝑜₁)', str(phi1.rep_formula(encoding=pu.encodings.unicode)))
        self.assertEqual(
            '\\mathit{r}_{1}\\left(\\mathit{o}_{1}\\right)',
            str(phi1.rep_formula(encoding=pu.encodings.latex_math)))
        self.assertEqual('r2(o1)', str(phi2.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('𝑟₂(𝑜₁)', str(phi2.rep_formula(encoding=pu.encodings.unicode)))
        self.assertEqual(
            '\\mathit{r}_{2}\\left(\\mathit{o}_{1}\\right)',
            str(phi2.rep_formula(encoding=pu.encodings.latex_math)))
        self.assertEqual('(o1)r3', str(phi3.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('(𝑜₁)𝑟₃', str(phi3.rep_formula(encoding=pu.encodings.unicode)))
        self.assertEqual(
            '\\left(\\mathit{o}_{1}\\right)\\mathit{r}_{3}',
            str(phi3.rep_formula(encoding=pu.encodings.latex_math)))
        self.assertEqual('r4(o1, o2)', str(phi4.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('𝑟₄(𝑜₁, 𝑜₂)', str(phi4.rep_formula(encoding=pu.encodings.unicode)))
        self.assertEqual(
            '\\mathit{r}_{4}\\left(\\mathit{o}_{1}, \\mathit{o}_{2}\\right)',
            str(phi4.rep_formula(encoding=pu.encodings.latex_math)))
