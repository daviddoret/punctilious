from __future__ import annotations

import abc
import typing
import os
import csv


def prioritize_value(*args) -> typing.Any:
    """Return the first non-None object in ⌜*args⌝."""
    for a in args:
        if a is not None:
            return a
    return None


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
        self._default = Treatment('Default')

    @property
    def default(self) -> Treatment:
        """If no treatment is specified, typesetting uses the default treatment."""
        return self._default


treatments = Treatments()


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


class SymbolCategory:
    """A broad category for symbols."""

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


class SymbolCategories:
    """A catalog of out-of-the-box symbol-categories."""

    def __init__(self):
        self._letter: SymbolCategory = SymbolCategory('letter')
        self._digit: SymbolCategory = SymbolCategory('digit')

    @property
    def digit(self) -> SymbolCategory:
        """The digit symbol-category."""
        return self._digit

    @property
    def letter(self) -> SymbolCategory:
        """The letter symbol-category."""
        return self._letter

    def get(self, name) -> SymbolCategory:
        try:
            # Use getattr to get the value of the property by name
            item = getattr(self, name)
            if not isinstance(item, SymbolCategory):
                raise Exception('incorrect property')
            return item
        except AttributeError:
            # Handle the case where the property does not exist
            raise Exception('incorrect property')


symbol_categories = SymbolCategories()


class FontCase:
    """A typesetting font-family."""

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


class FontCases:
    """A catalog of out-of-the-box font-cases."""

    def __init__(self):
        self._lowercase = FontCase('lowercase')
        self._uppercase = FontCase('uppercase')
        self._na = FontCase('n/a')

    def get_from_character(self, character: str) -> FontCase:
        """Returns the font_case of the first character in the input string. If the input string is an empty string, returns the n/a font-case."""
        if character == '':
            return self.na
        elif character[0].islower():
            return self.lowercase
        elif character[0].isupper():
            return self.uppercase
        else:
            return self.na

    def get_from_name(self, name: str) -> FontCase:
        """Returns a font-case from its unique name."""
        try:
            # Use getattr to get the value of the property by name
            item = getattr(self, name)
            if not isinstance(item, FontCase):
                raise Exception('incorrect property')
            return item
        except AttributeError:
            # Handle the case where the property does not exist
            raise Exception('incorrect property')

    @property
    def lowercase(self) -> FontCase:
        """The lowercase font-case."""
        return self._lowercase

    @property
    def na(self) -> FontCase:
        """The n/a (not applicable) font-case. To be used whenever a symbol is not a letter."""
        return self._na

    @property
    def uppercase(self) -> FontCase:
        """The uppercase font-case."""
        return self._uppercase


font_cases = FontCases()


class FontFamily:
    """A typesetting font-family."""

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


class FontFamilies:
    """A catalog of out-of-the-box font-families."""

    def __init__(self):
        self._blackboard = FontFamily('blackboard')
        self._calligraphic = FontFamily('calligraphic')
        self._gothic = FontFamily('gothic')
        self._sans_serif = FontFamily('sans serif')
        self._serif = FontFamily('serif')

    @property
    def blackboard(self) -> FontFamily:
        """The blackboard font-family."""
        return self._blackboard

    @property
    def calligraphic(self) -> FontFamily:
        """The calligraphic font-family."""
        return self._calligraphic

    def get(self, name) -> FontFamily:
        try:
            # Use getattr to get the value of the property by name
            item = getattr(self, name)
            if not isinstance(item, FontFamily):
                raise Exception('incorrect property')
            return item
        except AttributeError:
            # Handle the case where the property does not exist
            raise Exception('incorrect property')

    @property
    def gothic(self) -> FontFamily:
        """The gothic font-family."""
        return self._gothic

    @property
    def sans_serif(self) -> FontFamily:
        """The sans-serif font-family."""
        return self._sans_serif

    @property
    def serif(self) -> FontFamily:
        """The serif font-family."""
        return self._serif


font_families = FontFamilies()


