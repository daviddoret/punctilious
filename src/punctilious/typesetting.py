from __future__ import annotations

import abc
import typing
import os
import csv
import warnings
import logging
import collections

import log


class Tag:
    """A typesetting tag is a class of objects to which we wish to link some typesetting methods."""

    def __init__(self, name: str, predecessor: typing.Optional[Tag] = None):
        self._name = name
        self._predecessor: typing.Optional[Tag] = predecessor
        self._weight: int = 1000 if predecessor is None else predecessor.weight + 1000
        log.debug(f"tag: {name}, weight: {self._weight}")

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        return self._name

    @property
    def weight(self) -> int:
        """A score that orders tags by degree of specialization."""
        return self._weight

    @property
    def predecessor(self) -> typing.Optional[Tag]:
        return self._predecessor


class Tags:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Tags, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._internal_data_structure: set[Tag] = set()
        self._default = self._register(name="default")
        self._symbol = self.register(name="symbol")

    def _register(self, name: str, predecessor: typing.Optional[Tag] = None) -> Tag:
        """The protected version of the register method is called once for the root element, because it has no predecessor."""
        tag: Tag = Tag(name=name, predecessor=predecessor)
        self._internal_data_structure.add(tag)
        return tag

    @property
    def default(self) -> Tag:
        """If no tag is specified, typesetting uses the default tag."""
        return self._default

    def register(self, name: str, predecessor: typing.Optional[Tag] = None) -> Tag:
        if predecessor is None:
            predecessor = self.default
        return self._register(name=name, predecessor=predecessor)

    @property
    def symbol(self) -> Tag:
        return self._symbol


tags = Tags()


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
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Protocols, cls).__new__(cls)
        return cls._singleton

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
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Treatments, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._default = Treatment('default')

    @property
    def default(self) -> Treatment:
        """If no treatment is specified, typesetting uses the default treatment."""
        return self._default


treatments = Treatments()


class Flavor:
    """A flavor is a refined typesetting approach for a treatment.

    For example, if several conventions are possible to typeset a particular object with a particular treatment,
    of if several authors use different conventions,
    then flavors may be used to distinguish these.

    """

    def __init__(self, name: str, predecessor: typing.Optional[Flavor] = None):
        self._name = name
        self._predecessor: typing.Optional[Tag] = predecessor
        self._weight: int = 100 if predecessor is None else predecessor.weight + 100
        log.debug(f"flavor: {self.name}, weight: {self.weight}")

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        return self._name

    @property
    def weight(self) -> int:
        """A score that orders tags by degree of specialization."""
        return self._weight

    @property
    def predecessor(self) -> typing.Optional[Flavor]:
        return self._predecessor

    @predecessor.setter
    def predecessor(self, predecessor: typing.Optional[Flavor]):
        """Makes it possible to modify the order of preference between flavours at run-time."""
        # TODO: BUG: Prevent self-reference
        # TODO: BUG: Prevent circularity
        # TODO: BUG: Prevent unlimited weight increase
        self._predecessor: typing.Optional[Tag] = predecessor
        self._weight: int = 100 if predecessor is None else predecessor.weight + 100
        log.debug(f"flavor: {self.name}, weight: {self.weight}")


class Flavors:
    """A catalog of out-of-the-box flavors."""''
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Flavors, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._internal_data_structure: set[Flavor] = set()
        self._default = self._register(name='default')

    def _register(self, name: str, predecessor: typing.Optional[Flavor] = None) -> Flavor:
        """The protected version of the register method is called once for the root element, because it has no predecessor."""
        flavor: Flavor = Flavor(name=name, predecessor=predecessor)
        self._internal_data_structure.add(flavor)
        return flavor

    @property
    def default(self) -> Flavor:
        """If no flavor is specified, typesetting uses the default flavor."""
        return self._default

    def register(self, name: str, predecessor: typing.Optional[Flavor] = None) -> Flavor:
        if predecessor is None:
            predecessor = self.default
        return self._register(name=name, predecessor=predecessor)


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
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Languages, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._enus = Language('English (US)')
        self._frch = Language('French (Switzerland)')
        self._default = self._enus

    @property
    def default(self) -> Language:
        """If no language is specified, typesetting uses the default language."""
        return self._default

    @property
    def enus(self) -> Language:
        """The English (US) language."""
        return self._enus

    @property
    def frch(self) -> Language:
        """The French (Swiss) language."""
        return self._frch


languages = Languages()


