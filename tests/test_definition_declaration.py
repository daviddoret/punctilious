from unittest import TestCase
import punctilious as p
import random_data


class TestDefinition(TestCase):
    def test_definition(self):
        echo_definition = p.configuration.echo_definition_declaration
        p.configuration.echo_definition_declaration = True
        u = p.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        content3 = random_data.random_sentence()
        content4 = random_data.random_sentence()
        content5 = random_data.random_sentence()
        d1 = u.declare_definition(content1)
        d2 = u.declare_definition(content2)
        d3 = u.declare_definition(content3, title=p.Title('1.1.1'))
        d4 = u.declare_definition(content4, title='1.1.2')
        d5 = u.declare_definition(content5, title='1.1.3', dashed_name='my-definition')
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 𝗱𝗲𝗰𝗹𝗮𝗿𝗮𝘁𝗶𝗼𝗻 (𝑜₁): “{content1}”', d1.rep_report(wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 𝗱𝗲𝗰𝗹𝗮𝗿𝗮𝘁𝗶𝗼𝗻 (𝑜₂): “{content2}”', d2.rep_report(wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 𝗱𝗲𝗰𝗹𝗮𝗿𝗮𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟭 (𝑜₃): “{content3}”',
                         d3.rep_report(wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 𝗱𝗲𝗰𝗹𝗮𝗿𝗮𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟮 (𝑜₄): “{content4}”',
                         d4.rep_report(wrap=False))
        self.assertEqual(f'𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻 𝗱𝗲𝗰𝗹𝗮𝗿𝗮𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟯 (𝑜₅): “{content5}”',
                         d5.rep_report(wrap=False))
        p.configuration.echo_definition_declaration = echo_definition
