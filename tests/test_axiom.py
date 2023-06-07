from unittest import TestCase
import punctilious as p
import random_data


class TestAxiom(TestCase):
    def test_axiom(self):
        echo_axiom = p.configuration.echo_axiom
        p.configuration.echo_axiom = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        a1 = u.axiom('Some axiom content.')
        a2 = u.axiom('Another axiom content.')
        print(a1.repr_as_statement())
        print(a2.repr_as_statement())
        self.assertEqual('Let 𝑎₁ be the axiom: “Some axiom content.”', a1.repr_as_statement())
        self.assertEqual('Let 𝑎₂ be the axiom: “Another axiom content.”', a2.repr_as_statement())
        p.configuration.echo_note = echo_axiom
