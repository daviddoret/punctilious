from __future__ import annotations
import io
import uuid as uuid_pkg
import yaml
import importlib.resources
import collections.abc
import re

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
        phi: tuple = (c, a,)
        return super().__new__(cls, phi)

    def __repr__(self):
        return self.connector.__str__() + self.arguments.__str__()

    def __str__(self):
        return self.connector.__str__() + self.arguments.__str__()

    @property
    def arguments(self):
        return self[1]

    @property
    def connector(self):
        return self[0]

    @property
    def represent(self):
        XXX
        return self._representation_function


def ensure_formula_arguments(o=None) -> FormulaArguments:
    if isinstance(o, FormulaArguments):
        return o
    elif isinstance(o, collections.abc.Iterable):
        return FormulaArguments(*o)
    elif o is None:
        return FormulaArguments()
    else:
        raise ValueError(f'o cannot be constrained into FormulaArguments {FormulaArguments}. {type(o)}')


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


def ensure_connector(o) -> Connector:
    """Assure that `o` is of type Connector, converting as necessary, or raise an error."""
    if isinstance(o, Connector):
        return o
    elif isinstance(o, dict):
        uuid = o['uuid'] if 'uuid' in o.keys() else None
        slug = o['slug'] if 'slug' in o.keys() else None
        tokens = o['tokens'] if 'tokens' in o.keys() else tuple()
        syntactic_rules = o['syntactic_rules'] if 'syntactic_rules' in o.keys() else None
        representation = o['representation'] if 'representation' in o.keys() else None
        o = Connector(uuid=uuid, slug=slug, syntactic_rules=syntactic_rules, representation=representation)
        return o
    else:
        raise TypeError('Connector assurance failure.')


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

    def __init__(self, *args, **kwargs):
        # prepare a dictionary that maps slugs and tokens to connectors
        slug_dict = dict(zip(tuple(i.slug for i in self), tuple(i for i in self)))
        self._slug_index = slug_dict
        # aliases_connectors = tuple(slug_dict[i.slug] for i in self for j in i.tokens)
        # alias_dict = dict(zip(tokens, aliases_connectors))
        # self._slug_index = slug_dict | alias_dict
        super().__init__()

    def __new__(cls, *args, **kwargs):
        typed_connectors = tuple(ensure_connector(r) for r in args)
        return super().__new__(cls, typed_connectors)

    def __repr__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def get_from_slug(self, slug: str):
        if slug in self._slug_index.keys():
            return self._slug_index[slug]
        else:
            raise IndexError(f'Connector slug not found: "{slug}".')

    def get_from_token(self, slug: str):
        if slug in self._slug_index.keys():
            return self._slug_index[slug]
        else:
            raise IndexError(f'Connector slug not found: "{slug}".')

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Connector:
    # __slots__ = ('_uuid', '_slug', '_tokens', '_syntactic_rules', '_representation')

    def __call__(self, *args):
        return Formula(c=self, a=args)

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.package, self.slug))

    def __init__(self, package=None, slug=None, syntactic_rules=None, connector_representation=None,
                 formula_representation=None):
        self._package = package
        self._slug = slug
        self._syntactic_rules = ensure_syntactic_rules(syntactic_rules)
        self._connector_representation: _presentation.Representation = connector_representation
        self._formula_representation: _presentation.Representation = formula_representation

    def __repr__(self):
        return self.slug

    def __str__(self):
        return self.slug

    @property
    def connector_representation(self) -> _presentation.Representation:
        return self._connector_representation

    @connector_representation.setter
    def connector_representation(self, connector_representation):
        self._connector_representation = connector_representation

    @property
    def formula_representation(self) -> _presentation.Representation:
        return self._formula_representation

    @formula_representation.setter
    def formula_representation(self, formula_representation):
        self._formula_representation = formula_representation

    @property
    def package(self):
        return self._package

    def rep(self, **kwargs) -> str:
        return self.connector_representation.rep(**kwargs)

    def rep_formula(self, **kwargs):
        return self.formula_representation.rep()

    @property
    def slug(self):
        return self._slug

    @property
    def syntactic_rules(self):
        return self._syntactic_rules

    def to_dict(self):
        d = {}
        if self.slug is not None:
            d['slug'] = self.slug
        if self.syntactic_rules is not None:
            d['syntactic_rules'] = self.syntactic_rules
        if self.connector_representation is not None:
            d['connector_representation'] = self.connector_representation
        if self.formula_representation is not None:
            d['formula_representation'] = self.formula_representation
        return d

    def to_yaml(self, default_flow_style):
        return yaml.dump(self.to_dict(), default_flow_style=default_flow_style)


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


def declare_variable(rep: _presentation.Representation):
    """Declare a new variable.

    A variable is a connector that takes no arguments that is designated as a variable.

    :param rep:
    :return:
    """
    # Create a new connector.
    c = Connector(connector_representation=rep)
    return Variable(c=c)
