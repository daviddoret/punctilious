"""A catalog of well-known mathematical operators."""

import _bundling

bundle = _bundling.YamlFileBundle(path='data.connectors',
                                  resource='operators_1.yaml')

conjunction = bundle.connectors.get_from_uuid('b5a16d91-9974-48fa-901e-b777eb38e290', raise_error_if_not_found=True)

disjunction = bundle.connectors.get_from_uuid('0fbb1b71-8ffb-483c-9a11-ea990c7f6a2a', raise_error_if_not_found=True)

entailment = bundle.connectors.get_from_uuid('edf63cea-9f29-4bce-aae1-ea8565d69e08', raise_error_if_not_found=True)

negation = bundle.connectors.get_from_uuid('1341a021-0f42-4024-bf87-5fa7767be0ac', raise_error_if_not_found=True)