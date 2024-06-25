import pytest
import punctilious as pu


# from punctilious.axiomatic_system_1 import is_formula_equivalent, is_in_map_domain


@pytest.fixture
def c1():
    return pu.as1.Connective(formula_typesetter=pu.as1.typesetters.classical_formula(
        connective_typesetter='c1'))


@pytest.fixture
def c2():
    return pu.as1.Connective(formula_typesetter=pu.as1.typesetters.classical_formula(
        connective_typesetter='c2'))


@pytest.fixture
def c3():
    return pu.as1.Connective(formula_typesetter=pu.as1.typesetters.classical_formula(
        connective_typesetter='c3'))


@pytest.fixture
def fb1(c1):
    fb = pu.as1.FormulaBuilder(c=c1)
    return fb


@pytest.fixture
def fb2(c2):
    fb = pu.as1.FormulaBuilder(c=c2)
    return fb


@pytest.fixture
def fb3(c3):
    fb = pu.as1.FormulaBuilder(c=c3)
    return fb


@pytest.fixture
def fb4(c1, c2, c3):
    fb1 = pu.as1.FormulaBuilder(c=c1)
    n1_0 = fb1.append(term=c1)
    n1_0.append(term=c3)
    n1_0.append(term=c2)
    fb1.append(term=c2)
    n1_2 = fb1.append(term=c3)
    n1_2_0 = n1_2.append(term=c1)
    n1_2_0_0 = n1_2_0.append(term=c1)
    n1_2_0_0.append(term=c1)
    n1_2_0_0.append(term=c3)
    n1_2_0.append(term=c1)
    n1_2.append(term=c2)
    return fb1


@pytest.fixture
def fb5(c1, c2, c3):
    fb1 = pu.as1.FormulaBuilder(c=c1)
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
    return pu.as1.let_x_be_a_simple_object(formula_typesetter='apple')


@pytest.fixture
def ananas():
    return pu.as1.let_x_be_a_simple_object(formula_typesetter='ananas')


@pytest.fixture
def strawberry():
    return pu.as1.let_x_be_a_simple_object(formula_typesetter='strawberry')


@pytest.fixture
def blueberry():
    return pu.as1.let_x_be_a_simple_object(formula_typesetter='blueberry')


@pytest.fixture
def fruits(apple, ananas, blueberry, strawberry):
    fruits = pu.as1.Enumeration(elements=(apple, ananas, blueberry, strawberry))
    return fruits


class TestConnective:
    def test_connective(self, c1, c2):
        assert c1 is not c2

    def test_simple(self):
        a = pu.as1.let_x_be_a_simple_object(formula_typesetter='a')
        x = a.__str__()
        pass

    def test_call(self):
        x, y, z = pu.as1.let_x_be_a_variable(formula_typesetter=('x', 'y', 'z',))
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_unary_connective(formula_typesetter='f')
        g = pu.as1.let_x_be_a_binary_connective(formula_typesetter='g')
        h = pu.as1.let_x_be_a_ternary_connective(formula_typesetter='h')
        assert pu.as1.is_formula_equivalent(phi=f(), psi=pu.as1.Formula(connective=f, terms=None))
        assert pu.as1.is_formula_equivalent(phi=g(x), psi=pu.as1.Formula(connective=g, terms=(x,)))
        assert pu.as1.is_formula_equivalent(phi=h(x, y), psi=pu.as1.Formula(connective=h, terms=(x, y,)))


class TestFormulaBuilder:
    def test_assure_term(self):
        fb = pu.as1.FormulaBuilder()
        fb.assure_term(i=3)
        assert len(fb) == 4

    def test_formula_builder(self, c1, c2, c3, fb4):
        assert fb4.connective is c1
        assert fb4[0].connective is c1
        assert fb4[1].connective is c2
        assert fb4[2].connective is c3

    def test_set_term(self):
        x, y, z = pu.as1.let_x_be_a_simple_object(formula_typesetter=('x', 'y', 'z',))
        fb = pu.as1.FormulaBuilder(c=None)
        fb.set_term(i=5, phi=y)
        assert fb.arity == 6
        fb.set_term(i=4, phi=z)
        assert fb.arity == 6
        fb.set_term(i=9, phi=x)
        assert fb.arity == 10

    def test_term_0(self, c1, c2, c3):
        fb = pu.as1.FormulaBuilder(c=c1)
        fb.term_0 = c2
        assert fb.connective is c1
        assert fb[0].connective is c2

    def test_terms(self, fb1, fb2, fb3):
        terms1 = pu.as1.FormulaBuilder()
        assert len(terms1) == 0
        terms2 = pu.as1.FormulaBuilder(terms=(fb1,))
        assert len(terms2) == 1
        assert terms2[0].connective is fb1.connective
        assert terms2.term_0.connective is fb1.connective
        terms3 = pu.as1.FormulaBuilder(terms=(fb1, fb2, fb1, fb1, fb3))
        assert len(terms3) == 5
        assert terms3[0].connective is fb1.connective
        assert terms3.term_0.connective is fb1.connective
        assert terms3[1].connective is fb2.connective
        assert terms3.term_1.connective is fb2.connective
        assert terms3[2].connective is fb1.connective
        assert terms3[3].connective is fb1.connective
        assert terms3[4].connective is fb3.connective

    def test_to_formula(self, fb4):
        phi1 = fb4.to_formula()
        assert phi1.connective is fb4.connective
        assert phi1[0].connective is fb4[0].connective
        assert phi1[0][0].connective is fb4[0][0].connective
        assert phi1[0][1].connective is fb4[0][1].connective
        assert phi1[1].connective is fb4[1].connective
        assert phi1[2].connective is fb4[2].connective
        assert phi1[2][0].connective is fb4[2][0].connective
        assert phi1[2][0][0].connective is fb4[2][0][0].connective
        assert phi1[2][0][1].connective is fb4[2][0][1].connective
        assert phi1[2][1].connective is fb4[2][1].connective


