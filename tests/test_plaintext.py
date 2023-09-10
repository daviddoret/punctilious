from unittest import TestCase
import punctilious as pu
import punctilious.random_data as rd


class TestPlaintext(TestCase):
    def test_plaintext(self):
        self.assertEqual(rd.pangram1, pu.Plaintext(rd.pangram1))
        self.assertEqual('', pu.Plaintext(''))
        self.assertIsNone(pu.Plaintext(None))
        self.assertIsNone(pu.Plaintext(None, empty_if_none=False))
        self.assertEqual('', pu.Plaintext(None, empty_if_none=True))
        self.assertEqual('abcdefghijklmnopqrstuvwxyz',
                         pu.Plaintext('𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧'))
