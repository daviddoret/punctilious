import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_03_representation as _representation
import punctilious.pu_11_bundling as _bundling

_greek_alphabet_uppercase_serif_italic = _bundling.load_bundle_from_yaml_file_resource(
    path='punctilious.data.representations',
    resource='greek_alphabet_uppercase_serif_italic.yaml')

alpha: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '0b78780f-1eba-47b6-bb20-36e688abe69e', raise_error_if_not_found=True)

beta: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '955fbd94-208b-41ed-80d8-af76b0165a4c', raise_error_if_not_found=True)

gamma: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    'c8f9f0c8-3ff3-44f7-af59-f8ec673b777d', raise_error_if_not_found=True)

delta: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '6fa30814-b5f5-4826-bab1-f0d6bf0d0db0', raise_error_if_not_found=True)

epsilon: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '9aa47841-845f-41b5-82ea-7a620d843232', raise_error_if_not_found=True)

zeta: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '0a21c25b-9b5d-44e4-a5fa-5e2ac56a61ff', raise_error_if_not_found=True)

eta: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '5ff632bd-25dc-42fb-97e7-62b7d07275fa', raise_error_if_not_found=True)

theta: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '8b89822f-ed39-4459-8635-25dda022898b', raise_error_if_not_found=True)

iota: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '6f0d39a7-7147-4afa-8109-032a3db7e078', raise_error_if_not_found=True)

kappa: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '06ab959a-5e60-43a7-9a6d-666a3469d84e', raise_error_if_not_found=True)

lambda2: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '55c8fd12-d8b6-47ae-a60e-1833776d7afc', raise_error_if_not_found=True)

mu: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    'be530dad-6aec-4e23-a987-431268f29e54', raise_error_if_not_found=True)

nu: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '76f6d9fb-e679-4a01-8a8c-0b73929fb5b6', raise_error_if_not_found=True)

xi: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '4407a62c-baf6-45f6-8cf3-f9842ac6f4a8', raise_error_if_not_found=True)

omicron: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '3d91ccf4-547a-4715-868c-dae76cf1f662', raise_error_if_not_found=True)

pi: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    'a81c2831-32c0-4af2-9e35-188f77b1c02c', raise_error_if_not_found=True)

rho: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    'b155af3f-22d0-4925-b9b6-76956ecb5085', raise_error_if_not_found=True)

sigma: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '5b045e7f-f22e-4f63-a632-2344b294be7a', raise_error_if_not_found=True)

tau: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    'c490c323-8d9c-4a30-8839-1945908c3368', raise_error_if_not_found=True)

upsilon: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    'bd08b70e-5b8b-4a48-b50d-c9708b874611', raise_error_if_not_found=True)

phi: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '0392b688-e665-424d-8d35-e7373f0a223b', raise_error_if_not_found=True)

chi: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '9cb5900e-f898-4ab0-ba6c-652ae8061aaf', raise_error_if_not_found=True)

psi: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '55d0a419-b1b7-456e-8064-1c4fa68161c5', raise_error_if_not_found=True)

omega: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    'b0d2d08a-b0f0-4281-b60a-5fb496b45f26', raise_error_if_not_found=True)

nabla: _representation.AbstractRepresentation = _identifiers.load_unique_identifiable(
    '4d9ae39c-472a-4b50-a3a9-a0cd8ffc5bf0', raise_error_if_not_found=True)

_alphabet = d = {
    'alpha': alpha,
    'beta': beta,
    'gamma': gamma,
    'delta': delta,
    'epsilon': epsilon,
    'zeta': zeta,
    'eta': eta,
    'theta': theta,
    'iota': iota,
    'kappa': kappa,
    'lambda': lambda2,
    'mu': mu,
    'nu': nu,
    'xi': xi,
    'omicron': omicron,
    'pi': pi,
    'rho': rho,
    'sigma': sigma,
    'tau': tau,
    'upsilon': upsilon,
    'phi': phi,
    'chi': chi,
    'psi': psi,
    'omega': omega,
    'nabla': nabla
}


def get_letter(character: str) -> _representation.AbstractRepresentation | None:
    global _alphabet
    return _alphabet.get(character, None)