class TestFormula:

    def test_formula(self, c1, c2, c3, phi4):
        assert phi4.connective is c1
        assert phi4[0].connective is c1
        assert phi4[1].connective is c2
        assert phi4[2].connective is c3

    def test_term_1(self, c1, c2):
        fb = pu.as1.FormulaBuilder(c=c2)
        fb.term_0.connective = c1
        phi = fb.to_formula()
        assert phi.term_0.connective is c1
        assert phi[0].connective is c1

    def test_terms(self, c1, phi1, phi2, phi3):
        terms1 = pu.as1.Formula(connective=c1)
        assert len(terms1) == 0
        terms2 = pu.as1.Formula(connective=c1, terms=(phi1,))
        assert len(terms2) == 1
        assert terms2[0].connective is phi1.connective
        assert terms2.term_0.connective is phi1.connective
        terms3 = pu.as1.Formula(connective=c1, terms=(phi1, phi2, phi1, phi1, phi3))
        assert len(terms3) == 5
        assert terms3[0].connective is phi1.connective
        assert terms3.term_0.connective is phi1.connective
        assert terms3[1].connective is phi2.connective
        assert terms3.term_1.connective is phi2.connective
        assert terms3[2].connective is phi1.connective
        assert terms3[3].connective is phi1.connective
        assert terms3[4].connective is phi3.connective

    def test_to_formula_builder(self, phi4):
        fb1 = phi4.to_formula_builder()
        assert fb1.connective is phi4.connective
        assert fb1[0].connective is phi4[0].connective
        assert fb1[0][0].connective is phi4[0][0].connective
        assert fb1[0][1].connective is phi4[0][1].connective
        assert fb1[1].connective is phi4[1].connective
        assert fb1[2].connective is phi4[2].connective
        assert fb1[2][0].connective is phi4[2][0].connective
        assert fb1[2][0][0].connective is phi4[2][0][0].connective
        assert fb1[2][0][1].connective is phi4[2][0][1].connective
        assert fb1[2][1].connective is phi4[2][1].connective


class TestIsSubformulaofFormula:
    def test_is_subformula_of_formula(self):
        c1 = pu.as1.FreeArityConnective(formula_typesetter='c1')
        c2 = pu.as1.FreeArityConnective(formula_typesetter='c2')
        c3 = pu.as1.FreeArityConnective(formula_typesetter='c3')
        assert pu.as1.is_subformula_of_formula(
            subformula=c1(c2, c3, c2(c1)),
            formula=c1(c2, c3, c2(c1))
        )
        assert not pu.as1.is_subformula_of_formula(
            subformula=c1(c2, c3, c2(c2)),
            formula=c1(c2, c3, c2(c1))
        )
        assert pu.as1.is_subformula_of_formula(
            subformula=c2(c2),
            formula=c1(c2, c3, c2(c2))
        )
        assert pu.as1.is_subformula_of_formula(
            subformula=c3(c2, c1),
            formula=c1(c2, c3(c2(c1(c3(c2, c1)))), c2(c2))
        )


class TestConnectiveEquivalence:
    def test_is_connective_equivalent(self):
        a, b, c = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c',))
        c1 = pu.as1.BinaryConnective(formula_typesetter='c1')
        c2 = pu.as1.BinaryConnective(formula_typesetter='c2')
        phi = a | c1 | b
        assert pu.as1.is_connective_equivalent(phi=phi, psi=phi)
        psi = b | c1 | c
        assert pu.as1.is_connective_equivalent(phi=phi, psi=psi)
        omega = a | c2 | b
        assert not pu.as1.is_connective_equivalent(phi=phi, psi=omega)


class TestFormulaEquivalence:
    def test_is_formula_equivalent(self, phi2, phi3, phi4, phi5):
        assert pu.as1.is_formula_equivalent(phi=phi2, psi=phi2)
        assert pu.as1.is_formula_equivalent(phi=phi3, psi=phi3)
        assert pu.as1.is_formula_equivalent(phi=phi4, psi=phi4)
        assert pu.as1.is_formula_equivalent(phi=phi5, psi=phi5)
        assert not pu.as1.is_formula_equivalent(phi=phi2, psi=phi3)
        assert not pu.as1.is_formula_equivalent(phi=phi3, psi=phi4)
        assert not pu.as1.is_formula_equivalent(phi=phi4, psi=phi5)


class TestTupl:
    def test_tupl(self, phi1, phi2, phi3):
        cb1 = pu.as1.TuplBuilder((phi1, phi2, phi3,))
        c1 = cb1.to_tupl()
        c2 = pu.as1.Tupl((phi1, phi2, phi3,))
        assert pu.as1.is_formula_equivalent(c1, c2)
        assert len(c1) == 3
        assert len(c2) == 3
        c3 = pu.as1.Tupl()
        assert len(c3) == 0

    def test_in(self):
        x = pu.as1.let_x_be_a_variable(formula_typesetter='x')
        y = pu.as1.let_x_be_a_variable(formula_typesetter='y')
        c = pu.as1.Tupl(elements=(x,))
        assert x in c
        assert y not in c
        assert len(c) == 1


