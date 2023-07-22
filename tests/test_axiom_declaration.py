from unittest import TestCase
import punctilious as pu
import random_data


class TestAxiomDeclaration(TestCase):

    def test_title(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        a1 = u.declare_axiom(content1)
        self.assertEqual('Axiom (a1)', a1.rep_title(cap=True, encoding=pu.encodings.plaintext))
        self.assertEqual('axiom (a1)', a1.rep_title(cap=False, encoding=pu.encodings.plaintext))
        self.assertEqual('Axiom (𝑎₁)', a1.rep_title(cap=True, encoding=pu.encodings.unicode))
        self.assertEqual('axiom (𝑎₁)', a1.rep_title(cap=False, encoding=pu.encodings.unicode))

    def test_axiom_declaration(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        content3 = random_data.random_sentence()
        content4 = random_data.random_sentence()
        content5 = random_data.random_sentence()
        a1 = u.declare_axiom(content1)
        a2 = u.declare_axiom(content2, ref='1.1.1')
        a3 = u.declare_axiom(content3, symbol='b')
        a4 = u.declare_axiom(content4, symbol='c',
                             subtitle='the axiom of test')
        a5 = u.declare_axiom(content5, ref='1.1.2', symbol='d',
                             subtitle='the other axiom of test')
        self.assertEqual(f'Axiom (𝑎₁): ⌜{content1}⌝',
                         a1.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(f'Axiom 1.1.1 (𝑎₂): ⌜{content2}⌝',
                         a2.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(f'Axiom (𝑏₁): ⌜{content3}⌝',
                         a3.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(f'Axiom (𝑐₁) - the axiom of test: ⌜{content4}⌝',
                         a4.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(f'Axiom 1.1.2 (𝑑₁) - the other axiom of test: ⌜{content5}⌝',
                         a5.rep_report(encoding=pu.encodings.unicode, wrap=False))
