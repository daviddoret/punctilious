import pathlib
import foundations as _foundations


class OperatorsRepresentation1(_foundations.Package):
    __slots__ = ('_conjunction_representation', '_entailment_representation', '_negation_representation')
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'operators_representation_1.yaml'
            package = _foundations.Package.instantiate_from_python_package_resource(path=path, resource=resource)
            self._conjunction_representation = package.representations['conjunction_representation']
            self._entailment_representation = package.representations['entailment_representation']
            self._negation_representation = package.representations['negation_representation']
            self.__class__._singleton_initialized = True
            _foundations.get_logger().debug(
                f'OperatorsRepresentation1 singleton ({id(self)}) initialized.')

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