class TestEnumeration:
    def test_tupl(self, phi1, phi2, phi3):
        cb1 = pu.as1.EnumerationBuilder((phi1, phi2, phi3, phi1, phi3,))
        e1 = cb1.to_enumeration()
        print(e1)
        e1 = pu.as1.Enumeration((phi1, phi2, phi3,))
        e2 = pu.as1.Enumeration((phi1, phi2, phi3,))
        e3 = pu.as1.Enumeration((phi3, phi1, phi2,))
        assert len(e1) == 3
        assert len(e2) == 3
        assert len(e3) == 3
        assert pu.as1.is_enumeration_equivalent(e1, e2)
        assert pu.as1.is_enumeration_equivalent(e1, e3)
        assert pu.as1.is_enumeration_equivalent(e2, e3)
        e4 = pu.as1.Enumeration((phi2, phi1,))
        assert not pu.as1.is_enumeration_equivalent(e4, e1)
        assert not pu.as1.is_enumeration_equivalent(e4, e2)
        assert not pu.as1.is_enumeration_equivalent(e4, e3)

    def test_has_element(self):
        c1 = pu.as1.let_x_be_a_binary_connective(formula_typesetter='c1')
        c2 = pu.as1.let_x_be_a_binary_connective(formula_typesetter='c2')
        x = pu.as1.let_x_be_a_simple_object(formula_typesetter='x')
        y = pu.as1.let_x_be_a_simple_object(formula_typesetter='y')
        phi1 = x | c1 | y
        phi2 = x | c2 | y
        phi3 = y | c1 | x
        e1 = pu.as1.Enumeration(elements=(phi1, phi2, phi3,))
        assert e1.has_element(phi=phi1)
        assert not e1.has_element(phi=x | c1 | x)
        phi1_other_instance = x | c1 | y
        assert e1.has_element(phi=phi1_other_instance)
        assert e1.get_element_index(phi=phi1) == 0
        assert e1.get_element_index(phi=phi2) == 1
        assert e1.get_element_index(phi=phi3) == 2

    def test_exception(self):
        a = pu.as1.let_x_be_a_simple_object(formula_typesetter='a')
        b = pu.as1.let_x_be_a_simple_object(formula_typesetter='b')
        c = pu.as1.let_x_be_a_simple_object(formula_typesetter='c')
        with pytest.raises(pu.as1.CustomException, match='e110'):
            # duplicate formula-equivalent formulas are forbidden in enumerations.
            e1 = pu.as1.Enumeration(elements=(a, b, c, b,))

    def test_enumeration(self):
        a, b, c, x, y, z = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'x', 'y', 'z',))
        baczx = pu.as1.Enumeration(elements=(b, a, c, z, x))
        assert pu.as1.is_formula_equivalent(phi=baczx, psi=baczx)
        assert pu.as1.is_enumeration_equivalent(phi=baczx, psi=baczx)
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
        baczx2 = pu.as1.Enumeration(elements=(b, a, c, z, x))
        assert pu.as1.is_formula_equivalent(phi=baczx, psi=baczx2)
        assert pu.as1.is_enumeration_equivalent(phi=baczx, psi=baczx2)

    def test_is_well_formed_enumeration(self):
        a, b, c = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c',))
        star = pu.as1.FreeArityConnective(formula_typesetter='*')
        phi1 = pu.as1.Formula(connective=star, terms=(a, b, c,))
        assert pu.as1.is_well_formed_enumeration(phi=phi1)
        phi2 = pu.as1.Formula(connective=star, terms=None)
        assert pu.as1.is_well_formed_enumeration(phi=phi2)
        phi3 = pu.as1.Formula(connective=star, terms=(a, a, b, c,))
        assert not pu.as1.is_well_formed_enumeration(phi=phi3)
        phi4 = pu.as1.Formula(connective=star, terms=(a, b, b, c,))
        assert not pu.as1.is_well_formed_enumeration(phi=phi4)
        phi5 = pu.as1.Formula(connective=star, terms=(a, b, c, c,))
        assert not pu.as1.is_well_formed_enumeration(phi=phi5)


class TestFormulaEquivalenceWithVariables:
    def test_is_formula_equivalent_with_variables(self):
        x = pu.as1.let_x_be_a_variable(formula_typesetter='x')
        y = pu.as1.let_x_be_a_variable(formula_typesetter='y')
        is_a = pu.as1.let_x_be_a_binary_connective(formula_typesetter='is-a')
        human = pu.as1.let_x_be_a_simple_object(formula_typesetter='human')
        platypus = pu.as1.let_x_be_a_simple_object(formula_typesetter='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_typesetter='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_typesetter='aristotle')
        assert pu.as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | human,
            psi=aristotle | is_a | human,
            variables=())
        with pytest.raises(pu.as1.CustomException, match='e118'):
            # the following is ill-formed because the variable is an element of phi, and not of psi.
            # reminder: formula-equivalence-with-variables is non-commutative.
            pu.as1.is_formula_equivalent_with_variables(
                phi=aristotle | is_a | x,
                psi=aristotle | is_a | human,
                variables=(x,))
        assert pu.as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | human,
            psi=aristotle | is_a | x,
            variables=(x,))
        assert not pu.as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | human,
            psi=aristotle | is_a | platypus,
            variables=())
        assert not pu.as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | x,
            psi=aristotle | is_a | human,
            variables=(y,))
        assert not pu.as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | x,
            psi=platypus | is_a | human,
            variables=(x,))

    def test_is_formula_equivalent_with_variables_2(self):
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        ab = pu.as1.Tupl(elements=(a, b,))
        cd = pu.as1.Tupl(elements=(c, d,))
        assert not pu.as1.is_formula_equivalent(phi=ab, psi=cd)
        m = pu.as1.MapBuilder()
        assert pu.as1.is_formula_equivalent_with_variables(phi=ab, psi=cd, variables=(c, d,), variables_fixed_values=m)
        assert pu.as1.is_formula_equivalent(phi=m.get_assigned_value(phi=c), psi=a)
        assert pu.as1.is_formula_equivalent(phi=m.get_assigned_value(phi=d), psi=b)
        bba = pu.as1.Tupl(elements=(b, b, a,))
        cca = pu.as1.Tupl(elements=(c, c, a,))
        m = pu.as1.MapBuilder()
        assert pu.as1.is_formula_equivalent_with_variables(phi=bba, psi=bba, variables=(), variables_fixed_values=m)
        m = pu.as1.MapBuilder()
        assert pu.as1.is_formula_equivalent_with_variables(phi=bba, psi=cca, variables=(c,), variables_fixed_values=m)
        assert pu.as1.is_formula_equivalent(phi=m.get_assigned_value(phi=c), psi=b)
        ababbba = pu.as1.Tupl(elements=(a, b, a, b, b, a,))
        acaccca = pu.as1.Tupl(elements=(a, c, a, c, c, a,))
        m = pu.as1.MapBuilder()
        assert pu.as1.is_formula_equivalent_with_variables(phi=ababbba, psi=acaccca, variables=(c,),
                                                           variables_fixed_values=m)
        assert pu.as1.is_formula_equivalent(phi=m.get_assigned_value(phi=c), psi=b)
        multilevel1 = pu.as1.Tupl(elements=(a, b, a, b, b, c, c,))
        multilevel2 = pu.as1.Tupl(elements=(a, multilevel1, a, multilevel1, c,))
        multilevel3 = pu.as1.Tupl(elements=(c, multilevel2, a, multilevel1,))
        print(multilevel3)
        test = pu.as1.replace_formulas(phi=multilevel3, m={a: e, b: d})
        m = pu.as1.MapBuilder()
        assert pu.as1.is_formula_equivalent_with_variables(phi=multilevel3, psi=test, variables=(d, e,),
                                                           variables_fixed_values=m)
        assert pu.as1.is_formula_equivalent(phi=m.get_assigned_value(phi=d), psi=b)
        assert pu.as1.is_formula_equivalent(phi=m.get_assigned_value(phi=e), psi=a)


