from unittest import TestCase
import punctilious as pu
import random_data


class TestRelationDict(TestCase):
    def test_relation_dict(self):
        pu.configuration.echo_default = False
        pu.configuration.text_format = pu.text_formats.plaintext
        u = pu.UniverseOfDiscourse()
        self.assertEqual('==>', u.r.implication.rep())
        self.assertEqual('and', u.r.conjunction.rep())
