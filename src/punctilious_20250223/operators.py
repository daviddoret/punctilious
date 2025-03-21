"""Standard representation mappings for the operators in the `operators_1` connectors bundle."""

import punctilious_20250223.pu_02_unique_identifiers as _identifiers
import punctilious_20250223.pu_11_bundling as _bundling

_operators_1_connectors_bundle = _bundling.load_bundle_from_yaml_file_resource(
    path='punctilious_20250223.data.connectors',
    resource='operators.yaml')

conjunction = _identifiers.load_unique_identifiable('b5a16d91-9974-48fa-901e-b777eb38e290',
                                                    raise_error_if_not_found=True)
"""The abstract representation of the logical conjunction connector."""

land = conjunction
"""Alias for `conjunction`."""

and2 = conjunction
"""Alias for `conjunction`."""

disjunction = _identifiers.load_unique_identifiable('0fbb1b71-8ffb-483c-9a11-ea990c7f6a2a',
                                                    raise_error_if_not_found=True)
"""The abstract representation of the logical disjunction connector."""

lor = disjunction
"""Alias for `disjunction`."""

or2 = disjunction
"""Alias for `disjunction`."""

element_of = _identifiers.load_unique_identifiable(
    'bbdb3df8-f516-4605-b3f6-011508ef685c',
    raise_error_if_not_found=True)
"""The abstract representation of the membership operator."""

in2 = element_of
"""Alias for `element_of`."""

entailment = _identifiers.load_unique_identifiable('edf63cea-9f29-4bce-aae1-ea8565d69e08',
                                                   raise_error_if_not_found=True)

negation = _identifiers.load_unique_identifiable('1341a021-0f42-4024-bf87-5fa7767be0ac',
                                                 raise_error_if_not_found=True)

tuple2 = _identifiers.load_unique_identifiable('c138b200-111a-4a40-ac3c-c8afa8e615fb',
                                               raise_error_if_not_found=True)
"""Name `tuple2` is used instead of `tuple` to avoid conflict with the Python reserved word."""

# Load default representations
_bundling.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.representations',
                                              resource='operators.yaml')

# Map default representations to the connectors
_bundling.load_bundle_from_yaml_file_resource(path='punctilious_20250223.data.mappings',
                                              resource='operators.yaml')

pass
