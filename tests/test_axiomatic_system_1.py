import pytest
import punctilious as pu
from punctilious.connectives_standard_library_1 import *


# from punctilious.axiomatic_system_1 import is_formula_equivalent, is_in_map_domain


@pytest.fixture
def c1():
    return pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(
        connective_typesetter='c1'))


@pytest.fixture
def c2():
    return pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(
        connective_typesetter='c2'))


@pytest.fixture
def c3():
    return pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(
        connective_typesetter='c3'))


@pytest.fixture
def apple():
    return pu.as1.let_x_be_a_simple_object(formula_ts='apple')


@pytest.fixture
def ananas():
    return pu.as1.let_x_be_a_simple_object(formula_ts='ananas')


@pytest.fixture
def strawberry():
    return pu.as1.let_x_be_a_simple_object(formula_ts='strawberry')


@pytest.fixture
def blueberry():
    return pu.as1.let_x_be_a_simple_object(formula_ts='blueberry')


@pytest.fixture
def fruits(apple, ananas, blueberry, strawberry):
    fruits = pu.as1.Enumeration(elements=(apple, ananas, blueberry, strawberry))
    return fruits


class TestConnective:
    def test_connective(self, c1, c2):
        assert c1 is not c2

    def test_simple(self):
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        x = a.__str__()
        pass

    def test_call(self):
        x, y, z = pu.as1.let_x_be_a_variable(formula_ts=('x', 'y', 'z',))
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_unary_connective(formula_ts='f')
        g = pu.as1.let_x_be_a_binary_connective(formula_ts='g')
        h = pu.as1.let_x_be_a_ternary_connective(formula_ts='h')
        assert pu.as1.is_formula_equivalent(phi=f(), psi=pu.as1.Formula(c=f, t=None))
        assert pu.as1.is_formula_equivalent(phi=g(x), psi=pu.as1.Formula(c=g, t=(x,)))
        assert pu.as1.is_formula_equivalent(phi=h(x, y), psi=pu.as1.Formula(c=h, t=(x, y,)))


class TestIsSubformulaFormula:
    def test_is_subformula_of_formula(self):
        c1 = pu.as1.FreeArityConnective(formula_ts='c1')
        c2 = pu.as1.FreeArityConnective(formula_ts='c2')
        c3 = pu.as1.FreeArityConnective(formula_ts='c3')
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
        a, b, c = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c',))
        c1 = pu.as1.BinaryConnective(formula_ts='c1')
        c2 = pu.as1.BinaryConnective(formula_ts='c2')
        phi = a | c1 | b
        assert pu.as1.is_connective_equivalent(phi=phi, psi=phi)
        psi = b | c1 | c
        assert pu.as1.is_connective_equivalent(phi=phi, psi=psi)
        omega = a | c2 | b
        assert not pu.as1.is_connective_equivalent(phi=phi, psi=omega)


class TestFormulaEquivalence:
    def test_is_formula_equivalent(self):
        pass


class TestTupl:
    def test_tupl(self):
        pass

    def test_in(self):
        x = pu.as1.let_x_be_a_variable(formula_ts='x')
        y = pu.as1.let_x_be_a_variable(formula_ts='y')
        c = pu.as1.Tupl(elements=(x,))
        assert x in c
        assert y not in c
        assert len(c) == 1


class TestEnumeration:
    def test_enumeration(self):
        pass

    def test_has_element(self):
        c1 = pu.as1.let_x_be_a_binary_connective(formula_ts='c1')
        c2 = pu.as1.let_x_be_a_binary_connective(formula_ts='c2')
        x = pu.as1.let_x_be_a_simple_object(formula_ts='x')
        y = pu.as1.let_x_be_a_simple_object(formula_ts='y')
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
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        b = pu.as1.let_x_be_a_simple_object(formula_ts='b')
        c = pu.as1.let_x_be_a_simple_object(formula_ts='c')
        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_AS1_029):
            # duplicate formula-equivalent formulas are forbidden in enumerations.
            e1 = pu.as1.Enumeration(elements=(a, b, c, b,))

    def test_enumeration(self):
        a, b, c, x, y, z = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'x', 'y', 'z',))
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
        a, b, c = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c',))
        star = pu.as1.FreeArityConnective(formula_ts='*')
        phi1 = pu.as1.Formula(c=star, t=(a, b, c,))
        assert pu.as1.is_well_formed_enumeration(e=phi1)
        phi2 = pu.as1.Formula(c=star, t=None)
        assert pu.as1.is_well_formed_enumeration(e=phi2)
        phi3 = pu.as1.Formula(c=star, t=(a, a, b, c,))
        assert not pu.as1.is_well_formed_enumeration(e=phi3)
        phi4 = pu.as1.Formula(c=star, t=(a, b, b, c,))
        assert not pu.as1.is_well_formed_enumeration(e=phi4)
        phi5 = pu.as1.Formula(c=star, t=(a, b, c, c,))
        assert not pu.as1.is_well_formed_enumeration(e=phi5)


