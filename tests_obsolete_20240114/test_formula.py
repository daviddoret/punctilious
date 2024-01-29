from unittest import TestCase
import punctilious as pu


class TestFormula(TestCase):
    def test_formula(self):
        pu.configuration.encoding = pu.encodings.plaintext
        pu.configuration.echo_default = None
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()

        r1 = u.c1.declare(arity=1, formula_rep=pu.CompoundFormula.function_call)
        phi1 = u.declare_compound_formula(r1, o1)
        self.assertEqual('r1(o1)', str(phi1.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('𝑟₁(𝑜₁)', str(phi1.rep_formula(encoding=pu.encodings.unicode_extended)))
        self.assertEqual('\\mathit{r}_{1}\\left(\\mathit{o}_{1}\\right)',
                         str(phi1.rep_formula(encoding=pu.encodings.latex)))

        r2 = u.c1.declare(arity=1, formula_rep=pu.CompoundFormula.prefix)
        phi2 = u.declare_compound_formula(r2, o1)
        self.assertEqual('r2(o1)', str(phi2.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('𝑟₂(𝑜₁)', str(phi2.rep_formula(encoding=pu.encodings.unicode_extended)))
        self.assertEqual('\\mathit{r}_{2}\\left(\\mathit{o}_{1}\\right)',
                         str(phi2.rep_formula(encoding=pu.encodings.latex)))

        r3 = u.c1.declare(arity=1, formula_rep=pu.CompoundFormula.postfix)
        phi3 = u.declare_compound_formula(r3, o1)
        self.assertEqual('(o1)r3', str(phi3.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('(𝑜₁)𝑟₃', str(phi3.rep_formula(encoding=pu.encodings.unicode_extended)))
        self.assertEqual('\\left(\\mathit{o}_{1}\\right)\\mathit{r}_{3}',
                         str(phi3.rep_formula(encoding=pu.encodings.latex)))

        r4 = u.c1.declare(arity=2, formula_rep=pu.CompoundFormula.function_call)
        phi4 = u.declare_compound_formula(r4, o1, o2)
        self.assertEqual('r4(o1, o2)', str(phi4.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('𝑟₄(𝑜₁, 𝑜₂)', str(phi4.rep_formula(encoding=pu.encodings.unicode_extended)))
        self.assertEqual('\\mathit{r}_{4}\\left(\\mathit{o}_{1}, \\mathit{o}_{2}\\right)',
                         str(phi4.rep_formula(encoding=pu.encodings.latex)))

        r5 = u.c1.declare(arity=2, formula_rep=pu.CompoundFormula.infix)
        phi5 = u.declare_compound_formula(r5, o1, o2)
        self.assertEqual('(o1 r5 o2)', str(phi5.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('(𝑜₁ 𝑟₅ 𝑜₂)', str(phi5.rep_formula(encoding=pu.encodings.unicode_extended)))
        self.assertEqual('\\left(\\mathit{o}_{1} \\mathit{r}_{5} \\mathit{o}_{2}\\right)',
                         str(phi5.rep_formula(encoding=pu.encodings.latex)))

        r6 = u.c1.declare(arity=3, formula_rep=pu.CompoundFormula.function_call)
        phi6 = u.declare_compound_formula(r6, o1, o2, o1)
        self.assertEqual('r6(o1, o2, o1)', str(phi6.rep_formula(encoding=pu.encodings.plaintext)))
        self.assertEqual('𝑟₆(𝑜₁, 𝑜₂, 𝑜₁)', str(phi6.rep_formula(encoding=pu.encodings.unicode_extended)))

        r7 = u.c1.declare(formula_rep=pu.CompoundFormula.function_call)
        phi7 = u.declare_compound_formula(r7, o1, o2, o1, o3, o2, o1)
        self.assertEqual('r7(o1, o2, o1, o3, o2, o1)', str(phi7.rep_formula(encoding=pu.encodings.plaintext)))

        r8 = u.c1.declare(formula_rep=pu.CompoundFormula.collection)
        phi8 = u.declare_compound_formula(r8, o1, o2, o1, o3, o2, o1)
        self.assertEqual('(o1, o2, o1, o3, o2, o1)', str(phi8.rep_formula(encoding=pu.encodings.plaintext)))

        r9 = u.c1.declare(formula_rep=pu.CompoundFormula.collection, collection_start='{', collection_separator='; ',
                          collection_end='}')
        phi9 = u.declare_compound_formula(r9, o1, o2, o1, o3, o2, o1)
        self.assertEqual('{o1; o2; o1; o3; o2; o1}', str(phi9.rep_formula(encoding=pu.encodings.plaintext)))