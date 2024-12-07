import lark
import jinja2


class Formula:
    def __init__(self, connector, arguments=None):
        if arguments is None:
            arguments = []
        self.connector = connector
        self.arguments = arguments

    def __str__(self):
        return f'{self.connector}({", ".join(map(str, self.arguments))})'


class Transformer(lark.Transformer):
    """Transformed the Lark tree parsed of a Technical1 input, into a proper Formula."""

    def parse_function_formula(self, items) -> Formula:
        """Transform a function with a word and optional arguments."""
        function_connector = items[0]
        arguments = items[1] if len(items) > 1 else []
        return Formula(connector=function_connector, arguments=arguments)

    def parse_function_formula_arguments(self, items):
        """Transform a list of expressions into a Python list."""
        return list(items)

    def parse_infix_formula(self, items):
        """Transform a list of expressions into a Python list."""
        left_operand = items[0]
        infix_connector = items[1]
        right_operand = items[2]
        arguments = [left_operand, right_operand]
        return Formula(connector=infix_connector, arguments=arguments)

    def parse_prefix_formula(self, items):
        """Transform a list of expressions into a Python list."""
        prefix_connector = items[0]
        operand = items[1]
        arguments = [operand, ]
        return Formula(connector=prefix_connector, arguments=arguments)

    def parse_atomic_formula(self, items):
        """Transform a list of expressions into a Python list."""
        atomic_connector = items[0]
        arguments = []
        return Formula(connector=atomic_connector, arguments=arguments)


class Connector:

    def __init__(self, connector: str):
        self.connector = connector

    def __str__(self):
        return self.connector


class Interpreter:
    _GRAMMAR_TEMPLATE = """
        ?start : formula_expression

        ?formula_expression : FUNCTION_CONNECTOR "(" function_formula_arguments ")" -> parse_function_formula
             | formula_expression INFIX_CONNECTOR formula_expression -> parse_infix_formula
             | PREFIX_CONNECTOR ATOMIC_CONNECTOR -> parse_prefix_formula
             | ATOMIC_CONNECTOR -> parse_atomic_formula
             | "(" FUNCTION_CONNECTOR "(" function_formula_arguments ")" ")" -> parse_function_formula
             | "(" formula_expression INFIX_CONNECTOR formula_expression ")" -> parse_infix_formula
             | "(" PREFIX_CONNECTOR ATOMIC_CONNECTOR ")" -> parse_prefix_formula
             | "(" ATOMIC_CONNECTOR ")" -> parse_atomic_formula     

        function_formula_arguments . 20 : formula_expression ("," formula_expression)* -> parse_function_formula_arguments
        parenthesized_formula_expression .10 : "(" formula_expression ")"

        # OPEN_PARENTHESIS : "("
        # CLOSE_PARENTHESIS : ")"
        # COMMA : ","
        {{ function_connectors }}
        {{ infix_connectors }} 
        {{ prefix_connectors }} 
        {{ atomic_connectors }}

        %import common.WS
        %ignore WS
    """

    def __init__(self, atomic_connectors: dict, prefix_connectors: dict, infix_connectors: dict,
                 function_connectors: dict):
        self._atomic_connectors = atomic_connectors
        self._prefix_connectors = prefix_connectors
        self._infix_connectors = infix_connectors
        self._function_connectors = function_connectors
        self._jinja2_template: jinja2.Template = jinja2.Template(self.__class__._GRAMMAR_TEMPLATE)
        self._transformer = Transformer()
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
        lark_terminals_declaration = ''
        if len(d.keys()) > 0:
            lark_terminals_declaration = ' | '.join(
                self.escape_lark_terminal_value(connector) for connector in d.keys())
            lark_terminals_declaration = f'{terminal_name} . {terminal_priority} : {lark_terminals_declaration}'
        return lark_terminals_declaration

    def escape_lark_terminal_value(self, value: str):
        return '"' + value.replace('"', '\\"') + '"'

    @property
    def grammar(self):
        return self._grammar

    def interpret(self, input_string: str) -> Formula:
        tree = self._parser.parse(input_string)
        print(tree)
        result = self._transformer.transform(tree)
        print(result)
        return result


p = Connector('P')
q = Connector('Q')
r = Connector('R')
weird = Connector('weird')
lnot = Connector('not')
land = Connector('and')
is_a_proposition = Connector('is-a-proposition')
atomic_connectors = {'P': p, 'Q': q, 'R': r, '"weird"': weird}
prefix_connectors = {'not': lnot}
infix_connectors = {'and': land}
function_connectors = {'not': lnot, 'is-a-proposition': is_a_proposition}

# Output the parsed structure
interpreter = Interpreter(atomic_connectors=atomic_connectors, prefix_connectors=prefix_connectors,
                          infix_connectors=infix_connectors, function_connectors=function_connectors)
input_string = "is-a-proposition(P)"
formula = interpreter.interpret(input_string)
input_string = "P and Q"
formula = interpreter.interpret(input_string)
input_string = "not P"
formula = interpreter.interpret(input_string)
input_string = "(P and Q)"
formula = interpreter.interpret(input_string)
input_string = "(P and Q) and (Q and P)"
formula = interpreter.interpret(input_string)
input_string = "not(not P)"
formula = interpreter.interpret(input_string)
input_string = "not(not (is-a-proposition(P) and Q) and (Q and P))"
formula = interpreter.interpret(input_string)

pass
