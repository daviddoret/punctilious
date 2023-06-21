from unittest import TestCase
import punctilious as pu
import random_data


class TestAxiomInclusion(TestCase):
    def test_axiom_inclusion(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_axiom_declaration = True
        pu.configuration.echo_axiom_inclusion = True
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        ad1 = u.declare_axiom(content1)
        ad2 = u.declare_axiom(content2)
        t = u.t()
        ai1 = t.include_axiom(ad1)
        ai2 = t.include_axiom(ad2)