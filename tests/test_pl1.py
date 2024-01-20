import pytest
from punctilious import formal_language as fl
import formal_language_en_us
from punctilious import pl1 as pl1
import pl1_en_us
import pl1_fr_ch


class TestPL1:
    def test_connectives(self):
        l: pl1.PL1 = pl1.PL1()
        assert str(l.connectives.negation) == "lnot"
