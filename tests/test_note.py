from unittest import TestCase
import punctilious as p
import random_data


class TestNoteIntroduction(TestCase):
    def test_note_introduction(self):
        echo_note = p.configuration.echo_note
        p.configuration.echo_note = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o2.declare()
        r1 = u.r.declare(1, signal_proposition=True)
        t = u.t(
            'testing-theory')
        a = u.axiom('The arbitrary axiom of testing.')
        ap = t.postulate_axiom(a)
        t.dai(u.f(r1, o1), ap=ap)
        note = t.take_note('Hello world!', reference='N1')
        self.assertEqual('𝐍𝐨𝐭𝐞 𝐍𝟏: Hello world!', note.repr_as_statement())
        comment = t.take_note('Foo', reference='N2', category=p.note_categories.comment)
        self.assertEqual('𝐂𝐨𝐦𝐦𝐞𝐧𝐭 𝐍𝟐: Foo', comment.repr_as_statement())
        remark = t.take_note('Bar', reference='N3', category=p.note_categories.remark)
        self.assertEqual('𝐑𝐞𝐦𝐚𝐫𝐤 𝐍𝟑: Bar', remark.repr_as_statement())
        p.configuration.echo_note = echo_note
