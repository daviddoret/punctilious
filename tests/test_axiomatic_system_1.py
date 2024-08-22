import pytest
import punctilious as pu
from punctilious.connectives_standard_library_1 import *


# from punctilious.axiomatic_system_1 import is_formula_equivalent, is_in_map_domain


@pytest.fixture
def c123():
    c1 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(
        connective_typesetter='c1'))
    c2 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(
        connective_typesetter='c2'))
    c3 = pu.as1.Connective(formula_ts=pu.as1.typesetters.classical_formula(
        connective_typesetter='c3'))
    return c1, c2, c3


@pytest.fixture
def fruits():
    apple = pu.as1.let_x_be_a_simple_object(formula_ts='apple')
    ananas = pu.as1.let_x_be_a_simple_object(formula_ts='ananas')
    strawberry = pu.as1.let_x_be_a_simple_object(formula_ts='strawberry')
    blueberry = pu.as1.let_x_be_a_simple_object(formula_ts='blueberry')
    return apple, ananas, strawberry, blueberry


class TestConnective:
    def test_connective(self, c123):
        c1, c2, c3, = c123
        assert c1 is not c2

    def test_simple(self):
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        x = a.__str__()
        pass

    def test_call(self):
        x, y, z = pu.as1.let_x_be_some_variables(reps=('x', 'y', 'z',))
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_unary_connective(formula_ts='f')
        g = pu.as1.let_x_be_a_binary_connective(formula_ts='g')
        h = pu.as1.let_x_be_a_ternary_connective(formula_ts='h')
        assert pu.as1.is_formula_equivalent(phi=f(), psi=pu.as1.WellFormedFormula(con=f, t=None))
        assert pu.as1.is_formula_equivalent(phi=g(x), psi=pu.as1.WellFormedFormula(con=g, t=(x,)))
        assert pu.as1.is_formula_equivalent(phi=h(x, y), psi=pu.as1.WellFormedFormula(con=h, t=(x, y,)))


class TestIsSubformulaFormula:
    def test_is_subformula_of_formula(self):
        c1 = pu.as1.FreeArityConnective(formula_ts='c1')
        c2 = pu.as1.FreeArityConnective(formula_ts='c2')
        c3 = pu.as1.FreeArityConnective(formula_ts='c3')
        assert pu.as1.is_recursively_included_in(
            s=c1(c2, c3, c2(c1)),
            f=c1(c2, c3, c2(c1))
        )
        assert not pu.as1.is_recursively_included_in(
            s=c1(c2, c3, c2(c2)),
            f=c1(c2, c3, c2(c1))
        )
        assert pu.as1.is_recursively_included_in(
            s=c2(c2),
            f=c1(c2, c3, c2(c2))
        )
        assert pu.as1.is_recursively_included_in(
            s=c3(c2, c1),
            f=c1(c2, c3(c2(c1(c3(c2, c1)))), c2(c2))
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
        c = pu.as1.WellFormedTupl(e=(x,))
        assert x in c
        assert y not in c
        assert len(c) == 1

    def test_iterate(self):
        a, b, c, d, e, f = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e', 'f',))
        phi1 = pu.as1.WellFormedTupl(e=(a, b, c, d, e, f,))
        assert a in phi1
        assert len(phi1) == 6
        assert len(tuple(pu.as1.iterate_tuple_elements(phi=phi1))) == 6
        assert len(tuple(pu.as1.iterate_tuple_elements(phi=phi1, max_elements=0))) == 0
        assert len(tuple(pu.as1.iterate_tuple_elements(phi=phi1, max_elements=2))) == 2
        assert len(tuple(pu.as1.iterate_tuple_elements(phi=phi1, max_elements=6))) == 6
        phi2 = pu.as1.WellFormedTupl(e=(f, f, a, b, d, e, b, b, f,))
        assert a in phi2
        assert len(phi2) == 9
        assert len(tuple(pu.as1.iterate_tuple_elements(phi=phi2))) == 9
        assert len(tuple(pu.as1.iterate_tuple_elements(phi=phi2, max_elements=0))) == 0
        assert len(tuple(pu.as1.iterate_tuple_elements(phi=phi2, max_elements=2))) == 2
        assert len(tuple(pu.as1.iterate_tuple_elements(phi=phi2, max_elements=6))) == 6


class TestEnumeration:

    def test_is_element_of_enumeration(self):
        ca = pu.as1.let_x_be_a_binary_connective(formula_ts='c1')
        cb = pu.as1.let_x_be_a_binary_connective(formula_ts='c2')
        x = pu.as1.let_x_be_a_simple_object(formula_ts='x')
        y = pu.as1.let_x_be_a_simple_object(formula_ts='y')
        phi1 = x | ca | y
        phi2 = x | cb | y
        phi3 = y | ca | x
        e1 = pu.as1.WellFormedEnumeration(e=(phi1, phi2, phi3,))
        assert pu.as1.is_element_of_enumeration(e=e1, x=phi1)
        assert not pu.as1.is_element_of_enumeration(e=e1, x=x | ca | x)
        phi1_other_instance = x | ca | y
        assert pu.as1.is_element_of_enumeration(e=e1, x=phi1_other_instance)
        assert pu.as1.get_index_of_first_equivalent_element_in_enumeration(e=e1, x=phi1) == 0
        assert pu.as1.get_index_of_first_equivalent_element_in_enumeration(e=e1, x=phi2) == 1
        assert pu.as1.get_index_of_first_equivalent_element_in_enumeration(e=e1, x=phi3) == 2

    def test_enumeration_duplicate_elements(self):
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        b = pu.as1.let_x_be_a_simple_object(formula_ts='b')
        c = pu.as1.let_x_be_a_simple_object(formula_ts='c')
        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_AS1_029):
            # duplicate formula-equivalent formulas are forbidden in enumerations.
            e1 = pu.as1.WellFormedEnumeration(e=(a, b, c, b,))
        # with strip_duplicates, duplicates are automatically removed.
        e1 = pu.as1.WellFormedEnumeration(e=(a, b, c, b,), strip_duplicates=True)

    def test_enumeration(self):
        a, b, c, x, y, z = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'x', 'y', 'z',))
        baczx = pu.as1.WellFormedEnumeration(e=(b, a, c, z, x))
        assert pu.as1.is_formula_equivalent(phi=baczx, psi=baczx)
        assert pu.as1.is_enumeration_equivalent(phi=baczx, psi=baczx)
        assert pu.as1.is_element_of_enumeration(e=baczx, x=a)
        assert pu.as1.is_element_of_enumeration(e=baczx, x=b)
        assert pu.as1.is_element_of_enumeration(e=baczx, x=c)
        assert pu.as1.is_element_of_enumeration(e=baczx, x=x)
        assert pu.as1.is_element_of_enumeration(e=baczx, x=z)
        assert pu.as1.get_index_of_first_equivalent_element_in_enumeration(e=baczx, x=b) == 0
        assert pu.as1.get_index_of_first_equivalent_element_in_enumeration(e=baczx, x=a) == 1
        assert pu.as1.get_index_of_first_equivalent_element_in_enumeration(e=baczx, x=c) == 2
        assert pu.as1.get_index_of_first_equivalent_element_in_enumeration(e=baczx, x=z) == 3
        assert pu.as1.get_index_of_first_equivalent_element_in_enumeration(e=baczx, x=x) == 4
        assert not pu.as1.is_element_of_enumeration(x=y, e=baczx)
        baczx2 = pu.as1.WellFormedEnumeration(e=(b, a, c, z, x))
        assert pu.as1.is_formula_equivalent(phi=baczx, psi=baczx2)
        assert pu.as1.is_enumeration_equivalent(phi=baczx, psi=baczx2)

    def test_is_well_formed_enumeration(self):
        a, b, c = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c',))
        # ill-formed enumerations because of wrong connective
        star = pu.as1.FreeArityConnective(formula_ts='*')
        phi1 = pu.as1.WellFormedFormula(con=star, t=(a, b, c,))
        assert not pu.as1.is_well_formed_enumeration(e=phi1)
        phi2 = pu.as1.WellFormedFormula(con=star, t=None)
        assert not pu.as1.is_well_formed_enumeration(e=phi2)
        phi3 = pu.as1.WellFormedFormula(con=star, t=(a, a, b, c,))
        assert not pu.as1.is_well_formed_enumeration(e=phi3)
        phi4 = pu.as1.WellFormedFormula(con=star, t=(a, b, b, c,))
        assert not pu.as1.is_well_formed_enumeration(e=phi4)
        phi5 = pu.as1.WellFormedFormula(con=star, t=(a, b, c, c,))
        assert not pu.as1.is_well_formed_enumeration(e=phi5)
        # well-formed enumerations
        phi1 = pu.as1.WellFormedFormula(con=pu.csl1.enumeration, t=(a, b, c,))
        assert pu.as1.is_well_formed_enumeration(e=phi1)
        phi2 = pu.as1.WellFormedFormula(con=pu.csl1.enumeration, t=None)
        assert pu.as1.is_well_formed_enumeration(e=phi2)
        # ill-formed enumerations because of duplicate elements
        phi3 = pu.as1.WellFormedFormula(con=pu.csl1.enumeration, t=(a, a, b, c,), )
        assert not pu.as1.is_well_formed_enumeration(e=phi3)
        phi4 = pu.as1.WellFormedFormula(con=pu.csl1.enumeration, t=(a, b, b, c,))
        assert not pu.as1.is_well_formed_enumeration(e=phi4)
        phi5 = pu.as1.WellFormedFormula(con=pu.csl1.enumeration, t=(a, b, c, c,))
        assert not pu.as1.is_well_formed_enumeration(e=phi5)

    def test_is_sub_enumeration(self):
        a, b, c, d, x, y, z = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'x', 'y', 'z',))
        assert pu.as1.is_sub_enumeration(s=(a,), e=(a,))
        assert pu.as1.is_sub_enumeration(s=(a, x, b, d,), e=(z, y, b, x, a, d,))
        assert pu.as1.is_sub_enumeration(s=None, e=(z, y, b, x, a, d,))
        assert pu.as1.is_sub_enumeration(s=None, e=None)
        assert pu.as1.is_sub_enumeration(s=(a, x, b, d, z, y), e=(z, y, b, x, a, d,))
        assert not pu.as1.is_sub_enumeration(s=(z, y, b, x, a, d,), e=None)
        assert not pu.as1.is_sub_enumeration(s=(z, y, b, x, a, d,), e=(a, x, b, d,))