class TestFormulaEquivalenceWithVariables:
    def test_is_formula_equivalent_with_variables(self):
        x = pu.as1.let_x_be_a_variable(formula_ts='x')
        y = pu.as1.let_x_be_a_variable(formula_ts='y')
        is_a = pu.as1.let_x_be_a_binary_connective(formula_ts='is-a')
        human = pu.as1.let_x_be_a_simple_object(formula_ts='human')
        platypus = pu.as1.let_x_be_a_simple_object(formula_ts='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_ts='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_ts='aristotle')
        assert pu.as1.is_formula_equivalent_with_variables(
            phi=aristotle | is_a | human,
            psi=aristotle | is_a | human,
            variables=())
        with pytest.raises(pu.u1.ApplicativeError):
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
        with pytest.raises(pu.u1.ApplicativeError):
            # the following is ill-formed because the variable is an element of phi, and not of psi.
            # reminder: formula-equivalence-with-variables is non-commutative.
            assert not pu.as1.is_formula_equivalent_with_variables(
                phi=aristotle | is_a | x,
                psi=platypus | is_a | human,
                variables=(x,))

    def test_is_formula_equivalent_with_variables_2(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        ab = pu.as1.Tupl(elements=(a, b,))
        cd = pu.as1.Tupl(elements=(c, d,))
        assert not pu.as1.is_formula_equivalent(phi=ab, psi=cd)
        m = pu.as1.Map()
        is_equivalent, m = pu.as1.is_formula_equivalent_with_variables_2(phi=ab, psi=cd, variables=(c, d,),
                                                                         variables_fixed_values=m)
        assert is_equivalent
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=m, preimage=c), psi=a)
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=m, preimage=d), psi=b)
        bba = pu.as1.Tupl(elements=(b, b, a,))
        cca = pu.as1.Tupl(elements=(c, c, a,))
        m = pu.as1.Map()
        is_equivalent, m = pu.as1.is_formula_equivalent_with_variables_2(phi=bba, psi=bba, variables=(),
                                                                         variables_fixed_values=m)
        assert is_equivalent
        m = pu.as1.Map()
        is_equivalent, m = pu.as1.is_formula_equivalent_with_variables_2(phi=bba, psi=cca, variables=(c,),
                                                                         variables_fixed_values=m)
        assert is_equivalent
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=m, preimage=c), psi=b)
        ababbba = pu.as1.Tupl(elements=(a, b, a, b, b, a,))
        acaccca = pu.as1.Tupl(elements=(a, c, a, c, c, a,))
        m = pu.as1.Map()
        is_equivalent, m = pu.as1.is_formula_equivalent_with_variables_2(phi=ababbba, psi=acaccca, variables=(c,),
                                                                         variables_fixed_values=m)
        assert is_equivalent
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=m, preimage=c), psi=b)
        multilevel1 = pu.as1.Tupl(elements=(a, b, a, b, b, c, c,))
        multilevel2 = pu.as1.Tupl(elements=(a, multilevel1, a, multilevel1, c,))
        multilevel3 = pu.as1.Tupl(elements=(c, multilevel2, a, multilevel1,))
        print(multilevel3)
        test = pu.as1.replace_formulas(phi=multilevel3, m={a: e, b: d})
        m = pu.as1.Map()
        is_equivalent, m = pu.as1.is_formula_equivalent_with_variables_2(phi=multilevel3, psi=test, variables=(d, e,),
                                                                         variables_fixed_values=m)
        assert is_equivalent
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=m, preimage=d), psi=b)
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=m, preimage=e), psi=a)


