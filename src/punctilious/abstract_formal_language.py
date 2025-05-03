"""Formal language independent of any representation.

"""

# python special features
from __future__ import annotations
# python packages
import typing
import collections.abc
# external packages
# punctilious modules
import util
import const


def data_validate_connector_index(o: int) -> ConnectorIndex:
    """Performs data validation on `o`, assuring it is of type `ConnectorIndex`, applying implicit conversion if necessary.
    """
    if isinstance(o, ConnectorIndex):
        return o
    elif isinstance(o, int):
        return ConnectorIndex(o)
    else:
        raise util.PunctiliousException('`ConnectorIndex` ensurance failure. `o` is not of a supported type.', o=o)


def data_validate_connector_index_tuple(o: FlexibleConnectorIndexIterator) -> tuple[ConnectorIndex, ...]:
    """Performs data validation on `o`, assuring it is of type `tuple[ConnectorIndex]`, applying implicit conversion if necessary.

    :param o:
    :return:
    """
    if o is None:
        return tuple()
    elif isinstance(o, collections.abc.Iterable):
        return tuple(data_validate_connector_index(fp) for fp in o)
    else:
        raise util.PunctiliousException(
            'Data validation error. `o` is not implicitly convertible to `tuple[ConnectorIndex, ...]`.', o=o)


def data_validate_abstract_formula(o: FlexibleAbstractFormula) -> AbstractFormula:
    """Performs data validation on `o`, assuring it is of type `AbstractFormula`, applying implicit conversion if necessary.

    :param o:
    :return:
    """
    if isinstance(o, AbstractFormula):
        return o
    elif isinstance(o, ConnectorIndex):
        # implicit conversion of ConnectorIndex `o` to AbstractFormula o().
        return AbstractFormula(o)
    elif isinstance(o, int):
        # implicit conversion of int `o` to AbstractFormula o().
        return AbstractFormula(o)
    elif isinstance(o, tuple) and len(o) == 2:
        # implicit conversion of tuple of length 2 `o` to AbstractFormula o0(*o1).
        structure = AbstractFormula(root=o[0], terms=o[1])
        return structure
    elif isinstance(o, tuple) and len(o) == 1:
        # implicit conversion of tuple of length 1 `o` to AbstractFormula o0(*o1).
        structure = AbstractFormula(root=o[0], terms=tuple())
        return structure
    else:
        raise util.PunctiliousException('`AbstractFormula` ensurance failure. `o` is not of a supported type.', o=o,
                                        o_type=type(o).__name__)


def data_validate_formula_structure_terms(o: FlexibleAbstractFormulaTerms) -> AbstractFormulaTerms:
    """Performs data validation on `o`, assuring it is of type `AbstractFormulaTerms`, applying implicit conversion if necessary.

    :param o:
    :return:
    """
    # Logic is implemented in Terms.__new__().
    return AbstractFormulaTerms(o)


class ConnectorIndex(int):
    """A `ConnectorIndex` is a model of natural number (whose first element is mapped to 0),
    that is used as a connector index to build formula-structures.

    """

    def __str__(self):
        return f'i{self.as_int()}'

    def as_int(self) -> int:
        return int(self)

    def is_connector_index_equivalent_to(self, connector_index: FlexibleConnectorIndex) -> bool:
        """Returns `True` if `self` is connector-index-equivalent to `other`.
        Raises an exception if `other` is not a `ConnectorIndex`."""
        connector_index: ConnectorIndex = data_validate_connector_index(connector_index)
        return self is connector_index or self.as_int() == connector_index.as_int()


def data_validate_connector_index_dict(o) -> ConnectorIndexDict:
    if isinstance(o, ConnectorIndex):
        return o
    elif isinstance(o, dict):
        return ConnectorIndexDict(o)
    else:
        raise util.PunctiliousException('Data validation failure', o=o)


