import pytest

import punctilious as pu


@pytest.fixture
def rpt1():
    return pu.rpt.RootedPlaneTree()


@pytest.fixture
def rpt2(rpt1):
    return pu.rpt.RootedPlaneTree(rpt1)


@pytest.fixture
def rpt3(rpt1):
    return pu.rpt.RootedPlaneTree(rpt1, rpt1, rpt1, rpt1, rpt1)


@pytest.fixture
def rpt4(rpt1, rpt2, rpt3):
    return pu.rpt.RootedPlaneTree(rpt1, rpt2, rpt3, rpt2)


@pytest.fixture
def rgf1():
    return pu.rgf.RestrictedGrowthFunctionSequence(1, )


@pytest.fixture
def rgf2():
    return pu.rgf.RestrictedGrowthFunctionSequence(1, 1, )


@pytest.fixture
def rgf3():
    return pu.rgf.RestrictedGrowthFunctionSequence(1, 2, )


@pytest.fixture
def s1():
    return (1, 2, 3,)


@pytest.fixture
def s2():
    return (1, 3, 2,)


@pytest.fixture
def s3():
    return (1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 4, 3, 2, 3,)


@pytest.fixture
def s4():
    return (1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 4, 3, 7, 3,)


@pytest.fixture
def af1(rpt1, rgf1):
    return pu.af.AbstractFormula(rpt1, rgf1)


@pytest.fixture
def af2(rpt2, rgf2):
    return pu.af.AbstractFormula(rpt2, rgf2)


@pytest.fixture
def af3(rpt2, rgf3):
    return pu.af.AbstractFormula(rpt2, rgf3)
