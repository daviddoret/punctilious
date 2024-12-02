from __future__ import annotations
import io
import uuid
import yaml
import pathlib
import logging
import jinja2
import sys
import importlib.resources
import typing
import abc
import collections.abc

# punctilious modules
import presentation


class Logger:
    __slots__ = ('_native_logger')
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            self._native_logger = logging.getLogger('punctilious')
            self._native_logger.setLevel(logging.DEBUG)
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.flush = lambda: sys.stdout.flush()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            stream_handler.setFormatter(formatter)
            self._native_logger.addHandler(stream_handler)
            self.__class__._singleton_initialized = True
            get_logger().debug(
                f'Logger singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(Logger, cls).__new__(cls)
        return cls._singleton

    def debug(self, msg: str):
        self._native_logger.debug(msg)

    def info(self, msg: str):
        self._native_logger.info(msg)


def ensure_formula(o=None) -> Formula:
    if isinstance(o, Formula):
        return o
    elif isinstance(o, Connector):
        return Formula(c=o)
    else:
        raise ValueError('o cannot be constrained into a Formula.')


class Formula:
    # __slots__ = tuple('_root_connector', '_arguments', )

    def __init__(self, c, *args):
        self._root_connector = ensure_connector(c)
        self._arguments = ensure_formula_arguments(*args)

    @property
    def arguments(self):
        return self._arguments

    @property
    def root_connector(self):
        return self._root_connector


def ensure_formula_arguments(o=None) -> FormulaArguments:
    if isinstance(o, FormulaArguments):
        return o
    elif isinstance(o, collections.abc.Iterable):
        return FormulaArguments(*o)
    elif o is None:
        return FormulaArguments()
    else:
        raise ValueError('o cannot be constrained into FormulaArguments.')


class FormulaArguments(tuple[Formula]):
    """A tuple of formula arguments."""

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __new__(cls, *args, **kwargs) -> tuple[Formula, ...]:
        typed_arguments: tuple[Formula, ...] = tuple(ensure_formula(a) for a in args)
        return super().__new__(cls, typed_arguments)

    def __repr__(self):
        return '(' + ', '.join(str(a) for a in self) + ')'

    def __str__(self):
        return '(' + ', '.join(str(a) for a in self) + ')'


def get_logger():
    return Logger()


class Preferences:
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


def ensure_slug(o: str | Slug) -> Slug:
    if isinstance(o, Slug):
        return o
    elif isinstance(o, str):
        return Slug(o)
    else:
        raise ValueError(f'Invalid slug {o}')


class Slug(str):
    pass


class Slugs(dict):
    def __init__(self):
        super().__init__()

    def __setitem__(self, slug, value):
        slug = ensure_slug(o=slug)
        if slug in self:
            raise KeyError(f"Key '{slug}' already exists.")
        super().__setitem__(slug, value)


class Import:
    __slots__ = ('_slug', '_scheme', '_path', '_resource', '_method', '_package')

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self._slug, self._scheme, self._path, self._resource, self._method))

    def __init__(self, slug, scheme, path, resource, method, load=True):
        self._slug = slug
        self._scheme = scheme
        self._path = path
        self._resource = resource
        self._method = method
        if load:
            if scheme == 'python_package':
                self._package = PythonPackage(path=path, resource=resource)

    def __repr__(self):
        return self.slug

    def __str__(self):
        return self.slug

    @property
    def method(self):
        return self._method

    @property
    def package(self):
        return self._package

    @property
    def path(self):
        return self._path

    @property
    def resource(self):
        return self._resource

    @property
    def slug(self):
        return self._slug

    @property
    def scheme(self):
        return self._scheme

    def to_dict(self):
        d = {}
        if self.slug is not None:
            d['local_name'] = self.slug
        if self.scheme is not None:
            d['scheme'] = self.scheme
        if self.path is not None:
            d['path'] = self.path
        if self.resource is not None:
            d['resource'] = self.resource
        if self.method is not None:
            d['method'] = self.method
        return d

    def to_yaml(self, default_flow_style):
        yaml.dump(self.to_dict(), default_flow_style=default_flow_style)


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


