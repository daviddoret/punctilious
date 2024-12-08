import _foundations as _foundations
import _presentation as _presentation


class GreekAlphabetLowercaseSerifItalic(_foundations.PythonPackage):
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'greek_alphabet_lowercase_serif_italic.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _foundations.get_logger().debug(
                f'GreekAlphabetLowercaseSerifItalic singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(GreekAlphabetLowercaseSerifItalic, cls).__new__(cls)
        return cls._singleton

    @property
    def alpha(self) -> _presentation.Representation:
        return self.representations.get_from_slug('alpha')

    @property
    def beta(self) -> _presentation.Representation:
        return self.representations.get_from_slug('beta')

    @property
    def gamma(self) -> _presentation.Representation:
        return self.representations.get_from_slug('gamma')

    @property
    def delta(self) -> _presentation.Representation:
        return self.representations.get_from_slug('delta')

    @property
    def epsilon(self) -> _presentation.Representation:
        return self.representations.get_from_slug('epsilon')

    @property
    def zeta(self) -> _presentation.Representation:
        return self.representations.get_from_slug('zeta')

    @property
    def eta(self) -> _presentation.Representation:
        return self.representations.get_from_slug('eta')

    @property
    def theta(self) -> _presentation.Representation:
        return self.representations.get_from_slug('theta')

    @property
    def iota(self) -> _presentation.Representation:
        return self.representations.get_from_slug('iota')

    @property
    def kappa(self) -> _presentation.Representation:
        return self.representations.get_from_slug('kappa')

    @property
    def lambda2(self) -> _presentation.Representation:
        return self.representations.get_from_slug('lambda')

    @property
    def mu(self) -> _presentation.Representation:
        return self.representations.get_from_slug('mu')

    @property
    def nu(self) -> _presentation.Representation:
        return self.representations.get_from_slug('nu')

    @property
    def xi(self) -> _presentation.Representation:
        return self.representations.get_from_slug('xi')

    @property
    def omicron(self) -> _presentation.Representation:
        return self.representations.get_from_slug('omicron')

    @property
    def pi(self) -> _presentation.Representation:
        return self.representations.get_from_slug('pi')

    @property
    def rho(self) -> _presentation.Representation:
        return self.representations.get_from_slug('rho')

    @property
    def sigma(self) -> _presentation.Representation:
        return self.representations.get_from_slug('sigma')

    @property
    def tau(self) -> _presentation.Representation:
        return self.representations.get_from_slug('tau')

    @property
    def upsilon(self) -> _presentation.Representation:
        return self.representations.get_from_slug('upsilon')

    @property
    def phi(self) -> _presentation.Representation:
        return self.representations.get_from_slug('phi')

    @property
    def chi(self) -> _presentation.Representation:
        return self.representations.get_from_slug('chi')

    @property
    def psi(self) -> _presentation.Representation:
        return self.representations.get_from_slug('psi')

    @property
    def omega(self) -> _presentation.Representation:
        return self.representations.get_from_slug('omega')