class TestFormulaEquivalenceWithVariables2:
    def test_is_formula_equivalent_with_variables(self):
        x = pu.as1.let_x_be_a_variable(formula_typesetter='x')
        y = pu.as1.let_x_be_a_variable(formula_typesetter='y')
        is_a = pu.as1.let_x_be_a_binary_connective(
            formula_typesetter=pu.as1.InfixFormulaTypesetter(connective_typesetter='is-a'))
        human = pu.as1.let_x_be_a_simple_object(formula_typesetter='human')
        platypus = pu.as1.let_x_be_a_simple_object(formula_typesetter='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_typesetter='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_typesetter='aristotle')

        result, map, = pu.as1.is_formula_equivalent_with_variables_2(
            phi=aristotle | is_a | human,
            psi=aristotle | is_a | human,
            variables=())
        assert result

        with pytest.raises(Exception):
            # the following is ill-formed because the variable is an element of phi, and not of psi.
            # reminder: formula-equivalence-with-variables is non-commutative.
            pu.as1.is_formula_equivalent_with_variables_2(
                phi=aristotle | is_a | x,
                psi=aristotle | is_a | human,
                variables=(x,))

        result, map, = pu.as1.is_formula_equivalent_with_variables_2(
            phi=aristotle | is_a | human,
            psi=aristotle | is_a | x,
            variables=(x,))
        assert result
        assert pu.as1.is_formula_equivalent(phi=map.get_assigned_value(phi=x), psi=human)

        result, map, = pu.as1.is_formula_equivalent_with_variables_2(
            phi=human,
            psi=platypus,
            variables=())
        assert not result

        result, map, = pu.as1.is_formula_equivalent_with_variables_2(
            phi=aristotle | is_a | human,
            psi=aristotle | is_a | platypus,
            variables=())
        assert not result

        result, map, = pu.as1.is_formula_equivalent_with_variables_2(
            phi=aristotle | is_a | x,
            psi=aristotle | is_a | human,
            variables=(y,))
        assert not result

        with pytest.raises(Exception):
            result, map, = pu.as1.is_formula_equivalent_with_variables_2(
                phi=aristotle | is_a | x,
                psi=platypus | is_a | human,
                variables=(x,))

    def test_is_formula_equivalent_with_variables_2(self):
        a, b, c, d, e, = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        ab = pu.as1.Tupl(elements=(a, b,))
        cd = pu.as1.Tupl(elements=(c, d,))
        assert not pu.as1.is_formula_equivalent(phi=ab, psi=cd)
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(
            phi=ab, psi=cd,
            variables=(c, d,),
            variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=map.get_assigned_value(phi=c), psi=a)
        assert pu.as1.is_formula_equivalent(phi=map.get_assigned_value(phi=d), psi=b)

        bba = pu.as1.Tupl(elements=(b, b, a,))
        cca = pu.as1.Tupl(elements=(c, c, a,))
        m = pu.as1.MapBuilder()
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=bba, psi=bba, variables=(),
                                                                     variables_fixed_values=None)
        assert result

        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=bba, psi=cca, variables=(c,),
                                                                     variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=map.get_assigned_value(phi=c), psi=b)

        ababbba = pu.as1.Tupl(elements=(a, b, a, b, b, a,))
        acaccca = pu.as1.Tupl(elements=(a, c, a, c, c, a,))
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=ababbba, psi=acaccca, variables=(c,),
                                                                     variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=map.get_assigned_value(phi=c), psi=b)

        multilevel1 = pu.as1.Tupl(elements=(a, b, a, b, b, c, c,))
        multilevel2 = pu.as1.Tupl(elements=(a, multilevel1, a, multilevel1, c,))
        multilevel3 = pu.as1.Tupl(elements=(c, multilevel2, a, multilevel1,))
        print(multilevel3)
        test = pu.as1.replace_formulas(phi=multilevel3, m={a: e, b: d})
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=multilevel3, psi=test, variables=(d, e,),
                                                                     variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=map.get_assigned_value(phi=d), psi=b)
        assert pu.as1.is_formula_equivalent(phi=map.get_assigned_value(phi=e), psi=a)