class TestFormulaEquivalenceWithVariables2:
    def test_is_formula_equivalent_with_variables(self):
        x = pu.as1.let_x_be_a_variable(formula_ts='x')
        y = pu.as1.let_x_be_a_variable(formula_ts='y')
        is_a = pu.as1.let_x_be_a_binary_connective(
            formula_ts=pu.as1.InfixFormulaTypesetter(connective_ts='is-a'))
        human = pu.as1.let_x_be_a_simple_object(formula_ts='human')
        platypus = pu.as1.let_x_be_a_simple_object(formula_ts='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_ts='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_ts='aristotle')

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
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=x), psi=human)

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
        a, b, c, d, e, = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        ab = pu.as1.Tupl(elements=(a, b,))
        cd = pu.as1.Tupl(elements=(c, d,))
        assert not pu.as1.is_formula_equivalent(phi=ab, psi=cd)
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(
            phi=ab, psi=cd,
            variables=(c, d,),
            variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=c), psi=a)
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=d), psi=b)

        bba = pu.as1.Tupl(elements=(b, b, a,))
        cca = pu.as1.Tupl(elements=(c, c, a,))
        m = pu.as1.Map()
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=bba, psi=bba, variables=(),
                                                                     variables_fixed_values=None)
        assert result

        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=bba, psi=cca, variables=(c,),
                                                                     variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=c), psi=b)

        ababbba = pu.as1.Tupl(elements=(a, b, a, b, b, a,))
        acaccca = pu.as1.Tupl(elements=(a, c, a, c, c, a,))
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=ababbba, psi=acaccca, variables=(c,),
                                                                     variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=c), psi=b)

        multilevel1 = pu.as1.Tupl(elements=(a, b, a, b, b, c, c,))
        multilevel2 = pu.as1.Tupl(elements=(a, multilevel1, a, multilevel1, c,))
        multilevel3 = pu.as1.Tupl(elements=(c, multilevel2, a, multilevel1,))
        print(multilevel3)
        test = pu.as1.replace_formulas(phi=multilevel3, m={a: e, b: d})
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=multilevel3, psi=test, variables=(d, e,),
                                                                     variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=d), psi=b)
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=e), psi=a)


class TestReplaceConnectives:
    def test_replace_connectives(self):
        c1 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(connective_typesetter='c1'))
        c2 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(connective_typesetter='c2'))
        c3 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(connective_typesetter='c3'))
        c4 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(connective_typesetter='c4'))
        d1 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(connective_typesetter='d1'))
        d2 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(connective_typesetter='d2'))
        d3 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(connective_typesetter='d3'))
        d4 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(connective_typesetter='d4'))
        phi = c1(c2(c3, c3, c3, c1, c4(c3, c2, c1)), c3)
        m = pu.as1.Map(d=(c1, c2, c3, c4,), c=(d1, d2, d3, d4,))
        psi = pu.as1.replace_connectives(phi=phi, m=m)
        n = pu.as1.Map(d=(d1, d2, d3, d4,), c=(c1, c2, c3, c4,))
        phi2 = pu.as1.replace_connectives(phi=psi, m=n)
        assert pu.as1.is_formula_equivalent(phi=phi, psi=phi2)
        pass


class TestNaturalTransformation:
    def test_natural_transformation(self):
        x = pu.as1.let_x_be_a_variable(formula_ts='x')
        y = pu.as1.let_x_be_a_variable(formula_ts='y')
        is_a = pu.as1.let_x_be_a_binary_connective(
            formula_ts=pu.as1.typesetters.infix_formula(connective_typesetter='is-a'))
        human = pu.as1.let_x_be_a_simple_object(formula_ts='human')
        platypus = pu.as1.let_x_be_a_simple_object(formula_ts='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_ts='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_ts='aristotle')
        p1 = x | is_a | human
        p2 = aristotle | is_a | human
        premises = pu.as1.Enumeration(elements=(p1,))
        conclusion = x | is_a | mortal
        variables = pu.as1.Enumeration(elements=(x,))
        f = pu.as1.NaturalTransformation(c=conclusion, v=variables, d=None,
                                         p=premises)
        arguments = pu.as1.Tupl(elements=(p2,))
        output = f.apply_transformation(p=arguments)
        phi = aristotle | is_a | mortal
        pu.as1.is_formula_equivalent(phi=phi, psi=output)

    def test_is_well_formed_natural_transformation(self):
        x = pu.as1.let_x_be_a_variable(formula_ts='x')
        y = pu.as1.let_x_be_a_variable(formula_ts='y')
        is_a = pu.as1.let_x_be_a_binary_connective(
            formula_ts=pu.as1.typesetters.infix_formula(connective_typesetter='is-a'))
        human = pu.as1.let_x_be_a_simple_object(formula_ts='human')
        platypus = pu.as1.let_x_be_a_simple_object(formula_ts='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_ts='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_ts='aristotle')
        p1 = x | is_a | human
        p2 = aristotle | is_a | human
        conclusion = x | is_a | mortal
        variables = pu.as1.Enumeration(elements=(x,))
        declarations = pu.as1.Enumeration(elements=None)
        premises = pu.as1.Tupl(elements=(p1,))
        phi1 = pu.as1._connectives.natural_transformation(conclusion, variables, declarations, premises)
        assert pu.as1.is_well_formed_natural_transformation(t=phi1)
        phi1 = pu.as1.coerce_natural_transformation(t=phi1)
        conclusion = x | is_a | mortal
        variables = pu.as1.Enumeration(elements=(x,))
        declarations = pu.as1.Enumeration(elements=None)
        premises = pu.as1.Tupl(elements=(platypus, platypus,))
        phi2 = pu.as1._connectives.natural_transformation(conclusion, variables, declarations, premises, premises)
        assert not pu.as1.is_well_formed_natural_transformation(t=phi2)


