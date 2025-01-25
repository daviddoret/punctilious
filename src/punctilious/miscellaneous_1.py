import punctilious.pu_02_unique_identifiers as _identifiers
import punctilious.pu_03_representation as _representation
import punctilious.pu_11_bundling as _bundling

_miscellaneous_1 = _bundling.load_bundle_from_yaml_file_resource(
    path='punctilious.data.representations',
    resource='miscellaneous_1.yaml')

empty_string: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '68007b08-f95d-4399-9162-a81dc90e7cfa', raise_error_if_not_found=True)

font = d = {
    'empty_string': empty_string
}


def get_abstract_representation(character: str) -> _representation.AbstractRepresentation | None:
    global font
    return _alphabet.get(character, None)
