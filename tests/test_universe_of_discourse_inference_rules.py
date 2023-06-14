from unittest import TestCase
import punctilious as p
import random_data


class TestInferenceRules(TestCase):
    def test_inference_rules(self):
        p.configuration.echo_default = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        dni = u.inference_rules.double_negation_introduction
        pass
