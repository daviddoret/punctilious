import pytest
import uuid

import punctilious.abstract_formal_language as afl


class TestConnectorIndex:
    def test_connector_index_01(self):
        fp0 = afl.ConnectorIndex(0)
        fp0b = afl.ConnectorIndex(0)
        fp1 = afl.ConnectorIndex(1)
        assert fp0 == fp0b
        assert fp0 != fp1
        assert fp0 is fp0b
        assert fp0 is not fp1
        assert fp1 > fp0
        with pytest.raises(Exception) as e:
            afl.ConnectorIndex(None)
        with pytest.raises(Exception) as e:
            afl.ConnectorIndex('a')

    def test_connector_index_equivalence(self):
        fp0 = afl.ConnectorIndex(0)
        fp0b = afl.ConnectorIndex(0)
        fp1 = afl.ConnectorIndex(1)
        assert fp0.is_connector_index_equivalent_to(fp0b)
        assert not (fp0.is_connector_index_equivalent_to(fp1))
        assert not (fp1.is_connector_index_equivalent_to(fp0))
        assert not (fp1.is_connector_index_equivalent_to(fp0b))
        assert fp1.is_connector_index_equivalent_to(fp1)


class TestAbstractFormulaTerms:
    def test_abstract_formula_terms_hash(self):
        t1 = afl.AbstractFormulaTerms()
        t2 = afl.AbstractFormulaTerms()
        assert hash(t1) == hash(t2)
        t3 = afl.AbstractFormulaTerms((0, 1, 2, 3,))
        t4 = afl.AbstractFormulaTerms((0, 1, 2, 3,))
        assert hash(t3) == hash(t4)
        t5 = afl.AbstractFormulaTerms((0, 1, 2, 2,))
        assert not hash(t5) == hash(t3)
        t6 = afl.AbstractFormulaTerms((0, 1, 2,))
        assert not hash(t6) == hash(t3)
        t7 = afl.AbstractFormulaTerms((0, 1, (1, (2, 3, 4, 5, 6, 7, (7, (1, 2)))), 3,))
        t8 = afl.AbstractFormulaTerms((0, 1, (1, (2, 3, 4, 5, 6, 7, (7, (1, 2)))), 3,))
        t9 = afl.AbstractFormulaTerms((0, 1, (1, (2, 3, 4, 5, 6, 7, (7, (1, 1)))), 3,))
        assert hash(t7) == hash(t8)
        assert not hash(t7) == hash(t9)


class TestAbstractFormula:

    def test_abstract_formula_01(self):
        s0 = afl.AbstractFormula(0)
        assert s0.is_leaf
        assert s0.is_canonical
        s0b = afl.AbstractFormula(0)
        assert s0 == s0b
        assert id(s0) == id(s0b)
        assert s0 is s0b
        s1 = afl.AbstractFormula(1)
        assert s1.is_leaf
        assert not s1.is_canonical
        assert s1 is not s0
        s2 = afl.AbstractFormula(2)
        assert s2.is_leaf
        assert not s2.is_canonical
        s3 = afl.AbstractFormula(0, (s0,))
        assert not s3.is_leaf
        assert s3.is_canonical
        s4 = afl.AbstractFormula(0, (s1,))
        assert not s4.is_leaf
        assert s4.is_canonical
        s5 = afl.AbstractFormula(0, (s2,))
        assert not s5.is_leaf
        assert not s5.is_canonical
        s6 = afl.AbstractFormula(0, (s2, s5, s1, s0,))
        assert not s6.is_leaf
        assert not s6.is_canonical
        s7 = afl.AbstractFormula(0, (s1, s2, s3, s4, s5, s6,))
        assert not s7.is_leaf
        assert s7.is_canonical
        s7b = afl.AbstractFormula(0, (s1, s2, s3, s4, s5, s6,))
        assert s7 == s7b
        assert id(s7) == id(s7b)
        assert s7 is s7b
        assert s7 is not s5
        pass

    def test_abstract_formula_hash(self):
        pass

    def test_abstract_formula_is_canonical(self):
        fs1 = afl.AbstractFormula(0)
        assert fs1.is_canonical
        fs2 = afl.AbstractFormula(0, (1, 2, 3))
        assert fs1.is_canonical
        fs3 = afl.AbstractFormula(1)
        assert not fs3.is_canonical
        fs4 = afl.AbstractFormula(0, (3, 2, 3))
        assert not fs4.is_canonical
        fs5 = afl.AbstractFormula(0, (0, 1, (2, (3, 1, 0, 0)), 2, 3))
        assert fs5.is_canonical
        fs6 = afl.AbstractFormula(0, (0, 1, (2, (3, 1, 0, 5)), 2, 3))
        assert not fs6.is_canonical

    def test_abstract_formula_equivalence(self):
        fs1 = afl.AbstractFormula(0)
        assert fs1.is_abstract_formula_equivalent_to(fs1)
        fs2 = afl.AbstractFormula(1)
        assert not fs1.is_abstract_formula_equivalent_to(fs2)
        fs3 = afl.AbstractFormula(0, (1, 2, 0, 1,))
        assert not fs1.is_abstract_formula_equivalent_to(fs3)
        fs4 = afl.AbstractFormula(0, (1, 2, 0, 1,))
        assert fs3.is_abstract_formula_equivalent_to(fs4)
        fs5 = afl.AbstractFormula(0, (1, 2, 1, 1,))
        assert not fs3.is_abstract_formula_equivalent_to(fs5)
        fs6 = afl.AbstractFormula(0, (1, (0, (1, 2, 3,)), 0, 1,))
        assert fs6.is_abstract_formula_equivalent_to(fs6)
        fs7 = afl.AbstractFormula(0, (1, (0, (1, 2, 2,)), 0, 1,))
        assert not fs7.is_abstract_formula_equivalent_to(fs6)

    def test_abstract_formula_substitute_indexes(self):
        # TODO: RESUME HERE
        m1 = {0: 1}
        fs1 = afl.AbstractFormula(0)
        fs1b = fs1.transform_by_connector_index_substitution(m1)
        fs1c = afl.AbstractFormula(1)
        assert fs1b is fs1c
