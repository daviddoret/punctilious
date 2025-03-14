"""The latin alphabet in uppercase, serif, and italic.

"""
import punctilious_20250223.pu_03_representation as _rpr
import punctilious_20250223.pu_11_bundling as _bnd

_latin_alphabet_uppercase_serif_italic = _bnd.load_bundle_from_yaml_file_resource(
    path='punctilious_20250223.data.representations',
    resource='latin_alphabet_uppercase_serif_italic.yaml')

a: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '6e051a5e-b506-4987-8abc-52a874db5167',
    raise_error_if_not_found=True)

b: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '03716dd9-1d6d-49de-9e68-32ad1bb6f0fa',
    raise_error_if_not_found=True)

c: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    'bf450059-23f8-4aa3-8f59-3a99c0dbef1c',
    raise_error_if_not_found=True)

d: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '12246e24-2727-448b-be6b-5384479e4ba9',
    raise_error_if_not_found=True)

e: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '0e3a8b98-7985-4ea7-a5a3-978c6e662f32',
    raise_error_if_not_found=True)

f: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    'd337fa5b-d0dc-426a-be51-75bdb398175e',
    raise_error_if_not_found=True)

g: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '2ffb6982-5cf4-418f-8db1-7da3244175aa',
    raise_error_if_not_found=True)

h: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '359a06c5-848e-44cf-85b8-2dc96621499d',
    raise_error_if_not_found=True)

i: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '7df4209b-6030-45bb-adcf-dcf192a61387',
    raise_error_if_not_found=True)

j: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '537d05b1-e51a-4226-be70-64da37aa03d2',
    raise_error_if_not_found=True)

k: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '770d954c-abb0-4101-ae1b-4becb6a92f38',
    raise_error_if_not_found=True)

l: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '468b8ebe-8182-49cd-be79-e8acfdc3b4f4',
    raise_error_if_not_found=True)

m: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    'd5bcbd3f-7043-4c18-a805-f365a6cab94a',
    raise_error_if_not_found=True)

n: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    'e93ec289-a813-468e-9001-9a310f94c834',
    raise_error_if_not_found=True)

o: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    'bca0e5d4-66d7-4bec-b2c3-5501933b2035',
    raise_error_if_not_found=True)

p: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    'ccc2166d-26b3-477f-814c-d38a08bc4c1a',
    raise_error_if_not_found=True)

q: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '410d4a1c-8400-44fa-99ad-5ce171c7903a',
    raise_error_if_not_found=True)

r: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '550def99-d785-4db9-8ec4-d31b33fc07a1',
    raise_error_if_not_found=True)

s: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    'f24c3c12-e029-47fb-ba1c-5dd77a780962',
    raise_error_if_not_found=True)

t: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '0a6c69f4-9733-46ac-adc1-478e1db6c1d9',
    raise_error_if_not_found=True)

u: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '466658ea-47d2-4a77-b694-0bcadaeb9b97',
    raise_error_if_not_found=True)

v: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    'f9e352a1-ad9f-4295-8ce3-fed40dc696d7',
    raise_error_if_not_found=True)

w: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '3723ffe0-42b6-49ab-971f-ed6a47176b96',
    raise_error_if_not_found=True)

x: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '1dcba4db-96f8-4f9c-9df6-ac4165eb4f7f',
    raise_error_if_not_found=True)

y: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '8ec6c7da-7f4c-467e-9915-20a659dcafb4',
    raise_error_if_not_found=True)

z: _rpr.AbstractRepresentation = _rpr.load_abstract_representation(
    '3116add7-3977-4fdc-8a6c-ab7d65bdcaf9',
    raise_error_if_not_found=True)

font = _rpr.Font(
    {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i, 'j': j, 'k': k, 'l': l, 'm': m,
     'n': n, 'o': o, 'p': p, 'q': q, 'r': r, 's': s, 't': t, 'u': u, 'v': v, 'w': w, 'x': x, 'y': y, 'z': z})


def get_letter(character: str) -> _rpr.AbstractRepresentation | None:
    global font
    return font.get(character, None)
