import _util
import _representation
import _formal_language
import _bundling


class LatinAlphabetLowercaseSerifRoman(_bundling.YamlFileBundle):
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'latin_alphabet_lowercase_serif_roman.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _util.get_logger().debug(
                f'LatinAlphabetLowercaseSerifRoman singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(LatinAlphabetLowercaseSerifRoman, cls).__new__(cls)
        return cls._singleton

    @property
    def a(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('a')

    @property
    def b(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('b')

    @property
    def c(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('c')

    @property
    def d(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('d')

    @property
    def e(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('e')

    @property
    def f(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('f')

    @property
    def g(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('g')

    @property
    def h(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('h')

    @property
    def i(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('i')

    @property
    def j(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('j')

    @property
    def k(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('k')

    @property
    def l(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('l')

    @property
    def m(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('m')

    @property
    def n(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('n')

    @property
    def o(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('o')

    @property
    def p(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('p')

    @property
    def q(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('q')

    @property
    def r(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('r')

    @property
    def s(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('s')

    @property
    def t(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('t')

    @property
    def u(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('u')

    @property
    def v(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('v')

    @property
    def w(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('w')

    @property
    def x(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('x')

    @property
    def y(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('y')

    @property
    def z(self) -> _representation.AbstractRepresentation:
        return self.representations.get_from_uuid('z')
