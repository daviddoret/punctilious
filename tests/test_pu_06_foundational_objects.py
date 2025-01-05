import pytest
import punctilious as pu


class TestSet1:
    def test_1(self):
        set1 = pu.foundational_connectors.set_1
        a = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='d'))
        phi1 = set1(a(), b(), c())
        phi2 = pu.foundational_objects.ensure_set_1(o=phi1)
        assert pu.formal_language.is_formula_equivalent(phi=phi1, psi=phi2)
        phi3 = set1(a(), b(), a())
        with pytest.raises(ValueError):
            pu.foundational_objects.ensure_set_1(o=phi3)
        with pytest.raises(ValueError):
            pu.foundational_objects.Set1(a(), b(), a())
        phi4 = set1(a(), b(a()), a(b()), c(a()))
        phi5 = pu.foundational_objects.ensure_set_1(o=phi4)
        assert len(phi5.arguments) == 4
        phi6 = set1()
        phi7 = pu.foundational_objects.ensure_set_1(o=phi6)
        assert len(phi7.arguments) == 0


class TestMap1:
    def test_1(self):
        map1 = pu.foundational_connectors.map_1
        a = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='c'))
        x = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='z'))
        domain = pu.foundational_objects.Set1(a(), b(), c())
        codomain = pu.foundational_objects.Tuple1(x(), y(), z())
        m1 = pu.foundational_objects.Map1(d=domain,
                                          c=codomain)
        assert m1.get_image(x=a()).is_formula_equivalent(x())
        assert m1.get_image(x=b()).is_formula_equivalent(y())
        assert m1.get_image(x=c()).is_formula_equivalent(z())
        with pytest.raises(ValueError):
            m1.get_image(x=x())
