"""Bundling refers to the capability to bundle together formal language components,
store them in YAML files or other containers, and reload them from these.

"""

# external modules
import importlib
import importlib.resources
import os
import yaml
import io
import itertools
import typing

# punctilious modules
import punctilious.pu_01_utilities as _util
import punctilious.pu_02_unique_identifiers as _identifiers
import punctilious.pu_03_representation as _representation
import punctilious.pu_04_formal_language as _formal_language
import punctilious.pu_08_meta_language as _meta_language
import punctilious.pu_07_interpretation as _interpretation
import punctilious.pu_10_no_interpretation_interpreter as _no_interpretation_interpreter


class Bundles(dict):
    __slots__ = ()
    _singleton = None
    _singleton_initialized = None

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
                 representations=None, connectors=None, statements=None):
        super().__init__(uid=uid)
        self._schema = schema
        self._imports = imports
        self._aliases = aliases
        representations = _representation.ensure_abstract_representations(representations)
        self._representations = representations
        connectors = _formal_language.ensure_connectors(connectors)
        self._connectors = connectors
        self._statements = statements

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
                representations: _representation.AbstractRepresentations = load_abstract_representations(
                    d.get('representations', None),
                    append_representation_renderers=True)
                # Load connectors
                connectors: _formal_language.Connectors = load_connectors(
                    d.get('connectors', None),
                    overwrite_mutable_properties=True)
                pass
                statements = load_statements(d.get('statements', None))
                justifications = _meta_language.Justifications.instantiate_from_list(
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


def load_bundle_from_yaml_file_resource(
        path: str,
        resource: str) -> Bundle:
    """Load a bundle from a YAML file in the current Python package resource files.
    """
    package_path = importlib.resources.files(path).joinpath(resource)
    with importlib.resources.as_file(package_path) as yaml_file_path:
        return load_bundle_from_yaml_file(yaml_file_path)


def load_bundle_from_yaml_file(
        yaml_file_path: int | str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> Bundle:
    """Load a bundle from a YAML file.
    """
    with open(yaml_file_path, 'r') as yaml_file:
        d: dict = yaml.safe_load(yaml_file)
        return load_bundle_from_dict(d=d)


def load_bundle_from_dict(d: dict) -> Bundle:
    """Load a bundle from a raw dictionary.
    """
    bundle: Bundle | None = _identifiers.load_unique_identifiable(o=d, raise_error_if_not_found=False)
    if bundle is not None:
        # _util.get_logger().debug(f'Bundle already loaded: {bundle}.')
        pass
    else:
        # The connector does not exist in memory.

        schema = d['schema']
        uid: _identifiers.UniqueIdentifier = _identifiers.ensure_unique_identifier(d['uid'])
        _util.get_logger().debug(f'Bundle: {uid}')
        interpreter: _interpretation.Interpret | None
        interpreter_uid = d.get('interpreter', None)
        if interpreter_uid is not None:
            # _util.get_logger().debug(f'Interpret UID: {interpreter_uid}')
            interpreter: _interpretation.Interpret = _identifiers.load_unique_identifiable(o=interpreter_uid,
                                                                                           raise_error_if_not_found=False)
            if interpreter_uid is None:
                raise ReferenceError(f'Missing interpreter: {interpreter_uid}')
        else:
            _util.get_logger().debug(f'Interpret UID: None')
            interpreter: _interpretation.Interpret = _no_interpretation_interpreter.get_no_interpretation_interpreter()
        # _util.get_logger().debug(f'Interpret: {interpreter}')
        untyped_imports = d['imports'] if 'imports' in d.keys() else tuple()
        imports = Imports(*untyped_imports)
        aliases = None  # To be implemented
        representations: _representation.AbstractRepresentations = load_abstract_representations(
            d.get('representations', None),
            append_representation_renderers=True)
        # Load connectors
        connectors: _formal_language.Connectors = load_connectors(
            d.get('connectors', None),
            overwrite_mutable_properties=True)
        # statements = load_statements(d.get('statements', None), interpreter=interpreter)
        # justifications = _meta_language.Justifications.instantiate_from_list(
        #     l=d['justifications'] if 'justifications' in d.keys() else None)
        bundle: Bundle = Bundle(schema=schema, uid=uid, imports=imports, aliases=aliases,
                                representations=representations, connectors=connectors)
    return bundle


def load_statement(o: typing.Mapping, interpret: _interpretation.Interpret):
    """Receives a raw Statement, typically from a YAML file, and returns a typed Statement instance.

    Interpret raw strings as formulas.

    :param interpret:
    :param o: a raw Connector.
    :return: a typed Connector instance.
    """
    statement: _meta_language.Statement | None = _identifiers.load_unique_identifiable(o,
                                                                                       raise_error_if_not_found=False)
    if statement is None:
        # The object was not already loaded in memory.

        # Interprets the formulas from the original formulas in raw string format from the YAML file.
        variables = interpret_formulas(o=o.get('variables', None), interpret=interpret)
        premises = interpret_formulas(o=o.get('premises', None), interpret=interpret)
        conclusion = interpret_formula(o=o.get('conclusion', None), interpret=interpret)

        # Prepares the sub-formulas.
        variables = _formal_language.Formula(c=_meta_language.tuple2, a=variables)
        premises = _formal_language.Formula(c=_meta_language.tuple2, a=premises)

        # Prepares the statement formula.
        statement = _formal_language.Formula(c=_meta_language.tuple2, a=(variables, premises, conclusion,))
    else:
        # The representation exists in memory.
        pass
    return statement


def interpret_formula(o: str, interpret: _interpretation.Interpret) -> _interpretation.InterpretedFormula:
    """Parse an original formula in raw string format, and transform it to an InterpretedFormula.

    :param o: the original formula in string format.
    :param interpret: the Interpret able to parse and transform the original formula.
    :return:
    """
    phi: _interpretation.InterpretedFormula = _interpretation.InterpretedFormula(original_formula=o,
                                                                                 interpret=interpret)
    return phi


def interpret_formulas(o: typing.Iterable | None, interpret: _interpretation.Interpret) -> tuple[
    _interpretation.InterpretedFormula, ...]:
    """Receives an iterable collection of original formulas in raw string format, e.g.: from a YAML file,
    and returns a tuple of InterpretedFormulas.

    :param interpret:
    :param o: a raw Connector.
    :return: a typed Connector instance.
    """
    if o is None:
        o = tuple()
    formulas: tuple[_interpretation.InterpretedFormula, ...] = tuple(
        interpret_formula(o=str(i), interpret=interpret) for i in o)
    return formulas


def load_statements(o: typing.Iterable | None, interpreter: _interpretation.Interpret):
    """Receives a raw Statements collection, typically from a YAML file,
    and returns a typed Statements instance.

    :param interpreter:
    :param o: a raw Statements collection.
    :return: a typed Statements instance.
    """
    if o is None:
        o = []
    statements: typing.Union[list, list[_formal_language.Formula, ...]] = []
    for i in o:
        _util.get_logger().debug(f'statement: {i}')
        statement: _formal_language.Formula = load_statement(i, interpret=interpreter)
        statements.append(statement)
    # return _meta_language.Statements(*statements)
    raise NotImplementedError('not implemented.')


def load_abstract_representation(o: typing.Mapping,
                                 append_representation_renderers: bool = False) -> _representation.AbstractRepresentation:
    """Receives a raw Representation, typically from a YAML file, and returns a typed Representation instance.

    :param append_representation_renderers: if the representation is already loaded in memory,
        append new renderers to it.
    :param o: a raw Representation.
    :return: a typed Representation instance.
    """
    representation: _representation.AbstractRepresentation | None = _identifiers.load_unique_identifiable(o,
                                                                                                          raise_error_if_not_found=False)
    if representation is None:
        # The representation does not exist in memory.
        representation = _representation.ensure_abstract_representation(o)
    else:
        # The representation exists in memory.
        if append_representation_renderers:
            # Overwrite the mutable properties.
            if 'renderers' in o.keys():
                new_renderers = _representation.ensure_renderers(o['renderers'])
                # _util.get_logger().debug('new_renderers: {new_renderers}')
                merged_renderers = set(representation.renderers + new_renderers)
                merged_renderers = _representation.Renderers(*merged_renderers)
                representation.renderers = merged_renderers
    return representation


def load_abstract_representations(o: typing.Iterable | None,
                                  append_representation_renderers: bool = False) -> _representation.AbstractRepresentations:
    """Receives a raw Representations collection, typically from a YAML file,
    and returns a typed Representations instance.

    :param append_representation_renderers: if representations are already loaded in memory,
        append new renderers to the existing representations.
    :param o: a raw Representations collection.
    :return: a typed Representations instance.
    """
    if o is None:
        o = []
    representations: list[_representation.AbstractRepresentation] = []
    for i in o:
        representation: _representation.AbstractRepresentation = load_abstract_representation(
            i, append_representation_renderers=append_representation_renderers)
        representations.append(representation)
    return _representation.AbstractRepresentations(*representations)


def load_connector(o: typing.Mapping, overwrite_mutable_properties: bool = False) -> _formal_language.Connector:
    """Receives a raw Connector, typically from a YAML file, and returns a typed Connector instance.

    :param overwrite_mutable_properties: if `o` is already loaded in memory, overwrite its mutable properties:
        `connector_representation`, and `formula_representation`.
    :param o: a raw Connector.
    :return: a typed Connector instance.
    """
    connector: _formal_language.Connector | None = _identifiers.load_unique_identifiable(o,
                                                                                         raise_error_if_not_found=False)
    if connector is None:
        # The connector does not exist in memory.
        connector = _formal_language.ensure_connector(o)
    else:
        # The connector exists in memory.
        if overwrite_mutable_properties:
            # Overwrite the mutable properties.
            if 'connector_representation' in o.keys():
                connector.connector_representation = load_abstract_representation(
                    o['connector_representation'])
            if 'formula_representation' in o.keys():
                connector.formula_representation = load_abstract_representation(
                    o['formula_representation'])
    return connector


def load_connectors(o: typing.Iterable | None,
                    overwrite_mutable_properties: bool = False) -> _formal_language.Connectors:
    """Receives a raw Connectors collection, typically from a YAML file,
    and returns a typed Connectors instance.

    :param overwrite_mutable_properties: if connectors are already loaded in memory, overwrite their mutable properties:
        `connector_representation`, and `formula_representation`.
    :param o: a raw Connectors collection.
    :return: a typed Connectors instance.
    """
    if o is None:
        o = []
    connectors: list[_formal_language.Connector] = []
    for i in o:
        connector: _formal_language.Connector = load_connector(
            i,
            overwrite_mutable_properties=overwrite_mutable_properties)
        connectors.append(connector)
    return _formal_language.Connectors(*connectors)
