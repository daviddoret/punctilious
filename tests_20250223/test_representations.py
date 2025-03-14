import punctilious_20250223 as pu


class TestRepresentation:
    def test_representation(self):
        p = pu.declare_variable(rep=pu.latin_alphabet_uppercase_serif_italic.p)
        q = pu.declare_variable(rep=pu.latin_alphabet_uppercase_serif_italic.q)
        phi = pu.fml.Formula(pu.operators.conjunction, (p, q,))
        # print(phi)


class TestRendererForStringConstant:
    def test_renderer_for_string_constant(self):
        r1 = pu.rpr.RendererForStringConstant(string_constant='hello')
        assert r1.rep() == 'hello'
        r2 = pu.rpr.RendererForStringConstant(string_constant='world')
        assert r2.rep() == 'world'


class TestRendererForStringTemplate:
    def test_renderer_for_string_template(self):
        r1 = pu.rpr.RendererForStringTemplate(string_template='hello {{ a1 }}')
        assert r1.rep(variables={'a1': 'world'}) == 'hello world'
