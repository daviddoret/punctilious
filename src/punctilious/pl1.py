"""This python module defines the PL1 formal-language."""

from __future__ import annotations

import abc
import typing

import formal_language as fl


class MetaVariable(fl.FormalObject):
    def __init__(self):
        super().__init__()


_metavariable_class = fl.FormalPythonClass(python_class=MetaVariable)
"""The class of all PL1 metavariables."""


class MetaVariableAccretorTuple(fl.AccretorTuple):
    """An accretor for meta-variables."""

    def __init__(self):
        super().__init__(valid_formal_classes=(_metavariable_class,))


class MetaLanguage(fl.FormalLanguage):
    def __init__(self):
        super().__init__()
        self._variables = MetaVariableAccretorTuple()
        self.add(x=self._variables)

    @property
    def variables(self):
        return self._variables


class Proposition(fl.FormalObject):
    def __init__(self):
        super().__init__()


_proposition_class = fl.FormalPythonClass(python_class=Proposition)


class PropositionalVariableAccretorTuple(fl.AccretorTuple):
    def __init__(self):
        super().__init__(valid_formal_classes=(_proposition_class,))


class Negation(fl.UnaryConnective):
    def __init__(self):
        super().__init__()


_negation = fl.FormalPythonClass(python_class=Negation)


class MaterialImplication(fl.BinaryConnective):
    """In [Vernant 2022], the term conditional is used instead. The term material-implication is preferred here."""

    def __init__(self):
        super().__init__()


_material_implication = fl.FormalPythonClass(python_class=MaterialImplication)


class PropositionalConnectiveAccretorTuple(fl.AccretorTuple):
    def __init__(self):
        super().__init__(valid_formal_classes=(_material_implication, _negation,))
        self._material_implication = MaterialImplication()
        self.add(x=self._material_implication)
        self._negation = Negation()
        self.add(x=self._negation)

    @property
    def material_implication(self) -> MaterialImplication:
        return self._material_implication

    @property
    def negation(self) -> Negation:
        return self._negation


class PL1(fl.FormalLanguage):
    def __init__(self):
        super().__init__()
        self._metalanguage = MetaLanguage()
        self.add(x=self._metalanguage)
        self._connectives = PropositionalConnectiveAccretorTuple()
        self.add(x=self._connectives)

    @property
    def connectives(self) -> PropositionalConnectiveAccretorTuple:
        return self._connectives

    @property
    def metalanguage(self) -> MetaLanguage:
        return self._metalanguage
