import pytest
import punctilious.axiomatic_system_1 as as1


@pytest.fixture
def c1():
    return as1.Connective(rep='c1')


@pytest.fixture
def c2():
    return as1.Connective(rep='c2')


@pytest.fixture
def c3():
    return as1.Connective(rep='c3')


@pytest.fixture
def fb1(c1):
    fb = as1.FormulaBuilder(c=c1)
    return fb


@pytest.fixture
def fb2(c2):
    fb = as1.FormulaBuilder(c=c2)
    return fb


@pytest.fixture
def fb3(c3):
    fb = as1.FormulaBuilder(c=c3)
    return fb


@pytest.fixture
def fb4(c1, c2, c3):
    fb1 = as1.FormulaBuilder(c=c1)
    n1_0 = fb1.append(term=c1)
    n1_0_0 = n1_0.append(term=c3)
    n1_0_1 = n1_0.append(term=c2)
    n1_1 = fb1.append(term=c2)
    n1_2 = fb1.append(term=c3)
    n1_2_0 = n1_2.append(term=c1)
    n1_2_0_0 = n1_2_0.append(term=c1)
    n1_2_0_0_0 = n1_2_0_0.append(term=c1)
    n1_2_0_0_1 = n1_2_0_0.append(term=c3)
    n1_2_0_1 = n1_2_0.append(term=c1)
    n1_2_1 = n1_2.append(term=c2)
    return fb1


@pytest.fixture
def fb5(c1, c2, c3):
    fb1 = as1.FormulaBuilder(c=c1)
    n1_0 = fb1.append(term=c1)
    n1_0_0 = n1_0.append(term=c3)
    n1_1 = fb1.append(term=c2)
    n1_2 = fb1.append(term=c3)
    n1_2_0 = n1_2.append(term=c1)
    n1_2_0_0 = n1_2_0.append(term=c1)
    n1_2_0_0_0 = n1_2_0_0.append(term=c1)
    n1_2_0_0_1 = n1_2_0_0.append(term=c3)
    n1_2_0_0_2 = n1_2_0_0.append(term=c1)
    n1_2_0_1 = n1_2_0.append(term=c1)
    n1_2_1 = n1_2.append(term=c2)
    return fb1


@pytest.fixture
def phi1(fb1):
    phi = fb1.to_formula()
    return phi


@pytest.fixture
def phi2(fb2):
    phi = fb2.to_formula()
    return phi


@pytest.fixture
def phi3(fb3):
    phi = fb3.to_formula()
    return phi


@pytest.fixture
def phi4(fb4):
    phi = fb4.to_formula()
    return phi


@pytest.fixture
def phi5(fb5):
    phi = fb5.to_formula()
    return phi


@pytest.fixture
def apple():
    return as1.let_x_be_a_simple_object(rep='apple')


@pytest.fixture
def ananas():
    return as1.let_x_be_a_simple_object(rep='ananas')


@pytest.fixture
def strawberry():
    return as1.let_x_be_a_simple_object(rep='strawberry')


@pytest.fixture
def blueberry():
    return as1.let_x_be_a_simple_object(rep='blueberry')


@pytest.fixture
def fruits(apple, ananas, blueberry, strawberry):
    fruits = as1.Enumeration(elements=(apple, ananas, blueberry, strawberry))
    return fruits


class TestConnective:
    def test_connective(self, c1, c2):
        assert c1 is not c2


