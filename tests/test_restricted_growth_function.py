import pytest

import punctilious as pu


class TestRestrictedGrowthFunctionSequence:
    def test_data_validation(self, s3a, s3b, s14a, s14b):
        assert pu.rgf.data_validate_restricted_growth_function_sequence_elements(s3a) == s3a
        assert pu.rgf.data_validate_restricted_growth_function_sequence_elements(s14a) == s14a
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgf.data_validate_restricted_growth_function_sequence_elements(s3b)
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgf.data_validate_restricted_growth_function_sequence_elements(s14b)

    def test_data_validation_in_construction(self, s3a, s3b, s14a, s14b):
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgf.RestrictedGrowthFunctionSequence(*s3b)
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgf.RestrictedGrowthFunctionSequence(*s14b)

    def test_equality(self, s3a, s3b, s14a, s14b):
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s3a) == pu.rgf.RestrictedGrowthFunctionSequence(*s3a)
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s14a) == pu.rgf.RestrictedGrowthFunctionSequence(*s14a)

    def test_inequality(self, s3a, s3b, s14a, s14b):
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s3a) != pu.rgf.RestrictedGrowthFunctionSequence(*s14a)
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s14a) != pu.rgf.RestrictedGrowthFunctionSequence(*s3a)

    def test_cache(self, s3a, s3b, s14a, s14b):
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s3a) is pu.rgf.RestrictedGrowthFunctionSequence(*s3a)
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s14a) is pu.rgf.RestrictedGrowthFunctionSequence(*s14a)
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s3a) is not pu.rgf.RestrictedGrowthFunctionSequence(*s14a)
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s14a) is not pu.rgf.RestrictedGrowthFunctionSequence(*s3a)

    def test_conversion_from_arbitrary_sequence(self):
        assert pu.rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (0, 1, 2,)) == pu.rgf.RestrictedGrowthFunctionSequence(0, 1, 2)
        assert pu.rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (2, 1, 0,)) == pu.rgf.RestrictedGrowthFunctionSequence(0, 1, 2)
        assert pu.rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (2, 4, 4, 9, 0, 2, 2, 0,)) == pu.rgf.RestrictedGrowthFunctionSequence(0, 1, 1, 2, 3, 0, 0, 3)

    def test_max_value(self, rgf1, rgf2a, rgf2b, rgf6a, rgf12a):
        assert rgf1.max_value == 0
        assert rgf2a.max_value == 0
        assert rgf2b.max_value == 1
        assert rgf6a.max_value == 5
        assert rgf12a.max_value == 11
