from unittest import TestCase
import punctilious as pu


class TestInferenceRules(TestCase):
    def test_inference_rules(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        dni = u.i.double_negation_introduction
        pass
