from unittest import TestCase
import punctilious as pu
import random_data


class TestNameSet(TestCase):
    def test_nameset_1(self):
        n = pu.NameSet(symbol='x', index=1, acronym='xy', name='something',
                       explicit_name='something precise')
        self.assertEqual('x', n.rep_compact())
        self.assertEqual('something precise', n.rep_accurate())
        self.assertEqual('something', n.rep_conventional())

    def test_nameset_2(self):
        n = pu.NameSet(symbol='⩒', index=1, name='dot big vee')
        self.assertEqual('⩒', n.rep_compact())
        self.assertEqual('dot big vee', n.rep_accurate())
        self.assertEqual('dot big vee', n.rep_conventional())
        self.assertEqual('dot big vee', n.rep_compact(text_format=pu.text_formats.plaintext))
        self.assertEqual('⩒', n.rep_compact(text_format=pu.text_formats.unicode))

    def test_nameset_3(self):
        pu.configuration.echo_default = False
        pu.configuration.text_format = pu.text_formats.unicode
        n = pu.NameSet(symbol=pu.StyledText('x', text_style=pu.text_styles.serif_bold), index=1,
                       acronym='xy',
                       name=pu.StyledText('something', text_style=pu.text_styles.monospace),
                       explicit_name='something precise')
        self.assertEqual('𝐱', n.rep_compact())
        self.assertEqual('something precise', n.rep_accurate())
        self.assertEqual('𝚜𝚘𝚖𝚎𝚝𝚑𝚒𝚗𝚐', n.rep_conventional())
        self.assertEqual('x', n.rep_compact(text_format=pu.text_formats.plaintext))
        self.assertEqual('something precise', n.rep_accurate(text_format=pu.text_formats.plaintext))
        self.assertEqual('something', n.rep_conventional(text_format=pu.text_formats.plaintext))
        self.assertEqual('𝐱', n.rep_compact(text_format=pu.text_formats.unicode))
        self.assertEqual('something precise', n.rep_accurate(text_format=pu.text_formats.unicode))
        self.assertEqual('𝚜𝚘𝚖𝚎𝚝𝚑𝚒𝚗𝚐', n.rep_conventional(text_format=pu.text_formats.unicode))
        self.assertEqual('\\mathbf{x}', n.rep_compact(text_format=pu.text_formats.latex_math))
        self.assertEqual('\\mathnormal{something precise}',
                         n.rep_accurate(text_format=pu.text_formats.latex_math))
        self.assertEqual('\\mathtt{something}',
                         n.rep_conventional(text_format=pu.text_formats.latex_math))