class FontVariant:
    """A typesetting font-variant."""

    def __init__(self, name: str, latex_opening_tag: str, latex_closing_tag: str):
        self._name: str = name
        self._typesetting_clazzes: typing.Dict[Protocol, typing.Tuple[str, str]] = dict()
        # Register the default typesetting opening and closing clazzes for every protocol.
        self.typesetting_clazzes[protocols.latex] = (latex_opening_tag, latex_closing_tag)
        self.typesetting_clazzes[protocols.unicode_limited] = ('', '')
        self.typesetting_clazzes[protocols.unicode_extended] = ('', '')

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

    def typeset(self, content: typing.Generator[str, None, None], protocol: Protocol) -> typing.Generator[
        str, None, None]:
        """Typeset some arbitrary content by yielding strings, enclosing content in applicable clazzes."""
        yield self.typesetting_clazzes[protocol][0]  # Opening tag
        yield from content
        yield self.typesetting_clazzes[protocol][1]  # Closing tag

    @property
    def typesetting_clazzes(self) -> typing.Dict[Protocol, typing.Tuple[str, str]]:
        return self._typesetting_clazzes


class FontVariants:
    """A catalog of out-of-the-box font-variants."""

    def __init__(self):
        self._italic = FontVariant(name='italic', latex_opening_tag='\\textit{', latex_closing_tag='}')
        self._normal = FontVariant(name='normal', latex_opening_tag='', latex_closing_tag='')

    def get(self, name) -> FontVariant:
        try:
            # Use getattr to get the value of the property by name
            item = getattr(self, name)
            if not isinstance(item, FontVariant):
                raise Exception('incorrect property')
            return item
        except AttributeError:
            # Handle the case where the property does not exist
            raise Exception('incorrect property')

    @property
    def italic(self) -> FontVariant:
        """The italic font-variant."""
        return self._italic

    @property
    def normal(self) -> FontVariant:
        """The normal font-variant."""
        return self._normal


font_variants = FontVariants()


class FontWeight:
    """A typesetting font-weight."""

    def __init__(self, name: str, latex_opening_tag: str, latex_closing_tag: str):
        self._name: str = name
        self._typesetting_clazzes: typing.Dict[Protocol, typing.Tuple[str, str]] = dict()
        # Register the default typesetting opening and closing clazzes for every protocol.
        self.typesetting_clazzes[protocols.latex] = (latex_opening_tag, latex_closing_tag)
        self.typesetting_clazzes[protocols.unicode_limited] = ('', '')
        self.typesetting_clazzes[protocols.unicode_extended] = ('', '')

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

    def typeset(self, content: typing.Generator[str, None, None], protocol: Protocol) -> typing.Generator[
        str, None, None]:
        """Typeset some arbitrary content by yielding strings, enclosing content in applicable clazzes."""
        yield self.typesetting_clazzes[protocol][0]  # Opening tag
        yield from content
        yield self.typesetting_clazzes[protocol][1]  # Closing tag

    @property
    def typesetting_clazzes(self) -> typing.Dict[Protocol, typing.Tuple[str, str]]:
        return self._typesetting_clazzes


class FontWeights:
    """A catalog of out-of-the-box font weights."""

    def __init__(self):
        self._bold = FontWeight(name='regular', latex_opening_tag='\\mathbf{', latex_closing_tag='}')
        self._regular = FontWeight(name='bold', latex_opening_tag='', latex_closing_tag='')
        self._default = self._regular
        self._fail_safe = self._regular

    @property
    def bold(self) -> FontWeight:
        """The bold font-weight."""
        return self._bold

    def get(self, name) -> FontWeight:
        try:
            # Use getattr to get the value of the property by name
            item = getattr(self, name)
            if not isinstance(item, FontWeight):
                raise Exception('incorrect property')
            return item
        except AttributeError:
            # Handle the case where the property does not exist
            raise Exception('incorrect property')

    @property
    def regular(self) -> FontWeight:
        """The regular font-weight."""
        return self._regular


font_weights = FontWeights()


