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
    return pu.rpt.RootedPlaneTree()


@pytest.fixture
def t2_a_aa(t1_a):
    return pu.rpt.RootedPlaneTree(t1_a)


@pytest.fixture
def t3_a_aa_aaa(t2_a_aa):
    return pu.t_rpt.RootedPlaneTree(t2_a_aa)


@pytest.fixture
def t3_a_aa_ab(t1_a):
    return pu.rpt.RootedPlaneTree(t1_a, t1_a)


@pytest.fixture
def t7_a_aa_ab_aaa_aaaa_aba_abaa(t3_a_aa_ab):
    return pu.rpt.RootedPlaneTree(t3_a_aa_ab, t3_a_aa_ab)


@pytest.fixture
def t6_a_aa_ab_ac_ad_ae(t1_a):
    return pu.rpt.RootedPlaneTree(t1_a, t1_a, t1_a, t1_a, t1_a)


@pytest.fixture
def t12(t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae):
    return pu.rpt.RootedPlaneTree(t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t2_a_aa)


@pytest.fixture
def t_big(t1_a, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12):
    return pu.rpt.RootedPlaneTree(t12, t2_a_aa, t6_a_aa_ab_ac_ad_ae, t12, t2_a_aa)


@pytest.fixture
def us0(s0):
    return pu.sl.UnrestrictedSequence(*s0)


@pytest.fixture
def us00(s00):
    return pu.sl.UnrestrictedSequence(*s00)


@pytest.fixture
def us01(s01):
    return pu.sl.UnrestrictedSequence(*s01)


@pytest.fixture
def us10(s10):
    return pu.sl.UnrestrictedSequence(*s10)


@pytest.fixture
def us012345():
    return pu.sl.UnrestrictedSequence(0, 1, 2, 3, 4, 5, )


@pytest.fixture
def us746107():
    return pu.sl.UnrestrictedSequence(7, 4, 6, 1, 0, 7, )


@pytest.fixture
def us0123456789_10_11():
    return pu.sl.UnrestrictedSequence(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, )


@pytest.fixture
def rgfs0(s0):
    return pu.sl.RestrictedGrowthFunctionSequence(*s0)


@pytest.fixture
def rgfs00(s00):
    return pu.sl.RestrictedGrowthFunctionSequence(*s00)


@pytest.fixture
def rgfs01(s01):
    return pu.sl.RestrictedGrowthFunctionSequence(*s01)


@pytest.fixture
def rgfs012345():
    return pu.sl.RestrictedGrowthFunctionSequence(0, 1, 2, 3, 4, 5, )


@pytest.fixture
def rgfs0123456789_10_11():
    return pu.sl.RestrictedGrowthFunctionSequence(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, )


@pytest.fixture
def caf1(t1_a, rgfs0):
    return pu.afl.CanonicalAbstractFormula(t1_a, rgfs0)


@pytest.fixture
def caf2a(t2_a_aa, rgfs00):
    return pu.afl.CanonicalAbstractFormula(t2_a_aa, rgfs00)


@pytest.fixture
def caf2b(t2_a_aa, rgfs01):
    return pu.afl.CanonicalAbstractFormula(t2_a_aa, rgfs01)


@pytest.fixture
def caf3a(t3_a_aa_aaa, rgf3a):
    return pu.afl.CanonicalAbstractFormula(t3_a_aa_aaa, rgf3a)


@pytest.fixture
def caf6a(t6_a_aa_ab_ac_ad_ae, rgfs012345):
    return pu.afl.CanonicalAbstractFormula(t6_a_aa_ab_ac_ad_ae, rgfs012345)


@pytest.fixture
def caf12a(t12, rgfs0123456789_10_11):
    return pu.afl.CanonicalAbstractFormula(t12, rgfs0123456789_10_11)


@pytest.fixture
def caf_big(t_big):
    return pu.afl.CanonicalAbstractFormula(t_big,
                                           (0, 1, 2, 0, 2, 0, 3, 0, 1, 2, 4, 5, 2, 4, 3, 6, 0, 7, 0, 8, 5, 4, 3, 2, 1,
                                            4,
                                            9, 10,
                                            7, 7, 7, 9, 0, 11, 12,))


@pytest.fixture
def ncaf1(t1_a, rgfs0):
    return pu.afl.NonCanonicalAbstractFormula(t1_a, rgfs0)


@pytest.fixture
def ncaf2a(t2_a_aa, rgfs00):
    return pu.afl.NonCanonicalAbstractFormula(t2_a_aa, rgfs00)


@pytest.fixture
def ncaf2b(t2_a_aa, rgfs01):
    return pu.afl.NonCanonicalAbstractFormula(t2_a_aa, rgfs01)


@pytest.fixture
def ncaf3a(t3_a_aa_aaa, rgf3a):
    return pu.afl.NonCanonicalAbstractFormula(t3_a_aa_aaa, rgf3a)


@pytest.fixture
def ncaf6a(t6_a_aa_ab_ac_ad_ae, rgfs012345):
    return pu.afl.NonCanonicalAbstractFormula(t6_a_aa_ab_ac_ad_ae, rgfs012345)


@pytest.fixture
def ncaf12a(t12, rgfs0123456789_10_11):
    return pu.afl.NonCanonicalAbstractFormula(t12, rgfs0123456789_10_11)


@pytest.fixture
def ncaf_big(t_big):
    return pu.afl.CanonicalAbstractFormula(t_big,
                                           (0, 1, 2, 0, 2, 0, 3, 0, 1, 2, 4, 5, 2, 4, 3, 6, 0, 7, 0, 8, 5, 4, 3, 2, 1,
                                            4,
                                            9, 10,
                                            7, 7, 7, 9, 0, 11, 12,))


@pytest.fixture
def phi1a(caf1):
    """The formula 1.

    :param af1:
    :return:
    """
    return pu.formula.Formula(caf1, (pu.connective_library.one,), )


@pytest.fixture
def phi2a(caf2a):
    """The formula: 1(1).

    :param af2a:
    :return:
    """
    return pu.formula.Formula(caf2a, (pu.connective_library.one,), )


@pytest.fixture
def phi2b(caf2b):
    """The formula: -1.

    :param af2b:
    :return:
    """
    return pu.formula.Formula(caf2b, (pu.connective_library.minus, pu.connective_library.one,), )


@pytest.fixture
def phi6a(caf6a):
    """set(1, 2, 3, 4, 5)

    :param af6a:
    :return:
    """
    return pu.formula.Formula(caf6a,
                              (pu.connective_library.set_by_extension, pu.connective_library.one,
                               pu.connective_library.two,
                               pu.connective_library.three,
                               pu.connective_library.four,
                               pu.connective_library.five,), )
