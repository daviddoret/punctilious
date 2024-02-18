import pytest

# import punctilious as pu
import utils


class TestTypesettingClass:
    def test_typesetting_class(self):
        class H1(utils.TypesettingClass):
            FORMAL_OBJECT = utils.TC(None)
            FORMULA = utils.TC(FORMAL_OBJECT)
            BINARY_FORMULA = utils.TC(FORMULA)

        utils.TypesettingClass.load_elements(H1)

        class H2(utils.TypesettingClass):
            FORMAL_OBJECT = utils.TC(None)
            FORMULA = utils.TC(FORMAL_OBJECT)
            BINARY_FORMULA = utils.TC(FORMULA)

        utils.TypesettingClass.load_elements(H2)

        assert H1.FORMAL_OBJECT.is_subclass_of(H1.FORMAL_OBJECT)
        assert H1.FORMULA.is_subclass_of(H1.FORMAL_OBJECT)
        assert H1.FORMULA.is_subclass_of(H1.FORMAL_OBJECT)
        assert H1.FORMULA.is_subclass_of(H1.FORMULA)
        assert H1.BINARY_FORMULA.is_subclass_of(H1.FORMAL_OBJECT)
        assert H1.BINARY_FORMULA.is_subclass_of(H1.FORMULA)
        assert H1.BINARY_FORMULA.is_subclass_of(H1.BINARY_FORMULA)
        assert not H1.FORMULA.is_subclass_of(H2.FORMULA)
        assert not H1.FORMAL_OBJECT.is_subclass_of(H1.BINARY_FORMULA)
        assert not H1.FORMULA.is_subclass_of(H1.BINARY_FORMULA)
