from unittest import TestCase
import punctilious as pu
import random_data


class TestDefinition(TestCase):
    def test_definition(self):
        pu.configuration.echo_definition_declaration = False
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        content3 = random_data.random_sentence()
        content4 = random_data.random_sentence()
        content5 = random_data.random_sentence()
        d1 = u.declare_definition(content1)
        d2 = u.declare_definition(content2)
        d3 = u.declare_definition(content3, title=pu.TitleOBSOLETE('1.1.1'))
        d4 = u.declare_definition(content4, title='1.1.2')
        d5 = u.declare_definition(content5, title='1.1.3', dashed_name='my-definition')

        self.assertEqual(f'Definition (o1): {content1}',
                         d1.rep_report(text_format=pu.encodings.plaintext, wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 (𝑜₁): {content1}',
                         d1.rep_report(text_format=pu.encodings.unicode, wrap=False))

        self.assertEqual(f'Definition (o2): {content2}',
                         d2.rep_report(text_format=pu.encodings.plaintext, wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 (𝑜₂): {content2}',
                         d2.rep_report(text_format=pu.encodings.unicode, wrap=False))

        self.assertEqual(f'Definition 1.1.1 (o3): {content3}',
                         d3.rep_report(text_format=pu.encodings.plaintext, wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟭 (𝑜₃): {content3}',
                         d3.rep_report(text_format=pu.encodings.unicode, wrap=False))

        self.assertEqual(f'Definition 1.1.2 (o4): {content4}',
                         d4.rep_report(text_format=pu.encodings.plaintext, wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟮 (𝑜₄): {content4}',
                         d4.rep_report(text_format=pu.encodings.unicode, wrap=False))

        self.assertEqual(f'Definition 1.1.3 (o5): {content5}',
                         d5.rep_report(text_format=pu.encodings.plaintext, wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟯 (𝑜₅): {content5}',
                         d5.rep_report(text_format=pu.encodings.unicode, wrap=False))
