import pytest

import punctilious as pu


class TestSymbols:
    def test_to_string(self):
        a = pu.ts.symbols.open_parenthesis.to_string()
        pu.log.debug(msg=a)