class TestFormulaEquivalenceWithVariables:
    def test_is_formula_equivalent_with_variables(self):
        x = pu.as1.let_x_be_a_variable(formula_ts='x')
        y = pu.as1.let_x_be_a_variable(formula_ts='y')
        is_a = pu.as1.let_x_be_a_binary_connective(as1.typesetters.infix_formula(connective_typesetter='is-a'))
        human = pu.as1.let_x_be_a_simple_object(formula_ts='human')
        platypus = pu.as1.let_x_be_a_simple_object(formula_ts='platypus')
        mortal = pu.as1.let_x_be_a_simple_object(formula_ts='mortal')
        aristotle = pu.as1.let_x_be_a_simple_object(formula_ts='aristotle')
        phi = aristotle | is_a | human
        psi = aristotle | is_a | human
        assert pu.as1.is_formula_equivalent_with_variables(
            phi=phi,
            psi=psi,
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
        ab = pu.as1.WellFormedTupl(e=(a, b,))
        cd = pu.as1.WellFormedTupl(e=(c, d,))
        assert not pu.as1.is_formula_equivalent(phi=ab, psi=cd)
        m = pu.as1.WellFormedMap()
        is_equivalent, m = pu.as1.is_formula_equivalent_with_variables_2(phi=ab, psi=cd, variables=(c, d,),
                                                                         variables_fixed_values=m)
        assert is_equivalent
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=m, preimage=c), psi=a)
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=m, preimage=d), psi=b)
        bba = pu.as1.WellFormedTupl(e=(b, b, a,))
        cca = pu.as1.WellFormedTupl(e=(c, c, a,))
        m = pu.as1.WellFormedMap()
        is_equivalent, m = pu.as1.is_formula_equivalent_with_variables_2(phi=bba, psi=bba, variables=(),
                                                                         variables_fixed_values=m)
        assert is_equivalent
        m = pu.as1.WellFormedMap()
        is_equivalent, m = pu.as1.is_formula_equivalent_with_variables_2(phi=bba, psi=cca, variables=(c,),
                                                                         variables_fixed_values=m)
        assert is_equivalent
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=m, preimage=c), psi=b)
        ababbba = pu.as1.WellFormedTupl(e=(a, b, a, b, b, a,))
        acaccca = pu.as1.WellFormedTupl(e=(a, c, a, c, c, a,))
        m = pu.as1.WellFormedMap()
        is_equivalent, m = pu.as1.is_formula_equivalent_with_variables_2(phi=ababbba, psi=acaccca, variables=(c,),
                                                                         variables_fixed_values=m)
        assert is_equivalent
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=m, preimage=c), psi=b)
        multilevel1 = pu.as1.WellFormedTupl(e=(a, b, a, b, b, c, c,))
        multilevel2 = pu.as1.WellFormedTupl(e=(a, multilevel1, a, multilevel1, c,))
        multilevel3 = pu.as1.WellFormedTupl(e=(c, multilevel2, a, multilevel1,))
        print(multilevel3)
        test = pu.as1.substitute_formulas(phi=multilevel3, m={a: e, b: d})
        m = pu.as1.WellFormedMap()
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
            formula_ts=pu.as1.TypesetterForInfixFormula(connective_ts='is-a'))
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
        ab = pu.as1.WellFormedTupl(e=(a, b,))
        cd = pu.as1.WellFormedTupl(e=(c, d,))
        assert not pu.as1.is_formula_equivalent(phi=ab, psi=cd)
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(
            phi=ab, psi=cd,
            variables=(c, d,),
            variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=c), psi=a)
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=d), psi=b)

        bba = pu.as1.WellFormedTupl(e=(b, b, a,))
        cca = pu.as1.WellFormedTupl(e=(c, c, a,))
        m = pu.as1.WellFormedMap()
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=bba, psi=bba, variables=(),
                                                                     variables_fixed_values=None)
        assert result

        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=bba, psi=cca, variables=(c,),
                                                                     variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=c), psi=b)

        ababbba = pu.as1.WellFormedTupl(e=(a, b, a, b, b, a,))
        acaccca = pu.as1.WellFormedTupl(e=(a, c, a, c, c, a,))
        result, map, = pu.as1.is_formula_equivalent_with_variables_2(phi=ababbba, psi=acaccca, variables=(c,),
                                                                     variables_fixed_values=None)
        assert result
        assert pu.as1.is_formula_equivalent(phi=pu.as1.get_image_from_map(m=map, preimage=c), psi=b)

        multilevel1 = pu.as1.WellFormedTupl(e=(a, b, a, b, b, c, c,))
        multilevel2 = pu.as1.WellFormedTupl(e=(a, multilevel1, a, multilevel1, c,))
        multilevel3 = pu.as1.WellFormedTupl(e=(c, multilevel2, a, multilevel1,))
        print(multilevel3)
        test = pu.as1.substitute_formulas(phi=multilevel3, m={a: e, b: d})
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
        m = pu.as1.WellFormedMap(d=(c1, c2, c3, c4,), c=(d1, d2, d3, d4,))
        psi = pu.as1.substitute_connectives(phi=phi, m=m)
        n = pu.as1.WellFormedMap(d=(d1, d2, d3, d4,), c=(c1, c2, c3, c4,))
        phi2 = pu.as1.substitute_connectives(phi=psi, m=n)
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
        premises = pu.as1.WellFormedEnumeration(e=(p1,))
        conclusion = x | is_a | mortal
        variables = pu.as1.WellFormedEnumeration(e=(x,))
        f = pu.as1.TransformationByVariableSubstitution(o=conclusion, v=variables, d=None,
                                                        i=premises)
        arguments = pu.as1.WellFormedTupl(e=(p2,))
        output = f.apply_transformation(i=arguments)
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
        variables = pu.as1.WellFormedEnumeration(e=(x,))
        declarations = pu.as1.WellFormedEnumeration(e=None)
        premises = pu.as1.WellFormedTupl(e=(p1,))
        phi1 = pu.as1.transformation_by_variable_substitution_connective(conclusion, variables, declarations,
                                                                         premises)
        assert pu.as1.is_well_formed_transformation_by_variable_substitution(t=phi1)
        phi1 = pu.as1.coerce_transformation_by_variable_substitution(t=phi1)
        conclusion = x | is_a | mortal
        variables = pu.as1.WellFormedEnumeration(e=(x,))
        declarations = pu.as1.WellFormedEnumeration(e=None)
        premises = pu.as1.WellFormedTupl(e=(platypus, platypus,))
        phi2 = pu.as1.transformation_by_variable_substitution_connective(conclusion, variables, declarations,
                                                                         premises, premises)
        assert not pu.as1.is_well_formed_transformation_by_variable_substitution(t=phi2)


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
            phi=pu.as1.substitute_formulas(phi=x | is_a | human, m={x: aristotle}),
            psi=aristotle | is_a | human)
        assert not pu.as1.is_formula_equivalent(
            phi=pu.as1.substitute_formulas(phi=x | is_a | human, m={x: platypus}),
            psi=aristotle | is_a | human)
        phi = aristotle | is_a | human
        phi = pu.as1.substitute_formulas(phi=phi, m={human: aristotle})
        psi = aristotle | is_a | aristotle
        assert pu.as1.is_formula_equivalent(
            phi=phi,
            psi=psi)
        omega1 = (aristotle | is_a | human) | land | (platypus | is_a | animal)
        omega2 = pu.as1.substitute_formulas(phi=omega1,
                                            m={human: aristotle})
        assert pu.as1.is_formula_equivalent(
            phi=omega2,
            psi=(aristotle | is_a | aristotle) | land | (platypus | is_a | animal))

    def test_replace_formulas_two_variables(self):
        a, b, c, d = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd',))
        c1 = pu.as1.let_x_be_a_unary_connective(formula_ts='c1')
        c2 = pu.as1.let_x_be_a_binary_connective(formula_ts='c2')
        phi = a | c2 | b
        psi = pu.as1.substitute_formulas(phi=phi, m={a: c, b: d})
        assert pu.as1.is_formula_equivalent(phi=c | c2 | d, psi=psi)
        phi = (b | c2 | a) | c2 | ((a | c2 | b) | c2 | (a | c2 | a))
        psi = pu.as1.substitute_formulas(phi=phi, m={a: c, b: d})
        assert pu.as1.is_formula_equivalent(phi=(d | c2 | c) | c2 | ((c | c2 | d) | c2 | (c | c2 | c)), psi=psi)


