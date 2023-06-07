from unittest import TestCase
import punctilious as p
import random_data


class TestSymbolicObjct(TestCase):
    def test__init__(self):
        u = p.UniverseOfDiscourse()
        t = u.t()
        with self.assertRaises(p.FailedVerificationException):
            u.o('')
        o1_symbol = random_data.random_word(3)
        o1 = u.o(o1_symbol)
        self.assertEqual(o1_symbol, o1.repr_as_symbol())
        self.assertIs(u, o1.universe_of_discourse)
        o2_symbol = random_data.random_word(3)
        o2 = u.o(o2_symbol)
        self.assertEqual(o2_symbol, o2.repr_as_symbol())
        self.assertIs(u, o2.universe_of_discourse)


class TestEquality(TestCase):
    def test_equality(self):
        t1 = core.TheoryElaboration(symbol='equality-test-theory', extended_theories={core.foundation_theory})
        a1 = core.NaturalLanguageAxiom(theory=t1, natural_language='Whatever I wish to be true is true.')
        mira = core.SimpleObjct(theory=t1, symbol='Mira', capitalizable=False)
        cat = core.SimpleObjct(theory=t1, symbol='cat', capitalizable=True)
        growls_at = core.Relation(theory=t1, symbol='growls-at', arity=2)
        snarls_at = core.Relation(theory=t1, symbol='snarls-at', arity=2)
        grows_equal_snarls_formula = core.Formula(theory=t1, relation=core.equality, parameters=(growls_at, snarls_at))
        grows_equal_snarls = core.FormalAxiom(theory=t1, axiom=a1,
                                              valid_proposition=grows_equal_snarls_formula)
        # snarls_equal_growls_formula = core.Formula(theory=t1, relation=core.foundation_theory.equal, parameters=(snarls_at, growls_at))
        p1 = core.ModusPonens(theory=t1, p_implies_q=core.commutativity_of_equality, p=grows_equal_snarls)
        # Mira_growls_at_cat = core.DirectAxiomInferenceStatement(theory=t1, axiom=a1,
        #    valid_proposition=core.Formula(theory=t1, relation=growls_at, parameters=(mira, cat)))
        t1.prnt()


class TestAxiom(TestCase):

    def test_init(self):
        t1 = core.TheoryElaboration()
        a1 = core.NaturalLanguageAxiom(theory=t1,
                                       natural_language='If something is red, then it is neither green, nor blue.')
        a2 = core.NaturalLanguageAxiom(theory=t1,
                                       natural_language='If something is green, then it is neither red, nor blue.')
        a3 = core.NaturalLanguageAxiom(theory=t1,
                                       natural_language='If something is blue, then it is neither red, nor green.')
        self.assertIs(t1, a1.theory)
        self.assertIs(t1, a2.theory)
        self.assertIs(t1, a3.theory)


class TestStatement(TestCase):

    def test_init(self):
        t1 = core.TheoryElaboration()
        a1 = core.NaturalLanguageAxiom(theory=t1, text='If something is red, then it is neither green, nor blue.')
        s1 = core.Statement(theory=t1, valid_proposition=a1)

        self.assertIs(t1, s1.theory)
        print(s1)


class TestFormula(TestCase):

    def test_init(self):
        t1 = core.TheoryElaboration()
        o11 = core.SimpleObjct(theory=t1)
        o12 = core.SimpleObjct(theory=t1)

        r_unary = core.Relation(theory=t1, arity=1)
        phi_unary = core.Formula(theory=t1, relation=r_unary, parameters=tuple([o11]))
        self.assertEqual('◆₁(ℴ₁)', phi_unary.repr(rep=core.Formula.frmts.prefix_operator))
        self.assertEqual('(ℴ₁)◆₁', phi_unary.repr(rep=core.Formula.frmts.suffix_operator))
        self.assertEqual('◆₁(ℴ₁)', phi_unary.repr(rep=core.Formula.frmts.function_call))
        self.assertEqual('𝜑₁', phi_unary.repr(rep=core.Formula.frmts.symbol))

        r_binary = core.Relation(theory=t1, arity=2)
        phi_binary = core.Formula(theory=t1, relation=r_binary, parameters=tuple([o11, o12]))
        self.assertEqual('◆₂(ℴ₁, ℴ₂)', phi_binary.repr(rep=core.Formula.frmts.function_call))
        self.assertEqual('(ℴ₁ ◆₂ ℴ₂)', phi_binary.repr(rep=core.Formula.frmts.infix_operator))
        self.assertEqual('𝜑₂', phi_binary.repr(rep=core.Formula.frmts.symbol))

    def test_str(self):
        self.fail()


class TestNote(TestCase):
    pass