class Renderer:
    """"""
    __slots__ = ('_mode', '_language', '_encoding', '_parentheses', '_template', '_jinja2_template')

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self._mode, self._language, self._encoding, self._parentheses))

    def __init__(self, mode=None, language=None, encoding=None, parentheses=None, template=None):
        self._mode = mode
        self._language = language
        self._encoding = encoding
        self._parentheses = parentheses
        self._template = template
        self._jinja2_template = jinja2.Template(self._template)

    def __repr__(self):
        return self.template

    def __str__(self):
        return self.template

    @property
    def encoding(self):
        return self._encoding

    @property
    def language(self):
        return self._language

    @property
    def jinja2_template(self):
        return self._jinja2_template

    @property
    def mode(self):
        return self._mode

    @property
    def parentheses(self):
        return self._parentheses

    @property
    def template(self):
        return self._template

    def to_dict(self):
        d = {}
        if self.mode is not None:
            d['mode'] = self.mode
        if self.language is not None:
            d['language'] = self.language
        if self.encoding is not None:
            d['encoding'] = self.encoding
        if self.parentheses is not None:
            d['parentheses'] = self.parentheses
        if self.template is not None:
            d['template'] = self.template
        return d

    def to_yaml(self, default_flow_style):
        return yaml.dump(self.to_dict(), default_flow_style=default_flow_style)


class Imports(tuple):
    """A tuple of Import instances."""

    def __init__(self, *args, **kwargs):
        self._slug_index = tuple(i.slug for i in self)
        super().__init__()

    def __new__(cls, *args, **kwargs):
        typed_imports = tuple(ensure_import(r) for r in args)
        return super().__new__(cls, typed_imports)

    def __repr__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def get_from_slug(self, slug: str):
        if slug in self._slug_index:
            slug_index = self._slug_index.index(slug)
            return self[slug_index]
        else:
            raise IndexError(f'Import slug not found: "{slug}".')

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Representations(tuple):
    """A tuple of Representation instances."""

    def __init__(self, *args, **kwargs):
        self._slug_index = tuple(i.slug for i in self)
        super().__init__()

    def __new__(cls, *args, **kwargs):
        typed_representations = tuple(ensure_representation(r) for r in args)
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
            raise IndexError(f'Representation slug not found: "{slug}".')

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


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
        uuid4 = o['uuid4'] if 'uuid4' in o.keys() else None
        slug = o['slug'] if 'slug' in o.keys() else None
        tokens = o['tokens'] if 'tokens' in o.keys() else tuple()
        syntactic_rules = o['syntactic_rules'] if 'syntactic_rules' in o.keys() else None
        representation = o['representation'] if 'representation' in o.keys() else None
        o = Connector(uuid4=uuid4, slug=slug, syntactic_rules=syntactic_rules, representation=representation)
        return o
    else:
        raise TypeError('Connector assurance failure.')


def ensure_import(o) -> Import:
    """Assure that `o` is of type Import, converting as necessary, or raise an error."""
    if isinstance(o, Import):
        return o
    elif isinstance(o, dict):
        slug = o['slug'] if 'slug' in o.keys() else None
        scheme = o['scheme'] if 'scheme' in o.keys() else None
        path = o['path'] if 'path' in o.keys() else None
        resource = o['resource'] if 'resource' in o.keys() else None
        method = o['method'] if 'method' in o.keys() else None
        o = Import(slug=slug, scheme=scheme, path=path, resource=resource, method=method)
        return o
    else:
        raise TypeError('Import assurance failure.')