class BaseSymbol:
    """A base symbol is a symbol that may be typeset with font-family, font-variant, and font-weight,
    and protocol."""

    def __init__(self, name: str, category: SymbolCategory):
        self._name = name
        self._category = category
        self._typesetting_methods: typing.Dict[FontCase, typing.Dict[FontFamily, typing.Dict[
            FontVariant, typing.Dict[FontWeight, typing.Dict[Protocol, typing.Tuple[str, str, str]]]]]] = dict()

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return self._name

    def __str__(self):
        global font_cases
        global font_families
        global font_variants
        global font_weights
        global protocols
        return ''.join(self.typeset(font_case=font_cases.lowercase, font_family=font_families.serif,
            font_variant=font_variants.normal, font_weight=font_weights.regular, protocol=protocols.unicode_limited))

    def register_typesetting_method(self, font_case: FontCase, font_family: FontFamily, font_variant: FontVariant,
        font_weight: FontWeight, latex_opening_tag: str, latex_content: str, latex_closing_tag: str,
        unicode_limited_content: str, unicode_extended_content: str) -> None:
        """Register a typesetting method for the given protocol, treatment, and language.
        If protocol, treatment, and/or language are not specified, use the defaults.
        If default protocol, treatment, and/or language are not defined, use the fail-safe.
        If a typesetting method was already registered for the given protocol, treatment, and language, substitute
        the previously registered method with the new one."""
        global font_cases
        global font_families
        global font_variants
        global font_weights
        global protocols
        if font_case not in self.typesetting_methods:
            self.typesetting_methods[font_case]: typing.Dict[FontFamily, typing.Dict[
                FontVariant, typing.Dict[FontWeight, typing.Dict[Protocol, typing.Callable]]]] = dict()
        if font_family not in self.typesetting_methods[font_case]:
            self.typesetting_methods[font_case][font_family]: typing.Dict[FontFamily, typing.Dict[
                FontVariant, typing.Dict[FontWeight, typing.Dict[Protocol, typing.Callable]]]] = dict()
        if font_variant not in self.typesetting_methods[font_case][font_family]:
            self.typesetting_methods[font_case][font_family][font_variant]: typing.Dict[
                FontFamily, typing.Dict[FontWeight, typing.Dict[Protocol, typing.Callable]]] = dict()
        if font_weight not in self.typesetting_methods[font_case][font_family][font_variant]:
            self.typesetting_methods[font_case][font_family][font_variant][font_weight]: typing.Dict[
                Protocol, typing.Tuple[str, str, str]] = dict()
        self.typesetting_methods[font_case][font_family][font_variant][font_weight][protocols.unicode_limited] = (
            '', unicode_limited_content, '')
        self.typesetting_methods[font_case][font_family][font_variant][font_weight][protocols.latex] = (
            latex_opening_tag, latex_content, latex_closing_tag)
        self.typesetting_methods[font_case][font_family][font_variant][font_weight][protocols.unicode_extended] = (
            '', unicode_extended_content, '')

    def typeset(self, font_case: FontCase, font_family: FontFamily, font_variant: FontVariant, font_weight: FontWeight,
        protocol: Protocol) -> typing.Generator[str, None, None]:
        """Typeset this object by yielding strings."""
        global font_cases
        global font_families
        global font_variants
        global font_weights
        global protocols
        if font_case is None or font_case not in self.typesetting_methods:
            raise Exception('Missing typesetting font_case error.')
        if font_family is None or font_family not in self.typesetting_methods[font_case]:
            raise Exception('Missing typesetting font_family error.')
        if font_variant is None or font_variant not in self.typesetting_methods[font_case][font_family]:
            raise Exception('Missing typesetting font_variant error.')
        if font_weight is None or font_weight not in self.typesetting_methods[font_case][font_family][font_variant]:
            raise Exception('Missing typesetting font_weight error.')
        if protocol is None or protocol not in self.typesetting_methods[font_case][font_family][font_variant][
            font_weight]:
            raise Exception('Missing typesetting protocol error.')
        yield ''.join(self.typesetting_methods[font_case][font_family][font_variant][font_weight][protocol])

    @property
    def typesetting_methods(self) -> typing.Dict[FontCase, typing.Dict[FontFamily, typing.Dict[
        FontVariant, typing.Dict[FontWeight, typing.Dict[Protocol, typing.Tuple[str, str, str]]]]]]:
        return self._typesetting_methods


def yield_csv_rows(file_name):
    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the full path to the data folder and CSV file
    data_folder_path = os.path.join(current_directory, '../../data')
    csv_file_path = os.path.join(data_folder_path, file_name)

    # Load and read the CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')  # delimiter='\t')

        # Loop through the records
        for row in csv_reader:
            yield row


