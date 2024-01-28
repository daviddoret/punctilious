from __future__ import annotations

import abc
import typing
import log


class Clazz:
    """A typesetting clazz is a class of objects to which we wish to link some typesetting methods."""

    def __init__(self, name: str, predecessor: typing.Optional[Clazz] = None):
        self._name = name
        self._predecessor: typing.Optional[Clazz] = predecessor
        self._weight: int = 1000 if predecessor is None else predecessor.weight + 1000
        log.debug(f"clazz: {name}, weight: {self._weight}")

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
        """A score that orders clazzes by degree of specialization."""
        return self._weight

    @property
    def predecessor(self) -> typing.Optional[Clazz]:
        return self._predecessor


class Clazzes:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Clazzes, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._internal_data_structure: set[Clazz] = set()
        self._default: Clazz = self._register(name="default")
        self._indexed_symbol: Clazz = self._register(name="indexed_symbol")
        self._styled_text: Clazz = self.register(name="styled_text")
        self._symbol: Clazz = self.register(name="symbol")

    def _register(self, name: str, predecessor: typing.Optional[Clazz] = None) -> Clazz:
        """The protected version of the register method is called once for the root element, because it has no predecessor."""
        clazz: Clazz = Clazz(name=name, predecessor=predecessor)
        self._internal_data_structure.add(clazz)
        return clazz

    @property
    def default(self) -> Clazz:
        """If no clazz is specified, typesetting uses the default clazz."""
        return self._default

    @property
    def indexed_symbol(self) -> Clazz:
        return self._indexed_symbol

    def register(self, name: str, predecessor: typing.Optional[Clazz] = None) -> Clazz:
        if predecessor is None:
            predecessor = self.default
        return self._register(name=name, predecessor=predecessor)

    @property
    def styled_text(self) -> Clazz:
        return self._styled_text

    @property
    def symbol(self) -> Clazz:
        return self._symbol


clazzes = Clazzes()


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


class Representations:
    """A catalog of out-of-the-box representations."""
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Representations, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._default = Representation('default')

    @property
    def default(self) -> Representation:
        """If no representation is specified, typesetting uses the default representation."""
        return self._default


representations = Representations()


