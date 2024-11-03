# Formats
TECHNICAL_1 = 'technical_1'
UNICODE_1 = 'unicode_1'
UNICODE_2 = 'unicode_2'
LATEX_MATH_1 = 'latex_math_1'

# Representation methods
TEMPLATE_1 = 'template_1'

# Lark grammars
TECHNICAL_1_GRAMMAR = """
    ?start: expr

    WORD: /[a-z]/ | /[a-z][a-z0-9_]*[a-z0-9]/

    ?expr: WORD "(" [expr_list] ")"       -> func
         | WORD                            -> word
    expr_list: expr ("," expr)*            -> expr_list

    // %import common.CNAME -> WORD
    %import common.WS
    %ignore WS
"""