class ConnectorIndexDict(dict):
    """A python dictionary whose keys and values are both of type ConnectorIndex."""

    def __init__(self, initial_data=None):
        super().__init__()
        if initial_data:
            for key, value in initial_data.items():
                # key = data_validate_connector_index_dict(key)
                # value = data_validate_connector_index_dict(value)
                self[key] = value

    def __setitem__(self, key, value):
        key = data_validate_connector_index(key)
        value = data_validate_connector_index(value)
        super().__setitem__(key, value)

    def update(self, other=None, **kw):
        for key, value in kw.items():
            self[key] = value


class AbstractFormula(tuple):
    """A `AbstractFormula` is an abstract formula structure, independent of connectors.

    """

    def __init__(self, root: FlexibleConnectorIndex, terms: FlexibleAbstractFormulaTerms = tuple()):
        global _abstract_formulas
        root: ConnectorIndex = data_validate_connector_index(root)
        terms: AbstractFormulaTerms = data_validate_formula_structure_terms(terms)
        super(AbstractFormula, self).__init__()
        # `is_canonical` is cached, because this property will be pervasively necessary.
        is_canonical, _ = self.check_canonicity()
        self._is_canonical: bool = is_canonical
        connector_indexes = [self.root]
        for term in self.terms:
            for ci in term.connector_indexes:
                if ci not in connector_indexes:
                    connector_indexes.append(ci)
        connector_indexes = sorted(connector_indexes)
        self._connector_indexes: tuple[ConnectorIndex, ...] = tuple(connector_indexes)

    def __new__(cls, root: FlexibleConnectorIndex, terms: FlexibleAbstractFormulaTerms = tuple()):
        global _abstract_formulas
        root: ConnectorIndex = data_validate_connector_index(root)
        terms: AbstractFormulaTerms = data_validate_formula_structure_terms(o=terms)
        terms = super(AbstractFormula, cls).__new__(cls, (root, terms,))
        return terms

    def arity(self) -> int:
        """Returns the `arity` of the `AbstractFormula`.

        The `arity` of a `AbstractFormula` is the number of terms it contains.

        :return:
        """
        return len(self._connector_indexes)

    def check_canonicity(self, max_pointer: int | None = None) -> tuple[bool, int | None]:
        """Returns `True` if this structure participates in a canonical structure, `False` otherwise.

        :param max_pointer: The greatest pointer in precedent points.
        :return:
        """
        if max_pointer is None:
            if self.root != 0:
                # this is a root structure, but its pointer is not p0.
                return False, None
            else:
                max_pointer: int = self.root
        if self.root > max_pointer + 1:
            # this is not a root structure, but its pointer is too big.
            return False, None
        if self.root == max_pointer + 1:
            # this is the only authorized increment of max_pointer.
            max_pointer = self.root
        for sub_structure in self.terms:
            check, max_pointer = sub_structure.check_canonicity(max_pointer=max_pointer)
            if not check:
                return False, None
        return True, max_pointer

    @property
    def connector_indexes(self) -> tuple[ConnectorIndex, ...]:
        """Returns

        :return:
        """
        return self._connector_indexes

    @property
    def connector_indexes_count(self):
        """Returns the number of distinct `ConnectorIndex` in the `AbstractFormula`.
        """
        return len(self.connector_indexes)

    @property
    def is_canonical(self) -> bool:
        """Returns `True` if this structure is a canonical, `False` otherwise.

        A structure is a canonical if and only if
        the pointers appearing in the structure,
        when read left-to-right, depth-first,
        are such that no pointer `p_i` ever appear in the structure
        unless i=0, or `p_(i-1)` already appeared in the structure.

        :return:
        """
        return self._is_canonical

    def is_abstract_formula_equivalent_to(self, x: FlexibleAbstractFormula) -> bool:
        """

        ## Definition
        
        Two formula-structures a and b are formula-structure-equivalent if and only if
         - the root of a is connector-index equivalent to the root of b,
         - the arity of a is equal to the arity of b,
         - in order, every term of a is formula-structure-equivalent to the corresponding term of b.

        :param x:
        :param implicit_tuple_conversion:
        :return:
        """
        x: AbstractFormula = data_validate_abstract_formula(x)
        if self is x:
            return True
        elif not (self.root.is_connector_index_equivalent_to(x.root)):
            return False
        elif not (self.arity() == x.arity()):
            return False
        elif not (
                all(fs1.is_abstract_formula_equivalent_to(fs2) for fs1, fs2 in
                    zip(self.terms, x.terms))):
            return False
        return True

    @property
    def is_leaf(self) -> bool:
        """Returns `True` if the structure is a leaf, `False` otherwise.

        A structure is a leaf if and only if it contains no sub-terms.
        """
        return len(self.terms) == 0

    @property
    def root(self) -> ConnectorIndex:
        """The `root` of the `AbstractFormula`.

        The `root` of a `AbstractFormula` is the topmost `ConnectorIndex` of the formula tree..

        :return:
        """
        return self[0]

    def transform_by_connector_index_substitution(self,
                                                  m: dict[
                                                      FlexibleAbstractFormula, FlexibleConnectorIndex]) -> AbstractFormula:
        """Returns an `AbstractFormula` `y` that is a `transformation by connector index substitution` on this `AbstractFormula`,
        given substitution map `m`.

        ## Definition

        A transformation by connector-index substitution is a transformation ...
        TODO: Complete formal definition.

        :param m:
        :return:
        """
        m: ConnectorIndexDict = data_validate_connector_index_dict(m)
        if len(m.keys()) == 0:
            # Trivial case, no substitution is required.
            return self
        else:
            return AbstractFormula(root=m.get(self.root, self.root),
                                   terms=(term.transform_by_connector_index_substitution(m) for term in self.terms))

    @property
    def terms(self) -> tuple[AbstractFormula]:
        """The tuple of terms (sub-structures) contained in this `AbstractFormula`.

        :return:
        """
        return self[1]

    def to_list(self) -> list:
        """Returns a Python `list` of equivalent structure. This is useful to manipulate formulas because
        lists are mutable."""
        return [self.root, [term.to_list() for term in self.terms]]


