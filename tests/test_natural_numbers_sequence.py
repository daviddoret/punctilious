import pytest

import punctilious as pu


class TestNaturalNumbersSequence:
    def test_data_validation(self, s10, s012, s021, s00010203043212, s00010203043262):
        assert pu.sl.data_validate_natural_numbers_sequence_elements(s10) == s10
        assert pu.sl.data_validate_natural_numbers_sequence_elements(s012) == s012
        assert pu.sl.data_validate_natural_numbers_sequence_elements(s00010203043212) == s00010203043212
        assert pu.sl.data_validate_natural_numbers_sequence_elements(s021) == s021
        assert pu.sl.data_validate_natural_numbers_sequence_elements(s00010203043262) == s00010203043262

    def test_equality(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.sl.NaturalNumberSequence(*s012) == pu.sl.NaturalNumberSequence(*s012)
        assert pu.sl.NaturalNumberSequence(*s00010203043212) == pu.sl.NaturalNumberSequence(
            *s00010203043212)

    def test_inequality(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.sl.NaturalNumberSequence(*s012) != pu.sl.NaturalNumberSequence(
            *s00010203043212)
        assert pu.sl.NaturalNumberSequence(*s00010203043212) != pu.sl.NaturalNumberSequence(
            *s012)

    def test_cache(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.sl.NaturalNumberSequence(*s012) is pu.sl.NaturalNumberSequence(*s012)
        assert pu.sl.NaturalNumberSequence(*s00010203043212) is pu.sl.NaturalNumberSequence(
            *s00010203043212)
        assert pu.sl.NaturalNumberSequence(*s012) is not pu.sl.NaturalNumberSequence(
            *s00010203043212)
        assert pu.sl.NaturalNumberSequence(
            *s00010203043212) is not pu.sl.NaturalNumberSequence(*s012)

    def test_max_value(self, nns0, nns00, nns01, nns012345, nns0123456789_10_11):
        assert nns0.max_value == 0
        assert nns00.max_value == 0
        assert nns01.max_value == 1
        assert nns012345.max_value == 5
        assert nns0123456789_10_11.max_value == 11

    def test_is_natural_numbers_sequence_equivalent_to(self, nns0, nns00, nns01, nns10, nns012345, nns746107,
                                                       nns0123456789_10_11):
        assert nns0.is_natural_numbers_sequence_equivalent_to(nns0)
        assert nns00.is_natural_numbers_sequence_equivalent_to(nns00)
        assert nns01.is_natural_numbers_sequence_equivalent_to(nns01)
        assert nns10.is_natural_numbers_sequence_equivalent_to(nns10)
        assert nns012345.is_natural_numbers_sequence_equivalent_to(nns012345)
        assert nns746107.is_natural_numbers_sequence_equivalent_to(nns746107)
        assert nns0123456789_10_11.is_natural_numbers_sequence_equivalent_to(nns0123456789_10_11)

        assert not nns0.is_natural_numbers_sequence_equivalent_to(nns00)
        assert not nns0.is_natural_numbers_sequence_equivalent_to(nns01)
        assert not nns0.is_natural_numbers_sequence_equivalent_to(nns10)
        assert not nns0.is_natural_numbers_sequence_equivalent_to(nns012345)
        assert not nns0.is_natural_numbers_sequence_equivalent_to(nns746107)
        assert not nns0.is_natural_numbers_sequence_equivalent_to(nns0123456789_10_11)

        assert not nns00.is_natural_numbers_sequence_equivalent_to(nns0)
        assert not nns00.is_natural_numbers_sequence_equivalent_to(nns01)
        assert not nns00.is_natural_numbers_sequence_equivalent_to(nns10)
        assert not nns00.is_natural_numbers_sequence_equivalent_to(nns012345)
        assert not nns00.is_natural_numbers_sequence_equivalent_to(nns746107)
        assert not nns00.is_natural_numbers_sequence_equivalent_to(nns0123456789_10_11)

        assert not nns10.is_natural_numbers_sequence_equivalent_to(nns0)
        assert not nns10.is_natural_numbers_sequence_equivalent_to(nns00)
        assert not nns10.is_natural_numbers_sequence_equivalent_to(nns01)
        assert not nns10.is_natural_numbers_sequence_equivalent_to(nns012345)
        assert not nns10.is_natural_numbers_sequence_equivalent_to(nns746107)
        assert not nns10.is_natural_numbers_sequence_equivalent_to(nns0123456789_10_11)

    def test_concatenate_single(self, nns0, nns00, nns01, nns012345, nns0123456789_10_11):
        assert nns0.concatenate_with(nns00) == pu.sl.NaturalNumberSequence(*nns0, *nns00)
        assert pu.sl.concatenate_flexible_natural_numbers_sequences(nns0123456789_10_11,
                                                                    nns00) == pu.sl.NaturalNumberSequence(
            *nns0123456789_10_11, *nns00)
