import lark


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


class Interpreter:
    _grammar = """
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
        FUNCTION_CONNECTOR . 4 : "not" | "non" | "¬" | "~" | "is-a-proposition" | "is-a-natural-number"
        INFIX_CONNECTOR . 3 : "and" | "et" | "∧" | "^" | "or"
        PREFIX_CONNECTOR . 2 : "not" | "non" | "¬" | "~"
        ATOMIC_CONNECTOR . 1 : "P" | "Q" | "R"

        %import common.WS
        %ignore WS
    """

    def __init__(self):
        self._parser = lark.Lark(Interpreter._grammar, start='start', parser='earley', debug=True)
        self._transformer = Transformer()

    def interpret(self, input_string: str) -> Formula:
        tree = self._parser.parse(input_string)
        print(tree)
        result = self._transformer.transform(tree)
        print(result)
        return result


# Output the parsed structure
interpreter = Interpreter()
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
