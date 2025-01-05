import pytest
import punctilious as pu


class TestSetDefinedByExtension:
    def test_1(self):
        set2 = pu.foundational_connectors.set_1
        a = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='d'))
        phi1 = set2(a(), b(), c())
        phi2 = pu.foundational_objects.ensure_set_1(o=phi1)
        assert pu.formal_language.is_formula_equivalent(phi=phi1, psi=phi2)
        phi3 = set2(a(), b(), a())
        with pytest.raises(ValueError):
            pu.foundational_objects.ensure_set_1(o=phi3)
        with pytest.raises(ValueError):
            pu.foundational_objects.Set1(a(), b(), a())
        phi4 = set2(a(), b(a()), a(b()), c(a()))
        phi5 = pu.foundational_objects.ensure_set_1(o=phi4)
        assert len(phi5.arguments) == 4
        phi6 = set2()
        phi7 = pu.foundational_objects.ensure_set_1(o=phi6)
        assert len(phi7.arguments) == 0
