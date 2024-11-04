# Representation methods
# TECHNICAL_1: The default method for unambiguous machine-friendly but still human-readable representation.
TECHNICAL_1 = 'technical_1'
# TEMPLATE_1: The default method for human-friendly representation.
TEMPLATE_1 = 'template_1'

# Formats / Encodings
# Ignored by TECHNICAL_1 representation method
UNICODE_1 = 'unicode_1'
UNICODE_2 = 'unicode_2'
LATEX_MATH_1 = 'latex_math_1'

# Lark grammars
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
