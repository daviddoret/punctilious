# special features
from __future__ import annotations

# external modules
import yaml
import collections.abc
import typing
import uuid as uuid_pkg
import abc

# punctilious modules
import punctilious.constants as _cst
import punctilious.pu_01_utilities as _utl
import punctilious.pu_02_unique_identifiers as _ids
import punctilious.pu_03_representation as _rpr

_implicit_conversion_mapping: list[tuple[typing.Callable, Connector]] = []
"""A global variable where implicit conversion is configured. See `implicit_conversion`."""


def configure_implicit_conversion(test_function: typing.Callable, conversion_function: typing.Callable,
                                  priority: int | None = None) -> None:
    """Configure implicit conversion.

    :param test_function: A boolean Python function.
    :param conversion_function:
    :return:
    """
    global _implicit_conversion_mapping
    if priority is None:
        _implicit_conversion_mapping.append((test_function, conversion_function))
    else:
        _implicit_conversion_mapping.insert(priority, (test_function, conversion_function))


def ensure_formula(o: object = None) -> Formula:
    global _implicit_conversion_mapping
    if isinstance(o, Formula):
        return o
    if isinstance(o, Connector):
        # This is a convention: when a connector * is passed as is, it is interpreted as *().
        return Formula(connector=o)
    for mapping in _implicit_conversion_mapping:
        test_function: typing.Callable = mapping[0]
        if test_function(o):
            conversion_function: Connector = mapping[1]
            return conversion_function(o)
    else:
        raise _utl.PunctiliousError(f'`o` cannot be interpreted as a Formula.',
                                    o=o)


