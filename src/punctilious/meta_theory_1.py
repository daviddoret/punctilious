# import typing
import sys

import presentation_layer_1 as pl1
import axiomatic_system_1 as as1
from connectives_standard_library_1 import *

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise ImportError(
        'This module does not support being directly executed as a script. Please use the import statement.')

# THIS MUST BE AN ALGORITHMIC INFERENCE-RULE!!!!!!
with as1.let_x_be_a_variable(formula_ts='phi') as phi, as1.let_x_be_a_variable(formula_ts='t') as t:
    is_valid_in: as1.InferenceRule = as1.InferenceRule(
        mechanism=as1.let_x_be_a_transformation(
            premises=(
                t | is_a | theory,
                phi | is_a | formula,
                phi | is_valid_statement_in | t,
            ),
            conclusion=psi,
            variables=(phi, psi,)),
        ref_ts=pl1.Monospace(text='MP'))
    """The modus-ponens inference-rule.

    Abbreviation: MP

    Premises:
     1. phi | is_a | proposition,
     2. psi | is_a | proposition,
     3. phi | implies | psi,
     4. phi

    Conclusion: psi

    Variables: phi, psi
    """
