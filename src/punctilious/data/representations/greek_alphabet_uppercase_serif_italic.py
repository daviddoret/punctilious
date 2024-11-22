from ... import foundations as _foundations


class GreekAlphabetUppercaseSerifItalicPackage(_foundations.PythonPackage):
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'greek_alphabet_uppercase_serif_italic_representation_1.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _foundations.get_logger().debug(
                f'GreekAlphabetUppercaseSerifItalic singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(GreekAlphabetUppercaseSerifItalicPackage, cls).__new__(cls)
            _foundations.get_logger().debug(
                f'GreekAlphabetUppercaseSerifItalic singleton ({id(cls._singleton)}) created.')
        return cls._singleton

    @property
    def alpha(self) -> _foundations.Representation:
        return self.representations['alpha']

    @property
    def phi(self) -> _foundations.Representation:
        return self.representations['phi']

    @property
    def psi(self) -> _foundations.Representation:
        return self.representations['psi']
