import pytest
import punctilious as pu


class TestRepresentation:
    def test_representation(self):
        p = pu.declare_variable(rep=pu.latin_alphabet_uppercase_serif_italic.p)
        q = pu.declare_variable(rep=pu.latin_alphabet_uppercase_serif_italic.q)
        phi = pu.Formula(pu.operators_1.conjunction, (p, q,))
        print(phi)
