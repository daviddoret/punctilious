import _util
import _representation
import _formal_language
import _bundling


class Operators1Representations(_bundling.YamlFileBundle):
    """A punctilious package of well-known mathematical operators."""
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'operators_1.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _util.get_logger().debug(
                f'Operators1Representations 1 singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(Operators1Representations, cls).__new__(cls)
        return cls._singleton