class Formula(tuple):
    # __slots__ = tuple('_root_connector', '_arguments', )

    def __eq__(self, other):
        """Python equality is implemented as formula-equivalence."""
        other = ensure_formula(other)
        return self.is_formula_equivalent(other_formula=other)

    def __init__(self, connector, arguments=None):
        """

        :param connector: A connector.
        :param arguments: A (possibly empty) collection of arguments.
        """
        super().__init__()

    def __getitem__(self, index):
        """Returns the """
        if isinstance(index, slice):
            # Handle slicing
            return self.arguments[index.start:index.stop:index.step]
        else:
            # Handle single index
            return self.arguments[index]

    def __hash__(self):
        return hash((self.connector, self.arguments))

    def __iter__(self):
        """Iterates the 1st level arguments of the formula.

        Note: This is equivalent to the explicit `iterate_arguments()` method.
        """
        yield from self.iterate_top_level_arguments()

    def __ne__(self, other):
        return not self == other

    def __new__(cls, connector, arguments=None):
        connector: Connector = ensure_connector(connector)
        arguments: FormulaArguments = ensure_formula_arguments(arguments)
        phi: tuple[Connector, FormulaArguments] = (connector, arguments,)
        return super().__new__(cls, phi)

    def __repr__(self):
        # return self.connector.__str__() + self.arguments.__str__()
        return self.represent()

    def __str__(self):
        return self.represent()

    @property
    def arguments(self) -> FormulaArguments:
        return super().__getitem__(_cst.FORMULA_ARGUMENTS_INDEX)

    @property
    def arity(self) -> int:
        """Return the arity of the formula, that is its number of arguments.

        :return:
        """
        return len(self.arguments)

    @property
    def connector(self) -> Connector:
        return super().__getitem__(_cst.FORMULA_CONNECTOR_INDEX)

    def get_argument_first_index(self, argument: Formula) -> int:
        """Returns the 0-based index of `argument` in this formula.

        Note that `argument` may occur at multiple positions in the formula arguments,
        only the first position is returned."""
        argument = ensure_formula(o=argument)
        for i, x in enumerate(self.arguments):
            if argument.is_formula_equivalent(x):
                return i
        raise ValueError('`argument` is not an argument of this formula.')

    def get_raw_element(self, index) -> Formula:
        """Returns the `index` raw element of the formula.

        Note: `__getitem__` is overridden to return formula arguments, which is the
        naturally expected behavior in most circumstances. This method gives access to the
        raw `__getitem__` method of the Python `tuple` super class.
        """
        yield from super().__getitem__(index)

    def has_top_level_argument(self, argument: Formula) -> bool:
        """Returns `True` if `argument` is a direct argument of the formula.

        By direct argument, it is meant that arguments' sub-formulas are not being considered.

        Note that `argument` may be multiple times a direct argument of the formula."""
        return is_top_level_element_of(formula=argument, container=self)

    @property
    def has_unique_arguments(self) -> bool:
        """Returns `True` if the exists no pair of two formula direct arguments that are formula-equivalent."""
        return formulas_are_unique(*self.arguments)

    @property
    def is_atomic(self) -> bool:
        """A formula is atomic if it has no arguments."""
        return self.arity == 0

    @property
    def is_binary(self) -> bool:
        """A formula is binary if it has exactly two arguments."""
        return self.arity == 2

    def is_formula_equivalent(self, other_formula: Formula) -> bool:
        """Returns `True` if this formula is formula-equivalent to `other_formula`, `False` otherwise"""
        other_formula = ensure_formula(o=other_formula)
        if not self.is_root_connector_equivalent(other=other_formula):
            return False
        elif not self.arity == other_formula.arity:
            return False
        else:
            return all(this_argument.is_formula_equivalent(other_argument)
                       for this_argument, other_argument in zip(self.arguments, other_formula.arguments))

    def is_root_connector_equivalent(self, other: Formula) -> bool:
        """Returns `True` if this formula is root-connector-equivalent to `other_formula`, `False` otherwise."""
        other: Formula = ensure_formula(o=other)
        return self.connector.is_connector_equivalent_to(other.connector)

    @property
    def is_ternary(self) -> bool:
        """A formula is ternary if it has exactly three arguments."""
        return self.arity == 3

    @property
    def is_unary(self) -> bool:
        """A formula is unary if it has exactly one argument."""
        return self.arity == 1

    def iterate_top_level_arguments(self) -> typing.Generator[Formula, None, None]:
        """Iterates the formula (first-level) arguments using the following algorithm:
         - left-right.
        """
        for x in self.arguments:
            yield x

    def iterate_raw_elements(self) -> typing.Generator[Formula, None, None]:
        """Iterates the two formula raw level components, that is the connector and the arguments.

        Note: `__iter__` is overridden to iterate the formula arguments, which is the
        naturally expected behavior in most circumstances. This method gives access to the
        raw `__iter__` method of the Python `tuple` super class.
        """
        yield from super().__iter__()

    def iterate_tree(self, include_root: bool = True) -> typing.Generator[Formula, None, None]:
        """Iterates the formula tree using the following algorithm:
         - top-down first,
         - left-right second.
        """
        if include_root:
            yield self
        for x in self.iterate_top_level_arguments():
            yield from x.iterate_tree(include_root=True)

    def represent(self, is_subformula: bool = False, prefs=None) -> str:
        return self.connector.rep_formula(argument=self.arguments, is_subformula=is_subformula, prefs=prefs)

    def to_python_list(self, include_connector: bool = False, recursive: bool = False) -> list:
        """Returns a raw Python list representation of this formula.

        :param include_connector: If `False` (default), outputs formulas as (argument_1, argument_2, ..., argument_n).
            If `True`, outputs formula as (connector, (argument_1, argument_2, ..., argument_n))
        :param recursive: If `False` (default), leave sub-formulas intact. If `True`, apply the transformation
            recursively to sub-formulas.
        :return: A Python list.
        """
        if not recursive:
            if not include_connector:
                return list(self.arguments)
            else:
                return [self.connector, list(self.arguments), ]
        else:
            if not include_connector:
                return list(
                    argument.to_python_list(include_connector=include_connector, recursive=recursive) for argument in
                    self.arguments)
            else:
                return [self.connector, list(
                    argument.to_python_list(include_connector=include_connector, recursive=recursive) for argument in
                    self.arguments), ]

    def to_python_tuple(self, include_connector: bool = False, recursive: bool = False) -> tuple:
        """Returns a raw Python tuple representation of this formula.

        :param include_connector: If `False` (default), outputs formulas as (argument_1, argument_2, ..., argument_n).
            If `True`, outputs formula as (connector, (argument_1, argument_2, ..., argument_n))
        :param recursive: If `False` (default), leave sub-formulas intact. If `True`, apply the transformation
            recursively to sub-formulas.
        :return: A Python tuple.
        """
        if not recursive:
            if not include_connector:
                return tuple(self.arguments)
            else:
                return self.connector, tuple(self.arguments),
        else:
            if not include_connector:
                return tuple(
                    argument.to_python_list(include_connector=include_connector, recursive=recursive) for argument in
                    self.arguments)
            else:
                return (self.connector, tuple(
                    argument.to_python_list(include_connector=include_connector, recursive=recursive) for argument in
                    self.arguments),)

    def tree_contains_formula(self, phi: Formula, include_root: bool = True) -> bool:
        """Returns `True` if the formula tree contains formula `phi`.

        :param phi:
        :param include_root: Consider the case where the root formula is formula-equivalent to `phi` as valid.
            This is the default behavior.
        :return:
        """
        phi = ensure_formula(o=phi)
        for psi in self.iterate_tree(include_root=include_root):
            if phi.is_formula_equivalent(other_formula=psi):
                return True
        return False