class TestTransformation:
    def test_transformation(self):
        x = pu.as1.let_x_be_a_variable(formula_typesetter='x')
        y = pu.as1.let_x_be_a_variable(formula_typesetter='y')
        is_a = pu.as1.let_x_be_a_binary_connective(formula_typesetter='is-a')
        human = pu.as1.let_x_be_a_simple_object(formula_typesetter='human')
        platypus = pu.as1.let_x_be_a_simple_object(formula_typesetter='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_typesetter='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_typesetter='aristotle')
        p1 = x | is_a | human
        p2 = aristotle | is_a | human
        premises = pu.as1.Enumeration(elements=(p1,))
        conclusion = x | is_a | mortal
        variables = pu.as1.Enumeration(elements=(x,))
        f = pu.as1.Transformation(premises=premises, conclusion=conclusion, variables=variables)
        arguments = pu.as1.Tupl(elements=(p2,))
        output = f.apply_transformation(arguments=arguments)
        pu.as1.is_formula_equivalent(phi=aristotle | is_a | mortal, psi=output)

    def test_is_well_formed_transformation(self):
        x = pu.as1.let_x_be_a_variable(formula_typesetter='x')
        y = pu.as1.let_x_be_a_variable(formula_typesetter='y')
        is_a = pu.as1.let_x_be_a_binary_connective(formula_typesetter='is-a')
        human = pu.as1.let_x_be_a_simple_object(formula_typesetter='human')
        platypus = pu.as1.let_x_be_a_simple_object(formula_typesetter='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_typesetter='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_typesetter='aristotle')
        p1 = x | is_a | human
        p2 = aristotle | is_a | human
        premises = pu.as1.Enumeration(elements=(p1,))
        conclusion = x | is_a | mortal
        variables = pu.as1.Enumeration(elements=(x,))
        phi1 = pu.as1.connectives.transformation(premises, conclusion, variables)
        assert pu.as1.is_well_formed_transformation(phi=phi1)
        t = pu.as1.Tupl(elements=(platypus, platypus,))
        phi2 = pu.as1.connectives.transformation(premises, conclusion, t)
        assert not pu.as1.is_well_formed_transformation(phi=phi2)


class TestReplaceFormulas:
    def test_replace_formulas(self):
        land = pu.as1.let_x_be_a_binary_connective(formula_typesetter='land')
        x = pu.as1.let_x_be_a_variable(formula_typesetter='x')
        y = pu.as1.let_x_be_a_variable(formula_typesetter='y')
        is_a = pu.as1.let_x_be_a_binary_connective(formula_typesetter='is-a')
        human = pu.as1.let_x_be_a_simple_object(formula_typesetter='human')
        animal = pu.as1.let_x_be_a_simple_object(formula_typesetter='animal')
        platypus = pu.as1.let_x_be_a_simple_object(formula_typesetter='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_typesetter='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_typesetter='aristotle')
        assert pu.as1.is_formula_equivalent(
            phi=pu.as1.replace_formulas(phi=x | is_a | human, m={x: aristotle}),
            psi=aristotle | is_a | human)
        assert not pu.as1.is_formula_equivalent(
            phi=pu.as1.replace_formulas(phi=x | is_a | human, m={x: platypus}),
            psi=aristotle | is_a | human)
        phi = aristotle | is_a | human
        phi = pu.as1.replace_formulas(phi=phi, m={human: aristotle})
        psi = aristotle | is_a | aristotle
        assert pu.as1.is_formula_equivalent(
            phi=phi,
            psi=psi)
        omega1 = (aristotle | is_a | human) | land | (platypus | is_a | animal)
        omega2 = pu.as1.replace_formulas(phi=omega1,
                                         m={human: aristotle})
        assert pu.as1.is_formula_equivalent(
            phi=omega2,
            psi=(aristotle | is_a | aristotle) | land | (platypus | is_a | animal))

    def test_replace_formulas_two_variables(self):
        a, b, c, d = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd'))
        c1 = pu.as1.let_x_be_a_unary_connective(formula_typesetter='c1')
        c2 = pu.as1.let_x_be_a_binary_connective(formula_typesetter='c2')
        phi = a | c2 | b
        psi = pu.as1.replace_formulas(phi=phi, m={a: c, b: d})
        assert pu.as1.is_formula_equivalent(phi=c | c2 | d, psi=psi)
        phi = (b | c2 | a) | c2 | ((a | c2 | b) | c2 | (a | c2 | a))
        psi = pu.as1.replace_formulas(phi=phi, m={a: c, b: d})
        assert pu.as1.is_formula_equivalent(phi=(d | c2 | c) | c2 | ((c | c2 | d) | c2 | (c | c2 | c)), psi=psi)


class TestMap:
    def test_map(self, fruits):
        red = pu.as1.let_x_be_a_simple_object(formula_typesetter='red')
        yellow = pu.as1.let_x_be_a_simple_object(formula_typesetter='yellow')
        blue = pu.as1.let_x_be_a_simple_object(formula_typesetter='blue')
        codomain = pu.as1.Tupl(elements=(red, yellow, blue, red))
        m1 = pu.as1.Map(domain=fruits, codomain=codomain)
        assert len(m1) == 2
        assert pu.as1.is_in_map_domain(phi=fruits[0], m=m1)
        assert pu.as1.is_in_map_domain(phi=fruits[1], m=m1)
        assert pu.as1.is_in_map_domain(phi=fruits[2], m=m1)
        assert pu.as1.is_in_map_domain(phi=fruits[3], m=m1)
        assert pu.as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[0]), red)
        assert pu.as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[1]), yellow)
        assert pu.as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[2]), blue)
        assert pu.as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[3]), red)
        m1 = pu.as1.reduce_map(m=m1, preimage=fruits[2])
        assert pu.as1.is_in_map_domain(phi=fruits[0], m=m1)
        assert pu.as1.is_in_map_domain(phi=fruits[1], m=m1)
        assert not pu.as1.is_in_map_domain(phi=fruits[2], m=m1)
        assert pu.as1.is_in_map_domain(phi=fruits[3], m=m1)
        m1 = pu.as1.extend_map(m=m1, preimage=fruits[3], image=yellow)
        assert pu.as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[0]), red)
        assert pu.as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[1]), yellow)
        assert pu.as1.is_formula_equivalent(m1.get_assigned_value(phi=fruits[3]), yellow)


class TestEnumerationEquivalence:
    def test_enumeration_equivalence(self):
        red, yellow, blue = pu.as1.let_x_be_a_simple_object(formula_typesetter=('red', 'yellow', 'blue',))
        e1 = pu.as1.Enumeration(elements=(red, yellow, blue,))
        e2 = pu.as1.Enumeration(elements=(yellow, red, blue,))
        assert pu.as1.is_enumeration_equivalent(phi=e1, psi=e2)
        assert not pu.as1.is_formula_equivalent(phi=e1, psi=e2)


