from __future__ import annotations

import abc
import typing
import os
import csv
import warnings
import logging


class Protocol:
    """A typesetting technical protocol."""

    def __init__(self, name: str):
        self._name: str = name

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name


class Protocols:
    """A catalog of out-of-the-box typesetting protocols."""

    def __init__(self):
        self._latex = Protocol('LaTeX')
        self._unicode_limited = Protocol('Plain text')
        self._unicode_extended = Protocol('Unicode')
        self._default = self._unicode_limited
        self._fail_safe = self._unicode_limited

    @property
    def default(self) -> Protocol:
        """If no protocol is specified, typesetting uses the default protocol."""
        return self._default

    @property
    def fail_safe(self) -> Protocol:
        """If neither the specified protocol, nor the default protocol are supported, typesetting uses the fail-safe
        protocol."""
        return self._fail_safe

    @property
    def latex(self) -> Protocol:
        """The LaTeX rendering protocol. Uses LaTeX math for formulae, and LaTeX for general text."""
        return self._latex

    @property
    def unicode_limited(self) -> Protocol:
        """The unicode-limited rendering protocol. Uses a limited character set that is assumed to be supported in all computing environments."""
        return self._unicode_limited

    @property
    def unicode_extended(self) -> Protocol:
        """The unicode-extended rendering protocol. Uses an extended character set of math symbols that may not be fully supported in some environments."""
        return self._unicode_extended


protocols = Protocols()


class Treatment:
    """A treatment is a typesetting approach used to convey specific information about some object.

    Sample 1:
    Let b be a book, then "Full text", "Summary", "Title", and "ISBN" may be candidate treatments.

    Sample 2:
    Let phi be a mathematical formula, "Variable name", "Formula", "Tree representation" may be candidate treatments.
    """

    def __init__(self, name: str):
        self._name: str = name

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name


class Treatments:
    """A catalog of out-of-the-box treatments."""

    def __init__(self):
        self._default = Treatment('default')
        self._symbol_representation = Treatment('symbolic representation')

    @property
    def default(self) -> Treatment:
        """If no treatment is specified, typesetting uses the default treatment."""
        return self._default

    @property
    def symbolic_representation(self) -> Treatment:
        """Represent the formal-object as a symbol."""
        return self._symbol_representation


treatments = Treatments()


class Flavor:
    """A flavor is a refined typesetting approach for a treatment.

    For example, if several conventions are possible to typeset a particular object with a particular treatment,
    of if several authors use different conventions,
    then flavors may be used to distinguish these.

    """

    def __init__(self, name: str):
        self._name: str = name

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name


class Flavors:
    """A catalog of out-of-the-box flavors."""

    def __init__(self):
        self._default = Flavor('Default')

    @property
    def default(self) -> Flavor:
        """If no flavor is specified, typesetting uses the default flavor."""
        return self._default


flavors = Flavors()


class Language:
    """A language. Enables the translation of typesettable objects."""

    def __init__(self, name: str):
        self._name: str = name

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name


class Languages:
    """A catalog of out-of-the-box languages."""

    def __init__(self):
        self._fr_ch = Language('French (Switzerland)')
        self._en_us = Language('English (US)')
        self._default = self._en_us

    @property
    def default(self) -> Language:
        """If no language is specified, typesetting uses the default language."""
        return self._default

    @property
    def en_us(self) -> Language:
        """The american English language."""
        return self._en_us


languages = Languages()

typesetting_methods: typing.Dict[
    type, typing.Dict[Treatment, typing.Dict[Flavor, typing.Dict[Language, typing.Callable]]]] = dict()


def register_typesetting_method(method: typing.Callable, python_type: type, treatment: Treatment, flavor: Flavor,
    language: Language) -> None:
    """Register a typesetting method for the given protocol, treatment, and language.
    If protocol, treatment, and/or language are not specified, use the defaults.
    If default protocol, treatment, and/or language are not defined, use the fail-safe.
    If a typesetting method was already registered for the given protocol, treatment, and language, substitute
    the previously registered method with the new one."""
    global typesetting_methods
    global protocols
    global treatments
    global favors
    global languages
    if python_type not in typesetting_methods:
        typesetting_methods[python_type] = dict()
    if treatment not in typesetting_methods[python_type]:
        typesetting_methods[python_type][treatment] = dict()
    if flavor not in typesetting_methods[python_type][treatment]:
        typesetting_methods[python_type][treatment][flavor] = dict()
    typesetting_methods[python_type][treatment][flavor][language]: typing.Callable = method


def typeset(o: TypesettableObject, protocol: Protocol, treatment: typing.Optional[Treatment],
    flavor: typing.Optional[Flavor], language: typing.Optional[Language]) -> typing.Generator[str, None, None]:
    global typesetting_methods
    global protocols
    global treatments
    global flavors
    global languages
    ordered_types: typing.Generator[type, any, None] = (t for t in o.__class__.mro())  # A tuple of types ordered by
    # inheritance.
    python_type: typing.Optional[type] = next(t for t in ordered_types if t in typesetting_methods)
    if python_type is None:
        raise Exception('Unsupported python type.')
    if treatment not in typesetting_methods[python_type]:
        unsupported_treatment: Treatment = treatment
        treatment = next(iter(typesetting_methods[python_type]))
        logging.debug(msg=f'None or unsupported treatment {unsupported_treatment} replaced by {treatment}.')
    if flavor not in typesetting_methods[python_type][treatment]:
        unsupported_flavor: Flavor = flavor
        flavor = next(iter(typesetting_methods[python_type][treatment]))
        logging.debug(msg=f'None or unsupported flavor {unsupported_flavor} replaced by {flavor}.')
    if language not in typesetting_methods[python_type][treatment][flavor]:
        unsupported_language: Language = language
        language = next(iter(typesetting_methods[python_type][treatment][flavor]))
        logging.debug(msg=f'None or unsupported language {unsupported_language} replaced by {language}.')
    generator: typing.Generator[str, None, None] = typesetting_methods[python_type][treatment][flavor][language](o=o,
        protocol=protocol, treatment=treatment, flavor=flavor, language=language)
    yield from generator