class TestRelation(TestCase):
    def test_init(self):
        t1 = core.TheoryElaboration()
        r11 = core.Relation(theory=t1, arity=1)
        self.assertIs(t1, r11.theory)
        self.assertEqual(1, r11.arity)
        r12 = core.Relation(theory=t1, arity=2)
        self.assertIs(t1, r12.theory)
        self.assertEqual(2, r12.arity)
        r13 = core.Relation(theory=t1, arity=2)
        self.assertIs(t1, r13.theory)
        self.assertEqual(2, r13.arity)
        t2 = core.TheoryElaboration()
        r21 = core.Relation(theory=t2, arity=2)
        self.assertIs(t2, r21.theory)
        self.assertEqual(2, r21.arity)
        r22 = core.Relation(theory=t2, arity=1)
        self.assertIs(t2, r22.theory)
        self.assertEqual(1, r22.arity)
        r23 = core.Relation(theory=t2, arity=1)
        self.assertIs(t2, r23.theory)
        self.assertEqual(1, r23.arity)
        pass


class TestSimpleObjct(TestCase):
    def test_init(self):
        t1 = core.TheoryElaboration()
        o11 = core.SimpleObjct(theory=t1)
        o12 = core.SimpleObjct(theory=t1)
        o13 = core.SimpleObjct(theory=t1)
        t2 = core.TheoryElaboration()
        o21 = core.SimpleObjct(theory=t2)
        o22 = core.SimpleObjct(theory=t2)
        o23 = core.SimpleObjct(theory=t2)
        pass


class TestTheory(TestCase):
    def test___init__(self):
        t1 = core.TheoryElaboration(dashed='test-theory-1')
        a1 = core.NaturalLanguageAxiom(theory=t1, text='If a filooboo is wala, then it is sholo.')
        s1 = core.Statement(theory=t1, valid_proposition=a1)
        t1.print()


