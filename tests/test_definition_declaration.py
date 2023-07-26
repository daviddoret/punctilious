from unittest import TestCase
import punctilious as pu
import random_data


class TestDefinitionDeclaration(TestCase):

    def test_title(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        a1 = u.declare_definition(content1)
        self.assertEqual('Definition (d1)', a1.rep_title(cap=True, encoding=pu.encodings.plaintext))
        self.assertEqual('definition (d1)',
                         a1.rep_title(cap=False, encoding=pu.encodings.plaintext))
        self.assertEqual('𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 (𝑑₁)', a1.rep_title(cap=True, encoding=pu.encodings.unicode))
        self.assertEqual('𝗱𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 (𝑑₁)', a1.rep_title(cap=False, encoding=pu.encodings.unicode))

    def test_definition_declaration(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        content3 = random_data.random_sentence()
        content4 = random_data.random_sentence()
        content5 = random_data.random_sentence()
        a1 = u.declare_definition(content1)
        a2 = u.declare_definition(content2, ref='1.1.1')
        a3 = u.declare_definition(content3, symbol='b')
        a4 = u.declare_definition(content4, symbol='c',
                                  subtitle='the definition of test')
        a5 = u.declare_definition(content5, ref='1.1.2', symbol='d',
                                  subtitle='the other definition of test')
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 (𝑑₁): ⌜{content1}⌝',
                         a1.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟭 (𝑑₂): ⌜{content2}⌝',
                         a2.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 (𝑏₁): ⌜{content3}⌝',
                         a3.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 (𝑐₁) - the definition of test: ⌜{content4}⌝',
                         a4.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟮 (𝑑₁) - the other definition of test: ⌜{content5}⌝',
                         a5.rep_report(encoding=pu.encodings.unicode, wrap=False))
