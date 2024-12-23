"""Standard representation mappings for the operators in the `operators_1` connectors bundle."""

import _bundling

_connectors = _bundling.YamlFileBundle(path='data.connectors',
                                       resource='operators_1.yaml')

conjunction = _connectors.connectors.get_from_uuid('b5a16d91-9974-48fa-901e-b777eb38e290',
                                                   raise_error_if_not_found=True)

disjunction = _connectors.connectors.get_from_uuid('0fbb1b71-8ffb-483c-9a11-ea990c7f6a2a',
                                                   raise_error_if_not_found=True)

entailment = _connectors.connectors.get_from_uuid('edf63cea-9f29-4bce-aae1-ea8565d69e08', raise_error_if_not_found=True)

negation = _connectors.connectors.get_from_uuid('1341a021-0f42-4024-bf87-5fa7767be0ac', raise_error_if_not_found=True)

# Load default representations
_bundling.load_bundle_from_yaml_file_resource(path='data.representations',
                                              resource='operators_1.yaml')

# Map default representations to the connectors
_bundling.load_bundle_from_yaml_file_resource(path='data.mappings',
                                              resource='operators_1.yaml')

pass
