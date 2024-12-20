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
        return self.representations.get_from_uuid('afe52656-2e58-4d44-962d-9626837d1538')

    @property
    def b(self) -> _representation.Representation:
        return self.representations.get_from_uuid('a8537227-dc4e-44f4-aa7e-5ca77ff7f52a')

    @property
    def c(self) -> _representation.Representation:
        return self.representations.get_from_uuid('7eb064c5-04aa-4e50-97ed-2b668740b297')

    @property
    def d(self) -> _representation.Representation:
        return self.representations.get_from_uuid('61e53ead-071f-4ee9-8034-26bbcf473adf')

    @property
    def e(self) -> _representation.Representation:
        return self.representations.get_from_uuid('c7127341-bf02-4906-8ce2-4e5214659aba')

    @property
    def f(self) -> _representation.Representation:
        return self.representations.get_from_uuid('9fdf65e4-6767-4aab-8bae-9eca8fdaeab3')

    @property
    def g(self) -> _representation.Representation:
        return self.representations.get_from_uuid('976458ce-e635-4fc6-9ed3-e51d99262486')

    @property
    def h(self) -> _representation.Representation:
        return self.representations.get_from_uuid('3c5552ce-137e-4335-bb4b-f4264c0c67f5')

    @property
    def i(self) -> _representation.Representation:
        return self.representations.get_from_uuid('f3d34f76-4d13-4c4f-8bf0-7918987ead7b')

    @property
    def j(self) -> _representation.Representation:
        return self.representations.get_from_uuid('9ca1e589-9154-4d3e-9f43-d1b987420d40')

    @property
    def k(self) -> _representation.Representation:
        return self.representations.get_from_uuid('661fcb36-39bc-4b86-bce2-13f74eb6187a')

    @property
    def l(self) -> _representation.Representation:
        return self.representations.get_from_uuid('514e35c2-59fa-4447-9a3d-1dfd538fed4e')

    @property
    def m(self) -> _representation.Representation:
        return self.representations.get_from_uuid('ae96c043-2614-45f2-9654-dce8e798863a')

    @property
    def n(self) -> _representation.Representation:
        return self.representations.get_from_uuid('39839448-063c-44be-967d-f62e55006bca')

    @property
    def o(self) -> _representation.Representation:
        return self.representations.get_from_uuid('c70a20c6-0b0e-482e-a921-54bf940d6fef')

    @property
    def p(self) -> _representation.Representation:
        return self.representations.get_from_uuid('811efd48-e609-4a2a-9e7f-81f1c785a621')

    @property
    def q(self) -> _representation.Representation:
        return self.representations.get_from_uuid('a6345c88-0b14-4765-97c4-2bc76a39a7be')

    @property
    def r(self) -> _representation.Representation:
        return self.representations.get_from_uuid('9b273681-8a5e-4294-bda3-9782ec0735ff')

    @property
    def s(self) -> _representation.Representation:
        return self.representations.get_from_uuid('181b27c0-0126-4853-90c2-a0ce2aaedd23')

    @property
    def t(self) -> _representation.Representation:
        return self.representations.get_from_uuid('dd9ac12f-adc0-41bb-bc31-89398526b11c')

    @property
    def u(self) -> _representation.Representation:
        return self.representations.get_from_uuid('40188d9a-aaa7-439d-a1ca-3a65c2e0ccd5')

    @property
    def v(self) -> _representation.Representation:
        return self.representations.get_from_uuid('cebf8c41-eeb6-4a3c-aa7f-d15decf723d3')

    @property
    def w(self) -> _representation.Representation:
        return self.representations.get_from_uuid('cc26acea-2398-4205-bffa-7dfbf3d7f3fd')

    @property
    def x(self) -> _representation.Representation:
        return self.representations.get_from_uuid('5cc6cc25-11ed-421e-b453-d1afb8c16c99')

    @property
    def y(self) -> _representation.Representation:
        return self.representations.get_from_uuid('45de23e4-815c-4ed6-a4f8-f4446d145edc')

    @property
    def z(self) -> _representation.Representation:
        return self.representations.get_from_uuid('726f2faf-8169-428c-9a2e-46c76989ea57')