class TestMap:
    def test_map(self, fruits):
        red, yellow, blue = pu.as1.let_x_be_some_simple_objects(reps=('red', 'yellow', 'blue',))
        c = pu.as1.WellFormedTupl(e=(red, yellow, blue, red))
        m1 = pu.as1.WellFormedMap(d=fruits, c=c)
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
        e1 = pu.as1.WellFormedEnumeration(e=(red, yellow, blue,))
        e2 = pu.as1.WellFormedEnumeration(e=(yellow, red, blue,))
        assert pu.as1.is_enumeration_equivalent(phi=e1, psi=e2)
        assert not pu.as1.is_formula_equivalent(phi=e1, psi=e2)


class TestUnionEnumeration:
    def test_union_enumeration(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        abc = pu.as1.WellFormedEnumeration(e=(a, b, c,))
        cd = pu.as1.WellFormedEnumeration(e=(c, d,))
        abcd1 = pu.as1.union_enumeration(phi=abc, psi=cd)
        abcd2 = pu.as1.WellFormedEnumeration(e=(a, b, c, d,))
        assert pu.as1.is_enumeration_equivalent(phi=abcd1, psi=abcd2)
        abcde1 = pu.as1.WellFormedEnumeration(e=(a, b, c, d, e,))
        abcde2 = pu.as1.WellFormedEnumeration(e=(a, b, c, e, d,))
        assert pu.as1.is_enumeration_equivalent(phi=abcde1, psi=abcde2)
        assert not pu.as1.is_formula_equivalent(phi=abcde1, psi=abcde2)  # because of order
        abcde3 = pu.as1.union_enumeration(phi=abcde1, psi=abcde1)
        assert pu.as1.is_enumeration_equivalent(phi=abcde3, psi=abcde1)
        assert pu.as1.is_formula_equivalent(phi=abcde3, psi=abcde1)


class TestEmptyEnumeration:
    def test_empty_enumeration(self):
        a = pu.as1.EmptyEnumeration()
        x, y, z = pu.as1.let_x_be_some_simple_objects(reps=('x', 'y', 'z',))
        assert not pu.as1.is_element_of_enumeration(x=x, e=a)
        assert a.arity == 0


class TestInferenceRule:
    def test_inference_rule_without_premises(self):
        # elaborate a theory
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_binary_connective(formula_ts='f')
        phi = a | f | b
        rule = pu.as1.TransformationByVariableSubstitution(o=phi, v=None, d=None, i=None)
        ir = pu.as1.WellFormedInferenceRule(f=rule)
        axiomatization = pu.as1.WellFormedAxiomatization(d=(ir,))

        # derivation from the axiom
        i = pu.as1.WellFormedInference(p=None, i=ir)
        isolated_theorem = pu.as1.WellFormedTheorem(p=phi, i=i)
        t = pu.as1.append_to_theory(isolated_theorem, t=axiomatization)
        assert pu.as1.is_formula_equivalent(
            phi=isolated_theorem.valid_statement,
            psi=phi)

    def test_is_well_formed_postulation(self):
        a, b = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b',))
        star = pu.as1.let_x_be_a_binary_connective(
            formula_ts=pu.as1.typesetters.classical_formula(connective_typesetter='*'))
        f = pu.as1.TransformationByVariableSubstitution(o=a | star | b, v=None, d=None, i=None)
        phi1 = pu.as1.connective_for_inference_rule(f)
        assert pu.as1.is_well_formed_inference_rule(i=phi1)

        # incorrect connective
        phi2 = pu.as1.WellFormedFormula(con=pu.as1.connective_for_inference,
                                        t=(pu.as1.connective_for_inference_rule, f,))
        assert not pu.as1.is_well_formed_inference_rule(i=phi2)

        # incorrect connective
        phi2 = pu.as1.WellFormedFormula(con=pu.as1.connective_for_inference_rule, t=None)
        assert not pu.as1.is_well_formed_inference_rule(i=phi2)

        # incorrect axiomatic-postulation
        phi3 = f | pu.as1.connective_for_theory_component | pu.csl1.enumeration
        assert not pu.as1.is_well_formed_inference_rule(i=phi3)


class TestFormulaToTuple:
    def test_formula_to_tuple(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_unary_connective(formula_ts='f')
        g = pu.as1.let_x_be_a_binary_connective(formula_ts='g')
        h = pu.as1.let_x_be_a_ternary_connective(formula_ts='h')
        phi1 = h(e, b, d)
        e1_result = pu.as1.transform_formula_to_tuple(phi=phi1)
        e1_expected = pu.as1.WellFormedTupl(e=(e, b, d,))
        assert pu.as1.is_formula_equivalent(phi=e1_result, psi=e1_expected)
        phi2 = h(phi1, b, g(a, f(b)))
        e2_result = pu.as1.transform_formula_to_tuple(phi=phi2)
        e2_expected = pu.as1.WellFormedTupl(e=(phi1, b, g(a, f(b)),))
        assert pu.as1.is_formula_equivalent(phi=e2_result, psi=e2_expected)


class TestProofByPostulation:
    def test_is_well_formed(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        star3 = pu.as1.let_x_be_a_ternary_connective(formula_ts='*3')
        rule1 = pu.as1.TransformationByVariableSubstitution(o=star3(e, b, d), v=None, d=None,
                                                            i=None)
        phi1 = pu.as1.connective_for_inference_rule(rule1)
        assert pu.as1.is_well_formed_inference_rule(i=phi1)
        phi2 = rule1 | pu.as1.connective_for_map | pu.as1.connective_for_inference_rule
        assert not pu.as1.is_well_formed_inference_rule(i=phi2)
        phi3 = rule1 | pu.as1.connective_for_theory_component | b
        assert not pu.as1.is_well_formed_inference_rule(i=phi3)


class TestTheorem:
    def test_coerce_theorem(self):
        t = pu.as1.let_x_be_a_theory()
        a, b = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b',))
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=a)
        ir1 = pu.as1.WellFormedInferenceRule(f=pu.as1.TransformationByVariableSubstitution(o=b, i=(a,)))
        t = pu.as1.append_to_theory(ir1, t=t)
        if1 = pu.as1.WellFormedInference(p=(a,), i=ir1)
        # For the purpose of this test,
        # build the theorem manually,
        # i.e. without using a derivation function.
        tm1 = pu.as1.WellFormedTheorem(p=b, i=if1)
        tm1 = pu.as1.coerce_theorem(m=tm1)

        tm2 = pu.as1.connective_for_theorem(b, if1)
        assert pu.as1.is_formula_equivalent(phi=tm1, psi=tm2)
        tm2 = pu.as1.coerce_theorem(m=tm2)

        t = pu.as1.append_to_theory(tm1, t=t)
        pass


class TestInference:
    def test_inference(self):
        x, y, z = pu.as1.let_x_be_some_variables(reps=('x', 'y', 'z',))
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_binary_connective(formula_ts='f')
        t = pu.as1.TransformationByVariableSubstitution(o=x | f | z, v=(x, y, z,), d=None,
                                                        i=(x | f | y, y | f | z,), )
        p = (a | f | b, b | f | c,)
        theorem = a | f | c
        pu.as1.is_formula_equivalent(phi=theorem, psi=t(i=p))
        inference_rule = pu.as1.WellFormedInferenceRule(f=t)
        inference = pu.as1.WellFormedInference(i=inference_rule, p=p, a=None)
        theorem_2 = pu.as1.WellFormedTheorem(p=theorem, i=inference)
        pu.as1.is_formula_equivalent(
            phi=theorem_2,
            psi=theorem | pu.as1.connective_for_theory_component | pu.as1.connective_for_inference(
                inference_rule, p,
                pu.as1.WellFormedTupl()))

    def test_is_well_formed_inference(self):
        x, y, z = pu.as1.let_x_be_some_variables(reps=('x', 'y', 'z',))
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        f = pu.as1.let_x_be_a_binary_connective(formula_ts='f')
        t = pu.as1.TransformationByVariableSubstitution(o=x | f | z, v=(x, y, z,), d=None,
                                                        i=(x | f | y, y | f | z,))
        p = pu.as1.WellFormedTupl(e=(a | f | b, b | f | c,))
        i = pu.as1.WellFormedInferenceRule(f=t)
        phi1 = pu.as1.connective_for_inference(i, p, as1.WellFormedTupl())
        assert pu.as1.is_well_formed_inference(i=phi1)
        phi2 = pu.as1.connective_for_inference(i, as1.WellFormedTupl())
        assert not pu.as1.is_well_formed_inference(i=phi2)
        phi3 = p | pu.as1.connective_for_theory_component | i
        assert not pu.as1.is_well_formed_inference(i=phi3)
        phi4 = f(a, a, b, b) | pu.as1.connective_for_theory_component | i
        assert not pu.as1.is_well_formed_inference(i=phi4)


class TestProofByInference:
    def test_is_well_formed(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        x, y, z = pu.as1.let_x_be_some_variables(reps=('x', 'y', 'z',))
        star = pu.as1.let_x_be_a_binary_connective(
            formula_ts=pu.as1.typesetters.infix_formula(connective_typesetter=pu.pl1.symbols.asterisk_operator))
        premises = pu.as1.WellFormedEnumeration(e=(x | star | y, y | star | z,))
        conclusion = x | star | z
        variables = pu.as1.WellFormedEnumeration(e=(x, y, z,))
        f = pu.as1.TransformationByVariableSubstitution(o=conclusion, v=variables, d=None,
                                                        i=premises)
        ir = pu.as1.WellFormedInferenceRule(f=f)
        p = (a | star | b, b | star | c,)
        i = pu.as1.WellFormedInference(p=p, i=ir)
        outcome = f.apply_transformation(i=p)
        m = pu.as1.WellFormedTheorem(p=a | star | c, i=i)
        assert pu.as1.is_well_formed_theorem(m=m)
        assert pu.as1.is_well_formed_theorem(m=pu.as1.connective_for_theorem(a | star | c, i))

        i2 = pu.as1.WellFormedInference(p=(a | star | b, b | star | a,), i=ir)
        assert not pu.as1.is_well_formed_theorem(m=pu.as1.connective_for_theorem(a | star | c, i2))
        pass


class TestAlgorithm:
    def test_algorithm(self):

        t = as1.let_x_be_a_theory()
        a = as1.let_x_be_a_simple_object(formula_ts='a')
        b = as1.let_x_be_a_simple_object(formula_ts='b')
        g = as1.let_x_be_a_unary_connective(formula_ts=as1.TypesetterForClassicalFormula(connective_ts='g'))
        t, _ = as1.let_x_be_an_axiom(t=t, s=a)

        def hello_world(i: pu.as1.WellFormedTupl | None = None, raise_error_if_false: bool = False):
            i = as1.coerce_tuple(s=i)
            if i.arity == 1 and as1.is_formula_equivalent(phi=i[0], psi=a):
                return True, g(a)
            else:
                if raise_error_if_false:
                    raise pu.u1.ApplicativeError(msg='Test algorithm failure', i=i)
                else:
                    return False, None

        hello_world_con = as1.ConnectiveLinkedWithAlgorithm(a=hello_world, formula_ts='hello-world')

        with as1.let_x_be_a_variable(formula_ts=as1.typesetters.text(text='x')) as x:
            f = as1.let_x_be_a_transformation_by_variable_substitution(a=hello_world_con,
                                                                       o=g(x),
                                                                       i=(x,),
                                                                       v={x, },
                                                                       d=None)
        i = as1.WellFormedInferenceRule(f=f)
        t, i = as1.let_x_be_an_inference_rule(t=t, i=i)
        m, _, d = as1.derive_1(t=t, c=g(a), p=(a,), i=i, a=None, raise_error_if_false=True)
        pass


class TestIteratePermutationsOfEnumerationElementsWithFixedSize:
    def test_iterate_permutations_of_enumeration_elements_with_fixed_size(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))

        e = pu.as1.WellFormedEnumeration()
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=0):
            i = i + 1
        assert i == 0

        e = pu.as1.WellFormedEnumeration(e=(a,))
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=0):
            i = i + 1
        assert i == 0
        i = 0
        for x in pu.as1.iterate_permutations_of_enumeration_elements_with_fixed_size(e=e, n=1):
            i = i + 1
        assert i == 1

        e = pu.as1.WellFormedEnumeration(e=(a, b,))
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

        e = pu.as1.WellFormedEnumeration(e=(a, b, c,))
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
                                                                         variables_values=pu.as1.WellFormedMap(d=(e,),
                                                                                                               c=(d,)))
        assert valid
        valid, s, = pu.as1.are_valid_statements_in_theory_with_variables(s=(a, c, e,), t=t, variables=(e,),
                                                                         variables_values=None)
        assert valid