def to_string(o: TypesettableObject, protocol: Protocol, treatment: typing.Optional[Treatment],
    flavor: typing.Optional[Flavor], language: typing.Optional[Language]) -> str:
    return ''.join(typeset(o=o, protocol=protocol, treatment=treatment, flavor=flavor, language=language))


class TypesettableObject(abc.ABC):
    """The typesettable-object abstract class makes it possible to equip some object in such a way
    that may be typeset by registering typesetting methods for the desired treatments and languages."""

    def __init__(self):
        pass

    def __repr__(self):
        return self.to_string(protocol=protocols.unicode_limited)

    def __str__(self):
        return self.to_string(protocol=protocols.unicode_limited)

    def to_string(self, protocol: typing.Optional[Protocol] = None, treatment: typing.Optional[Treatment] = None,
        flavor: typing.Optional[Flavor] = None, language: typing.Optional[Language] = None) -> str:
        return to_string(o=self, protocol=protocol, treatment=treatment, flavor=flavor, language=language)

    def typeset(self, protocol: typing.Optional[Protocol] = None, treatment: typing.Optional[Treatment] = None,
        language: typing.Optional[Language] = None, flavor: typing.Optional[Flavor] = None) -> typing.Generator[
        str, None, None]:
        """Typeset this object by yielding strings."""
        yield from typeset(o=self, protocol=protocol, treatment=treatment, flavor=flavor, language=language)


class Symbol(TypesettableObject):
    """An atomic symbol."""

    def __init__(self, latex_math: str, unicode_extended: str, unicode_limited: str):
        self._latex_math = latex_math
        self._unicode_extended = unicode_extended
        self._unicode_limited = unicode_limited
        super().__init__()

    @property
    def latex_math(self) -> str:
        return self._latex_math

    @property
    def unicode_extended(self) -> str:
        return self._unicode_extended

    @property
    def unicode_limited(self) -> str:
        return self._unicode_limited


def typeset_symbol(o: Symbol, protocol: typing.Optional[Protocol] = None, treatment: typing.Optional[Treatment] = None,
    language: typing.Optional[Language] = None, flavor: typing.Optional[Flavor] = None) -> typing.Generator[
    str, None, None]:
    match protocol:
        case protocols.latex:
            yield o.latex_math
        case protocols.unicode_extended:
            yield o.unicode_extended
        case protocols.unicode_limited:
            yield o.unicode_limited
        case _:
            raise Exception('Unsupported protocol.')


class Symbols:
    """A catalog of out-of-the-box symbols."""

    def __init__(self):
        self._not_sign = Symbol(latex_math='\\lnot', unicode_extended='¬', unicode_limited='lnot')
        self._rightwards_arrow = Symbol(latex_math='\\rightarrow', unicode_extended='→', unicode_limited='-->')

    @property
    def not_sign(self) -> Symbol:
        return self._not_sign

    @property
    def rightwards_arrow(self) -> Symbol:
        return self._rightwards_arrow


symbols = Symbols()

register_typesetting_method(method=typeset_symbol, python_type=Symbol, treatment=treatments.default,
    flavor=flavors.default, language=languages.default)


# print(symbols.not_sign.to_string(protocol=protocols.unicode_extended))
# print(symbols.not_sign.to_string(protocol=protocols.latex))
# print(symbols.rightwards_arrow.to_string(protocol=protocols.unicode_extended))
# print(symbols.rightwards_arrow.to_string(protocol=protocols.latex))


def register_symbol(python_type: type, symbol: Symbol, treatment: Treatment, flavor: Flavor, language: Language):
    """Register a typesetting-method for a python-type that outputs an atomic symbol."""

    # dynamically generate the desired typesetting-method.
    def typesetting_method(o: formal_language.FormalObject, protocol: Protocol, treatment: Treatment, flavor: Flavor,
        language: Language):
        return typeset_symbol(o=symbol, protocol=protocol)

    # register that typesetting-method.
    register_typesetting_method(method=typesetting_method, python_type=python_type, treatment=treatment, flavor=flavor,
        language=language)


def register_styledstring(python_type: type, text: str, treatment: Treatment, flavor: Flavor, language: Language):
    """Register a typesetting-method for a python-type that outputs a string.

    TODO: modify this function to use StyledString instead of str.
    """

    # dynamically generate the desired typesetting-method.
    def typesetting_method(o: formal_language.FormalObject, protocol: Protocol, treatment: Treatment, flavor: Flavor,
        language: Language):
        yield text

    # register that typesetting-method.
    register_typesetting_method(method=typesetting_method, python_type=python_type, treatment=treatment, flavor=flavor,
        language=language)