def ensure_formula_arguments(o=None) -> FormulaArguments:
    if isinstance(o, FormulaArguments):
        return o
    elif isinstance(o, collections.abc.Iterable):
        return FormulaArguments(*o)
    elif o is None:
        return FormulaArguments()
    else:
        raise ValueError(f'o cannot be constrained into FormulaArguments {FormulaArguments}. {type(o)}')


def ensure_formulas(*formulas: Formula) -> tuple[Formula, ...]:
    """

    :param formulas:
    :return:
    """
    return tuple(ensure_formula(o=x) for x in formulas)


import enum


def ensure_unique_formulas(*formulas: Formula,
                           duplicate_processing: _cst.DuplicateProcessing = _cst.DuplicateProcessing.RAISE_ERROR) -> \
        tuple[
            Formula, ...]:
    """Ensure that a collection of formulas contains only unique formulas.

    :param duplicate_processing: DuplicateProcessing.RAISE_ERROR or DuplicateProcessing.STRIP.
    :param formulas:
    :return:
    """
    formulas: tuple[Formula, ...] = ensure_formulas(*formulas)
    n = len(formulas)
    unique_formulas: list[Formula] = []
    for phi in formulas:
        if any(is_formula_equivalent(phi=phi, psi=psi) for psi in unique_formulas):
            if duplicate_processing == _cst.DuplicateProcessing.RAISE_ERROR:
                raise _utl.PunctiliousError(
                    title='Formulas are not unique',
                    details='Formula `phi` occurs at least twice in `formulas`.'
                            ' It follows that `formulas` are not unique.',
                    phi=phi,
                    formulas=formulas)
        else:
            unique_formulas.append(phi)
    unique_formulas: tuple[Formula, ...] = tuple(unique_formulas)
    return unique_formulas


def ensure_connectors(o=None) -> Connectors:
    """

    :param o:
    and if `o` is a UniqueIdentifiable that is already loaded in memory, overwrite its mutable properties (i.e.: update
    `o`).
    :return:
    """
    if isinstance(o, Connectors):
        return o
    elif isinstance(o, collections.abc.Iterable):
        return Connectors(*o)
    elif o is None:
        return Connectors()
    else:
        raise ValueError(f'o cannot be constrained into Connectors: {o}. {type(o)}')


class FormulaArguments(tuple[Formula]):
    """A tuple of formulas. Used to represent the arguments of a non-atomic formula."""

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __new__(cls, *args, **kwargs) -> tuple[Formula, ...]:
        typed_arguments: tuple[Formula, ...] = tuple(ensure_formula(a) for a in args)
        return super().__new__(cls, typed_arguments)

    def __repr__(self):
        return '(' + ', '.join(str(a) for a in self) + ')'

    def __str__(self):
        return '(' + ', '.join(str(a) for a in self) + ')'


