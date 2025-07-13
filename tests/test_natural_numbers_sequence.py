import punctilious as pu


class TestNaturalNumbersSequence:
    def test_data_validation(self, s10, s012, s021, s00010203043212, s00010203043262):
        assert pu.nnsl.NaturalNumberSequence.data_validate_elements(s10)[1] == s10
        assert pu.nnsl.NaturalNumberSequence.data_validate_elements(s012)[1] == s012
        assert pu.nnsl.NaturalNumberSequence.data_validate_elements(s00010203043212)[1] == s00010203043212
        assert pu.nnsl.NaturalNumberSequence.data_validate_elements(s021)[1] == s021
        assert pu.nnsl.NaturalNumberSequence.data_validate_elements(s00010203043262)[1] == s00010203043262

    def test_equality(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.nnsl.NaturalNumberSequence(*s012) == pu.nnsl.NaturalNumberSequence(*s012)
        assert pu.nnsl.NaturalNumberSequence(*s00010203043212) == pu.nnsl.NaturalNumberSequence(
            *s00010203043212)

    def test_inequality(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.nnsl.NaturalNumberSequence(*s012) != pu.nnsl.NaturalNumberSequence(
            *s00010203043212)
        assert pu.nnsl.NaturalNumberSequence(*s00010203043212) != pu.nnsl.NaturalNumberSequence(
            *s012)

    def test_cache(self, s012, s021, s00010203043212, s00010203043262):
        assert pu.nnsl.NaturalNumberSequence(*s012) is pu.nnsl.NaturalNumberSequence(*s012)
        assert pu.nnsl.NaturalNumberSequence(*s00010203043212) is pu.nnsl.NaturalNumberSequence(
            *s00010203043212)
        assert pu.nnsl.NaturalNumberSequence(*s012) is not pu.nnsl.NaturalNumberSequence(
            *s00010203043212)
        assert pu.nnsl.NaturalNumberSequence(
            *s00010203043212) is not pu.nnsl.NaturalNumberSequence(*s012)

    def test_max_value(self, nns0, nns00, nns01, nns012345, nns0123456789_10_11):
        assert nns0.max_value == 1
        assert nns00.max_value == 1
        assert nns01.max_value == 2
        assert nns012345.max_value == 6
        assert nns0123456789_10_11.max_value == 12

    def test_is_natural_numbers_sequence_equivalent_to(self, nns0, nns00, nns01, nns10, nns012345, nns746107,
                                                       nns0123456789_10_11):
        assert nns0.is_natural_number_sequence_equivalent_to(nns0)
        assert nns00.is_natural_number_sequence_equivalent_to(nns00)
        assert nns01.is_natural_number_sequence_equivalent_to(nns01)
        assert nns10.is_natural_number_sequence_equivalent_to(nns10)
        assert nns012345.is_natural_number_sequence_equivalent_to(nns012345)
        assert nns746107.is_natural_number_sequence_equivalent_to(nns746107)
        assert nns0123456789_10_11.is_natural_number_sequence_equivalent_to(nns0123456789_10_11)

        assert not nns0.is_natural_number_sequence_equivalent_to(nns00)
        assert not nns0.is_natural_number_sequence_equivalent_to(nns01)
        assert not nns0.is_natural_number_sequence_equivalent_to(nns10)
        assert not nns0.is_natural_number_sequence_equivalent_to(nns012345)
        assert not nns0.is_natural_number_sequence_equivalent_to(nns746107)
        assert not nns0.is_natural_number_sequence_equivalent_to(nns0123456789_10_11)

        assert not nns00.is_natural_number_sequence_equivalent_to(nns0)
        assert not nns00.is_natural_number_sequence_equivalent_to(nns01)
        assert not nns00.is_natural_number_sequence_equivalent_to(nns10)
        assert not nns00.is_natural_number_sequence_equivalent_to(nns012345)
        assert not nns00.is_natural_number_sequence_equivalent_to(nns746107)
        assert not nns00.is_natural_number_sequence_equivalent_to(nns0123456789_10_11)

        assert not nns10.is_natural_number_sequence_equivalent_to(nns0)
        assert not nns10.is_natural_number_sequence_equivalent_to(nns00)
        assert not nns10.is_natural_number_sequence_equivalent_to(nns01)
        assert not nns10.is_natural_number_sequence_equivalent_to(nns012345)
        assert not nns10.is_natural_number_sequence_equivalent_to(nns746107)
        assert not nns10.is_natural_number_sequence_equivalent_to(nns0123456789_10_11)

    def test_concatenate_single(self, nns0, nns00, nns01, nns012345, nns0123456789_10_11):
        assert nns0.concatenate_with(nns00) == pu.nnsl.NaturalNumberSequence(*nns0, *nns00)
        assert pu.nnsl.concatenate_natural_number_sequences(nns0123456789_10_11,
                                                            nns00) == pu.nnsl.NaturalNumberSequence(
            *nns0123456789_10_11, *nns00)

    def test_is_restricted_growth_function_sequence(self):
        s = pu.nnsl.NaturalNumberSequence(1, 1, 1)
        assert s.is_restricted_growth_function_sequence
        s = pu.nnsl.NaturalNumberSequence(1, 2, 1)
        assert s.is_restricted_growth_function_sequence
        s = pu.nnsl.NaturalNumberSequence(1, 2, 3)
        assert s.is_restricted_growth_function_sequence
        s = pu.nnsl.NaturalNumberSequence(4, 3, 2)
        assert not s.is_restricted_growth_function_sequence
        s = pu.nnsl.NaturalNumberSequence(1, 3, 2)
        assert not s.is_restricted_growth_function_sequence

    def test_canonical_natural_number_sequence(self):
        s = pu.nnsl.NaturalNumberSequence(4, 3, 2)
        t = s.canonical_natural_number_sequence
        u = pu.nnsl.NaturalNumberSequence(1, 2, 3)
        assert t == u

        s = pu.nnsl.NaturalNumberSequence(1, 2, 3)
        t = s.canonical_natural_number_sequence
        assert s == t

        s = pu.nnsl.NaturalNumberSequence(1, 7, 9, 14, 14, 14, 12, 1, 3, 2, 7, 9)
        t = s.canonical_natural_number_sequence
        u = pu.nnsl.NaturalNumberSequence(1, 2, 3, 4, 4, 4, 5, 1, 6, 7, 2, 3)
        assert t == u

    def test_image(self):
        s = pu.nnsl.NaturalNumberSequence(1, 1, 1)
        assert s.image == (1,)
        s = pu.nnsl.NaturalNumberSequence(1, 2, 1)
        assert s.image == (1, 2,)
        s = pu.nnsl.NaturalNumberSequence(1, 2, 3)
        assert s.image == (1, 2, 3,)
        s = pu.nnsl.NaturalNumberSequence(1, 2, 2, 8, 3, 2, 3, 1, )
        assert s.image == (1, 2, 3, 8,)

    def test_image_cardinality(self):
        s = pu.nnsl.NaturalNumberSequence(1, 1, 1)
        assert s.image_cardinality == 1
        s = pu.nnsl.NaturalNumberSequence(1, 2, 1)
        assert s.image_cardinality == 2
        s = pu.nnsl.NaturalNumberSequence(1, 2, 3)
        assert s.image_cardinality == 3
        s = pu.nnsl.NaturalNumberSequence(1, 2, 2, 8, 3, 2, 3, 1, )
        assert s.image_cardinality == 4

    def test_concatenation(self):
        s1 = pu.nnsl.NaturalNumberSequence(1, 1, 1)
        s2 = pu.nnsl.NaturalNumberSequence(1, )
        s3 = pu.nnsl.NaturalNumberSequence(9, )
        s4 = pu.nnsl.NaturalNumberSequence(6, 7, 2, )
        assert pu.nnsl.concatenate_natural_number_sequences(s1, s2) == (1, 1, 1, 1,)
        assert pu.nnsl.concatenate_natural_number_sequences(s4, s4, s4) == (6, 7, 2, 6, 7, 2, 6, 7, 2,)
        assert pu.nnsl.concatenate_natural_number_sequences(s4, s3, s2, s1) == (6, 7, 2, 9, 1, 1, 1, 1,)

    def test_canonical_ordering(self):
        assert pu.nnsl.NaturalNumberSequence(1, 1, 1).is_less_than_under_o1(pu.nnsl.NaturalNumberSequence(1, 1, 2))
        assert pu.nnsl.NaturalNumberSequence(1, 4, 17).is_less_than_under_o1(pu.nnsl.NaturalNumberSequence(1, 5, 19))

    def test_is_increasing(self):
        s = pu.nnsl.NaturalNumberSequence(1, )
        assert s.is_increasing
        s = pu.nnsl.NaturalNumberSequence(17, )
        assert s.is_increasing
        s = pu.nnsl.NaturalNumberSequence(1, 2, 3, )
        assert s.is_increasing
        s = pu.nnsl.NaturalNumberSequence(1, 2, 2, 7, 8, 12, 2000, 2000, )
        assert s.is_increasing
        s = pu.nnsl.NaturalNumberSequence(1, 2, 1, )
        assert not s.is_increasing
        s = pu.nnsl.NaturalNumberSequence(1, 2, 2, 8, 9, 8, 2000, 2000, )
        assert not s.is_increasing

    def test_is_strictly_increasing(self):
        s = pu.nnsl.NaturalNumberSequence(1, )
        assert s.is_strictly_increasing
        s = pu.nnsl.NaturalNumberSequence(17, )
        assert s.is_strictly_increasing
        s = pu.nnsl.NaturalNumberSequence(1, 2, 3, )
        assert s.is_strictly_increasing
        s = pu.nnsl.NaturalNumberSequence(1, 2, 2, 7, 8, 12, 2000, 2001, )
        assert not s.is_strictly_increasing
        s = pu.nnsl.NaturalNumberSequence(1, 2, 1, )
        assert not s.is_strictly_increasing
        s = pu.nnsl.NaturalNumberSequence(1, 2, 6, 7, 8, 100, 2000, 2000, )
        assert not s.is_strictly_increasing
