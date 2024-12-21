import _util
import _representation
import _formal_language
import _bundling


class GreekAlphabetLowercaseSerifItalic(_bundling.YamlFileBundle):
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'greek_alphabet_lowercase_serif_italic.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _util.get_logger().debug(
                f'GreekAlphabetLowercaseSerifItalic singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(GreekAlphabetLowercaseSerifItalic, cls).__new__(cls)
        return cls._singleton

    @property
    def alpha(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('af966a34-70de-4a6a-b558-7abbf2446863', raise_error_if_not_found=True)

    @property
    def beta(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('469ec9d4-2e12-476f-8481-31c6af81aca3', raise_error_if_not_found=True)

    @property
    def gamma(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('b1ac97b8-a6e7-4b67-80eb-f81ef9eb9063', raise_error_if_not_found=True)

    @property
    def delta(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('16bf14cd-9afc-4440-b357-fab02b9b5e42', raise_error_if_not_found=True)

    @property
    def epsilon(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('22a3f9c5-c551-4995-a9c5-fc9d1ab8ddcc', raise_error_if_not_found=True)

    @property
    def zeta(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('1ee46da0-9965-4c7e-802c-5febde2de5ba', raise_error_if_not_found=True)

    @property
    def eta(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('6d026717-63e1-4d4c-a501-e5e928ab44b8', raise_error_if_not_found=True)

    @property
    def theta(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('a3c8444d-6b51-4ab4-8576-769f4dd6510c', raise_error_if_not_found=True)

    @property
    def iota(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('6950e5e9-ebcc-425f-b893-cbb627c3e053', raise_error_if_not_found=True)

    @property
    def kappa(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('c723f39a-a6d9-4714-a1f3-b5a95d34c8b6', raise_error_if_not_found=True)

    @property
    def lambda2(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('2a7b543b-451a-4dd4-a5fc-1bb04d1c5df5', raise_error_if_not_found=True)

    @property
    def mu(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('76680bec-be5e-47fa-ae3b-7e284a718d1d', raise_error_if_not_found=True)

    @property
    def nu(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('17017741-7ff0-4610-a01e-288f2ff0ad8a', raise_error_if_not_found=True)

    @property
    def xi(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('bcd97e99-bab4-4a7b-a0d9-cb563cec365b', raise_error_if_not_found=True)

    @property
    def omicron(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('8ccf8abe-9b59-4155-8baf-4e35dea6617b', raise_error_if_not_found=True)

    @property
    def pi(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('f1baf6d1-899b-46ee-859f-16f2684aa097', raise_error_if_not_found=True)

    @property
    def rho(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('3ef4b18e-5e14-4199-bd56-1e1003f87059', raise_error_if_not_found=True)

    @property
    def sigma(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('4cb54736-72c0-4d11-b0d3-d8a734c83037', raise_error_if_not_found=True)

    @property
    def tau(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('86f864be-9374-4a12-b0c3-ae5fef923afb', raise_error_if_not_found=True)

    @property
    def upsilon(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('7c79a352-903d-4662-beb3-32b664fb2682', raise_error_if_not_found=True)

    @property
    def phi(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('8359a003-5e6a-47be-bc05-51a3959b237c', raise_error_if_not_found=True)

    @property
    def chi(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('5ead0605-09d5-4d3c-9115-17e91523ba88', raise_error_if_not_found=True)

    @property
    def psi(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('4321183d-3c52-4194-9730-2ff00067d767', raise_error_if_not_found=True)

    @property
    def omega(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('7f7cd2bb-be7b-49e4-8a4a-ac087a568111', raise_error_if_not_found=True)
