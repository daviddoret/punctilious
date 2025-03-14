import pytest
import punctilious_20250223 as pu


class TestWellFormedUniqueExtensionTuple:
    def test_1(self):
        unique_tuple = pu.mtl.unique_extension_tuple_connector
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        phi1 = unique_tuple(a(), b(), c())
        assert pu.mtl.is_well_formed_unique_extension_tuple(phi1)
        phi2 = pu.mtl.ensure_well_formed_unique_extension_tuple(formula=phi1)
        assert pu.fml.is_formula_equivalent(phi=phi1, psi=phi2)
        phi3 = unique_tuple(a(), b(), a())
        with pytest.raises(pu.utl.PunctiliousError):
            pu.mtl.ensure_well_formed_unique_extension_tuple(formula=phi3)
        with pytest.raises(pu.utl.PunctiliousError):
            pu.mtl.WellFormedUniqueExtensionTuple(a(), b(), a())
        phi4 = unique_tuple(a(), b(a()), a(b()), c(a()))
        phi5 = pu.mtl.ensure_well_formed_unique_extension_tuple(formula=phi4)
        assert len(phi5.arguments) == 4
        phi6 = unique_tuple()
        phi7 = pu.mtl.ensure_well_formed_unique_extension_tuple(formula=phi6)
        assert len(phi7.arguments) == 0

        # implicit conversion
        phi8 = pu.fml.ensure_formula({a(), b(), c(), })
        phi8 = pu.mtl.ensure_well_formed_formula(phi8)
        assert phi8.is_well_formed_unique_extension_tuple_equivalent_to(phi1)


class TestWellFormedExtensionTuple:
    def test_1(self):
        extension_tuple = pu.mtl.extension_tuple_connector
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        phi1 = extension_tuple(a(), b(), c())
        assert pu.mtl.is_well_formed_extension_tuple(phi1)
        phi2 = pu.mtl.ensure_well_formed_extension_tuple(phi1)
        assert pu.fml.is_formula_equivalent(phi=phi1, psi=phi2)
        phi3 = extension_tuple(a(), b(), a())
        assert not phi3.has_unique_arguments
        phi4 = extension_tuple(a(), b(a()), a(b()), c(a()))
        phi5 = pu.mtl.ensure_well_formed_extension_tuple(phi4)
        assert len(phi5.arguments) == 4
        phi6 = extension_tuple()
        phi7 = pu.mtl.ensure_well_formed_extension_tuple(phi6)
        assert len(phi7.arguments) == 0

        # implicit conversion
        phi8 = pu.fml.ensure_formula((a(), b(), c(),))
        assert phi8.is_formula_equivalent(phi1)
        phi8 = pu.fml.ensure_formula([a(), b(), c(), ])
        assert phi8.is_formula_equivalent(phi1)


class TestUnionSets1:
    def test_1(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        s1 = pu.mtl.WellFormedUniqueExtensionTuple()
        s2 = pu.mtl.WellFormedUniqueExtensionTuple(a(), b(), d())
        s3 = pu.mtl.WellFormedUniqueExtensionTuple(b())
        s4 = pu.mtl.WellFormedUniqueExtensionTuple(d(), c())
        s5 = pu.mtl.WellFormedUniqueExtensionTuple(a(), b(), c(), d())

        after = pu.mtl.union_unique_tuples(s1, s1)
        assert after.is_well_formed_unique_extension_tuple_equivalent_to(s1)

        after = pu.mtl.union_unique_tuples(s1, s2)
        assert after.is_well_formed_unique_extension_tuple_equivalent_to(s2)

        after = pu.mtl.union_unique_tuples(s2, s3)
        assert after.is_well_formed_unique_extension_tuple_equivalent_to(s2)

        after = pu.mtl.union_unique_tuples(s2, s4)
        assert after.is_well_formed_unique_extension_tuple_equivalent_to(s5)


class TestWellFormedExtensionMap:
    def test_1(self):
        map1 = pu.mtl.extension_map_connector
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        x = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='z'))
        domain = pu.mtl.WellFormedUniqueExtensionTuple(a(), b(), c())
        codomain = pu.mtl.WellFormedExtensionTuple(x(), y(), z())
        m1 = pu.mtl.WellFormedExtensionMap(domain=domain,
                                           codomain=codomain)
        assert m1.get_image(x=a()).is_formula_equivalent(x())
        assert m1.get_image(x=b()).is_formula_equivalent(y())
        assert m1.get_image(x=c()).is_formula_equivalent(z())
        with pytest.raises(pu.utl.PunctiliousError):
            m1.get_image(x=x())

        domain = pu.mtl.WellFormedUniqueExtensionTuple(c(), b(), a())
        codomain = pu.mtl.WellFormedExtensionTuple(z(), y(), x())
        m2 = pu.mtl.WellFormedExtensionMap(domain=domain,
                                           codomain=codomain)

        assert m1.is_map_equivalent(other=m2)


