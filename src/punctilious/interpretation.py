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
    ?start: expr

    WORD: /[a-z]/ | /[a-z][a-z0-9_]*[a-z0-9]/

    ?expr: WORD "(" [expr_list] ")"       -> parse_function
         | WORD                            -> parse_function
    expr_list: expr ("," expr)*            -> parse_arguments
    
    terminal: "and", "et", "∧", ^"

    // %import common.CNAME -> WORD
    %import common.WS
    %ignore WS
"""

# Define the parser
technical_1_parser = lark.Lark(cons.TECHNICAL_1_GRAMMAR, start='start')


class Technical1Transformer(lark.Transformer):
    """Transformed the Lark tree parsed of a Technical1 input, into a proper Formula."""

    def parse_function(self, items) -> Formula:
        """Transform a function with a word and optional arguments."""
        connector_snake_case_id = items[0]
        connector = Connectors()[connector_snake_case_id]
        args = items[1] if len(items) > 1 else []
        return Formula(root_connector=connector, arguments=args)

    def parse_arguments(self, items):
        """Transform a list of expressions into a Python list."""
        return list(items)
