import punctilious as pu


class TestBellNumber:
    def test_get_bell_number(self):
        assert pu.bell_number_library.get_bell_number(0) == 1
        assert pu.bell_number_library.get_bell_number(1) == 1
        assert pu.bell_number_library.get_bell_number(2) == 2
        assert pu.bell_number_library.get_bell_number(3) == 5
        assert pu.bell_number_library.get_bell_number(4) == 15
        assert pu.bell_number_library.get_bell_number(5) == 52
        assert pu.bell_number_library.get_bell_number(6) == 203
        assert pu.bell_number_library.get_bell_number(7) == 877
        assert pu.bell_number_library.get_bell_number(8) == 4140
        assert pu.bell_number_library.get_bell_number(9) == 21147
        assert pu.bell_number_library.get_bell_number(10) == 115975
        assert pu.bell_number_library.get_bell_number(11) == 678570
        assert pu.bell_number_library.get_bell_number(12) == 4213597