base_symbols: typing.Dict[str, BaseSymbol] = dict()
"""A complete database of symbols."""

unicode_index: typing.Dict[str, BaseSymbol] = dict()
"""An index to lookup base-symbols from unicode characters."""


# TODO: Implement a caching mechanism to speed unicode transformations.

def load_symbols():
    global base_symbols
    global unicode_index
    base_symbols = dict()
    for row in yield_csv_rows(file_name='base_symbols_database.csv'):
        name = row['name']
        current_symbol: BaseSymbol
        if name not in base_symbols:
            symbol_category: SymbolCategory = symbol_categories.get(row['category'])
            current_symbol = BaseSymbol(name=name, category=symbol_category)
            base_symbols[name] = current_symbol
        else:
            current_symbol = base_symbols[name]
        font_case = font_cases.get_from_name(row['font_case'])
        font_family = font_families.get(row['font_family'])
        font_variant = font_variants.get(row['font_variant'])
        font_weight = font_weights.get(row['font_weight'])
        latex_content = row['latex_content']
        unicode_limited_content = row['unicode_limited_content']
        unicode_extended_content = row['unicode_extended_content']
        if unicode_extended_content not in unicode_index:
            unicode_index[unicode_extended_content] = current_symbol
        current_symbol.register_typesetting_method(font_case=font_case, font_family=font_family,
            font_variant=font_variant, font_weight=font_weight, latex_content=latex_content,
            unicode_limited_content=unicode_limited_content, unicode_extended_content=unicode_extended_content)


load_symbols()


def style_unicode(unicode: str, font_family: FontFamily, font_variant: FontVariant, font_weight: FontWeight) -> \
    typing.Generator[str, None, None]:
    """Makes a best effort to change the style of a unicode string."""
    global unicode_index
    for c in unicode:
        font_case: FontCase = font_cases.get_from_character(character=c)
        if c not in unicode_index:
            # This symbol is not present in our database of well-known symbols.
            # Our best effort consists in yielding it as is.
            yield c
        else:
            # This symbol is present in our database of well-known symbols.
            base_symbol: BaseSymbol = unicode_index[c]
            yield StyledSymbol(base_symbol=base_symbol, font_case=font_case, font_family=font_family,
                font_variant=font_variant, font_weight=font_weight).as_unicode_extended()


class Greeks:
    def __init__(self):
        global base_symbols
        self._alpha = base_symbols['Greek alpha']
        self._beta = base_symbols['Greek beta']
        self._gamma = base_symbols['Greek gamma']
        self._delta = base_symbols['Greek delta']
        self._epsilon = base_symbols['Greek epsilon']
        self._zeta = base_symbols['Greek zeta']
        self._eta = base_symbols['Greek eta']
        self._theta = base_symbols['Greek theta']
        self._iota = base_symbols['Greek iota']
        self._kappa = base_symbols['Greek kappa']
        self._lambda = base_symbols['Greek lambda']
        self._mu = base_symbols['Greek mu']
        self._nu = base_symbols['Greek nu']
        self._xi = base_symbols['Greek xi']
        self._omicron = base_symbols['Greek omicron']
        self._pi = base_symbols['Greek pi']
        self._rho = base_symbols['Greek rho']
        self._sigma = base_symbols['Greek sigma']
        self._tau = base_symbols['Greek tau']
        self._upsilon = base_symbols['Greek upsilon']
        self._phi = base_symbols['Greek phi']
        self._chi = base_symbols['Greek chi']
        self._psi = base_symbols['Greek psi']
        self._omega = base_symbols['Greek omega']

    @property
    def alpha(self) -> BaseSymbol:
        return self._alpha

    @property
    def beta(self) -> BaseSymbol:
        return self._beta

    @property
    def gamma(self) -> BaseSymbol:
        return self._gamma

    @property
    def delta(self) -> BaseSymbol:
        return self._delta

    @property
    def epsilon(self) -> BaseSymbol:
        return self._epsilon

    @property
    def zeta(self) -> BaseSymbol:
        return self._zeta

    @property
    def eta(self) -> BaseSymbol:
        return self._eta

    @property
    def theta(self) -> BaseSymbol:
        return self._theta

    @property
    def iota(self) -> BaseSymbol:
        return self._iota

    @property
    def kappa(self) -> BaseSymbol:
        return self._kappa

    @property
    def lambda2(self) -> BaseSymbol:
        """N.B.: lambda is renamed to lambda2 to avoid a name conflict with the Python lambda reserved word."""
        return self._lambda

    @property
    def mu(self) -> BaseSymbol:
        return self._mu

    @property
    def nu(self) -> BaseSymbol:
        return self._nu

    @property
    def xi(self) -> BaseSymbol:
        return self._xi

    @property
    def omicron(self) -> BaseSymbol:
        return self._omicron

    @property
    def pi(self) -> BaseSymbol:
        return self._pi

    @property
    def rho(self) -> BaseSymbol:
        return self._rho

    @property
    def sigma(self) -> BaseSymbol:
        return self._sigma

    @property
    def tau(self) -> BaseSymbol:
        return self._tau

    @property
    def upsilon(self) -> BaseSymbol:
        return self._upsilon

    @property
    def phi(self) -> BaseSymbol:
        return self._phi

    @property
    def chi(self) -> BaseSymbol:
        return self._chi

    @property
    def psi(self) -> BaseSymbol:
        return self._psi

    @property
    def omega(self) -> BaseSymbol:
        return self._omega


