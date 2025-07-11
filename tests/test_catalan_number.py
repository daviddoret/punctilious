import punctilious as pu


class TestCatalanNumber:
    def test_get_catalan_number(self):
        assert pu.catalan_number_library.get_catalan_number(0) == 1
        assert pu.catalan_number_library.get_catalan_number(1) == 1
        assert pu.catalan_number_library.get_catalan_number(2) == 2
        assert pu.catalan_number_library.get_catalan_number(3) == 5
        assert pu.catalan_number_library.get_catalan_number(4) == 14
        assert pu.catalan_number_library.get_catalan_number(5) == 42
        assert pu.catalan_number_library.get_catalan_number(6) == 132
        assert pu.catalan_number_library.get_catalan_number(7) == 429
        assert pu.catalan_number_library.get_catalan_number(8) == 1430
        assert pu.catalan_number_library.get_catalan_number(9) == 4862
        assert pu.catalan_number_library.get_catalan_number(10) == 16796
        assert pu.catalan_number_library.get_catalan_number(11) == 58786
        assert pu.catalan_number_library.get_catalan_number(12) == 208012