class TestUnionEnumeration:
    def test_union_enumeration(self):
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e'))
        abc = pu.as1.Enumeration(elements=(a, b, c,))
        cd = pu.as1.Enumeration(elements=(c, d,))
        abcd1 = pu.as1.union_enumeration(phi=abc, psi=cd)
        abcd2 = pu.as1.Enumeration(elements=(a, b, c, d,))
        assert pu.as1.is_enumeration_equivalent(phi=abcd1, psi=abcd2)
        abcde1 = pu.as1.Enumeration(elements=(a, b, c, d, e,))
        abcde2 = pu.as1.Enumeration(elements=(a, b, c, e, d,))
        assert pu.as1.is_enumeration_equivalent(phi=abcde1, psi=abcde2)
        assert not pu.as1.is_formula_equivalent(phi=abcde1, psi=abcde2)  # because of order
        abcde3 = pu.as1.union_enumeration(phi=abcde1, psi=abcde1)
        assert pu.as1.is_enumeration_equivalent(phi=abcde3, psi=abcde1)
        assert pu.as1.is_formula_equivalent(phi=abcde3, psi=abcde1)


class TestEmptyEnumeration:
    def test_empty_enumeration(self):
        a = pu.as1.EmptyEnumeration()
        x, y, z = pu.as1.let_x_be_a_simple_object(formula_typesetter=('x', 'y', 'z',))
        assert not a.has_element(phi=x)
        assert a.arity == 0


class TestEnumerationBuilder:
    def test_get_element_index(self):
        # assert False
        pass


class TestInferenceRule:
    def test_inference_rule_without_premises(self):
        # elaborate a theory
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_binary_connective(formula_typesetter='f')
        phi = a | f | b
        rule = pu.as1.Transformation(premises=None, conclusion=phi, variables=None)
        ir = pu.as1.InferenceRule(transformation=rule)
        axiomatization = pu.as1.Axiomatization(derivations=(ir,))

        # derivation from the axiom
        i = pu.as1.Inference(premises=None, transformation_rule=rule)
        isolated_theorem = pu.as1.Derivation(valid_statement=phi, justification=i)
        pu.as1.Theory(derivations=(*axiomatization, isolated_theorem))
        assert pu.as1.is_formula_equivalent(
            phi=isolated_theorem.valid_statement,
            psi=phi)

    def test_is_well_formed_postulation(self):
        a, b = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b',))
        f = pu.as1.let_x_be_a_binary_connective(formula_typesetter='f')
        rule = pu.as1.Transformation(premises=None, conclusion=a | f | b,
                                     variables=None)
        phi1 = rule | pu.as1.connectives.follows_from | pu.as1.connectives.inference_rule
        assert pu.as1.is_well_formed_inference_rule(phi=phi1)

        # incorrect connective
        phi2 = rule | pu.as1.connectives.inference | pu.as1.connectives.inference_rule
        assert not pu.as1.is_well_formed_inference_rule(phi=phi2)

        # incorrect axiomatic-postulation
        phi3 = rule | pu.as1.connectives.follows_from | pu.as1.connectives.enumeration
        assert not pu.as1.is_well_formed_inference_rule(phi=phi3)


class TestFormulaToTuple:
    def test_formula_to_tuple(self):
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_unary_connective(formula_typesetter='f')
        g = pu.as1.let_x_be_a_binary_connective(formula_typesetter='g')
        h = pu.as1.let_x_be_a_ternary_connective(formula_typesetter='h')
        phi1 = h(e, b, d)
        e1_result = pu.as1.formula_to_tuple(phi=phi1)
        e1_expected = pu.as1.enumeration(elements=(e, b, d,))
        assert pu.as1.is_formula_equivalent(phi=e1_result, psi=e1_expected)
        phi2 = h(phi1, b, g(a, f(b)))
        e2_result = pu.as1.formula_to_tuple(phi=phi2)
        e2_expected = pu.as1.enumeration(elements=(phi1, b, g(a, f(b)),))
        assert pu.as1.is_formula_equivalent(phi=e2_result, psi=e2_expected)


class TestProofByPostulation:
    def test_is_well_formed(self):
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        star3 = pu.as1.let_x_be_a_ternary_connective(formula_typesetter='*3')
        rule1 = pu.as1.Transformation(premises=None, conclusion=star3(e, b, d), variables=None)
        phi1 = rule1 | pu.as1.connectives.follows_from | pu.as1.connectives.inference_rule
        assert pu.as1.is_well_formed_inference_rule(phi=phi1)
        phi2 = rule1 | pu.as1.connectives.map | pu.as1.connectives.inference_rule
        assert not pu.as1.is_well_formed_inference_rule(phi=phi2)
        phi3 = rule1 | pu.as1.connectives.follows_from | b
        assert not pu.as1.is_well_formed_inference_rule(phi=phi3)


class TestInference:
    def test_inference(self):
        x, y, z = pu.as1.let_x_be_a_variable(formula_typesetter=('x', 'y', 'z',))
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_binary_connective(formula_typesetter='f')
        t = pu.as1.Transformation(premises=(x | f | y, y | f | z,), conclusion=x | f | z, variables=(x, y, z,))
        p = (a | f | b, b | f | c,)
        theorem = a | f | c
        pu.as1.is_formula_equivalent(phi=theorem, psi=t(arguments=p))
        i = pu.as1.Theorem(valid_statement=theorem, i=pu.as1.Inference(premises=p, transformation_rule=t))
        pu.as1.is_formula_equivalent(
            phi=i,
            psi=theorem | pu.as1.connectives.follows_from | pu.as1.connectives.inference(p, t))

    def test_is_well_formed_inference(self):
        x, y, z = pu.as1.let_x_be_a_variable(formula_typesetter=('x', 'y', 'z',))
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_binary_connective(formula_typesetter='f')
        t = pu.as1.Transformation(premises=(x | f | y, y | f | z,), conclusion=x | f | z, variables=(x, y, z,))
        p = (a | f | b, b | f | c,)
        phi1 = p | pu.as1.connectives.inference | t
        assert pu.as1.is_well_formed_inference(phi=phi1)
        phi2 = p | pu.as1.connectives.inference | a
        assert not pu.as1.is_well_formed_inference(phi=phi2)
        phi3 = p | pu.as1.connectives.follows_from | t
        assert not pu.as1.is_well_formed_inference(phi=phi3)
        phi4 = f(a, a, b, b) | pu.as1.connectives.follows_from | t
        assert not pu.as1.is_well_formed_inference(phi=phi4)


