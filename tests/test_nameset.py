from unittest import TestCase
import punctilious as pu
import random_data


class TestNameSet(TestCase):
    def test_nameset_1(self):
        n = pu.NameSet(symbol='x', index=1, acronym='xy', name='something',
                       explicit_name='something precise')

        pu.configuration.text_format = pu.text_formats.unicode
        self.assertEqual('𝑥₁', n.rep_compact())
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗉𝗋𝖾𝖼𝗂𝗌𝖾 𝟣', n.rep_accurate())
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝟣', n.rep_conventional())
        self.assertEqual('𝑥₁', n.rep_symbol())
        self.assertEqual('𝚡𝚢𝟣', n.rep_acronym())
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝟣', n.rep_name())
        self.assertEqual('𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗉𝗋𝖾𝖼𝗂𝗌𝖾 𝟣', n.rep_explicit_name())

        pu.configuration.text_format = pu.text_formats.latex_math
        self.assertEqual('\\mathit{x}_{1}', n.rep_compact())
        self.assertEqual('\\mathsf{something precise} \\mathsf{1}', n.rep_accurate())
        self.assertEqual('\\mathsf{something} \\mathsf{1}', n.rep_conventional())
        self.assertEqual('\\mathit{x}_{1}', n.rep_symbol())
        self.assertEqual('\\mathtt{xy}\\mathsf{1}', n.rep_acronym())
        self.assertEqual('\\mathsf{something} \\mathsf{1}', n.rep_name())
        self.assertEqual('\\mathsf{something precise} \\mathsf{1}', n.rep_explicit_name())

        pu.configuration.text_format = pu.text_formats.plaintext
        self.assertEqual('x1', n.rep_compact())
        self.assertEqual('something precise 1', n.rep_accurate())
        self.assertEqual('something 1', n.rep_conventional())
        self.assertEqual('x1', n.rep_symbol())
        self.assertEqual('xy1', n.rep_acronym())
        self.assertEqual('something 1', n.rep_name())
        self.assertEqual('something precise 1', n.rep_explicit_name())
