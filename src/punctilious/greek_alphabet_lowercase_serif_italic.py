import punctilious.pu_03_representation as _representation
import punctilious.pu_07_bundling as _bundling

_greek_alphabet_lowercase_serif_italic = _bundling.load_bundle_from_yaml_file_resource(
    path='punctilious.data.representations',
    resource='greek_alphabet_lowercase_serif_italic.yaml')

alpha: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'af966a34-70de-4a6a-b558-7abbf2446863', raise_error_if_not_found=True)

beta: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '469ec9d4-2e12-476f-8481-31c6af81aca3', raise_error_if_not_found=True)

gamma: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'b1ac97b8-a6e7-4b67-80eb-f81ef9eb9063', raise_error_if_not_found=True)

delta: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '16bf14cd-9afc-4440-b357-fab02b9b5e42', raise_error_if_not_found=True)

epsilon: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '22a3f9c5-c551-4995-a9c5-fc9d1ab8ddcc', raise_error_if_not_found=True)

zeta: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '1ee46da0-9965-4c7e-802c-5febde2de5ba', raise_error_if_not_found=True)

eta: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '6d026717-63e1-4d4c-a501-e5e928ab44b8', raise_error_if_not_found=True)

theta: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'a3c8444d-6b51-4ab4-8576-769f4dd6510c', raise_error_if_not_found=True)

iota: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '6950e5e9-ebcc-425f-b893-cbb627c3e053', raise_error_if_not_found=True)

kappa: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'c723f39a-a6d9-4714-a1f3-b5a95d34c8b6', raise_error_if_not_found=True)

lambda2: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '2a7b543b-451a-4dd4-a5fc-1bb04d1c5df5', raise_error_if_not_found=True)

mu: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '76680bec-be5e-47fa-ae3b-7e284a718d1d', raise_error_if_not_found=True)

nu: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '17017741-7ff0-4610-a01e-288f2ff0ad8a', raise_error_if_not_found=True)

xi: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'bcd97e99-bab4-4a7b-a0d9-cb563cec365b', raise_error_if_not_found=True)

omicron: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '8ccf8abe-9b59-4155-8baf-4e35dea6617b', raise_error_if_not_found=True)

pi: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    'f1baf6d1-899b-46ee-859f-16f2684aa097', raise_error_if_not_found=True)

rho: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '3ef4b18e-5e14-4199-bd56-1e1003f87059', raise_error_if_not_found=True)

sigma: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '4cb54736-72c0-4d11-b0d3-d8a734c83037', raise_error_if_not_found=True)

tau: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '86f864be-9374-4a12-b0c3-ae5fef923afb', raise_error_if_not_found=True)

upsilon: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '7c79a352-903d-4662-beb3-32b664fb2682', raise_error_if_not_found=True)

phi: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '8359a003-5e6a-47be-bc05-51a3959b237c', raise_error_if_not_found=True)

chi: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '5ead0605-09d5-4d3c-9115-17e91523ba88', raise_error_if_not_found=True)

psi: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '4321183d-3c52-4194-9730-2ff00067d767', raise_error_if_not_found=True)

omega: _representation.AbstractRepresentation = _greek_alphabet_lowercase_serif_italic.representations.get_from_uuid(
    '7f7cd2bb-be7b-49e4-8a4a-ac087a568111', raise_error_if_not_found=True)

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
    'omega': omega
}


def get_letter(character: str) -> _representation.AbstractRepresentation | None:
    global _alphabet
    return _alphabet.get(character, None)
