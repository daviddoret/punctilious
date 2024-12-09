import _util
import _presentation
import _foundations
import _packaging


class Operators1(_packaging.PythonPackage):
    """A punctilious package of well-known mathematical operators."""
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.connectors'
            resource = 'operators_1.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _util.get_logger().debug(
                f'Operators 1 singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(Operators1, cls).__new__(cls)
        return cls._singleton

    @property
    def conjunction(self) -> _foundations.Connector:
        return self.connectors.get_from_slug('conjunction')

    @property
    def entailment(self) -> _foundations.Connector:
        return self.connectors.get_from_slug('entailment')

    @property
    def entails(self) -> _foundations.Connector:
        return self.connectors.get_from_slug('entails')

    @property
    def land(self) -> _foundations.Connector:
        return self.connectors.get_from_slug('and')

    @property
    def lnot(self) -> _foundations.Connector:
        return self.connectors.get_from_slug('not')

    @property
    def negation(self) -> _foundations.Connector:
        return self.connectors.get_from_slug('negation')
