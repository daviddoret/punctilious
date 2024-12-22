import _util
import _representation
import _bundling

bundle = _bundling.YamlFileBundle(path='data.representations',
                                  resource='latin_alphabet_lowercase_serif_bold.yaml')

a: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('90874c51-f563-47df-85bf-c49384239f55')

b: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('fa676069-09a3-4423-a4b4-9ce2a70b270b')

c: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('c0c98727-d806-4d94-aba5-78f54fddd20b')

d: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('5ce74683-43d9-47d9-bb81-e449d73f20bd')

e: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('38ea17ef-91e1-4990-9f14-4b7d8db6fdab')

f: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('80b9c503-766b-4d4e-8e72-16823b3f6303')

g: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('5657ebe5-945f-4c75-addc-359408c0ea4d')

h: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('e297f5f6-8ce2-4d35-aeb2-9139de51c34b')

i: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('29d5d1ee-8223-41fc-88c3-5428c8df3175')

j: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('4233a1b5-b800-4e46-aeee-d815f77feeb8')

k: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('94125edd-41e4-4179-874d-3efcef65e1fb')

l: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('ae268ed6-8527-43aa-b6e0-569e4332c581')

m: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('55a078ec-a18b-4baf-860b-f9c6a9fbc4ab')

n: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('5f42bd83-c078-4bc4-aa58-6a8c54cb77e2')

o: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('5b48ef44-ffcf-4fa4-91d6-d9986ff3be91')

p: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('a223f8ca-5fa4-4a09-8a61-52422a5de09f')

q: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('499c9ccf-4814-4f27-bf96-684dc5c77ed4')

r: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('624756d9-a896-42b8-bb77-d58c36004dd6')

s: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('735c262b-8116-498b-a029-e9d7e0bb25fa')

t: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('c362261c-fda1-4bc3-9867-580a4e2329f2')

u: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('59c0f877-287e-4155-912d-11a6b640de8a')

v: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('fb9ce8dd-f18c-4a64-a1c2-9b849a29783c')

w: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('0e75f4af-4d40-4f13-8714-1a1874b6b2b7')

x: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('db32652b-c562-4b76-a4c6-55da2647f8b2')

y: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('08a07f8a-a8ff-4421-9522-e39eca19b3d0')

z: _representation.AbstractRepresentation = bundle.representations.get_from_uuid('e29bc832-b331-4c6d-b49e-460dad19b9d2')

_alphabet = {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i, 'j': j, 'k': k, 'l': l, 'm': m,
             'n': n, 'o': o, 'p': p, 'q': q, 'r': r, 's': s, 't': t, 'u': u, 'v': v, 'w': w, 'x': x, 'y': y, 'z': z}


def get_letter(character: str) -> _representation.AbstractRepresentation | None:
    global _alphabet
    return _alphabet.get(character, None)