class TestStripDuplicateFormulasInPythonTuple:
    def test_strip_duplicate_formulas_in_python_tuple(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        t1 = pu.as1.WellFormedTupl(e=(a, b, a, a, e, e,))
        t2 = pu.as1.WellFormedTupl(e=(a, b, e,))
        t3 = pu.as1.strip_duplicate_formulas_in_python_tuple(t=t1)
        t3 = pu.as1.WellFormedTupl(e=t3)
        assert not pu.as1.is_formula_equivalent(phi=t1, psi=t3)
        assert pu.as1.is_formula_equivalent(phi=t2, psi=t3)


class TestCoerceEnumeration:
    def test_coerce_enumeration(self):
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        e1 = pu.as1.WellFormedEnumeration(e=(a, b, a, a, e, e,), strip_duplicates=True)
        e2 = pu.as1.WellFormedEnumeration(e=(a, b, e,), strip_duplicates=True)
        e3 = pu.as1.WellFormedEnumeration(e=e1, strip_duplicates=True)
        assert pu.as1.is_formula_equivalent(phi=e1, psi=e3)
        assert pu.as1.is_formula_equivalent(phi=e2, psi=e3)
        assert pu.as1.is_formula_equivalent(phi=e1, psi=e2)


class TestAxiomatization:
    def test_is_well_formed(self):
        # elaborate a theory
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        x, y, z = pu.as1.let_x_be_some_variables(reps=('x', 'y', 'z',))
        star1 = pu.as1.let_x_be_a_unary_connective(formula_ts='*1')
        star2 = pu.as1.let_x_be_a_binary_connective(formula_ts='*2')
        axiom_ok_1 = pu.as1.WellFormedAxiom(p=a | star2 | b)
        axiom_ok_2 = pu.as1.WellFormedAxiom(p=star1(c))
        assert pu.as1.is_well_formed_axiom(a=axiom_ok_2)

        # simple case
        e1 = pu.as1.WellFormedEnumeration(e=(axiom_ok_1, axiom_ok_2,))
        e1 = pu.as1.WellFormedAxiomatization(d=e1)
        assert pu.as1.is_well_formed_axiomatization(a=e1)

        # extreme case: the empty enumeration
        e2 = pu.as1.WellFormedEnumeration()
        e2 = pu.as1.WellFormedAxiomatization(d=e2)
        assert pu.as1.is_well_formed_axiomatization(a=e2)
        a1 = pu.as1.WellFormedAxiomatization(d=(axiom_ok_1, axiom_ok_2,))  # does not raise an exception

        # bad case: an enumeration with a non-axiom
        e3 = pu.as1.WellFormedEnumeration(e=(axiom_ok_1, axiom_ok_2, star1(e),))
        assert not pu.as1.is_well_formed_axiomatization(a=e3)
        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_AS1_062):
            a2 = pu.as1.WellFormedAxiomatization(d=e3)  # raise an e123 exception


