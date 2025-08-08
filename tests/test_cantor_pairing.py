import random
import punctilious as pu


class TestCantorPairing:
    def test_cantor_pairing_and_unpairing(self):
        for i in range(0, 32):
            n = random.randint(0, 32000)
            x, y = pu.cpl.cantor_pairing_inverse(n)
            n2 = pu.cpl.cantor_pairing(x, y)
            assert n == n2

    def test_cantor_pairing_limit_cases(self):
        n = 0
        x, y = pu.cpl.cantor_pairing_inverse(n)
        n2 = pu.cpl.cantor_pairing(x, y)
        n == n2

        n = 1
        x, y = pu.cpl.cantor_pairing_inverse(n)
        n2 = pu.cpl.cantor_pairing(x, y)
        n == n2

    def test_cantor_tupling_and_untupling_special_cases(self):

        s = ()
        n = pu.cpl.cantor_tupling_with_sentinel_value(*s)
        s2 = pu.cpl.cantor_tupling_with_sentinel_value_inverse(n)
        assert s == s2

        s = (0,)
        n = pu.cpl.cantor_tupling_with_sentinel_value(*s)
        s2 = pu.cpl.cantor_tupling_with_sentinel_value_inverse(n)
        assert s == s2

        s = (1,)
        n = pu.cpl.cantor_tupling_with_sentinel_value(*s)
        s2 = pu.cpl.cantor_tupling_with_sentinel_value_inverse(n)
        assert s == s2

        s = (35, 41,)
        n = pu.cpl.cantor_tupling_with_sentinel_value(*s)
        s2 = pu.cpl.cantor_tupling_with_sentinel_value_inverse(n)
        assert s == s2

        s = (35, 41, 12,)
        n = pu.cpl.cantor_tupling_with_sentinel_value(*s)
        s2 = pu.cpl.cantor_tupling_with_sentinel_value_inverse(n)
        assert s == s2

        s = (35, 41, 12, 71,)
        n = pu.cpl.cantor_tupling_with_sentinel_value(*s)
        s2 = pu.cpl.cantor_tupling_with_sentinel_value_inverse(n)
        assert s == s2

        s = (75, 154, 136, 227, 127)
        n = pu.cpl.cantor_tupling_with_sentinel_value(*s)
        s2 = pu.cpl.cantor_tupling_with_sentinel_value_inverse(n)
        assert s == s2

        s = (0, 1, 2, 3,)
        n = pu.cpl.cantor_tupling_with_sentinel_value(*s)
        s2 = pu.cpl.cantor_tupling_with_sentinel_value_inverse(n)
        assert s == s2

        s = (0, 0, 0, 0,)
        n = pu.cpl.cantor_tupling_with_sentinel_value(*s)
        s2 = pu.cpl.cantor_tupling_with_sentinel_value_inverse(n)
        assert s == s2

    def test_cantor_tupling_and_untupling_random_cases(self):
        for i in range(32):
            l = random.randint(0, 8)
            s = tuple(random.randint(0, 256) for x in range(l))
            n = pu.cpl.cantor_tupling_with_sentinel_value(*s)
            s2 = pu.cpl.cantor_tupling_with_sentinel_value_inverse(n)
            assert s == s2
