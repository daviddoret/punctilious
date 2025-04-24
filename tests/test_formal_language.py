import pytest
import uuid

import punctilious.formal_language as fl


class TestConnectorIndex:
    def test_connector_index_01(self):
        fp0 = fl.ConnectorIndex(0)
        fp0b = fl.ConnectorIndex(0)
        fp1 = fl.ConnectorIndex(1)
        assert fp0 == fp0b
        assert fp0 != fp1
        assert fp0 is fp0b
        assert fp0 is not fp1
        assert fp1 > fp0
        with pytest.raises(Exception) as e:
            fl.ConnectorIndex(None)
        with pytest.raises(Exception) as e:
            fl.ConnectorIndex('a')

    def test_connector_index_equivalence(self):
        fp0 = fl.ConnectorIndex(0)
        fp0b = fl.ConnectorIndex(0)
        fp1 = fl.ConnectorIndex(1)
        assert fp0.is_connector_index_equivalent_to(fp0b)
        assert not (fp0.is_connector_index_equivalent_to(fp1))
        assert not (fp1.is_connector_index_equivalent_to(fp0))
        assert not (fp1.is_connector_index_equivalent_to(fp0b))
        assert fp1.is_connector_index_equivalent_to(fp1)


class TestFormulaStructureTerms:
    def test_formula_structure_terms_hash(self):
        t1 = fl.FormulaStructureTerms()
        t2 = fl.FormulaStructureTerms()
        assert hash(t1) == hash(t2)
        t3 = fl.FormulaStructureTerms((0, 1, 2, 3,))
        t4 = fl.FormulaStructureTerms((0, 1, 2, 3,))
        assert hash(t3) == hash(t4)
        t5 = fl.FormulaStructureTerms((0, 1, 2, 2,))
        assert not hash(t5) == hash(t3)
        t6 = fl.FormulaStructureTerms((0, 1, 2,))
        assert not hash(t6) == hash(t3)
        t7 = fl.FormulaStructureTerms((0, 1, (1, (2, 3, 4, 5, 6, 7, (7, (1, 2)))), 3,))
        t8 = fl.FormulaStructureTerms((0, 1, (1, (2, 3, 4, 5, 6, 7, (7, (1, 2)))), 3,))
        t9 = fl.FormulaStructureTerms((0, 1, (1, (2, 3, 4, 5, 6, 7, (7, (1, 1)))), 3,))
        assert hash(t7) == hash(t8)
        assert not hash(t7) == hash(t9)


class TestFormulaStructure:

    def test_formula_structure_01(self):
        s0 = fl.FormulaStructure(0)
        assert s0.is_leaf
        assert s0.is_canonical
        s0b = fl.FormulaStructure(0)
        assert s0 == s0b
        assert id(s0) == id(s0b)
        assert s0 is s0b
        s1 = fl.FormulaStructure(1)
        assert s1.is_leaf
        assert not s1.is_canonical
        assert s1 is not s0
        s2 = fl.FormulaStructure(2)
        assert s2.is_leaf
        assert not s2.is_canonical
        s3 = fl.FormulaStructure(0, (s0,))
        assert not s3.is_leaf
        assert s3.is_canonical
        s4 = fl.FormulaStructure(0, (s1,))
        assert not s4.is_leaf
        assert s4.is_canonical
        s5 = fl.FormulaStructure(0, (s2,))
        assert not s5.is_leaf
        assert not s5.is_canonical
        s6 = fl.FormulaStructure(0, (s2, s5, s1, s0,))
        assert not s6.is_leaf
        assert not s6.is_canonical
        s7 = fl.FormulaStructure(0, (s1, s2, s3, s4, s5, s6,))
        assert not s7.is_leaf
        assert s7.is_canonical
        s7b = fl.FormulaStructure(0, (s1, s2, s3, s4, s5, s6,))
        assert s7 == s7b
        assert id(s7) == id(s7b)
        assert s7 is s7b
        assert s7 is not s5
        pass

    def test_formula_structure_hash(self):
        pass

    def test_formula_structure_is_canonical(self):
        fs1 = fl.FormulaStructure(0)
        assert fs1.is_canonical
        fs2 = fl.FormulaStructure(0, (1, 2, 3))
        assert fs1.is_canonical
        fs3 = fl.FormulaStructure(1)
        assert not fs3.is_canonical
        fs4 = fl.FormulaStructure(0, (3, 2, 3))
        assert not fs4.is_canonical
        fs5 = fl.FormulaStructure(0, (0, 1, (2, (3, 1, 0, 0)), 2, 3))
        assert fs5.is_canonical
        fs6 = fl.FormulaStructure(0, (0, 1, (2, (3, 1, 0, 5)), 2, 3))
        assert not fs6.is_canonical

    def test_formula_structure_equivalence(self):
        fs1 = fl.FormulaStructure(0)
        assert fs1.is_formula_structure_equivalent_to(fs1)
        fs2 = fl.FormulaStructure(1)
        assert not fs1.is_formula_structure_equivalent_to(fs2)
        fs3 = fl.FormulaStructure(0, (1, 2, 0, 1,))
        assert not fs1.is_formula_structure_equivalent_to(fs3)
        fs4 = fl.FormulaStructure(0, (1, 2, 0, 1,))
        assert fs3.is_formula_structure_equivalent_to(fs4)
        fs5 = fl.FormulaStructure(0, (1, 2, 1, 1,))
        assert not fs3.is_formula_structure_equivalent_to(fs5)
        fs6 = fl.FormulaStructure(0, (1, (0, (1, 2, 3,)), 0, 1,))
        assert fs6.is_formula_structure_equivalent_to(fs6)
        fs7 = fl.FormulaStructure(0, (1, (0, (1, 2, 2,)), 0, 1,))
        assert not fs7.is_formula_structure_equivalent_to(fs6)


class TestConnector:
    def test_connector_1(self):
        uid1 = uuid.uuid4()
        uid2 = uuid.uuid4()
        c1 = fl.Connector(uid=uid1)
        c2 = fl.Connector(uid=uid2)
        assert c1.is_connector_equivalent_to(c1)
        assert not (c1.is_connector_equivalent_to(c2))
        assert c1 != c2
        assert c1 == c1
        assert c2 == c2
        c1_reuse = fl.Connector(uid=uid1)
        assert c1 == c1_reuse
        assert c1 is c1_reuse
        assert id(c1) == id(c1_reuse)
        assert c1_reuse != c2


class TestFormula:
    def test_formula(self):
        c1 = fl.Connector()
        c2 = fl.Connector()
        c3 = fl.Connector()
        s1 = fl.FormulaStructure(0)
        s2 = fl.FormulaStructure(1)
        s3 = fl.FormulaStructure(0, (s1,))
        s4 = fl.FormulaStructure(1, (s1, s2,))
        s4 = fl.FormulaStructure(2, (s3, s1, s2, s3, s4,))
        phi1 = fl.Formula((c1,), s1)
        phi2 = fl.Formula((c2,), s1)
        assert phi1 != phi2
        phi1b = fl.Formula((c1,), s1)
        assert phi1 == phi1b
        phi3 = fl.Formula((c1,), s3)
        phi4 = fl.Formula((c2,), s3)
        with pytest.raises(Exception) as e:
            fl.Formula((c2, c2,), s3)
        phi5 = fl.Formula((c2, c3, c1,), s4)
        phi6 = fl.Formula((c3, c2, c1,), s4)
        phi7 = fl.Formula((c1, c2, c3,), s4)
        pass
