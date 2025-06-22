import pytest

import punctilious as pu


class TestUnrestrictedSequence:
    def test_data_validation(self, s10, s012, s021, s00010203043212, s00010203043262):
        assert pu.us.data_validate_unrestricted_sequence_elements(s10) == s10
        assert pu.us.data_validate_unrestricted_sequence_elements(s012) == s012
        assert pu.us.data_validate_unrestricted_sequence_elements(s00010203043212) == s00010203043212
        assert pu.us.data_validate_unrestricted_sequence_elements(s021) == s021
        assert pu.us.data_validate_unrestricted_sequence_elements(s00010203043262) == s00010203043262

    def test_equality(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.us.UnrestrictedSequence(*s012) == pu.us.UnrestrictedSequence(*s012)
        assert pu.us.UnrestrictedSequence(*s00010203043212) == pu.us.UnrestrictedSequence(
            *s00010203043212)

    def test_inequality(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.us.UnrestrictedSequence(*s012) != pu.us.UnrestrictedSequence(
            *s00010203043212)
        assert pu.us.UnrestrictedSequence(*s00010203043212) != pu.us.UnrestrictedSequence(
            *s012)

    def test_cache(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.us.UnrestrictedSequence(*s012) is pu.us.UnrestrictedSequence(*s012)
        assert pu.us.UnrestrictedSequence(*s00010203043212) is pu.us.UnrestrictedSequence(
            *s00010203043212)
        assert pu.us.UnrestrictedSequence(*s012) is not pu.us.UnrestrictedSequence(
            *s00010203043212)
        assert pu.us.UnrestrictedSequence(
            *s00010203043212) is not pu.us.UnrestrictedSequence(*s012)

    def test_max_value(self, us0, us00, us01, us012345, us0123456789_10_11):
        assert us0.max_value == 0
        assert us00.max_value == 0
        assert us01.max_value == 1
        assert us012345.max_value == 5
        assert us0123456789_10_11.max_value == 11

    def test_is_unrestricted_sequence_equivalent_to(self, us0, us00, us01, us10, us012345, us746107,
                                                    us0123456789_10_11):
        assert us0.is_unrestricted_sequence_equivalent_to(us0)
        assert us00.is_unrestricted_sequence_equivalent_to(us00)
        assert us01.is_unrestricted_sequence_equivalent_to(us01)
        assert us10.is_unrestricted_sequence_equivalent_to(us10)
        assert us012345.is_unrestricted_sequence_equivalent_to(us012345)
        assert us746107.is_unrestricted_sequence_equivalent_to(us746107)
        assert us0123456789_10_11.is_unrestricted_sequence_equivalent_to(us0123456789_10_11)

        assert not us0.is_unrestricted_sequence_equivalent_to(us00)
        assert not us0.is_unrestricted_sequence_equivalent_to(us01)
        assert not us0.is_unrestricted_sequence_equivalent_to(us10)
        assert not us0.is_unrestricted_sequence_equivalent_to(us012345)
        assert not us0.is_unrestricted_sequence_equivalent_to(us746107)
        assert not us0.is_unrestricted_sequence_equivalent_to(us0123456789_10_11)

        assert not us00.is_unrestricted_sequence_equivalent_to(us0)
        assert not us00.is_unrestricted_sequence_equivalent_to(us01)
        assert not us00.is_unrestricted_sequence_equivalent_to(us10)
        assert not us00.is_unrestricted_sequence_equivalent_to(us012345)
        assert not us00.is_unrestricted_sequence_equivalent_to(us746107)
        assert not us00.is_unrestricted_sequence_equivalent_to(us0123456789_10_11)

        assert not us10.is_unrestricted_sequence_equivalent_to(us0)
        assert not us10.is_unrestricted_sequence_equivalent_to(us00)
        assert not us10.is_unrestricted_sequence_equivalent_to(us01)
        assert not us10.is_unrestricted_sequence_equivalent_to(us012345)
        assert not us10.is_unrestricted_sequence_equivalent_to(us746107)
        assert not us10.is_unrestricted_sequence_equivalent_to(us0123456789_10_11)

    def test_concatenate_single(self, us0, us00, us01, us012345, us0123456789_10_11):
        assert us0.concatenate_with(us00) == pu.us.UnrestrictedSequence(*us0, *us00)
        assert pu.us.concatenate_flexible_unrestricted_sequences(us0123456789_10_11,
                                                                 us00) == pu.us.UnrestrictedSequence(
            *us0123456789_10_11, *us00)
