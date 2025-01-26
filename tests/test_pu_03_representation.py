import punctilious as pu


class TestTypesettingLibrary:

    def test_is_unicode_subscriptable(self):
        assert pu.representation.TypesettingLibrary.is_unicode_subscriptable('123')
        assert pu.representation.TypesettingLibrary.is_unicode_subscriptable('aex')
        assert pu.representation.TypesettingLibrary.is_unicode_subscriptable('aex123')
        assert not pu.representation.TypesettingLibrary.is_unicode_subscriptable('b')

    def test_convert_to_unicode_subscript(self):
        assert pu.representation.TypesettingLibrary.convert_to_unicode_subscript('123') == '₁₂₃'
        assert pu.representation.TypesettingLibrary.convert_to_unicode_subscript('aex') == 'ₐₑₓ'
        assert pu.representation.TypesettingLibrary.convert_to_unicode_subscript('aex123') == 'ₐₑₓ₁₂₃'
        assert pu.representation.TypesettingLibrary.convert_to_unicode_subscript('Hello World!') == 'Hₑₗₗₒ Wₒᵣₗd!'