class TestReplaceFormulas:
    def test_replace_formulas(self):
        land = pu.as1.let_x_be_a_binary_connective(formula_ts='land')
        x = pu.as1.let_x_be_a_variable(formula_ts='x')
        y = pu.as1.let_x_be_a_variable(formula_ts='y')
        is_a = pu.as1.let_x_be_a_binary_connective(formula_ts='is-a')
        human = pu.as1.let_x_be_a_simple_object(formula_ts='human')
        animal = pu.as1.let_x_be_a_simple_object(formula_ts='animal')
        platypus = pu.as1.let_x_be_a_simple_object(formula_ts='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_ts='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_ts='aristotle')
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
        a, b, c, d = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd',))
        c1 = pu.as1.let_x_be_a_unary_connective(formula_ts='c1')
        c2 = pu.as1.let_x_be_a_binary_connective(formula_ts='c2')
        phi = a | c2 | b
        psi = pu.as1.replace_formulas(phi=phi, m={a: c, b: d})
        assert pu.as1.is_formula_equivalent(phi=c | c2 | d, psi=psi)
        phi = (b | c2 | a) | c2 | ((a | c2 | b) | c2 | (a | c2 | a))
        psi = pu.as1.replace_formulas(phi=phi, m={a: c, b: d})
        assert pu.as1.is_formula_equivalent(phi=(d | c2 | c) | c2 | ((c | c2 | d) | c2 | (c | c2 | c)), psi=psi)


class TestMap:
    def test_map(self, fruits):
        red, yellow, blue = pu.as1.let_x_be_some_simple_objects(reps=('red', 'yellow', 'blue',))
        c = pu.as1.Tupl(elements=(red, yellow, blue, red))
        m1 = pu.as1.Map(d=fruits, c=c)
        assert len(m1) == 2
        assert pu.as1.is_in_map_domain(phi=fruits[0], m=m1)
        assert pu.as1.is_in_map_domain(phi=fruits[1], m=m1)
        assert pu.as1.is_in_map_domain(phi=fruits[2], m=m1)
        assert pu.as1.is_in_map_domain(phi=fruits[3], m=m1)
        assert pu.as1.is_formula_equivalent(pu.as1.get_image_from_map(m=m1, preimage=fruits[0]), red)
        assert pu.as1.is_formula_equivalent(pu.as1.get_image_from_map(m=m1, preimage=fruits[1]), yellow)
        assert pu.as1.is_formula_equivalent(pu.as1.get_image_from_map(m=m1, preimage=fruits[2]), blue)
        assert pu.as1.is_formula_equivalent(pu.as1.get_image_from_map(m=m1, preimage=fruits[3]), red)
        m1 = pu.as1.reduce_map(m=m1, preimage=fruits[2])
        assert pu.as1.is_in_map_domain(phi=fruits[0], m=m1)
        assert pu.as1.is_in_map_domain(phi=fruits[1], m=m1)
        assert not pu.as1.is_in_map_domain(phi=fruits[2], m=m1)
        assert pu.as1.is_in_map_domain(phi=fruits[3], m=m1)
        m1 = pu.as1.append_pair_to_map(m=m1, preimage=fruits[3], image=yellow)
        assert pu.as1.is_formula_equivalent(pu.as1.get_image_from_map(m=m1, preimage=fruits[0]), red)
        assert pu.as1.is_formula_equivalent(pu.as1.get_image_from_map(m=m1, preimage=fruits[1]), yellow)
        assert pu.as1.is_formula_equivalent(pu.as1.get_image_from_map(m=m1, preimage=fruits[3]), yellow)
        pass


class TestEnumerationEquivalence:
    def test_enumeration_equivalence(self):
        red, yellow, blue = pu.as1.let_x_be_some_simple_objects(reps=('red', 'yellow', 'blue',))
        e1 = pu.as1.Enumeration(elements=(red, yellow, blue,))
        e2 = pu.as1.Enumeration(elements=(yellow, red, blue,))
        assert pu.as1.is_enumeration_equivalent(phi=e1, psi=e2)
        assert not pu.as1.is_formula_equivalent(phi=e1, psi=e2)