class TestFormulaBuilder:
    def test_assure_term(self):
        fb = as1.FormulaBuilder()
        fb.assure_term(i=3)
        assert len(fb) == 4

    def test_formula_builder(self, c1, c2, c3, fb4):
        assert fb4.c is c1
        assert fb4[0].c is c1
        assert fb4[1].c is c2
        assert fb4[2].c is c3

    def test_term_0(self, c1, c2, c3):
        fb = as1.FormulaBuilder(c=c1)
        fb.term_0 = c2
        assert fb.c is c1
        assert fb[0].c is c2

    def test_terms(self, fb1, fb2, fb3):
        terms1 = as1.FormulaBuilder()
        assert len(terms1) == 0
        terms2 = as1.FormulaBuilder(terms=(fb1,))
        assert len(terms2) == 1
        assert terms2[0].c is fb1.c
        assert terms2.term_0.c is fb1.c
        terms3 = as1.FormulaBuilder(terms=(fb1, fb2, fb1, fb1, fb3))
        assert len(terms3) == 5
        assert terms3[0].c is fb1.c
        assert terms3.term_0.c is fb1.c
        assert terms3[1].c is fb2.c
        assert terms3.term_1.c is fb2.c
        assert terms3[2].c is fb1.c
        assert terms3[3].c is fb1.c
        assert terms3[4].c is fb3.c

    def test_to_formula(self, fb4):
        phi1 = fb4.to_formula()
        assert phi1.c is fb4.c
        assert phi1[0].c is fb4[0].c
        assert phi1[0][0].c is fb4[0][0].c
        assert phi1[0][1].c is fb4[0][1].c
        assert phi1[1].c is fb4[1].c
        assert phi1[2].c is fb4[2].c
        assert phi1[2][0].c is fb4[2][0].c
        assert phi1[2][0][0].c is fb4[2][0][0].c
        assert phi1[2][0][1].c is fb4[2][0][1].c
        assert phi1[2][1].c is fb4[2][1].c


class TestFormula:

    def test_formula(self, c1, c2, c3, phi4):
        assert phi4.c is c1
        assert phi4[0].c is c1
        assert phi4[1].c is c2
        assert phi4[2].c is c3

    def test_term_1(self, c1, c2, c3):
        fb = as1.FormulaBuilder()
        fb.term_0 = c1
        phi = fb.to_formula()
        assert phi.term_0.c is c1
        assert phi[0].c is c1

    def test_terms(self, c1, phi1, phi2, phi3):
        terms1 = as1.Formula(c=c1)
        assert len(terms1) == 0
        terms2 = as1.Formula(c=c1, terms=(phi1,))
        assert len(terms2) == 1
        assert terms2[0].c is phi1.c
        assert terms2.term_0.c is phi1.c
        terms3 = as1.Formula(c=c1, terms=(phi1, phi2, phi1, phi1, phi3))
        assert len(terms3) == 5
        assert terms3[0].c is phi1.c
        assert terms3.term_0.c is phi1.c
        assert terms3[1].c is phi2.c
        assert terms3.term_1.c is phi2.c
        assert terms3[2].c is phi1.c
        assert terms3[3].c is phi1.c
        assert terms3[4].c is phi3.c

    def test_to_formula_builder(self, phi4):
        fb1 = phi4.to_formula_builder()
        assert fb1.c is phi4.c
        assert fb1[0].c is phi4[0].c
        assert fb1[0][0].c is phi4[0][0].c
        assert fb1[0][1].c is phi4[0][1].c
        assert fb1[1].c is phi4[1].c
        assert fb1[2].c is phi4[2].c
        assert fb1[2][0].c is phi4[2][0].c
        assert fb1[2][0][0].c is phi4[2][0][0].c
        assert fb1[2][0][1].c is phi4[2][0][1].c
        assert fb1[2][1].c is phi4[2][1].c


class TestConnectiveEquivalence:
    def test_is_connective_equivalent(self):
        a = as1.let_x_be_a_simple_object(rep='a')
        b = as1.let_x_be_a_simple_object(rep='b')
        c = as1.let_x_be_a_simple_object(rep='c')
        c1 = as1.BinaryConnective(rep='c1')
        c2 = as1.BinaryConnective(rep='c2')
        phi = a | c1 | b
        assert as1.is_connective_equivalent(phi=phi, psi=phi)
        psi = b | c1 | c
        assert as1.is_connective_equivalent(phi=phi, psi=psi)
        omega = a | c2 | b
        assert not as1.is_connective_equivalent(phi=phi, psi=omega)


class TestFormulaEquivalence:
    def test_is_formula_equivalent(self, phi2, phi3, phi4, phi5):
        assert as1.is_formula_equivalent(phi=phi2, psi=phi2)
        assert as1.is_formula_equivalent(phi=phi3, psi=phi3)
        assert as1.is_formula_equivalent(phi=phi4, psi=phi4)
        assert as1.is_formula_equivalent(phi=phi5, psi=phi5)
        assert not as1.is_formula_equivalent(phi=phi2, psi=phi3)
        assert not as1.is_formula_equivalent(phi=phi3, psi=phi4)
        assert not as1.is_formula_equivalent(phi=phi4, psi=phi5)


