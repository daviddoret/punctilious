"""A catalog of well-known predicates."""

import punctilious.pu_02_unique_identifiers as _uid
import punctilious.pu_11_bundling as _bnd

_bnd.load_bundle_from_yaml_file_resource(path='punctilious.data.connectors',
                                         resource='predicates.yaml')
# _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.representations',
#                                              resource='predicates.yaml')
# _bundling.load_bundle_from_yaml_file_resource(path='punctilious.data.mappings',
#                                              resource='predicates.yaml')

is_a_well_formed_integer_number = _uid.load_unique_identifiable('6c8db03d-926c-4d0c-89b2-fa8318ec983f')
"""The well-known `is-a-well-formed-integer-number` predicate connector from number theory."""

is_a_well_formed_natural_number = _uid.load_unique_identifiable('5be66a92-b1d0-4bc9-9b44-e356f5c15510')
"""The well-known `is-a-well-formed-integer-number` predicate connector from number theory."""
is_a_well_formed_propositional_logic_formula = _uid.load_unique_identifiable(
    '42040abe-47d0-4089-b9f3-9791a6455652')
"""The well-known `is-a-well-formed-integer-number` predicate connector from number theory."""
is_a_well_formed_propositional_logic_variable = _uid.load_unique_identifiable(
    'a8d06d03-8aa6-478c-aecf-d9c3a8701c1c')
"""The well-known `is-a-well-formed-integer-number` predicate connector from number theory."""
is_a_well_formed_rational_number = _uid.load_unique_identifiable('1a920192-94ff-4447-8b46-bdd061845980')
"""The well-known `is-a-well-formed-integer-number` predicate connector from number theory."""
is_a_well_formed_real_number = _uid.load_unique_identifiable('c1fa7584-1ce5-4d1f-850b-7a959c346097')
"""The well-known `is-a-well-formed-integer-number` predicate connector from number theory."""
is_a_well_formed_set = _uid.load_unique_identifiable('f629b6fe-d76a-4855-ae28-1a282732cac4')
"""The well-known `is-a-well-formed-integer-number` predicate connector from number theory."""

pass