class TestSubstitute:
    def test_1(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        x = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='z'))
        domain = pu.mtl.WellFormedUniqueExtensionTuple(a(), b(), c())
        codomain = pu.mtl.WellFormedExtensionTuple(x(), y(), z())
        m1 = pu.mtl.WellFormedExtensionMap(domain=domain,
                                           codomain=codomain)

        phi = pu.mtl.substitute_formulas(
            phi=a(b(c())),
            m=m1)
        assert phi.is_formula_equivalent(other_formula=a(b(z())))

        phi = pu.mtl.substitute_formulas(
            phi=a(b(c(), b(), c()), c(b())),
            m=m1)
        assert phi.is_formula_equivalent(other_formula=a(b(z(), y(), z()), c(y())))

        phi = pu.mtl.substitute_formulas(
            phi=x(z(z(z(y()), z(x(y()))))),
            m=m1)
        assert phi.is_formula_equivalent(other_formula=x(z(z(z(y()), z(x(y()))))))

        domain = pu.mtl.WellFormedUniqueExtensionTuple(b(b(c())))
        codomain = pu.mtl.WellFormedExtensionTuple(x(y()))
        m2 = pu.mtl.WellFormedExtensionMap(domain=domain,
                                           codomain=codomain)

        phi = pu.mtl.substitute_formulas(
            phi=a(b(c()), b(b(c())), b(b(b(c()))), b(b(b(b(c()))))),
            m=m2)
        assert phi.is_formula_equivalent(other_formula=a(b(c()), x(y()), b(x(y())), b(b(x(y())))))

    def test_2(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        e = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='e'))
        f = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='f'))
        x = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='z'))
        domain = pu.mtl.WellFormedUniqueExtensionTuple(a(), b(), c())
        codomain = pu.mtl.WellFormedExtensionTuple(x(), y(), z())
        m1 = pu.mtl.WellFormedExtensionMap(domain=domain,
                                           codomain=codomain)
        # no match
        input = e(f(), d(e()))
        output = pu.mtl.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(input)

        # basic root match
        input = a()
        output = pu.mtl.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(x())

        # several level 1 arguments
        input = a(d(), e(), b(), a(), f(), c())
        output = pu.mtl.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(a(d(), e(), y(), x(), f(), z()))

        # arguments at different levels
        input = a(d(b(), e()), e(a()), b(), a(), f(), c(c()))
        output = pu.mtl.substitute_formulas(phi=input, m=m1)
        assert output.is_formula_equivalent(a(d(y(), e()), e(x()), y(), x(), f(), c(z())))

        domain = pu.mtl.WellFormedUniqueExtensionTuple(a(a(b())), b(a(), b(b(b())), c()), c())
        codomain = pu.mtl.WellFormedExtensionTuple(x(), y(a(), y(), z(b())), z(x(y(a()))))
        m2 = pu.mtl.WellFormedExtensionMap(domain=domain,
                                           codomain=codomain)

        # multi level variables and multi level values
        input = a(d(b(), e(b(a(), b(b(b(a(a(b())))))))), e(a()), b(a(a(b()))), a(b(a(), b(b(b())), c())), f(), c(c()))
        output = pu.mtl.substitute_formulas(phi=input, m=m2)
        assert output.is_formula_equivalent(
            a(d(b(), e(b(a(), b(b(b(x())))))), e(a()), b(x()), a(y(a(), y(), z(b()))), f(), c(z(x(y(a()))))))


