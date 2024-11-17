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


class Import:
    def __init__(self, local_name, source, method):
        self.local_name = local_name
        self.source = source
        self.method = method

    def __repr__(self):
        return self.to_yaml(default_flow_style=True)

    def __str__(self):
        return self.to_yaml(default_flow_style=True)

    def to_raw(self):
        d = {}
        if self.local_name is not None:
            d['local_name'] = self.local_name
        if self.source is not None:
            d['source'] = self.source
        if self.method is not None:
            d['method'] = self.method
        return d

    def to_yaml(self, default_flow_style):
        yaml.dump(self.to_raw(), default_flow_style=default_flow_style)


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
    def load_from_raw(cls, raw: dict):
        fixed_arity = None
        min_arity = None
        max_arity = None
        if 'fixed_arity' in raw.keys():
            fixed_arity = raw['fixed_arity']
        if 'min_arity' in raw.keys():
            min_arity = raw['min_arity']
        if 'max_arity' in raw.keys():
            max_arity = raw['max_arity']
        o = SyntacticRules(fixed_arity=fixed_arity, min_arity=min_arity, max_arity=max_arity)
        return o


class Configuration:
    def __init__(self, mode=None, language=None, encoding=None, template=None):
        self.mode = mode
        self.language = language
        self.encoding = encoding
        self.template = template

    def __repr__(self):
        return self.template

    def __str__(self):
        return self.template

    @classmethod
    def load_from_raw(cls, raw: dict | None):
        if raw is None:
            raw = {}
        mode = raw['mode'] if 'mode' in raw.keys() else None
        language = raw['language'] if 'language' in raw.keys() else None
        encoding = raw['encoding'] if 'encoding' in raw.keys() else None
        template = raw['template'] if 'template' in raw.keys() else None
        o = Configuration(mode=mode, language=language, encoding=encoding, template=template)
        return o

    def to_raw(self):
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
        return yaml.dump(self.to_raw(), default_flow_style=default_flow_style)


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
    def load_from_raw(cls, raw: list):
        l2 = []
        for c_raw in raw:
            c = Configuration.load_from_raw(raw=c_raw)
            l2.append(c)
        o = Configurations(*l2)
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
    def load_from_raw(cls, raw: list):
        l2 = []
        for c_raw in raw:
            c = Representation.load_from_raw(raw=c_raw)
            l2.append(c)
        o = Representations(*l2)
        return o

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Representation:
    _in_memory = {}

    def __hash__(self):
        return hash((self.uuid4, self.syntactic_rules, self.configurations))

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
    def load_from_raw(cls, raw: dict, reload: bool = False):
        uuid4 = raw['uuid4']
        if uuid4 in cls._in_memory.keys() and not reload:
            logger.debug(f'representation {uuid4} skipped because it was already loaded.')
            return cls._in_memory[uuid4]
        else:
            o = Representation()
            o.uuid4 = uuid4
            o.slug = raw['slug']
            o.syntactic_rules = SyntacticRules.load_from_raw(
                raw=raw['syntactic_rules'] if 'syntactic_rules' in raw else None)
            o.configurations = Configurations.load_from_raw(
                raw=raw['configurations'] if 'configurations' in raw else None)
            cls._in_memory[uuid4] = o
            return o

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Connector:
    _uuid4_index = {}

    def __init__(self):
        self.uuid4 = None
        self.syntactic_rules = None
        self.representation = None

    def __repr__(self):
        return self.to_yaml(default_flow_style=True)

    def __str__(self):
        return self.to_yaml(default_flow_style=True)

    @classmethod
    def load_from_raw(cls, raw: dict, reload: bool = False):
        uuid4 = raw['uuid4']
        if uuid4 in cls._uuid4_index.keys() and not reload:
            logger.debug(f'element {uuid4} skipped because it was already loaded.')
            return cls._uuid4_index[uuid4]
        else:
            o = Connector()
            o.uuid4 = uuid4
            if 'syntactic_rules' in raw:
                o.syntactic_rules = SyntacticRules.load_from_raw(raw=raw['syntactic_rules'])
            r_list = []
            # TODO: Load representation here from local_name
            o.representation = None
            cls._uuid4_index[uuid4] = o
            return o

    def to_raw(self):
        d = {}
        if self.uuid4 is not None:
            d['uuid4'] = self.uuid4
        if self.syntactic_rules is not None:
            d['syntactic_rules'] = self.syntactic_rules
        if self.representation is not None:
            d['representation'] = self.representation
        return d

    def to_yaml(self, default_flow_style):
        return yaml.dump(self.to_raw(), default_flow_style=default_flow_style)


class Package:
    _uuid4_index = {}

    def __init__(self, ):
        self.schema = None
        self.uuid4 = None
        self.imports = None
        self.aliases = None
        self.representations = None
        self.connectors = None

    @classmethod
    def load_from_raw(cls, raw: dict, reload: bool = False):
        uuid4 = raw['uuid4']
        if uuid4 in cls._uuid4_index.keys() and not reload:
            logger.debug(f'package {uuid4} skipped because it was already loaded.')
            return cls._uuid4_index[uuid4]
        else:
            o = Package()
            o.schema = raw['schema']
            o.uuid4 = raw['uuid4']
            i_list = []
            for i_as_dict in raw['imports']:
                # i = Import.load_from_raw(raw=i_as_dict)
                i_list.append(i_as_dict)
            o.imports = i_list
            o.aliases = raw['aliases']
            if raw['representations'] is not None:
                o.representations = Representations.load_from_raw(raw=raw['representations'])
            else:
                o.representations = Representations.load_from_raw(raw=[])
            c_list = []
            for c_as_dict in raw['connectors']:
                c = Connector.load_from_raw(raw=c_as_dict)
                c_list.append(c)
            o.connectors = c_list
            return o

    @classmethod
    def load_from_yaml(cls, yaml_file_path: pathlib.Path):
        global logger
        d = load_yaml_file_path(yaml_file_path=yaml_file_path)
        o = cls.load_from_raw(raw=d)
        logger.info(f'package {yaml_file_path} loaded.')
        return o


def load_yaml_file_path(yaml_file_path: pathlib.Path):
    with open(yaml_file_path, 'r') as file:
        d: dict = yaml.safe_load(file)
        return d


p = pathlib.Path('../punctilious_package_1/data/test/test_1.yaml')
d = Package.load_from_yaml(yaml_file_path=p)
print(d)
print('goodbye')
