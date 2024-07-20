import pytest
import punctilious as pu
from punctilious.connectives_standard_library_1 import *


class TestTypesettingConfiguration:
    def test_typesetting_configuration(self):
        p = pu.as1.NullaryConnective()
        p.formula_ts = pu.as1.typesetters.symbol(symbol=pu.pl1.symbols.p_uppercase_serif_italic)
        phi = pu.as1.Formula(con=p)
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.latex_math) == '\\textit{P}'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑃'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'P'

        q = pu.as1.NullaryConnective()
        q.formula_ts = pu.as1.typesetters.symbol(symbol=pu.pl1.symbols.q_uppercase_serif_italic)
        phi = pu.as1.Formula(con=q)
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.latex_math) == '\\textit{Q}'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑄'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'Q'

        ast = pu.as1.BinaryConnective()
        phi = pu.as1.Formula(con=ast, t=(p, q,))

        ast.formula_ts = pu.as1.typesetters.classical_formula(
            connective_typesetter=pu.pl1.symbols.asterisk_operator)
        assert phi.typeset_as_string(
            encoding=pu.pl1.encodings.latex_math) == '\\ast\\left(\\textit{P}, \\textit{Q}\\right)'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '∗(𝑃, 𝑄)'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == '*(P, Q)'

        ast.formula_ts = pu.as1.typesetters.infix_formula(
            connective_typesetter=pu.pl1.symbols.asterisk_operator)
        assert phi.typeset_as_string(
            encoding=pu.pl1.encodings.latex_math) == '\\textit{P} \\ast \\textit{Q}'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑃 ∗ 𝑄'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'P * Q'

        p1 = pu.as1.NullaryConnective()
        p1.formula_ts = pu.as1.typesetters.indexed_symbol(symbol=pu.pl1.symbols.p_uppercase_serif_italic,
                                                          index=1)
        phi = pu.as1.Formula(con=p1)
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.latex_math) == '\\textit{P}_{1}'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑃₁'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'P1'

        p2 = pu.as1.NullaryConnective()
        p2.formula_ts = pu.as1.typesetters.indexed_symbol(symbol=pu.pl1.symbols.p_uppercase_serif_italic,
                                                          index=2)
        phi = pu.as1.Formula(con=p2)
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.latex_math) == '\\textit{P}_{2}'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑃₂'
        assert phi.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'P2'


class TestMonospace:
    def test_monospace(self):
        text = 'The quick brown fox jumps over the lazy dog 0123456789'
        t = pu.pl1.Monospace(text=text)
        output = t.typeset_as_string()
        assert output == '𝚃𝚑𝚎 𝚚𝚞𝚒𝚌𝚔 𝚋𝚛𝚘𝚠𝚗 𝚏𝚘𝚡 𝚓𝚞𝚖𝚙𝚜 𝚘𝚟𝚎𝚛 𝚝𝚑𝚎 𝚕𝚊𝚣𝚢 𝚍𝚘𝚐 0123456789'


class TestScript:
    def test_script(self):
        text = 'The quick brown fox jumps over the lazy dog 0123456789'
        t = pu.pl1.Script(text=text)
        output = t.typeset_as_string()
        assert output == '𝒯𝒽ℯ 𝓆𝓊𝒾𝒸𝓀 𝒷𝓇ℴ𝓌𝓃 𝒻ℴ𝓍 𝒿𝓊𝓂𝓅𝓈 ℴ𝓋ℯ𝓇 𝓉𝒽ℯ 𝓁𝒶𝓏𝓎 𝒹ℴℊ 0123456789'
