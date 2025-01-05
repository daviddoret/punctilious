import pytest
import punctilious as pu


class TestFormulasAreUnique:
    def test_1(self):
        a = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='d'))
        assert pu.formal_language.formulas_are_unique()
        assert pu.formal_language.formulas_are_unique(a(), b(), c(), d())
        assert not pu.formal_language.formulas_are_unique(a(), b(), c(), a(), d())
        with pytest.raises(ValueError):
            pu.formal_language.formulas_are_unique(a(), b(), 5, a(), d())
