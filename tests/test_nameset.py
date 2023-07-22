from unittest import TestCase
import punctilious as pu
import random_data


class TestNameSet(TestCase):
    def test_nameset_1(self):
        n = pu.NameSet(symbol='x', index=1, acronym='xy', name='something',
                       explicit_name='something precise', ref='1.1.1', subtitle='my subtitle')

        # Basic representations
        self.assertEqual('𝑥₁', n.rep_symbol(encoding=pu.encodings.unicode))
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀', n.rep_name(encoding=pu.encodings.unicode))
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗉𝗋𝖾𝖼𝗂𝗌𝖾', n.rep_explicit_name(encoding=pu.encodings.unicode))
        # Prioritized representations
        self.assertEqual('𝑥₁', n.rep_compact_name(encoding=pu.encodings.unicode))
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗉𝗋𝖾𝖼𝗂𝗌𝖾', n.rep_accurate_name(encoding=pu.encodings.unicode))
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝟣', n.rep_conventional_name(encoding=pu.encodings.unicode))
        self.assertEqual('𝚡𝚢𝟣', n.rep_acronym(encoding=pu.encodings.unicode))

        pu.configuration.encoding = pu.encodings.latex_math
        self.assertEqual('\\mathit{x}_{1}', n.rep_compact_name())
        self.assertEqual('\\mathsf{something precise} \\mathsf{1}', n.rep_accurate_name())
        self.assertEqual('\\mathsf{something} \\mathsf{1}', n.rep_conventional_name())
        self.assertEqual('\\mathit{x}_{1}', n.rep_symbol())
        self.assertEqual('\\mathtt{xy}\\mathsf{1}', n.rep_acronym())
        self.assertEqual('\\mathsf{something} \\mathsf{1}', n.rep_name())
        self.assertEqual('\\mathsf{something precise} \\mathsf{1}', n.rep_explicit_name())

        pu.configuration.encoding = pu.encodings.plaintext
        self.assertEqual('x1', n.rep_compact_name())
        self.assertEqual('something precise 1', n.rep_accurate_name())
        self.assertEqual('something 1', n.rep_conventional_name())
        self.assertEqual('x1', n.rep_symbol())
        self.assertEqual('xy1', n.rep_acronym())
        self.assertEqual('something 1', n.rep_name())
        self.assertEqual('something precise 1', n.rep_explicit_name())

    def test_nameset_title(self):
        n1 = pu.NameSet(symbol='x', index=1, cat=pu.title_categories.proposition)
        s1 = n1.rep_title(encoding=pu.encodings.plaintext)
        print(s1)
