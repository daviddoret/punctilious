import punctilious.pu_01_utilities as _utilities
import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_03_representation as _representation
import punctilious.pu_04_formal_language as _formal_language
import punctilious.pu_05_fundamental_connectors as _fundamental_connectors


class Tuple(_formal_language.Formula):
    """A Tuple is a Formula whose connector is the `tuple` connector.
    """

    def __init__(self, *a):
        super().__init__(c=_fundamental_connectors.tuple2, a=a)


class ExtensionSet(_formal_language.Formula):
    """An ExtensionSet is a Tuple where all arguments are unique.
    """

    def __init__(self, *a):
        # check that all arguments are unique.

        super().__init__(c=_fundamental_connectors.tuple2, a=a)


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
        super().__init__(c=_fundamental_connectors.tuple2, a=(d, c,))
        self._vertical_map = _utilities.get_empty_dict()
