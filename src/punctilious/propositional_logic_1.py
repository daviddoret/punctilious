"""A catalog of well-known mathematical operators."""

import _bundling

bundle = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                                       resource='propositional_logic_1.yaml')

bundle2 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
                                                        resource='propositional_logic_1.yaml')

bundle3 = _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.mappings',
                                                        resource='propositional_logic_1.yaml')

is_a_propositional_variable = bundle.connectors.get_from_uuid('81277fd4-280d-4436-a465-79b4e83aadf5',
                                                              raise_error_if_not_found=True)
