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
    def atomic_formula(self) -> _representation.AbstractRepresentation:
        """A formula representation for atomic formulas of the form: `𝗖` where 𝗖 is the connector.

        :return: A formula representation.
        """
        return self.representations.get_from_uuid('f6bd05d7-ee5b-4480-9d59-ea9fa3a13516', raise_error_if_not_found=True)

    @property
    def function_formula(self) -> _representation.AbstractRepresentation:
        """A formula representation for function formulas of the form: `𝗖(𝗮₁, 𝗮₂, …, 𝗮ₙ)` where 𝗖 is the connector and 𝗮ᵢ
        is an argument.

        :return: A formula representation.
        """
        return self.representations.get_from_uuid('cd1df2f9-f04d-4321-8430-5191082da985', raise_error_if_not_found=True)

    @property
    def infix_formula(self) -> _representation.AbstractRepresentation:
        """A formula representation for infix formulas of the form: `𝗮₁ 𝗖 𝗮₂` where 𝗖 is the connector and 𝗮ᵢ
        is an argument.

        :return: A formula representation.
        """
        return self.representations.get_from_uuid('d83bd1a4-97cf-4a7e-975d-21711333b971', raise_error_if_not_found=True)

    @property
    def prefix_formula(self) -> _representation.AbstractRepresentation:
        """A formula representation for infix formulas of the form: `𝗖𝗮₁` where 𝗖 is the connector and 𝗮ᵢ
        is an argument.

        :return: A formula representation.
        """
        return self.representations.get_from_uuid('ca64ae2f-f8a7-4a87-a99d-57d86a8ba0ad', raise_error_if_not_found=True)

    @property
    def postfix_formula(self) -> _representation.AbstractRepresentation:
        """A formula representation for infix formulas of the form: `𝗮₁𝗖` where 𝗖 is the connector and 𝗮ᵢ
        is an argument.

        :return: A formula representation.
        """
        return self.representations.get_from_uuid('af99c47e-c6b8-43e0-a8f4-6331ba79e8fd', raise_error_if_not_found=True)

    @property
    def system_formula(self) -> _representation.AbstractRepresentation:
        """A formula representation for system formulas of the form: `(𝗖, (𝗮₁, 𝗮₂, …, 𝗮ₙ))` where 𝗖 is the connector
        and 𝗮ᵢ is an argument.

        :return: A formula representation.
        """
        return self.representations.get_from_uuid('8df8b738-3efc-4da5-928a-ea4d7d053598', raise_error_if_not_found=True)