class Preferences:
    # The correct class for presentation preferences is presentation.TagsPreferences.
    __slots__ = ('_representation_mode', '_encoding', '_language')
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            self._representation_mode = 'symbolic'
            self._encoding = 'unicode_basic'
            self._language = 'en'
            self.__class__._singleton_initialized = True
            _utl.debug(
                f'Preferences singleton ({id(self)}) initialized.')
            _utl.debug(f'Preferences: {str(self.to_dict())}')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(Preferences, cls).__new__(cls)
        return cls._singleton

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        self._encoding = value

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value

    @property
    def representation_mode(self):
        return self._representation_mode

    @representation_mode.setter
    def representation_mode(self, value):
        self._representation_mode = value

    def to_dict(self):
        d = {}
        if self.encoding is not None:
            d['encoding'] = self.encoding
        if self.language is not None:
            d['language'] = self.language
        if self.representation_mode is not None:
            d['representation_mode'] = self.representation_mode
        return d

    def to_yaml(self, default_flow_style=True):
        yaml.dump(self.to_dict(), default_flow_style=default_flow_style)


def get_preferences():
    return Preferences()


class SyntacticRules:
    __slots__ = ('_fixed_arity', '_min_arity', '_max_arity')

    def __init__(self, fixed_arity=None, min_arity=None, max_arity=None):
        self._fixed_arity = fixed_arity
        self._min_arity = min_arity
        self._max_arity = max_arity

    def __repr__(self):
        formatted_items = [f'{key}: {value}' for key, value in self.to_dict().items()]
        return '(' + ', '.join(formatted_items) + ')'

    def __str__(self):
        formatted_items = [f'{key}: {value}' for key, value in self.to_dict().items()]
        return '(' + ', '.join(formatted_items) + ')'

    @property
    def fixed_arity(self):
        return self._fixed_arity

    @property
    def max_arity(self):
        return self._max_arity

    @property
    def min_arity(self):
        return self._min_arity

    def to_dict(self):
        d = dict()
        if self.fixed_arity is not None:
            d['fixed_arity'] = self.fixed_arity
        if self.min_arity is not None:
            d['min_arity'] = self.min_arity
        if self.max_arity is not None:
            d['max_arity'] = self.max_arity
        return d

    def to_yaml(self, default_flow_style):
        yaml.dump(self.to_dict(), default_flow_style=default_flow_style)


def ensure_tokens(o) -> tuple[str, ...]:
    if isinstance(o, collections.abc.Iterable):
        o = tuple(str(i) for i in o)
        return o
    elif o is None:
        return tuple()
    else:
        raise TypeError(f'Tokens assurance failure. Type: {type(o)}. Object: {o}.')


def ensure_syntactic_rules(o) -> SyntacticRules:
    """Assure that `o` is of type SyntacticRules, converting as necessary, or raise an error."""
    if isinstance(o, SyntacticRules):
        return o
    elif isinstance(o, dict):
        fixed_arity = o['fixed_arity'] if 'fixed_arity' in o.keys() else None
        min_arity = o['min_arity'] if 'min_arity' in o.keys() else None
        max_arity = o['max_arity'] if 'max_arity' in o.keys() else None
        o = SyntacticRules(fixed_arity=fixed_arity, min_arity=min_arity, max_arity=max_arity)
        return o
    elif o is None:
        # None is mapped to empty syntactic-rules.
        return SyntacticRules()
    else:
        raise TypeError('SyntacticRules assurance failure.')


