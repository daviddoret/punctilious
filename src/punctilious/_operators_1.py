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
        return self.connectors.get_from_uuid('b5a16d91-9974-48fa-901e-b777eb38e290', raise_error_if_not_found=True)

    @property
    def disjunction(self) -> _formal_language.Connector:
        return self.connectors.get_from_uuid('0fbb1b71-8ffb-483c-9a11-ea990c7f6a2a', raise_error_if_not_found=True)

    @property
    def entailment(self) -> _formal_language.Connector:
        return self.connectors.get_from_uuid('edf63cea-9f29-4bce-aae1-ea8565d69e08', raise_error_if_not_found=True)

    @property
    def negation(self) -> _formal_language.Connector:
        return self.connectors.get_from_uuid('1341a021-0f42-4024-bf87-5fa7767be0ac', raise_error_if_not_found=True)
