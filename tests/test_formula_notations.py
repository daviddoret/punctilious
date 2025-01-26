import punctilious as pu


class TestFormulaNotations:

    def test_atomic_formula(self):
        unicode_basic_option = pu.rpr.Option('technical_language', 'unicode_basic')
        unicode_extended_option = pu.rpr.Option('technical_language', 'unicode_extended')
        latex_math_option = pu.rpr.Option('technical_language', 'latex_math')
        prefs = pu.rpr.Preferences()
        x = pu.formal_language.Connector(
            connector_representation=pu.latin_alphabet_uppercase_serif_italic.x,
            formula_representation=pu.formula_notations.atomic_formula,
        )
        renderer_123 = pu.representation.RendererForStringConstant('123')
        subscript_123 = pu.representation.AbstractRepresentation(
            uid=None, renderers=(renderer_123,))
        x123 = pu.formal_language.Connector(
            connector_representation=pu.latin_alphabet_uppercase_serif_italic.x,
            subscript_representation=subscript_123,
            formula_representation=pu.formula_notations.atomic_formula,
        )
        prefs[unicode_basic_option] = 100
        assert not x().connector.has_subscript
        assert x().represent(prefs=prefs) == 'X'
        assert x123().represent(prefs=prefs) == 'X123'
        prefs[unicode_extended_option] = 200
        assert x().represent(prefs=prefs) == '𝑋'
        assert x123().represent(prefs=prefs) == '𝑋₁₂₃'
        prefs[latex_math_option] = 10000
        assert x().represent(prefs=prefs) == '\\textit{X}'
        assert x123().represent(prefs=prefs) == '\\textit{X}_{123}'

    def test_infix_notation(self):
        prefs = pu.rpr.Preferences()
        tag = pu.rpr.Option('technical_language', 'unicode_basic')
        prefs[tag] = 100
        assert pu.formula_notations.infix_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y',)},
            prefs=prefs) == 'x f y'

    def test_formula_notation(self):
        prefs = pu.rpr.Preferences()
        tag = pu.rpr.Option('technical_language', 'unicode_basic')
        prefs[tag] = 100

        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ()},
            prefs=prefs) == 'f()'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x',)},
            prefs=prefs) == 'f(x)'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y',)},
            prefs=prefs) == 'f(x, y)'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y', 'z',)},
            prefs=prefs) == 'f(x, y, z)'

        tag = pu.rpr.Option('technical_language', 'latex_math')
        prefs[tag] = 200

        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x',)},
            prefs=prefs) == 'f\\left(x\\right)'

    def test_prefix_notation(self):
        prefs = pu.rpr.Preferences()
        tag = pu.rpr.Option('technical_language', 'unicode_basic')
        prefs[tag] = 100

        assert pu.formula_notations.prefix_formula.rep(
            variables={'connector': '++', 'argument': ('x',)},
            prefs=prefs) == '++x'
        pass