class Flavor:
    """A flavor is a refined typesetting approach for a representation.

    For example, if several conventions are possible to typeset a particular object with a particular representation,
    of if several authors use different conventions,
    then flavors may be used to distinguish these.

    """

    def __init__(self, name: str, predecessor: typing.Optional[Flavor] = None):
        self._name = name
        self._predecessor: typing.Optional[Clazz] = predecessor
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
        """A score that orders clazzes by degree of specialization."""
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
        self._predecessor: typing.Optional[Clazz] = predecessor
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
        self._text_style = self.register(name="text_style.serif_normal", predecessor=self._default)
        self._text_style_serif_normal = self.register(name="text_style.serif_normal", predecessor=self._text_style)
        self._text_style_serif_bold = self.register(name="text_style.serif_bold", predecessor=self._text_style)
        self._text_style_serif_italic = self.register(name="text_style.serif_italic", predecessor=self._text_style)
        self._text_style_serif_bold_italic = self.register(name="text_style.serif_bold_italic",
            predecessor=self._text_style)
        self._text_style_sans_serif_normal = self.register(name="text_style.sans_serif_normal",
            predecessor=self._text_style)
        self._text_style_sans_serif_bold = self.register(name="text_style.sans_serif_bold",
            predecessor=self._text_style)
        self._text_style_sans_serif_italic = self.register(name="text_style.sans_serif_italic",
            predecessor=self._text_style)
        self._text_style_sans_serif_bold_italic = self.register(name="text_style.sans_serif_bold_italic",
            predecessor=self._text_style)
        self._text_style_script_normal = self.register(name="text_style.script_normal", predecessor=self._text_style)
        self._text_style_script_bold = self.register(name="text_style.script_bold", predecessor=self._text_style)
        self._text_style_fraktur_normal = self.register(name="text_style.fraktur_normal", predecessor=self._text_style)
        self._text_style_fraktur_bold = self.register(name="text_style.fraktur_bold", predecessor=self._text_style)
        self._text_style_monospace = self.register(name="text_style.monospace", predecessor=self._text_style)
        self._text_style_double_struck = self.register(name="text_style.double_struck", predecessor=self._text_style)

    def _register(self, name: str, predecessor: typing.Optional[Flavor] = None) -> Flavor:
        """The protected version of the register method is called once for the root element, because it has no predecessor."""
        flavor: Flavor = Flavor(name=name, predecessor=predecessor)
        self._internal_data_structure.add(flavor)
        return flavor

    @property
    def default(self) -> Flavor:
        """If no flavor is specified, typesetting uses the default flavor."""
        return self._default

    @property
    def text_style_serif_normal(self) -> Flavor:
        return self._text_style_serif_normal

    @property
    def text_style_serif_bold(self) -> Flavor:
        return self._text_style_serif_bold

    @property
    def text_style_serif_italic(self) -> Flavor:
        return self._text_style_serif_italic

    @property
    def text_style_serif_bold_italic(self) -> Flavor:
        return self._text_style_serif_bold_italic

    @property
    def text_style_sans_serif_normal(self) -> Flavor:
        return self._text_style_sans_serif_normal

    @property
    def text_style_sans_serif_bold(self) -> Flavor:
        return self._text_style_sans_serif_bold

    @property
    def text_style_sans_serif_italic(self) -> Flavor:
        return self._text_style_sans_serif_italic

    @property
    def text_style_sans_serif_bold_italic(self) -> Flavor:
        return self._text_style_sans_serif_bold_italic

    @property
    def text_style_script_normal(self) -> Flavor:
        return self._text_style_script_normal

    @property
    def text_style_script_bold(self) -> Flavor:
        return self._text_style_script_bold

    @property
    def text_style_fraktur_normal(self) -> Flavor:
        return self._text_style_fraktur_normal

    @property
    def text_style_fraktur_bold(self) -> Flavor:
        return self._text_style_fraktur_bold

    @property
    def text_style_monospace(self) -> Flavor:
        return self._text_style_monospace

    @property
    def text_style_double_struck(self) -> Flavor:
        return self._text_style_double_struck

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


typesetting_methods: typing.Dict[typing.FrozenSet[Clazz, Representation], typing.Dict[
    typing.FrozenSet[Clazz, Flavor, Language], typing.Callable]] = (TypesettingMethods())


def register_typesetting_method(python_function: typing.Callable, clazz: Clazz, representation: Representation,
    flavor: Flavor, language: Language) -> typing.Callable:
    """Register a typesetting method for the given protocol, representation, and language.
    If protocol, representation, and/or language are not specified, use the defaults.
    If default protocol, representation, and/or language are not defined, use the fail-safe.
    If a typesetting method was already registered for the given protocol, representation, and language, substitute
    the previously registered method with the new one."""

    global typesetting_methods
    key: typing.FrozenSet[Clazz, Representation] = frozenset([clazz, representation])
    if key not in typesetting_methods:
        typesetting_methods[key] = dict()
    solution: typing.FrozenSet[Clazz, Flavor, Language] = frozenset([clazz, flavor, language])
    typesetting_methods[key][solution]: typing.Callable = python_function
    if representation is not representations.default:
        # the first registered typesetting_method is promoted as the default typesetting_method
        register_typesetting_method(python_function=python_function, clazz=clazz,
            representation=representations.default, flavor=flavor, language=language)
    return python_function