class TestProofByInference:
    def test_is_well_formed(self):
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        x, y, z = pu.as1.let_x_be_a_variable(formula_typesetter=('x', 'y', 'z',))
        star = pu.as1.let_x_be_a_binary_connective(formula_typesetter='*')
        premises = pu.as1.Enumeration(elements=(x | star | y, y | star | z,))
        conclusion = x | star | z
        variables = pu.as1.Enumeration(elements=(x, y, z,))
        f = pu.as1.Transformation(premises=premises, conclusion=conclusion, variables=variables)
        i = pu.as1.Inference(premises=(a | star | b, b | star | c,), transformation_rule=f)
        assert pu.as1.is_well_formed_theorem(phi=(a | star | c) | pu.as1.connectives.follows_from | i)
        pu.as1.Theorem(valid_statement=a | star | c, i=i)  # would raise an exception if it was unsuccessful
        assert not pu.as1.is_well_formed_theorem(phi=(a | star | d) | pu.as1.connectives.follows_from | i)
        i2 = pu.as1.Inference(premises=(a | star | b, b | star | a,), transformation_rule=f)
        assert not pu.as1.is_well_formed_theorem(phi=(a | star | c) | pu.as1.connectives.follows_from | i2)
        pass


class TestIteratePermutationsOfEnumerationElementsWithFixedSize:
    def test_iterate_permutations_of_enumeration_elements_with_fixed_size(self):
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))

        e = pu.as1.Enumeration()
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=0):
            i = i + 1
        assert i == 0

        e = pu.as1.Enumeration(elements=(a,))
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=0):
            i = i + 1
        assert i == 0
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=1):
            i = i + 1
        assert i == 1

        e = pu.as1.Enumeration(elements=(a, b,))
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=0):
            i = i + 1
        assert i == 0
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=1):
            i = i + 1
        assert i == 2
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=2):
            i = i + 1
        assert i == 2

        e = pu.as1.Enumeration(elements=(a, b, c,))
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=0):
            i = i + 1
        assert i == 0
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=1):
            i = i + 1
        assert i == 3
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=2):
            i = i + 1
        assert i == 6
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=3):
            i = i + 1
        assert i == 6


class TestAreValidStatementsInTheory:
    def test_are_valid_statements_in_theory(self):
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        t, _, = pu.as1.let_x_be_an_axiom(t=None, valid_statement=a)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, valid_statement=c)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, valid_statement=d)
        assert pu.as1.are_valid_statements_in_theory(s=(a, c,), t=t)
        assert pu.as1.are_valid_statements_in_theory(s=(a, c, d,), t=t)
        assert pu.as1.are_valid_statements_in_theory(s=(d, a, c,), t=t)
        assert pu.as1.are_valid_statements_in_theory(s=None, t=t)
        assert not pu.as1.are_valid_statements_in_theory(s=(e,), t=t)
        assert not pu.as1.are_valid_statements_in_theory(s=(a, b, d,), t=t)
        assert not pu.as1.are_valid_statements_in_theory(s=(a, e, b,), t=t)


class TestAreValidStatementsInTheoryWithVariables:
    def test_are_valid_statements_in_theory_with_variables(self):
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        t, _, = pu.as1.let_x_be_an_axiom(t=None, valid_statement=a)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, valid_statement=c)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, valid_statement=d)
        valid, s, = pu.as1.are_valid_statements_in_theory_with_variables(s=(a, c,), t=t, variables=None,
                                                                         variables_values=None)
        assert valid
        valid, s, = pu.as1.are_valid_statements_in_theory_with_variables(s=(a, c, e,), t=t, variables=(e,),
                                                                         variables_values=pu.as1.Map(domain=(e,),
                                                                                                     codomain=(d,)))
        assert valid
        valid, s, = pu.as1.are_valid_statements_in_theory_with_variables(s=(a, c, e,), t=t, variables=(e,),
                                                                         variables_values=None)
        assert valid


class TestStripDuplicateFormulasInPythonTuple:
    def test_strip_duplicate_formulas_in_python_tuple(self):
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        t1 = pu.as1.Tupl(elements=(a, b, a, a, e, e,))
        t2 = pu.as1.Tupl(elements=(a, b, e,))
        t3 = pu.as1.strip_duplicate_formulas_in_python_tuple(t=t1)
        t3 = pu.as1.Tupl(elements=t3)
        assert not pu.as1.is_formula_equivalent(phi=t1, psi=t3)
        assert pu.as1.is_formula_equivalent(phi=t2, psi=t3)


class TestCoerceEnumeration:
    def test_coerce_enumeration(self):
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        e1 = pu.as1.Enumeration(elements=(a, b, a, a, e, e,), strip_duplicates=True)
        e2 = pu.as1.Enumeration(elements=(a, b, e,), strip_duplicates=True)
        e3 = pu.as1.Enumeration(elements=e1, strip_duplicates=True)
        assert pu.as1.is_formula_equivalent(phi=e1, psi=e3)
        assert pu.as1.is_formula_equivalent(phi=e2, psi=e3)
        assert pu.as1.is_formula_equivalent(phi=e1, psi=e2)


