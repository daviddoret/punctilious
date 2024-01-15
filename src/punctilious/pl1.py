"""This python module defines the PL1 formal-language."""

from __future__ import annotations

import abc
import typing

import formal_language


class MetaLanguageConnective(formal_language.Connective):
    def __init__(self):
        super().__init__()


class MetaLanguageVariable(formal_language.AtomicObject):
    def __init__(self):
        super().__init__()


class MetaLanguage(formal_language.FormalLanguage):
    def __init__(self):
        super().__init__()


class PropositionalVariable:
    def __init__(self):
        super().__init__()


class Connective(formal_language.Connective):
    def __init__(self):
        super().__init__()


class Negation(Connective):
    def __init__(self):
        super().__init__()


class MaterialImplication(Connective):
    """In [Vernant 2022], the term conditional is used instead. The term material-implication is preferred here."""

    def __init__(self):
        super().__init__()


class PL1(formal_language.FormalLanguage):
    def __init__(self):
        super().__init__()
