from unittest import TestCase
import punctilious as pu
import random_data


class TestAxiomDeclaration(TestCase):
    def test_axiom_declaration(self):
        pu.configuration.echo_default = False
        pu.configuration.text_format = pu.text_formats.plaintext
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        content3 = random_data.random_sentence()
        content4 = random_data.random_sentence()
        content5 = random_data.random_sentence()
        a1 = u.declare_axiom(content1)
        a2 = u.declare_axiom(content2)
        a3 = u.declare_axiom(content3, title=pu.Title('1.1.1'))
        a4 = u.declare_axiom(content4, title='1.1.2')
        a5 = u.declare_axiom(content5, '1.1.3')
        self.assertEqual(f'Axiom declaration (o1): “{content1}”.', a1.rep_report(wrap=False))
        self.assertEqual(f'Axiom declaration (o2): “{content2}”.', a2.rep_report(wrap=False))
        self.assertEqual(f'Axiom declaration 1.1.1 (o3): “{content3}”.', a3.rep_report(wrap=False))
        self.assertEqual(f'Axiom declaration 1.1.2 (o4): “{content4}”.', a4.rep_report(wrap=False))
        self.assertEqual(f'Axiom declaration 1.1.3 (o5): “{content5}”.', a5.rep_report(wrap=False))