class TestDemonstration:
    def test_is_well_formed(self):
        # elaborate a theory
        theory = pu.as1.let_x_be_a_collection_of_axioms(axioms=None)
        a, b, c, d, e = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e',))
        x, y, z = pu.as1.let_x_be_some_variables(reps=('x', 'y', 'z',))
        star = pu.as1.let_x_be_a_binary_connective(formula_ts='*')
        theory, axiom_1, = pu.as1.let_x_be_an_axiom(t=theory, s=a | star | b)
        theory, axiom_2, = pu.as1.let_x_be_an_axiom(t=theory, s=b | star | c)
        theory, ir1, = pu.as1.let_x_be_an_inference_rule(t=theory,
                                                         p=(x | star | y,
                                                            y | star | z,),
                                                         c=x | star | z,
                                                         v=(x, y, z,))

        # derive a theorem
        demo2, _, _ = pu.as1.derive_1(t=theory,
                                      c=a | star | c,
                                      p=(
                                          a | star | b,
                                          b | star | c,),
                                      i=ir1, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=a | star | c, t=demo2)

        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_AS1_039):
            # invalid proof raise exception
            pu.as1.WellFormedTheory(d=(axiom_1, axiom_2, a | star | e))

        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_AS1_039):
            # invalid proof sequence exception
            pu.as1.WellFormedTheory(d=(axiom_1, axiom_2, a | star | c, ir1,))
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
        t1, a1 = pu.as1.let_x_be_an_axiom(t=None, a=pu.as1.WellFormedAxiom(p=p))

        t1, success, _, = pu.as1.derive_0(t=t1, c=p)

        if_p_then_q = pu.as1.WellFormedInferenceRule(
            f=pu.as1.TransformationByVariableSubstitution(o=q, v=(), d=None, i=(p,)))
        t1 = pu.as1.append_to_theory(if_p_then_q, t=t1)

        with pu.as1.let_x_be_a_variable(formula_ts='x') as x, pu.as1.let_x_be_a_variable(
                formula_ts='y') as y:
            x_y_then_x_and_y = pu.as1.WellFormedInferenceRule(
                f=pu.as1.TransformationByVariableSubstitution(
                    o=x | pu.csl1.land | y, v=(x, y,),
                    d=None, i=(x, y,)))
        t1 = pu.as1.WellFormedTheory(d=(*t1, x_y_then_x_and_y,))

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
        t2, success, _, = pu.as1.auto_derive_2(t=t2,
                                               c=p | pu.csl1.land | q)
        assert success
        pass
        # auto-derivation of an impossible theorem fails and raises an auto-derivation-failure
        t2, success, _, = pu.as1.auto_derive_2(t=t2,
                                               c=p | pu.csl1.lor | q)
        assert not success
        pass

        # use auto-derivation-2
        t3, success, derivation, _ = pu.as1.auto_derive_4(t=t1,
                                                          c=p | pu.csl1.land | q,
                                                          max_recursion=8, debug=False)
        assert success
        pass

        t3, success, derivation, _ = pu.as1.auto_derive_4(t=t1,
                                                          c=p | pu.csl1.lor | q,
                                                          max_recursion=8, debug=False)
        assert not success
        pass


