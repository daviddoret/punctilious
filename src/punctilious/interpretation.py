import lark

TECHNICAL_1_GRAMMAR = """
    ?start: expr

    WORD: /[a-z]/ | /[a-z][a-z0-9_]*[a-z0-9]/

    ?expr: WORD "(" [expr_list] ")"       -> parse_function
         | WORD                            -> parse_function
    expr_list: expr ("," expr)*            -> parse_arguments

    // %import common.CNAME -> WORD
    %import common.WS
    %ignore WS
"""

TECHNICAL_2_GRAMMAR = """
    ?start : formula_expression

    ?formula_expression : [FUNCTION_CONNECTOR] "(" function_formula_arguments ")" -> parse_function_formula
         | formula_expression [INFIX_CONNECTOR] formula_expression -> parse_infix_formula
         | PREFIX_CONNECTOR [ATOMIC_CONNECTOR] -> parse_prefix_formula
         | ATOMIC_CONNECTOR -> parse_atomic_formula
         
    function_formula_arguments : formula_expression ("," formula_expression)* -> parse_function_formula_arguments
    
    FUNCTION_CONNECTOR . 1 : "is-a-proposition" | "is-a-natural-number"
    INFIX_CONNECTOR . 2 : "and" | "et" | "∧" | "^"
    PREFIX_CONNECTOR . 3 : "not" | "non" | "¬" | "~"
    ATOMIC_CONNECTOR . 4 : "P" | "Q" | "R"
    
    %import common.WS
    %ignore WS
"""


class Formula:
    def __init__(self, connector, arguments=None):
        if arguments is None:
            arguments = []
        self.connector = connector
        self.arguments = arguments

    def __str__(self):
        return f'{self.connector}({", ".join(map(str, self.arguments))})'


class Technical1Transformer(lark.Transformer):
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


def interpret_formula(input_string: str) -> Formula:
    # Define the parser
    parser = lark.Lark(TECHNICAL_2_GRAMMAR, start='start')

    transformer = Technical1Transformer()

    tree = parser.parse(input_string)
    print(tree)
    result = transformer.transform(tree)
    print(result)
    return result


# Output the parsed structure
input_string = "is-a-proposition(P)"
formula = interpret_formula(input_string)

pass
