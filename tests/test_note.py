from unittest import TestCase
import punctilious as pu
import random_data


class TestNoteIntroduction(TestCase):
    def test_note_introduction(self):
        pu.configuration.echo_note = True
        pu.configuration.encoding = pu.encodings.unicode
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        r1 = u.r.declare(1, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom('The arbitrary axiom of testing.')
        ap = t.include_axiom(a)
        t.i.axiom_interpretation.infer_statement(ap, u.f(r1, o1))
        note = t.take_note('Hello world!', ref='1.1.1')
        self.assertEqual('𝗡𝗼𝘁𝗲 𝟭.𝟭.𝟭 (🗅₂): Hello world!', note.rep_report())
        comment = t.take_note('Foo', ref='1.1.2', cat=pu.title_categories.comment)
        self.assertEqual('𝗖𝗼𝗺𝗺𝗲𝗻𝘁 𝟭.𝟭.𝟮 (🗅₃): Foo', comment.rep_report())
        remark = t.take_note('Bar', ref='1.1.3', cat=pu.title_categories.remark)
        self.assertEqual('𝗥𝗲𝗺𝗮𝗿𝗸 𝟭.𝟭.𝟯 (🗅₄): Bar', remark.rep_report())
