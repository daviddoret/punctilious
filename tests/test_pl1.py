import pytest

import fl1
import punctilious as pu


class TestPL1:
    def test_connectives_1(self):
        l: pu.pl1.PL1 = pu.pl1.PL1()

        y = l.connectives.conditional
        assert y.to_string(protocol=pu.ts.protocols.latex) == "\\rightarrow"
        assert y.to_string(protocol=pu.ts.protocols.unicode_extended) == "→"
        assert y.to_string(protocol=pu.ts.protocols.unicode_limited) == "-->"

    def test_connectives_2(self):
        l: pu.pl1.PL1 = pu.pl1.PL1()

        x = l.connectives.negation
        assert x.to_string(protocol=pu.ts.protocols.latex) == "\\lnot"
        assert x.to_string(protocol=pu.ts.protocols.unicode_extended) == "¬"
        assert x.to_string(protocol=pu.ts.protocols.unicode_limited) == "lnot"

    def test_connectives_3(self):
        l: pu.pl1.PL1 = pu.pl1.PL1()
        x = l.connectives.negation
        # change flavor preference
        pu.pl1_ts.flavors.negation_tilde.predecessor = pu.pl1_ts.flavors.negation_not
        assert x.to_string(protocol=pu.ts.protocols.latex) == "\\sim"
        assert x.to_string(protocol=pu.ts.protocols.unicode_extended) == "~"
        assert x.to_string(protocol=pu.ts.protocols.unicode_limited) == "~"

        # restore flavor preference
        pu.pl1_ts.flavors.negation_not.predecessor = pu.pl1_ts.flavors.negation_tilde
        assert x.to_string(protocol=pu.ts.protocols.latex) == "\\lnot"
        assert x.to_string(protocol=pu.ts.protocols.unicode_extended) == "¬"
        assert x.to_string(protocol=pu.ts.protocols.unicode_limited) == "lnot"

    def test_formulas(self):
        l1: pu.pl1.PL1 = pu.pl1.PL1()
        pa = l1.propositional_variables.declare_proposition_variable()
        phi1 = l1.compound_formulas.declare_unary_formula(connective=l1.connectives.negation, term=pa)
        assert phi1 in l1.compound_formulas

        pb = l1.propositional_variables.declare_proposition_variable()
        phi2 = l1.compound_formulas.declare_binary_formula(connective=l1.connectives.conditional, term_1=pa, term_2=pb)
        assert phi2 in l1.compound_formulas

        l2: pu.pl1.PL1 = pu.pl1.PL1()
        with pytest.raises(Exception) as e_info:
            # connective not in the language
            l1.compound_formulas.declare_unary_formula(connective=l2.connectives.negation, term=pa)

        l2_pa = l2.propositional_variables.declare_proposition_variable()
        with pytest.raises(Exception) as e_info:
            # term not in the language
            l1.compound_formulas.declare_unary_formula(connective=l1.connectives.negation, term=l2_pa)

        # compound of compound formula
        phi3 = l1.compound_formulas.declare_binary_formula(connective=l1.connectives.conditional, term_1=phi1,
            term_2=phi2)
        assert phi3 in l1.compound_formulas

        pass

    def test_propositional_variables(self):
        l: pu.pl1.PL1 = pu.pl1.PL1()

        assert len(l.propositional_variables) == 0
        pa = l.propositional_variables.declare_proposition_variable()
        assert len(l.propositional_variables) == 1
        pb = l.propositional_variables.declare_proposition_variable()
        assert len(l.propositional_variables) == 2
        assert pa is not pb

    def test_declare_unary_formula(self):
        l1: pu.pl1.PL1 = pu.pl1.PL1()

        lnot: fl1.UnaryConnective = l1.connectives.negation
        pa = l1.propositional_variables.declare_proposition_variable()
        pb = l1.propositional_variables.declare_proposition_variable()
        pc = l1.propositional_variables.declare_proposition_variable()

        pd: fl1.UnaryFormula = l1.compound_formulas.declare_unary_formula(connective=lnot, term=pa)
        pe: fl1.UnaryFormula = l1.compound_formulas.declare_unary_formula(connective=lnot, term=pa)
        # Check that two equal formulas are only instanciated once in python
        assert pd is pe
        assert pd == pe
        assert id(pd) == id(pe)
        pf: fl1.UnaryFormula = l1.compound_formulas.declare_unary_formula(connective=lnot, term=pb)
        assert pd is not pf
        assert pd != pf
        assert id(pd) != id(pf)
