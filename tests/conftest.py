import pytest

import punctilious as pu


# raw sequences


@pytest.fixture
def s0():
    return (0,)


@pytest.fixture
def s1():
    return (1,)


@pytest.fixture
def s2():
    return (2,)


@pytest.fixture
def s3():
    return (3,)


@pytest.fixture
def s4():
    return (4,)


@pytest.fixture
def s5():
    return (5,)


@pytest.fixture
def s00():
    return 0, 0,


@pytest.fixture
def s01():
    return 0, 1,


@pytest.fixture
def s10():
    return 1, 0,


@pytest.fixture
def s012():
    return 0, 1, 2,


@pytest.fixture
def s021():
    return 0, 2, 1,


@pytest.fixture
def s00010203043212():
    return 0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 3, 2, 1, 2,


@pytest.fixture
def s00010203043262():
    return 0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 3, 2, 6, 2,


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
def nns0(s0):
    return pu.sl.NaturalNumberSequence(*s0)


@pytest.fixture
def nns1(s1):
    return pu.sl.NaturalNumberSequence(*s1)


@pytest.fixture
def nns00(s00):
    return pu.sl.NaturalNumberSequence(*s00)


@pytest.fixture
def nns01(s01):
    return pu.sl.NaturalNumberSequence(*s01)


@pytest.fixture
def nns10(s10):
    return pu.sl.NaturalNumberSequence(*s10)


@pytest.fixture
def nns000(s00):
    return pu.sl.NaturalNumberSequence(*s00)


@pytest.fixture
def nns012345():
    return pu.sl.NaturalNumberSequence(0, 1, 2, 3, 4, 5, )


@pytest.fixture
def nns746107():
    return pu.sl.NaturalNumberSequence(7, 4, 6, 1, 0, 7, )


@pytest.fixture
def nns0123456789_10_11():
    return pu.sl.NaturalNumberSequence(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, )


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
def af3a(t3_a_aa_aaa, nns3a):
    return pu.afl.AbstractFormula(t3_a_aa_aaa, nns3a)


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