class TestTheory:
    def test_iterate_axioms(self):
        a, b, c, d, e, f, g = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e', 'f', 'g',))
        t = pu.as1.WellFormedTheory()
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=a)
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=b)
        t, i1 = pu.as1.let_x_be_an_inference_rule(t=t,
                                                  f=pu.as1.TransformationByVariableSubstitution(o=f, v=None, i=None))
        t, _, _ = pu.as1.derive_1(t=t, c=f, p=None, i=i1, raise_error_if_false=True)
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=d)
        t, i2 = pu.as1.let_x_be_an_inference_rule(t=t,
                                                  f=pu.as1.TransformationByVariableSubstitution(o=g, v=None, i=None))
        t, _, _ = pu.as1.derive_1(t=t, c=g, p=None, i=i2, raise_error_if_false=True)
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=e)

        # iterate axioms
        assert len(tuple(pu.as1.iterate_theory_axioms(t=t))) == 4
        assert len(tuple(pu.as1.iterate_theory_axioms(t=t, max_components=2))) == 2
        assert len(tuple(pu.as1.iterate_theory_axioms(t=t, max_components=3))) == 2
        assert len(tuple(pu.as1.iterate_theory_axioms(t=t, max_components=4))) == 2
        assert len(tuple(pu.as1.iterate_theory_axioms(t=t, max_components=5))) == 3

        # iterate inference-rules
        assert len(tuple(pu.as1.iterate_theory_inference_rules(t=t))) == 2
        assert len(tuple(pu.as1.iterate_theory_inference_rules(t=t, max_components=2))) == 0
        assert len(tuple(pu.as1.iterate_theory_inference_rules(t=t, max_components=3))) == 1
        assert len(tuple(pu.as1.iterate_theory_inference_rules(t=t, max_components=4))) == 1
        assert len(tuple(pu.as1.iterate_theory_inference_rules(t=t, max_components=5))) == 1
        assert len(tuple(pu.as1.iterate_theory_inference_rules(t=t, max_components=6))) == 2

        # iterate theorems
        assert len(tuple(pu.as1.iterate_theory_theorems(t=t))) == 2
        assert len(tuple(pu.as1.iterate_theory_theorems(t=t, max_components=3))) == 0
        assert len(tuple(pu.as1.iterate_theory_theorems(t=t, max_components=4))) == 1
        assert len(tuple(pu.as1.iterate_theory_theorems(t=t, max_components=5))) == 1
        assert len(tuple(pu.as1.iterate_theory_theorems(t=t, max_components=6))) == 1
        assert len(tuple(pu.as1.iterate_theory_theorems(t=t, max_components=7))) == 2

        # iterate propositions
        assert len(tuple(pu.as1.iterate_theory_propositions(t=t))) == 6
        assert len(tuple(pu.as1.iterate_theory_propositions(t=t, max_components=0))) == 0
        assert len(tuple(pu.as1.iterate_theory_propositions(t=t, max_components=1))) == 1
        assert len(tuple(pu.as1.iterate_theory_propositions(t=t, max_components=2))) == 2
        assert len(tuple(pu.as1.iterate_theory_propositions(t=t, max_components=3))) == 2
        assert len(tuple(pu.as1.iterate_theory_propositions(t=t, max_components=4))) == 3
        assert len(tuple(pu.as1.iterate_theory_propositions(t=t, max_components=5))) == 4
        assert len(tuple(pu.as1.iterate_theory_propositions(t=t, max_components=6))) == 4
        assert len(tuple(pu.as1.iterate_theory_propositions(t=t, max_components=7))) == 5

    def test_would_be_valid(self):
        a, b, c, d, e, f, g = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e', 'f', 'g',))
        t = pu.as1.WellFormedTheory()
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=a)
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=b)
        t, i1 = pu.as1.let_x_be_an_inference_rule(t=t,
                                                  f=pu.as1.TransformationByVariableSubstitution(o=f, v=None, i=None))
        t, _, _ = pu.as1.derive_1(t=t, c=f, p=None, i=i1, raise_error_if_false=True)
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=d)
        t, i2 = pu.as1.let_x_be_an_inference_rule(t=t,
                                                  f=pu.as1.TransformationByVariableSubstitution(o=g, v=None, i=None))
        t, _, _ = pu.as1.derive_1(t=t, c=g, p=None, i=i2, raise_error_if_false=True)
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=e)

        u_limit_index = 2
        v = pu.as1.WellFormedEnumeration(e=t[0:u_limit_index])
        u_ok = pu.as1.WellFormedEnumeration(e=(t[u_limit_index],))
        u_nok = pu.as1.WellFormedEnumeration(e=(t[u_limit_index + 1],))
        test, _, _ = pu.as1.would_be_valid_components_in_theory(v=v, u=u_ok)
        assert test
        test, _, _ = pu.as1.would_be_valid_components_in_theory(v=v, u=u_nok)
        assert not test  # this theorem cannot be derived without the above inference-rule

        u_limit_index = 5
        v = pu.as1.WellFormedEnumeration(e=t[0:u_limit_index])
        u_ok = pu.as1.WellFormedEnumeration(e=(t[u_limit_index],))
        u_nok = pu.as1.WellFormedEnumeration(e=(t[u_limit_index + 1],))
        test, _, _ = pu.as1.would_be_valid_components_in_theory(v=v, u=u_ok)
        assert test
        test, _, _ = pu.as1.would_be_valid_components_in_theory(v=v, u=u_nok)
        assert not test  # this theorem cannot be derived without the above inference-rule

    def test_transform_to_axiomatization_and_axiomatization_equivalence(self):
        a, b, c, d, e, f, g = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e', 'f', 'g',))
        t1 = pu.as1.WellFormedTheory()
        t2, _ = pu.as1.let_x_be_an_axiom(t=t1, s=a)
        t3, _ = pu.as1.let_x_be_an_axiom(t=t2, s=b)
        t4, i1 = pu.as1.let_x_be_an_inference_rule(t=t3,
                                                   f=pu.as1.TransformationByVariableSubstitution(o=f, v=None, i=None))
        t5, _, _ = pu.as1.derive_1(t=t4, c=f, p=None, i=i1, raise_error_if_false=True)
        t6, _ = pu.as1.let_x_be_an_axiom(t=t5, s=d)
        t7, i2 = pu.as1.let_x_be_an_inference_rule(t=t6,
                                                   f=pu.as1.TransformationByVariableSubstitution(o=g, v=None, i=None))
        t8, _, _ = pu.as1.derive_1(t=t7, c=g, p=None, i=i2, raise_error_if_false=True)
        t9, _ = pu.as1.let_x_be_an_axiom(t=t8, s=e)

        a1 = pu.as1.transform_theory_to_axiomatization(t=t1)
        a2 = pu.as1.transform_theory_to_axiomatization(t=t2)
        a3 = pu.as1.transform_theory_to_axiomatization(t=t3)
        a4 = pu.as1.transform_theory_to_axiomatization(t=t4)
        a5 = pu.as1.transform_theory_to_axiomatization(t=t5)
        a6 = pu.as1.transform_theory_to_axiomatization(t=t6)
        a7 = pu.as1.transform_theory_to_axiomatization(t=t7)
        a8 = pu.as1.transform_theory_to_axiomatization(t=t8)
        a9 = pu.as1.transform_theory_to_axiomatization(t=t9)

        assert not pu.as1.is_formula_equivalent(phi=a1, psi=a2)
        assert not pu.as1.is_formula_equivalent(phi=a2, psi=a3)
        assert not pu.as1.is_formula_equivalent(phi=a3, psi=a4)
        assert pu.as1.is_formula_equivalent(phi=a4, psi=a5)
        assert not pu.as1.is_formula_equivalent(phi=a5, psi=a6)
        assert not pu.as1.is_formula_equivalent(phi=a6, psi=a7)
        assert pu.as1.is_formula_equivalent(phi=a7, psi=a8)
        assert not pu.as1.is_formula_equivalent(phi=a8, psi=a9)

        assert not pu.as1.is_axiomatization_equivalent(t1=t1, t2=t2)
        assert not pu.as1.is_axiomatization_equivalent(t1=t2, t2=t3)
        assert not pu.as1.is_axiomatization_equivalent(t1=t3, t2=t4)
        assert pu.as1.is_axiomatization_equivalent(t1=t4, t2=t5)
        assert not pu.as1.is_axiomatization_equivalent(t1=t5, t2=t6)
        assert not pu.as1.is_axiomatization_equivalent(t1=t6, t2=t7)
        assert pu.as1.is_axiomatization_equivalent(t1=t7, t2=t8)
        assert not pu.as1.is_axiomatization_equivalent(t1=t8, t2=t9)

    def test_is_extension_of(self):
        a, b, c, d, e, f, g = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e', 'f', 'g',))
        t1 = pu.as1.WellFormedTheory()
        t2, _ = pu.as1.let_x_be_an_axiom(t=t1, s=a)
        t3, _ = pu.as1.let_x_be_an_axiom(t=t2, s=b)
        t4, i1 = pu.as1.let_x_be_an_inference_rule(t=t3,
                                                   f=pu.as1.TransformationByVariableSubstitution(o=f, v=None, i=None))
        t5, _, _ = pu.as1.derive_1(t=t4, c=f, p=None, i=i1, raise_error_if_false=True)
        t6, _ = pu.as1.let_x_be_an_axiom(t=t5, s=d)
        t7, i2 = pu.as1.let_x_be_an_inference_rule(t=t6,
                                                   f=pu.as1.TransformationByVariableSubstitution(o=g, v=None, i=None))
        t8, _, _ = pu.as1.derive_1(t=t7, c=g, p=None, i=i2, raise_error_if_false=True)
        t9, _ = pu.as1.let_x_be_an_axiom(t=t8, s=e)

        assert pu.as1.is_extension_of(t2=t2, t1=t1)
        assert pu.as1.is_extension_of(t2=t3, t1=t2)
        assert pu.as1.is_extension_of(t2=t4, t1=t3)
        assert pu.as1.is_extension_of(t2=t5, t1=t4)
        assert pu.as1.is_extension_of(t2=t6, t1=t5)
        assert pu.as1.is_extension_of(t2=t7, t1=t6)
        assert pu.as1.is_extension_of(t2=t8, t1=t7)
        assert pu.as1.is_extension_of(t2=t9, t1=t8)

        assert pu.as1.is_extension_of(t2=t1, t1=t1)
        assert pu.as1.is_extension_of(t2=t2, t1=t2)
        assert pu.as1.is_extension_of(t2=t3, t1=t3)
        assert pu.as1.is_extension_of(t2=t4, t1=t4)
        assert pu.as1.is_extension_of(t2=t5, t1=t5)
        assert pu.as1.is_extension_of(t2=t6, t1=t6)
        assert pu.as1.is_extension_of(t2=t7, t1=t7)
        assert pu.as1.is_extension_of(t2=t8, t1=t8)
        assert pu.as1.is_extension_of(t2=t9, t1=t9)

        assert not pu.as1.is_extension_of(t2=t1, t1=t2)
        assert not pu.as1.is_extension_of(t2=t2, t1=t3)
        assert not pu.as1.is_extension_of(t2=t3, t1=t4)
        assert pu.as1.is_extension_of(t2=t4, t1=t5)  # t5 contains a new theorem but axiomatization is left unchanged.
        assert not pu.as1.is_extension_of(t2=t5, t1=t6)
        assert not pu.as1.is_extension_of(t2=t6, t1=t7)
        assert pu.as1.is_extension_of(t2=t7, t1=t8)  # t8 contains a new theorem but axiomatization is left unchanged.
        assert not pu.as1.is_extension_of(t2=t8, t1=t9)


