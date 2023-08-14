from unittest import TestCase
import punctilious as pu
import random_data


class TestAxiomDeclaration(TestCase):

    def test_title(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        a1 = u.declare_axiom(content1)
        self.assertEqual('Axiom (A1)', a1.rep_title(cap=True, encoding=pu.encodings.plaintext))
        self.assertEqual('axiom (A1)', a1.rep_title(cap=False, encoding=pu.encodings.plaintext))
        self.assertEqual('𝗔𝘅𝗶𝗼𝗺 (𝑎₁)', a1.rep_title(cap=True, encoding=pu.encodings.unicode))
        self.assertEqual('𝗮𝘅𝗶𝗼𝗺 (𝑎₁)', a1.rep_title(cap=False, encoding=pu.encodings.unicode))

    def test_axiom_declaration(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        content1 = '𝒷ℴℴ𝓇ℴ𝒶 𝒷ℯℯ𝒹𝓊 𝓇𝒾ℴ𝒷𝓁ℴ 𝒷𝓎𝓊𝒹𝒾ℯ𝓀𝓊.'  # random_data.random_sentence()
        content2 = '𝓇ℯ𝒹𝓊 𝒹ℴ𝒷ℴℯ 𝒹𝒾𝓃𝓊 𝒷𝒶𝒹𝓇𝓎𝓊 𝒽𝓎𝓋𝒾𝓋ℴ𝒾 𝒷ℯ𝒷𝒾 𝓏𝓎𝒶ℊ𝓃𝓊 𝒹𝓎𝒶𝓀ℯ 𝓈𝒾𝓏ℴℴ 𝒷𝒶𝓁ℴ 𝓅ℴ𝒶𝒹ℴℯ 𝒷𝒾𝓃ℴ𝒷𝓇𝓊 𝒻𝓁ℴ𝒹𝒾ℴ 𝓁𝒾𝒽𝒶 𝓇𝓎ℯ𝓅ℯ 𝓅ℴ𝒾𝓈𝓉𝒾𝒻𝓁𝓎ℴ 𝓉ℯ𝒷𝓁ℴℯ 𝒹ℴ𝒷𝓇ℯ 𝒿ℴℯ𝒷𝒾 𝒷𝒶𝒿𝓎𝓊 𝓈𝓉𝒶𝒷𝓎𝒶𝓁𝒶 ℊ𝓃𝒶𝒷𝓇𝒾 𝓂ℴ𝒶𝒻ℴ𝓊 𝒹ℴ𝓊𝓉𝓊 𝓈𝓊𝒹𝒾 ℊ𝓃ℴ𝒷𝓊 𝓂𝓊𝒹ℯ𝒷𝒾 𝒷ℯ𝒹ℴ𝒷ℯ 𝒻𝓁𝒾ℴ𝒷𝒾 𝒹𝒶𝓏𝒶ℯ.'  # random_data.random_sentence(min_words=30)
        content3 = '𝒷𝓇𝓎ℯ𝒷𝓇𝒾 𝒷𝓎𝒶𝒷𝓇𝓎ℴ𝒷ℴ𝓊 𝒷𝓊𝒷𝒾.'  # random_data.random_sentence()
        content4 = '𝒷𝓁ℴ𝓁ℯ 𝒷𝓁ℴ𝒿ℯ 𝒽𝓎𝓊ℊ𝓃ℯℯ.'  # random_data.random_sentence()
        content5 = '𝒹𝒾𝓅𝒾𝓋𝒾 𝓈𝓉𝒾𝓂ℴ𝓋ℴ 𝒻𝓇𝒾𝒻𝓊𝒷𝓊 𝒹ℴ𝒷ℯ 𝒹𝓇𝓊𝓂𝓊𝒹ℴ𝒾𝓉𝓊.'  # random_data.random_sentence()
        a1 = u.declare_axiom(content1)
        a2 = u.declare_axiom(content2)
        a3 = u.declare_axiom(content3, symbol='B')
        a4 = u.declare_axiom(content4, symbol='C', name='the axiom of test')
        a5 = u.declare_axiom(content5, acronym='oaot', symbol='d', name='the other axiom of test')
        self.assertEqual(
            f'𝖫𝖾𝗍 ⌜𝒜₁⌝ 𝖻𝖾 𝗍𝗁𝖾 𝑎𝑥𝑖𝑜𝑚 ⌜𝒷ℴℴ𝓇ℴ𝒶 𝒷ℯℯ𝒹𝓊 𝓇𝒾ℴ𝒷𝓁ℴ 𝒷𝓎𝓊𝒹𝒾ℯ𝓀𝓊.⌝ 𝗂𝗇 𝒰₁.',
            a1.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(
            f'𝖫𝖾𝗍 ⌜𝒜₂⌝ 𝖻𝖾 𝗍𝗁𝖾 𝑎𝑥𝑖𝑜𝑚 ⌜𝓇ℯ𝒹𝓊 𝒹ℴ𝒷ℴℯ 𝒹𝒾𝓃𝓊 𝒷𝒶𝒹𝓇𝓎𝓊 𝒽𝓎𝓋𝒾𝓋ℴ𝒾 𝒷ℯ𝒷𝒾 𝓏𝓎𝒶ℊ𝓃𝓊 𝒹𝓎𝒶𝓀ℯ 𝓈𝒾𝓏ℴℴ 𝒷𝒶𝓁ℴ 𝓅ℴ𝒶𝒹ℴℯ 𝒷𝒾𝓃ℴ𝒷𝓇𝓊 𝒻𝓁ℴ𝒹𝒾ℴ 𝓁𝒾𝒽𝒶 𝓇𝓎ℯ𝓅ℯ 𝓅ℴ𝒾𝓈𝓉𝒾𝒻𝓁𝓎ℴ 𝓉ℯ𝒷𝓁ℴℯ 𝒹ℴ𝒷𝓇ℯ 𝒿ℴℯ𝒷𝒾 𝒷𝒶𝒿𝓎𝓊 𝓈𝓉𝒶𝒷𝓎𝒶𝓁𝒶 ℊ𝓃𝒶𝒷𝓇𝒾 𝓂ℴ𝒶𝒻ℴ𝓊 𝒹ℴ𝓊𝓉𝓊 𝓈𝓊𝒹𝒾 ℊ𝓃ℴ𝒷𝓊 𝓂𝓊𝒹ℯ𝒷𝒾 𝒷ℯ𝒹ℴ𝒷ℯ 𝒻𝓁𝒾ℴ𝒷𝒾 𝒹𝒶𝓏𝒶ℯ.⌝ 𝗂𝗇 𝒰₁.',
            a2.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(
            f'𝖫𝖾𝗍 ⌜𝐵₁⌝ 𝖻𝖾 𝗍𝗁𝖾 𝑎𝑥𝑖𝑜𝑚 ⌜𝒷𝓇𝓎ℯ𝒷𝓇𝒾 𝒷𝓎𝒶𝒷𝓇𝓎ℴ𝒷ℴ𝓊 𝒷𝓊𝒷𝒾.⌝ 𝗂𝗇 𝒰₁.',
            a3.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(
            f'𝖫𝖾𝗍 ⌜𝐶₁⌝ 𝖻𝖾 𝗍𝗁𝖾 𝑎𝑥𝑖𝑜𝑚 ⌜𝒷𝓁ℴ𝓁ℯ 𝒷𝓁ℴ𝒿ℯ 𝒽𝓎𝓊ℊ𝓃ℯℯ.⌝ 𝗂𝗇 𝒰₁, 𝗄𝗇𝗈𝗐𝗇 𝖺𝗌 𝗍𝗁𝖾 𝖺𝗑𝗂𝗈𝗆 𝗈𝖿 𝗍𝖾𝗌𝗍.',
            a4.rep_report(encoding=pu.encodings.unicode, wrap=False))
        self.assertEqual(
            f'𝖫𝖾𝗍 ⌜𝑑₁⌝ 𝖻𝖾 𝗍𝗁𝖾 𝑎𝑥𝑖𝑜𝑚 ⌜𝒹𝒾𝓅𝒾𝓋𝒾 𝓈𝓉𝒾𝓂ℴ𝓋ℴ 𝒻𝓇𝒾𝒻𝓊𝒷𝓊 𝒹ℴ𝒷ℯ 𝒹𝓇𝓊𝓂𝓊𝒹ℴ𝒾𝓉𝓊.⌝ 𝗂𝗇 𝒰₁, 𝗄𝗇𝗈𝗐𝗇 𝖺𝗌 𝗍𝗁𝖾 𝗈𝗍𝗁𝖾𝗋 𝖺𝗑𝗂𝗈𝗆 𝗈𝖿 𝗍𝖾𝗌𝗍, 𝗈𝗋 𝗌𝗂𝗆𝗉𝗅𝗒 𝗈𝖺𝗈𝗍.',
            a5.rep_report(encoding=pu.encodings.unicode, wrap=False))
