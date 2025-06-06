import pytest

import punctilious as pu


@pytest.fixture
def s1():
    return (1, 2, 3,)


@pytest.fixture
def s2():
    return (1, 3, 2,)


@pytest.fixture
def s3():
    return (1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 4, 3, 2, 3,)


@pytest.fixture
def s4():
    return (1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 4, 3, 7, 3,)


class TestRestrictedGrowthFunctionSequence:
    def test_data_validation(self, s1, s2, s3, s4):
        assert pu.edp.data_validate_restricted_growth_function_sequence_elements(s1) == s1
        assert pu.edp.data_validate_restricted_growth_function_sequence_elements(s3) == s3
        with pytest.raises(pu.util.PunctiliousException):
            pu.edp.data_validate_restricted_growth_function_sequence_elements(s2)
        with pytest.raises(pu.util.PunctiliousException):
            pu.edp.data_validate_restricted_growth_function_sequence_elements(s4)

    def test_data_validation_in_construction(self, s1, s2, s3, s4):
        with pytest.raises(pu.util.PunctiliousException):
            pu.edp.RestrictedGrowthFunctionSequence(*s2)
        with pytest.raises(pu.util.PunctiliousException):
            pu.edp.RestrictedGrowthFunctionSequence(*s4)

    def test_equality(self, s1, s2, s3, s4):
        assert pu.edp.RestrictedGrowthFunctionSequence(*s1) == pu.edp.RestrictedGrowthFunctionSequence(*s1)
        assert pu.edp.RestrictedGrowthFunctionSequence(*s3) == pu.edp.RestrictedGrowthFunctionSequence(*s3)

    def test_inequality(self, s1, s2, s3, s4):
        assert pu.edp.RestrictedGrowthFunctionSequence(*s1) != pu.edp.RestrictedGrowthFunctionSequence(*s3)
        assert pu.edp.RestrictedGrowthFunctionSequence(*s3) != pu.edp.RestrictedGrowthFunctionSequence(*s1)

    def test_cache(self, s1, s2, s3, s4):
        assert pu.edp.RestrictedGrowthFunctionSequence(*s1) is pu.edp.RestrictedGrowthFunctionSequence(*s1)
        assert pu.edp.RestrictedGrowthFunctionSequence(*s3) is pu.edp.RestrictedGrowthFunctionSequence(*s3)
        assert pu.edp.RestrictedGrowthFunctionSequence(*s1) is not pu.edp.RestrictedGrowthFunctionSequence(*s3)
        assert pu.edp.RestrictedGrowthFunctionSequence(*s3) is not pu.edp.RestrictedGrowthFunctionSequence(*s1)