def data_validate_unicity(elements: typing.Iterable, raise_error_on_duplicate: bool = True) -> tuple:
    """Given some `elements`, returns a tuple of unique elements.

    :param elements:
    :param raise_error_on_duplicate:
    :return:
    """
    unique_elements = []
    for element in elements:
        if element not in unique_elements:
            unique_elements.append(element)
        elif raise_error_on_duplicate:
            raise ValueError('Duplicate elements.')
    return tuple(unique_elements)


class AbstractFormulaTerms(tuple):
    """Formula Structure Terms"""

    def __init__(self, terms: FlexibleAbstractFormulaTerms = None):
        pass

    def __new__(cls, terms: FlexibleAbstractFormulaTerms = None):
        global _abstract_formula_terms
        if terms is None:
            terms = tuple()
        elif isinstance(terms, collections.abc.Iterator) and not isinstance(terms, tuple):
            terms = tuple(terms)
        elif isinstance(terms, collections.abc.Generator):
            terms = tuple(terms)
        if isinstance(terms, tuple):
            terms: tuple[FlexibleAbstractFormula, ...] = tuple(
                data_validate_abstract_formula(term) for term in terms)
            return super(AbstractFormulaTerms, cls).__new__(cls, terms)
        else:
            raise util.PunctiliousException('Data validation error for `Terms` `o`.', terms=terms)


# Type aliases
FlexibleConnectorIndex = typing.Union[ConnectorIndex, int,]
FlexibleConnectorIndexIterator = typing.Union[None, collections.abc.Iterator,]
FlexibleAbstractFormula = typing.Union[AbstractFormula, collections.abc.Iterator, FlexibleConnectorIndex, int,]
FlexibleAbstractFormulaTerms = typing.Union[AbstractFormulaTerms,
collections.abc.Iterator, collections.abc.Generator, tuple, None]

pass
