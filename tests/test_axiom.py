from unittest import TestCase
import punctilious as p
import random_data


class TestAxiom(TestCase):
    def test_axiom(self):
        echo_axiom = p.configuration.echo_axiom
        p.configuration.echo_axiom = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        content3 = random_data.random_sentence()
        content4 = random_data.random_sentence()
        content5 = random_data.random_sentence()
        a1 = u.axiom(content1)
        a2 = u.axiom(content2)
        a3 = u.axiom(content3, header=p.ObjctHeader('1.1.1'))
        a4 = u.axiom(content4, header='1.1.2')
        a5 = u.axiom(content5, '1.1.3')
        self.assertEqual(f'𝐚₁: “{content1}”', a1.repr_as_statement(wrap=False))
        self.assertEqual(f'𝐚₂: “{content2}”', a2.repr_as_statement(wrap=False))
        self.assertEqual(f'𝐀𝐱𝐢𝐨𝐦 𝟏.𝟏.𝟏 (a₃): “{content3}”', a3.repr_as_statement(wrap=False))
        self.assertEqual(f'𝐀𝐱𝐢𝐨𝐦 𝟏.𝟏.𝟐 (a₄): “{content4}”', a4.repr_as_statement(wrap=False))
        self.assertEqual(f'𝐀𝐱𝐢𝐨𝐦 𝟏.𝟏.𝟑 (a₅): “{content5}”', a5.repr_as_statement(wrap=False))
        p.configuration.echo_axiom = echo_axiom