class TestTupl:
    def test_tupl(self, phi1, phi2, phi3):
        cb1 = as1.TuplBuilder((phi1, phi2, phi3,))
        c1 = cb1.to_tupl()
        c2 = as1.Tupl((phi1, phi2, phi3,))
        assert as1.is_formula_equivalent(c1, c2)
        assert len(c1) == 3
        assert len(c2) == 3
        c3 = as1.Tupl()
        assert len(c3) == 0

    def test_in(self):
        x = as1.let_x_be_a_variable(rep='x')
        y = as1.let_x_be_a_variable(rep='y')
        c = as1.Tupl(elements=(x,))
        assert x in c
        assert y not in c
        assert len(c) == 1


class TestEnumeration:
    def test_tupl(self, phi1, phi2, phi3):
        cb1 = as1.EnumerationBuilder((phi1, phi2, phi3, phi1, phi3))
        e1 = cb1.to_enumeration()
        e2 = as1.Enumeration((phi1, phi2, phi3,))
        e3 = as1.Enumeration((phi3, phi1, phi2,))
        assert len(e1) == 3
        assert len(e2) == 3
        assert len(e3) == 3
        assert as1.is_enumeration_equivalent(e1, e2)
        assert as1.is_enumeration_equivalent(e1, e3)
        assert as1.is_enumeration_equivalent(e2, e3)
        e4 = as1.Enumeration((phi2, phi1,))
        assert not as1.is_enumeration_equivalent(e4, e1)
        assert not as1.is_enumeration_equivalent(e4, e2)
        assert not as1.is_enumeration_equivalent(e4, e3)

    def test_has_element(self):
        c1 = as1.let_x_be_a_binary_connective(rep='c1')
        c2 = as1.let_x_be_a_binary_connective(rep='c2')
        x = as1.let_x_be_a_simple_object(rep='x')
        y = as1.let_x_be_a_simple_object(rep='y')
        phi1 = x | c1 | y
        phi2 = x | c2 | y
        phi3 = y | c1 | x
        e1 = as1.Enumeration(elements=(phi1, phi2, phi3,))
        assert e1.has_element(phi=phi1)
        assert not e1.has_element(phi=x | c1 | x)
        phi1_other_instance = x | c1 | y
        assert e1.has_element(phi=phi1_other_instance)
        assert e1.get_element_index(phi=phi1) == 0
        assert e1.get_element_index(phi=phi2) == 1
        assert e1.get_element_index(phi=phi3) == 2

    def test_warning(self):
        a = as1.let_x_be_a_simple_object(rep='a')
        b = as1.let_x_be_a_simple_object(rep='b')
        c = as1.let_x_be_a_simple_object(rep='c')
        with pytest.warns(Warning) as record:
            # duplicate formula-equivalent formulas are ignored and raise a warning.
            e1 = as1.Enumeration(elements=(a, b, c, b,))
            if not record:
                pytest.fail(f'Warning {as1.ErrorCodes.e104} not issued.')


class TestFormulaEquivalenceWithVariables:
    def test_is_formula_equivalent_with_variables(self):
        x = as1.let_x_be_a_variable(rep='x')
        y = as1.let_x_be_a_variable(rep='y')
        is_a = as1.let_x_be_a_binary_connective(rep='is-a')
        human = as1.let_x_be_a_simple_object(rep='human')
        platypus = as1.let_x_be_a_simple_object(rep='platypus')
        mortal = as1.let_x_be_a_simple_object(rep='mortal')
        aristotle = as1.let_x_be_a_simple_object(rep='aristotle')
        assert as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | human,
            psi=aristotle | is_a | human,
            v=())
        # the following is ill-formed because the variable is an element of phi, and not of psi.
        # reminder: formula-equivalence-with-variables is non-commutative.
        assert not as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | x,
            psi=aristotle | is_a | human,
            v=(x,))
        assert as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | human,
            psi=aristotle | is_a | x,
            v=(x,))
        assert not as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | human,
            psi=aristotle | is_a | platypus,
            v=())
        assert not as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | x,
            psi=aristotle | is_a | human,
            v=(y,))
        assert not as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | x,
            psi=platypus | is_a | human,
            v=(x,))


