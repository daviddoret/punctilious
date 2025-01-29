import pytest
import punctilious as pu


class TestFormulasAreUnique:
    def test_1(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        assert pu.fml.formulas_are_unique()
        assert pu.fml.formulas_are_unique(a(), b(), c(), d())
        assert not pu.fml.formulas_are_unique(a(), b(), c(), a(), d())
        with pytest.raises(pu.utl.PunctiliousError):
            pu.fml.formulas_are_unique(a(), b(), 5, a(), d())


class TestFormula:
    def test_contains_formula(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        e = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='e'))
        phi = a(b(a(b(c(d(a(), c(d())), a(b()), d())))))
        assert phi.tree_contains_formula(phi=a())
        assert phi.tree_contains_formula(phi=b())
        assert not phi.tree_contains_formula(phi=c())
        assert phi.tree_contains_formula(phi=c(d()))
        assert phi.tree_contains_formula(phi=d())
        assert not phi.tree_contains_formula(phi=e())

        assert a().tree_contains_formula(phi=a())
        assert a().tree_contains_formula(phi=a(), include_root=True)
        assert not a().tree_contains_formula(phi=a(), include_root=False)


class TestEnsureUniqueFormulas:
    def test_1(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        e = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='e'))

        before = (a(), b(), c(),)
        after = pu.fml.ensure_unique_formulas(*before)
        assert before == after

        before = (a(), b(), c(), a(),)
        after = pu.fml.ensure_unique_formulas(
            *before,
            duplicate_processing=pu.constants.ExtraneousElementOptions.STRIP)
        assert before != after
        assert after == (a(), b(), c(),)

        before = (a(), b(), c(), a(), c(), c(), c(), b(), a())
        with pytest.raises(pu.utl.PunctiliousError):
            after = pu.fml.ensure_unique_formulas(
                *before,
                duplicate_processing=pu.constants.ExtraneousElementOptions.RAISE_ERROR)
        after = pu.fml.ensure_unique_formulas(
            *before,
            duplicate_processing=pu.constants.ExtraneousElementOptions.STRIP)
        assert before != after
        assert after == (a(), b(), c(),)
