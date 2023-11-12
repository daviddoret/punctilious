from unittest import TestCase
import punctilious as pu


class TestNoteIntroduction(TestCase):
    def test_note_introduction(self):
        pu.configuration.echo_note = True
        pu.configuration.encoding = pu.encodings.unicode
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        r1 = u.c1.declare(1, signal_proposition=True)
        t = u.declare_theory()
        a = u.declare_axiom('The arbitrary axiom of testing.')
        ap = t.include_axiom(a)
        t.i.axiom_interpretation.infer_formula_statement(ap, u.declare_compound_formula(r1, o1))
        note = t.take_note('Hello world!', ref='1.1.1')
        self.assertEqual('𝗡𝗼𝘁𝗲 𝟭.𝟭.𝟭 (🗅₁): 𝖧𝖾𝗅𝗅𝗈 𝗐𝗈𝗋𝗅𝖽!', note.rep_report())
        comment = t.take_note('Foo', ref='1.1.2', paragraph_header=pu.paragraph_headers.comment)
        self.assertEqual('𝗖𝗼𝗺𝗺𝗲𝗻𝘁 𝟭.𝟭.𝟮 (🗅₂): 𝖥𝗈𝗈', comment.rep_report())
        remark = t.take_note('Bar', paragraph_header=pu.paragraph_headers.remark)
        self.assertEqual('𝗥𝗲𝗺𝗮𝗿𝗸 (🗅₃): 𝖡𝖺𝗋', remark.rep_report())