class TestTheoreticalObject(TestCase):
    def test_is_formula_equivalent_to(self):
        t1 = core.TheoryElaboration()
        o1 = core.SimpleObjct(theory=t1)
        o2 = core.SimpleObjct(theory=t1)
        r1 = core.Relation(theory=t1, arity=1)
        r2 = core.Relation(theory=t1, arity=1)
        r3 = core.Relation(theory=t1, arity=2)
        r4 = core.Relation(theory=t1, arity=2)
        # Test with unary relation.
        phi1 = core.Formula(theory=t1, relation=r1, parameters=tuple([o1]))
        self.assertTrue(phi1.is_formula_equivalent_to(phi1))
        phi2 = core.Formula(theory=t1, relation=r1, parameters=tuple([o1]))
        self.assertTrue(phi1.is_formula_equivalent_to(phi2))
        phi3 = core.Formula(theory=t1, relation=r2, parameters=tuple([o1]))
        self.assertFalse(phi1.is_formula_equivalent_to(phi3))
        phi4 = core.Formula(theory=t1, relation=r1, parameters=tuple([o2]))
        self.assertFalse(phi1.is_formula_equivalent_to(phi4))
        # Test with binary relation.
        phi5 = core.Formula(theory=t1, relation=r3, parameters=tuple([o1, o2]))
        self.assertTrue(phi5.is_formula_equivalent_to(phi5))
        phi6 = core.Formula(theory=t1, relation=r3, parameters=tuple([o1, o2]))
        self.assertTrue(phi5.is_formula_equivalent_to(phi6))
        phi7 = core.Formula(theory=t1, relation=r4, parameters=tuple([o1, o2]))
        self.assertFalse(phi5.is_formula_equivalent_to(phi7))
        phi8 = core.Formula(theory=t1, relation=r3, parameters=tuple([o2, o1]))
        self.assertFalse(phi5.is_formula_equivalent_to(phi8))

    def test_is_masked_variable_similar_to(self):
        t1 = core.TheoryElaboration()
        o1 = core.SimpleObjct(theory=t1)
        o2 = core.SimpleObjct(theory=t1)
        r1 = core.Relation(theory=t1, arity=1)
        r2 = core.Relation(theory=t1, arity=1)
        r3 = core.Relation(theory=t1, arity=2)
        r4 = core.Relation(theory=t1, arity=2)
        x1 = core.FreeVariable(theory=t1)
        x2 = core.FreeVariable(theory=t1)
        # Test with unary relation.
        phi1 = core.Formula(theory=t1, relation=r1, parameters=tuple([o1]))
        self.assertTrue(phi1.is_masked_formula_similar_to(o2=phi1))
        self.assertTrue(phi1.is_masked_formula_similar_to(o2=phi1, mask={x1, x2}))
        phi2 = core.Formula(theory=t1, relation=r1, parameters=tuple([o1]))
        self.assertTrue(phi1.is_masked_formula_similar_to(o2=phi2))
        self.assertTrue(phi1.is_masked_formula_similar_to(o2=phi2, mask={x1, x2}))
        phi3 = core.Formula(theory=t1, relation=r2, parameters=tuple([o1]))
        self.assertFalse(phi1.is_masked_formula_similar_to(o2=phi3))
        self.assertFalse(phi1.is_masked_formula_similar_to(o2=phi3, mask={x1, x2}))
        phi4 = core.Formula(theory=t1, relation=r1, parameters=tuple([o2]))
        self.assertFalse(phi1.is_masked_formula_similar_to(phi4))
        self.assertFalse(phi1.is_masked_formula_similar_to(phi4, mask={x1, x2}))
        phi21 = core.Formula(theory=t1, relation=x1, parameters=tuple([o1]))
        self.assertTrue(phi1.is_masked_formula_similar_to(o2=phi21, mask={x1}))
        self.assertFalse(phi1.is_masked_formula_similar_to(o2=phi21, mask={x2}))
        phi22 = core.Formula(theory=t1, relation=r1, parameters=tuple([x1]))
        self.assertTrue(phi1.is_masked_formula_similar_to(o2=phi22, mask={x1}))
        self.assertFalse(phi1.is_masked_formula_similar_to(o2=phi22, mask={x2}))

        # Test with binary relation.
        phi5 = core.Formula(theory=t1, relation=r3, parameters=tuple([o1, o2]))
        self.assertTrue(phi5.is_masked_formula_similar_to(o2=phi5))
        self.assertTrue(phi5.is_masked_formula_similar_to(o2=phi5, mask={x1, x2}))
        phi6 = core.Formula(theory=t1, relation=r3, parameters=tuple([o1, o2]))
        self.assertTrue(phi5.is_masked_formula_similar_to(o2=phi6))
        self.assertTrue(phi5.is_masked_formula_similar_to(o2=phi6, mask={x1, x2}))
        phi7 = core.Formula(theory=t1, relation=r4, parameters=tuple([o1, o2]))
        self.assertFalse(phi5.is_masked_formula_similar_to(o2=phi7))
        self.assertFalse(phi5.is_masked_formula_similar_to(o2=phi7, mask={x1, x2}))
        phi8 = core.Formula(theory=t1, relation=r3, parameters=tuple([o2, o1]))
        self.assertFalse(phi5.is_masked_formula_similar_to(o2=phi8))
        self.assertFalse(phi5.is_masked_formula_similar_to(o2=phi8, mask={x1, x2}))
        phi31 = core.Formula(theory=t1, relation=x1, parameters=tuple([o1, o2]))
        self.assertTrue(phi5.is_masked_formula_similar_to(o2=phi31, mask={x1}))
        self.assertFalse(phi5.is_masked_formula_similar_to(o2=phi31, mask={x2}))
        phi32 = core.Formula(theory=t1, relation=r3, parameters=tuple([x1, o2]))
        self.assertTrue(phi5.is_masked_formula_similar_to(o2=phi32, mask={x1}))
        self.assertFalse(phi5.is_masked_formula_similar_to(o2=phi32, mask={x2}))

    def test_substitute(self):
        t1 = core.TheoryElaboration()
        o1 = core.SimpleObjct(theory=t1)
        o2 = core.SimpleObjct(theory=t1)
        o3 = core.SimpleObjct(theory=t1)
        r1 = core.Relation(theory=t1, arity=2)
        r2 = core.Relation(theory=t1, arity=2)
        x1 = core.FreeVariable(theory=t1)
        x2 = core.FreeVariable(theory=t1)
        # Test with unary relation.
        phi1 = core.Formula(theory=t1, relation=r1, parameters=tuple([o1, o2]))
        # Substitute a parameter
        phi2 = phi1.substitute({o1: o3})
        phi2_expected = core.Formula(theory=t1, relation=r1, parameters=tuple([o3, o2]))
        self.assertTrue(phi2_expected.is_formula_equivalent_to(phi2))
        # Substitute a relation
        phi3 = phi1.substitute({r1: r2})
        phi3_expected = core.Formula(theory=t1, relation=r2, parameters=tuple([o1, o2]))
        self.assertTrue(phi3_expected.is_formula_equivalent_to(phi3))
        # Substitute with variables
        phi4 = phi1.substitute({r1: x1, o1: x2})
        phi4_expected = core.Formula(theory=t1, relation=x1, parameters=tuple([x2, o2]))
        self.assertTrue(phi4_expected.is_formula_equivalent_to(phi4))
