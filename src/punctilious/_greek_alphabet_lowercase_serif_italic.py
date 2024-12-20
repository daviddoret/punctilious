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
    def alpha(self) -> _representation.Representation:
        return self.representations.get_from_uuid('alpha')

    @property
    def beta(self) -> _representation.Representation:
        return self.representations.get_from_uuid('beta')

    @property
    def gamma(self) -> _representation.Representation:
        return self.representations.get_from_uuid('gamma')

    @property
    def delta(self) -> _representation.Representation:
        return self.representations.get_from_uuid('delta')

    @property
    def epsilon(self) -> _representation.Representation:
        return self.representations.get_from_uuid('epsilon')

    @property
    def zeta(self) -> _representation.Representation:
        return self.representations.get_from_uuid('zeta')

    @property
    def eta(self) -> _representation.Representation:
        return self.representations.get_from_uuid('eta')

    @property
    def theta(self) -> _representation.Representation:
        return self.representations.get_from_uuid('theta')

    @property
    def iota(self) -> _representation.Representation:
        return self.representations.get_from_uuid('iota')

    @property
    def kappa(self) -> _representation.Representation:
        return self.representations.get_from_uuid('kappa')

    @property
    def lambda2(self) -> _representation.Representation:
        return self.representations.get_from_uuid('lambda')

    @property
    def mu(self) -> _representation.Representation:
        return self.representations.get_from_uuid('mu')

    @property
    def nu(self) -> _representation.Representation:
        return self.representations.get_from_uuid('nu')

    @property
    def xi(self) -> _representation.Representation:
        return self.representations.get_from_uuid('xi')

    @property
    def omicron(self) -> _representation.Representation:
        return self.representations.get_from_uuid('omicron')

    @property
    def pi(self) -> _representation.Representation:
        return self.representations.get_from_uuid('pi')

    @property
    def rho(self) -> _representation.Representation:
        return self.representations.get_from_uuid('rho')

    @property
    def sigma(self) -> _representation.Representation:
        return self.representations.get_from_uuid('sigma')

    @property
    def tau(self) -> _representation.Representation:
        return self.representations.get_from_uuid('tau')

    @property
    def upsilon(self) -> _representation.Representation:
        return self.representations.get_from_uuid('upsilon')

    @property
    def phi(self) -> _representation.Representation:
        return self.representations.get_from_uuid('phi')

    @property
    def chi(self) -> _representation.Representation:
        return self.representations.get_from_uuid('chi')

    @property
    def psi(self) -> _representation.Representation:
        return self.representations.get_from_uuid('psi')

    @property
    def omega(self) -> _representation.Representation:
        return self.representations.get_from_uuid('omega')
