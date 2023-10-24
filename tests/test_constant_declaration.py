from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestConstantDeclaration(TestCase):

    def test_constant_declaration(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare()
        c1 = u.c.declare(value=o1)
        c1.re
        c2 = u.c.declare(value=o1 | r1 | o2)
        c3 = u.c.declare(value=o3, symbol='X',
            auto_index=False)  # self.assertEqual(  #    f'𝖫𝖾𝗍 ⌜𝑑₁⌝ 𝖻𝖾 𝗍𝗁𝖾 𝑑𝑒𝑓𝑖𝑛𝑖𝑡𝑖𝑜𝑛 ⌜𝒹𝒾𝓅𝒾𝓋𝒾 𝓈𝓉𝒾𝓂ℴ𝓋ℴ 𝒻𝓇𝒾𝒻𝓊𝒷𝓊 𝒹ℴ𝒷ℯ 𝒹𝓇𝓊𝓂𝓊𝒹ℴ𝒾𝓉𝓊.⌝ 𝗂𝗇 {u_unicode}, 𝗄𝗇𝗈𝗐𝗇 𝖺𝗌 𝗍𝗁𝖾 𝗈𝗍𝗁𝖾𝗋 𝖽𝖾𝖿𝗂𝗇𝗂𝗍𝗂𝗈𝗇 𝗈𝖿 𝗍𝖾𝗌𝗍, 𝗈𝗋 𝗌𝗂𝗆𝗉𝗅𝗒 𝗈𝖺𝗈𝗍.',  #    a5.rep_report(encoding=pu.encodings.unicode, wrap=False))
