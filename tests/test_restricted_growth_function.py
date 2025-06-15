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
            (1, 2, 3,)) == pu.rgf.RestrictedGrowthFunctionSequence(1, 2, 3)
        assert pu.rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (3, 2, 1,)) == pu.rgf.RestrictedGrowthFunctionSequence(1, 2, 3)
        assert pu.rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (3, 5, 5, 10, 1, 3, 3, 1,)) == pu.rgf.RestrictedGrowthFunctionSequence(1, 2, 2, 3, 4, 1, 1, 4)

    def test_max_value(self, rgf1, rgf2a, rgf2b, rgf6a, rgf12a):
        assert rgf1.max_value == 1
        assert rgf2a.max_value == 1
        assert rgf2b.max_value == 2
        assert rgf6a.max_value == 6
        assert rgf12a.max_value == 12
