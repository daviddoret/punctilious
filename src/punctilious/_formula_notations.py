import _util
import _presentation
import _formal_language
import _packaging


class FormulaNotations(_packaging.PythonPackage):
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
    def atomic_formula(self) -> _presentation.Representation:
        return self.representations.get_from_slug('atomic_formula')

    @property
    def function_formula(self) -> _presentation.Representation:
        return self.representations.get_from_slug('function_formula')

    @property
    def infix_formula(self) -> _presentation.Representation:
        return self.representations.get_from_slug('infix_formula')

    @property
    def prefix_formula(self) -> _presentation.Representation:
        return self.representations.get_from_slug('prefix_formula')