class TestFormulaEquivalenceWithVariables:
    def test_2(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        e = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='e'))
        f = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='f'))
        x = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='z'))
        variables = pu.mtl.WellFormedUniqueExtensionTuple(x(), y(), z())
        values = pu.mtl.WellFormedExtensionTuple(d(), e(), f())
        m1 = pu.mtl.WellFormedExtensionMap(domain=variables,
                                           codomain=values)
        # no match
        formulas_with_variables = b(c(), a(b()))
        formula_without_variables = pu.mtl.substitute_formulas(phi=formulas_with_variables, m=m1)
        assert formula_without_variables.is_formula_equivalent(formulas_with_variables)
        check, m3 = pu.mtl.is_formula_equivalent_with_variables(
            formula_without_variables=formulas_with_variables,
            formula_with_variables=formula_without_variables,
            variables=variables)
        assert check

        # basic root match
        formulas_with_variables = x()
        formula_without_variables = pu.mtl.substitute_formulas(phi=formulas_with_variables, m=m1)
        assert formula_without_variables.is_formula_equivalent(d())
        check, m3 = pu.mtl.is_formula_equivalent_with_variables(
            formula_without_variables=formula_without_variables,
            formula_with_variables=formulas_with_variables,
            variables=variables)
        assert check
        assert m3.get_image(x()) == d()

        # several level 1 arguments
        formulas_with_variables = x(a(), b(), y(), x(), c(), z())
        formula_without_variables = pu.mtl.substitute_formulas(phi=formulas_with_variables, m=m1)
        assert formula_without_variables.is_formula_equivalent(x(a(), b(), e(), d(), c(), f()))
        check, m3 = pu.mtl.is_formula_equivalent_with_variables(
            formula_without_variables=formula_without_variables,
            formula_with_variables=formulas_with_variables,
            variables=variables)
        assert check
        assert m3.get_image(x()) == d()
        assert m3.get_image(y()) == e()
        assert m3.get_image(z()) == f()

        # several level 2 arguments
        formulas_with_variables = x(a(x(), y()), b(y(), z()))
        formula_without_variables = pu.mtl.substitute_formulas(phi=formulas_with_variables, m=m1)
        assert formula_without_variables.is_formula_equivalent(x(a(d(), e()), b(e(), f())))
        check, m3 = pu.mtl.is_formula_equivalent_with_variables(
            formula_without_variables=formula_without_variables,
            formula_with_variables=formulas_with_variables,
            variables=variables)
        assert check
        assert m3.get_image(x()) == d()
        assert m3.get_image(y()) == e()
        assert m3.get_image(z()) == f()

        # arguments at different levels
        formulas_with_variables = x(a(y(), b()), b(x()), y(), x(), c(), z(z()))
        formula_without_variables = pu.mtl.substitute_formulas(phi=formulas_with_variables, m=m1)
        assert formula_without_variables.is_formula_equivalent(x(a(e(), b()), b(d()), e(), d(), c(), z(f())))
        check, m3 = pu.mtl.is_formula_equivalent_with_variables(
            formula_without_variables=formula_without_variables,
            formula_with_variables=formulas_with_variables,
            variables=variables)
        assert check
        assert m3.get_image(x()) == d()
        assert m3.get_image(y()) == e()
        assert m3.get_image(z()) == f()

        variables = pu.mtl.WellFormedUniqueExtensionTuple(x(x(y())), y(x(), y(y(y())), z()), z())
        values = pu.mtl.WellFormedExtensionTuple(d(), e(x(), e(), f(y())), f(d(e(x()))))
        m2 = pu.mtl.WellFormedExtensionMap(domain=variables,
                                           codomain=values)

        # multi level variables and multi level values
        formulas_with_variables = x(a(y(), b(y(x(), y(y(y(x(x(y())))))))), b(x()), y(x(x(y()))),
                                    x(y(x(), y(y(y())), z())), c(), z(z()))
        formula_without_variables = pu.mtl.substitute_formulas(phi=formulas_with_variables, m=m2)
        assert formula_without_variables.is_formula_equivalent(
            x(a(y(), b(y(x(), y(y(y(d())))))), b(x()), y(d()), x(e(x(), e(), f(y()))), c(), z(f(d(e(x()))))))
        check, m3 = pu.mtl.is_formula_equivalent_with_variables(
            formula_without_variables=formula_without_variables,
            formula_with_variables=formulas_with_variables,
            variables=variables)
        assert check


class TestWellFormedNaturalInferenceRule:
    def test_1(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        e = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='e'))
        f = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='f'))
        x = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='z'))
        variables = pu.mtl.WellFormedUniqueExtensionTuple(x(), y(), z())
        premises = pu.mtl.WellFormedUniqueExtensionTuple(
            a(x(), y()),
            b(y(), z())
        )
        conclusion = c(x(), z())
        inference_rule = pu.mtl.WellFormedNaturalInferenceRule(
            variables=variables,
            premises=premises,
            conclusion=conclusion
        )
        arguments = pu.mtl.WellFormedExtensionTuple(
            a(d(), e()),
            b(e(), f())
        )
        conclusion_with_variable_assignments = inference_rule.apply_rule(inputs=arguments)
        assert conclusion_with_variable_assignments.is_formula_equivalent(
            other_formula=c(d(), f()))


