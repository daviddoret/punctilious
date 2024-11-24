import punctilious

from lark import Lark, Transformer, v_args

# Define the Lark grammar
grammar = """
%import common.WORD  // Import the WORD token for slugs
%import common.WS    // Import whitespace handling
%ignore WS           // Ignore whitespace between elements

start: expression

expression: formula
          | infix_expr
          | infix_expr_with_parenthesis
          | connector_slug

formula: connector_slug "(" expression ("," expression)* ")"

infix_expr: expression connector_slug expression

infix_expr_with_parenthesis: "(" expression connector_slug expression ")"

connector_slug: /[a-z]/ | /[a-z][a-z0-9_]*[a-z0-9]/
"""

# Create the Lark parser instance
parser = Lark(grammar, start='start', parser='lalr')


# Transformer class to convert the parse tree into a more usable format
class TreeTransformer(Transformer):

    # Convert infix expressions into a tuple: ('infix', left, slug, right)
    def infix_expr(self, items):
        left, slug, right = items
        return ('infix', left, slug, right)

    # Convert formula expressions into a tuple: ('formula', slug, arguments)
    def formula(self, items):
        slug = items[0]
        arguments = items[1:]
        return ('formula', slug, arguments)

    def infix_expr_with_parenthesis(self, items):
        left, slug, right = items
        return ('infix', left, slug, right)

    # Slugs are returned as a simple value
    def slug(self, items):
        return items[0].value  # 'value' is the actual string of the slug


# Parse function
def parse_input(input_text):
    # Parse the input text using the parser
    parse_tree = parser.parse(input_text)

    # Use the transformer to convert the parse tree into a more useful format
    transformer = TreeTransformer()
    transformed_tree = transformer.transform(parse_tree)

    return transformed_tree


# Example inputs

# Parse the inputs and print the results
print("Input 1 (Simple slug):")
input1 = "foo"  # Simple slug
print(parse_input(input1))

print("\nInput 2 (Infix expression):")
input2 = "foo bar baz"  # Infix expression
print(parse_input(input2))

print("\nInput 3 (Formula expression):")
input3 = "foo(bar, baz, qux)"  # Formula expression
print(parse_input(input3))

print("\nInput 4 (Formula expression):")
input4 = "foo(bar, baz, zoo qux too)"  # Formula expression
print(parse_input(input4))
