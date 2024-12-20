import _util
import _representation
import _formal_language
import _bundling


class FormulaNotations(_bundling.YamlFileBundle):
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            path = 'data.representations'
            resource = 'formula_notations.yaml'
            super().__init__(path=path, resource=resource)
            self.__class__._singleton_initialized = True
            _util.get_logger().debug(
                f'FormulaNotations singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(FormulaNotations, cls).__new__(cls)
        return cls._singleton

    @property
    def atomic_formula(self) -> _representation.Representation:
        return self.representations.get_from_uuid('f6bd05d7-ee5b-4480-9d59-ea9fa3a13516')

    @property
    def function_formula(self) -> _representation.Representation:
        return self.representations.get_from_uuid('cd1df2f9-f04d-4321-8430-5191082da985')

    @property
    def infix_formula(self) -> _representation.Representation:
        return self.representations.get_from_uuid('d83bd1a4-97cf-4a7e-975d-21711333b971')

    @property
    def prefix_formula(self) -> _representation.Representation:
        return self.representations.get_from_uuid('af99c47e-c6b8-43e0-a8f4-6331ba79e8fd')