class TestUnionEnumeration:
    def test_union_enumeration(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
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
        x, y, z = pu.as1.let_x_be_some_simple_objects(reps=('x', 'y', 'z',))
        assert not a.has_element(phi=x)
        assert a.arity == 0


class TestInferenceRule:
    def test_inference_rule_without_premises(self):
        # elaborate a theory
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_binary_connective(formula_ts='f')
        phi = a | f | b
        rule = pu.as1.NaturalTransformation(c=phi, v=None, d=None, p=None)
        ir = pu.as1.InferenceRule(t=rule)
        axiomatization = pu.as1.Axiomatization(d=(ir,))

        # derivation from the axiom
        i = pu.as1.Inference(p=None, i=ir)
        isolated_theorem = pu.as1.Theorem(valid_statement=phi, i=i)
        t = pu.as1.append_to_theory(isolated_theorem, t=axiomatization)
        assert pu.as1.is_formula_equivalent(
            phi=isolated_theorem.valid_statement,
            psi=phi)

    def test_is_well_formed_postulation(self):
        a, b = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b',))
        f = pu.as1.let_x_be_a_binary_connective(formula_ts='f')
        rule = pu.as1.NaturalTransformation(c=a | f | b, v=None, d=None, p=None)
        phi1 = rule | pu.as1._connectives.follows_from | pu.as1._connectives.inference_rule
        assert pu.as1.is_well_formed_inference_rule(i=phi1)

        # incorrect connective
        phi2 = pu.as1.Formula(c=pu.as1._connectives.inference, t=(pu.as1._connectives.inference_rule, rule,))
        assert not pu.as1.is_well_formed_inference_rule(i=phi2)

        # incorrect axiomatic-postulation
        phi3 = rule | pu.as1._connectives.follows_from | pu.as1._connectives.enumeration
        assert not pu.as1.is_well_formed_inference_rule(i=phi3)


class TestFormulaToTuple:
    def test_formula_to_tuple(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_unary_connective(formula_ts='f')
        g = pu.as1.let_x_be_a_binary_connective(formula_ts='g')
        h = pu.as1.let_x_be_a_ternary_connective(formula_ts='h')
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
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        star3 = pu.as1.let_x_be_a_ternary_connective(formula_ts='*3')
        rule1 = pu.as1.NaturalTransformation(c=star3(e, b, d), v=None, d=None,
                                             p=None)
        phi1 = rule1 | pu.as1._connectives.follows_from | pu.as1._connectives.inference_rule
        assert pu.as1.is_well_formed_inference_rule(i=phi1)
        phi2 = rule1 | pu.as1._connectives.map_formula | pu.as1._connectives.inference_rule
        assert not pu.as1.is_well_formed_inference_rule(i=phi2)
        phi3 = rule1 | pu.as1._connectives.follows_from | b
        assert not pu.as1.is_well_formed_inference_rule(i=phi3)


class TestTheorem:
    def test_coerce_theorem(self):
        t = pu.as1.let_x_be_a_theory()
        a, b = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b',))
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=a)
        i = pu.as1.InferenceRule(t=pu.as1.NaturalTransformation(c=b, p=(a,)))
        t = pu.as1.append_to_theory(i, t=t)
        i2 = pu.as1.Inference(p=(a,), i=i)
        # For the purpose of this test,
        # build the theorem manually,
        # i.e. without using a derivation function.
        m = pu.as1.Theorem(valid_statement=b, i=i2)
        m = pu.as1.coerce_theorem(t=m)
        m2 = b | follows_from | i2
        assert pu.as1.is_formula_equivalent(phi=m, psi=m2)
        m2 = pu.as1.coerce_theorem(t=m2)
        t = pu.as1.append_to_theory(m, t=t)
        pass


class TestInference:
    def test_inference(self):
        x, y, z = pu.as1.let_x_be_a_variable(formula_ts=('x', 'y', 'z',))
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_binary_connective(formula_ts='f')
        t = pu.as1.NaturalTransformation(c=x | f | z, v=(x, y, z,), d=None,
                                         p=(x | f | y, y | f | z,), )
        p = (a | f | b, b | f | c,)
        theorem = a | f | c
        pu.as1.is_formula_equivalent(phi=theorem, psi=t(p=p, a=None))
        inference_rule = pu.as1.InferenceRule(t=t)
        inference = pu.as1.Inference(i=inference_rule, p=p, a=None)
        theorem_2 = pu.as1.Theorem(valid_statement=theorem, i=inference)
        pu.as1.is_formula_equivalent(
            phi=theorem_2,
            psi=theorem | pu.as1._connectives.follows_from | pu.as1._connectives.inference(inference_rule, p,
                                                                                           pu.as1.Tupl()))

    def test_is_well_formed_inference(self):
        x, y, z = pu.as1.let_x_be_a_variable(formula_ts=('x', 'y', 'z',))
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_binary_connective(formula_ts='f')
        t = pu.as1.NaturalTransformation(c=x | f | z, v=(x, y, z,), d=None,
                                         p=(x | f | y, y | f | z,))
        p = (a | f | b, b | f | c,)
        i = pu.as1.InferenceRule(t=t)
        phi1 = pu.as1._connectives.inference(i, p, as1.Tupl())
        assert pu.as1.is_well_formed_inference(i=phi1)
        phi2 = pu.as1._connectives.inference(i, as1.Tupl())
        assert not pu.as1.is_well_formed_inference(i=phi2)
        phi3 = p | pu.as1._connectives.follows_from | i
        assert not pu.as1.is_well_formed_inference(i=phi3)
        phi4 = f(a, a, b, b) | pu.as1._connectives.follows_from | i
        assert not pu.as1.is_well_formed_inference(i=phi4)


class TestProofByInference:
    def test_is_well_formed(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        x, y, z = pu.as1.let_x_be_a_variable(formula_ts=('x', 'y', 'z',))
        star = pu.as1.let_x_be_a_binary_connective(
            formula_ts=pu.as1.typesetters.infix_formula(connective_typesetter=pu.pl1.symbols.asterisk_operator))
        premises = pu.as1.Enumeration(elements=(x | star | y, y | star | z,))
        conclusion = x | star | z
        variables = pu.as1.Enumeration(elements=(x, y, z,))
        f = pu.as1.NaturalTransformation(c=conclusion, v=variables, d=None,
                                         p=premises)
        ir = pu.as1.InferenceRule(t=f)
        p = (a | star | b, b | star | c,)
        i = pu.as1.Inference(p=p, i=ir)
        outcome = f.apply_transformation(p=p)
        m = pu.as1.Theorem(valid_statement=a | star | c, i=i)
        assert pu.as1.is_well_formed_theorem(t=m)
        assert pu.as1.is_well_formed_theorem(t=(a | star | c) | pu.as1._connectives.follows_from | i)

        i2 = pu.as1.Inference(p=(a | star | b, b | star | a,), i=ir)
        assert not pu.as1.is_well_formed_theorem(t=(a | star | c) | pu.as1._connectives.follows_from | i2)
        pass


class TestAlgorithm:
    def test_algorithm(self):
        def x_is_a_theory(p: pu.as1.Tupl | None = None, a: pu.as1.Tupl | None = None):
            p = as1.coerce_tupl(t=p)
            a = as1.coerce_tupl(t=a)
            if not a.arity == 1:
                raise pu.u1.ApplicativeError(msg='wrong arguments', p=p, type_p=type(p), a=a, type_a=type(a))
            t = a[0]
            if as1.is_well_formed_theory(t=t):
                t = as1.coerce_theory(t=t)
                phi = is_well_formed_theory_predicate(t)
                return phi
            else:
                phi = lnot(theory_predicate(t))
                return phi

        t = as1.let_x_be_a_theory()
        m = as1.let_x_be_a_theory()
        with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='x')) as x:
            algo = as1.AlgorithmicTransformation(external_algorithm=x_is_a_theory,
                                                 c=is_well_formed_theory_predicate(x),
                                                 v={x, },
                                                 d={x, })
        i = as1.InferenceRule(t=algo)
        m, i = as1.let_x_be_an_inference_rule(t1=m, i=i)
        c = is_well_formed_theory_predicate(t)
        m, d = as1.derive_1(t=m, c=c, p=None, i=i, a=(t,))
        pass


