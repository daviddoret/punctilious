"""This python module defines the PL1 formal-language."""

from __future__ import annotations

import abc
import typing

import formal_language


class MetaVariable(formal_language.FormalObject):
    def __init__(self):
        super().__init__()


class MetaVariableAccretorTuple(formal_language.AccretorTuple):
    """An accretor for meta-variables."""

    def __init__(self):
        super().__init__(valid_formal_classes=(MetaVariable,))


class MetaLanguage(formal_language.FormalLanguage):
    def __init__(self):
        super().__init__()
        self._variables = MetaVariableAccretorTuple()

    @property
    def variables(self):
        return self._variables


class PropositionalVariable(formal_language.FormalObject):
    def __init__(self):
        super().__init__()


class PropositionalVariableAccretorTuple(formal_language.AccretorTuple):
    def __init__(self):
        super().__init__(valid_formal_classes=(PropositionalVariable,))


class Negation(formal_language.UnaryConnective):
    def __init__(self):
        super().__init__()


class MaterialImplication(formal_language.BinaryConnective):
    """In [Vernant 2022], the term conditional is used instead. The term material-implication is preferred here."""

    def __init__(self):
        super().__init__()


class PropositionalConnectiveAccretorTuple(formal_language.AccretorTuple):
    def __init__(self):
        super().__init__(valid_formal_classes=(MaterialImplication, Negation,))
        self._material_implication = MaterialImplication()
        self.add(self._material_implication)
        self._negation = Negation()
        self.add(self._negation)


class PL1(formal_language.FormalLanguage):
    def __init__(self):
        super().__init__()
        self._metalanguage = MetaLanguage()
        self._connectives = PropositionalConnectiveAccretorTuple()

    @property
    def connectives(self) -> PropositionalConnectiveAccretorTuple:
        return self._connectives

    @property
    def metalanguage(self) -> MetaLanguage:
        return self._metalanguage
