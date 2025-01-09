import pytest
import punctilious as pu


class TestUniqueTuple:
    def test_1(self):
        set1 = pu.foundational_connectors.unique_extension_tuple
        a = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='d'))
        phi1 = set1(a(), b(), c())
        phi2 = pu.foundational_objects.ensure_unique_extension_tuple(o=phi1)
        assert pu.formal_language.is_formula_equivalent(phi=phi1, psi=phi2)
        phi3 = set1(a(), b(), a())
        with pytest.raises(ValueError):
            pu.foundational_objects.ensure_unique_extension_tuple(o=phi3)
        with pytest.raises(ValueError):
            pu.foundational_objects.UniqueExtensionTuple(a(), b(), a())
        phi4 = set1(a(), b(a()), a(b()), c(a()))
        phi5 = pu.foundational_objects.ensure_unique_extension_tuple(o=phi4)
        assert len(phi5.arguments) == 4
        phi6 = set1()
        phi7 = pu.foundational_objects.ensure_unique_extension_tuple(o=phi6)
        assert len(phi7.arguments) == 0


class TestUnionSets1:
    def test_1(self):
        a = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='d'))
        s1 = pu.foundational_objects.UniqueExtensionTuple()
        s2 = pu.foundational_objects.UniqueExtensionTuple(a(), b(), d())
        s3 = pu.foundational_objects.UniqueExtensionTuple(b())
        s4 = pu.foundational_objects.UniqueExtensionTuple(d(), c())
        s5 = pu.foundational_objects.UniqueExtensionTuple(a(), b(), c(), d())

        after = pu.foundational_objects.union_unique_tuples(s1, s1)
        assert after.is_unique_extension_tuple_equivalent_to(s1)

        after = pu.foundational_objects.union_unique_tuples(s1, s2)
        assert after.is_unique_extension_tuple_equivalent_to(s2)

        after = pu.foundational_objects.union_unique_tuples(s2, s3)
        assert after.is_unique_extension_tuple_equivalent_to(s2)

        after = pu.foundational_objects.union_unique_tuples(s2, s4)
        assert after.is_unique_extension_tuple_equivalent_to(s5)


class TestMap1:
    def test_1(self):
        map1 = pu.foundational_connectors.extension_map
        a = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='c'))
        x = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='z'))
        domain = pu.foundational_objects.UniqueExtensionTuple(a(), b(), c())
        codomain = pu.foundational_objects.ExtensionTuple(x(), y(), z())
        m1 = pu.foundational_objects.ExtensionMap(domain=domain,
                                                  codomain=codomain)
        assert m1.get_image(x=a()).is_formula_equivalent(x())
        assert m1.get_image(x=b()).is_formula_equivalent(y())
        assert m1.get_image(x=c()).is_formula_equivalent(z())
        with pytest.raises(ValueError):
            m1.get_image(x=x())

        domain = pu.foundational_objects.UniqueExtensionTuple(c(), b(), a())
        codomain = pu.foundational_objects.ExtensionTuple(z(), y(), x())
        m2 = pu.foundational_objects.ExtensionMap(domain=domain,
                                                  codomain=codomain)

        assert m1.is_map_equivalent(other=m2)


