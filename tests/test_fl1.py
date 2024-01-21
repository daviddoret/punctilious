import pytest
import punctilious as pu


class TestConnective:
    def test_typesetting(self):
        c = pu.fl1.Connective()
        assert (c.to_string(protocol=ts.protocols.unicode_limited) == "*")


class TestAccretor:
    def test_add(self):
        ml: pu.fl1.MetaLanguage = pu.fl1.MetaLanguage()
        a: pu.fl1.AccretorTuple = pu.fl1.AccretorTuple(valid_formal_classes=(ml.formal_classes.formal_object_class,))
        assert len(a) == 0
        x: pu.fl1.FormalObject = pu.fl1.FormalObject()
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
            z: pu.fl1.FormalObject = pu.fl1.FormalObject()
            a.add(z)
        assert len(a) == 1
        pass


class TestFormalPythonClass:

    def test_has_element(self):
        ml: pu.fl1.MetaLanguage = pu.fl1.MetaLanguage()
        x: pu.fl1.FormalObject = pu.fl1.FormalObject()
        assert ml.formal_classes.formal_object_class.has_element(x=x)
        assert not ml.formal_classes.connective_class.has_element(x=x)
        y: pu.fl1.FormalObject = pu.fl1.Connective()
        assert ml.formal_classes.formal_object_class.has_element(x=y)
        assert ml.formal_classes.connective_class.has_element(x=y)