class TypesettingMethods(dict):
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(TypesettingMethods, cls).__new__(cls)
        return cls._singleton


typesetting_methods: typing.Dict[
    typing.FrozenSet[Tag, Treatment], typing.Dict[typing.FrozenSet[Tag, Flavor, Language], typing.Callable]] = (
    TypesettingMethods())


def register_typesetting_method(python_function: typing.Callable, tag: Tag, treatment: Treatment, flavor: Flavor,
    language: Language) -> typing.Callable:
    """Register a typesetting method for the given protocol, treatment, and language.
    If protocol, treatment, and/or language are not specified, use the defaults.
    If default protocol, treatment, and/or language are not defined, use the fail-safe.
    If a typesetting method was already registered for the given protocol, treatment, and language, substitute
    the previously registered method with the new one."""

    global typesetting_methods
    key: typing.FrozenSet[Tag, Treatment] = frozenset([tag, treatment])
    if key not in typesetting_methods:
        typesetting_methods[key] = dict()
    solution: typing.FrozenSet[Tag, Flavor, Language] = frozenset([tag, flavor, language])
    typesetting_methods[key][solution]: typing.Callable = python_function
    if treatment is not treatments.default:
        # the first registered typesetting_method is promoted as the default typesetting_method
        register_typesetting_method(python_function=python_function, tag=tag, treatment=treatments.default,
            flavor=flavor, language=language)
    return python_function


def typeset(o: Typesettable, protocol: typing.Optional[Protocol] = None, treatment: typing.Optional[Treatment] = None,
    language: typing.Optional[Language] = None, **kwargs) -> typing.Generator[str, None, None]:
    global typesetting_methods
    global protocols
    global treatments
    global flavors
    global languages

    if treatment is None:
        treatment: Treatment = o.default_treatment
        if treatment is None:
            treatment: Treatment = treatments.default
    if language is None:
        language: Language = languages.default

    log.debug(msg=f"protocol: {protocol}")

    keys: set[typing.FrozenSet[Tag, Treatment]] = {frozenset([tag, treatment]) for tag in o.typesetting_tags}
    available_keys: set[typing.FrozenSet[Tag, Treatment]] = keys.intersection(typesetting_methods)

    # some typesetting methods were found, choose the best one.
    best_generator = None
    best_key: typing.Optional[typing.FrozenSet[Tag, Treatment]] = None
    best_solution: typing.Optional[typing.FrozenSet[Tag, Flavor, Language]] = None
    best_flavor: Flavor = None
    best_score = 0
    key: typing.FrozenSet[Tag, Treatment]
    solution: typing.FrozenSet[Tag, Flavor, Language]
    for key in available_keys:
        for solution, generator in typesetting_methods[key].items():
            # solution is of the form set[tag,flavour,language,].
            flavor: Flavor = next(iter(flavor for flavor in solution if isinstance(flavor, Flavor)))
            score = next(iter(solution.intersection(o.typesetting_tags))).weight
            score = score + flavor.weight
            score = score + (1 if languages in solution else 0)
            if score > best_score:
                best_score = score
                best_key = key
                best_solution = solution
                best_flavor = flavor
                best_generator = generator
                log.debug(msg=f"New: {best_score} {best_key} {best_solution} {best_flavor}")
    if best_generator is None:
        # no typesetting method found, use fallback typesetting instead.
        yield from fallback_typesetting_method(o=o, protocol=protocol, treatment=treatment, language=language)
    else:
        yield from best_generator(o=o, protocol=protocol, treatment=treatment, flavor=best_flavor, language=language)


def to_string(o: Typesettable, protocol: typing.Optional[Protocol] = None, treatment: typing.Optional[Treatment] = None,
    language: typing.Optional[Language] = None) -> str:
    return ''.join(typeset(o=o, protocol=protocol, treatment=treatment, language=language))


