import pathlib
import foundations as _foundations


class Operators:
    __slots__ = ('_conjunction', '_entailment', '_negation')
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            _path = pathlib.Path('data/representations/operators_representation_1.yaml')
            _package = _foundations.Package.instantiate_from_yaml_file(yaml_file_path=_path)
            self._conjunction = _package.representations['conjunction']
            self._entailment = _package.representations['entailment']
            self._negation = _package.representations['negation']
            self.__class__._singleton_initialized = True
            _foundations.get_logger().debug(
                f'GreekAlphabetLowercaseSerifItalic singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(Operators, cls).__new__(cls)
            _foundations.get_logger().debug(
                f'Operators singleton ({id(cls._singleton)}) created.')
        return cls._singleton

    @property
    def conjunction(self):
        return self._conjunction

    @property
    def entailment(self):
        return self._entailment

    @property
    def negation(self):
        return self._negation
