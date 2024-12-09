import importlib
import yaml
import _util
import _presentation
import _formal_language


class Packages(dict):
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
    __slots__ = ('_schema', '_uuid', '_slug', '_imports', '_aliases', '_representations', '_connectors', '_theorems',
                 '_justifications')

    # _uuid_index = {}

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
                uuid = d['uuid']
                slug = d['slug']
                untyped_imports = d['imports'] if 'imports' in d.keys() else tuple()
                imports = _formal_language.Imports(*untyped_imports)
                aliases = None  # To be implemented
                untyped_representations = d['representations'] if 'representations' in d.keys() else tuple()
                representations = _presentation.Representations(*untyped_representations)
                # Load connectors
                typed_connectors = []
                for raw_connector in d['connectors'] if 'connectors' in d.keys() else []:
                    uuid = raw_connector['uuid']
                    slug = raw_connector['slug']
                    tokens = raw_connector['tokens']
                    syntactic_rules = _formal_language.ensure_syntactic_rules(o=
                                                                              raw_connector[
                                                                                  'syntactic_rules'] if 'syntactic_rules' in raw_connector.keys() else None)
                    representation_reference = raw_connector['representation']
                    representation = self._resolve_package_representation_reference(ref=representation_reference,
                                                                                    i=imports, r=representations)
                    o = _formal_language.Connector(uuid=uuid, slug=slug, tokens=tokens, syntactic_rules=syntactic_rules,
                                                   representation=representation)
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

    def _resolve_package_representation_reference(self, ref: str, i: _formal_language.Imports,
                                                  r: _presentation.Representations):
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
