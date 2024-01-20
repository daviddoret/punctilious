import pytest
from punctilious import formal_language as fl


class TestAccretor:
    def test_add(self):
        a: fl.AccretorTuple = fl.AccretorTuple(valid_python_types=(fl.FormalObject,))
        assert len(a) == 0
        x: fl.FormalObject = fl.FormalObject()
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
            z = fl.FormalObject = fl.FormalObject()
            a.add(z)
        assert len(a) == 1


class TestFormalPythonClass:
    def test_has_element(self):
        ml: fl.MetaLanguage = fl.MetaLanguage()
        x: fl.FormalObject = fl.FormalObject()
        assert ml.formal_classes.formal_object_class.has_element(x=x)
        assert not ml.formal_classes.connective_class.has_element(x=x)
        y: fl.FormalObject = fl.Connective()
        assert ml.formal_classes.formal_object_class.has_element(x=y)
        assert ml.formal_classes.connective_class.has_element(x=y)
        z: str = "hello world"
        assert not ml.formal_classes.formal_object_class.has_element(x=z)
        assert not ml.formal_classes.connective_class.has_element(x=z)