class TestIteratePermutationsOfEnumerationElementsWithFixedSize:
    def test_iterate_permutations_of_enumeration_elements_with_fixed_size(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))

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
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        t, _, = pu.as1.let_x_be_an_axiom(t=None, s=a)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=c)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=d)
        assert pu.as1.are_valid_statements_in_theory(s=(a, c,), t=t)
        assert pu.as1.are_valid_statements_in_theory(s=(a, c, d,), t=t)
        assert pu.as1.are_valid_statements_in_theory(s=(d, a, c,), t=t)
        assert pu.as1.are_valid_statements_in_theory(s=None, t=t)
        assert not pu.as1.are_valid_statements_in_theory(s=(e,), t=t)
        assert not pu.as1.are_valid_statements_in_theory(s=(a, b, d,), t=t)
        assert not pu.as1.are_valid_statements_in_theory(s=(a, e, b,), t=t)


class TestAreValidStatementsInTheoryWithVariables:
    def test_are_valid_statements_in_theory_with_variables(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        t, _, = pu.as1.let_x_be_an_axiom(t=None, s=a)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=c)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=d)
        valid, s, = pu.as1.are_valid_statements_in_theory_with_variables(s=(a, c,), t=t, variables=None,
                                                                         variables_values=None)
        assert valid
        valid, s, = pu.as1.are_valid_statements_in_theory_with_variables(s=(a, c, e,), t=t, variables=(e,),
                                                                         variables_values=pu.as1.Map(d=(e,),
                                                                                                     c=(d,)))
        assert valid
        valid, s, = pu.as1.are_valid_statements_in_theory_with_variables(s=(a, c, e,), t=t, variables=(e,),
                                                                         variables_values=None)
        assert valid


