import punctilious as pu


class TestDeduplicateIntegerSequence:
    def test_deduplicate_integer_sequence(self):
        assert pu.util.deduplicate_integer_sequence(()) == ()
        assert pu.util.deduplicate_integer_sequence((1, 2, 3,)) == (1, 2, 3,)
        assert pu.util.deduplicate_integer_sequence((5, 7, 1, 5, 2, 6, 6, 7, 4, 3, 0,)) == (5, 7, 1, 2, 6, 4,
                                                                                            3, 0,)
