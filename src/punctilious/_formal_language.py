from __future__ import annotations
import io
import uuid as uuid_pkg
import yaml
import importlib.resources
import collections.abc
import re
import typing

# punctilious modules
import _util
from _util import get_logger
import _identifiers
import _representation


def ensure_formula(o=None) -> Formula:
    if isinstance(o, Formula):
        return o
    elif isinstance(o, Connector):
        return Formula(c=o)
    elif isinstance(o, collections.abc.Iterable):
        # If o is an iterable, the assumption is that it is of the shape:
        # singleton (c) where c is a connector,
        # or pair (c, a) where c is a connector, and a is an n-tuple of argument sub-formulas.
        t = tuple(o)
        if len(t) == 1:
            return Formula(c=t[0])
        elif len(t) == 2:
            c = ensure_connector(t[0])
            a = ensure_formula_arguments(t[1])
            return Formula(c=c, a=a)
        else:
            raise ValueError(f'Formula must be a 1-tuple, or 2-tuple. {t}')
    else:
        raise ValueError(f'o cannot be constrained into a Formula. {type(o)}: {o}')


class Formula(tuple):
    # __slots__ = tuple('_root_connector', '_arguments', )

    def __init__(self, c, a=None):
        """

        :param c: A connector.
        :param args: A (possibly empty) collection of arguments.
        """
        super().__init__()

    def __new__(cls, c, a=None):
        c: Connector = ensure_connector(c)
        a: FormulaArguments = ensure_formula_arguments(a)
        phi: tuple[Connector, FormulaArguments] = (c, a,)
        return super().__new__(cls, phi)

    def __repr__(self):
        return self.connector.__str__() + self.arguments.__str__()

    def __str__(self):
        return self.represent()

    @property
    def arguments(self) -> FormulaArguments:
        return self[1]

    @property
    def connector(self) -> Connector:
        return self[0]

    def represent(self):
        return self.connector.rep_formula(argument=self.arguments)


def ensure_formula_arguments(o=None) -> FormulaArguments:
    if isinstance(o, FormulaArguments):
        return o
    elif isinstance(o, collections.abc.Iterable):
        return FormulaArguments(*o)
    elif o is None:
        return FormulaArguments()
    else:
        raise ValueError(f'o cannot be constrained into FormulaArguments {FormulaArguments}. {type(o)}')


