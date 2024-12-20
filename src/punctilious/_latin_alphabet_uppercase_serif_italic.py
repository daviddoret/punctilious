import _util
import _representation
import _formal_language
import _bundling


class LatinAlphabetUppercaseSerifItalic(_bundling.YamlFileBundle):
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'latin_alphabet_uppercase_serif_italic.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _util.get_logger().debug(
                f'LatinAlphabetUppercaseSerifItalic singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(LatinAlphabetUppercaseSerifItalic, cls).__new__(cls)
        return cls._singleton

    @property
    def a(self) -> _representation.Representation:
        return self.representations.get_from_uuid('6e051a5e-b506-4987-8abc-52a874db5167')

    @property
    def b(self) -> _representation.Representation:
        return self.representations.get_from_uuid('03716dd9-1d6d-49de-9e68-32ad1bb6f0fa')

    @property
    def c(self) -> _representation.Representation:
        return self.representations.get_from_uuid('bf450059-23f8-4aa3-8f59-3a99c0dbef1c')

    @property
    def d(self) -> _representation.Representation:
        return self.representations.get_from_uuid('12246e24-2727-448b-be6b-5384479e4ba9')

    @property
    def e(self) -> _representation.Representation:
        return self.representations.get_from_uuid('0e3a8b98-7985-4ea7-a5a3-978c6e662f32')

    @property
    def f(self) -> _representation.Representation:
        return self.representations.get_from_uuid('d337fa5b-d0dc-426a-be51-75bdb398175e')

    @property
    def g(self) -> _representation.Representation:
        return self.representations.get_from_uuid('2ffb6982-5cf4-418f-8db1-7da3244175aa')

    @property
    def h(self) -> _representation.Representation:
        return self.representations.get_from_uuid('359a06c5-848e-44cf-85b8-2dc96621499d')

    @property
    def i(self) -> _representation.Representation:
        return self.representations.get_from_uuid('7df4209b-6030-45bb-adcf-dcf192a61387')

    @property
    def j(self) -> _representation.Representation:
        return self.representations.get_from_uuid('537d05b1-e51a-4226-be70-64da37aa03d2')

    @property
    def k(self) -> _representation.Representation:
        return self.representations.get_from_uuid('770d954c-abb0-4101-ae1b-4becb6a92f38')

    @property
    def l(self) -> _representation.Representation:
        return self.representations.get_from_uuid('468b8ebe-8182-49cd-be79-e8acfdc3b4f4')

    @property
    def m(self) -> _representation.Representation:
        return self.representations.get_from_uuid('d5bcbd3f-7043-4c18-a805-f365a6cab94a')

    @property
    def n(self) -> _representation.Representation:
        return self.representations.get_from_uuid('e93ec289-a813-468e-9001-9a310f94c834')

    @property
    def o(self) -> _representation.Representation:
        return self.representations.get_from_uuid('bca0e5d4-66d7-4bec-b2c3-5501933b2035')

    @property
    def p(self) -> _representation.Representation:
        return self.representations.get_from_uuid('ccc2166d-26b3-477f-814c-d38a08bc4c1a')

    @property
    def q(self) -> _representation.Representation:
        return self.representations.get_from_uuid('410d4a1c-8400-44fa-99ad-5ce171c7903a')

    @property
    def r(self) -> _representation.Representation:
        return self.representations.get_from_uuid('550def99-d785-4db9-8ec4-d31b33fc07a1')

    @property
    def s(self) -> _representation.Representation:
        return self.representations.get_from_uuid('f24c3c12-e029-47fb-ba1c-5dd77a780962')

    @property
    def t(self) -> _representation.Representation:
        return self.representations.get_from_uuid('0a6c69f4-9733-46ac-adc1-478e1db6c1d9')

    @property
    def u(self) -> _representation.Representation:
        return self.representations.get_from_uuid('466658ea-47d2-4a77-b694-0bcadaeb9b97')

    @property
    def v(self) -> _representation.Representation:
        return self.representations.get_from_uuid('f9e352a1-ad9f-4295-8ce3-fed40dc696d7')

    @property
    def w(self) -> _representation.Representation:
        return self.representations.get_from_uuid('3723ffe0-42b6-49ab-971f-ed6a47176b96')

    @property
    def x(self) -> _representation.Representation:
        return self.representations.get_from_uuid('1dcba4db-96f8-4f9c-9df6-ac4165eb4f7f')

    @property
    def y(self) -> _representation.Representation:
        return self.representations.get_from_uuid('8ec6c7da-7f4c-467e-9915-20a659dcafb4')

    @property
    def z(self) -> _representation.Representation:
        return self.representations.get_from_uuid('3116add7-3977-4fdc-8a6c-ab7d65bdcaf9')