class TestAxiomatization:
    def test_is_well_formed(self):
        # elaborate a theory
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        x, y, z = pu.as1.let_x_be_a_variable(formula_typesetter=('x', 'y', 'z',))
        star1 = pu.as1.let_x_be_a_unary_connective(formula_typesetter='*1')
        star2 = pu.as1.let_x_be_a_binary_connective(formula_typesetter='*2')
        axiom_ok_1 = pu.as1.Axiom(valid_statement=a | star2 | b)
        axiom_ok_2 = pu.as1.Axiom(valid_statement=star1(c))
        assert pu.as1.is_well_formed_axiom(phi=axiom_ok_2)

        # simple case
        e1 = pu.as1.Enumeration(elements=(axiom_ok_1, axiom_ok_2,))
        e1 = pu.as1.Axiomatization(derivations=e1)
        assert pu.as1.is_well_formed_axiomatization(phi=e1)

        # extreme case: the empty enumeration
        e2 = pu.as1.Enumeration()
        e2 = pu.as1.Axiomatization(derivations=e2)
        assert pu.as1.is_well_formed_axiomatization(phi=e2)
        a1 = pu.as1.Axiomatization(derivations=(axiom_ok_1, axiom_ok_2,))  # does not raise an exception

        # bad case: an enumeration with a non-axiom
        e3 = pu.as1.Enumeration(elements=(axiom_ok_1, axiom_ok_2, star1(e),))
        assert not pu.as1.is_well_formed_axiomatization(phi=e3)
        with pytest.raises(pu.as1.CustomException, match='e123'):
            a2 = pu.as1.Axiomatization(derivations=e3)  # raise an e123 exception


class TestDemonstration:
    def test_is_well_formed(self):
        # elaborate a theory
        theory = pu.as1.let_x_be_a_collection_of_axioms(axioms=None)
        a, b, c, d, e = pu.as1.let_x_be_a_simple_object(formula_typesetter=('a', 'b', 'c', 'd', 'e',))
        x, y, z = pu.as1.let_x_be_a_variable(formula_typesetter=('x', 'y', 'z',))
        star = pu.as1.let_x_be_a_binary_connective(formula_typesetter='*')
        theory, axiom_1, = pu.as1.let_x_be_an_axiom(t=theory, valid_statement=a | star | b)
        theory, axiom_2, = pu.as1.let_x_be_an_axiom(t=theory, valid_statement=b | star | c)
        theory, ir1, = pu.as1.let_x_be_an_inference_rule(theory=theory,
                                                         premises=(x | star | y,
                                                                   y | star | z,),
                                                         conclusion=x | star | z,
                                                         variables=(x, y, z,))

        # derive a theorem
        demo2, _, = pu.as1.derive_1(t=theory,
                                    conjecture=a | star | c,
                                    premises=(
                                        a | star | b,
                                        b | star | c,),
                                    inference_rule=ir1)
        assert pu.as1.is_valid_statement_in_theory(phi=a | star | c, t=demo2)

        with pytest.raises(pu.as1.CustomException, match='e123'):
            # invalid proof raise exception
            pu.as1.Theory(derivations=(axiom_1, axiom_2, a | star | e))

        with pytest.raises(pu.as1.CustomException, match='e123'):
            # invalid proof sequence exception
            pu.as1.Theory(derivations=(axiom_1, axiom_2, a | star | c, ir1,))
            pass


class TestVariable:
    def test_variable(self):
        with pu.as1.let_x_be_a_variable(formula_typesetter='x') as x:
            print(x)
        with pu.as1.let_x_be_a_variable(formula_typesetter='x') as x, pu.as1.let_x_be_a_variable(
                formula_typesetter='y') as y:
            print(x)
            print(y)
            pass


class TestAutoDerivation:
    def test_auto_derivation(self):
        # elaborate a theory
        p = pu.as1.let_x_be_a_simple_object(formula_typesetter='P')
        q = pu.as1.let_x_be_a_simple_object(formula_typesetter='Q')
        t1, a1 = pu.as1.let_x_be_an_axiom(t=None, axiom=pu.as1.Axiom(valid_statement=p))

        t1, success, _, = pu.as1.derive_0(t=t1, conjecture=p)

        if_p_then_q = pu.as1.InferenceRule(
            transformation=pu.as1.Transformation(premises=(p,), conclusion=q, variables=()))
        t1 = pu.as1.extend_theory(if_p_then_q, t=t1)

        with pu.as1.let_x_be_a_variable(formula_typesetter='x') as x, pu.as1.let_x_be_a_variable(
                formula_typesetter='y') as y:
            x_y_then_x_and_y = pu.as1.InferenceRule(
                transformation=pu.as1.Transformation(premises=(x, y,), conclusion=x | pu.as1.connectives.land | y,
                                                     variables=(x, y,)))
        t1 = pu.as1.Theory(derivations=(*t1, x_y_then_x_and_y,))

        pass
        # auto-derivation of an existing valid-statement
        t2, success, _, = pu.as1.derive_0(t=t1, conjecture=p)
        assert success
        pass
        # auto-derivation of a simple theorem, without variables
        t2, success, _, = pu.as1.derive_2(t=t2, conjecture=q, inference_rule=if_p_then_q)
        assert success
        pass

        # auto-derivation of a simple theorem, without some variables
        t2, success, _, = pu.as1.auto_derive_2(t=t2, conjecture=p | pu.as1.connectives.land | q)
        assert success
        pass
        # auto-derivation of an impossible theorem fails and raises an auto-derivation-failure
        t2, success, _, = pu.as1.auto_derive_2(t=t2, conjecture=p | pu.as1.connectives.lor | q)
        assert not success
        pass

        # use auto-derivation-2
        t3, success, derivation, _ = pu.as1.auto_derive_4(t=t1, conjecture=p | pu.as1.connectives.land | q,
                                                          max_recursion=8, debug=True)
        assert success
        pass

        t3, success, derivation, _ = pu.as1.auto_derive_4(t=t1, conjecture=p | pu.as1.connectives.lor | q,
                                                          max_recursion=8, debug=True)
        assert not success
        pass


class TestFormulaDepth:
    def test_get_formula_depth(self):
        c = pu.as1.FreeArityConnective(formula_typesetter=pu.pl1.symbols.x_uppercase_serif_italic)
        phi1 = pu.as1.Formula(connective=c, terms=None)
        assert pu.as1.get_formula_depth(phi=phi1) == 1
        phi2 = pu.as1.Formula(connective=c, terms=(phi1, phi1,))
        assert pu.as1.get_formula_depth(phi=phi2) == 2
        phi3 = pu.as1.Formula(connective=c, terms=(phi1, phi2, phi1, phi2))
        assert pu.as1.get_formula_depth(phi=phi3) == 3