class Connectors(tuple):
    """A tuple of Connector instances."""

    def __getitem__(self, key) -> Connector:
        if isinstance(key, int):
            # Default behavior for integer keys
            return super().__getitem__(key)
        if isinstance(key, _ids.FlexibleUUID):
            # Custom behavior for uuid keys
            item: Connector | None = self.get_from_uuid(uuid=key, raise_error_if_not_found=False)
            if item is not None:
                return item
        if isinstance(key, _ids.FlexibleUniqueIdentifier):
            # Custom behavior for UniqueIdentifier keys
            item: Connector | None = self.get_from_uid(uid=key, raise_error_if_not_found=False)
            if item is not None:
                return item
        else:
            raise TypeError(f'Unsupported key type: {type(key).__name__}')

    def __init__(self, *args):
        self._index = tuple(i.uid for i in self)
        super().__init__()

    def __new__(cls, *args):
        typed_connectors = tuple(ensure_connector(r) for r in args)
        return super().__new__(cls, typed_connectors)

    def __repr__(self):
        return '(' + ', '.join(e.uid.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.uid.slug for e in self) + ')'

    def get_from_uid(self, uid: _ids.FlexibleUniqueIdentifier,
                     raise_error_if_not_found: bool = False) -> Connector | None:
        """Return a Connector by its UniqueIdentifier.

        :param uid: a UniqueIdentifier.
        :param raise_error_if_not_found:
        :return:
        """
        uid: _ids.UniqueIdentifier = _ids.ensure_unique_identifier(uid)
        item: Connector | None = next((item for item in self if item.uid == uid), None)
        if item is None and raise_error_if_not_found:
            raise IndexError(f'Connector not found. UID: "{uid}".')
        else:
            return item

    def get_from_uuid(self, uuid: _ids.FlexibleUUID,
                      raise_error_if_not_found: bool = False) -> Connector | None:
        """Return a Connector by its UUID.

        :param uuid: a UUID.
        :param raise_error_if_not_found:
        :return:
        """
        uuid: _ids.uuid_pkg.UUID = _ids.ensure_uuid(uuid)
        if uuid in self._index:
            identifier_index = self._index.index(uuid)
            return self[identifier_index]
        elif raise_error_if_not_found:
            raise IndexError(f'Connector not found. UUID: "{uuid}".')
        else:
            return None

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Connector(_ids.UniqueIdentifiable):
    """
    TODO: Inherit from tuple to manage immutable properties.
    """
    _no_uid_unique_index: int = 0

    def __call__(self, *args):
        """Return a formula with this connector as the root connector, and the arguments as its arguments."""
        return Formula(connector=self, arguments=args)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((type(self), self.uid))

    def __init__(self, uid: _ids.FlexibleUniqueIdentifier | None = None,
                 package=None,
                 syntactic_rules=SyntacticRules(),
                 connector_representation: _rpr.AbstractRepresentation | None = None,
                 formula_representation: _rpr.AbstractRepresentation | None = None,
                 subscript_representation: _rpr.AbstractRepresentation | None = None,
                 superscript_representation: _rpr.AbstractRepresentation | None = None
                 ):
        if uid is None:
            # Assigns automatically a new uid
            Connector._no_uid_unique_index = Connector._no_uid_unique_index + 1
            slug: str = f'c{Connector._no_uid_unique_index}'
            uid = _ids.create_uid(slug)
        self._package = package
        self._syntactic_rules = ensure_syntactic_rules(syntactic_rules)
        self._connector_representation: _rpr.AbstractRepresentation = connector_representation
        self._formula_representation: _rpr.AbstractRepresentation = formula_representation
        self._subscript_representation: _rpr.AbstractRepresentation = subscript_representation
        self._superscript_representation: _rpr.AbstractRepresentation = superscript_representation
        super().__init__(uid=uid)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __repr__(self):
        return f'{self.uid.slug}[{self.uid.uuid}]'

    def __str__(self):
        return f'{self.uid.slug}'

    @property
    def connector_representation(self) -> _rpr.AbstractRepresentation:
        return self._connector_representation

    @connector_representation.setter
    def connector_representation(self, connector_representation):
        self._connector_representation = connector_representation

    @property
    def formula_representation(self) -> _rpr.AbstractRepresentation:
        return self._formula_representation

    @formula_representation.setter
    def formula_representation(self, formula_representation):
        self._formula_representation = formula_representation

    @property
    def has_subscript(self) -> bool:
        return self.subscript_representation is None

    @property
    def has_superscript(self) -> bool:
        return self.superscript_representation is None

    def is_connector_equivalent_to(self, other: Connector) -> bool:
        """Returns True if the connectors are equivalent, False otherwise."""
        return self.uid.is_unique_identifier_equivalent(other.uid)

    def rep_connector(self, prefs=None, **kwargs) -> str:
        return self.connector_representation.rep(prefs=prefs, **kwargs)

    def rep_formula(self, argument: FormulaArguments | None = None, is_subformula: bool = False, prefs=None) -> str:
        """Returns the string representation of the formula.
        """
        connector_representation: str
        if self.connector_representation is None:
            # Fail-safe representation when `connector_representation` is not defined.
            connector_representation = self.uid.slug.human_friendly_representation
        else:
            connector_representation: str = self.rep_connector(prefs=prefs)
        if self.subscript_representation is None:
            # Fail-safe representation when `subscript_representation` is not defined.
            subscript_representation = ''
        else:
            subscript_representation: str = self.rep_subscript(prefs=prefs)
        if self.superscript_representation is None:
            # Fail-safe representation when `superscript_representation` is not defined.
            superscript_representation = ''
        else:
            superscript_representation: str = self.rep_superscript(prefs=prefs)
        formula_representation: str
        if self.formula_representation is None:
            # Fail-safe representation when `formula_representation` is not defined.
            arguments_representation: str = ', '.join(
                tuple(i.represent(is_subformula=True, prefs=prefs) for i in argument))
            formula_representation = f'{connector_representation}({arguments_representation})'
        else:
            argument = ensure_formula_arguments(argument)
            argument_representations = tuple(a.represent(is_subformula=True, prefs=prefs) for a in argument)
            variables = {
                'connector': connector_representation,
                'has_subscript': self.has_subscript,
                'subscript': subscript_representation,
                'has_superscript': self.has_superscript,
                'superscript': superscript_representation,
                'argument': argument_representations,
                'is_subformula': is_subformula}
            # TODO: NICE_TO_HAVE: Find a way to manage connector precedences, and pass parent and
            #   child connector
            #   precedences as a variables to the jinja2 template to manage with more accuracy the
            #   parenthesization. Precedence should not be a static connector property, but should
            #   rather be a property of the representation, or possibly of the mapping.
            formula_representation: str = self.formula_representation.rep(variables=variables, prefs=prefs)
        return formula_representation

    def rep_subscript(self, prefs=None, **kwargs) -> str:
        if self.has_subscript:
            return self.subscript_representation.rep(prefs=prefs, **kwargs)
        else:
            return ''

    def rep_superscript(self, prefs=None, **kwargs) -> str:
        if self.has_superscript:
            return self.superscript_representation.rep(prefs=prefs, **kwargs)
        else:
            return ''

    @property
    def subscript_representation(self) -> _rpr.AbstractRepresentation | None:
        return self._subscript_representation

    @subscript_representation.setter
    def subscript_representation(self, subscript_representation: _rpr.AbstractRepresentation | None):
        self._subscript_representation = subscript_representation

    @property
    def superscript_representation(self) -> _rpr.AbstractRepresentation | None:
        return self._superscript_representation

    @superscript_representation.setter
    def superscript_representation(self, superscript_representation: _rpr.AbstractRepresentation | None):
        self._superscript_representation = superscript_representation

    @property
    def syntactic_rules(self):
        return self._syntactic_rules

    def to_dict(self):
        d = {}
        if self.uid is not None:
            d['identifier'] = self.uid
        if self.syntactic_rules is not None:
            d['syntactic_rules'] = self.syntactic_rules
        if self.connector_representation is not None:
            d['connector_representation'] = self.connector_representation
        if self.formula_representation is not None:
            d['formula_representation'] = self.formula_representation
        if self.subscript_representation is not None:
            d['subscript_representation'] = self.subscript_representation
        if self.superscript_representation is not None:
            d['superscript_representation'] = self.superscript_representation
        return d

    def to_yaml(self, default_flow_style):
        return yaml.dump(self.to_dict(), default_flow_style=default_flow_style)


