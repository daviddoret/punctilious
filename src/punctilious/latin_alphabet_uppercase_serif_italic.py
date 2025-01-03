"""The latin alphabet in uppercase, serif, and italic.

"""
import punctilious.pu_03_representation as _representation
import punctilious.pu_10_bundling as _bundling

_latin_alphabet_uppercase_serif_italic = _bundling.load_bundle_from_yaml_file_resource(
    path='punctilious.data.representations',
    resource='latin_alphabet_uppercase_serif_italic.yaml')

a: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '6e051a5e-b506-4987-8abc-52a874db5167',
    raise_error_if_not_found=True)

b: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '03716dd9-1d6d-49de-9e68-32ad1bb6f0fa',
    raise_error_if_not_found=True)

c: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    'bf450059-23f8-4aa3-8f59-3a99c0dbef1c',
    raise_error_if_not_found=True)

d: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '12246e24-2727-448b-be6b-5384479e4ba9',
    raise_error_if_not_found=True)

e: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '0e3a8b98-7985-4ea7-a5a3-978c6e662f32',
    raise_error_if_not_found=True)

f: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    'd337fa5b-d0dc-426a-be51-75bdb398175e',
    raise_error_if_not_found=True)

g: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '2ffb6982-5cf4-418f-8db1-7da3244175aa',
    raise_error_if_not_found=True)

h: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '359a06c5-848e-44cf-85b8-2dc96621499d',
    raise_error_if_not_found=True)

i: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '7df4209b-6030-45bb-adcf-dcf192a61387',
    raise_error_if_not_found=True)

j: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '537d05b1-e51a-4226-be70-64da37aa03d2',
    raise_error_if_not_found=True)

k: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '770d954c-abb0-4101-ae1b-4becb6a92f38',
    raise_error_if_not_found=True)

l: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '468b8ebe-8182-49cd-be79-e8acfdc3b4f4',
    raise_error_if_not_found=True)

m: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    'd5bcbd3f-7043-4c18-a805-f365a6cab94a',
    raise_error_if_not_found=True)

n: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    'e93ec289-a813-468e-9001-9a310f94c834',
    raise_error_if_not_found=True)

o: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    'bca0e5d4-66d7-4bec-b2c3-5501933b2035',
    raise_error_if_not_found=True)

p: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    'ccc2166d-26b3-477f-814c-d38a08bc4c1a',
    raise_error_if_not_found=True)

q: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '410d4a1c-8400-44fa-99ad-5ce171c7903a',
    raise_error_if_not_found=True)

r: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '550def99-d785-4db9-8ec4-d31b33fc07a1',
    raise_error_if_not_found=True)

s: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    'f24c3c12-e029-47fb-ba1c-5dd77a780962',
    raise_error_if_not_found=True)

t: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '0a6c69f4-9733-46ac-adc1-478e1db6c1d9',
    raise_error_if_not_found=True)

u: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '466658ea-47d2-4a77-b694-0bcadaeb9b97',
    raise_error_if_not_found=True)

v: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    'f9e352a1-ad9f-4295-8ce3-fed40dc696d7',
    raise_error_if_not_found=True)

w: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '3723ffe0-42b6-49ab-971f-ed6a47176b96',
    raise_error_if_not_found=True)

x: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '1dcba4db-96f8-4f9c-9df6-ac4165eb4f7f',
    raise_error_if_not_found=True)

y: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '8ec6c7da-7f4c-467e-9915-20a659dcafb4',
    raise_error_if_not_found=True)

z: _representation.AbstractRepresentation = _latin_alphabet_uppercase_serif_italic.representations.get_from_uuid(
    '3116add7-3977-4fdc-8a6c-ab7d65bdcaf9',
    raise_error_if_not_found=True)

_alphabet = {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i, 'j': j, 'k': k, 'l': l, 'm': m,
             'n': n, 'o': o, 'p': p, 'q': q, 'r': r, 's': s, 't': t, 'u': u, 'v': v, 'w': w, 'x': x, 'y': y, 'z': z}


def get_letter(character: str) -> _representation.AbstractRepresentation | None:
    global _alphabet
    return _alphabet.get(character, None)
