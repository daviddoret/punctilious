from unittest import TestCase
import punctilious as pu
import random_data


class TestTitle(TestCase):
    def test_title(self):
        pu.configuration.echo_default = False
        pu.configuration.text_format = pu.text_formats.plaintext

        title1 = pu.Title('1.1.1')
        self.assertEqual('uncategorized 1.1.1', title1.repr_as_title())
        self.assertEqual('Uncategorized 1.1.1', title1.repr_as_title(cap=True))
        self.assertEqual('uncat. 1.1.1', title1.repr_as_ref())

        title2 = pu.Title('1.1.2', pu.title_categories.proposition)
        self.assertEqual('proposition 1.1.2', title2.repr_as_title())
        self.assertEqual('Proposition 1.1.2', title2.repr_as_title(cap=True))
        self.assertEqual('prop. 1.1.2', title2.repr_as_ref())
        self.assertEqual('𝗽𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟮', title2.repr_as_title(text_format=pu.text_formats.unicode))
        self.assertEqual('𝗣𝗿𝗼𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝟭.𝟭.𝟮', title2.repr_as_title(text_format=pu.text_formats.unicode, cap=True))
        self.assertEqual('𝗽𝗿𝗼𝗽. 𝟭.𝟭.𝟮', title2.repr_as_ref(text_format=pu.text_formats.unicode))
        self.assertEqual('\\boldsymbol\\mathsf{proposition 1.1.2}}',
                         title2.repr_as_title(text_format=pu.text_formats.latex_math))
        self.assertEqual('\\boldsymbol\\mathsf{Proposition 1.1.2}}',
                         title2.repr_as_title(text_format=pu.text_formats.latex_math, cap=True))
        self.assertEqual('\\boldsymbol\\mathsf{prop. 1.1.2}}',
                         title2.repr_as_ref(text_format=pu.text_formats.latex_math))

        complement3 = random_data.random_sentence()
        title3 = pu.Title(f'1.1.3', pu.title_categories.lemma, complement=complement3)
        self.assertEqual(f'lemma 1.1.3 - {complement3}', title3.repr_as_title())
        self.assertEqual(f'Lemma 1.1.3 - {complement3}', title3.repr_as_title(cap=True))
        self.assertEqual(f'lem. 1.1.3', title3.repr_as_ref())
        self.assertEqual(f'𝗹𝗲𝗺. 𝟭.𝟭.𝟯', title3.repr_as_ref(text_format=pu.text_formats.unicode))
        self.assertEqual(f'\\boldsymbol\\mathsf{{lemma 1.1.3 - {complement3}}}}}',
                         title3.repr_as_title(text_format=pu.text_formats.latex_math))
        self.assertEqual(f'\\boldsymbol\\mathsf{{Lemma 1.1.3 - {complement3}}}}}',
                         title3.repr_as_title(text_format=pu.text_formats.latex_math, cap=True))
        self.assertEqual(f'\\boldsymbol\\mathsf{{lem. 1.1.3}}}}',
                         title3.repr_as_ref(text_format=pu.text_formats.latex_math))
