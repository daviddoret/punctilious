"""Bundling refers to the capability to bundle together formal language components,
store them in YAML files or other containers, and reload them from these.

"""

import importlib
import importlib.resources
import typing

import yaml
import io
import uuid as uuid_pkg
import itertools
import _util
import _representation
import _formal_language


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


class Bundle:
    """Inherit from tuple and make it immutable..

    """

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self._uuid))

    def __init__(self, schema=None, uuid=None, slug=None, imports=None, aliases=None, representations=None,
                 connectors=None, theorems=None, justifications=None):
        if uuid is None:
            uuid = uuid_pkg.uuid4()
        if slug is None:
            slug = f'package_{str(uuid).replace('-', '_')}'
        self._schema = schema
        self._uuid = uuid
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
    def uuid(self):
        return self._uuid


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
                file: io.TextIOBase
                d: dict = yaml.safe_load(file)
                schema = d['schema']
                uuid = d['uuid']
                slug = d['slug']
                untyped_imports = d['imports'] if 'imports' in d.keys() else tuple()
                imports = Imports(*untyped_imports)
                aliases = None  # To be implemented
                untyped_representations = d['representations'] if 'representations' in d.keys() else tuple()
                representations = _representation.Representations(*untyped_representations)
                # Load connectors
                typed_connectors = []
                for raw_connector in d['connectors'] if 'connectors' in d.keys() else []:
                    slug = raw_connector['slug']
                    syntactic_rules = _formal_language.ensure_syntactic_rules(o=
                                                                              raw_connector[
                                                                                  'syntactic_rules'] if 'syntactic_rules' in raw_connector.keys() else None)
                    connector_representation_reference = raw_connector.get('connector_representation', None)
                    connector_representation = self._resolve_package_representation_reference(
                        ref=connector_representation_reference,
                        i=imports, r=representations) if connector_representation_reference is not None else None
                    formula_representation_reference = raw_connector.get('formula_representation', None)
                    formula_representation = self._resolve_package_representation_reference(
                        ref=formula_representation_reference,
                        i=imports, r=representations) if formula_representation_reference is not None else None
                    o = _formal_language.Connector(package=self, slug=slug,
                                                   syntactic_rules=syntactic_rules,
                                                   connector_representation=connector_representation,
                                                   formula_representation=formula_representation)
                    typed_connectors.append(o)
                typed_connectors = _formal_language.Connectors(*typed_connectors)
                # Load connectors
                untyped_theorems = d['theorems'] if 'theorems' in d.keys() else tuple()
                theorems = _formal_language.Theorems(*untyped_theorems)
                justifications = _formal_language.Justifications.instantiate_from_list(
                    l=d['justifications'] if 'justifications' in d.keys() else None)
                super().__init__(schema=schema, uuid=uuid, slug=slug, imports=imports, aliases=aliases,
                                 representations=representations, connectors=typed_connectors, theorems=theorems,
                                 justifications=justifications)

    def _resolve_package_representation_reference(self, ref: str, i: Imports,
                                                  r: _representation.Representations):
        """Given the reference of a representation in string format,
        typically as the representation attribute of a connector in a YAML file,
        finds and returns the corresponding representation object, either
        from the local representations, or via an import.

        :param ref:
        :param i: The package imports.
        :param r: The package representations.
        :return:
        """
        ref_tuple: tuple = tuple(ref.split('.'))
        if len(ref_tuple) == 1:
            # This is a local reference.
            r = r.get_from_slug(slug=ref)
            return r
        elif len(ref_tuple) == 2:
            # This is a reference in an imported YAML file.
            p_ref = ref_tuple[0]
            p: Bundle = i.get_from_slug(slug=p_ref).package
            ref = ref_tuple[1]
            r = p.representations.get_from_slug(slug=ref)
            return r
        else:
            raise ValueError(f'Improper reference: "{ref}".')


class MultiBundle(Bundle):
    """A bundle composed of multiple sub-bundles.

    """

    def __init__(self, bundles: tuple[Bundle, ...]):
        # IMPROVEMENT: Validate first that there are no duplicates.
        connectors = tuple(itertools.chain.from_iterable(d.connectors for d in bundles))
        representations = tuple(itertools.chain.from_iterable(d.representations for d in bundles))
        # theorems = tuple(itertools.chain.from_iterable(d.theorems for d in bundles))
        super().__init__(connectors=connectors, representations=representations)
