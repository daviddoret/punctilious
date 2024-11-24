from ... import foundations as _foundations


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
            _foundations.get_logger().debug(
                f'GreekAlphabetLowercaseSerifItalic singleton ({id(cls._singleton)}) created.')
        return cls._singleton

    @property
    def alpha(self) -> _foundations.Representation:
        return self.representations.get_from_slug('alpha')

    @property
    def phi(self) -> _foundations.Representation:
        return self.representations.get_from_slug('phi')

    @property
    def psi(self) -> _foundations.Representation:
        return self.representations.get_from_slug('psi')
