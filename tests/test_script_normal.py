from unittest import TestCase
import punctilious as pu
import random_data


class TestScriptNormal(TestCase):
    def test_script_normal(self):
        compo = pu.ScriptNormal(plaintext=random_data.pangram1)

        self.assertEqual('the quick brown fox jumps over the lazy dog. 0123456789!',
                         compo.rep(encoding=pu.encodings.plaintext, cap=False))
        self.assertEqual('The quick brown fox jumps over the lazy dog. 0123456789!',
                         compo.rep(encoding=pu.encodings.plaintext, cap=True))
        self.assertEqual(
            '𝓉𝒽ℯ 𝓆𝓊𝒾𝒸𝓀 𝒷𝓇ℴ𝓌𝓃 𝒻ℴ𝓍 𝒿𝓊𝓂𝓅𝓈 ℴ𝓋ℯ𝓇 𝓉𝒽ℯ 𝓁𝒶𝓏𝓎 𝒹ℴℊ. 𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫!',
            compo.rep(encoding=pu.encodings.unicode))
        self.assertEqual('\\mathcal{the quick brown fox jumps over the lazy dog. 0123456789!}',
                         compo.rep(encoding=pu.encodings.latex_math))
