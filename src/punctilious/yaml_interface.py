import uuid

import yaml
import pathlib
import logging


def get_logger():
    # create logger
    logger = logging.getLogger('punctilious')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger


logger = get_logger()


class Imports(tuple):

    def __init__(self, *args):
        pass

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, args)

    def __repr__(self):
        return '(' + ', '.join(str(e) for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(str(e) for e in self) + ')'

    @classmethod
    def instantiate_from_list(cls, l: list):
        typed_l = []
        for d in l:
            o = Import.instantiate_from_dict(d=d)
            typed_l.append(o)
        return Imports(*typed_l)

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Import:
    __slots__ = ('_slug', '_source', '_method')

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self._slug, self._source))

    def __init__(self, slug, source, method):
        self._slug = slug
        self._source = source
        self._method = method

    def __repr__(self):
        return self.slug

    def __str__(self):
        return self.slug

    @classmethod
    def instantiate_from_dict(cls, d: dict | None):
        if d is None:
            d = {}
        slug = d['slug'] if 'slug' in d.keys() else None
        source = d['source'] if 'source' in d.keys() else None
        method = d['method'] if 'method' in d.keys() else None
        o = Import(slug=slug, source=source, method=method)
        return o

    @property
    def method(self):
        return self._method

    @property
    def slug(self):
        return self._slug

    @property
    def source(self):
        return self._source

    def to_dict(self):
        d = {}
        if self.slug is not None:
            d['local_name'] = self.slug
        if self.source is not None:
            d['source'] = self.source
        if self.method is not None:
            d['method'] = self.method
        return d

    def to_yaml(self, default_flow_style):
        yaml.dump(self.to_dict(), default_flow_style=default_flow_style)


class SyntacticRules:
    def __init__(self, fixed_arity=None, min_arity=None, max_arity=None):
        self.fixed_arity = fixed_arity
        self.min_arity = min_arity
        self.max_arity = max_arity

    def __repr__(self):
        formatted_items = [f'{key}: {value}' for key, value in self.to_dict().items()]
        return '(' + ', '.join(formatted_items) + ')'

    def __str__(self):
        formatted_items = [f'{key}: {value}' for key, value in self.to_dict().items()]
        return '(' + ', '.join(formatted_items) + ')'

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

    @classmethod
    def instantiate_from_list(cls, d: dict):
        if d is None:
            d = {}
        fixed_arity = d['fixed_arity'] if 'fixed_arity' in d.keys() else None
        min_arity = d['min_arity'] if 'min_arity' in d.keys() else None
        max_arity = d['max_arity'] if 'max_arity' in d.keys() else None
        o = SyntacticRules(fixed_arity=fixed_arity, min_arity=min_arity, max_arity=max_arity)
        return o


class Configuration:
    """"""
    __slots__ = ('_mode', '_language', '_encoding', '_template')

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self._mode, self._language, self._encoding))

    def __init__(self, mode=None, language=None, encoding=None, template=None):
        self._mode = mode
        self._language = language
        self._encoding = encoding
        self._template = template

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

    @classmethod
    def instantiate_from_dict(cls, d: dict | None):
        if d is None:
            d = {}
        mode = d['mode'] if 'mode' in d.keys() else None
        language = d['language'] if 'language' in d.keys() else None
        encoding = d['encoding'] if 'encoding' in d.keys() else None
        template = d['template'] if 'template' in d.keys() else None
        o = Configuration(mode=mode, language=language, encoding=encoding, template=template)
        return o

    @property
    def mode(self):
        return self._mode

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
        if self.template is not None:
            d['template'] = self.template
        return d

    def to_yaml(self, default_flow_style):
        return yaml.dump(self.to_dict(), default_flow_style=default_flow_style)