class TestSubstitute:
    def test_1(self):
        a = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='c'))
        x = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='z'))
        domain = pu.foundational_objects.UniqueExtensionTuple(a(), b(), c())
        codomain = pu.foundational_objects.ExtensionTuple(x(), y(), z())
        m1 = pu.foundational_objects.ExtensionMap(domain=domain,
                                                  codomain=codomain)

        phi = pu.foundational_objects.substitute_formulas(
            phi=a(b(c())),
            m=m1)
        assert phi.is_formula_equivalent(other=a(b(z())))

        phi = pu.foundational_objects.substitute_formulas(
            phi=a(b(c(), b(), c()), c(b())),
            m=m1)
        assert phi.is_formula_equivalent(other=a(b(z(), y(), z()), c(y())))

        phi = pu.foundational_objects.substitute_formulas(
            phi=x(z(z(z(y()), z(x(y()))))),
            m=m1)
        assert phi.is_formula_equivalent(other=x(z(z(z(y()), z(x(y()))))))

        domain = pu.foundational_objects.UniqueExtensionTuple(b(b(c())))
        codomain = pu.foundational_objects.ExtensionTuple(x(y()))
        m2 = pu.foundational_objects.ExtensionMap(domain=domain,
                                                  codomain=codomain)

        phi = pu.foundational_objects.substitute_formulas(
            phi=a(b(c()), b(b(c())), b(b(b(c()))), b(b(b(b(c()))))),
            m=m2)
        assert phi.is_formula_equivalent(other=a(b(c()), x(y()), b(x(y())), b(b(x(y())))))

    def test_2(self):
        a = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='d'))
        e = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='e'))
        f = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='f'))
        x = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='z'))
        domain = pu.foundational_objects.UniqueExtensionTuple(a(), b(), c())
        codomain = pu.foundational_objects.ExtensionTuple(x(), y(), z())
        m1 = pu.foundational_objects.ExtensionMap(domain=domain,
                                                  codomain=codomain)
        # no match
        input = e(f(), d(e()))
        output = pu.foundational_objects.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(input)

        # basic root match
        input = a()
        output = pu.foundational_objects.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(x())

        # several level 1 arguments
        input = a(d(), e(), b(), a(), f(), c())
        output = pu.foundational_objects.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(a(d(), e(), y(), x(), f(), z()))

        # arguments at different levels
        input = a(d(b(), e()), e(a()), b(), a(), f(), c(c()))
        output = pu.foundational_objects.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(a(d(y(), e()), e(x()), y(), x(), f(), c(z())))

        domain = pu.foundational_objects.UniqueExtensionTuple(a(a(b())), b(a(), b(b(b())), c()), c())
        codomain = pu.foundational_objects.ExtensionTuple(x(), y(a(), y(), z(b())), z(x(y(a()))))
        m2 = pu.foundational_objects.ExtensionMap(domain=domain,
                                                  codomain=codomain)

        # multi level variables and multi level values
        input = a(d(b(), e(b(a(), b(b(b(a(a(b())))))))), e(a()), b(a(a(b()))), a(b(a(), b(b(b())), c())), f(), c(c()))
        output = pu.foundational_objects.substitute_formulas(phi=input, m=m2)
        assert output.is_formula_equivalent(
            a(d(b(), e(b(a(), b(b(b(x())))))), e(a()), b(x()), a(y(a(), y(), z(b()))), f(), c(z(x(y(a()))))))


class TestFormulaEquivalenceWithVariables:
    def test_2(self):
        a = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='d'))
        e = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='e'))
        f = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='f'))
        x = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.formal_language.Connector(uid=pu.identifiers.create_uid(slug='z'))
        domain = pu.foundational_objects.UniqueExtensionTuple(a(), b(), c())
        codomain = pu.foundational_objects.ExtensionTuple(x(), y(), z())
        m1 = pu.foundational_objects.ExtensionMap(domain=domain,
                                                  codomain=codomain)
        # no match
        input = e(f(), d(e()))
        output = pu.foundational_objects.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(input)
        pu.foundational_objects.is_formula_equivalent_with_variables(phi=input, psi=output, v=domain)

        # basic root match
        input = a()
        output = pu.foundational_objects.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(x())

        # several level 1 arguments
        input = a(d(), e(), b(), a(), f(), c())
        output = pu.foundational_objects.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(a(d(), e(), y(), x(), f(), z()))

        # arguments at different levels
        input = a(d(b(), e()), e(a()), b(), a(), f(), c(c()))
        output = pu.foundational_objects.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(a(d(y(), e()), e(x()), y(), x(), f(), c(z())))

        domain = pu.foundational_objects.UniqueExtensionTuple(a(a(b())), b(a(), b(b(b())), c()), c())
        codomain = pu.foundational_objects.ExtensionTuple(x(), y(a(), y(), z(b())), z(x(y(a()))))
        m2 = pu.foundational_objects.ExtensionMap(domain=domain,
                                                  codomain=codomain)

        # multi level variables and multi level values
        input = a(d(b(), e(b(a(), b(b(b(a(a(b())))))))), e(a()), b(a(a(b()))), a(b(a(), b(b(b())), c())), f(), c(c()))
        output = pu.foundational_objects.substitute_formulas(phi=input, m=m2)
        assert output.is_formula_equivalent(
            a(d(b(), e(b(a(), b(b(b(x())))))), e(a()), b(x()), a(y(a(), y(), z(b()))), f(), c(z(x(y(a()))))))
