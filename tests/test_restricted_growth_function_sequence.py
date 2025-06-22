import pytest

import punctilious as pu


class TestRestrictedGrowthFunctionSequence:
    def test_data_validation(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.rgfs.data_validate_restricted_growth_function_sequence_elements(s012) == s012
        assert pu.rgfs.data_validate_restricted_growth_function_sequence_elements(s00010203043212) == s00010203043212
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgfs.data_validate_restricted_growth_function_sequence_elements(s021)
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgfs.data_validate_restricted_growth_function_sequence_elements(s00010203043262)

    def test_data_validation_in_construction(self, s012, s021, s00010203043212, s00010203043262):
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgfs.RestrictedGrowthFunctionSequence(*s021)
        with pytest.raises(pu.util.PunctiliousException):
            pu.rgfs.RestrictedGrowthFunctionSequence(*s00010203043262)

    def test_equality(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s012) == pu.rgfs.RestrictedGrowthFunctionSequence(*s012)
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s00010203043212) == pu.rgfs.RestrictedGrowthFunctionSequence(
            *s00010203043212)

    def test_inequality(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s012) != pu.rgfs.RestrictedGrowthFunctionSequence(
            *s00010203043212)
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s00010203043212) != pu.rgfs.RestrictedGrowthFunctionSequence(
            *s012)

    def test_cache(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s012) is pu.rgfs.RestrictedGrowthFunctionSequence(*s012)
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s00010203043212) is pu.rgfs.RestrictedGrowthFunctionSequence(
            *s00010203043212)
        assert pu.rgfs.RestrictedGrowthFunctionSequence(*s012) is not pu.rgfs.RestrictedGrowthFunctionSequence(
            *s00010203043212)
        assert pu.rgfs.RestrictedGrowthFunctionSequence(
            *s00010203043212) is not pu.rgfs.RestrictedGrowthFunctionSequence(*s012)

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
        assert pu.rgfs.concatenate_flexible_restricted_growth_function_sequences(rgf12a,
                                                                                 rgf2a) == pu.rgfs.RestrictedGrowthFunctionSequence(
            *rgf12a, *rgf2a)
