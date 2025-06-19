import pytest

import punctilious as pu


class TestRestrictedGrowthFunctionSequence:
    def test_data_validation(self, s3a, s3b, s14a, s14b):
        assert pu.rgfs.data_validate_restricted_growth_function_sequence_elements(s3a) == s3a
        assert pu.rgfs.data_validate_restricted_growth_function_sequence_elements(s14a) == s14a
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgfs.data_validate_restricted_growth_function_sequence_elements(s3b)
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgfs.data_validate_restricted_growth_function_sequence_elements(s14b)

    def test_data_validation_in_construction(self, s3a, s3b, s14a, s14b):
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgfs.RestrictedGrowthFunctionSequence(*s3b)
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgfs.RestrictedGrowthFunctionSequence(*s14b)

    def test_equality(self, s3a, s3b, s14a, s14b):
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s3a) == pu.rgfs.RestrictedGrowthFunctionSequence(*s3a)
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s14a) == pu.rgfs.RestrictedGrowthFunctionSequence(*s14a)

    def test_inequality(self, s3a, s3b, s14a, s14b):
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s3a) != pu.rgfs.RestrictedGrowthFunctionSequence(*s14a)
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s14a) != pu.rgfs.RestrictedGrowthFunctionSequence(*s3a)

    def test_cache(self, s3a, s3b, s14a, s14b):
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s3a) is pu.rgfs.RestrictedGrowthFunctionSequence(*s3a)
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s14a) is pu.rgfs.RestrictedGrowthFunctionSequence(*s14a)
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s3a) is not pu.rgfs.RestrictedGrowthFunctionSequence(*s14a)
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s14a) is not pu.rgfs.RestrictedGrowthFunctionSequence(*s3a)

    def test_conversion_from_arbitrary_sequence(self):
        assert pu.rgfs.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (0, 1, 2,)) == pu.rgfs.RestrictedGrowthFunctionSequence(0, 1, 2)
        assert pu.rgfs.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (2, 1, 0,)) == pu.rgfs.RestrictedGrowthFunctionSequence(0, 1, 2)
        assert pu.rgfs.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (2, 4, 4, 9, 0, 2, 2, 0,)) == pu.rgfs.RestrictedGrowthFunctionSequence(0, 1, 1, 2, 3, 0, 0, 3)

    def test_max_value(self, rgf1, rgf2a, rgf2b, rgf6a, rgf12a):
        assert rgf1.max_value == 0
        assert rgf2a.max_value == 0
        assert rgf2b.max_value == 1
        assert rgf6a.max_value == 5
        assert rgf12a.max_value == 11

    def test_is_restricted_growth_function_sequence_equivalent_to(self, rgf1, rgf2a, rgf2b, rgf6a, rgf12a):
        assert rgf1.is_restricted_growth_function_sequence_equivalent_to(rgf1)
        assert rgf2a.is_restricted_growth_function_sequence_equivalent_to(rgf2a)
        assert rgf2b.is_restricted_growth_function_sequence_equivalent_to(rgf2b)
        assert rgf6a.is_restricted_growth_function_sequence_equivalent_to(rgf6a)
        assert rgf12a.is_restricted_growth_function_sequence_equivalent_to(rgf12a)

        assert not rgf1.is_restricted_growth_function_sequence_equivalent_to(rgf2a)
        assert not rgf1.is_restricted_growth_function_sequence_equivalent_to(rgf2b)
        assert not rgf1.is_restricted_growth_function_sequence_equivalent_to(rgf6a)
        assert not rgf1.is_restricted_growth_function_sequence_equivalent_to(rgf12a)

        assert not rgf2a.is_restricted_growth_function_sequence_equivalent_to(rgf1)
        assert not rgf2a.is_restricted_growth_function_sequence_equivalent_to(rgf2b)
        assert not rgf2a.is_restricted_growth_function_sequence_equivalent_to(rgf6a)
        assert not rgf2a.is_restricted_growth_function_sequence_equivalent_to(rgf12a)

    def test_concatenate_single(self, rgf1, rgf2a, rgf2b, rgf6a, rgf12a):
        assert rgf1.concatenate_with(rgf2a) == pu.rgfs.RestrictedGrowthFunctionSequence(*rgf1, *rgf2a)
        assert pu.rgfs.concatenate_flexible_restricted_growth_sequences(rgf12a,
                                                                        rgf2a) == pu.rgfs.RestrictedGrowthFunctionSequence(
            *rgf12a, *rgf2a)
