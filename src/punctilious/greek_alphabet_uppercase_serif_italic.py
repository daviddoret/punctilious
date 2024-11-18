import pathlib
import foundations as _foundations


class GreekAlphabetUppercaseSerifItalic:
    __slots__ = ('_alpha', '_phi', '_psi')
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            _path = pathlib.Path('data/representations/greek_alphabet_uppercase_serif_italic_representation_1.yaml')
            _package = _foundations.Package.instantiate_from_yaml_file(yaml_file_path=_path)
            self._alpha = _package.representations['alpha']
            self._phi = _package.representations['phi']
            self._psi = _package.representations['psi']
            self.__class__._singleton_initialized = True
            _foundations.get_logger().debug(
                f'GreekAlphabetUppercaseSerifItalic singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(GreekAlphabetUppercaseSerifItalic, cls).__new__(cls)
            _foundations.get_logger().debug(
                f'GreekAlphabetUppercaseSerifItalic singleton ({id(cls._singleton)}) created.')
        return cls._singleton

    @property
    def alpha(self):
        return self._alpha

    @property
    def phi(self):
        return self._phi

    @property
    def psi(self):
        return self._psi
