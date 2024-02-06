from __future__ import annotations

import abc
import typing
import log


class TypesettingClass:
    """A typesetting typesetting_class is a class of objects to which we wish to link some typesetting methods."""

    def __init__(self, name: str, superclass: typing.Optional[TypesettingClass] = None):
        self._name = name
        self._superclass: typing.Optional[TypesettingClass] = superclass

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def is_subclass_of(self, c: TypesettingClass):
        """Return True if self is a sub-class of c, False otherwise."""
        d = self
        while True:
            if d == c:
                return True
            if d.superclass is None:
                return False
            d = d.superclass

    @property
    def name(self) -> str:
        return self._name

    @property
    def superclass(self) -> typing.Optional[TypesettingClass]:
        return self._superclass


class TypesettingClasses:
    """A collection of typesetting classes."""
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(TypesettingClasses, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._internal_data_structure: set[TypesettingClass] = set()
        self._typesettable: TypesettingClass = self._register(name="typesettable")
        self._indexed_symbol: TypesettingClass = self.register(name="indexed_symbol", superclass=self._typesettable)
        self._styled_text: TypesettingClass = self.register(name="styled_text", superclass=self._typesettable)
        self._symbol: TypesettingClass = self.register(name="symbol", superclass=self._typesettable)

    def _register(self, name: str, superclass: typing.Optional[TypesettingClass] = None) -> TypesettingClass:
        """The protected version of the register method is called once for the root element, because it has no predecessor."""
        typesetting_class: TypesettingClass = TypesettingClass(name=name, superclass=superclass)
        self._internal_data_structure.add(typesetting_class)
        return typesetting_class

    @property
    def indexed_symbol(self) -> TypesettingClass:
        return self._indexed_symbol

    def register(self, name: str, superclass: TypesettingClass) -> TypesettingClass:
        return self._register(name=name, superclass=superclass)

    @property
    def styled_text(self) -> TypesettingClass:
        return self._styled_text

    @property
    def symbol(self) -> TypesettingClass:
        return self._symbol

    @property
    def typesettable(self) -> TypesettingClass:
        return self._typesettable


typesetting_classes = TypesettingClasses()


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


class Representation:
    """A representation is a typesetting approach used to convey specific information about some object.

    Sample 1:
    Let b be a book, then "Full text", "Summary", "Title", and "ISBN" may be candidate representations.

    Sample 2:
    Let phi be a mathematical formula, "Variable name", "Formula", "Tree representation" may be candidate representations.
    """

    def __init__(self, name: str, predecessor: typing.Optional[Representation]):
        self._name: str = name
        self._predecessor: typing.Optional[Representation] = predecessor

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

    @property
    def predecessor(self) -> typing.Optional[Representation]:
        return self._predecessor


class Representations:
    """A catalog of out-of-the-box representations."""
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Representations, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._technical_representation = Representation(name='technical-representation', predecessor=None)
        self._symbolic_representation = Representation(name='symbolic-representation',
            predecessor=self.technical_representation)
        self._common_language = Representation(name='common-language', predecessor=self.technical_representation)

    @property
    def common_language(self) -> Representation:
        """The common-language representation used in free text."""
        return self._common_language

    @property
    def technical_representation(self) -> Representation:
        """The root / default representation. It provides a fail-safe unambiguous but verbose typesetting."""
        return self._technical_representation

    @property
    def symbolic_representation(self) -> Representation:
        """The formal representation used in formulas."""
        return self._symbolic_representation


representations = Representations()


class Preference:
    """A preference is a refined typesetting approach for a representation.

    For example, if several conventions are possible to typeset a particular object with a particular representation,
    of if several authors use different conventions,
    then preferences may be used to distinguish these.

    """

    def __init__(self, name: str, predecessor: typing.Optional[Preference] = None):
        self._name = name
        self._predecessor: typing.Optional[TypesettingClass] = predecessor
        self._weight: int = 100 if predecessor is None else predecessor.weight + 100
        log.debug(f"preference: {self.name}, weight: {self.weight}")

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
        """A score that orders typesetting_classes by degree of specialization."""
        return self._weight

    @property
    def predecessor(self) -> typing.Optional[Preference]:
        return self._predecessor

    @predecessor.setter
    def predecessor(self, predecessor: typing.Optional[Preference]):
        """Makes it possible to modify the order of preference between flavours at run-time."""
        # TODO: BUG: Prevent self-reference
        # TODO: BUG: Prevent circularity
        # TODO: BUG: Prevent unlimited weight increase
        self._predecessor: typing.Optional[TypesettingClass] = predecessor
        self._weight: int = 100 if predecessor is None else predecessor.weight + 100
        log.debug(f"preference: {self.name}, weight: {self.weight}")


class Preferences:
    """A catalog of out-of-the-box preferences."""''
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Preferences, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._internal_data_structure: set[Preference] = set()
        self._default = self._register(name='default')
        self._text_style = self.register(name="text_style.serif_normal", superclass=self._default)
        self._text_style_serif_normal = self.register(name="text_style.serif_normal", superclass=self._text_style)
        self._text_style_serif_bold = self.register(name="text_style.serif_bold", superclass=self._text_style)
        self._text_style_serif_italic = self.register(name="text_style.serif_italic", superclass=self._text_style)
        self._text_style_serif_bold_italic = self.register(name="text_style.serif_bold_italic",
            superclass=self._text_style)
        self._text_style_sans_serif_normal = self.register(name="text_style.sans_serif_normal",
            superclass=self._text_style)
        self._text_style_sans_serif_bold = self.register(name="text_style.sans_serif_bold", superclass=self._text_style)
        self._text_style_sans_serif_italic = self.register(name="text_style.sans_serif_italic",
            superclass=self._text_style)
        self._text_style_sans_serif_bold_italic = self.register(name="text_style.sans_serif_bold_italic",
            superclass=self._text_style)
        self._text_style_script_normal = self.register(name="text_style.script_normal", superclass=self._text_style)
        self._text_style_script_bold = self.register(name="text_style.script_bold", superclass=self._text_style)
        self._text_style_fraktur_normal = self.register(name="text_style.fraktur_normal", superclass=self._text_style)
        self._text_style_fraktur_bold = self.register(name="text_style.fraktur_bold", superclass=self._text_style)
        self._text_style_monospace = self.register(name="text_style.monospace", superclass=self._text_style)
        self._text_style_double_struck = self.register(name="text_style.double_struck", superclass=self._text_style)

    def _register(self, name: str, predecessor: typing.Optional[Preference] = None) -> Preference:
        """The protected version of the register method is called once for the root element, because it has no predecessor."""
        preference: Preference = Preference(name=name, predecessor=predecessor)
        self._internal_data_structure.add(preference)
        return preference

    @property
    def default(self) -> Preference:
        """If no preference is specified, typesetting uses the default preference."""
        return self._default

    @property
    def text_style_serif_normal(self) -> Preference:
        return self._text_style_serif_normal

    @property
    def text_style_serif_bold(self) -> Preference:
        return self._text_style_serif_bold

    @property
    def text_style_serif_italic(self) -> Preference:
        return self._text_style_serif_italic

    @property
    def text_style_serif_bold_italic(self) -> Preference:
        return self._text_style_serif_bold_italic

    @property
    def text_style_sans_serif_normal(self) -> Preference:
        return self._text_style_sans_serif_normal

    @property
    def text_style_sans_serif_bold(self) -> Preference:
        return self._text_style_sans_serif_bold

    @property
    def text_style_sans_serif_italic(self) -> Preference:
        return self._text_style_sans_serif_italic

    @property
    def text_style_sans_serif_bold_italic(self) -> Preference:
        return self._text_style_sans_serif_bold_italic

    @property
    def text_style_script_normal(self) -> Preference:
        return self._text_style_script_normal

    @property
    def text_style_script_bold(self) -> Preference:
        return self._text_style_script_bold

    @property
    def text_style_fraktur_normal(self) -> Preference:
        return self._text_style_fraktur_normal

    @property
    def text_style_fraktur_bold(self) -> Preference:
        return self._text_style_fraktur_bold

    @property
    def text_style_monospace(self) -> Preference:
        return self._text_style_monospace

    @property
    def text_style_double_struck(self) -> Preference:
        return self._text_style_double_struck

    def register(self, name: str, superclass: typing.Optional[Preference] = None) -> Preference:
        if superclass is None:
            superclass = self.default
        return self._register(name=name, predecessor=superclass)


preferences = Preferences()


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


typesetting_methods: typing.Dict[int, typing.Callable] = dict()


def register_typesetting_method(python_function: typing.Callable, c: TypesettingClass,
    representation: Representation) -> None:
    """Register a typesetting method for the given representation, and hierarchical-class.
    If a typesetting method was already registered for the given protocol, representation, and language, substitute
    the previously registered method with the new one."""

    global typesetting_methods
    key: int = hash((c, representation,))
    if key in typesetting_methods:
        log.info(msg=f'Override typesetting-method: ({c},{representation})')
    typesetting_methods[key] = python_function


def typeset(o: Typesettable, protocol: typing.Optional[Protocol] = None,
    representation: typing.Optional[Representation] = None, **kwargs) -> typing.Generator[str, None, None]:
    global typesetting_methods
    global representations

    if representation is None:
        representation: Representation = o.default_representation
        if representation is None:
            # fallback to the fail-safe representation method.
            representation: Representation = representations.technical_representation

    # Find a typesetting method in the class-hierarchy
    # for the required representation.
    typesetting_method: typing.Callable
    c: TypesettingClass = o.typesetting_class
    while True:
        key: int = hash((c, representation,))
        if key in typesetting_methods:
            typesetting_method = typesetting_methods[key]
            break
        if c.superclass is None:
            # This is the root, use the fallback method.
            typesetting_method = fallback_typesetting_method
            break
        else:
            c = c.superclass

    yield from typesetting_method(o=o, protocol=protocol, representation=representation, **kwargs)


def typeset_obsolete(o: Typesettable, protocol: typing.Optional[Protocol] = None,
    representation: typing.Optional[Representation] = None, language: typing.Optional[Language] = None, **kwargs) -> \
    typing.Generator[str, None, None]:
    global typesetting_methods
    global protocols
    global representations
    global preferences
    global languages

    if representation is None:
        representation: Representation = o.default_representation
        if representation is None:
            # fallback to the fail-safe representation method.
            representation: Representation = representations.technical_representation
    if language is None:
        language: Language = languages.default

    # log.debug(msg=f"protocol: {protocol}")

    keys: set[typing.FrozenSet[TypesettingClass, Representation]] = {frozenset([typesetting_class, representation]) for
        typesetting_class in o.typesetting_typesetting_classes}
    available_keys: set[typing.FrozenSet[TypesettingClass, Representation]] = keys.intersection(typesetting_methods)

    # some typesetting methods were found, choose the best one.
    best_generator = None
    best_key: typing.Optional[typing.FrozenSet[TypesettingClass, Representation]] = None
    best_solution: typing.Optional[typing.FrozenSet[TypesettingClass, Preference, Language]] = None
    best_preference: Preference = None
    best_score = 0
    key: typing.FrozenSet[TypesettingClass, Representation]
    solution: typing.FrozenSet[TypesettingClass, Preference, Language]
    for key in available_keys:
        for solution, generator in typesetting_methods[key].items():
            # solution is of the form set[typesetting_class,flavour,language,].
            preference: Preference = next(
                iter(preference for preference in solution if isinstance(preference, Preference)))
            score = next(iter(solution.intersection(o.typesetting_typesetting_classes))).weight
            score = score + preference.weight
            score = score + (1 if languages in solution else 0)
            if score > best_score:
                best_score = score
                best_key = key
                best_solution = solution
                best_preference = preference
                best_generator = generator  # log.debug(msg=f"New: {best_score} {best_key} {best_solution} {best_preference}")
    if best_generator is None:
        # no typesetting method found, use fallback typesetting instead.
        kwargs['preference'] = best_preference
        yield from fallback_typesetting_method(o=o, protocol=protocol, representation=representation, language=language,
            **kwargs)
    else:
        kwargs['preference'] = best_preference
        yield from best_generator(o=o, protocol=protocol, representation=representation, language=language, **kwargs)


def to_string(o: Typesettable, protocol: typing.Optional[Protocol] = None,
    representation: typing.Optional[Representation] = None, language: typing.Optional[Language] = None) -> str:
    return ''.join(typeset(o=o, protocol=protocol, representation=representation, language=language))


class Typesettable(abc.ABC):
    """The typesettable abstract class makes it possible to equip some object in such a way
    that may be typeset by registering typesetting methods for the desired representations and languages."""

    def __init__(self, tc: typing.Optional[TypesettingClass] = None,
        default_rep: typing.Optional[Representation] = None):
        if tc is None:
            tc = typesetting_classes.typesettable
        elif not tc.is_subclass_of(c=typesetting_classes.typesettable):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        if default_rep is None:
            default_rep = representations.technical_representation
        super().__init__()
        self._default_representation: Representation = default_rep
        self._typesetting_class = tc

    def __repr__(self):
        return self.to_string(protocol=protocols.unicode_limited)

    def __str__(self):
        return self.to_string(protocol=protocols.unicode_limited)

    @property
    def default_representation(self) -> Representation:
        return self._default_representation

    @property
    def typesetting_class(self) -> TypesettingClass:
        return self._typesetting_class

    def is_an_element_of_typesetting_class(self, c: TypesettingClass) -> bool:
        """Return True if this object is an element of the typesetting_class c, False otherwise."""
        current_class: TypesettingClass = self.typesetting_class
        while True:
            if current_class == c:
                return True
            else:
                if current_class.superclass is None:
                    # this was the root class,
                    # it follows that self is not a member of the class.
                    return False
                else:
                    # climbs the hierarchy.
                    current_class = current_class.superclass

    def to_string(self, protocol: typing.Optional[Protocol] = None,
        representation: typing.Optional[Representation] = None, language: typing.Optional[Language] = None) -> str:
        return to_string(o=self, protocol=protocol, representation=representation, language=language)

    def typeset(self, **kwargs) -> typing.Generator[str, None, None]:
        """Typeset this object by yielding strings."""
        yield from typeset(o=self, **kwargs)


class Symbol(Typesettable):
    """An atomic symbol."""

    def __init__(self, latex_math: str, unicode_extended: str, unicode_limited: str):
        self._latex_math = latex_math
        self._unicode_extended = unicode_extended
        self._unicode_limited = unicode_limited
        super().__init__(tc=typesetting_classes.symbol, default_rep=representations.symbolic_representation)

    @property
    def latex_math(self) -> str:
        return self._latex_math

    @property
    def unicode_extended(self) -> str:
        return self._unicode_extended

    @property
    def unicode_limited(self) -> str:
        return self._unicode_limited


def typeset_styled_text(o: StyledText, protocol: typing.Optional[Protocol] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    if protocol is None:
        protocol = protocols.default
    match protocol:
        case protocols.latex:
            yield o.neutral_text
        case protocols.unicode_extended:
            yield o.neutral_text
        case protocols.unicode_limited:
            yield o.neutral_text
        case _:
            raise Exception('Unsupported protocol.')


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
        self._not_sign = Symbol(latex_math='\\lnot', unicode_extended='¬', unicode_limited='not')
        self._open_parenthesis = Symbol(latex_math='\\left(', unicode_extended='(', unicode_limited='(')
        self._p_uppercase_serif_italic = Symbol(latex_math='\\textit{P}', unicode_extended='𝑃', unicode_limited='P')
        self._q_uppercase_serif_italic = Symbol(latex_math='\\textit{Q}', unicode_extended='𝑄', unicode_limited='Q')
        self._r_uppercase_serif_italic = Symbol(latex_math='\\textit{R}', unicode_extended='𝑅', unicode_limited='R')
        self._p_uppercase_serif_italic_bold = Symbol(latex_math='\\bm{\\textit{P}}', unicode_extended='𝑷',
            unicode_limited='PP')
        self._q_uppercase_serif_italic_bold = Symbol(latex_math='\\bm{\\textit{Q}}', unicode_extended='𝑸',
            unicode_limited='QQ')
        self._r_uppercase_serif_italic_bold = Symbol(latex_math='\\bm{\\textit{R}}', unicode_extended='𝑹',
            unicode_limited='RR')
        self._rightwards_arrow = Symbol(latex_math='\\rightarrow', unicode_extended='→', unicode_limited='-->')
        self._space = Symbol(latex_math=' ', unicode_extended=' ', unicode_limited=' ')
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
    def p_uppercase_serif_italic(self) -> Symbol:
        return self._p_uppercase_serif_italic

    @property
    def p_uppercase_serif_italic_bold(self) -> Symbol:
        return self._p_uppercase_serif_italic_bold

    @property
    def q_uppercase_serif_italic(self) -> Symbol:
        return self._q_uppercase_serif_italic

    @property
    def q_uppercase_serif_italic_bold(self) -> Symbol:
        return self._q_uppercase_serif_italic_bold

    @property
    def r_uppercase_serif_italic(self) -> Symbol:
        return self._r_uppercase_serif_italic

    @property
    def r_uppercase_serif_italic_bold(self) -> Symbol:
        return self._r_uppercase_serif_italic_bold

    @property
    def rightwards_arrow(self) -> Symbol:
        return self._rightwards_arrow

    @property
    def space(self) -> Symbol:
        return self._space

    @property
    def tilde(self) -> Symbol:
        return self._tilde


symbols = Symbols()


class IndexedSymbol(Typesettable):

    def __init__(self, symbol: Symbol, index: int):
        self._symbol: Symbol = symbol
        self._index: int = index
        super().__init__(tc=typesetting_classes.indexed_symbol)

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.symbol, self.index,))

    @property
    def index(self) -> int:
        return self._index

    @property
    def symbol(self) -> Symbol:
        return self._symbol