def ensure_connectors(o=None) -> Connectors:
    """

    :param o:
    :param overwrite_mutable_properties: If `o` is in a raw format such as a dictionary (e.g.: read from a YAML file),
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


def ensure_theorems(o=None) -> Theorems:
    if isinstance(o, Theorems):
        return o
    elif isinstance(o, collections.abc.Iterable):
        return Theorems(*o)
    elif o is None:
        return Theorems()
    else:
        raise ValueError(f'o cannot be constrained into Theorems: {o}. {type(o)}')


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
            get_logger().debug(
                f'Preferences singleton ({id(self)}) initialized.')
            get_logger().debug(f'Preferences: {str(self.to_dict())}')

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


class Theorems(tuple):
    """A tuple of Theorem instances."""

    def __init__(self, *args, **kwargs):
        self._slug_index = tuple(i.slug for i in self)
        super().__init__()

    def __new__(cls, *args, **kwargs):
        typed_representations = tuple(ensure_theorem(r) for r in args)
        return super().__new__(cls, typed_representations)

    def __repr__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def get_from_slug(self, slug: str):
        if slug in self._slug_index:
            slug_index = self._slug_index.index(slug)
            return self[slug_index]
        else:
            raise IndexError(f'Theorem slug not found: "{slug}".')

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


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


def ensure_theorem(o) -> Theorem:
    """Assure that `o` is of type Theorem, converting as necessary, or raise an error."""
    if isinstance(o, Theorem):
        return o
    elif isinstance(o, dict):
        uuid = o['uuid']
        slug = o['slug']
        variables = None
        assumptions = None
        statement = None
        justifications = None
        o = Theorem(uuid=uuid, slug=slug, variables=variables, assumptions=assumptions, statement=statement,
                    justifications=justifications)
        return o
    else:
        raise TypeError('Theorem assurance failure.')


class Connectors(tuple):
    """A tuple of Connector instances."""

    def __getitem__(self, key) -> Connector:
        if isinstance(key, int):
            # Default behavior for integer keys
            return super().__getitem__(key)
        if isinstance(key, _identifiers.FlexibleUUID):
            # Custom behavior for uuid keys
            item: Connector | None = self.get_from_uuid(uuid=key, raise_error_if_not_found=False)
            if item is not None:
                return item
        if isinstance(key, _identifiers.FlexibleUniqueIdentifier):
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

    def get_from_uid(self, uid: _identifiers.FlexibleUniqueIdentifier,
                     raise_error_if_not_found: bool = False) -> Connector | None:
        """Return a Connector by its UniqueIdentifier.

        :param uid: a UniqueIdentifier.
        :param raise_error_if_not_found:
        :return:
        """
        uid: _identifiers.UniqueIdentifier = _identifiers.ensure_unique_identifier(uid)
        item: Connector | None = next((item for item in self if item.uid == uid), None)
        if item is None and raise_error_if_not_found:
            raise IndexError(f'Connector not found. UID: "{uid}".')
        else:
            return item

    def get_from_uuid(self, uuid: _identifiers.FlexibleUUID,
                      raise_error_if_not_found: bool = False) -> Connector | None:
        """Return a Connector by its UUID.

        :param uuid: a UUID.
        :param raise_error_if_not_found:
        :return:
        """
        uuid: _identifiers.uuid_pkg.UUID = _identifiers.ensure_uuid(uuid)
        if uuid in self._index:
            identifier_index = self._index.index(uuid)
            return self[identifier_index]
        elif raise_error_if_not_found:
            raise IndexError(f'Connector not found. UUID: "{uuid}".')
        else:
            return None

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Connector(_identifiers.UniqueIdentifiable):
    # __slots__ = ('_uuid', '_slug', '_tokens', '_syntactic_rules', '_representation')

    def __call__(self, *args):
        return Formula(c=self, a=args)

    def __init__(self, package=None, uid=None, syntactic_rules=None, connector_representation=None,
                 formula_representation=None):
        self._package = package
        self._syntactic_rules = ensure_syntactic_rules(syntactic_rules)
        self._connector_representation: _representation.Representation = connector_representation
        self._formula_representation: _representation.Representation = formula_representation
        super().__init__(uid=uid)

    def __repr__(self):
        return f'{self.uid.slug} connector'

    def __str__(self):
        return f'{self.uid} connector'

    @property
    def connector_representation(self) -> _representation.Representation:
        return self._connector_representation

    @connector_representation.setter
    def connector_representation(self, connector_representation):
        self._connector_representation = connector_representation

    @property
    def formula_representation(self) -> _representation.Representation:
        return self._formula_representation

    @formula_representation.setter
    def formula_representation(self, formula_representation):
        self._formula_representation = formula_representation

    @property
    def package(self):
        return self._package

    def rep(self, **kwargs) -> str:
        return self.connector_representation.rep(**kwargs)

    def rep_formula(self, argument: FormulaArguments | None = None):
        """Returns the string representation of the formula *(a1, a2, ..., an),
        where:
         - * is this connector,
         - a1, a2, ..., an are the formula arguments.
        """
        if self.formula_representation is None:
            raise ValueError(f'Connector {self.uid} has no formula representation.')
        connector: str = self.rep()
        argument = ensure_formula_arguments(argument)
        argument_representations = tuple(a.represent() for a in argument)
        variables = {'connector': connector, 'argument': argument_representations}
        return self.formula_representation.rep(variables=variables)

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


def load_connector(o: typing.Mapping, overwrite_mutable_properties: bool = False) -> Connector:
    """Receives a raw Connector, typically from a YAML file, and returns a typed Connector instance.

    :param overwrite_mutable_properties: if `o` is already loaded in memory, overwrite its mutable properties:
        `connector_representation`, and `formula_representation`.
    :param o: a raw Connector.
    :return: a typed Connector instance.
    """
    connector: Connector | None = _identifiers.load_unique_identifiable(o)
    if connector is None:
        # The connector does not exist in memory.
        connector = ensure_connector(o)
    else:
        # The connector exists in memory.
        if overwrite_mutable_properties:
            if overwrite_mutable_properties:
                # Overwrite the mutable properties.
                if 'connector_representation' in o.keys():
                    connector.connector_representation = _representation.ensure_representation(
                        o['connector_representation'])
                if 'formula_representation' in o.keys():
                    connector.formula_representation = _representation.ensure_representation(
                        o['formula_representation'])
    return connector


def load_connectors(o: typing.Iterable | None, overwrite_mutable_properties: bool = False) -> Connectors:
    """Receives a raw Connectors collection, typically from a YAML file,
    and returns a typed Connectors instance.

    :param overwrite_mutable_properties: if connectors are already loaded in memory, overwrite their mutable properties:
        `connector_representation`, and `formula_representation`.
    :param o: a raw Connectors collection.
    :return: a typed Connectors instance.
    """
    if o is None:
        o = []
    connectors: list[Connector] = []
    for i in o:
        connector: Connector = load_connector(i, overwrite_mutable_properties=overwrite_mutable_properties)
        connectors.append(connector)
    return Connectors(*connectors)


class Theorem:
    __slots__ = ('_uuid', '_slug', '_variables', '_assumptions', '_statement', '_justifications')
    _uuid_index = {}

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self._uuid))

    def __init__(self, uuid=None, slug=None, variables=None, assumptions=None, statement=None, justifications=None):
        self._uuid = uuid
        self._slug = slug
        self._variables = variables
        self._assumptions = assumptions
        self._statement = statement
        self._justifications = justifications

    def __repr__(self):
        return self.slug

    def __str__(self):
        return self.slug

    @property
    def assumptions(self):
        return self._assumptions

    @property
    def justifications(self):
        return self._justifications

    @property
    def slug(self):
        return self._slug

    @property
    def statement(self):
        return self._statement

    @property
    def variables(self):
        return self._variables

    def to_dict(self):
        d = {}
        if self.uuid is not None:
            d['uuid'] = self.uuid
        if self.slug is not None:
            d['slug'] = self.slug
        if self.variables is not None:
            d['variables'] = self.variables
        if self.assumptions is not None:
            d['assumptions'] = self.assumptions
        if self.statement is not None:
            d['statement'] = self.statement
        if self.justifications is not None:
            d['justifications'] = self.justifications
        return d

    def to_yaml(self, default_flow_style):
        return yaml.dump(self.to_dict(), default_flow_style=default_flow_style)

    @property
    def uuid(self):
        return self._uuid


class Justifications(tuple):
    __slots__ = ()

    def __init__(self, *args):
        pass

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, args)

    def __repr__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    @classmethod
    def instantiate_from_list(cls, l: list | None):
        if l is None:
            l = []
        typed_l = []
        for d in l:
            o = ensure_justification(o=d)
            typed_l.append(o)
        return Connectors(*typed_l)

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Variable(Formula):
    """

    Global definition: formula of the form v().

    Local definition: a formula of the form v() with the following theorem:
    is_variable(v()).
    """

    def __init__(self, c):
        """

        :param c: A connector.
        """
        super().__init__(c=c, a=None)


_variable_counter = 0


def declare_variable(rep: _representation.Representation):
    """Declare a new variable.

    A variable is a connector that takes no arguments that is designated as a variable.

    :param rep:
    :return:
    """
    # Create a new connector.
    global _variable_counter
    _variable_counter = _variable_counter + 1
    c = Connector(
        uid=_identifiers.create_uid(slug=f'variable_{_variable_counter}'),
        connector_representation=rep)
    return Variable(c=c)
