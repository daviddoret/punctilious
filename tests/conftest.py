import pytest

import punctilious as pu


# raw sequences


@pytest.fixture
def raw_1():
    return (1,)


@pytest.fixture
def raw_2():
    return (2,)


@pytest.fixture
def raw_3():
    return (3,)


@pytest.fixture
def raw_4():
    return (4,)


@pytest.fixture
def raw_5():
    return (5,)


@pytest.fixture
def raw_6():
    return (6,)


@pytest.fixture
def raw_1_1():
    return 1, 1,


@pytest.fixture
def raw_1_2():
    return 1, 2,


@pytest.fixture
def raw_2_1():
    return 2, 1,


@pytest.fixture
def raw_1_2_3():
    return 1, 2, 3,


@pytest.fixture
def raw_1_3_2():
    return 1, 3, 2,


@pytest.fixture
def raw_00010203043212():
    return 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 4, 3, 2, 3,


@pytest.fixture
def raw_00010203043262():
    return 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 4, 3, 7, 3,


# rooted plane trees

@pytest.fixture
def t1_a():
    return pu.rptl.RootedPlaneTree()


@pytest.fixture
def t2_a_aa(t1_a):
    return pu.rptl.RootedPlaneTree(t1_a)


@pytest.fixture
def t3_a_aa_aaa(t2_a_aa):
    return pu.rptl.RootedPlaneTree(t2_a_aa)


@pytest.fixture
def t3_a_aa_ab(t1_a):
    return pu.rptl.RootedPlaneTree(t1_a, t1_a)


@pytest.fixture
def t6_a_aa_ab_ac_ad_ae(t1_a):
    return pu.rptl.RootedPlaneTree(t1_a, t1_a, t1_a, t1_a, t1_a)


@pytest.fixture
def t7_a_aa_ab_aaa_aaaa_aba_abaa(t3_a_aa_ab):
    return pu.rptl.RootedPlaneTree(t3_a_aa_ab, t3_a_aa_ab)


@pytest.fixture
def t12(t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae):
    return pu.rptl.RootedPlaneTree(t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa)


@pytest.fixture
def t_big(t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
    return pu.rptl.RootedPlaneTree(t12, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12, t2_a_aa)


@pytest.fixture
def nns0(raw_1):
    return pu.nn0sl.NaturalNumber0Sequence(*raw_1)


@pytest.fixture
def nns1(raw_2):
    return pu.nn0sl.NaturalNumber0Sequence(*raw_2)


@pytest.fixture
def nns00(raw_1_1):
    return pu.nn0sl.NaturalNumber0Sequence(*raw_1_1)


@pytest.fixture
def nns01(raw_1_2):
    return pu.nn0sl.NaturalNumber0Sequence(*raw_1_2)


@pytest.fixture
def nns10(raw_2_1):
    return pu.nn0sl.NaturalNumber0Sequence(*raw_2_1)


@pytest.fixture
def nns000(raw_1_1):
    return pu.nn0sl.NaturalNumber0Sequence(*raw_1_1)


@pytest.fixture
def nns001(raw_1_1):
    return pu.nn0sl.NaturalNumber0Sequence(1, 1, 2, )


@pytest.fixture
def nns012345():
    return pu.nn0sl.NaturalNumber0Sequence(1, 2, 3, 4, 5, 6, )


@pytest.fixture
def nns746107():
    return pu.nn0sl.NaturalNumber0Sequence(8, 5, 7, 2, 1, 8, )


@pytest.fixture
def nns0123456789_10_11():
    return pu.nn0sl.NaturalNumber0Sequence(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, )


@pytest.fixture
def af1(t1_a, nns0):
    return pu.afl.AbstractFormula(t1_a, nns0)


@pytest.fixture
def af1b(t1_a, nns1):
    return pu.afl.AbstractFormula(t1_a, nns1)


@pytest.fixture
def af2a(t2_a_aa, nns00):
    return pu.afl.AbstractFormula(t2_a_aa, nns00)


@pytest.fixture
def af2b(t2_a_aa, nns01):
    return pu.afl.AbstractFormula(t2_a_aa, nns01)


@pytest.fixture
def af3a(t3_a_aa_aaa, nns001):
    return pu.afl.AbstractFormula(t3_a_aa_aaa, nns001)


@pytest.fixture
def af6a(t6_a_aa_ab_ac_ad_ae, nns012345):
    return pu.afl.AbstractFormula(t6_a_aa_ab_ac_ad_ae, nns012345)


@pytest.fixture
def af12a(t12, nns0123456789_10_11):
    return pu.afl.AbstractFormula(t12, nns0123456789_10_11)


@pytest.fixture
def af_big(t_big):
    return pu.afl.AbstractFormula(t_big,
                                  (0, 1, 2, 0, 2, 0, 3, 0, 1, 2, 4, 5, 2, 4, 3, 6, 0, 7, 0, 8, 5, 4, 3, 2, 1,
                                   4,
                                   9, 10,
                                   7, 7, 7, 9, 0, 11, 12,))


@pytest.fixture
def phi1a(af1):
    """The formula 1.

    :param af1:
    :return:
    """
    return pu.fl.Formula(af1, (pu.cc.one,), )


@pytest.fixture
def phi2a(af2a):
    """The formula: 1(1).

    :param af2a:
    :return:
    """
    return pu.fl.Formula(af2a, (pu.cc.one,), )


@pytest.fixture
def phi2b(af2b):
    """The formula: -1.

    :param af2b:
    :return:
    """
    return pu.fl.Formula(af2b, (pu.cc.minus, pu.cc.one,), )


@pytest.fixture
def phi6a(af6a):
    """set(1, 2, 3, 4, 5)

    :param af6a:
    :return:
    """
    return pu.fl.Formula(af6a,
                         (pu.cc.set_by_extension, pu.cc.one,
                          pu.cc.two,
                          pu.cc.three,
                          pu.cc.four,
                          pu.cc.five,), )
