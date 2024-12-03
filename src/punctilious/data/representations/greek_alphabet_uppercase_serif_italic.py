from ... import foundations as _foundations
from ... import presentation as _presentation


class GreekAlphabetUppercaseSerifItalic(_foundations.PythonPackage):
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'greek_alphabet_uppercase_serif_italic.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _foundations.get_logger().debug(
                f'GreekAlphabetUppercaseSerifItalic singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(GreekAlphabetUppercaseSerifItalic, cls).__new__(cls)
        return cls._singleton

    @property
    def alpha(self) -> _presentation.Representation:
        return self.representations.get_from_slug('alpha')

    @property
    def phi(self) -> _presentation.Representation:
        return self.representations.get_from_slug('phi')

    @property
    def psi(self) -> _presentation.Representation:
        return self.representations.get_from_slug('psi')
