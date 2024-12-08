import _foundations as _foundations
import _presentation as _presentation


class LatinAlphabetUppercaseSerifItalic(_foundations.PythonPackage):
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'latin_alphabet_uppercase_serif_italic.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _foundations.get_logger().debug(
                f'LatinAlphabetUppercaseSerifItalic singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(LatinAlphabetUppercaseSerifItalic, cls).__new__(cls)
        return cls._singleton

    @property
    def p(self) -> _presentation.Representation:
        return self.representations.get_from_slug('p')

    @property
    def q(self) -> _presentation.Representation:
        return self.representations.get_from_slug('q')
