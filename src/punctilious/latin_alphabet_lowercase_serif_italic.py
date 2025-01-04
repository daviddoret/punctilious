"""The latin alphabet in lowercase, serif, and italic.

"""
import punctilious.pu_03_representation as _representation
import punctilious.pu_11_bundling as _bundling

_latin_alphabet_lowercase_serif_italic = _bundling.load_bundle_from_yaml_file_resource(
    path='punctilious.data.representations',
    resource='latin_alphabet_lowercase_serif_italic.yaml')

a: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'afe52656-2e58-4d44-962d-9626837d1538',
    raise_error_if_not_found=True)

b: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'a8537227-dc4e-44f4-aa7e-5ca77ff7f52a',
    raise_error_if_not_found=True)

c: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '7eb064c5-04aa-4e50-97ed-2b668740b297',
    raise_error_if_not_found=True)

d: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '61e53ead-071f-4ee9-8034-26bbcf473adf',
    raise_error_if_not_found=True)

e: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'c7127341-bf02-4906-8ce2-4e5214659aba',
    raise_error_if_not_found=True)

f: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '9fdf65e4-6767-4aab-8bae-9eca8fdaeab3',
    raise_error_if_not_found=True)

g: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '976458ce-e635-4fc6-9ed3-e51d99262486',
    raise_error_if_not_found=True)

h: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '3c5552ce-137e-4335-bb4b-f4264c0c67f5',
    raise_error_if_not_found=True)

i: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'f3d34f76-4d13-4c4f-8bf0-7918987ead7b',
    raise_error_if_not_found=True)

j: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '9ca1e589-9154-4d3e-9f43-d1b987420d40',
    raise_error_if_not_found=True)

k: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '661fcb36-39bc-4b86-bce2-13f74eb6187a',
    raise_error_if_not_found=True)

l: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '514e35c2-59fa-4447-9a3d-1dfd538fed4e',
    raise_error_if_not_found=True)

m: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'ae96c043-2614-45f2-9654-dce8e798863a',
    raise_error_if_not_found=True)

n: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '39839448-063c-44be-967d-f62e55006bca',
    raise_error_if_not_found=True)

o: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'c70a20c6-0b0e-482e-a921-54bf940d6fef',
    raise_error_if_not_found=True)

p: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '811efd48-e609-4a2a-9e7f-81f1c785a621',
    raise_error_if_not_found=True)

q: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'a6345c88-0b14-4765-97c4-2bc76a39a7be',
    raise_error_if_not_found=True)

r: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '9b273681-8a5e-4294-bda3-9782ec0735ff',
    raise_error_if_not_found=True)

s: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '181b27c0-0126-4853-90c2-a0ce2aaedd23',
    raise_error_if_not_found=True)

t: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'dd9ac12f-adc0-41bb-bc31-89398526b11c',
    raise_error_if_not_found=True)

u: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '40188d9a-aaa7-439d-a1ca-3a65c2e0ccd5',
    raise_error_if_not_found=True)

v: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'cebf8c41-eeb6-4a3c-aa7f-d15decf723d3',
    raise_error_if_not_found=True)

w: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'cc26acea-2398-4205-bffa-7dfbf3d7f3fd',
    raise_error_if_not_found=True)

x: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '5cc6cc25-11ed-421e-b453-d1afb8c16c99',
    raise_error_if_not_found=True)

y: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '45de23e4-815c-4ed6-a4f8-f4446d145edc',
    raise_error_if_not_found=True)

z: _representation.AbstractRepresentation = _latin_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '726f2faf-8169-428c-9a2e-46c76989ea57',
    raise_error_if_not_found=True)

_alphabet = {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i, 'j': j, 'k': k, 'l': l, 'm': m,
             'n': n, 'o': o, 'p': p, 'q': q, 'r': r, 's': s, 't': t, 'u': u, 'v': v, 'w': w, 'x': x, 'y': y, 'z': z}


def get_letter(character: str) -> _representation.AbstractRepresentation | None:
    global _alphabet
    return _alphabet.get(character, None)
