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
    n1_0 = fb1.append_term(c=c1)
    n1_0_0 = n1_0.append_term(c=c3)
    n1_0_1 = n1_0.append_term(c=c2)
    n1_1 = fb1.append_term(c=c2)
    n1_2 = fb1.append_term(c=c3)
    n1_2_0 = n1_2.append_term(c=c1)
    n1_2_0_0 = n1_2_0.append_term(c=c1)
    n1_2_0_0_0 = n1_2_0_0.append_term(c=c1)
    n1_2_0_0_1 = n1_2_0_0.append_term(c=c3)
    n1_2_0_1 = n1_2_0.append_term(c=c1)
    n1_2_1 = n1_2.append_term(c=c2)
    return fb1


@pytest.fixture
def fb5(c1, c2, c3):
    fb1 = as1.FormulaBuilder(c=c1)
    n1_0 = fb1.append_term(c=c1)
    n1_0_0 = n1_0.append_term(c=c3)
    n1_1 = fb1.append_term(c=c2)
    n1_2 = fb1.append_term(c=c3)
    n1_2_0 = n1_2.append_term(c=c1)
    n1_2_0_0 = n1_2_0.append_term(c=c1)
    n1_2_0_0_0 = n1_2_0_0.append_term(c=c1)
    n1_2_0_0_1 = n1_2_0_0.append_term(c=c3)
    n1_2_0_0_2 = n1_2_0_0.append_term(c=c1)
    n1_2_0_1 = n1_2_0.append_term(c=c1)
    n1_2_1 = n1_2.append_term(c=c2)
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


class TestConnective:
    def test_connective(self, c1, c2):
        assert c1 is not c2


class TestFormulaBuilder:
    def test_assure_term(self):
        fb = as1.FormulaBuilder()
        fb.assure_term(i=3)
        assert len(fb.terms) == 4

    def test_formula_builder(self, c1, c2, c3, fb4):
        assert fb4.c is c1
        assert fb4.terms[0].c is c1
        assert fb4.terms[1].c is c2
        assert fb4.terms[2].c is c3

    def test_term_0(self, c1, c2, c3):
        fb = as1.FormulaBuilder()
        fb.term_0 = c1
        assert fb.term_0.c is c1
        assert fb.terms[0].c is c1

    def test_to_formula(self, fb4):
        phi1 = fb4.to_formula()
        assert phi1.c is fb4.c
        assert phi1.terms[0].c is fb4.terms[0].c
        assert phi1.terms[0].terms[0].c is fb4.terms[0].terms[0].c
        assert phi1.terms[0].terms[1].c is fb4.terms[0].terms[1].c
        assert phi1.terms[1].c is fb4.terms[1].c
        assert phi1.terms[2].c is fb4.terms[2].c
        assert phi1.terms[2].terms[0].c is fb4.terms[2].terms[0].c
        assert phi1.terms[2].terms[0].terms[0].c is fb4.terms[2].terms[0].terms[0].c
        assert phi1.terms[2].terms[0].terms[1].c is fb4.terms[2].terms[0].terms[1].c
        assert phi1.terms[2].terms[1].c is fb4.terms[2].terms[1].c


class TestTermsBuilder:
    def test_terms_builder(self, fb1, fb2, fb3):
        terms1 = as1.TermsBuilder()
        assert len(terms1) == 0
        terms2 = as1.TermsBuilder(terms=(fb1,))
        assert len(terms2) == 1
        assert terms2[0].c is fb1.c
        assert terms2.term_0.c is fb1.c
        terms3 = as1.TermsBuilder(terms=(fb1, fb2, fb1, fb1, fb3))
        assert len(terms3) == 5
        assert terms3[0].c is fb1.c
        assert terms3.term_0.c is fb1.c
        assert terms3[1].c is fb2.c
        assert terms3.term_1.c is fb2.c
        assert terms3[2].c is fb1.c
        assert terms3[3].c is fb1.c
        assert terms3[4].c is fb3.c


class TestTerms:
    def test_terms(self, phi1, phi2, phi3):
        terms1 = as1.Terms()
        assert len(terms1) == 0
        terms2 = as1.Terms(terms=(phi1,))
        assert len(terms2) == 1
        assert terms2[0].c is phi1.c
        assert terms2.term_0.c is phi1.c
        terms3 = as1.Terms(terms=(phi1, phi2, phi1, phi1, phi3))
        assert len(terms3) == 5
        assert terms3[0].c is phi1.c
        assert terms3.term_0.c is phi1.c
        assert terms3[1].c is phi2.c
        assert terms3.term_1.c is phi2.c
        assert terms3[2].c is phi1.c
        assert terms3[3].c is phi1.c
        assert terms3[4].c is phi3.c


class TestFormula:

    def test_formula(self, c1, c2, c3, phi4):
        assert phi4.c is c1
        assert phi4.terms[0].c is c1
        assert phi4.terms[1].c is c2
        assert phi4.terms[2].c is c3

    def test_term_1(self, c1, c2, c3):
        fb = as1.FormulaBuilder()
        fb.term_0 = c1
        phi = fb.to_formula()
        assert phi.term_0.c is c1
        assert phi.terms[0].c is c1

    def test_to_formula_builder(self, phi4):
        fb1 = phi4.to_formula_builder()
        assert fb1.c is phi4.c
        assert fb1.terms[0].c is phi4.terms[0].c
        assert fb1.terms[0].terms[0].c is phi4.terms[0].terms[0].c
        assert fb1.terms[0].terms[1].c is phi4.terms[0].terms[1].c
        assert fb1.terms[1].c is phi4.terms[1].c
        assert fb1.terms[2].c is phi4.terms[2].c
        assert fb1.terms[2].terms[0].c is phi4.terms[2].terms[0].c
        assert fb1.terms[2].terms[0].terms[0].c is phi4.terms[2].terms[0].terms[0].c
        assert fb1.terms[2].terms[0].terms[1].c is phi4.terms[2].terms[0].terms[1].c
        assert fb1.terms[2].terms[1].c is phi4.terms[2].terms[1].c


class TestConnectiveEquivalence:
    def test_is_connective_equivalent(self, c1, c2, c3):
        assert as1.is_connective_equivalent(c=c1, d=c1)
        assert not as1.is_connective_equivalent(c=c1, d=c2)


class TestFormulaEquivalence:
    def test_is_formula_equivalent(self, phi2, phi3, phi4, phi5):
        assert as1.is_formula_equivalent(phi=phi2, psi=phi2)
        assert as1.is_formula_equivalent(phi=phi3, psi=phi3)
        assert as1.is_formula_equivalent(phi=phi4, psi=phi4)
        assert as1.is_formula_equivalent(phi=phi5, psi=phi5)
        assert not as1.is_formula_equivalent(phi=phi2, psi=phi3)
        assert not as1.is_formula_equivalent(phi=phi3, psi=phi4)
        assert not as1.is_formula_equivalent(phi=phi4, psi=phi5)