class Typesettable(abc.ABC):
    """The typesettable abstract class makes it possible to equip some object in such a way
    that may be typeset by registering typesetting methods for the desired treatments and languages."""

    def __init__(self, default_treatment: typing.Optional[Treatment] = None):
        self._typesetting_tags: set[Tag, ...] = set()
        self.tag(tag=tags.default)
        self._default_treatment: typing.Optional[Treatment] = default_treatment

    def __repr__(self):
        return self.to_string(protocol=protocols.unicode_limited)

    def __str__(self):
        return self.to_string(protocol=protocols.unicode_limited)

    @property
    def default_treatment(self) -> typing.Optional[Treatment]:
        return self._default_treatment

    def tag(self, tag: Tag):
        self.typesetting_tags.add(tag)

    def to_string(self, protocol: typing.Optional[Protocol] = None, treatment: typing.Optional[Treatment] = None,
        language: typing.Optional[Language] = None) -> str:
        return to_string(o=self, protocol=protocol, treatment=treatment, language=language)

    @property
    def typesetting_tags(self) -> set[Tag, ...]:
        return self._typesetting_tags

    def typeset(self, protocol: typing.Optional[Protocol] = None, treatment: typing.Optional[Treatment] = None,
        language: typing.Optional[Language] = None) -> typing.Generator[str, None, None]:
        """Typeset this object by yielding strings."""
        yield from typeset(o=self, protocol=protocol, treatment=treatment, language=language)


class Symbol(Typesettable):
    """An atomic symbol."""

    def __init__(self, latex_math: str, unicode_extended: str, unicode_limited: str):
        self._latex_math = latex_math
        self._unicode_extended = unicode_extended
        self._unicode_limited = unicode_limited
        super().__init__()
        self.tag(tag=tags.symbol)

    @property
    def latex_math(self) -> str:
        return self._latex_math

    @property
    def unicode_extended(self) -> str:
        return self._unicode_extended

    @property
    def unicode_limited(self) -> str:
        return self._unicode_limited


def typeset_symbol(o: Symbol, protocol: typing.Optional[Protocol] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    if protocol is None:
        protocol = protocols.default
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
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Symbols, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._asterisk_operator = Symbol(latex_math='\\ast', unicode_extended='∗', unicode_limited='*')
        self._close_parenthesis = Symbol(latex_math='\\right)', unicode_extended=')', unicode_limited=')')
        self._collection_separator = Symbol(latex_math=', ', unicode_extended=', ', unicode_limited=', ')
        self._not_sign = Symbol(latex_math='\\lnot', unicode_extended='¬', unicode_limited='lnot')
        self._open_parenthesis = Symbol(latex_math='\\left(', unicode_extended='(', unicode_limited='(')
        self._rightwards_arrow = Symbol(latex_math='\\rightarrow', unicode_extended='→', unicode_limited='-->')
        self._tilde = Symbol(latex_math='\\sim', unicode_extended='~', unicode_limited='~')

    @property
    def asterisk_operator(self) -> Symbol:
        return self._asterisk_operator

    @property
    def close_parenthesis(self) -> Symbol:
        return self._close_parenthesis

    @property
    def collection_separator(self) -> Symbol:
        return self._collection_separator

    @property
    def not_sign(self) -> Symbol:
        return self._not_sign

    @property
    def open_parenthesis(self) -> Symbol:
        return self._open_parenthesis

    @property
    def rightwards_arrow(self) -> Symbol:
        return self._rightwards_arrow

    @property
    def tilde(self) -> Symbol:
        return self._tilde


symbols = Symbols()


def register_symbol(tag: Tag, symbol: Symbol, **kwargs1) -> typing.Callable:
    """Register a typesetting-method that outputs an atomic symbol."""

    # dynamically generate the desired typesetting-method.
    def typesetting_method(o: Typesettable, **kwargs2) -> typing.Generator[str, None, None]:
        merged_kwargs = {**kwargs1, **kwargs2}  # overwrite kwargs1 with kwargs2
        return typeset_symbol(o=symbol, **merged_kwargs)

    # register that typesetting-method.
    python_function: typing.Callable = register_typesetting_method(python_function=typesetting_method, tag=tag,
        **kwargs1)

    return python_function


def register_styledstring(tag: Tag, text: str, **kwargs1) -> typing.Callable:
    """Register a typesetting-method for a python-type that outputs a string.

    TODO: modify this function to use StyledString instead of str.
    """

    # dynamically generate the desired typesetting-method.
    def typesetting_method(o: Typesettable, **kwargs2) -> typing.Generator[str, None, None]:
        yield text

    # register that typesetting-method.
    python_function = register_typesetting_method(python_function=typesetting_method, tag=tag, **kwargs1)

    return python_function


def fallback_typesetting_method(o: Typesettable, **kwargs):
    """The fallback-typesetting-method assure a minimalist representation for all TypesettableObject."""
    yield f"{type(o).__name__}-{id(o)}"


register_typesetting_method(python_function=typeset_symbol, tag=tags.symbol, treatment=treatments.default,
    flavor=flavors.default, language=languages.default)

log.debug(f"Module {__name__}: loaded.")