class TestFormula:
    def test_get_formula_depth(self):
        c = pu.as1.FreeArityConnective(formula_ts=pu.pl1.symbols.x_uppercase_serif_italic)
        phi1 = pu.as1.WellFormedFormula(con=c, t=None)
        assert pu.as1.rank(phi=phi1) == 1
        phi2 = pu.as1.WellFormedFormula(con=c, t=(phi1, phi1,))
        assert pu.as1.rank(phi=phi2) == 2
        phi3 = pu.as1.WellFormedFormula(con=c, t=(phi1, phi2, phi1, phi2))
        assert pu.as1.rank(phi=phi3) == 3

    def test_iterate(self):
        a, b, c, d, e, f = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e', 'f',))
        phi1 = pu.as1.WellFormedFormula(con=a, t=(a, b, c, d, e, f,))
        assert a in phi1
        assert len(phi1) == 6
        assert len(tuple(pu.as1.iterate_formula_terms(phi=phi1))) == 6
        assert len(tuple(pu.as1.iterate_formula_terms(phi=phi1, max_terms=0))) == 0
        assert len(tuple(pu.as1.iterate_formula_terms(phi=phi1, max_terms=2))) == 2
        assert len(tuple(pu.as1.iterate_formula_terms(phi=phi1, max_terms=6))) == 6
        phi2 = pu.as1.WellFormedFormula(con=a, t=(f, f, a, b, d, e, b, b, f,))
        assert a in phi2
        assert len(phi2) == 9
        assert len(tuple(pu.as1.iterate_formula_terms(phi=phi2))) == 9
        assert len(tuple(pu.as1.iterate_formula_terms(phi=phi2, max_terms=0))) == 0
        assert len(tuple(pu.as1.iterate_formula_terms(phi=phi2, max_terms=2))) == 2
        assert len(tuple(pu.as1.iterate_formula_terms(phi=phi2, max_terms=6))) == 6


class TestTheoreticalContext:
    def test_theoretical_context(self):
        a, b, c, d, e, f, g = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd', 'e', 'f', 'g',))
        ab = pu.as1.WellFormedAxiomatization()
        ab, ax1 = pu.as1.let_x_be_an_axiom(t=ab, s=a)
        ab, _ = pu.as1.let_x_be_an_axiom(t=ab, s=b)
        ab, i1 = pu.as1.let_x_be_an_inference_rule(t=ab,
                                                   f=pu.as1.TransformationByVariableSubstitution(o=f, v=None, i=None))

        assert isinstance(ab, pu.as1.WellFormedAxiomatization)
        assert isinstance(ab, pu.as1.WellFormedTheoreticalContext)
        assert pu.as1.is_well_formed_theoretical_context(t=ab)
        assert not pu.as1.is_well_formed_theoretical_context(t=a)
        assert not pu.as1.is_well_formed_theoretical_context(t=ax1)

        t, _, _ = pu.as1.derive_1(t=ab, c=f, p=None, i=i1, raise_error_if_false=True)
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=d)
        t, i2 = pu.as1.let_x_be_an_inference_rule(t=t,
                                                  f=pu.as1.TransformationByVariableSubstitution(o=g, v=None, i=None))
        t, _, _ = pu.as1.derive_1(t=t, c=g, p=None, i=i2, raise_error_if_false=True)
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=e)

        assert isinstance(t, pu.as1.WellFormedTheory)
        assert isinstance(t, pu.as1.WellFormedTheoreticalContext)
        assert pu.as1.is_well_formed_theoretical_context(t=t)

        # h, _ = pu.as1.WellFormedHypothesis(b=t, a=c)

        # assert isinstance(h, pu.as1.WellFormedHypothesis)
        # assert isinstance(h, pu.as1.WellFormedTheoreticalContext)
        # assert pu.as1.is_well_formed_theoretical_context(t=h)


