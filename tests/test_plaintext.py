from unittest import TestCase
import plaintext as ma
import random_data as rd


class TestPlaintext(TestCase):
    def test_plaintext(self):
        self.assertEqual(rd.pangram1, ma.Plaintext(rd.pangram1))
        self.assertEqual('', ma.Plaintext(''))
        self.assertIsNone(ma.Plaintext(None))
        self.assertIsNone(ma.Plaintext(None, empty_if_none=False))
        self.assertEqual('', ma.Plaintext(None, empty_if_none=True))
        self.assertEqual('abcdefghijklmnopqrstuvwxyz',
                         ma.Plaintext('𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧'))
