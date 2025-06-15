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
def rpt3a(rpt2):
    return pu.rpt.RootedPlaneTree(rpt2)


@pytest.fixture
def rpt3b(rpt1):
    return pu.rpt.RootedPlaneTree(rpt1, rpt1)


@pytest.fixture
def rpt7a(rpt3b):
    return pu.rpt.RootedPlaneTree(rpt3b, rpt3b)


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
def af12a(rpt12a, rgf12a):
    return pu.af.AbstractFormula(rpt12a, rgf12a)


@pytest.fixture
def phi1(af1):
    """1

    :param af1:
    :return:
    """
    return pu.formula.Formula((pu.connective_library.one,), af1)


@pytest.fixture
def phi2a(af2a):
    """1(1)

    :param af2a:
    :return:
    """
    return pu.formula.Formula((pu.connective_library.one,), af2a)


@pytest.fixture
def phi2b(af2b):
    """1(2)

    :param af2b:
    :return:
    """
    return pu.formula.Formula((pu.connective_library.minus, pu.connective_library.one,), af2b)


@pytest.fixture
def phi6a(af6a):
    """set(1, 2, 3, 4, 5)

    :param af6a:
    :return:
    """
    return pu.formula.Formula(
        (pu.connective_library.set_by_extension, pu.connective_library.one, pu.connective_library.two,
         pu.connective_library.three,
         pu.connective_library.four,
         pu.connective_library.five,), af6a)
