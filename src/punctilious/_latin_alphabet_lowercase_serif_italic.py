import _util
import _representation
import _formal_language
import _bundling


class LatinAlphabetLowercaseSerifItalic(_bundling.YamlFileBundle):
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
        return self.representations.get_from_identifier('a')

    @property
    def b(self) -> _representation.Representation:
        return self.representations.get_from_identifier('b')

    @property
    def c(self) -> _representation.Representation:
        return self.representations.get_from_identifier('c')

    @property
    def d(self) -> _representation.Representation:
        return self.representations.get_from_identifier('d')

    @property
    def e(self) -> _representation.Representation:
        return self.representations.get_from_identifier('e')

    @property
    def f(self) -> _representation.Representation:
        return self.representations.get_from_identifier('f')

    @property
    def g(self) -> _representation.Representation:
        return self.representations.get_from_identifier('g')

    @property
    def h(self) -> _representation.Representation:
        return self.representations.get_from_identifier('h')

    @property
    def i(self) -> _representation.Representation:
        return self.representations.get_from_identifier('i')

    @property
    def j(self) -> _representation.Representation:
        return self.representations.get_from_identifier('j')

    @property
    def k(self) -> _representation.Representation:
        return self.representations.get_from_identifier('k')

    @property
    def l(self) -> _representation.Representation:
        return self.representations.get_from_identifier('l')

    @property
    def m(self) -> _representation.Representation:
        return self.representations.get_from_identifier('m')

    @property
    def n(self) -> _representation.Representation:
        return self.representations.get_from_identifier('n')

    @property
    def o(self) -> _representation.Representation:
        return self.representations.get_from_identifier('o')

    @property
    def p(self) -> _representation.Representation:
        return self.representations.get_from_identifier('p')

    @property
    def q(self) -> _representation.Representation:
        return self.representations.get_from_identifier('q')

    @property
    def r(self) -> _representation.Representation:
        return self.representations.get_from_identifier('r')

    @property
    def s(self) -> _representation.Representation:
        return self.representations.get_from_identifier('s')

    @property
    def t(self) -> _representation.Representation:
        return self.representations.get_from_identifier('t')

    @property
    def u(self) -> _representation.Representation:
        return self.representations.get_from_identifier('u')

    @property
    def v(self) -> _representation.Representation:
        return self.representations.get_from_identifier('v')

    @property
    def w(self) -> _representation.Representation:
        return self.representations.get_from_identifier('w')

    @property
    def x(self) -> _representation.Representation:
        return self.representations.get_from_identifier('x')

    @property
    def y(self) -> _representation.Representation:
        return self.representations.get_from_identifier('y')

    @property
    def z(self) -> _representation.Representation:
        return self.representations.get_from_identifier('z')
