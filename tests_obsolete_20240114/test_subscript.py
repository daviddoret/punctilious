from unittest import TestCase
import punctilious as pu


class TestSubscriptNormal(TestCase):
    def test_subscript_normal(self):
        compo = pu.Subscript(plaintext='hello world 0123456789')

        self.assertEqual('hello world 0123456789', compo.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('ₕₑₗₗₒ wₒᵣₗd ₀₁₂₃₄₅₆₇₈₉', compo.rep(encoding=pu.encodings.unicode_extended))
        self.assertEqual('_{hello world 0123456789}', compo.rep(encoding=pu.encodings.latex))