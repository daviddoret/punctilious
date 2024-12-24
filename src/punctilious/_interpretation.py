import lark
import jinja2

from punctilious._util import get_logger
import punctilious._formal_language as _formal_language


class Transformer(lark.Transformer):
    """Transformed the Lark tree parsed of a Technical1 input, into a proper Formula."""

    def __init__(self, atomic_connectors: dict, prefix_connectors: dict, infix_connectors: dict,
                 function_connectors: dict):
        self._atomic_connectors = atomic_connectors
        self._prefix_connectors = prefix_connectors
        self._infix_connectors = infix_connectors
        self._function_connectors = function_connectors
        super().__init__()

    def parse_function_formula(self, items) -> _formal_language.Formula:
        """Transform a function with a word and optional arguments."""
        function_connector_terminal = items[0]
        if function_connector_terminal not in self._function_connectors.keys():
            get_logger().error(f'Unknown function connector: {function_connector_terminal}')
            raise ValueError(f'Unknown function connector: {function_connector_terminal}')
        function_connector = self._function_connectors[function_connector_terminal]
        arguments = items[1] if len(items) > 1 else []
        phi = _formal_language.Formula(function_connector, arguments)
        get_logger().debug(f'Parsed function formula: {phi}\n\tSource: {items}')
        return phi

    def parse_function_formula_arguments(self, items):
        """Transform a list of expressions into a Python list."""
        return tuple(items)

    def parse_infix_formula(self, items):
        """Transform a list of expressions into a Python list."""
        left_operand = items[0]
        infix_connector_terminal = items[1]
        if infix_connector_terminal not in self._infix_connectors.keys():
            get_logger().error(f'Unknown infix connector: {infix_connector_terminal}')
            raise ValueError(f'Unknown infix connector: {infix_connector_terminal}')
        infix_connector = self._infix_connectors[infix_connector_terminal]
        right_operand = items[2]
        # arguments = [left_operand, right_operand]
        phi = _formal_language.Formula(infix_connector, (left_operand, right_operand,))
        get_logger().debug(f'Parsed infix formula: {phi}\n\tSource: {items}')
        return phi

    def parse_prefix_formula(self, items):
        """Transform a list of expressions into a Python list."""
        prefix_connector_terminal = items[0]
        if prefix_connector_terminal not in self._prefix_connectors.keys():
            get_logger().error(f'Unknown prefix connector: {prefix_connector_terminal}')
            raise ValueError(f'Unknown prefix connector: {prefix_connector_terminal}')
        prefix_connector = self._prefix_connectors[prefix_connector_terminal]
        operand = items[1]
        phi = _formal_language.Formula(prefix_connector, (operand,))
        get_logger().debug(f'Parsed prefix formula: {phi}\n\tSource: {items}')
        return phi

    def parse_atomic_formula(self, items):
        """Transform a list of expressions into a Python list."""
        atomic_connector_terminal = items[0]
        if atomic_connector_terminal not in self._atomic_connectors.keys():
            get_logger().error(f'Unknown atomic connector: {atomic_connector_terminal}')
            raise ValueError(f'Unknown atomic connector: {atomic_connector_terminal}')
        atomic_connector = self._atomic_connectors[atomic_connector_terminal]
        # arguments = []
        return _formal_language.Formula(atomic_connector)


class Interpreter:

    def __init__(self, atomic_connectors: dict, prefix_connectors: dict, infix_connectors: dict,
                 function_connectors: dict):
        # self._jinja2_template: jinja2.Template = jinja2.Template(self.__class__._GRAMMAR_TEMPLATE)
        self._jinja2_template: jinja2.Template = _util.get_jinja2_template_from_package('data.grammars',
                                                                                        'formula_grammar_1.jinja2')
        self._transformer = Transformer(atomic_connectors=atomic_connectors,
                                        prefix_connectors=prefix_connectors,
                                        infix_connectors=infix_connectors,
                                        function_connectors=function_connectors)
        atomic_connectors = self.declare_lark_terminals(terminal_name='ATOMIC_CONNECTOR',
                                                        terminal_priority='1',
                                                        d=atomic_connectors)
        prefix_connectors = self.declare_lark_terminals(terminal_name='PREFIX_CONNECTOR',
                                                        terminal_priority='2',
                                                        d=prefix_connectors)
        infix_connectors = self.declare_lark_terminals(terminal_name='INFIX_CONNECTOR',
                                                       terminal_priority='3',
                                                       d=infix_connectors)
        function_connectors = self.declare_lark_terminals(terminal_name='FUNCTION_CONNECTOR',
                                                          terminal_priority='4',
                                                          d=function_connectors)
        self._grammar = self._jinja2_template.render({
            'atomic_connectors': atomic_connectors,
            'prefix_connectors': prefix_connectors,
            'infix_connectors': infix_connectors,
            'function_connectors': function_connectors})
        self._parser = lark.Lark(self._grammar, start='start', parser='earley', debug=True)

    def declare_lark_terminals(self, terminal_name, terminal_priority, d: dict):
        """Returns a lark terminals declaration line.
        Sample: TERM . 5 : "and" | "or" | "not"
        """
        lark_terminals_declaration = ''
        if len(d.keys()) > 0:
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
        tree = self._parser.parse(input_string)
        print(tree)
        result = self._transformer.transform(tree)
        print(result)
        return result


pass