def typeset(o: Typesettable, protocol: typing.Optional[Protocol] = None,
    representation: typing.Optional[Representation] = None, language: typing.Optional[Language] = None, **kwargs) -> \
    typing.Generator[str, None, None]:
    global typesetting_methods
    global protocols
    global representations
    global flavors
    global languages

    if representation is None:
        representation: Representation = o.default_representation
        if representation is None:
            representation: Representation = representations.default
    if language is None:
        language: Language = languages.default

    # log.debug(msg=f"protocol: {protocol}")

    keys: set[typing.FrozenSet[Clazz, Representation]] = {frozenset([clazz, representation]) for clazz in
        o.typesetting_clazzes}
    available_keys: set[typing.FrozenSet[Clazz, Representation]] = keys.intersection(typesetting_methods)

    # some typesetting methods were found, choose the best one.
    best_generator = None
    best_key: typing.Optional[typing.FrozenSet[Clazz, Representation]] = None
    best_solution: typing.Optional[typing.FrozenSet[Clazz, Flavor, Language]] = None
    best_flavor: Flavor = None
    best_score = 0
    key: typing.FrozenSet[Clazz, Representation]
    solution: typing.FrozenSet[Clazz, Flavor, Language]
    for key in available_keys:
        for solution, generator in typesetting_methods[key].items():
            # solution is of the form set[clazz,flavour,language,].
            flavor: Flavor = next(iter(flavor for flavor in solution if isinstance(flavor, Flavor)))
            score = next(iter(solution.intersection(o.typesetting_clazzes))).weight
            score = score + flavor.weight
            score = score + (1 if languages in solution else 0)
            if score > best_score:
                best_score = score
                best_key = key
                best_solution = solution
                best_flavor = flavor
                best_generator = generator  # log.debug(msg=f"New: {best_score} {best_key} {best_solution} {best_flavor}")
    if best_generator is None:
        # no typesetting method found, use fallback typesetting instead.
        kwargs['flavor'] = best_flavor
        yield from fallback_typesetting_method(o=o, protocol=protocol, representation=representation, language=language,
            **kwargs)
    else:
        kwargs['flavor'] = best_flavor
        yield from best_generator(o=o, protocol=protocol, representation=representation, language=language, **kwargs)


def to_string(o: Typesettable, protocol: typing.Optional[Protocol] = None,
    representation: typing.Optional[Representation] = None, language: typing.Optional[Language] = None) -> str:
    return ''.join(typeset(o=o, protocol=protocol, representation=representation, language=language))


class Typesettable(abc.ABC):
    """The typesettable abstract class makes it possible to equip some object in such a way
    that may be typeset by registering typesetting methods for the desired representations and languages."""

    def __init__(self, default_representation: typing.Optional[Representation] = None):
        self._typesetting_clazzes: set[Clazz, ...] = set()
        self.declare_clazz_element(clazz=clazzes.default)
        self._default_representation: typing.Optional[Representation] = default_representation

    def __repr__(self):
        return self.to_string(protocol=protocols.unicode_limited)

    def __str__(self):
        return self.to_string(protocol=protocols.unicode_limited)

    @property
    def default_representation(self) -> typing.Optional[Representation]:
        return self._default_representation

    def declare_clazz_element(self, clazz: Clazz):
        self.typesetting_clazzes.add(clazz)

    def to_string(self, protocol: typing.Optional[Protocol] = None,
        representation: typing.Optional[Representation] = None, language: typing.Optional[Language] = None) -> str:
        return to_string(o=self, protocol=protocol, representation=representation, language=language)

    @property
    def typesetting_clazzes(self) -> set[Clazz, ...]:
        return self._typesetting_clazzes

    def typeset(self, **kwargs) -> typing.Generator[str, None, None]:
        """Typeset this object by yielding strings."""
        yield from typeset(o=self, **kwargs)