FlexibleConnector = typing.Union[Connector, collections.abc.Mapping, collections.abc.Iterable]
FlexibleConnectors = typing.Union[Connectors, collections.abc.Iterable]


def ensure_connector(o: FlexibleConnector) -> Connector:
    """Assure that `o` is of type Connector, converting as necessary, or raise an error.

    :param o:
    :return:
    """
    if isinstance(o, Connector):
        return o
    elif isinstance(o, typing.Mapping):
        uid = o['uid'] if 'uid' in o.keys() else None
        syntactic_rules = o['syntactic_rules'] if 'syntactic_rules' in o.keys() else None
        connector_representation = o['connector_representation'] if 'connector_representation' in o.keys() else None
        formula_representation = o['formula_representation'] if 'formula_representation' in o.keys() else None
        o = Connector(uid=uid, syntactic_rules=syntactic_rules, connector_representation=connector_representation,
                      formula_representation=formula_representation)
        return o
    else:
        raise TypeError(f'Connector assurance failure. o: {str(o)}, type: {type(o).__name__}.')


def is_root_connector_equivalent(phi: Formula, psi: Formula) -> bool:
    """Determines whether two formulas are root-connector-equivalent.

    Args:
        phi: a formula
        psi: a formula

    Returns:
        bool: True if the formulas are root-connector-equivalent, False otherwise.

    """
    phi: Formula = ensure_formula(o=phi)
    psi: Formula = ensure_formula(o=psi)
    return phi.is_root_connector_equivalent(other=psi)


