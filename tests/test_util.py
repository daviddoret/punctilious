import punctilious as pu


class TestDeduplicateIntegerSequence:
    def test_deduplicate_integer_sequence(self):
        assert pu.util.deduplicate_integer_sequence(()) == ()
        assert pu.util.deduplicate_integer_sequence((1, 2, 3,)) == (1, 2, 3,)
        assert pu.util.deduplicate_integer_sequence((5, 7, 1, 5, 2, 6, 6, 7, 4, 3, 0,)) == (5, 7, 1, 2, 6, 4, 3, 0)

    def test_decrement_last_element(self):
        assert pu.util.decrement_last_element((0, 0, 0, 1,)) == (0, 0, 0, 0,)
        assert pu.util.decrement_last_element((4, 3, 2,)) == (4, 3, 1,)
        assert pu.util.decrement_last_element((1,)) == (0,)

    def test_increment_last_element(self):
        assert pu.util.increment_last_element((0, 0, 0, 0,)) == (0, 0, 0, 1,)
        assert pu.util.increment_last_element((4, 3, 2,)) == (4, 3, 3,)
        assert pu.util.increment_last_element((0,)) == (1,)
        assert pu.util.increment_last_element((1,)) == (2,)