class Symbol(Typesettable):
    """An atomic symbol."""

    def __init__(self, latex_math: str, unicode_extended: str, unicode_limited: str):
        self._latex_math = latex_math
        self._unicode_extended = unicode_extended
        self._unicode_limited = unicode_limited
        super().__init__()
        self.declare_clazz_element(clazz=clazzes.symbol)

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
        self._not_sign = Symbol(latex_math='\\lnot', unicode_extended='¬', unicode_limited='lnot')
        self._open_parenthesis = Symbol(latex_math='\\left(', unicode_extended='(', unicode_limited='(')
        self._p_uppercase_serif_italic = Symbol(latex_math='\\textit{P}', unicode_extended='𝑃', unicode_limited='P')
        self._q_uppercase_serif_italic = Symbol(latex_math='\\textit{Q}', unicode_extended='𝑄', unicode_limited='Q')
        self._r_uppercase_serif_italic = Symbol(latex_math='\\textit{R}', unicode_extended='𝑅', unicode_limited='R')
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
    def q_uppercase_serif_italic(self) -> Symbol:
        return self._q_uppercase_serif_italic

    @property
    def r_uppercase_serif_italic(self) -> Symbol:
        return self._r_uppercase_serif_italic

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
        super().__init__()
        self.declare_clazz_element(clazz=clazzes.indexed_symbol)

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


def register_symbol(clazz: Clazz, symbol: Symbol, **kwargs1) -> typing.Callable:
    """Register a typesetting-method that outputs an atomic symbol."""

    # dynamically generate the desired typesetting-method.
    def typesetting_method(o: Typesettable, **kwargs2) -> typing.Generator[str, None, None]:
        merged_kwargs = {**kwargs1, **kwargs2}  # overwrite kwargs1 with kwargs2
        return typeset_symbol(o=symbol, **merged_kwargs)

    # register that typesetting-method.
    python_function: typing.Callable = register_typesetting_method(python_function=typesetting_method, clazz=clazz,
        **kwargs1)

    return python_function


class StyledText(Typesettable):
    unicode_indexes = {flavors.text_style_serif_normal: 0, flavors.text_style_serif_bold: 1,
        flavors.text_style_serif_italic:                2, flavors.text_style_serif_bold_italic: 3,
        flavors.text_style_sans_serif_normal:           4, flavors.text_style_sans_serif_bold: 5,
        flavors.text_style_sans_serif_italic:           6, flavors.text_style_sans_serif_bold_italic: 7,
        flavors.text_style_script_normal:               8, flavors.text_style_script_bold: 9,
        flavors.text_style_fraktur_normal:              10, flavors.text_style_fraktur_bold: 11,
        flavors.text_style_monospace:                   12, flavors.text_style_double_struck: 13}
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
        self.declare_clazz_element(clazz=clazzes.styled_text)

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


def register_styledstring(clazz: Clazz, text: str, **kwargs1) -> typing.Callable:
    """Register a typesetting-method for a python-type that outputs a string.

    TODO: modify this function to use StyledString instead of str.
    """

    # dynamically generate the desired typesetting-method.
    def typesetting_method(o: Typesettable, **kwargs2) -> typing.Generator[str, None, None]:
        yield text

    # register that typesetting-method.
    python_function = register_typesetting_method(python_function=typesetting_method, clazz=clazz, **kwargs1)

    return python_function


def fallback_typesetting_method(o: Typesettable, **kwargs):
    """The fallback-typesetting-method assure a minimalist representation for all TypesettableObject."""
    yield f"{type(o).__name__}-{id(o)}"


register_typesetting_method(python_function=typeset_styled_text, clazz=clazzes.symbol,
    representation=representations.default, flavor=flavors.default, language=languages.default)
register_typesetting_method(python_function=typeset_symbol, clazz=clazzes.symbol,
    representation=representations.default, flavor=flavors.default, language=languages.default)
register_typesetting_method(python_function=typeset_indexed_symbol, clazz=clazzes.indexed_symbol,
    representation=representations.default, flavor=flavors.default, language=languages.default)

log.debug(f"Module {__name__}: loaded.")
