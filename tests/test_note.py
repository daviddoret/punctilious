from unittest import TestCase
import punctilious as p
import random_data


class TestNoteIntroduction(TestCase):
    def test_note_introduction(self):
        echo_note = p.configuration.echo_note
        p.configuration.echo_note = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o()
        r1 = u.r(1, signal_proposition=True)
        t = u.t(
            'testing-theory')
        a = t.a('The arbitrary axiom of testing.')
        t.dai(u.f(r1, o1), a=a)
        note = t.take_note('Hello world!')
        self.assertEqual('𝐍𝐨𝐭𝐞 𝟎: “Hello world!”', note.repr())
        p.configuration.echo_note = echo_note
