from unittest import TestCase
import punctilious as pu
import random_data


class TestInferenceRules(TestCase):
    def test_inference_rules(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        dni = u.inference_rules.double_negation_introduction
        pass