class TestWellFormedTheorem:
    def test_1(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        e = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='e'))
        f = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='f'))
        x = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='x'))
        y = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='y'))
        z = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='z'))
        variables = pu.mtl.WellFormedUniqueExtensionTuple(x(), y(), z())
        premises = pu.mtl.WellFormedUniqueExtensionTuple(
            a(x(), y()),
            b(y(), z())
        )
        conclusion = c(x(), z())
        inference_rule = pu.mtl.WellFormedNaturalInferenceRule(
            variables=variables,
            premises=premises,
            conclusion=conclusion
        )
        inputs = pu.mtl.WellFormedExtensionTuple(
            a(d(), e()),
            b(e(), f())
        )
        statement = inference_rule.apply_rule(inputs=inputs)

        theorem = pu.mtl.WellFormedTheorem(inputs=inputs,
                                           inference_rule=inference_rule,
                                           valid_statement=statement)

        assert theorem.valid_statement.is_formula_equivalent(statement)

        with pytest.raises(pu.utl.PunctiliousError):
            wrong_inputs = pu.mtl.WellFormedExtensionTuple(
                a(d(), e()),
                c(e(), f()))
            pu.mtl.WellFormedTheorem(inputs=wrong_inputs,
                                     inference_rule=inference_rule,
                                     valid_statement=statement)


class TestTheory:
    def test_1(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        e = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='e'))
        f = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='f'))
        x = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='x'))
        variables = pu.mtl.WellFormedUniqueExtensionTuple(x())
        premises = pu.mtl.WellFormedUniqueExtensionTuple(a(x()))
        conclusion = a(b(x()))
        inference_rule = pu.mtl.WellFormedNaturalInferenceRule(
            variables=variables,
            premises=premises,
            conclusion=conclusion
        )
        axiom = pu.mtl.WellFormedAxiom(a(c()))
        theory_components = (axiom, inference_rule)
        theory = pu.mtl.Theory(*theory_components)
        inputs = pu.mtl.WellFormedExtensionTuple(a(c()))
        theorem = pu.mtl.WellFormedTheorem(inputs=(a(c()),),
                                           inference_rule=inference_rule,
                                           valid_statement=a(b(c())))
        extended_theory = pu.mtl.Theory(*theory_components, theorem)

        pass


class TestWellFormedAxiom:
    def test_1(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))

        axiom_1_statement = a(b(c()), c())
        assert not pu.meta_language.is_well_formed_axiom(axiom_1_statement)
        assert not pu.meta_language.axiom_connector.validate_formula_well_formedness(axiom_1_statement)
        axiom_1_typed = pu.meta_language.WellFormedAxiom(axiom_1_statement)
        axiom_1_untyped = pu.meta_language.axiom_connector(axiom_1_statement)
        assert axiom_1_typed.is_formula_equivalent(axiom_1_untyped)
        assert axiom_1_untyped.is_formula_equivalent(axiom_1_typed)
        assert not axiom_1_typed.is_formula_equivalent(axiom_1_statement)
        assert pu.meta_language.is_well_formed_axiom(axiom_1_typed)
        assert pu.meta_language.is_well_formed_axiom(axiom_1_untyped)
        axiom_1_retyped = pu.meta_language.ensure_well_formed_axiom(axiom_1_untyped)
        assert axiom_1_retyped.is_formula_equivalent(axiom_1_typed)

        axiom_2_statement = a()
        assert not pu.meta_language.is_well_formed_axiom(axiom_2_statement)
        assert not pu.meta_language.axiom_connector.validate_formula_well_formedness(axiom_2_statement)
        axiom_2_typed = pu.meta_language.WellFormedAxiom(axiom_2_statement)
        axiom_2_untyped = pu.meta_language.axiom_connector(axiom_2_statement)
        assert axiom_2_typed.is_formula_equivalent(axiom_2_typed)
        assert axiom_2_untyped.is_formula_equivalent(axiom_2_typed)
        assert not axiom_2_typed.is_formula_equivalent(axiom_2_statement)
        assert pu.meta_language.is_well_formed_axiom(axiom_2_typed)
        assert pu.meta_language.is_well_formed_axiom(axiom_2_untyped)
        axiom_2_retyped = pu.meta_language.ensure_well_formed_axiom(axiom_2_untyped)
        assert axiom_2_retyped.is_formula_equivalent(axiom_2_typed)

        assert not axiom_1_typed.is_formula_equivalent(axiom_2_typed)
        assert not axiom_2_typed.is_formula_equivalent(axiom_1_typed)

        with pytest.raises(TypeError):
            pu.meta_language.WellFormedAxiom()

        with pytest.raises(pu.utl.PunctiliousError):
            pu.meta_language.WellFormedAxiom(None)

        with pytest.raises(TypeError):
            pu.meta_language.WellFormedAxiom(a(), b())

        with pytest.raises(pu.utl.PunctiliousError):
            pu.meta_language.ensure_well_formed_axiom(axiom_1_statement)

        pass
