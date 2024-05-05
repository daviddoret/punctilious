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

    def test_call(self):
        x, y, z = as1.let_x_be_a_variable(rep=('x', 'y', 'z',))
        a, b, c, d, e = as1.let_x_be_a_simple_object(rep=('a', 'b', 'c', 'd', 'e',))
        f = as1.let_x_be_a_unary_connective(rep='f')
        g = as1.let_x_be_a_binary_connective(rep='g')
        h = as1.let_x_be_a_ternary_connective(rep='h')
        assert as1.is_formula_equivalent(phi=f(), psi=as1.Formula(c=f, terms=None))
        assert as1.is_formula_equivalent(phi=g(x), psi=as1.Formula(c=g, terms=(x,)))
        assert as1.is_formula_equivalent(phi=h(x, y), psi=as1.Formula(c=h, terms=(x, y,)))


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

    def test_set_term(self):
        x, y, z = as1.let_x_be_a_simple_object(rep=('x', 'y', 'z',))
        fb = as1.FormulaBuilder(c=None)
        fb.set_term(i=5, phi=y)
        assert fb.arity == 6
        fb.set_term(i=4, phi=z)
        assert fb.arity == 6
        fb.set_term(i=9, phi=x)
        assert fb.arity == 10

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

    def test_term_1(self, c1, c2):
        fb = as1.FormulaBuilder(c=c2)
        fb.term_0.c = c1
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
        a, b, c = as1.let_x_be_a_simple_object(rep=('a', 'b', 'c',))
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
                pytest.fail(f'Warning {as1.EventCodes.e104} not issued.')

    def test_enumeration(self):
        a, b, c, x, y, z = as1.let_x_be_a_simple_object(rep=('a', 'b', 'c', 'x', 'y', 'z',))
        bbaccczx = as1.Enumeration(elements=(b, b, a, c, c, c, z, x))
        assert as1.is_formula_equivalent(phi=bbaccczx, psi=bbaccczx)
        assert as1.is_enumeration_equivalent(phi=bbaccczx, psi=bbaccczx)
        assert bbaccczx.has_element(phi=a)
        assert bbaccczx.has_element(phi=b)
        assert bbaccczx.has_element(phi=c)
        assert bbaccczx.has_element(phi=x)
        assert bbaccczx.has_element(phi=z)
        assert bbaccczx.get_element_index(phi=b) == 0
        assert bbaccczx.get_element_index(phi=a) == 1
        assert bbaccczx.get_element_index(phi=c) == 2
        assert bbaccczx.get_element_index(phi=z) == 3
        assert bbaccczx.get_element_index(phi=x) == 4
        assert not bbaccczx.has_element(phi=y)
        baczx = as1.Enumeration(elements=(b, a, c, z, x))
        assert as1.is_formula_equivalent(phi=baczx, psi=baczx)
        assert as1.is_enumeration_equivalent(phi=baczx, psi=baczx)
        assert baczx.has_element(phi=a)
        assert baczx.has_element(phi=b)
        assert baczx.has_element(phi=c)
        assert baczx.has_element(phi=x)
        assert baczx.has_element(phi=z)
        assert baczx.get_element_index(phi=b) == 0
        assert baczx.get_element_index(phi=a) == 1
        assert baczx.get_element_index(phi=c) == 2
        assert baczx.get_element_index(phi=z) == 3
        assert baczx.get_element_index(phi=x) == 4
        assert not baczx.has_element(phi=y)
        assert as1.is_enumeration_equivalent(phi=baczx, psi=bbaccczx)
        assert as1.is_formula_equivalent(phi=baczx, psi=bbaccczx)

    def test_is_of_the_form_enumeration(self):
        a, b, c = as1.let_x_be_a_simple_object(rep=('a', 'b', 'c',))
        star = as1.FreeArityConnective(rep='*')
        phi1 = as1.Formula(c=star, terms=(a, b, c,))
        assert as1.is_of_the_form_enumeration(phi=phi1)
        phi2 = as1.Formula(c=star, terms=None)
        assert as1.is_of_the_form_enumeration(phi=phi2)
        phi3 = as1.Formula(c=star, terms=(a, a, b, c,))
        assert not as1.is_of_the_form_enumeration(phi=phi3)
        phi4 = as1.Formula(c=star, terms=(a, b, b, c,))
        assert not as1.is_of_the_form_enumeration(phi=phi4)
        phi5 = as1.Formula(c=star, terms=(a, b, c, c,))
        assert not as1.is_of_the_form_enumeration(phi=phi5)


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
        with pytest.raises(as1.CustomException, match='e118'):
            # the following is ill-formed because the variable is an element of phi, and not of psi.
            # reminder: formula-equivalence-with-variables is non-commutative.
            as1.is_formula_equivalent_with_variables(
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

    def test_is_formula_equivalent_with_variables_2(self):
        a, b, c, d, e = as1.let_x_be_a_simple_object(rep=('a', 'b', 'c', 'd', 'e',))
        ab = as1.Tupl(elements=(a, b,))
        cd = as1.Tupl(elements=(c, d,))
        assert not as1.is_formula_equivalent(phi=ab, psi=cd)
        m = as1.MapBuilder()
        assert as1.is_formula_equivalent_with_variables(phi=ab, psi=cd, v=(c, d,), m=m)
        assert as1.is_formula_equivalent(phi=m.get_assigned_value(phi=c), psi=a)
        assert as1.is_formula_equivalent(phi=m.get_assigned_value(phi=d), psi=b)
        bba = as1.Tupl(elements=(b, b, a,))
        cca = as1.Tupl(elements=(c, c, a,))
        m = as1.MapBuilder()
        assert as1.is_formula_equivalent_with_variables(phi=bba, psi=bba, v=(), m=m)
        m = as1.MapBuilder()
        assert as1.is_formula_equivalent_with_variables(phi=bba, psi=cca, v=(c,), m=m)
        assert as1.is_formula_equivalent(phi=m.get_assigned_value(phi=c), psi=b)
        ababbba = as1.Tupl(elements=(a, b, a, b, b, a,))
        acaccca = as1.Tupl(elements=(a, c, a, c, c, a,))
        m = as1.MapBuilder()
        assert as1.is_formula_equivalent_with_variables(phi=ababbba, psi=acaccca, v=(c,), m=m)
        assert as1.is_formula_equivalent(phi=m.get_assigned_value(phi=c), psi=b)
        multilevel1 = as1.Tupl(elements=(a, b, a, b, b, c, c,))
        multilevel2 = as1.Tupl(elements=(a, multilevel1, a, multilevel1, c,))
        multilevel3 = as1.Tupl(elements=(c, multilevel2, a, multilevel1,))
        print(multilevel3)
        test = as1.replace_formulas(phi=multilevel3, m={a: e, b: d})
        m = as1.MapBuilder()
        assert as1.is_formula_equivalent_with_variables(phi=multilevel3, psi=test, v=(d, e,), m=m)
        assert as1.is_formula_equivalent(phi=m.get_assigned_value(phi=d), psi=b)
        assert as1.is_formula_equivalent(phi=m.get_assigned_value(phi=e), psi=a)


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
        f = as1.Transformation(premises=premises, conclusion=conclusion, variables=variables)
        arguments = as1.Tupl(elements=(p2,))
        output = f.apply_transformation(arguments=arguments)
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

    def test_replace_formulas_two_variables(self):
        a, b, c, d = as1.let_x_be_a_simple_object(rep=('a', 'b', 'c', 'd'))
        c1 = as1.let_x_be_a_unary_connective(rep='c1')
        c2 = as1.let_x_be_a_binary_connective(rep='c2')
        phi = a | c2 | b
        psi = as1.replace_formulas(phi=phi, m={a: c, b: d})
        assert as1.is_formula_equivalent(phi=c | c2 | d, psi=psi)
        phi = (b | c2 | a) | c2 | ((a | c2 | b) | c2 | (a | c2 | a))
        psi = as1.replace_formulas(phi=phi, m={a: c, b: d})
        assert as1.is_formula_equivalent(phi=(d | c2 | c) | c2 | ((c | c2 | d) | c2 | (c | c2 | c)), psi=psi)


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
        red, yellow, blue = as1.let_x_be_a_simple_object(rep=('red', 'yellow', 'blue',))
        e1 = as1.Enumeration(elements=(red, yellow, blue,))
        e2 = as1.Enumeration(elements=(yellow, red, blue,))
        assert as1.is_enumeration_equivalent(phi=e1, psi=e2)
        assert not as1.is_formula_equivalent(phi=e1, psi=e2)


class TestUnionEnumeration:
    def test_union_enumeration(self):
        a, b, c, d, e = as1.let_x_be_a_simple_object(rep=('a', 'b', 'c', 'd', 'e'))
        abc = as1.Enumeration(elements=(a, b, c,))
        cd = as1.Enumeration(elements=(c, d,))
        abcd1 = as1.union_enumeration(phi=abc, psi=cd)
        abcd2 = as1.Enumeration(elements=(a, b, c, d,))
        assert as1.is_enumeration_equivalent(phi=abcd1, psi=abcd2)
        abcde1 = as1.Enumeration(elements=(a, b, c, d, e,))
        abcde2 = as1.Enumeration(elements=(a, b, c, e, d,))
        assert as1.is_enumeration_equivalent(phi=abcde1, psi=abcde2)
        assert not as1.is_formula_equivalent(phi=abcde1, psi=abcde2)  # because of order
        abcde3 = as1.union_enumeration(phi=abcde1, psi=abcde1)
        assert as1.is_enumeration_equivalent(phi=abcde3, psi=abcde1)
        assert as1.is_formula_equivalent(phi=abcde3, psi=abcde1)


class TestEnumerationAccretor:
    def test_del_element(self):
        a = as1.EnumerationAccretor(elements=None)
        x, y, z = as1.let_x_be_a_simple_object(rep=('x', 'y', 'z',))
        a.append(element=x)
        a.append(element=y)
        a.append(element=z)
        assert a.has_element(phi=x)
        assert a.has_element(phi=y)
        assert a.has_element(phi=z)
        with pytest.raises(as1.CustomException, match='e114'):
            a.remove(y)
        with pytest.raises(as1.CustomException, match='e114'):
            a.pop(1)
        with pytest.raises(as1.CustomException, match='e114'):
            a.remove_formula(z)

    def insert_element(self):
        a = as1.EnumerationAccretor(elements=None)
        x, y, z = as1.let_x_be_a_simple_object(rep=('x', 'y', 'z',))
        a.append(element=x)
        a.append(element=z)
        assert a.has_element(phi=x)
        assert a.has_element(phi=z)
        with pytest.raises(as1.CustomException, match='e115'):
            a.insert(1, y)

    def set_element(self):
        a = as1.EnumerationAccretor(elements=None)
        x, y, z = as1.let_x_be_a_simple_object(rep=('x', 'y', 'z',))
        a.append(element=x)
        a.append(element=z)
        assert a.has_element(phi=x)
        assert a.has_element(phi=z)
        with pytest.raises(as1.CustomException, match='e116'):
            a[1] = y


class TestEmptyEnumeration:
    def test_empty_enumeration(self):
        a = as1.EmptyEnumeration()
        x, y, z = as1.let_x_be_a_simple_object(rep=('x', 'y', 'z',))
        assert not a.has_element(phi=x)
        assert a.arity == 0


class TestEnumerationBuilder:
    def test_get_element_index(self):
        # assert False
        pass


class TestPostulation:
    def test_postulation(self):
        a, b, c, d, e = as1.let_x_be_a_simple_object(rep=('a', 'b', 'c', 'd', 'e',))
        f = as1.let_x_be_a_binary_connective(rep='f')
        phi = a | f | b
        a = as1.ProofByPostulation(phi=phi)
        assert as1.is_formula_equivalent(
            phi=a,
            psi=phi | as1.connectives.follows_from | as1.connectives.postulation)


class TestInference:
    def test_inference(self):
        x, y, z = as1.let_x_be_a_variable(rep=('x', 'y', 'z',))
        a, b, c, d, e = as1.let_x_be_a_simple_object(rep=('a', 'b', 'c', 'd', 'e',))
        f = as1.let_x_be_a_binary_connective(rep='f')
        # land = as1.let_x_be_a_binary_connective(rep='land')
        t = as1.Transformation(premises=(x | f | y, y | f | z,), conclusion=x | f | z, variables=(x, y, z,))
        p = (a | f | b, b | f | c,)
        theorem = a | f | c
        as1.is_formula_equivalent(phi=theorem, psi=t(arguments=p))
        i = as1.ProofByInference(phi=theorem, i=as1.Inference(p=p, f=t))
        as1.is_formula_equivalent(phi=i,
                                  psi=theorem | as1.connectives.follows_from | as1.connectives.inference(p, t))


class TestFormulaToTuple:
    def test_formula_to_tuple(self):
        a, b, c, d, e = as1.let_x_be_a_simple_object(rep=('a', 'b', 'c', 'd', 'e',))
        f = as1.let_x_be_a_unary_connective(rep='f')
        g = as1.let_x_be_a_binary_connective(rep='g')
        h = as1.let_x_be_a_ternary_connective(rep='h')
        phi1 = h(e, b, d)
        e1_result = as1.formula_to_tuple(phi=phi1)
        e1_expected = as1.e(elements=(e, b, d,))
        assert as1.is_formula_equivalent(phi=e1_result, psi=e1_expected)
        phi2 = h(phi1, b, g(a, f(b)))
        e2_result = as1.formula_to_tuple(phi=phi2)
        e2_expected = as1.e(elements=(phi1, b, g(a, f(b)),))
        assert as1.is_formula_equivalent(phi=e2_result, psi=e2_expected)
