import punctilious

from lark import Lark, Transformer, v_args

# Define the Lark grammar
grammar = """
%import common.WORD  
%import common.WS    // Import whitespace handling
%ignore WS           // Ignore whitespace between elements

start: formula

formula: function_notation 
          | infix_operator_notation 
          | infix_operator_notation_with_parenthesis 
          | constant_notation 

connector_slug: /[a-z]/ | /[a-z][a-z0-9_]*[a-z0-9]/

function_notation: connector_slug "(" formula ("," formula)* ")" 

infix_operator_notation: formula connector_slug formula

infix_operator_notation_with_parenthesis: "(" formula connector_slug formula ")"

constant_notation: connector_slug
"""

# Create the Lark parser instance
parser = Lark(grammar, start='start', parser='lalr')


# Transformer class to convert the parse tree into a more usable format
class TreeTransformer(Transformer):

    # Convert formula expressions into a tuple: ('formula', slug, arguments)
    def function_notation(self, items):
        slug = items[0]
        arguments = items[1:]
        return ('formula', slug, arguments)

    # Convert infix expressions into a tuple: ('infix', left, slug, right)
    def connector_slug(self, items):
        slug = items[0]
        return (slug)

    # Convert infix expressions into a tuple: ('infix', left, slug, right)
    def infix_operator_notation(self, items):
        left, slug, right = items
        return ('infix', left, slug, right)

    def infix_operator_notation_with_parenthesis(self, items):
        left, slug, right = items
        return ('infix', left, slug, right)

    # Slugs are returned as a simple value
    def constant_notation(self, items):
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
