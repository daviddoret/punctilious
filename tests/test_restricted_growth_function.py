import pytest

import punctilious as pu


class TestRestrictedGrowthFunctionSequence:
    def test_data_validation(self, s1, s2, s3, s4):
        assert pu.rgf.data_validate_restricted_growth_function_sequence_elements(s1) == s1
        assert pu.rgf.data_validate_restricted_growth_function_sequence_elements(s3) == s3
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgf.data_validate_restricted_growth_function_sequence_elements(s2)
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgf.data_validate_restricted_growth_function_sequence_elements(s4)

    def test_data_validation_in_construction(self, s1, s2, s3, s4):
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgf.RestrictedGrowthFunctionSequence(*s2)
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgf.RestrictedGrowthFunctionSequence(*s4)

    def test_equality(self, s1, s2, s3, s4):
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s1) == pu.rgf.RestrictedGrowthFunctionSequence(*s1)
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s3) == pu.rgf.RestrictedGrowthFunctionSequence(*s3)

    def test_inequality(self, s1, s2, s3, s4):
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s1) != pu.rgf.RestrictedGrowthFunctionSequence(*s3)
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s3) != pu.rgf.RestrictedGrowthFunctionSequence(*s1)

    def test_cache(self, s1, s2, s3, s4):
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s1) is pu.rgf.RestrictedGrowthFunctionSequence(*s1)
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s3) is pu.rgf.RestrictedGrowthFunctionSequence(*s3)
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s1) is not pu.rgf.RestrictedGrowthFunctionSequence(*s3)
        assert pu.rgf.RestrictedGrowthFunctionSequence(*s3) is not pu.rgf.RestrictedGrowthFunctionSequence(*s1)

    def test_conversion_from_arbitrary_sequence(self):
        assert pu.rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (1, 2, 3,)) == pu.rgf.RestrictedGrowthFunctionSequence(1, 2, 3)
        assert pu.rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (3, 2, 1,)) == pu.rgf.RestrictedGrowthFunctionSequence(1, 2, 3)
        assert pu.rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (3, 5, 5, 10, 1, 3, 3, 1,)) == pu.rgf.RestrictedGrowthFunctionSequence(1, 2, 2, 3, 4, 1, 1, 4)