greeks = Greeks()


class StyledSymbol:
    """A styled symbol is a symbol with all styling properties defined: font-case, font-family, font-variant,
    and font-weight."""

    def __init__(self, base_symbol: BaseSymbol, font_case: FontCase, font_family: FontFamily, font_variant: FontVariant,
        font_weight: FontWeight):
        self._base_symbol = base_symbol
        self._font_case = font_case
        self._font_family = font_family
        self._font_variant = font_variant
        self._font_weight = font_weight

    def __hash__(self):
        return hash((self.base_symbol, self.font_case, self.font_family, self.font_variant, self.font_weight))

    def __repr__(self):
        global protocols
        return ''.join(self.typeset(protocol=protocols.unicode_limited))

    def __str__(self):
        global protocols
        return ''.join(self.typeset(protocol=protocols.unicode_limited))

    def as_latex(self):
        return ''.join(self.typeset(protocol=protocols.latex))

    def as_unicode_limited(self):
        return ''.join(self.typeset(protocol=protocols.unicode_limited))

    def as_unicode_extended(self):
        return ''.join(self.typeset(protocol=protocols.unicode_extended))

    @property
    def base_symbol(self) -> BaseSymbol:
        return self._base_symbol

    @property
    def font_case(self) -> FontCase:
        return self._font_case

    @property
    def font_family(self) -> FontFamily:
        return self._font_family

    @property
    def font_variant(self) -> FontVariant:
        return self._font_variant

    @property
    def font_weight(self) -> FontWeight:
        return self._font_weight

    def typeset(self, protocol: typing.Optional[Protocol] = None) -> typing.Generator[str, None, None]:
        yield from self.base_symbol.typeset(font_case=self.font_case, font_family=self.font_family,
            font_variant=self.font_variant, font_weight=self.font_weight, protocol=protocol)


phi_bold = StyledSymbol(base_symbol=greeks.phi, font_case=font_cases.lowercase, font_family=font_families.serif,
    font_variant=font_variants.normal, font_weight=font_weights.bold)
print(phi_bold.as_unicode_extended())
print(''.join(phi_bold.typeset(protocol=protocols.unicode_extended)))
print(phi_bold)


