"""Bundling refers to the capability to bundle together formal language components,
store them in YAML files or other containers, and reload them from these.

"""

import importlib
import importlib.resources

import os
import yaml
import io
import itertools
# punctilious modules
import punctilious.util as _util
import punctilious.identifiers as _identifiers
import punctilious.representation as _representation
import punctilious.formal_language as _formal_language


class Bundles(dict):
    __slots__ = ()
    _singleton = None
    _singleton_initialized = None
    _native_packages = {
        'greek_alphabet_lowercase_serif_italic_representation_1': '/data/representations/greek_alphabet_lowercase_serif_italic.yaml',
        'greek_alphabet_uppercase_serif_italic_representation_1': '/data/representations/greek_alphabet_uppercase_serif_italic.yaml',
        'operators_representation_1': '/data/representations/operators_1.yaml'
    }

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            self.__class__._singleton_initialized = True
            _util.get_logger().debug(
                f'Packages singleton ({id(self)}) initialized.')
        super().__init__()

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(Bundles, cls).__new__(cls)
        return cls._singleton

    def __repr__(self):
        return '(' + ', '.join(str(e) for e in self) + ')'

    def __setitem__(self, key, value):
        """Override __setitem__ to check value type before adding to the dictionary."""
        if not isinstance(value, Bundle):
            raise TypeError(f"Value must be of type Package")
        super().__setitem__(key, value)

    def __str__(self):
        return '(' + ', '.join(str(e) for e in self) + ')'

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)

    def update(self, other=None, **kwargs):
        if isinstance(other, dict):
            for k, v in other.items():
                if not isinstance(v, Bundle):
                    raise TypeError(f"Value must be of type Package")
                self[k] = v
        for k, v in kwargs.items():
            if not isinstance(v, Bundle):
                raise TypeError(f"Value must be of type Package")
            self[k] = v


def get_packages():
    return Bundles()


class Bundle(_identifiers.UniqueIdentifiable):
    """Inherit from tuple and make it immutable.

    """

    def __init__(self, uid: _identifiers.FlexibleUniqueIdentifier, schema=None, imports=None,
                 aliases=None,
                 representations=None, connectors=None, statements=None, justifications=None):
        super().__init__(uid=uid)
        self._schema = schema
        self._imports = imports
        self._aliases = aliases
        representations = _representation.ensure_abstract_representations(representations)
        self._representations = representations
        connectors = _formal_language.ensure_connectors(connectors)
        self._connectors = connectors
        statements = _formal_language.ensure_statements(statements)
        self._statements = statements
        self._justifications = justifications
        # Reference the package in the packages singleton.s
        p = get_packages()

    def __repr__(self):
        return f'{self.uid.slug} bundle'

    def __str__(self):
        return f'{self.uid.slug} bundle'

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
    def statements(self):
        return self._statements


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
                self._package = YamlFileBundle(path=path, resource=resource)

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


class YamlFileBundle(Bundle):
    """A package loaded from a single yaml file."""

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
                #                try:
                file: io.TextIOBase
                d: dict = yaml.safe_load(file)
                schema = d['schema']
                uid: _identifiers.UniqueIdentifier = _identifiers.ensure_unique_identifier(d['uid'])
                untyped_imports = d['imports'] if 'imports' in d.keys() else tuple()
                imports = Imports(*untyped_imports)
                aliases = None  # To be implemented
                representations: _representation.AbstractRepresentations = _representation.load_abstract_representations(
                    d.get('representations', None),
                    append_representation_renderers=True)
                # Load connectors
                connectors: _formal_language.Connectors = _formal_language.load_connectors(
                    d.get('connectors', None),
                    overwrite_mutable_properties=True)
                pass
                statements = _formal_language.load_statements(d.get('statements', None))
                justifications = _formal_language.Justifications.instantiate_from_list(
                    l=d['justifications'] if 'justifications' in d.keys() else None)
                super().__init__(schema=schema, uid=uid, imports=imports, aliases=aliases,
                                 representations=representations, connectors=connectors, statements=statements,
                                 justifications=justifications)


class MultiBundle(Bundle):
    """A bundle composed of multiple sub-bundles.

    """

    def __init__(self, bundles: tuple[Bundle, ...]):
        # IMPROVEMENT: Validate first that there are no duplicates.
        connectors = tuple(itertools.chain.from_iterable(d.connectors for d in bundles))
        representations = tuple(itertools.chain.from_iterable(d.representations for d in bundles))
        # statements = tuple(itertools.chain.from_iterable(d.statements for d in bundles))
        super().__init__(connectors=connectors, representations=representations)


def load_bundle_from_yaml_file_resource(path: str, resource: str) -> Bundle:
    """Load a bundle from a YAML file in the current Python package resource files.
    """
    package_path = importlib.resources.files(path).joinpath(resource)
    with importlib.resources.as_file(package_path) as yaml_file_path:
        return load_bundle_from_yaml_file(yaml_file_path)


def load_bundle_from_yaml_file(yaml_file_path: int | str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> Bundle:
    """Load a bundle from a YAML file.
    """
    with open(yaml_file_path, 'r') as yaml_file:
        d: dict = yaml.safe_load(yaml_file)
        return load_bundle_from_dict(d=d)


def load_bundle_from_dict(d: dict) -> Bundle:
    """Load a bundle from a raw dictionary.
    """
    bundle: Bundle | None = _identifiers.load_unique_identifiable(o=d)
    if bundle is not None:
        _util.get_logger().debug(f'Bundle already loaded: {bundle}.')
    else:
        # The connector does not exist in memory.

        schema = d['schema']
        uid: _identifiers.UniqueIdentifier = _identifiers.ensure_unique_identifier(d['uid'])
        untyped_imports = d['imports'] if 'imports' in d.keys() else tuple()
        imports = Imports(*untyped_imports)
        aliases = None  # To be implemented
        representations: _representation.AbstractRepresentations = _representation.load_abstract_representations(
            d.get('representations', None),
            append_representation_renderers=True)
        # Load connectors
        connectors: _formal_language.Connectors = _formal_language.load_connectors(
            d.get('connectors', None),
            overwrite_mutable_properties=True)
        statements = _formal_language.load_statements(d.get('statements', None))
        justifications = _formal_language.Justifications.instantiate_from_list(
            l=d['justifications'] if 'justifications' in d.keys() else None)
        bundle: Bundle = Bundle(schema=schema, uid=uid, imports=imports, aliases=aliases,
                                representations=representations, connectors=connectors, statements=statements,
                                justifications=justifications)
    return bundle
