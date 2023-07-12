from unittest import TestCase
import punctilious as pu
import random_data


class TestSimpleObjct(TestCase):
    def test_simple_objct(self):
        pu.configuration.echo_free_variable_declaration = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        self.assertEqual('o1', o1.rep(pu.encodings.plaintext))
        o2 = u.o.declare()
        self.assertEqual('o2', o2.rep(pu.encodings.plaintext))
        o3 = u.o.declare()
        self.assertEqual('o3', o3.rep(pu.encodings.plaintext))
        o4 = u.o.declare()
        self.assertEqual('o4', o4.rep(pu.encodings.plaintext))
        a1 = u.o.declare('a')
        self.assertEqual('a1', a1.rep(pu.encodings.plaintext))
        a2 = u.o.declare('a')
        self.assertEqual('a2', a2.rep(pu.encodings.plaintext))
