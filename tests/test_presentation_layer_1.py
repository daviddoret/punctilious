import pytest
import punctilious as pu


class TestTypesettingConfiguration:
    def test_typesetting_configuration(self):
        p = pu.as1.NullaryConnective()
        p.formula_typesetter = pu.as1.typesetters.symbol(symbol=pu.pl1.symbols.p_uppercase_serif_italic)
        phi = pu.as1.Formula(connective=p)
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.latex_math) == '\\textit{P}'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑃'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'P'

        q = pu.as1.NullaryConnective()
        q.formula_typesetter = pu.as1.typesetters.symbol(symbol=pu.pl1.symbols.q_uppercase_serif_italic)
        phi = pu.as1.Formula(connective=q)
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.latex_math) == '\\textit{Q}'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑄'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'Q'

        ast = pu.as1.BinaryConnective()
        phi = pu.as1.Formula(connective=ast, terms=(p, q,))

        ast.formula_typesetter = pu.as1.typesetters.classical_formula(symbol=pu.pl1.symbols.asterisk_operator)
        assert phi.typeset_as_string(
            encoding=pu.pl1.encodings.latex_math) == '\\ast\\left(\\textit{P}, \\textit{Q}\\right)'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '∗(𝑃, 𝑄)'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == '*(P, Q)'

        ast.formula_typesetter = pu.as1.typesetters.infix_formula(symbol=pu.pl1.symbols.asterisk_operator)
        assert phi.typeset_as_string(
            encoding=pu.pl1.encodings.latex_math) == '\\textit{P} \\ast \\textit{Q}'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑃 ∗ 𝑄'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'P * Q'

        p1 = pu.as1.NullaryConnective()
        p1.formula_typesetter = pu.as1.typesetters.indexed_symbol(symbol=pu.pl1.symbols.p_uppercase_serif_italic,
                                                                  index=1)
        phi = pu.as1.Formula(connective=p1)
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.latex_math) == '\\textit{P}_{1}'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑃₁'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'P1'

        p2 = pu.as1.NullaryConnective()
        p2.formula_typesetter = pu.as1.typesetters.indexed_symbol(symbol=pu.pl1.symbols.p_uppercase_serif_italic,
                                                                  index=2)
        phi = pu.as1.Formula(connective=p2)
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.latex_math) == '\\textit{P}_{2}'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑃₂'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'P2'
