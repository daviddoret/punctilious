from unittest import TestCase
import punctilious as pu
import random_data


class TestTitle(TestCase):
    def test_title(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext

        title1 = pu.TitleOBSOLETE('1.1.1')
        self.assertEqual('uncategorized 1.1.1', title1.rep_title())
        self.assertEqual('Uncategorized 1.1.1', title1.rep_title(cap=True))
        self.assertEqual('uncat. 1.1.1', title1.rep_ref())

        title2 = pu.TitleOBSOLETE('1.1.2', pu.title_categories.proposition)
        self.assertEqual('proposition 1.1.2', title2.rep_title())
        self.assertEqual('Proposition 1.1.2', title2.rep_title(cap=True))
        self.assertEqual('prop. 1.1.2', title2.rep_ref())
        self.assertEqual('𝗽𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟮', title2.rep_title(encoding=pu.encodings.unicode))
        self.assertEqual('𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟮',
                         title2.rep_title(encoding=pu.encodings.unicode, cap=True))
        self.assertEqual('𝗽𝗿𝗼𝗽. 𝟭.𝟭.𝟮', title2.rep_ref(encoding=pu.encodings.unicode))
        self.assertEqual('\\boldsymbol\\mathsf{proposition}} \\boldsymbol\\mathsf{1.1.2}}',
                         title2.rep_title(encoding=pu.encodings.latex))
        self.assertEqual('\\boldsymbol\\mathsf{Proposition}} \\boldsymbol\\mathsf{1.1.2}}',
                         title2.rep_title(encoding=pu.encodings.latex, cap=True))
        self.assertEqual('\\boldsymbol\\mathsf{prop.}} \\boldsymbol\\mathsf{1.1.2}}',
                         title2.rep_ref(encoding=pu.encodings.latex))

        complement3 = random_data.random_sentence()
        title3 = pu.TitleOBSOLETE(f'1.1.3', pu.title_categories.lemma, subtitle=complement3)
        self.assertEqual(f'lemma 1.1.3 - {complement3}', title3.rep_title())
        self.assertEqual(f'Lemma 1.1.3 - {complement3}', title3.rep_title(cap=True))
        self.assertEqual(f'lem. 1.1.3', title3.rep_ref())
        self.assertEqual(f'𝗹𝗲𝗺. 𝟭.𝟭.𝟯', title3.rep_ref(encoding=pu.encodings.unicode))
