import punctilious.pu_01_utilities as _utilities
import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_03_representation as _representation
import punctilious.pu_04_formal_language as _formal_language
import punctilious.pu_05_foundational_connectors as _foundational_connectors


class Tuple(_formal_language.Formula):
    """A Tuple is a Formula whose connector is the `tuple` connector.
    """

    def __init__(self, *a):
        super().__init__(c=_foundational_connectors.tuple2, a=a)


class SetDefinedByExtension(_formal_language.Formula):
    """A SetDefinedByExtension is a formula where all arguments are denoted as elements and are unique.
    """

    def __init__(self, *a):
        # check that all arguments are unique.
        n = len(a)
        for i in range(n):
            for j in range(i + 1, n):
                if _formal_language.is_formula_equivalent(phi=a[i], psi=a[j]):
                    raise ValueError(f'Arguments must be unique. a[{i}]={a[i]}, a[{j}]={a[j]}.')
        super().__init__(c=_foundational_connectors.set_defined_by_extension, a=a)

    def __new__(cls, *a):
        return super().__new__(cls, c=_foundational_connectors.set_defined_by_extension, a=a)


def ensure_set_defined_by_extension(o):
    """Ensures that the input is a SetDefinedByExtension.

    Args:
        o: an object

    Returns:
        SetDefinedByExtension: the input as an ExtensionSet

    Raises:
        ValueError: if the input is not an ExtensionSet
    """
    if isinstance(o, SetDefinedByExtension):
        return o
    if isinstance(o, _formal_language.Formula):
        if o.connector == _foundational_connectors.set_defined_by_extension:
            pass
            return SetDefinedByExtension(*o.arguments)
    raise ValueError(f'Expected an ExtensionSet. o={o}. type={type(o).__name__}')


class VerticalMap(_formal_language.Formula):
    """A vertical map is a tuple of the form:
        (D, C)
    where:
     - D is tuple denoted as the domain,
     - C is tuple denoted as the codomain,
     - the arity of D and C are equal,
     - elements in D are unique.
    """

    def __init__(self, d, c):
        super().__init__(c=_foundational_connectors.tuple2, a=(d, c,))
        self._vertical_map = _utilities.get_empty_dict()
