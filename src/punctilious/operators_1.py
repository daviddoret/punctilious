import pathlib
import foundations as _foundations


class Operators(_foundations.PythonPackage):
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.connectors'
            resource = 'operators_1.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _foundations.get_logger().debug(
                f'Operators singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(Operators, cls).__new__(cls)
            _foundations.get_logger().debug(
                f'Operators singleton ({id(cls._singleton)}) created.')
        return cls._singleton

    @property
    def conjunction(self) -> _foundations.Connector:
        return self.connectors['conjunction']

    @property
    def entailment(self) -> _foundations.Connector:
        return self.connectors['entailment']

    @property
    def negation(self) -> _foundations.Connector:
        return self.connectors['negation']
