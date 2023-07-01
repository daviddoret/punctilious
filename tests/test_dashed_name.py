from unittest import TestCase
import punctilious as p
import random_data


class TestDashedName(TestCase):
    def test_dashed_name(self):
        raw = random_data.random_dashed_name()
        dashed_name = p.DashedName(raw)
        self.assertEqual(raw, str(dashed_name))
        self.assertEqual(raw, dashed_name.rep())
        self.assertEqual(raw, dashed_name.rep_dashed_name())
