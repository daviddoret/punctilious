import pytest

import punctilious as pu


class TestRestrictedGrowthFunctionSequence:
    def test_data_validation(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.sl.data_validate_restricted_growth_function_sequence_elements(s012) == (True, s012,)
        assert pu.sl.data_validate_restricted_growth_function_sequence_elements(s00010203043212) == (True,
                                                                                                     s00010203043212,)
        with pytest.raises(pu.util.PunctiliousException):
            pu.sl.data_validate_restricted_growth_function_sequence_elements(s021)
        with pytest.raises(pu.util.PunctiliousException):
            pu.sl.data_validate_restricted_growth_function_sequence_elements(s00010203043262)

    def test_data_validation_in_construction(self, s012, s021, s00010203043212, s00010203043262):
        with pytest.raises(pu.util.PunctiliousException):
            pu.sl.RestrictedGrowthFunctionSequence(*s021)
        with pytest.raises(pu.util.PunctiliousException):
            pu.sl.RestrictedGrowthFunctionSequence(*s00010203043262)

    def test_equality(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.sl.RestrictedGrowthFunctionSequence(*s012) == pu.sl.RestrictedGrowthFunctionSequence(*s012)
        assert pu.sl.RestrictedGrowthFunctionSequence(*s00010203043212) == pu.sl.RestrictedGrowthFunctionSequence(
            *s00010203043212)

    def test_inequality(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.sl.RestrictedGrowthFunctionSequence(*s012) != pu.sl.RestrictedGrowthFunctionSequence(
            *s00010203043212)
        assert pu.sl.RestrictedGrowthFunctionSequence(*s00010203043212) != pu.sl.RestrictedGrowthFunctionSequence(
            *s012)

    def test_cache(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.sl.RestrictedGrowthFunctionSequence(*s012) is pu.sl.RestrictedGrowthFunctionSequence(*s012)
        assert pu.sl.RestrictedGrowthFunctionSequence(*s00010203043212) is pu.sl.RestrictedGrowthFunctionSequence(
            *s00010203043212)
        assert pu.sl.RestrictedGrowthFunctionSequence(*s012) is not pu.sl.RestrictedGrowthFunctionSequence(
            *s00010203043212)
        assert pu.sl.RestrictedGrowthFunctionSequence(
            *s00010203043212) is not pu.sl.RestrictedGrowthFunctionSequence(*s012)

    def test_conversion_from_arbitrary_sequence(self):
        assert pu.sl.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (0, 1, 2,)) == pu.sl.RestrictedGrowthFunctionSequence(0, 1, 2)
        assert pu.sl.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (2, 1, 0,)) == pu.sl.RestrictedGrowthFunctionSequence(0, 1, 2)
        assert pu.sl.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
            (2, 4, 4, 9, 0, 2, 2, 0,)) == pu.sl.RestrictedGrowthFunctionSequence(0, 1, 1, 2, 3, 0, 0, 3)

    def test_max_value(self, rgfs0, rgfs00, rgfs01, rgfs012345, rgfs0123456789_10_11):
        assert rgfs0.max_value == 0
        assert rgfs00.max_value == 0
        assert rgfs01.max_value == 1
        assert rgfs012345.max_value == 5
        assert rgfs0123456789_10_11.max_value == 11

    def test_is_restricted_growth_function_sequence_equivalent_to(self, rgfs0, rgfs00, rgfs01, rgfs012345,
                                                                  rgfs0123456789_10_11):
        assert rgfs0.is_restricted_growth_function_sequence_equivalent_to(rgfs0)
        assert rgfs00.is_restricted_growth_function_sequence_equivalent_to(rgfs00)
        assert rgfs01.is_restricted_growth_function_sequence_equivalent_to(rgfs01)
        assert rgfs012345.is_restricted_growth_function_sequence_equivalent_to(rgfs012345)
        assert rgfs0123456789_10_11.is_restricted_growth_function_sequence_equivalent_to(rgfs0123456789_10_11)

        assert not rgfs0.is_restricted_growth_function_sequence_equivalent_to(rgfs00)
        assert not rgfs0.is_restricted_growth_function_sequence_equivalent_to(rgfs01)
        assert not rgfs0.is_restricted_growth_function_sequence_equivalent_to(rgfs012345)
        assert not rgfs0.is_restricted_growth_function_sequence_equivalent_to(rgfs0123456789_10_11)

        assert not rgfs00.is_restricted_growth_function_sequence_equivalent_to(rgfs0)
        assert not rgfs00.is_restricted_growth_function_sequence_equivalent_to(rgfs01)
        assert not rgfs00.is_restricted_growth_function_sequence_equivalent_to(rgfs012345)
        assert not rgfs00.is_restricted_growth_function_sequence_equivalent_to(rgfs0123456789_10_11)

    def test_concatenate_single(self, rgfs0, rgfs00, rgfs01, rgfs012345, rgfs0123456789_10_11):
        assert rgfs0.concatenate_with(rgfs00) == pu.sl.RestrictedGrowthFunctionSequence(*rgfs0, *rgfs00)
        assert pu.sl.concatenate_flexible_restricted_growth_function_sequences(rgfs0123456789_10_11,
                                                                               rgfs00) == pu.sl.RestrictedGrowthFunctionSequence(
            *rgfs0123456789_10_11, *rgfs00)