def ensure_representation(o) -> Representation:
    """Assure that `o` is of type Representation, converting as necessary, or raise an error."""
    if isinstance(o, Representation):
        return o
    elif isinstance(o, dict):
        uuid4 = o['uuid4']
        slug = o['slug']
        syntactic_rules = ensure_syntactic_rules(o=o['syntactic_rules'] if 'syntactic_rules' in o else None)
        configurations = Configurations(
            *o['configurations'] if 'configurations' in o else None)
        o = Representation(uuid4=uuid4, slug=slug, syntactic_rules=syntactic_rules, renderers=configurations)
        return o
    else:
        raise TypeError(f'Representation assurance failure. Type: {type(o)}. Object: {o}.')


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
        uuid4 = o['uuid4']
        slug = o['slug']
        variables = None
        assumptions = None
        statement = None
        justifications = None
        o = Theorem(uuid4=uuid4, slug=slug, variables=variables, assumptions=assumptions, statement=statement,
                    justifications=justifications)
        return o
    else:
        raise TypeError('Theorem assurance failure.')


class Representation:
    __slots__ = ('_uuid4', '_slug', '_syntactic_rules', '_renderers')
    _in_memory = {}

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self.uuid4))

    def __init__(self, uuid4=None, slug=None, syntactic_rules=None, renderers=None):
        self._uuid4 = uuid4
        self._slug = slug
        self._syntactic_rules = syntactic_rules
        self._renderers = renderers

    def __repr__(self):
        return self.slug

    def __str__(self):
        return self.slug

    @property
    def renderers(self):
        return self._renderers

    def repr(self, args=None, encoding=None, mode=None, language=None) -> str:
        if args is None:
            args = ()
        configuration = self.renderers.select(encoding=encoding, mode=mode, language=language)
        if self.syntactic_rules.fixed_arity is not None and len(args) != self.syntactic_rules.fixed_arity:
            raise ValueError('The number of arguments does not match the fixed_arity syntactic_rule.')
        placeholder_names = tuple((f'a{i}' for i in tuple(range(1, len(args) + 1))))
        d = dict(zip(placeholder_names, args))
        output = configuration.jinja2_template.render(d)
        return output

    @property
    def slug(self):
        return self._slug

    @property
    def syntactic_rules(self):
        return self._syntactic_rules

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)

    @property
    def uuid4(self):
        return self._uuid4


class Configurations(tuple):
    """A tuple of Configuration instances."""

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __new__(cls, *args, **kwargs):
        typed_configurations = tuple(presentation.ensure_renderer(r) for r in args)
        return super().__new__(cls, typed_configurations)

    def __repr__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def select(self, encoding=None, mode=None, language=None) -> Renderer:

        encoding = get_preferences().encoding if encoding is None else encoding
        mode = get_preferences().representation_mode if mode is None else mode
        language = get_preferences().language if language is None else language

        match = next(
            (e for e in self if e.encoding == encoding and e.mode == mode and e.language == language),
            None)
        if match:
            return match

        match = next((e for e in self if e.encoding == encoding and e.mode == mode), None)
        if match:
            return match

        match = next((e for e in self if e.encoding == encoding), None)
        if match:
            return match

        return self[0]

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Connectors(tuple):
    """A tuple of Connector instances."""

    def __init__(self, *args, **kwargs):
        # prepare a dictionary that maps slugs and tokens to connectors
        slug_dict = dict(zip(tuple(i.slug for i in self), tuple(i for i in self)))
        tokens = tuple(j for i in self for j in i.tokens)
        aliases_connectors = tuple(slug_dict[i.slug] for i in self for j in i.tokens)
        alias_dict = dict(zip(tokens, aliases_connectors))
        self._slug_index = slug_dict | alias_dict
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
    __slots__ = ('_uuid4', '_slug', '_tokens', '_syntactic_rules', '_representation')
    _uuid4_index = {}

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self._uuid4))

    def __init__(self, uuid4=None, slug=None, tokens=None, syntactic_rules=None, representation=None):
        self._uuid4 = uuid4
        self._slug = slug
        self._tokens = ensure_tokens(tokens)
        self._syntactic_rules = ensure_syntactic_rules(syntactic_rules)
        self._representation: Representation = representation

    def __repr__(self):
        return self.slug

    def __str__(self):
        return self.slug

    def repr(self, args=None, encoding=None, mode=None, language=None) -> str:
        return self.representation.repr(args=args, encoding=encoding, mode=mode, language=language)

    @property
    def representation(self) -> Representation:
        return self._representation

    @property
    def slug(self):
        return self._slug

    @property
    def tokens(self):
        """Tokens are string representations used to identify the connector in a string representation of the
        formula."""
        return self._tokens

    @property
    def syntactic_rules(self):
        return self._syntactic_rules

    def to_dict(self):
        d = {}
        if self.uuid4 is not None:
            d['uuid4'] = self.uuid4
        if self.slug is not None:
            d['slug'] = self.slug
        if self.tokens is not None:
            d['tokens'] = self.tokens
        if self.syntactic_rules is not None:
            d['syntactic_rules'] = self.syntactic_rules
        if self.representation is not None:
            d['representation'] = self.representation
        return d

    def to_yaml(self, default_flow_style):
        return yaml.dump(self.to_dict(), default_flow_style=default_flow_style)

    @property
    def uuid4(self):
        return self._uuid4


