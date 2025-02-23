import pytest
import punctilious_20250223 as pu
import uuid
from test_shared_library import create_atomic_connector, create_function


class TestVariable:
    def test_declare_variable(self):
        """Test of representation with multiple string-constant renderers.
        """

        x = pu.declare_variable(pu.latin_alphabet_lowercase_serif_italic.x)
        y = pu.declare_variable(pu.latin_alphabet_lowercase_serif_italic.y)
        x2 = pu.declare_variable(pu.latin_alphabet_lowercase_serif_italic.x)
        assert x != y
        assert x != x2
        pass