class TestTransformation:
    def test_transformation(self):
        x = as1.let_x_be_a_variable(rep='x')
        y = as1.let_x_be_a_variable(rep='y')
        is_a = as1.let_x_be_a_binary_connective(rep='is-a')
        human = as1.let_x_be_a_simple_object(rep='human')
        platypus = as1.let_x_be_a_simple_object(rep='platypus')
        mortal = as1.let_x_be_a_simple_object(rep='mortal')
        aristotle = as1.let_x_be_a_simple_object(rep='aristotle')
        p1 = x | is_a | human
        p2 = aristotle | is_a | human
        premises = as1.Enumeration(elements=(p1,))
        conclusion = x | is_a | mortal
        variables = as1.Enumeration(elements=(x,))
        t = as1.Transformation(premises=premises, conclusion=conclusion, variables=variables)
        arguments = as1.Tupl(elements=(p2,))
        output = t.apply_transformation(arguments=arguments)
        as1.is_formula_equivalent(phi=aristotle | is_a | mortal, psi=output)


class TestReplaceFormulas:
    def test_replace_formulas(self):
        land = as1.let_x_be_a_binary_connective(rep='land')
        x = as1.let_x_be_a_variable(rep='x')
        y = as1.let_x_be_a_variable(rep='y')
        is_a = as1.let_x_be_a_binary_connective(rep='is-a')
        human = as1.let_x_be_a_simple_object(rep='human')
        animal = as1.let_x_be_a_simple_object(rep='animal')
        platypus = as1.let_x_be_a_simple_object(rep='platypus')
        mortal = as1.let_x_be_a_simple_object(rep='mortal')
        aristotle = as1.let_x_be_a_simple_object(rep='aristotle')
        assert as1.is_formula_equivalent(
            phi=as1.replace_formulas(phi=x | is_a | human, m={x: aristotle}),
            psi=aristotle | is_a | human)
        assert not as1.is_formula_equivalent(
            phi=as1.replace_formulas(phi=x | is_a | human, m={x: platypus}),
            psi=aristotle | is_a | human)
        phi = aristotle | is_a | human
        phi = as1.replace_formulas(phi=phi, m={human: aristotle})
        psi = aristotle | is_a | aristotle
        assert as1.is_formula_equivalent(
            phi=phi,
            psi=psi)
        omega1 = (aristotle | is_a | human) | land | (platypus | is_a | animal)
        omega2 = as1.replace_formulas(phi=omega1,
                                      m={human: aristotle})
        assert as1.is_formula_equivalent(
            phi=omega2,
            psi=(aristotle | is_a | aristotle) | land | (platypus | is_a | animal))


class TestMap:
    def test_map(self, fruits):
        red = as1.let_x_be_a_simple_object(rep='red')
        yellow = as1.let_x_be_a_simple_object(rep='yellow')
        blue = as1.let_x_be_a_simple_object(rep='blue')
        codomain = as1.Tupl(elements=(red, yellow, blue, red))
        m1 = as1.Map(domain=fruits, codomain=codomain)
        assert len(m1) == 2
        assert m1.is_defined_in(phi=fruits[0])
        assert m1.is_defined_in(phi=fruits[1])
        assert m1.is_defined_in(phi=fruits[2])
        assert m1.is_defined_in(phi=fruits[3])
        assert as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[0]), red)
        assert as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[1]), yellow)
        assert as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[2]), blue)
        assert as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[3]), red)


class TestEnumerationEquivalence:
    def test_enumeration_equivalence(self):
        red = as1.let_x_be_a_simple_object(rep='red')
        yellow = as1.let_x_be_a_simple_object(rep='yellow')
        blue = as1.let_x_be_a_simple_object(rep='blue')
        e1 = as1.Enumeration(elements=(red, yellow, blue,))
        e2 = as1.Enumeration(elements=(yellow, red, blue,))
        assert as1.is_enumeration_equivalent(phi=e1, psi=e2)
        assert not as1.is_formula_equivalent(phi=e1, psi=e2)
