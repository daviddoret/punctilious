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
        return self.representations.get_from_identifier('alpha')

    @property
    def beta(self) -> _representation.Representation:
        return self.representations.get_from_identifier('beta')

    @property
    def gamma(self) -> _representation.Representation:
        return self.representations.get_from_identifier('gamma')

    @property
    def delta(self) -> _representation.Representation:
        return self.representations.get_from_identifier('delta')

    @property
    def epsilon(self) -> _representation.Representation:
        return self.representations.get_from_identifier('epsilon')

    @property
    def zeta(self) -> _representation.Representation:
        return self.representations.get_from_identifier('zeta')

    @property
    def eta(self) -> _representation.Representation:
        return self.representations.get_from_identifier('eta')

    @property
    def theta(self) -> _representation.Representation:
        return self.representations.get_from_identifier('theta')

    @property
    def iota(self) -> _representation.Representation:
        return self.representations.get_from_identifier('iota')

    @property
    def kappa(self) -> _representation.Representation:
        return self.representations.get_from_identifier('kappa')

    @property
    def lambda2(self) -> _representation.Representation:
        return self.representations.get_from_identifier('lambda')

    @property
    def mu(self) -> _representation.Representation:
        return self.representations.get_from_identifier('mu')

    @property
    def nu(self) -> _representation.Representation:
        return self.representations.get_from_identifier('nu')

    @property
    def xi(self) -> _representation.Representation:
        return self.representations.get_from_identifier('xi')

    @property
    def omicron(self) -> _representation.Representation:
        return self.representations.get_from_identifier('omicron')

    @property
    def pi(self) -> _representation.Representation:
        return self.representations.get_from_identifier('pi')

    @property
    def rho(self) -> _representation.Representation:
        return self.representations.get_from_identifier('rho')

    @property
    def sigma(self) -> _representation.Representation:
        return self.representations.get_from_identifier('sigma')

    @property
    def tau(self) -> _representation.Representation:
        return self.representations.get_from_identifier('tau')

    @property
    def upsilon(self) -> _representation.Representation:
        return self.representations.get_from_identifier('upsilon')

    @property
    def phi(self) -> _representation.Representation:
        return self.representations.get_from_identifier('phi')

    @property
    def chi(self) -> _representation.Representation:
        return self.representations.get_from_identifier('chi')

    @property
    def psi(self) -> _representation.Representation:
        return self.representations.get_from_identifier('psi')

    @property
    def omega(self) -> _representation.Representation:
        return self.representations.get_from_identifier('omega')
