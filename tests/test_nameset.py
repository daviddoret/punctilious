from unittest import TestCase
import punctilious as pu
import random_data


class TestNameSet(TestCase):
    def test_nameset_1(self):
        pu.configuration.echo_default = False

        n = pu.NameSet(# symbolic names
            symbol='x', index=1, dashed_name='something-precise', # natural language names
            acronym='smthng', abridged_name='someth.', name='something',
            explicit_name='something precise', # section names
            paragraph_header=pu.paragraph_headers.note, ref='1.1.1', subtitle='about something')

        # Plaintext symbolic representations
        self.assertEqual('x1', n.rep_symbol(encoding=pu.encodings.plaintext))
        self.assertEqual('something-precise', n.rep_dashed_name(encoding=pu.encodings.plaintext))
        # Plaintext natural language representations
        self.assertEqual('smthng', n.rep_acronym(encoding=pu.encodings.plaintext))
        self.assertEqual('someth.', n.rep_abridged_name(encoding=pu.encodings.plaintext))
        self.assertEqual('something', n.rep_name(encoding=pu.encodings.plaintext))
        self.assertEqual('something precise', n.rep_explicit_name(encoding=pu.encodings.plaintext))
        # Plaintext prioritized name representations
        self.assertEqual('someth.', n.rep_compact_name(encoding=pu.encodings.plaintext))
        self.assertEqual('something precise', n.rep_accurate_name(encoding=pu.encodings.plaintext))
        self.assertEqual('something', n.rep_conventional_name(encoding=pu.encodings.plaintext))
        # Plaintext section title
        self.assertEqual('note 1.1.1 (x1) - about something',
            n.rep_title(encoding=pu.encodings.plaintext))

        # Unicode symbolic representations
        self.assertEqual('𝑥₁', n.rep_symbol(encoding=pu.encodings.unicode))
        self.assertEqual('𝑠𝑜𝑚𝑒𝑡ℎ𝑖𝑛𝑔-𝑝𝑟𝑒𝑐𝑖𝑠𝑒', n.rep_dashed_name(encoding=pu.encodings.unicode))
        # Unicode natural language representations
        self.assertEqual('𝗌𝗆𝗍𝗁𝗇𝗀', n.rep_acronym(encoding=pu.encodings.unicode))
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁.', n.rep_abridged_name(encoding=pu.encodings.unicode))
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀', n.rep_name(encoding=pu.encodings.unicode))
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗉𝗋𝖾𝖼𝗂𝗌𝖾', n.rep_explicit_name(encoding=pu.encodings.unicode))
        # Unicode prioritized name representations
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁.', n.rep_compact_name(encoding=pu.encodings.unicode))
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗉𝗋𝖾𝖼𝗂𝗌𝖾', n.rep_accurate_name(encoding=pu.encodings.unicode))
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀', n.rep_conventional_name(encoding=pu.encodings.unicode))
        # Unicode section title
        self.assertEqual('𝗻𝗼𝘁𝗲 𝟭.𝟭.𝟭 (𝑥₁) - about something',
            n.rep_title(encoding=pu.encodings.unicode))

        # LaTeX math basic representations
        self.assertEqual('\\mathit{x}_{1}', n.rep_symbol(encoding=pu.encodings.latex))
        self.assertEqual('\\mathit{something-precise}',
            n.rep_dashed_name(encoding=pu.encodings.latex))
        # LaTeX math natural language representations
        self.assertEqual('\\mathsf{smthng}', n.rep_acronym(encoding=pu.encodings.latex))
        self.assertEqual('\\mathsf{someth.}', n.rep_abridged_name(encoding=pu.encodings.latex))
        self.assertEqual('\\mathsf{something}', n.rep_name(encoding=pu.encodings.latex))
        self.assertEqual('\\mathsf{something precise}',
            n.rep_explicit_name(encoding=pu.encodings.latex))
        # LaTeX math prioritized name representations
        self.assertEqual('\\mathsf{someth.}', n.rep_compact_name(encoding=pu.encodings.latex))
        self.assertEqual('\\mathsf{something precise}',
            n.rep_accurate_name(encoding=pu.encodings.latex))
        self.assertEqual('\\mathsf{something}',
            n.rep_conventional_name(encoding=pu.encodings.latex))

    def test_nameset_title(self):
        n1 = pu.NameSet(symbol='x', index=1, paragraph_header=pu.paragraph_headers.hypothesis)
        s1 = n1.rep_title(encoding=pu.encodings.plaintext)
        print(s1)