class Theorem:
    __slots__ = ('_uuid4', '_slug', '_variables', '_assumptions', '_statement', '_justifications')
    _uuid4_index = {}

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self._uuid4))

    def __init__(self, uuid4=None, slug=None, variables=None, assumptions=None, statement=None, justifications=None):
        self._uuid4 = uuid4
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
        if self.uuid4 is not None:
            d['uuid4'] = self.uuid4
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
    def uuid4(self):
        return self._uuid4


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
            o = assure_justification(o=d)
            typed_l.append(o)
        return Connectors(*typed_l)

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Packages(dict):
    __slots__ = ()
    _singleton = None
    _singleton_initialized = None
    _native_packages = {
        'greek_alphabet_lowercase_serif_italic_representation_1': '/data/representations/greek_alphabet_lowercase_serif_italic.yaml',
        'greek_alphabet_uppercase_serif_italic_representation_1': '/data/representations/greek_alphabet_uppercase_serif_italic.yaml',
        'operators_representation_1': '/data/representations/operators_representation_1.yaml'
    }

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            self.__class__._singleton_initialized = True
            get_logger().debug(
                f'Packages singleton ({id(self)}) initialized.')
        super().__init__()

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(Packages, cls).__new__(cls)
        return cls._singleton

    def __repr__(self):
        return '(' + ', '.join(str(e) for e in self) + ')'

    def __setitem__(self, key, value):
        """Override __setitem__ to check value type before adding to the dictionary."""
        if not isinstance(value, Package):
            raise TypeError(f"Value must be of type Package")
        super().__setitem__(key, value)

    def __str__(self):
        return '(' + ', '.join(str(e) for e in self) + ')'

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)

    def update(self, other=None, **kwargs):
        if isinstance(other, dict):
            for k, v in other.items():
                if not isinstance(v, Package):
                    raise TypeError(f"Value must be of type Package")
                self[k] = v
        for k, v in kwargs.items():
            if not isinstance(v, Package):
                raise TypeError(f"Value must be of type Package")
            self[k] = v


def get_packages():
    return Packages()


