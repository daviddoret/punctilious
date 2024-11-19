import pathlib
import foundations as _foundations


class Operators:
    __slots__ = ('_conjunction', '_entailment', '_negation')
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.connectors'
            resource = 'operators_1.yaml'
            package = _foundations.Package.instantiate_from_python_package_resource(path=path, resource=resource)
            self._conjunction = package.representations['conjunction_representation']
            self._entailment = package.representations['entailment_representation']
            self._negation = package.representations['negation_representation']
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
