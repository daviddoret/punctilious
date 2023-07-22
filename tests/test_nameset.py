from unittest import TestCase
import punctilious as pu
import random_data


class TestNameSet(TestCase):
    def test_nameset_1(self):
        n = pu.NameSet(symbol='x', index=1, dashed_name='something-precise', acronym='smthng',
                       abridged_name='someth.', name='something', explicit_name='something precise',
                       ref='1.1.1', subtitle='my subtitle')

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

        # LaTeX math basic representations
        self.assertEqual('\\mathit{x}_{1}', n.rep_symbol(encoding=pu.encodings.latex_math))
        self.assertEqual('\\mathit{something-precise}',
                         n.rep_dashed_name(encoding=pu.encodings.latex_math))
        # LaTeX math natural language representations
        self.assertEqual('\\mathsf{smthng}', n.rep_acronym(encoding=pu.encodings.latex_math))
        self.assertEqual('\\mathsf{someth.}', n.rep_abridged_name(encoding=pu.encodings.latex_math))
        self.assertEqual('\\mathsf{something}', n.rep_name(encoding=pu.encodings.latex_math))
        self.assertEqual('\\mathsf{something precise}',
                         n.rep_explicit_name(encoding=pu.encodings.latex_math))
        # LaTeX math prioritized name representations
        self.assertEqual('\\mathsf{someth.}', n.rep_compact_name(encoding=pu.encodings.latex_math))
        self.assertEqual('\\mathsf{something precise}',
                         n.rep_accurate_name(encoding=pu.encodings.latex_math))
        self.assertEqual('\\mathsf{something}',
                         n.rep_conventional_name(encoding=pu.encodings.latex_math))

        # Unicode symbolic representations
        self.assertEqual('x1', n.rep_symbol(encoding=pu.encodings.plaintext))
        self.assertEqual('something-precise', n.rep_dashed_name(encoding=pu.encodings.plaintext))
        # Unicode natural language representations
        self.assertEqual('smthng', n.rep_acronym(encoding=pu.encodings.plaintext))
        self.assertEqual('someth.', n.rep_abridged_name(encoding=pu.encodings.plaintext))
        self.assertEqual('something', n.rep_name(encoding=pu.encodings.plaintext))
        self.assertEqual('something precise', n.rep_explicit_name(encoding=pu.encodings.plaintext))
        # Unicode prioritized name representations
        self.assertEqual('someth.', n.rep_compact_name(encoding=pu.encodings.plaintext))
        self.assertEqual('something precise', n.rep_accurate_name(encoding=pu.encodings.plaintext))
        self.assertEqual('something', n.rep_conventional_name(encoding=pu.encodings.plaintext))

    def test_nameset_title(self):
        n1 = pu.NameSet(symbol='x', index=1, cat=pu.title_categories.proposition)
        s1 = n1.rep_title(encoding=pu.encodings.plaintext)
        print(s1)