class Configurations(tuple):

    def __init__(self, *args):
        pass

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, args)

    def __repr__(self):
        return '(' + ', '.join(e.template for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.template for e in self) + ')'

    @classmethod
    def instantiate_from_list(cls, l: list):
        typed_l = []
        for d in l:
            c = Configuration.instantiate_from_dict(d=d)
            typed_l.append(c)
        o = Configurations(*typed_l)
        return o

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Representations(tuple):

    def __init__(self, *args):
        pass

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, args)

    def __repr__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    @classmethod
    def instantiate_from_list(cls, l: list):
        typed_l = []
        for d in l:
            o = Representation.instantiate_from_dict(d=d)
            typed_l.append(o)
        o = Representations(*typed_l)
        return o

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Representation:
    _in_memory = {}

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self.uuid4))

    def __init__(self, uuid4=None, slug=None, syntactic_rules=None, configurations=None):
        self.uuid4 = uuid4
        self.slug = slug
        self.syntactic_rules = syntactic_rules
        self.configurations = configurations

    def __repr__(self):
        return self.slug

    def __str__(self):
        return self.slug

    @classmethod
    def instantiate_from_dict(cls, d: dict | None, reload: bool = False):
        if d is None:
            d = {}
        uuid4 = d['uuid4']
        if uuid4 in cls._in_memory.keys() and not reload:
            o = cls._in_memory[uuid4]
            logger.debug(f'Reuse {str(o)}({uuid4}).')
            return o
        else:
            o = Representation()
            o.uuid4 = uuid4
            o.slug = d['slug']
            o.syntactic_rules = SyntacticRules.instantiate_from_list(
                d=d['syntactic_rules'] if 'syntactic_rules' in d else None)
            o.configurations = Configurations.instantiate_from_list(
                l=d['configurations'] if 'configurations' in d else None)
            cls._in_memory[uuid4] = o
            return o

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Connectors(tuple):

    def __init__(self, *args):
        pass

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, args)

    def __repr__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    @classmethod
    def instantiate_from_list(cls, l: list):
        typed_l = []
        for d in l:
            o = Connector.instantiate_from_dict(d=d)
            typed_l.append(o)
        return Connectors(*typed_l)

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Connector:
    __slots__ = ('_uuid4', '_slug', '_syntactic_rules', '_representation')
    _uuid4_index = {}

    def __hash__(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self._uuid4))

    def __init__(self, uuid4=None, slug=None, syntactic_rules=None, representation=None):
        self._uuid4 = uuid4
        self._slug = slug
        self._syntactic_rules = syntactic_rules
        self._representation = representation

    def __repr__(self):
        return self.slug

    def __str__(self):
        return self.slug

    @classmethod
    def instantiate_from_dict(cls, d: dict | None, reload: bool = False):
        if d is None:
            d = {}
        uuid4 = d['uuid4']
        if uuid4 in cls._uuid4_index.keys() and not reload:
            logger.debug(f'element {uuid4} skipped because it was already loaded.')
            return cls._uuid4_index[uuid4]
        else:
            slug = d['slug']
            syntactic_rules = SyntacticRules.instantiate_from_list(
                d=d['syntactic_rules'] if 'syntactic_rules' in d.keys() else None)
            representation = None
            o = Connector(uuid4=uuid4, slug=slug, syntactic_rules=syntactic_rules, representation=representation)
            cls._uuid4_index[uuid4] = o
            return o

    @property
    def representation(self):
        return self._representation

    @property
    def slug(self):
        return self._slug

    @property
    def syntactic_rules(self):
        return self._syntactic_rules

    def to_dict(self):
        d = {}
        if self.uuid4 is not None:
            d['uuid4'] = self.uuid4
        if self.slug is not None:
            d['slug'] = self.slug
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


class Theorems(tuple):

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
            o = Theorem.instanciate_from_dict(d=d)
            typed_l.append(o)
        return Connectors(*typed_l)

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Justifications(tuple):

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
            o = Justification.instantiate_from_list(l=d)
            typed_l.append(o)
        return Connectors(*typed_l)

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Package:
    __slots__ = ('_schema', '_uuid4', '_slug', '_imports', '_aliases', '_representations', '_connectors', '_theorems',
                 '_justifications')
    _uuid4_index = {}

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

    @classmethod
    def instantiate_from_dict(cls, d: dict | None, reload: bool = False):
        if d is None:
            d = {}
        uuid4 = d['uuid4']
        if uuid4 in cls._uuid4_index.keys() and not reload:
            reloaded = cls._uuid4_index[uuid4]
            logger.debug(f'package {reloaded}({uuid4}) skipped because it was already loaded.')
            return reloaded
        else:
            schema = d['schema']
            uuid4 = d['uuid4']
            slug = d['slug']
            imports = Imports.instantiate_from_list(
                l=d['imports'] if 'imports' in d.keys() else None)
            aliases = d['aliases']
            representations = Representations.instantiate_from_list(
                l=d['representations'] if 'representations' in d.keys() else None)
            connectors = Connectors.instantiate_from_list(
                l=d['connectors'] if 'connectors' in d.keys() else None)
            theorems = Theorems.instantiate_from_list(
                l=d['theorems'] if 'theorems' in d.keys() else None)
            justifications = Justifications.instantiate_from_list(
                l=d['justifications'] if 'justifications' in d.keys() else None)
            o = Package(schema=schema, uuid4=uuid4, slug=slug, imports=imports, aliases=aliases,
                        representations=representations, connectors=connectors, theorems=theorems,
                        justifications=justifications)
            return o

    @classmethod
    def load_from_yaml(cls, yaml_file_path: pathlib.Path):
        global logger
        d = load_yaml_file_path(yaml_file_path=yaml_file_path)
        o = cls.instantiate_from_dict(d=d)
        logger.info(f'package {yaml_file_path} loaded.')
        return o

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


def load_yaml_file_path(yaml_file_path: pathlib.Path):
    with open(yaml_file_path, 'r') as file:
        d: dict = yaml.safe_load(file)
        return d


p = pathlib.Path('../punctilious_package_1/data/test/test_1.yaml')
d = Package.load_from_yaml(yaml_file_path=p)
print(d)
print('goodbye')
