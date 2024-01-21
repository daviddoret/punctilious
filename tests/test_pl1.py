import pytest
import punctilious as pu


class TestPL1:
    def test_connectives(self):
        l: pu.pl1.PL1 = pu.pl1.PL1()

        y = l.connectives.material_implication
        assert y.to_string(protocol=pu.ts.protocols.latex) == "\\rightarrow"
        assert y.to_string(protocol=pu.ts.protocols.unicode_extended) == "→"
        assert y.to_string(protocol=pu.ts.protocols.unicode_limited) == "-->"

        x = l.connectives.negation
        assert x.to_string(protocol=pu.ts.protocols.latex) == "\\lnot"
        assert x.to_string(protocol=pu.ts.protocols.unicode_extended) == "¬"
        assert x.to_string(protocol=pu.ts.protocols.unicode_limited) == "lnot"

    def test_formulas(self):
        l1: pu.pl1.PL1 = pu.pl1.PL1()
        pa = l1.propositional_variables.declare_proposition_variable()
        phi1 = l1.formulas.declare_unary_formula(connective=l1.connectives.negation, term=pa)
        assert phi1 in l1.formulas

        pb = l1.propositional_variables.declare_proposition_variable()
        phi2 = l1.formulas.declare_binary_formula(connective=l1.connectives.material_implication, term_1=pa, term_2=pb)
        assert phi2 in l1.formulas

        l2: pu.pl1.PL1 = pu.pl1.PL1()
        with pytest.raises(Exception) as e_info:
            # connective not in the language
            l1.formulas.declare_unary_formula(connective=l2.connectives.negation, term=pa)

        l2_pa = l2.propositional_variables.declare_proposition_variable()
        with pytest.raises(Exception) as e_info:
            # term not in the language
            l1.formulas.declare_unary_formula(connective=l1.connectives.negation, term=l2_pa)

        # compound of compound formula
        phi3 = l1.formulas.declare_binary_formula(connective=l1.connectives.material_implication, term_1=phi1,
            term_2=phi2)
        assert phi3 in l1.formulas

        pass

    def test_propositional_variables(self):
        l: pu.pl1.PL1 = pu.pl1.PL1()

        assert len(l.propositional_variables) == 0
        pa = l.propositional_variables.declare_proposition_variable()
        assert len(l.propositional_variables) == 1
        pb = l.propositional_variables.declare_proposition_variable()
        assert len(l.propositional_variables) == 2
        assert pa is not pb
