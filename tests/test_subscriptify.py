from unittest import TestCase
import punctilious as pu
import random_data


class TestSubscriptify(TestCase):
    def test_subscriptify(self):
        raw = 'ax(12345)'
        self.assertEqual(raw, pu.subscriptify(raw, pu.text_formats.plaintext))
        self.assertEqual('ₐₓ₍₁₂₃₄₅₎', pu.subscriptify(raw, pu.text_formats.unicode))
        self.assertEqual('_{ax(12345)}', pu.subscriptify(raw, pu.text_formats.latex_math))
