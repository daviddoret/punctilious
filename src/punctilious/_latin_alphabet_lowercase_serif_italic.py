import _util
import _representation
import _formal_language
import _packaging


class LatinAlphabetLowercaseSerifItalic(_packaging.PythonPackage):
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'latin_alphabet_lowercase_serif_italic.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _util.get_logger().debug(
                f'LatinAlphabetLowercaseSerifItalic singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(LatinAlphabetLowercaseSerifItalic, cls).__new__(cls)
        return cls._singleton

    @property
    def a(self) -> _representation.Representation:
        return self.representations.get_from_slug('a')

    @property
    def b(self) -> _representation.Representation:
        return self.representations.get_from_slug('b')

    @property
    def c(self) -> _representation.Representation:
        return self.representations.get_from_slug('c')

    @property
    def d(self) -> _representation.Representation:
        return self.representations.get_from_slug('d')

    @property
    def e(self) -> _representation.Representation:
        return self.representations.get_from_slug('e')

    @property
    def f(self) -> _representation.Representation:
        return self.representations.get_from_slug('f')

    @property
    def g(self) -> _representation.Representation:
        return self.representations.get_from_slug('g')

    @property
    def h(self) -> _representation.Representation:
        return self.representations.get_from_slug('h')

    @property
    def i(self) -> _representation.Representation:
        return self.representations.get_from_slug('i')

    @property
    def j(self) -> _representation.Representation:
        return self.representations.get_from_slug('j')

    @property
    def k(self) -> _representation.Representation:
        return self.representations.get_from_slug('k')

    @property
    def l(self) -> _representation.Representation:
        return self.representations.get_from_slug('l')

    @property
    def m(self) -> _representation.Representation:
        return self.representations.get_from_slug('m')

    @property
    def n(self) -> _representation.Representation:
        return self.representations.get_from_slug('n')

    @property
    def o(self) -> _representation.Representation:
        return self.representations.get_from_slug('o')

    @property
    def p(self) -> _representation.Representation:
        return self.representations.get_from_slug('p')

    @property
    def q(self) -> _representation.Representation:
        return self.representations.get_from_slug('q')

    @property
    def r(self) -> _representation.Representation:
        return self.representations.get_from_slug('r')

    @property
    def s(self) -> _representation.Representation:
        return self.representations.get_from_slug('s')

    @property
    def t(self) -> _representation.Representation:
        return self.representations.get_from_slug('t')

    @property
    def u(self) -> _representation.Representation:
        return self.representations.get_from_slug('u')

    @property
    def v(self) -> _representation.Representation:
        return self.representations.get_from_slug('v')

    @property
    def w(self) -> _representation.Representation:
        return self.representations.get_from_slug('w')

    @property
    def x(self) -> _representation.Representation:
        return self.representations.get_from_slug('x')

    @property
    def y(self) -> _representation.Representation:
        return self.representations.get_from_slug('y')

    @property
    def z(self) -> _representation.Representation:
        return self.representations.get_from_slug('z')