class StyledText:
    """A text string a single style composed of font-family, font-variant, and font-weight.
    Note that font-case is free at the character-level."""

    def __init__(self, content: str, font_family: FontFamily, font_variant: FontVariant, font_weight: FontWeight):
        super()
        self._content = content
        self._font_family = font_family
        self._font_variant = font_variant
        self._font_weight = font_weight

    def __hash__(self):
        return hash((self.content, self.font_family, self.font_variant, self.font_weight))

    def __repr__(self):
        global protocols
        return ''.join(self.typeset(protocol=protocols.unicode_limited))

    def __str__(self):
        global protocols
        return ''.join(self.typeset(protocol=protocols.unicode_limited))

    def as_latex(self) -> str:
        return ''.join(self.typeset(protocol=protocols.latex))

    def as_unicode_limited(self) -> str:
        return ''.join(self.typeset(protocol=protocols.unicode_limited))

    def as_unicode_extended(self) -> str:
        return ''.join(self.typeset(protocol=protocols.unicode_extended))

    @property
    def content(self) -> str:
        return self._content

    @property
    def font_family(self) -> FontFamily:
        return self._font_family

    @property
    def font_variant(self) -> FontVariant:
        return self._font_variant

    @property
    def font_weight(self) -> FontWeight:
        return self._font_weight

    def typeset(self, protocol: Protocol) -> typing.Generator[str, None, None]:
        # TODO: Implement font-family with same approach than font-weight
        generator_1: typing.Generator[str, None, None] = self._typeset_content(protocol=protocol)
        generator_2: typing.Generator[str, None, None] = self.font_weight.typeset(content=generator_1,
            protocol=protocol)
        generator_3: typing.Generator[str, None, None] = self.font_variant.typeset(content=generator_2,
            protocol=protocol)
        yield from generator_3

    def _typeset_content(self, protocol: Protocol) -> typing.Generator[str, None, None]:
        """This is a private method."""
        if protocol == protocols.unicode_extended:
            # Unicode formatting is implemented at the single character level,
            # a transformation of the content is necessary.
            yield from style_unicode(unicode=self.content, font_family=self.font_family, font_variant=self.font_variant,
                font_weight=self.font_weight)
        else:
            # Otherwise, we assume that the protocol is based on clazzes,
            # and that the content can be yield as is.
            # This may evolve in the future with the implementation of other protocols.
            yield self.content


test_1 = StyledText(content='hello world αβγ', font_family=font_families.serif, font_variant=font_variants.normal,
    font_weight=font_weights.regular)
test_2 = StyledText(content='hello world αβγ', font_family=font_families.serif, font_variant=font_variants.normal,
    font_weight=font_weights.bold)
print(''.join(test_1.typeset(protocol=protocols.latex)))
print(''.join(test_2.typeset(protocol=protocols.latex)))
print(test_1.as_latex())
print(test_1.as_unicode_extended())
print(test_2.as_unicode_extended())


class TypesettableObject(abc.ABC):
    """The typesettable-object abstract class makes it possible to equip some object in such a way
    that may be typeset by registering typesetting methods for the desired treatments and languages."""

    _typesetting_methods: typing.Dict[Treatment, typing.Dict[Language, typing.Callable]] = dict()

    def __init__(self):
        pass

    def __repr__(self):
        return ''.join(self.typeset())

    def __str__(self):
        return ''.join(self.typeset())

    @staticmethod
    def register_typesetting_method(method: typing.Callable, protocol: typing.Optional[Protocol] = None,
        treatment: typing.Optional[Treatment] = None, language: typing.Optional[Language] = None) -> None:
        """Register a typesetting method for the given protocol, treatment, and language.
        If protocol, treatment, and/or language are not specified, use the defaults.
        If default protocol, treatment, and/or language are not defined, use the fail-safe.
        If a typesetting method was already registered for the given protocol, treatment, and language, substitute
        the previously registered method with the new one."""
        global protocols
        global treatments
        global languages
        TypesettableObject._typesetting_methods[protocol][treatment][language]: typing.Callable = method

    def typeset(self, protocol: typing.Optional[Protocol] = None, treatment: typing.Optional[Treatment] = None,
        language: typing.Optional[Language] = None, flavor: typing.Optional[Flavor] = None) -> typing.Generator[
        str, None, None]:
        """Typeset this object by yielding strings."""
        global protocols
        global treatments
        global languages
        if treatment is None or treatment not in self.typesetting_methods:
            raise Exception('Missing typesetting treatment error.')
        if language is None or language not in self.typesetting_methods[treatment]:
            raise Exception('Missing typesetting language error.')
        yield from TypesettableObject.typesetting_methods[treatment][language](protocol=protocol)

    @property
    def typesetting_methods(self) -> typing.Dict[Treatment, typing.Dict[Language, typing.Callable]]:
        return TypesettableObject._typesetting_methods
