import _util
import _representation
import _formal_language
import _bundling


class PropositionalLogic1(_bundling.YamlFileBundle):
    """A punctilious package of well-known mathematical operators."""
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.theorems'
            resource = 'propositional_logic_1.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _util.get_logger().debug(
                f'Propositional Logic 1 singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(PropositionalLogic1, cls).__new__(cls)
        return cls._singleton

    @property
    def absorption_law(self) -> _formal_language.Connector:
        return self.connectors.get_from_uuid('absorption_law')

    def declare_variable(self, rep: _representation.AbstractRepresentation) -> _formal_language.Variable:
        v = _formal_language.declare_variable(rep=rep)
        return v
