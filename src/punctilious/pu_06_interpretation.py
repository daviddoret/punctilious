"""The interpretation module contains all the necessary logic to read and decode formal language in strings.
This is necessary to load YAML file statements.
"""

# external modules
import lark
import jinja2
import uuid as uuid_package

# punctilious modules
import punctilious.pu_01_utilities as _utilities
import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_04_formal_language as _formal_language


class Transformer(lark.Transformer):
    """Transformed the Lark tree parsed of a Technical1 input, into a proper Formula."""

    def __init__(self, atomic_connectors: dict, prefix_connectors: dict,
                 postfix_connectors: dict,
                 infix_connectors: dict,
                 function_connectors: dict):
        # self._variable_connectors = variable_connectors
        self._atomic_connectors = atomic_connectors
        self._postfix_connectors = postfix_connectors
        self._prefix_connectors = prefix_connectors
        self._infix_connectors = infix_connectors
        self._function_connectors = function_connectors
        super().__init__()

    def parse_function_formula(self, items) -> _formal_language.Formula:
        """Transform a function with a word and optional arguments."""
        _utilities.get_logger().debug(f'parse function formula: {items}')
        function_connector_terminal = str(items[0])
        if function_connector_terminal not in self._function_connectors.keys():
            _utilities.get_logger().error(f'Unknown function connector: {function_connector_terminal}')
            raise ValueError(f'Unknown function connector: {function_connector_terminal}')
        function_connector = self._function_connectors[function_connector_terminal]
        arguments = items[1] if len(items) > 1 else []
        phi = _formal_language.Formula(function_connector, arguments)
        _utilities.get_logger().debug(f'Parsed function formula: {phi}\n\tSource: {items}')
        return phi

    def parse_function_formula_arguments(self, items):
        """Transform a list of expressions into a Python list."""
        return tuple(items)

    def parse_infix_formula(self, items):
        """Transform a list of expressions into a Python list."""
        _utilities.get_logger().debug(f'parse infix formula: {items}')
        left_operand = items[0]
        if not isinstance(left_operand, _formal_language.Formula):
            raise ValueError(
                f'Infix left_operand was not parsed as Formula. {left_operand}. {type(left_operand).__name__}')
        infix_connector_terminal = str(items[1])
        if infix_connector_terminal not in self._infix_connectors.keys():
            raise ValueError(f'Unknown infix connector: {infix_connector_terminal}')
        infix_connector = self._infix_connectors[infix_connector_terminal]
        right_operand = items[2]
        if not isinstance(right_operand, _formal_language.Formula):
            raise ValueError(
                f'Infix right_operand was not parsed as Formula. {right_operand}. {type(right_operand).__name__}')
        phi = _formal_language.Formula(infix_connector, (left_operand, right_operand,))
        _utilities.get_logger().debug(f'Parsed infix formula: {phi}\n\tSource: {items}')
        return phi

    def parse_prefix_formula(self, items):
        """Transform a list of expressions into a Python list."""
        _utilities.get_logger().debug(f'parse prefix formula: {items}')
        prefix_connector_terminal = items[0][0]
        if prefix_connector_terminal not in self._prefix_connectors.keys():
            _utilities.get_logger().debug(f'Unknown prefix connector: {prefix_connector_terminal}')
            raise ValueError(f'Unknown prefix connector: {prefix_connector_terminal}')
        prefix_connector = self._prefix_connectors[prefix_connector_terminal]
        operand = items[1]
        if not isinstance(operand, _formal_language.Formula):
            raise ValueError(
                f'Prefix operand was not parsed as Formula. {operand}. {type(operand).__name__}')
        phi = _formal_language.Formula(prefix_connector, (operand,))
        _utilities.get_logger().debug(f'Parsed prefix formula: {phi}\n\tSource: {items}')
        return phi

    def parse_postfix_formula(self, items):
        """Transform a list of expressions into a Python list."""
        _utilities.get_logger().debug(f'parse postfix formula: {items}')
        postfix_connector_terminal = str(items[1])
        if postfix_connector_terminal not in self._postfix_connectors.keys():
            _utilities.get_logger().debug(f'Unknown postfix connector: {postfix_connector_terminal}')
            raise ValueError(f'Unknown postfix connector: {postfix_connector_terminal}')
        postfix_connector = self._postfix_connectors[postfix_connector_terminal]
        operand = items[0]
        if not isinstance(operand, _formal_language.Formula):
            raise ValueError(
                f'Postfix operand was not parsed as Formula. {operand}. {type(operand).__name__}')
        phi = _formal_language.Formula(postfix_connector, (operand,))
        _utilities.get_logger().debug(f'Parsed postfix formula: {phi}\n\tSource: {items}')
        return phi

    def parse_atomic_formula(self, items):
        """Transform a list of expressions into a Python list."""
        _utilities.get_logger().debug(f'parse atomic formula: {items}')
        atomic_connector_terminal = items[0][0]
        if atomic_connector_terminal not in self._atomic_connectors.keys():
            _utilities.get_logger().debug(f'Unknown atomic connector: {atomic_connector_terminal}')
            raise ValueError(f'Unknown atomic connector: {atomic_connector_terminal}')
        atomic_connector = self._atomic_connectors[atomic_connector_terminal]
        # arguments = []
        return _formal_language.Formula(atomic_connector)


