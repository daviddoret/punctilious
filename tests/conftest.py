import pytest
from astroid.protocols import sequence_assigned_stmts

import punctilious as pu


# raw sequences

@pytest.fixture
def raw_0():
    return (0,)


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
def lrpt1(t1_a, nns0):
    return pu.lrptl.LabeledRootedPlaneTree.from_rpt_and_sequence(rpt=t1_a, sequence=nns0)


@pytest.fixture
def lrpt2(t1_a, nns1):
    return pu.lrptl.LabeledRootedPlaneTree.from_rpt_and_sequence(rpt=t1_a, sequence=nns1)


@pytest.fixture
def lrpt3(t2_a_aa, nns00):
    return pu.lrptl.LabeledRootedPlaneTree.from_rpt_and_sequence(rpt=t2_a_aa, sequence=nns00)


@pytest.fixture
def lrpt4(t2_a_aa, nns01):
    return pu.lrptl.LabeledRootedPlaneTree.from_rpt_and_sequence(rpt=t2_a_aa, sequence=nns01)


@pytest.fixture
def lrpt5(t3_a_aa_aaa, nns001):
    return pu.lrptl.LabeledRootedPlaneTree.from_rpt_and_sequence(rpt=t3_a_aa_aaa, sequence=nns001)


@pytest.fixture
def lrpt6(t6_a_aa_ab_ac_ad_ae, nns012345):
    return pu.lrptl.LabeledRootedPlaneTree.from_rpt_and_sequence(rpt=t6_a_aa_ab_ac_ad_ae, sequence=nns012345)


@pytest.fixture
def lrpt7(t12, nns0123456789_10_11):
    return pu.lrptl.LabeledRootedPlaneTree.from_rpt_and_sequence(rpt=t12, sequence=nns0123456789_10_11)


@pytest.fixture
def lrpt8(t_big):
    return pu.lrptl.LabeledRootedPlaneTree.from_rpt_and_sequence(rpt=t_big, sequence=
    (0, 1, 2, 0, 2, 0, 3, 0, 1, 2, 4, 5, 2, 4, 3, 6, 0, 7, 0, 8, 5, 4, 3, 2, 1,
     4,
     9, 10,
     7, 7, 7, 9, 0, 11, 12,))


@pytest.fixture
def phi1a(lrpt1):
    """The formula 1.

    :param af1:
    :return:
    """
    return pu.fl.Formula(lrpt1, (pu.cc.one,), )


@pytest.fixture
def phi2a(lrpt3):
    """The formula: 1(1).

    :param af2a:
    :return:
    """
    return pu.fl.Formula(lrpt3, (pu.cc.one,), )


@pytest.fixture
def phi2b(lrpt4):
    """The formula: -1.

    :param af2b:
    :return:
    """
    return pu.fl.Formula(lrpt4, (pu.cc.minus, pu.cc.one,), )


@pytest.fixture
def phi6a(lrpt6):
    """set(1, 2, 3, 4, 5)

    :param af6a:
    :return:
    """
    return pu.fl.Formula(lrpt6,
                         (pu.cc.set_by_extension, pu.cc.one,
                          pu.cc.two,
                          pu.cc.three,
                          pu.cc.four,
                          pu.cc.five,), )