class TestExtension:
    def test_extension_of_axioms(self):
        """Test various theory extensions with axioms."""
        a, b, c, d = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'd',))
        x, y, z = pu.as1.let_x_be_some_simple_objects(reps=('x', 'y', 'z',))

        def get_sub_theory(p):
            t = pu.as1.WellFormedTheory()
            t, ax = pu.as1.let_x_be_an_axiom(t=t, s=p)
            return t, ax

        ta, aa = get_sub_theory(p=a)

        tb, ab = get_sub_theory(p=b)
        tb, i1 = pu.as1.let_x_be_an_inference_rule(
            t=tb, f=pu.as1.TransformationByVariableSubstitution(o=x, v=None, i=(a, b,)))
        # it is not possible to derive `b` in `tb` because `a` is not in it.
        tb, ok, _ = pu.as1.derive_2(t=tb, c=x, i=i1, raise_error_if_false=False)
        assert not ok

        tc, ac = get_sub_theory(p=c)

        td, ad = get_sub_theory(p=d)

        t = pu.as1.WellFormedTheory()
        assert not pu.as1.is_valid_proposition_so_far_1(p=a, t=t)
        assert not pu.as1.is_valid_proposition_so_far_1(p=b, t=t)
        assert not pu.as1.is_valid_proposition_so_far_1(p=c, t=t)
        assert not pu.as1.is_valid_proposition_so_far_1(p=d, t=t)
        assert not pu.as1.is_axiom_of(a=aa, t=t)
        assert not pu.as1.is_axiom_of(a=ab, t=t)
        assert not pu.as1.is_axiom_of(a=ac, t=t)
        assert not pu.as1.is_axiom_of(a=ad, t=t)

        # test a first extension t(extends(ta))
        t, _ = pu.as1.let_x_be_an_extension(t=t, e=ta)
        assert pu.as1.is_valid_proposition_so_far_1(p=a, t=t)
        assert not pu.as1.is_valid_proposition_so_far_1(p=b, t=t)
        assert not pu.as1.is_valid_proposition_so_far_1(p=c, t=t)
        assert not pu.as1.is_valid_proposition_so_far_1(p=d, t=t)
        assert pu.as1.is_axiom_of(a=aa, t=t)
        assert not pu.as1.is_axiom_of(a=ab, t=t)
        assert not pu.as1.is_axiom_of(a=ac, t=t)
        assert not pu.as1.is_axiom_of(a=ad, t=t)

        # test a second extension t(extends(ta), extends(tb))
        t, _ = pu.as1.let_x_be_an_extension(t=t, e=tb)
        assert pu.as1.is_valid_proposition_so_far_1(p=a, t=t)
        assert pu.as1.is_valid_proposition_so_far_1(p=b, t=t)
        assert not pu.as1.is_valid_proposition_so_far_1(p=c, t=t)
        assert not pu.as1.is_valid_proposition_so_far_1(p=d, t=t)
        assert pu.as1.is_axiom_of(a=aa, t=t)
        assert pu.as1.is_axiom_of(a=ab, t=t)
        assert not pu.as1.is_axiom_of(a=ac, t=t)
        assert not pu.as1.is_axiom_of(a=ad, t=t)

        # now it is possible to derive `b` in `t` because it contains `a` in `ta` and `b` in `tb`.
        t, ok, _ = pu.as1.derive_2(t=t, c=x, i=i1, raise_error_if_false=False)
        assert ok

        # the other way around: tc(extends(t(extends(ta), extends(tb)))
        t, _ = pu.as1.let_x_be_an_extension(t=tc, e=t)
        assert pu.as1.is_valid_proposition_so_far_1(p=a, t=t)
        assert pu.as1.is_valid_proposition_so_far_1(p=b, t=t)
        assert pu.as1.is_valid_proposition_so_far_1(p=c, t=t)
        assert not pu.as1.is_valid_proposition_so_far_1(p=d, t=t)
        assert pu.as1.is_axiom_of(a=aa, t=t)
        assert pu.as1.is_axiom_of(a=ab, t=t)
        assert pu.as1.is_axiom_of(a=ac, t=t)
        assert not pu.as1.is_axiom_of(a=ad, t=t)

        # the other way around: td(extends(tc(extends(t(extends(ta), extends(tb)))))
        t, _ = pu.as1.let_x_be_an_extension(t=td, e=t)
        assert pu.as1.is_valid_proposition_so_far_1(p=a, t=t)
        assert pu.as1.is_valid_proposition_so_far_1(p=b, t=t)
        assert pu.as1.is_valid_proposition_so_far_1(p=c, t=t)
        assert pu.as1.is_valid_proposition_so_far_1(p=d, t=t)
        assert pu.as1.is_axiom_of(a=aa, t=t)
        assert pu.as1.is_axiom_of(a=ab, t=t)
        assert pu.as1.is_axiom_of(a=ac, t=t)
        assert pu.as1.is_axiom_of(a=ad, t=t)

        t, i2 = pu.as1.let_x_be_an_inference_rule(
            t=t, f=pu.as1.TransformationByVariableSubstitution(o=y, v=None, i=(a, b, c, d, x,)))
        t, ok, _ = pu.as1.derive_2(t=t, c=y, i=i2, raise_error_if_false=False)
        assert ok

    def test_extension_2(self):
        a, b, c, x, y, z = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'x', 'y', 'z',))
        ext1 = pu.as1.WellFormedAxiomatization()
        ext1, _ = pu.as1.let_x_be_an_axiom(t=ext1, s=a)
        ext1, _ = pu.as1.let_x_be_an_axiom(t=ext1, s=c)
        ext1, i1 = pu.as1.let_x_be_an_inference_rule(
            t=ext1, f=pu.as1.TransformationByVariableSubstitution(o=x, v=None, i=(a, b,)))
        assert isinstance(ext1, pu.as1.WellFormedAxiomatization)

        ab = pu.as1.WellFormedAxiomatization()
        ab, _ = pu.as1.let_x_be_an_axiom(t=ab, s=b)
        ab, i2 = pu.as1.let_x_be_an_inference_rule(
            t=ab, f=pu.as1.TransformationByVariableSubstitution(o=y, v=None, i=(a, c,)))

        ab_extended, _ = pu.as1.let_x_be_an_extension(t=ab, e=ext1)
        assert isinstance(ab_extended, pu.as1.WellFormedAxiomatization)

        _, ok, _ = pu.as1.derive_2(t=ab, c=x, i=i1, raise_error_if_false=False)
        assert not ok
        _, ok, _ = pu.as1.derive_2(t=ab, c=y, i=i2, raise_error_if_false=False)
        assert not ok

        ab_extended, ok, _ = pu.as1.derive_2(t=ab_extended, c=x, i=i1, raise_error_if_false=True)
        assert ok
        ab_extended, ok, _ = pu.as1.derive_2(t=ab_extended, c=y, i=i2, raise_error_if_false=True)
        assert ok


class TestAxiomaticBase:
    """Test the axiomatization-equivalence between theoretical contexts."""

    def test_theoretical_context(self):
        a, b, c, x, y, z = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b', 'c', 'x', 'y', 'z',))
        t1 = pu.as1.WellFormedAxiomatization()
        t1, axiom_a = pu.as1.let_x_be_an_axiom(t=t1, s=a)
        t1, axiom_c = pu.as1.let_x_be_an_axiom(t=t1, s=c)
        t1, i1 = pu.as1.let_x_be_an_inference_rule(
            t=t1, f=pu.as1.TransformationByVariableSubstitution(o=x, v=None, i=(a, b,)))
        assert isinstance(t1, pu.as1.WellFormedAxiomatization)

        t2 = pu.as1.WellFormedAxiomatization()
        t2, axiom_b = pu.as1.let_x_be_an_axiom(t=t2, s=b)
        t2, i2 = pu.as1.let_x_be_an_inference_rule(
            t=t2, f=pu.as1.TransformationByVariableSubstitution(o=y, v=None, i=(a, c,)))

        t3, _ = pu.as1.let_x_be_an_extension(t=t2, e=t1)

        t3, ok, _ = pu.as1.derive_2(t=t3, c=x, i=i1, raise_error_if_false=True)
        t3, ok, _ = pu.as1.derive_2(t=t3, c=y, i=i2, raise_error_if_false=True)

        t4 = pu.as1.WellFormedTheory(t=None, d=(i2, axiom_c, i1, axiom_a, axiom_b,))

        assert not pu.as1.is_axiomatization_equivalent(t1=t2, t2=t4)
        assert not pu.as1.is_axiomatization_equivalent(t1=t1, t2=t4)
        assert not pu.as1.is_axiomatization_equivalent(t1=t2, t2=t3)
        assert not pu.as1.is_axiomatization_equivalent(t1=t1, t2=t3)
        assert pu.as1.is_axiomatization_equivalent(t1=t3, t2=t4)


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
