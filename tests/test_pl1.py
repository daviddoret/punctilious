import pytest

import fl1
import log
import punctilious as pu


class TestPL1:
    def test_connectives_conditional(self):
        l: pu.pl1.PL1 = pu.pl1.PL1()

        y = l.connectives.conditional
        assert y.to_string(protocol=pu.ts.protocols.latex) == "\\rightarrow"
        assert y.to_string(protocol=pu.ts.protocols.unicode_extended) == "→"
        assert y.to_string(protocol=pu.ts.protocols.unicode_limited) == "-->"

    def test_connectives_negation(self):
        l: pu.pl1.PL1 = pu.pl1.PL1()
        x = l.connectives.negation

        # reset preference
        pu.pl1_presentation.preferences.negation_symbol.reset()
        assert x.to_string(protocol=pu.ts.protocols.latex) == "\\lnot"
        assert x.to_string(protocol=pu.ts.protocols.unicode_extended) == "¬"
        assert x.to_string(protocol=pu.ts.protocols.unicode_limited) == "not"

        # change preference
        pu.pl1_presentation.preferences.negation_symbol.symbol = pu.ts.symbols.tilde
        assert x.to_string(protocol=pu.ts.protocols.latex) == "\\sim"
        assert x.to_string(protocol=pu.ts.protocols.unicode_extended) == "~"
        assert x.to_string(protocol=pu.ts.protocols.unicode_limited) == "~"

        # reset preference
        pu.pl1_presentation.preferences.negation_symbol.reset()
        assert x.to_string(protocol=pu.ts.protocols.latex) == "\\lnot"
        assert x.to_string(protocol=pu.ts.protocols.unicode_extended) == "¬"
        assert x.to_string(protocol=pu.ts.protocols.unicode_limited) == "not"

    def test_formulas(self):
        l1: pu.pl1.PL1 = pu.pl1.PL1()
        pa = l1.propositional_variables.declare_proposition_variable()
        phi1 = l1.compound_formulas.declare_unary_formula(connective=l1.connectives.negation, term=pa)
        assert phi1 in l1.compound_formulas
        assert phi1.to_string(protocol=pu.ts.protocols.unicode_extended) == '¬𝑃'
        assert phi1.to_string(protocol=pu.ts.protocols.unicode_limited) == 'notP'
        assert phi1.to_string(protocol=pu.ts.protocols.latex) == '\\lnot\\textit{P}'

        pb = l1.propositional_variables.declare_proposition_variable()
        phi2 = l1.compound_formulas.declare_binary_formula(connective=l1.connectives.conditional, term_1=pa, term_2=pb)
        assert phi2 in l1.compound_formulas
        assert phi1.to_string(protocol=pu.ts.protocols.unicode_extended) == '¬𝑃'
        assert phi1.to_string(protocol=pu.ts.protocols.unicode_limited) == 'notP'
        assert phi1.to_string(protocol=pu.ts.protocols.latex) == '\\lnot\\textit{P}'

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
        pu.preferences.reset()

        l: pu.pl1.PL1 = pu.pl1.PL1()

        assert len(l.propositional_variables) == 0
        pa = l.propositional_variables.declare_proposition_variable()
        assert len(l.propositional_variables) == 1
        pb = l.propositional_variables.declare_proposition_variable()
        assert len(l.propositional_variables) == 2
        assert pa is not pb

        pc, pd, pe = l.propositional_variables.declare_proposition_variables(n=3)

        pu.preferences.typesetting.protocol.protocol = pu.ts.protocols.unicode_extended

        phi1 = l.compound_formulas.declare_binary_formula(connective=l.connectives.conditional, term_1=pa, term_2=pb)
        phi2 = l.compound_formulas.declare_binary_formula(connective=l.connectives.conditional, term_1=phi1, term_2=pc)
        phi3 = l.compound_formulas.declare_binary_formula(connective=l.connectives.conditional, term_1=phi2, term_2=pd)
        phi4 = l.compound_formulas.declare_binary_formula(connective=l.connectives.conditional, term_1=phi3, term_2=pe)

        log.debug(msg=phi4)
        pass

    def test_declare_unary_formula(self):
        l1: pu.pl1.PL1 = pu.pl1.PL1()

        lnot: fl1.UnaryConnective = l1.connectives.negation
        pa = l1.propositional_variables.declare_proposition_variable()
        pb = l1.propositional_variables.declare_proposition_variable()
        pc = l1.propositional_variables.declare_proposition_variable()

        pd: fl1.UnaryFormula = l1.compound_formulas.declare_unary_formula(connective=lnot, term=pa)
        pe: fl1.UnaryFormula = l1.compound_formulas.declare_unary_formula(connective=lnot, term=pa)
        # Check that only unique formulas are kept in the PL1 formula collection
        assert pd is pe
        assert pd == pe
        assert id(pd) == id(pe)
        # Check that non-unique formulas are kept
        pf: fl1.UnaryFormula = l1.compound_formulas.declare_unary_formula(connective=lnot, term=pb)
        assert pd is not pf
        assert pd != pf
        assert id(pd) != id(pf)

    def test_declare_binary_formula(self):
        l1 = pu.pl1.PL1()

        conditional = l1.connectives.conditional
        pa = l1.propositional_variables.declare_proposition_variable()
        pb = l1.propositional_variables.declare_proposition_variable()

        pd = l1.compound_formulas.declare_binary_formula(connective=conditional, term_1=pa, term_2=pb)
        # Check that only unique formulas are kept in the PL1 formula collection
        assert pd.to_string(protocol=pu.ts.protocols.unicode_extended) == '𝑃 → 𝑄'
        assert pd.to_string(protocol=pu.ts.protocols.unicode_limited) == 'P --> Q'
        assert pd.to_string(protocol=pu.ts.protocols.latex) == '\\textit{P} \\rightarrow \\textit{Q}'

    def test_compounding_formulas_1(self):
        l1 = pu.pl1.PL1()

        lnot = l1.connectives.negation
        limplies = l1.connectives.conditional

        # build a compounding formula with several layers of depth
        pa = l1.propositional_variables.declare_proposition_variable()
        pb = l1.propositional_variables.declare_proposition_variable()
        pc = l1.propositional_variables.declare_proposition_variable()
        pd = l1.compound_formulas.declare_unary_formula(connective=lnot, term=pa)
        pe = l1.compound_formulas.declare_unary_formula(connective=lnot, term=pd)
        pf = l1.compound_formulas.declare_binary_formula(connective=limplies, term_1=pe, term_2=pb)
        pg = l1.compound_formulas.declare_binary_formula(connective=limplies, term_1=pf, term_2=pf)
        ph = l1.compound_formulas.declare_binary_formula(connective=limplies, term_1=pa, term_2=pg)
        pi = l1.compound_formulas.declare_unary_formula(connective=lnot, term=ph)

        assert len(str(pi)) > 0
        log.debug(msg=str(pi))