def typeset_indexed_symbol(o: IndexedSymbol, protocol: typing.Optional[Protocol] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    if protocol is None:
        protocol = protocols.default
    match protocol:
        case protocols.latex:
            yield from o.symbol.typeset(protocol=protocol, **kwargs)
            yield "_{"
            yield str(o.index)
            yield "}"
        case protocols.unicode_extended:
            yield from o.symbol.typeset(protocol=protocol, **kwargs)
            yield unicode_subscriptify(s=str(o.index))
        case protocols.unicode_limited:
            yield from o.symbol.typeset(protocol=protocol, **kwargs)
            yield str(o.index)
        case _:
            raise Exception('Unsupported protocol.')


def register_symbol(c: TypesettingClass, representation: Representation, symbol: Symbol) -> typing.Callable:
    """Register a typesetting-method that outputs an atomic symbol."""

    # dynamically generate the desired typesetting-method.
    def typesetting_method(o: Typesettable, **kwargs2) -> typing.Generator[str, None, None]:
        merged_kwargs = {**kwargs2}  # overwrite kwargs1 with kwargs2
        return typeset_symbol(o=symbol, **merged_kwargs)

    # register that typesetting-method.
    register_typesetting_method(python_function=typesetting_method, c=c, representation=representation)


class StyledText(Typesettable):
    unicode_indexes = {preferences.text_style_serif_normal: 0, preferences.text_style_serif_bold: 1,
        preferences.text_style_serif_italic:                2, preferences.text_style_serif_bold_italic: 3,
        preferences.text_style_sans_serif_normal:           4, preferences.text_style_sans_serif_bold: 5,
        preferences.text_style_sans_serif_italic:           6, preferences.text_style_sans_serif_bold_italic: 7,
        preferences.text_style_script_normal:               8, preferences.text_style_script_bold: 9,
        preferences.text_style_fraktur_normal:              10, preferences.text_style_fraktur_bold: 11,
        preferences.text_style_monospace:                   12, preferences.text_style_double_struck: 13}
    unicode_styled_characters = {'a': 'a𝐚𝑎𝒂𝖺𝗮𝘢𝙖𝒶𝓪𝔞𝖆𝚊𝕒', 'b': 'b𝐛𝑏𝒃𝖻𝗯𝘣𝙗𝒷𝓫𝔟𝖇𝚋𝕓', 'c': 'c𝐜𝑐𝒄𝖼𝗰𝘤𝙘𝒸𝓬𝔠𝖈𝚌𝕔',
        'd':                          'd𝐝𝑑𝒅𝖽𝗱𝘥𝙙𝒹𝓭𝔡𝖉𝚍𝕕', 'e': 'e𝐞𝑒𝒆𝖾𝗲𝘦𝙚ℯ𝓮𝔢𝖊𝚎𝕖', 'f': 'f𝐟𝑓𝒇𝖿𝗳𝘧𝙛𝒻𝓯𝔣𝖋𝚏𝕗',
        'g':                          'g𝐠𝑔𝒈𝗀𝗴𝘨𝙜ℊ𝓰𝔤𝖌𝚐𝕘', 'h': 'h𝐡ℎ𝒉𝗁𝗵𝘩𝙝𝒽𝓱𝔥𝖍𝚑𝕙', 'i': 'i𝐢𝑖𝒊𝗂𝗶𝘪𝙞𝒾𝓲𝔦𝖎𝚒𝕚',
        'j':                          'j𝐣𝑗𝒋𝗃𝗷𝘫𝙟𝒿𝓳𝔧𝖏𝚓𝕛', 'k': 'k𝐤𝑘𝒌𝗄𝗸𝘬𝙠𝓀𝓴𝔨𝖐𝚔𝕜', 'l': 'l𝐥𝑙𝒍𝗅𝗹𝘭𝙡𝓁𝓵𝔩𝖑𝚕𝕝',
        'm':                          'm𝐦𝑚𝒎𝗆𝗺𝘮𝙢𝓂𝓶𝔪𝖒𝚖𝕞', 'n': 'n𝐧𝑛𝒏𝗇𝗻𝘯𝙣𝓃𝓷𝔫𝖓𝚗𝕟', 'o': 'o𝐨𝑜𝒐𝗈𝗼𝘰𝙤ℴ𝓸𝔬𝖔𝚘𝕠',
        'p':                          'p𝐩𝑝𝒑𝗉𝗽𝘱𝙥𝓅𝓹𝔭𝖕𝚙𝕡', 'q': 'q𝐪𝑞𝒒𝗊𝗾𝘲𝙦𝓆𝓺𝔮𝖖𝚚𝕢', 'r': 'r𝐫𝑟𝒓𝗋𝗿𝘳𝙧𝓇𝓻𝔯𝖗𝚛𝕣',
        's':                          's𝐬𝑠𝒔𝗌𝘀𝘴𝙨𝓈𝓼𝔰𝖘𝚜𝕤', 't': 't𝐭𝑡𝒕𝗍𝘁𝘵𝙩𝓉𝓽𝔱𝖙𝚝𝕥', 'u': 'u𝐮𝑢𝒖𝗎𝘂𝘶𝙪𝓊𝓾𝔲𝖚𝚞𝕦',
        'v':                          'v𝐯𝑣𝒗𝗏𝘃𝘷𝙫𝓋𝓿𝔳𝖛𝚟𝕧', 'w': 'w𝐰𝑤𝒘𝗐𝘄𝘸𝙬𝓌𝔀𝔴𝖜𝚠𝕨', 'x': 'x𝐱𝑥𝒙𝗑𝘅𝘹𝙭𝓍𝔁𝔵𝖝𝚡𝕩',
        'y':                          'y𝐲𝑦𝒚𝗒𝘆𝘺𝙮𝓎𝔂𝔶𝖞𝚢𝕪', 'z': 'z𝐳𝑧𝒛𝗓𝘇𝘻𝙯𝓏𝔃𝔷𝖟𝚣𝕫', 'A': 'A𝐀𝐴𝑨𝖠𝗔𝘈𝘼𝒜𝓐𝔄𝕬𝙰𝔸',
        'B':                          'B𝐁𝐵𝑩𝖡𝗕𝘉𝘽ℬ𝓑𝔅𝕭𝙱𝔹', 'C': 'C𝐂𝐶𝑪𝖢𝗖𝘊𝘾𝒞𝓒ℭ𝕮𝙲ℂ', 'D': 'D𝐃𝐷𝑫𝖣𝗗𝘋𝘿𝒟𝓓𝔇𝕯𝙳𝔻',
        'E':                          'E𝐄𝐸𝑬𝖤𝗘𝘌𝙀ℰ𝓔𝔈𝕰𝙴𝔼', 'F': 'F𝐅𝐹𝑭𝖥𝗙𝘍𝙁ℱ𝓕𝔉𝕱𝙵𝔽', 'G': 'G𝐆𝐺𝑮𝖦𝗚𝘎𝙂𝒢𝓖𝔊𝕲𝙶𝔾',
        'H':                          'H𝐇𝐻𝑯𝖧𝗛𝘏𝙃ℋ𝓗ℌ𝕳𝙷ℍ', 'I': 'I𝐈𝐼𝑰𝖨𝗜𝘐𝙄ℐ𝓘ℑ𝕴𝙸𝕀', 'J': 'J𝐉𝐽𝑱𝖩𝗝𝘑𝙅𝒥𝓙𝔍𝕵𝙹𝕁',
        'K':                          'K𝐊𝐾𝑲𝖪𝗞𝘒𝙆𝒦𝓚𝔎𝕶𝙺𝕂', 'L': 'L𝐋𝐿𝑳𝖫𝗟𝘓𝙇ℒ𝓛𝔏𝕷𝙻𝕃', 'M': 'M𝐌𝑀𝑴𝖬𝗠𝘔𝙈ℳ𝓜𝔐𝕸𝙼𝕄',
        'N':                          'N𝐍𝑁𝑵𝖭𝗡𝘕𝙉𝒩𝓝𝔑𝕹𝙽ℕ', 'O': 'O𝐎𝑂𝑶𝖮𝗢𝘖𝙊𝒪𝓞𝔒𝕺𝙾𝕆', 'P': 'P𝐏𝑃𝑷𝖯𝗣𝘗𝙋𝒫𝓟𝔓𝕻𝙿ℙ',
        'Q':                          'Q𝐐𝑄𝑸𝖰𝗤𝘘𝙌𝒬𝓠𝔔𝕼𝚀ℚ', 'R': 'R𝐑𝑅𝑹𝖱𝗥𝘙𝙍ℛ𝓡ℜ𝕽𝚁ℝ', 'S': 'S𝐒𝑆𝑺𝖲𝗦𝘚𝙎𝒮𝓢𝔖𝕾𝚂𝕊',
        'T':                          'T𝐓𝑇𝑻𝖳𝗧𝘛𝙏𝒯𝓣𝔗𝕿𝚃𝕋', 'U': 'U𝐔𝑈𝑼𝖴𝗨𝘜𝙐𝒰𝓤𝔘𝖀𝚄𝕌', 'V': 'V𝐕𝑉𝑽𝖵𝗩𝘝𝙑𝒱𝓥𝔙𝖁𝚅𝕍',
        'W':                          'W𝐖𝑊𝑾𝖶𝗪𝘞𝙒𝒲𝓦𝔚𝖂𝚆𝕎', 'X': 'X𝐗𝑋𝑿𝖷𝗫𝘟𝙓𝒳𝓧𝔛𝖃𝚇𝕏', 'Y': 'Y𝐘𝑌𝒀𝖸𝗬𝘠𝙔𝒴𝓨𝔜𝖄𝚈𝕐',
        'Z':                          'Z𝐙𝑍𝒁𝖹𝗭𝘡𝙕𝒵𝓩ℨ𝖅𝚉ℤ', '0': '0𝟎0𝟎𝟢𝟬𝟢𝟬𝟢𝟬𝟢𝟬𝟶𝟘', '1': '1𝟏1𝟏𝟣𝟭𝟣𝟭𝟣𝟭𝟣𝟭𝟷𝟙',
        '2':                          '2𝟐2𝟐𝟤𝟮𝟤𝟮𝟤𝟮𝟤𝟮𝟸𝟚', '3': '3𝟑3𝟑𝟥𝟯𝟥𝟯𝟥𝟯𝟥𝟯𝟹𝟛', '4': '4𝟒4𝟒𝟦𝟰𝟦𝟰𝟦𝟰𝟦𝟰𝟺𝟜',
        '5':                          '5𝟓5𝟓𝟧𝟱𝟧𝟱𝟧𝟱𝟧𝟱𝟻𝟝', '6': '6𝟔6𝟔𝟨𝟲𝟨𝟲𝟨𝟲𝟨𝟲𝟼𝟞', '7': '7𝟕7𝟕𝟩𝟳𝟩𝟳𝟩𝟳𝟩𝟳𝟽𝟟',
        '8':                          '8𝟖8𝟖𝟪𝟴𝟪𝟴𝟪𝟴𝟪𝟴𝟾𝟠', '9': '9𝟗9𝟗𝟫𝟵𝟫𝟵𝟫𝟵𝟫𝟵𝟿𝟡'}

    def __init__(self, neutral_text: str):
        self._neutral_text = neutral_text
        super().__init__()
        self.declare_typesetting_class_element(typesetting_class=typesetting_classes.styled_text)

    @property
    def neutral_text(self) -> str:
        return self._neutral_text


unicode_subscript_dictionary = {'0': u'₀', '1': u'₁', '2': u'₂', '3': u'₃', '4': u'₄', '5': u'₅', '6': u'₆', '7': u'₇',
    '8':                             u'₈', '9': u'₉', 'a': u'ₐ', 'e': u'ₑ', 'o': u'ₒ', 'x': u'ₓ',  # '???': u'ₔ',
    'h':                             u'ₕ', 'k': u'ₖ', 'l': u'ₗ', 'm': u'ₘ', 'n': u'ₙ', 'p': u'ₚ', 's': u'ₛ', 't': u'ₜ',
    '+':                             u'₊', '-': u'₋', '=': u'₌', '(': u'₍', ')': u'₎', 'j': u'ⱼ', 'i': u'ᵢ',
    # Alternative from the Unicode Phonetic Extensions block: ᵢ
    'r':                             u'ᵣ',  # Source: Unicode Phonetic Extensions block.
    'u':                             u'ᵤ',  # Source: Unicode Phonetic Extensions block.
    'v':                             u'ᵥ',  # Source: Unicode Phonetic Extensions block.
    'β':                             u'ᵦ',  # Source: Unicode Phonetic Extensions block.
    'γ':                             u'ᵧ',  # Source: Unicode Phonetic Extensions block.
    # '???': u'ᵨ', # Source: Unicode Phonetic Extensions block.
    'φ':                             u'ᵩ',  # Source: Unicode Phonetic Extensions block.
    'χ':                             u'ᵪ'  # Source: Unicode Phonetic Extensions block.
}


def unicode_subscriptify(s: str = ''):
    """Converts to unicode-subscript the string s.

    This is done in best effort, knowing that Unicode only contains a small subset of subscript characters.

    References:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript
        * https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts
    """
    global unicode_subscript_dictionary
    if isinstance(s, int):
        s = str(s)
    if s is None or s == '':
        return ''
    return ''.join([unicode_subscript_dictionary.get(c, c) for c in s])


def register_styledstring(typesetting_class: TypesettingClass, representation: Representation, text: str) -> None:
    """Register a typesetting-method for a python-type that outputs a string.

    TODO: modify this function to use StyledString instead of str.
    """

    # dynamically generate the desired typesetting-method.
    def typesetting_method(o: Typesettable, **kwargs2) -> typing.Generator[str, None, None]:
        yield text

    # register that typesetting-method.
    register_typesetting_method(python_function=typesetting_method, c=typesetting_class, representation=representation)


def fallback_typesetting_method(o: Typesettable, **kwargs):
    """The fallback-typesetting-method assure a minimalist representation for all TypesettableObject."""
    yield f"{type(o).__name__}-{id(o)}"


register_typesetting_method(python_function=typeset_styled_text, c=typesetting_classes.symbol,
    representation=representations.technical_representation)
register_typesetting_method(python_function=typeset_symbol, c=typesetting_classes.symbol,
    representation=representations.technical_representation)
register_typesetting_method(python_function=typeset_symbol, c=typesetting_classes.symbol,
    representation=representations.symbolic_representation)
register_typesetting_method(python_function=typeset_indexed_symbol, c=typesetting_classes.indexed_symbol,
    representation=representations.technical_representation)
register_typesetting_method(python_function=typeset_indexed_symbol, c=typesetting_classes.indexed_symbol,
    representation=representations.symbolic_representation)

log.debug(f"Module {__name__}: loaded.")