def is_formula_equivalent(phi: Formula, psi: Formula) -> bool:
    """Determines whether two formulas are formula-equivalent.

    Args:
        phi: a formula
        psi: a formula

    Returns:
        bool: True if the formulas are formula-equivalent, False otherwise.

    """
    phi = ensure_formula(o=phi)
    psi = ensure_formula(o=psi)
    return phi.is_formula_equivalent(other_formula=psi)


def formula_has_unique_arguments(phi: Formula) -> bool:
    """Check if a formula contains unique or duplicate arguments.
    """
    phi: Formula = ensure_formula(o=phi)
    return phi.has_unique_arguments


def formulas_are_unique(*formulas: Formula, raise_error_if_false: bool = False) -> bool:
    """Returns `True` if all formulas passed as arguments are unique,
    in other words there exists no pair of two formulas that are formula-equivalent.
    """
    formulas = ensure_formulas(*formulas)
    for i in range(len(formulas)):
        for j in range(i + 1, len(formulas)):  # Ensure j > i to avoid duplicates
            if is_formula_equivalent(formulas[i], formulas[j]):
                if raise_error_if_false:
                    raise _utl.PunctiliousError(
                        title='Formulas are not unique',
                        details='`formulas` are not unique because formula `phi` at index-position `i`'
                                ' is formula-equivalent with formula `psi` at index-position `j`.',
                        phi=formulas[i],
                        psi=formulas[j],
                        i=i,
                        j=j,
                        formulas=formulas
                    )
                return False
    return True


def load_connector(o: [typing.Mapping | str | uuid_pkg.UUID],
                   raise_error_if_not_found: bool = True) -> Connector:
    """Load a UniqueIdentifiable of type Connector from the general UID index.

    :param o:
    :param raise_error_if_not_found:
    :return:
    """
    o: _ids.UniqueIdentifiable = _ids.load_unique_identifiable(o=o, raise_error_if_not_found=True)
    if not isinstance(o, Connector):
        raise TypeError(f'`o` ({o}) of type `{str(type(o))}` is not of type `Connector`.')
    o: Connector
    return o


def arity(phi: Formula) -> int:
    """Returns the arity of a formula.

    Args:
        phi: a formula

    Returns:
        int: the arity of the formula

    """
    phi = ensure_formula(o=phi)
    return phi.arity


def is_atomic(phi: Formula) -> bool:
    """Determines whether a formula is atomic.

    Args:
        phi: a formula
        """
    phi = ensure_formula(o=phi)
    return phi.is_atomic


def is_binary(phi: Formula) -> bool:
    """Determines whether a formula is binary.

    Args:
        phi: a formula
        """
    phi = ensure_formula(o=phi)
    return phi.is_binary


def is_ternary(phi: Formula) -> bool:
    """Determines whether a formula is ternary.

    Args:
        phi: a formula
        """
    phi = ensure_formula(o=phi)
    return phi.is_ternary


def is_top_level_element_of(formula: Formula, container: typing.Iterable[Formula] | Formula) -> bool:
    """Returns `True` if `formula` is a top-level element of `container`, `False` otherwise.

    Note 1:
        - The top-level elements of a formula are its arguments.
        - The top-level elements of an iterable Python object are the top-level elements of that iterable.

    Note 2:
    In practice, using the default iterator (e.g. `formula in container`) is equivalent.
    This function is semantically more explicit in its intention.
    """
    if isinstance(container, Formula):
        container: Formula = ensure_formula(container)
        for x in container.iterate_top_level_arguments():
            if x.is_formula_equivalent(formula):
                return True
        return False
    if isinstance(container, typing.Iterable):
        for x in container:
            if x.is_formula_equivalent(formula):
                return True
        return False
    raise _utl.PunctiliousError(title='Non supported Python type.',
                                details='`container` is of a `python_type` that is not supported by this function.',
                                python_type=type(container).__name__,
                                container=container)
