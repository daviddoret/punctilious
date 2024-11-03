from __future__ import annotations
import json
import jsonschema
import punctilious_package_1
import cons


class Format:
    def __init__(self, snake_case_id: str):
        self.snake_case_id: str = snake_case_id

    def __str__(self):
        return self.snake_case_id

    def __repr__(self):
        return self.snake_case_id


class Formats:
    def __init__(self):
        self._formats = {
            cons.TECHNICAL_1: Format(snake_case_id=cons.TECHNICAL_1),
            cons.UNICODE_1: Format(snake_case_id=cons.UNICODE_1),
            cons.UNICODE_2: Format(snake_case_id=cons.UNICODE_2),
            cons.LATEX_MATH_1: Format(snake_case_id=cons.LATEX_MATH_1)}

    def __getitem__(self, item) -> Format:
        return self._formats[item]

    @property
    def latex_math_1(self):
        return self._formats[cons.LATEX_MATH_1]

    @property
    def technical_1(self):
        return self._formats[cons.TECHNICAL_1]

    @property
    def unicode_1(self):
        return self._formats[cons.UNICODE_1]

    @property
    def unicode_2(self):
        return self._formats[cons.UNICODE_2]


class RepresentationMethod:
    def __init__(self, snake_case_id: str):
        self.snake_case_id: str = snake_case_id

    def __str__(self):
        return self.snake_case_id

    def __repr__(self):
        return self.snake_case_id


class RepresentationMethods:
    def __init__(self):
        self._representation_methods = {
            cons.TEMPLATE_1: Format(snake_case_id=cons.TEMPLATE_1)}

    def __getitem__(self, item) -> Format:
        return self._representation_methods[item]

    @property
    def template_1(self):
        return self._representation_methods[cons.TEMPLATE_1]


class Connector:
    SCHEMA_FILE_PATH: str = '../punctilious_package_1/data/schemas/connector_1.json'
    schema_file = None

    def __init__(self, snake_case_id: str, representation_method: str, arity: int | None,
                 unicode_1_template: str | None,
                 unicode_2_template: str | None, latex_math_1_template: str | None):
        self.snake_case_id: str = snake_case_id
        self.representation_method: str = representation_method
        self.arity: int | None = arity
        self.unicode_1_template: str = unicode_1_template
        self.unicode_2_template: str = unicode_2_template
        self.latex_math_1_template: str = latex_math_1_template

    @classmethod
    def from_json(cls, snake_case_id: str):

        json_file_path: str = f'../punctilious_package_1/data/connectors/{snake_case_id}.json'

        with open(json_file_path, 'r') as f:
            data = json.load(f)

        if Connector.schema_file is None:
            with open(Connector.SCHEMA_FILE_PATH, 'r') as f:
                Connector.schema_file = json.load(f)

        try:
            jsonschema.validate(instance=data, schema=Connector.schema_file)

        except jsonschema.ValidationError as e:
            raise ValueError(f'Invalid JSON data: {e.message}')

        return cls(
            snake_case_id=data['snake_case_id'],
            representation_method=data.get('representation_method'),
            arity=data.get('arity'),
            unicode_1_template=data.get('unicode_1_template'),
            unicode_2_template=data.get('unicode_2_template'),
            latex_math_1_template=data.get('latex_math_1_template')
        )

    def __repr__(self):
        return self.snake_case_id

    def rep(self, args: list[Connector], format: Format) -> str:
        if self.representation_method == cons.TEMPLATE_1:
            if self.arity is not None:
                if self.arity != len(args):
                    raise ValueError(f'The arity of the representation method does not match the number of arguments.')
            if format.snake_case_id == cons.TECHNICAL_1:
                return self.technical_1_template.format(args=args)
            elif format.snake_case_id == cons.UNICODE_1:
                return self.unicode_1_template.format(args=args)
            elif format.snake_case_id == cons.UNICODE_2:
                return self.unicode_2_template.format(args=args)
            elif format.snake_case_id == cons.LATEX_MATH_1:
                return self.latex_math_1_template.format(args=args)
        else:
            raise ValueError(f'Unsupported representation method: {self.representation_method}.')


class Connectors:
    """An in-memory database of well-known connectors, which lazy loads connectors as needed."""

    def __init__(self):
        self._connectors = {}

    def __getitem__(self, snake_case_id: str) -> Connector:
        if snake_case_id not in self._connectors:
            self._connectors[snake_case_id] = Connector.from_json(snake_case_id=snake_case_id)
        return self._connectors[snake_case_id]

    @property
    def conjunction_1(self) -> Connector:
        return self['conjunction_1']

    @property
    def is_a_proposition_predicate_1(self) -> Connector:
        return self['is_a_proposition_predicate_1']


class Symbol:
    SCHEMA_FILE_PATH: str = '../punctilious_package_1/data/schemas/symbol_1.json'
    schema_file = None

    def __init__(self, snake_case_id: str, unicode_1: str, unicode_2: str, latex_math_1: str):
        self.snake_case_id: str = snake_case_id
        self.unicode_1: str = unicode_1
        self.unicode_2: str = unicode_2
        self.latex_math_1: str = latex_math_1

    def __repr__(self):
        return self.snake_case_id

    @property
    def technical_1(self):
        return self.snake_case_id

    @classmethod
    def from_json(cls, snake_case_id: str):

        json_file_path: str = f'../punctilious_package_1/data/symbols/{snake_case_id}.json'

        with open(json_file_path, 'r') as f:
            data = json.load(f)

        if Symbol.schema_file is None:
            with open(Symbol.SCHEMA_FILE_PATH, 'r') as f:
                Symbol.schema_file = json.load(f)

        try:
            jsonschema.validate(instance=data, schema=Symbol.schema_file)

        except jsonschema.ValidationError as e:
            raise ValueError(f'Invalid JSON data: {e.message}')

        return cls(
            snake_case_id=data['snake_case_id'],
            unicode_1=data.get('unicode_1'),
            unicode_2=data.get('unicode_2'),
            latex_math_1=data.get('latex_math_1')
        )

    def rep(self, format: Format) -> str:
        if format.snake_case_id == cons.TECHNICAL_1:
            return self.technical_1
        elif format.snake_case_id == cons.UNICODE_1:
            return self.unicode_1
        elif format.snake_case_id == cons.UNICODE_2:
            return self.unicode_2
        elif format.snake_case_id == cons.LATEX_MATH_1:
            return self.latex_math_1
        else:
            raise ValueError(f'Unsupported format: {format}.')


class Symbols:
    """An in-memory database of well-known symbols, which lazy loads symbols as needed."""

    def __init__(self):
        self._symbols = {}

    def __getitem__(self, snake_case_id: str) -> Symbol:
        if snake_case_id not in self._symbols:
            self._symbols[snake_case_id] = Symbol.from_json(snake_case_id=snake_case_id)
        return self._symbols[snake_case_id]

    @property
    def p_uppercase_serif_italic_1(self) -> Symbol:
        return self['p_uppercase_serif_italic_1']

    @property
    def q_uppercase_serif_italic_1(self) -> Symbol:
        return self['q_uppercase_serif_italic_1']

    @property
    def r_uppercase_serif_italic_1(self) -> Symbol:
        return self['r_uppercase_serif_italic_1']


class Formula:
    def __init__(self, root_connector: Connector, arguments: list[Formula] | None):
        self.root_connector = root_connector
        if arguments is None:
            arguments = ()
        self.arguments = arguments

    def __iter__(self):
        for argument in self.arguments:
            yield argument

    def arity(self) -> int:
        return len(self.arguments)
