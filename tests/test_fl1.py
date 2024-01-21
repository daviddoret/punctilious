import pytest
from punctilious import *


class TestConnective:
    def test_typesetting(self):
        c = fl1.Connective()
        assert (c.to_string(protocol=ts.protocols.unicode_limited) == "*")


class TestAccretor:
    def test_add(self):
        ml: fl1.MetaLanguage = fl1.MetaLanguage()
        a: fl1.AccretorTuple = fl1.AccretorTuple(valid_formal_classes=(ml.formal_classes.formal_object_class,))
        assert len(a) == 0
        x: fl1.FormalObject = fl1.FormalObject()
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
            z: fl1.FormalObject = fl1.FormalObject()
            a.add(z)
        assert len(a) == 1
        pass


class TestFormalPythonClass:

    def test_has_element(self):
        ml: fl1.MetaLanguage = fl1.MetaLanguage()
        x: fl1.FormalObject = fl1.FormalObject()
        assert ml.formal_classes.formal_object_class.has_element(x=x)
        assert not ml.formal_classes.connective_class.has_element(x=x)
        y: fl1.FormalObject = fl1.Connective()
        assert ml.formal_classes.formal_object_class.has_element(x=y)
        assert ml.formal_classes.connective_class.has_element(x=y)
