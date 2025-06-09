import pytest

import punctilious as pu


@pytest.fixture
def s3a():
    return (1, 2, 3,)


@pytest.fixture
def s3b():
    return (1, 3, 2,)


@pytest.fixture
def s14a():
    return (1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 4, 3, 2, 3,)


@pytest.fixture
def s14b():
    return (1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 4, 3, 7, 3,)


@pytest.fixture
def rpt1():
    return pu.rpt.RootedPlaneTree()


@pytest.fixture
def rpt2(rpt1):
    return pu.rpt.RootedPlaneTree(rpt1)


@pytest.fixture
def rpt6a(rpt1):
    return pu.rpt.RootedPlaneTree(rpt1, rpt1, rpt1, rpt1, rpt1)


@pytest.fixture
def rpt12a(rpt1, rpt2, rpt6a):
    return pu.rpt.RootedPlaneTree(rpt1, rpt2, rpt6a, rpt2)


@pytest.fixture
def rgf1():
    return pu.rgf.RestrictedGrowthFunctionSequence(1, )


@pytest.fixture
def rgf2a():
    return pu.rgf.RestrictedGrowthFunctionSequence(1, 1, )


@pytest.fixture
def rgf2b():
    return pu.rgf.RestrictedGrowthFunctionSequence(1, 2, )


@pytest.fixture
def rgf6a():
    return pu.rgf.RestrictedGrowthFunctionSequence(1, 2, 3, 4, 5, 6, )


@pytest.fixture
def rgf12a():
    return pu.rgf.RestrictedGrowthFunctionSequence(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, )


@pytest.fixture
def af1(rpt1, rgf1):
    return pu.af.AbstractFormula(rpt1, rgf1)


@pytest.fixture
def af2a(rpt2, rgf2a):
    return pu.af.AbstractFormula(rpt2, rgf2a)


@pytest.fixture
def af2b(rpt2, rgf2b):
    return pu.af.AbstractFormula(rpt2, rgf2b)


@pytest.fixture
def af6a(rpt6a, rgf6a):
    return pu.af.AbstractFormula(rpt6a, rgf6a)


@pytest.fixture
def af4(rpt12a, rgf12a):
    return pu.af.AbstractFormula(rpt12a, rgf12a)