class Package:
    __slots__ = ('_schema', '_uuid4', '_slug', '_imports', '_aliases', '_representations', '_connectors', '_theorems',
                 '_justifications')

    # _uuid4_index = {}

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self._uuid4))

    def __init__(self, schema=None, uuid4=None, slug=None, imports=None, aliases=None, representations=None,
                 connectors=None, theorems=None, justifications=None):
        if uuid4 is None:
            uuid4 = uuid.uuid4()
        if slug is None:
            slug = f'package_{str(uuid4).replace('-', '_')}'
        self._schema = schema
        self._uuid4 = uuid4
        self._slug = slug
        self._imports = imports
        self._aliases = aliases
        self._representations = representations
        self._connectors = connectors
        self._theorems = theorems
        self._justifications = justifications
        # Reference the package in the packages singleton.s
        p = get_packages()
        p[slug] = self
        pass

    def __repr__(self):
        return self.slug

    def __str__(self):
        return self.slug

    @property
    def aliases(self):
        return self._aliases

    @property
    def connectors(self):
        return self._connectors

    @property
    def imports(self):
        return self._imports

    @property
    def justifications(self):
        return self._justifications

    @property
    def representations(self):
        return self._representations

    @property
    def schema(self):
        return self._schema

    @property
    def slug(self):
        return self._slug

    @property
    def theorems(self):
        return self._theorems

    @property
    def uuid4(self):
        return self._uuid4


class PythonPackage(Package):
    """A package loaded from the current python package resources."""

    def __init__(self, path: str, resource: str):
        """Import a native package.

        This method is called when processing imports with `source_type: python_package_resources`.

        :param path: A python importlib.resources.files folder, e.g. `data.operators`.
        :param resource: A yaml filename, e.g. `operators_1.yaml`.
        :return:
        """
        package_path = importlib.resources.files(path).joinpath(resource)
        with importlib.resources.as_file(package_path) as file_path:
            with open(file_path, 'r') as file:
                file: io.TextIOBase
                d: dict = yaml.safe_load(file)
                schema = d['schema']
                uuid4 = d['uuid4']
                slug = d['slug']
                untyped_imports = d['imports'] if 'imports' in d.keys() else tuple()
                imports = Imports(*untyped_imports)
                aliases = None  # To be implemented
                untyped_representations = d['representations'] if 'representations' in d.keys() else tuple()
                representations = Representations(*untyped_representations)
                # Load connectors
                typed_connectors = []
                for raw_connector in d['connectors'] if 'connectors' in d.keys() else []:
                    uuid4 = raw_connector['uuid4']
                    slug = raw_connector['slug']
                    tokens = raw_connector['tokens']
                    syntactic_rules = ensure_syntactic_rules(o=
                                                             raw_connector[
                                                                 'syntactic_rules'] if 'syntactic_rules' in raw_connector.keys() else None)
                    representation_reference = raw_connector['representation']
                    representation = self._resolve_package_representation_reference(ref=representation_reference,
                                                                                    i=imports, r=representations)
                    o = Connector(uuid4=uuid4, slug=slug, tokens=tokens, syntactic_rules=syntactic_rules,
                                  representation=representation)
                    typed_connectors.append(o)
                typed_connectors = Connectors(*typed_connectors)
                # Load connectors
                untyped_theorems = d['theorems'] if 'theorems' in d.keys() else tuple()
                theorems = Theorems(*untyped_theorems)
                justifications = Justifications.instantiate_from_list(
                    l=d['justifications'] if 'justifications' in d.keys() else None)
                super().__init__(schema=schema, uuid4=uuid4, slug=slug, imports=imports, aliases=aliases,
                                 representations=representations, connectors=typed_connectors, theorems=theorems,
                                 justifications=justifications)

    def _resolve_package_representation_reference(self, ref: str, i: Imports, r: Representations):
        """Given the reference of a representation in string format,
        typically as the representation attribute of a connector in a YAML file,
        finds and returns the corresponding representation object, either
        from the local representations, or via an import."""
        ref_tuple: tuple = tuple(ref.split('.'))
        if len(ref_tuple) == 1:
            # This is a local reference.
            r = r.get_from_slug(slug=ref)
            return r
        elif len(ref_tuple) == 2:
            # This is a reference in an imported YAML file.
            p_ref = ref_tuple[0]
            p: Package = i.get_from_slug(slug=p_ref).package
            ref = ref_tuple[1]
            r = p.representations.get_from_slug(slug=ref)
            return r
        else:
            raise ValueError(f'Improper reference: "{ref}".')
