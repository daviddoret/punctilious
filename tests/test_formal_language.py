import pytest
import punctilious as pu


class TestAccretor:
    def test_add(self):
        a: pu.formal_language.Accretor = pu.formal_language.Accretor(
            valid_python_types=(pu.formal_language.FormalObject,))
        assert len(a) == 0
        x: pu.formal_language.FormalObject = pu.formal_language.FormalObject()
        a.add(x)
        assert len(a) == 1
        a.add(x)
        assert len(a) == 1
        for e in a:
            assert e is x
        with pytest.raises(Exception) as e_info:
            y: int = 5
            a.add(y)
        assert len(a) == 1
        a.lock()
        with pytest.raises(Exception) as e_info:
            z = pu.formal_language.FormalObject = pu.formal_language.FormalObject()
            a.add(z)
        assert len(a) == 1
