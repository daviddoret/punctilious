import pathlib
import foundations as _foundations


class GreekAlphabetLowercaseSerifItalic:
    __slots__ = ('_alpha', '_phi', '_psi')
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            _path = pathlib.Path('../punctilious_package_1/data/symbols/greek_alphabet_lowercase_serif_italic.yaml')
            _package = _foundations.Package.instantiate_from_yaml_file(yaml_file_path=_path)
            self._alpha = _package.representations['alpha']
            self._phi = _package.representations['phi']
            self._psi = _package.representations['psi']
            self.__class__._singleton_initialized = True

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(GreekAlphabetLowercaseSerifItalic, cls).__new__(cls)
            _foundations.get_logger().debug('GreekAlphabetLowercaseSerifItalic singleton initialized.')
        _foundations.get_logger().debug(id(cls._singleton))
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
