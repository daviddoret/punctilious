import punctilious as pu


class TestPrimeNumber:
    def test_get_next_prime_number(self):
        s = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
             107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
             227, 229, 233, 239, 241, 251, 257, 263, 269, 271,)
        p = 1
        for n in range(len(s)):
            p = pu.pnl.get_next_prime(p)
            assert s[n] == p

    def test_factorize(self):
        assert pu.pnl.factorize(1) == (0,)
        assert pu.pnl.factorize(2) == (1,)
        assert pu.pnl.factorize(3) == (0, 1,)
        assert pu.pnl.factorize(4) == (2,)
        assert pu.pnl.factorize(5) == (0, 0, 1,)
        assert pu.pnl.factorize(6) == (1, 1,)
        assert pu.pnl.factorize(7) == (0, 0, 0, 1,)
        assert pu.pnl.factorize(8) == (3,)
        assert pu.pnl.factorize(9) == (0, 2,)
        assert pu.pnl.factorize(10) == (1, 0, 1,)
        assert pu.pnl.factorize(11) == (0, 0, 0, 0, 1,)
        assert pu.pnl.factorize(12) == (2, 1,)
        assert pu.pnl.factorize(13) == (0, 0, 0, 0, 0, 1,)
        assert pu.pnl.factorize(14) == (1, 0, 0, 1,)
        assert pu.pnl.factorize(15) == (0, 1, 1,)
