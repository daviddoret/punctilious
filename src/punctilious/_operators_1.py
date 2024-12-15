import _util
import _representation
import _formal_language
import _bundling


class Operators1(_bundling.YamlFileBundle):
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
    def conjunction(self) -> _formal_language.Connector:
        return self.connectors.get_from_identifier('conjunction')

    @property
    def disjunction(self) -> _formal_language.Connector:
        return self.connectors.get_from_identifier('disjunction')

    @property
    def entailment(self) -> _formal_language.Connector:
        return self.connectors.get_from_identifier('entailment')

    @property
    def negation(self) -> _formal_language.Connector:
        return self.connectors.get_from_identifier('negation')