class TestStripDuplicateFormulasInPythonTuple:
    def test_strip_duplicate_formulas_in_python_tuple(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        t1 = pu.as1.Tupl(elements=(a, b, a, a, e, e,))
        t2 = pu.as1.Tupl(elements=(a, b, e,))
        t3 = pu.as1.strip_duplicate_formulas_in_python_tuple(t=t1)
        t3 = pu.as1.Tupl(elements=t3)
        assert not pu.as1.is_formula_equivalent(phi=t1, psi=t3)
        assert pu.as1.is_formula_equivalent(phi=t2, psi=t3)


class TestCoerceEnumeration:
    def test_coerce_enumeration(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        e1 = pu.as1.Enumeration(elements=(a, b, a, a, e, e,), strip_duplicates=True)
        e2 = pu.as1.Enumeration(elements=(a, b, e,), strip_duplicates=True)
        e3 = pu.as1.Enumeration(elements=e1, strip_duplicates=True)
        assert pu.as1.is_formula_equivalent(phi=e1, psi=e3)
        assert pu.as1.is_formula_equivalent(phi=e2, psi=e3)
        assert pu.as1.is_formula_equivalent(phi=e1, psi=e2)


class TestAxiomatization:
    def test_is_well_formed(self):
        # elaborate a theory
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        x, y, z = pu.as1.let_x_be_a_variable(formula_ts=('x', 'y', 'z',))
        star1 = pu.as1.let_x_be_a_unary_connective(formula_ts='*1')
        star2 = pu.as1.let_x_be_a_binary_connective(formula_ts='*2')
        axiom_ok_1 = pu.as1.Axiom(valid_statement=a | star2 | b)
        axiom_ok_2 = pu.as1.Axiom(valid_statement=star1(c))
        assert pu.as1.is_well_formed_axiom(a=axiom_ok_2)

        # simple case
        e1 = pu.as1.Enumeration(elements=(axiom_ok_1, axiom_ok_2,))
        e1 = pu.as1.Axiomatization(d=e1)
        assert pu.as1.is_well_formed_axiomatization(a=e1)

        # extreme case: the empty enumeration
        e2 = pu.as1.Enumeration()
        e2 = pu.as1.Axiomatization(d=e2)
        assert pu.as1.is_well_formed_axiomatization(a=e2)
        a1 = pu.as1.Axiomatization(d=(axiom_ok_1, axiom_ok_2,))  # does not raise an exception

        # bad case: an enumeration with a non-axiom
        e3 = pu.as1.Enumeration(elements=(axiom_ok_1, axiom_ok_2, star1(e),))
        assert not pu.as1.is_well_formed_axiomatization(a=e3)
        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_AS1_047):
            a2 = pu.as1.Axiomatization(d=e3)  # raise an e123 exception


class TestDemonstration:
    def test_is_well_formed(self):
        # elaborate a theory
        theory = pu.as1.let_x_be_a_collection_of_axioms(axioms=None)
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        x, y, z = pu.as1.let_x_be_a_variable(formula_ts=('x', 'y', 'z',))
        star = pu.as1.let_x_be_a_binary_connective(formula_ts='*')
        theory, axiom_1, = pu.as1.let_x_be_an_axiom(t=theory, s=a | star | b)
        theory, axiom_2, = pu.as1.let_x_be_an_axiom(t=theory, s=b | star | c)
        theory, ir1, = pu.as1.let_x_be_an_inference_rule(t1=theory,
                                                         p=(x | star | y,
                                                            y | star | z,),
                                                         c=x | star | z,
                                                         v=(x, y, z,))

        # derive a theorem
        demo2, _, = pu.as1.derive_1(t=theory,
                                    c=a | star | c,
                                    p=(
                                        a | star | b,
                                        b | star | c,),
                                    i=ir1)
        assert pu.as1.is_valid_statement_in_theory(phi=a | star | c, t=demo2)

        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_AS1_039):
            # invalid proof raise exception
            pu.as1.Theory(d=(axiom_1, axiom_2, a | star | e))

        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_AS1_039):
            # invalid proof sequence exception
            pu.as1.Theory(d=(axiom_1, axiom_2, a | star | c, ir1,))
            pass


