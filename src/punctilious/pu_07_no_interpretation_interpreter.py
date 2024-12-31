"""A catalog of useful interpreters to parse mathematical formulas."""

# external modules

# punctilious modules
import punctilious.pu_01_utilities as _utilities
import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_05_interpretation as _interpretation


def _generate_no_interpretation():
    interpreter = _interpretation.Interpret(
        uid=_identifiers.UniqueIdentifier(
            slug='no_interpretation',
            uuid='ccf14265-c568-4276-bbfc-cf3eec1b625b'),
        atomic_connectors={},
        prefix_connectors={},
        postfix_connectors={},
        infix_connectors={},
        function_connectors={})
    return interpreter


_no_interpreter: _interpretation.Interpret = _generate_no_interpretation()

pass