class TestPL1ML:
    def test_substitute_meta_variables(self):
        l1 = pu.pl1.PL1()

        va = l1.meta_language.meta_variables.declare_meta_variable()
        vb = l1.meta_language.meta_variables.declare_meta_variable()
        pa = l1.propositional_variables.declare_proposition_variable()
        pb = l1.propositional_variables.declare_proposition_variable()
        pc = l1.propositional_variables.declare_proposition_variable()
        map1 = {va: pa}
        map2 = {va: pa, vb: pb}

        phi = pa
        psi = l1.meta_language.substitute_meta_variables(phi=phi, m=map1)
        assert psi == pa

        phi = va
        psi = l1.meta_language.substitute_meta_variables(phi=phi, m=map1)
        assert psi == pa

        phi = l1.compound_formulas.declare_unary_formula(connective=l1.connectives.negation, term=pa)
        psi = l1.meta_language.substitute_meta_variables(phi=phi, m=map1)
        assert psi == phi

        phi = l1.meta_language.compound_formulas.declare_binary_formula(connective=l1.connectives.conditional,
            term_1=pa, term_2=va)
        pu.log.info(f'{phi}')
        psi = l1.meta_language.substitute_meta_variables(phi=phi, m=map1)
        chi = l1.compound_formulas.declare_binary_formula(connective=l1.connectives.conditional, term_1=pa, term_2=pa)
        pu.log.info(f'{psi} == {chi}')
        assert psi == chi

        phi2 = l1.meta_language.compound_formulas.declare_binary_formula(connective=l1.connectives.conditional,
            term_1=vb, term_2=phi)
        pu.log.info(f'{phi2}')
        psi = l1.meta_language.substitute_meta_variables(phi=phi2, m=map2)
        chi2 = l1.compound_formulas.declare_binary_formula(connective=l1.connectives.conditional, term_1=pb, term_2=chi)
        pu.log.info(f'{psi} == {chi2}')
        assert psi == chi2