class TestVariable:
    def test_variable(self):
        with pu.as1.let_x_be_a_variable(formula_ts='x') as x:
            print(x)
        with pu.as1.let_x_be_a_variable(formula_ts='x') as x, pu.as1.let_x_be_a_variable(
                formula_ts='y') as y:
            print(x)
            print(y)
            pass


class TestAutoDerivation:
    def test_auto_derivation(self):
        # elaborate a theory
        p = pu.as1.let_x_be_a_simple_object(formula_ts='P')
        q = pu.as1.let_x_be_a_simple_object(formula_ts='Q')
        t1, a1 = pu.as1.let_x_be_an_axiom(t=None, a=pu.as1.Axiom(valid_statement=p))

        t1, success, _, = pu.as1.derive_0(t=t1, c=p)

        if_p_then_q = pu.as1.InferenceRule(
            t=pu.as1.NaturalTransformation(c=q, v=(), d=None, p=(p,)))
        t1 = pu.as1.append_to_theory(if_p_then_q, t=t1)

        with pu.as1.let_x_be_a_variable(formula_ts='x') as x, pu.as1.let_x_be_a_variable(
                formula_ts='y') as y:
            x_y_then_x_and_y = pu.as1.InferenceRule(
                t=pu.as1.NaturalTransformation(c=x | pu.as1._connectives.land | y, v=(x, y,),
                                               d=None, p=(x, y,)))
        t1 = pu.as1.Theory(d=(*t1, x_y_then_x_and_y,))

        pass
        # auto-derivation of an existing valid-statement
        t2, success, _, = pu.as1.derive_0(t=t1, c=p)
        assert success
        pass
        # auto-derivation of a simple theorem, without variables
        t2, success, _, = pu.as1.derive_2(t=t2, c=q, i=if_p_then_q)
        assert success
        pass

        # auto-derivation of a simple theorem, without some variables
        t2, success, _, = pu.as1.auto_derive_2(t=t2, conjecture=p | pu.as1._connectives.land | q)
        assert success
        pass
        # auto-derivation of an impossible theorem fails and raises an auto-derivation-failure
        t2, success, _, = pu.as1.auto_derive_2(t=t2, conjecture=p | pu.as1._connectives.lor | q)
        assert not success
        pass

        # use auto-derivation-2
        t3, success, derivation, _ = pu.as1.auto_derive_4(t=t1, conjecture=p | pu.as1._connectives.land | q,
                                                          max_recursion=8, debug=False)
        assert success
        pass

        t3, success, derivation, _ = pu.as1.auto_derive_4(t=t1, conjecture=p | pu.as1._connectives.lor | q,
                                                          max_recursion=8, debug=False)
        assert not success
        pass


class TestFormulaDepth:
    def test_get_formula_depth(self):
        c = pu.as1.FreeArityConnective(formula_ts=pu.pl1.symbols.x_uppercase_serif_italic)
        phi1 = pu.as1.Formula(c=c, t=None)
        assert pu.as1.get_formula_depth(phi=phi1) == 1
        phi2 = pu.as1.Formula(c=c, t=(phi1, phi1,))
        assert pu.as1.get_formula_depth(phi=phi2) == 2
        phi3 = pu.as1.Formula(c=c, t=(phi1, phi2, phi1, phi2))
        assert pu.as1.get_formula_depth(phi=phi3) == 3


class TestMetaTheory:
    def test_meta_theory(self):
        t = pu.ml1.let_x_be_a_minimal_logic_1_theory()
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='P')
        pass
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=p)
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=lnot(p))  # This is a contradiction!
        # Let's prove t is inconsistent
        m = pu.as1.let_x_be_a_meta_theory(d=None)
        m = pu.as1.let_x_be_a_sub_theory_of_y(t=t, m=m)
        ## m, d = pu.as1.derive_1()
        ## TODO: Come back here and complete development.
        pass


class TestObjectCreation:
    def test_object_creation(self):
        if 1 == 2:
            t = as1.let_x_be_a_theory()
            x = as1.let_x_be_a_new_object()
            t2 = as1.NaturalTransformation(c=x | is_a | propositional_variable, v=(x,),
                                           d=(x,),
                                           p=None)
            # rule 1: a variable x in the enumeration of variables car either be listed in declarations,
            #   exclusive-or be referenced in premises, exclusive-or not be referenced.
            # rule 2: a new object in creations must not be present in previous derivations in the theory,
            #   otherwise it would be possible to "create the same object multiple times" which doesn't make sense.
            a = as1.let_x_be_an_axiom(t=t, a=a)
            t, _ = as1.derive_1(t=t, c=x | is_a | propositional_variable, )