class Interpreter(_identifiers.UniqueIdentifiable):

    def __init__(self, uid: _identifiers.UniqueIdentifier, atomic_connectors: dict, prefix_connectors: dict,
                 postfix_connectors: dict, infix_connectors: dict, function_connectors: dict):
        self._jinja2_template: jinja2.Template = _utilities.get_jinja2_template_from_package(
            'data.grammars',
            'formula_grammar_5.jinja2')
        self._transformer = Transformer(
            atomic_connectors=atomic_connectors,
            prefix_connectors=prefix_connectors,
            postfix_connectors=postfix_connectors,
            infix_connectors=infix_connectors,
            function_connectors=function_connectors)
        atomic_connectors = self.declare_lark_terminals(terminal_name='ATOMIC_CONNECTOR',
                                                        terminal_priority='2',
                                                        d=atomic_connectors)
        postfix_connectors = self.declare_lark_terminals(terminal_name='POSTFIX_CONNECTOR',
                                                         terminal_priority='3',
                                                         d=postfix_connectors)
        prefix_connectors = self.declare_lark_terminals(terminal_name='PREFIX_CONNECTOR',
                                                        terminal_priority='4',
                                                        d=prefix_connectors)
        infix_connectors = self.declare_lark_terminals(terminal_name='INFIX_CONNECTOR',
                                                       terminal_priority='5',
                                                       d=infix_connectors)
        function_connectors = self.declare_lark_terminals(terminal_name='FUNCTION_CONNECTOR',
                                                          terminal_priority='6',
                                                          d=function_connectors)

        grammar_dict = {
            'atomic_connectors': atomic_connectors,
            'postfix_connectors': postfix_connectors,
            'prefix_connectors': prefix_connectors,
            'infix_connectors': infix_connectors,
            'function_connectors': function_connectors}

        self._grammar = self._jinja2_template.render(grammar_dict)
        # parsers: earley, lalr, cyk
        self._parser = lark.Lark(self._grammar, start='start', parser='earley', debug=True)
        _utilities.get_logger().debug(f'grammar:\n{self._grammar}')
        super().__init__(uid=uid)
        _utilities.get_logger().debug(f'`{repr(self)}` configured.')

    def __repr__(self):
        return f'{self.uid.slug} ({self.uid.uuid}) interpreter'

    def __str__(self):
        return f'`{self.uid.slug}` interpreter'

    def declare_lark_terminals(self, terminal_name, terminal_priority, d: dict):
        """Returns a lark terminals declaration line.
        Sample: TERM . 5 : "and" | "or" | "not"
        """
        lark_terminals_declaration = ''

        if len(d.keys()) == 0:
            # This is a bit ugly, create a fake dictionary to avoid a lark.exceptions.GrammarError.
            d = {str(uuid_package.uuid4()): str(uuid_package.uuid4())}

        lark_terminals_declaration = ' | '.join(
            self.escape_lark_terminal_value(connector) for connector in d.keys())
        lark_terminals_declaration = f'{terminal_name} . {terminal_priority} : {lark_terminals_declaration}'
        return lark_terminals_declaration

    def escape_lark_terminal_value(self, value: str):
        """Return a doubly-quoted lark terminal value.
        Sample: "and"
        """
        return '"' + value.replace('"', '\\"') + '"'

    @property
    def grammar(self):
        return self._grammar

    def interpret(self, input_string: str) -> _formal_language.Formula:
        input_string: str = str(input_string)
        _utilities.get_logger().debug(f'interpretation of string: `{input_string}`')
        tree = self._parser.parse(input_string)
        _utilities.get_logger().debug(f'tree: `{tree}`')
        result = self._transformer.transform(tree)
        _utilities.get_logger().debug(f'string: `{input_string}` interpreted as: {result}')
        return result


pass
