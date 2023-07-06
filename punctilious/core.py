from __future__ import annotations
import collections.abc
import textwrap
import warnings
import repm
import contextlib
import abc
import collections
import networkx as nx
import unicode
import unidecode


class TextStyle:
    """A supported text style."""

    def __init__(self, font_style_name: str, unicode_table_index: int, latex_math_start_tag: str,
                 latex_math_end_tag: str):
        self.font_style_name = font_style_name
        self.unicode_table_index = unicode_table_index
        self.latex_math_start_tag = latex_math_start_tag
        self.latex_math_end_tag = latex_math_end_tag

    def __eq__(self, other):
        return type(other) is type(self) and hash(self) == hash(other)

    def __hash__(self):
        return hash((TextStyle, self.font_style_name))

    def __repr__(self):
        return self.font_style_name

    def __str__(self):
        return self.font_style_name


class TextStyles:
    """Expose a catalog of supported text-styles."""

    def __init__(self):
        self._no_style = TextStyle(
            font_style_name='no-style',
            unicode_table_index=unicode.unicode_sans_serif_normal_index,
            latex_math_start_tag=r'',
            latex_math_end_tag=r'')
        self.double_struck = TextStyle(
            font_style_name='double-struck',
            unicode_table_index=unicode.unicode_double_struck_index,
            latex_math_start_tag=r'\mathbb{',
            latex_math_end_tag=r'}')
        self.monospace = TextStyle(
            font_style_name='fraktur-normal',
            unicode_table_index=unicode.unicode_fraktur_normal_index,
            latex_math_start_tag=r'\mathfrak{',
            latex_math_end_tag=r'}')
        self.monospace = TextStyle(
            font_style_name='monospace',
            unicode_table_index=unicode.unicode_monospace_index,
            latex_math_start_tag=r'\mathtt{',
            latex_math_end_tag=r'}')
        self.sans_serif_bold = TextStyle(
            font_style_name='sans-serif-bold',
            unicode_table_index=unicode.unicode_sans_serif_bold_index,
            latex_math_start_tag=r'\boldsymbol\mathsf{',
            latex_math_end_tag=r'}}')
        self.sans_serif_normal = TextStyle(
            font_style_name='sans-serif-normal',
            unicode_table_index=unicode.unicode_sans_serif_normal_index,
            latex_math_start_tag=r'\mathsf{',
            latex_math_end_tag=r'}')
        self.script_normal = TextStyle(
            font_style_name='script-normal',
            unicode_table_index=unicode.unicode_script_normal_index,
            latex_math_start_tag=r'\mathcal{',
            latex_math_end_tag=r'}')
        self.serif_bold = TextStyle(
            font_style_name='serif-bold',
            unicode_table_index=unicode.unicode_serif_bold_index,
            latex_math_start_tag=r'\mathbf{',
            latex_math_end_tag=r'}')
        self.serif_italic = TextStyle(
            font_style_name='serif-italic',
            unicode_table_index=unicode.unicode_serif_italic_index,
            latex_math_start_tag=r'\mathit{',
            latex_math_end_tag=r'}')
        self.serif_normal = TextStyle(
            font_style_name='serif-normal',
            unicode_table_index=unicode.unicode_serif_normal_index,
            latex_math_start_tag=r'\mathnormal{',
            latex_math_end_tag=r'}')

    @property
    def no_style(self):
        """The ⌜no_style⌝ text-style is a neutral style.
        Rendering defaults to sans-serif-normal.
        It is expected to be overriden by passing the text_style parameter to the rendering method."""
        return self._no_style


text_styles = TextStyles()


class TextFormat:
    """A supported output text format."""

    def __init__(self, text_format_name: str):
        self._text_format_name = text_format_name

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((TextFormat, self._text_format_name))

    def __repr__(self):
        return self._text_format_name

    def __str__(self):
        return self._text_format_name


class TextFormats:
    def __init__(self):
        self.latex_math = TextFormat('latex-math')
        self.plaintext = TextFormat('plaintext')
        self.unicode = TextFormat('unicode')


text_formats = TextFormats()


class NameType(repm.ValueName):
    """A distinctive type of name supported to designate objects."""

    def __init__(self, value_name: str):
        super().__init__(value_name=value_name)


class NameTypes(repm.ValueName):
    """A catalog of supported name types."""

    def __init__(self, value_name: str):
        super().__init__(value_name=value_name)
        self._symbol = NameType('symbol')
        self._acronym = NameType('acronym')
        self._name = NameType('name')
        self._explicit_name = NameType('explicit name')

    @property
    def symbol(self) -> NameType:
        """A single-character representation, e.g.: ⌜=⌝,⌜x⌝,⌜∀⌝."""
        return self._symbol

    @property
    def acronym(self) -> NameType:
        """A shortened representation composed as a subset of the name characters, e.g.: ⌜qed⌝,⌜max⌝,⌜mp⌝."""
        return self._acronym

    @property
    def name(self) -> NameType:
        """A conventional representation, e.g.: ⌜equal⌝,⌜conjunction⌝."""
        return self._name

    @property
    def explicit_name(self) -> NameType:
        """An extended representation, e.g.: ⌜logical-and⌝,⌜if-and-only-if⌝."""
        return self._explicit_name


name_types = NameTypes(value_name='name types')
"""The catalog of the supported types of names / symbolic representations used to identify objects."""


def equal_not_none(s1: (None, str), s2: (None, str)):
    """Compare 2 strings are return if they are equal, unless either or both are None."""
    return False if s1 is None or s2 is None else s1 == s2


class StyledText:
    """A styled-text is a string of text that:
    - is of a supported text_style,
    - may support one or several text_format outputs."""

    def __init__(self, s: (None, str) = None, text_style: (None, TextStyle) = None,
                 plaintext: (None, str) = None, unicode: (None, str) = None,
                 latex_math: (None, str) = None
                 ):
        """

        :param s: A string. Leave it to the constructor to interpret if it is plaintext or unicode.
        :param plaintext:
        :param unicode:
        :param latex_math:
        :param text_style:
        """
        if s is not None and plaintext is None and s == unidecode.unidecode(s):
            plaintext = s
        if s is not None and unicode is None and s != unidecode.unidecode(s):
            unicode = s
        if unicode is not None and plaintext is None:
            if str(unicode).isalnum():
                # This is a best-effort mapping to plaintext.
                # It may lead to undesirable results,
                # e.g. symbol '¬' is mapped to '!'.
                # To avoid this, isalnum() is used as a temporary solution.
                plaintext = unidecode.unidecode(unicode)
        if text_style is None:
            text_style = text_styles.serif_normal
        self._plaintext = plaintext if plaintext != '' else None
        self._unicode = unicode if unicode != '' else None
        self._latex_math = latex_math if latex_math != '' else None
        self._text_style = text_style if text_style != '' else None

    def __eq__(self, other: (None, object, StyledText)) -> bool:
        """Two instances of TextStyle are equal if any of their formatted representation are equal and not None."""
        return type(self) is type(other) and \
            (self.text_style == other.text_style) and \
            (equal_not_none(self.plaintext, other.plaintext) or
             equal_not_none(self.unicode, other.unicode) or
             equal_not_none(self.latex_math, other.latex_math))

    def __hash__(self):
        """Two styled-texts are considered distinct if either their plaintext content or their style are distinct."""
        return hash(
            (StyledText, self._plaintext, self._unicode, self._latex_math, self._text_style))

    def __repr__(self) -> str:
        try:
            return self.rep()
        except:
            return repr(self.to_dict())

    def __str__(self) -> str:
        return self.rep()

    @property
    def latex_math(self) -> (None, str):
        return self._latex_math

    @property
    def plaintext(self) -> (None, str):
        return self._plaintext

    def rep(self, text_format: TextFormat = text_formats.plaintext, cap: bool = False):
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        match text_format:
            case text_formats.plaintext:
                return self.rep_as_plaintext(cap=cap)
            case text_formats.latex_math:
                return self.rep_as_latex_math(cap=cap)
            case text_formats.unicode:
                return self.rep_as_unicode(cap=cap)
            case _:
                return self.rep_as_plaintext(cap=cap)

    def rep_as_latex_math(self, cap: bool = False):
        content = self._plaintext if self._latex_math is None else self._latex_math
        content = content.capitalize() if cap else content
        return f'{self._text_style.latex_math_start_tag}{content}{self._text_style.latex_math_end_tag}'

    def rep_as_plaintext(self, cap: bool = False):
        content = self._plaintext
        content = content.capitalize() if cap else content
        return content

    def rep_as_unicode(self, cap: bool = False):
        content = self._plaintext if self._unicode is None else self._unicode
        content = content.capitalize() if cap else content
        return unicode.unicode_format(content, self._text_style.unicode_table_index)

    @property
    def text_style(self) -> TextStyle:
        return self._text_style

    def to_dict(self) -> dict:
        return {
            '_plaintext':  self._plaintext,
            '_unicode':    self._unicode,
            '_latex_math': self._latex_math,
            '_text_style': self._text_style
        }

    @property
    def unicode(self) -> (None, str):
        return self._unicode


def subscriptify(text: (str, StyledText) = '', text_format: TextFormat = text_formats.plaintext):
    text_format = get_config(text_format, configuration.text_format,
                             fallback_value=text_formats.plaintext)
    if text is None:
        return ''
    match text_format:
        case text_formats.plaintext:
            return text
        case text_formats.unicode:
            if isinstance(text, StyledText):
                # The Unicode set of subscript characters is very limited,
                # subscriptification must be executed on the plaintext value
                # of the Unicode string.
                text = text.rep_as_plaintext()
            return unicode.unicode_subscriptify(text)
        case text_formats.latex_math:
            return f'_{{{text}}}'
        case _:
            return text


class VerificationSeverity(repm.ValueName):
    def __init__(self, name):
        super().__init__(name)


class VerificationSeverities(repm.ValueName):
    def __init__(self, name):
        super().__init__(name)
        self.verbose = VerificationSeverity('verbose')
        self.information = VerificationSeverity('information')
        self.warning = VerificationSeverity('warning')
        self.error = VerificationSeverity('error')


verification_severities = VerificationSeverities('verification_severities')


def verify(
        assertion, msg,
        severity: VerificationSeverity = verification_severities.error, **kwargs):
    if not assertion:
        contextual_information = ''
        for key, value in kwargs.items():
            value_as_string = f'(str conversion failure of type {str(type(value))})'
            try:
                value_as_string = value.rep_as_fully_qualified_name()
            except AttributeError:
                try:
                    value_as_string = repr(value)
                finally:
                    pass
            finally:
                pass
            contextual_information += f'\n{key}: {value_as_string}'
        report = f'{str(severity).upper()}: {msg}\nContextual information:{contextual_information}'
        repm.prnt(report)
        if severity is verification_severities.warning:
            warnings.warn(report)
        if configuration.raise_exception_on_verification_error and severity is verification_severities.error:
            raise FailedVerificationException(msg=report, **kwargs)


class InconsistencyWarning(UserWarning):
    pass


class Configuration:
    """Configuration settings.

    This class allows the storage of all punctilious configuration and preference settings.

    """

    def __init__(self):
        self.auto_index = None
        self._echo_default = False
        self.default_relation_nameset = 'r'
        self.echo_axiom_declaration = None
        self.echo_axiom_inclusion = None
        self.echo_definition_declaration = None
        self.echo_definition_inclusion = None
        self.echo_definition_direct_inference = None
        self.echo_formula_declaration = False  # In general, this is too verbose.
        self.echo_hypothesis = None
        self.echo_inferred_statement = None
        self.echo_note = None
        self.echo_relation = None
        self.echo_simple_objct_declaration = None
        self.echo_statement = None
        self.echo_symbolic_objct = None
        self.echo_theory_elaboration_sequence_declaration = None
        self.echo_universe_of_discourse_declaration = None
        self.echo_free_variable_declaration = None
        self.echo_text_format = None
        self.output_index_if_max_index_equal_1 = False
        self.raise_exception_on_verification_error = True
        self.title_text_style = text_styles.sans_serif_bold
        self.text_format = text_formats.unicode
        self.text_output_indent = 2
        self.text_output_statement_column_width = 70
        self.text_output_justification_column_width = 40
        self.text_output_total_width = 122
        self.warn_on_inconsistency = True

    @property
    def echo_default(self) -> (None, bool):
        return self._echo_default

    @echo_default.setter
    def echo_default(self, value: (None, bool)):
        self._echo_default = value


configuration = Configuration()


def get_config(*args, fallback_value):
    """Return the first not None value."""
    for a in args:
        if a is not None:
            return a
    return fallback_value


def unpack_formula(o: (TheoreticalObject, Formula, FormulaStatement)) -> Formula:
    """Receive a theoretical-objct and unpack its formula if it is a statement that contains a formula."""
    verify(
        is_in_class(o, classes.theoretical_objct),
        'Parameter ⌜o⌝ must be an element of the theoretical-objct declarative-class.',
        o=o)
    if hasattr(o, 'valid_proposition'):
        # Unpack python objects that "contain" their formula,
        # such as FormulaStatement, DirectAxiomInference, etc.
        return o.valid_proposition
    else:
        return o


class Consistency(repm.ValueName):
    """A qualification regarding the consistency of a theory."""

    def __init__(self, name):
        super().__init__(name)


class ConsistencyValues(repm.ValueName):
    """The list of consistency values."""

    def __init__(self, name):
        super().__init__(name)

    proved_consistent = Consistency('proved-consistent')
    proved_inconsistent = Consistency('proved-inconsistent')
    undetermined = Consistency('undetermined')


consistency_values = ConsistencyValues('consistency-values')
"""The list of consistency values."""


class DeclarativeClass(repm.ValueName):
    """The DeclarativeClass python class models a declarative-class."""

    def __init__(self, name, natural_language_name):
        super().__init__(name)


class DeclarativeClassList(repm.ValueName):
    """A list of of well-known declarative-classes."""

    def __init__(self, name, natural_language_name):
        super().__init__(name)
        self.atheoretical_statement = DeclarativeClass('atheoretical_statement',
                                                       'atheoretical-statement')
        self.axiom = DeclarativeClass('axiom', 'axiom')
        self.axiom_inclusion = DeclarativeClass('axiom_inclusion', 'axiom-inclusion')
        self.definition = DeclarativeClass('definition', 'definition')
        self.definition_inclusion = DeclarativeClass('definition_inclusion', 'definition-inclusion')
        self.direct_axiom_inference = DeclarativeClass('direct_axiom_inference',
                                                       'direct-axiom-inference')
        self.direct_definition_inference = DeclarativeClass('direct_definition_inference',
                                                            'direct-definition-inference')
        self.formula = DeclarativeClass('formula', 'formula')
        self.formula_statement = DeclarativeClass('formula_statement', 'formula-statement')
        self.free_variable = DeclarativeClass('free_variable', 'free-variable')
        self.hypothesis = DeclarativeClass('hypothesis', 'hypothesis')
        self.inference_rule = DeclarativeClass('inference_rule', 'inference-rule')
        self.inference_rule_inclusion = DeclarativeClass('inference_rule_inclusion',
                                                         'inference-rule-inclusion')
        self.inferred_proposition = DeclarativeClass('inferred_proposition', 'inferred-proposition')
        self.note = DeclarativeClass('note', 'note')
        self.proposition = DeclarativeClass('proposition', 'proposition')
        self.relation = DeclarativeClass('relation', 'relation')
        self.simple_objct = DeclarativeClass('simple_objct', 'simple-objct')
        self.statement = DeclarativeClass('statement', 'statement')
        self.symbolic_objct = DeclarativeClass('symbolic_objct', 'symbolic-objct')
        self.theoretical_objct = DeclarativeClass('theoretical_objct', 'theoretical-objct')
        self.theory_elaboration = DeclarativeClass('theory', 'theory')
        self.universe_of_discourse = DeclarativeClass('universe_of_discourse',
                                                      'universe-of-discourse')
        # Shortcuts
        self.a = self.axiom
        self.dai = self.direct_axiom_inference
        self.ddi = self.direct_definition_inference
        self.f = self.formula
        self.r = self.relation
        self.t = self.theory_elaboration
        self.u = self.universe_of_discourse


"""A list of well-known declarative-classes."""
declarative_class_list = DeclarativeClassList('declarative_class_list', 'declarative-class-list')

"""A list of well-known declarative-classes. A shortcut for p.declarative_class_list."""
classes = declarative_class_list


def is_in_class(
        o: TheoreticalObject,
        c: DeclarativeClass) -> bool:
    """Return True if o is a member of the declarative-class c, False otherwise.

    :param o: An arbitrary python object.
    :param c: A declarative-class.
    :return: (bool).
    """
    # verify(o is not None, 'o is None.', o=o, c=c)
    # verify(hasattr(o, 'is_in_class'), 'o does not have attribute is_in_class.', o=o, c=c)
    verify(callable(getattr(o, 'is_in_class')), 'o.is_in_class() is not callable.', o=o, c=c)
    return o.is_in_class(c)


class FailedVerificationException(Exception):
    """Python custom exception raised whenever a verification fails if
    setting raise_exception_on_verification_failure = True."""

    def __init__(self, msg, **kwargs):
        self.msg = msg
        self.kwargs = kwargs


class UnsupportedInferenceRuleException(Exception):
    """Python custom exception raised if an attempt is made
     to use an inference rule on a theory."""

    def __init__(self, msg, **kwargs):
        self.msg = msg
        self.kwargs = kwargs


def set_attr(o, a, v):
    """A wrapper function for the naive setattr function.
    It set attributes on Tuple instances in a prudent manner.
    """
    assert isinstance(a, str)
    if not hasattr(o, a):
        setattr(o, a, v)
    else:
        assert getattr(o, a) is v


# import rich
# import rich.console
# import rich.markdown
# import rich.table

class NoNameSolutionException(LookupError):
    """The NoNameSolutionException is the exception that is raised when a NameSet cannot be represented because no representation was found for the required TextFormat."""

    def __init__(self, nameset, text_format):
        self.nameset = nameset
        self.text_format = text_format

    def __str__(self):
        return f'The nameset ⌜{repr(self.nameset)}⌝ contains no representation for the ⌜{self.text_format}⌝ text-format.'


class NameSet:
    """A set of qualified names used to identify an object.

    TODO: Enhancement: for relations in particular, add a verb NameType (e.g. implies).
    TODO: Enhancement: add dashed-name here, and a repr_symbolic (i.e. to support plaintext for non-ASCII symbols).
    """

    def __init__(self, s: (None, str) = None, symbol: (None, str, StyledText) = None,
                 index: (None, int, str) = None,
                 acronym: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
                 explicit_name: (None, str, StyledText) = None):
        if s is not None:
            # Shortcut parameter to quickly declare a nameset from a python string,
            # inferring in best-effort mode whether the string represent a symbol,
            # a name, or a representation of another name-type.
            if symbol is None and len(s) == 1:
                # Assumption: a string of a single character represent a symbol.
                symbol = s
            elif explicit_name is None and ' ' in s:
                # Assumption: a string containing some space represent an explicit-name.
                explicit_name = s
            elif name is None and len(s) > 1:
                name = s
        self._symbol = StyledText(s=symbol, text_style=text_styles.serif_italic) \
            if isinstance(symbol, str) else symbol
        self._acronym = StyledText(s=acronym, text_style=text_styles.monospace) \
            if isinstance(acronym, str) else acronym
        self._name = StyledText(s=name, text_style=text_styles.sans_serif_normal) \
            if isinstance(name, str) else name
        self._explicit_name = StyledText(s=explicit_name, text_style=text_styles.sans_serif_normal) \
            if isinstance(explicit_name, str) else explicit_name
        if isinstance(index, int):
            index = str(index)
        self._index = StyledText(s=index, text_style=text_styles.sans_serif_normal) \
            if isinstance(index, str) else index

    def __eq__(self, other):
        """Two NameSets n and m are equal if any of their name-types are equal,
        and their indexes are equal."""
        return type(self) is type(other) and \
            (self.symbol == other.nameset or
             self.acronym == other.acronym or
             self.name == other.name or
             self.explicit_name == other.explicit_name) and \
            self.index == other.index

    def __hash__(self):
        return hash((NameSet, self.symbol, self.acronym, self.name, self.explicit_name, self.index))

    def __repr__(self):
        try:
            return self.rep_compact(text_format=text_formats.plaintext)
        except NoNameSolutionException:
            return repr(self.to_dict())

    def __str__(self):
        try:
            return self.rep_compact(text_format=text_formats.plaintext)
        except NoNameSolutionException:
            return f'nameset {hash(self)}'

    @property
    def acronym(self) -> StyledText:
        return self._acronym

    @property
    def explicit_name(self) -> StyledText:
        return self._explicit_name

    @property
    def index(self) -> str:
        return self._index

    @property
    def name(self) -> StyledText:
        return self._name

    def rep(self, text_format: (None, TextFormat) = None) -> str:
        """Return the default representation for this python obje.

        :return:
        """
        return f'{self.rep_compact(text_format=text_format)}'

    def rep_accurate(self, text_format: (None, TextFormat) = None, cap: (None, bool) = None):
        """Returns the most accurate (longest) possible name in the nameset for the required text-format.

        Order of priority:
        1) explicit-name
        2) name
        3) acronym
        4) symbol
        """
        output = self.rep_explicit_name(text_format=text_format)
        if output is not None:
            return output
        output = self.rep_name(text_format=text_format)
        if output is not None:
            return output
        output = self.rep_acronym(text_format=text_format)
        if output is not None:
            return output
        output = self.rep_symbol(text_format=text_format)
        if output is not None:
            return output
        raise NoNameSolutionException(nameset=self, text_format=text_format)

    def rep_acronym(self, text_format: (None, TextFormat) = None) -> (None, str):
        """Return a string that represent the object as an acronym."""
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        if self._acronym is None:
            return None
        else:
            base = self._acronym.rep(text_format=text_format)
            index = '' if self._index is None else self._index.rep(text_format=text_format)
            output = None if base is None else f'{base}{index}'
            return output

    def rep_compact(self, text_format: (None, TextFormat) = None, cap: (None, bool) = None):
        """Returns the shortest possible name in the nameset for the required text-format.

        Order of priority:
        1) symbol
        2) acronym
        3) name
        4) explicit-name
        """
        output = self.rep_symbol(text_format=text_format)
        if output is not None:
            return output
        output = self.rep_acronym(text_format=text_format)
        if output is not None:
            return output
        output = self.rep_name(text_format=text_format)
        if output is not None:
            return output
        output = self.rep_explicit_name(text_format=text_format)
        if output is not None:
            return output
        raise NoNameSolutionException(nameset=self, text_format=text_format)

    def rep_conventional(self, text_format: (None, TextFormat) = None, cap: (None, bool) = None):
        """Returns the most conventional (default) possible name in the nameset for the required text-format.

        Order of priority:
        2) name
        3) acronym
        4) symbol
        1) explicit-name
        """
        output = self.rep_name(text_format=text_format)
        if output is not None:
            return output
        output = self.rep_acronym(text_format=text_format)
        if output is not None:
            return output
        output = self.rep_symbol(text_format=text_format)
        if output is not None:
            return output
        output = self.rep_explicit_name(text_format=text_format)
        if output is not None:
            return output
        raise NoNameSolutionException(nameset=self, text_format=text_format)

    def rep_explicit_name(self, text_format: (None, TextFormat) = None) -> (None, str):
        """Return a string that represent the object as an explicit name."""
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        if self._explicit_name is None:
            return None
        else:
            base = self._explicit_name.rep(text_format=text_format)
            index = '' if self._index is None else ' ' + self._index.rep(text_format=text_format)
            output = None if base is None else f'{base}{index}'
            return output

    def rep_name(self, text_format: (None, TextFormat) = None) -> (None, str):
        """Return a string that represent the object as a plain name."""
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        if self._name is None:
            return None
        else:
            base = self._name.rep(text_format=text_format)
            index = '' if self._index is None else ' ' + self._index.rep(text_format=text_format)
            output = None if base is None else f'{base}{index}'
            return output

    def rep_symbol(self, text_format: (None, TextFormat) = None) -> (None, str):
        """Return a string that represent the object as a symbol."""
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        if self._symbol is None:
            return None
        else:
            base = self._symbol.rep(text_format=text_format)
            index = subscriptify(text=self._index, text_format=text_format)
            output = None if base is None else f'{base}{index}'
            return output

    @property
    def symbol(self) -> StyledText:
        """The symbol core glyph.

        :return: (StyledText) The symbol core glyph.
        """
        return self._symbol

    def to_dict(self):
        return {
            'symbol':        self._symbol,
            'acronym':       self._acronym,
            'name':          self._name,
            'explicit_name': self._explicit_name
        }


class Title:
    """A title to introduce some symbolic-objcts in reports.

    TODO: QUESTION: rename Title to Name, Category to Nature, Reference to Abridged and Unabridged Name.


    Features:
    - long-names have a short (reference) and long (long-name) version.
    - long-names do not have an index.
    - long-names comprise a category that must be consistent with
        the declarative class of the symbolic-objct.
    """

    def __init__(self, ref: (None, str) = None, cat: (None, TitleCategory) = None,
                 subtitle: (None, str) = None,
                 abr: (None, str) = None):
        self._ref = ref
        self._abr = abr
        self._cat = title_categories.uncategorized if cat is None else cat
        self._subtitle = subtitle
        self._styled_title = None
        self._styled_ref = None

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        """Note that the title attribute is not hashed,
        because title is considered purely decorative.
        """
        return hash((self.cat, self.ref))

    def __repr__(self) -> str:
        return self.rep(text_format=text_formats.plaintext)

    def __str__(self) -> str:
        return self.rep(text_format=text_formats.plaintext)

    @property
    def cat(self) -> TitleCategory:
        """The category of this statement."""
        return self._cat

    @property
    def subtitle(self) -> str:
        """A conditional complement to the automatically structured title."""
        return self._subtitle

    @property
    def ref(self) -> str:
        """Unabridged name."""
        return self._ref

    @property
    def abr(self) -> str:
        """Abridged name."""
        return self._abr

    def rep(self, text_format: (None, TextFormat) = None, cap: bool = False) -> str:
        """Return the default representation for this long-name.

        :param cap: Whether the representation must be capitalized (default: False).
        :return: str
        """
        return self.rep_ref(text_format=text_format, cap=cap)

    def rep_title(self, text_format: (None, TextFormat) = None, cap: (None, bool) = None) -> str:
        """

        :param cap:
        :return:
        """
        return self.styled_title.rep(text_format=text_format, cap=cap)

    def rep_ref(self, text_format: (None, TextFormat) = None, cap: (None, bool) = None) -> str:
        return self.styled_ref.rep(text_format=text_format, cap=cap)

    def rep_mention(self, text_format: (None, TextFormat) = None, cap: (None, bool) = None) -> str:
        return self.styled_mention.rep(text_format=text_format, cap=cap)

    @property
    def styled_ref(self) -> StyledText:
        if self._styled_ref is None:
            text_style = get_config(configuration.title_text_style,
                                    fallback_value=text_styles.sans_serif_normal)
            self._styled_ref = StyledText(
                f'{self.cat.abridged_name}{"" if self.ref is None else " " + self.ref}',
                text_style=text_style)
        return self._styled_ref

    @property
    def styled_mention(self) -> StyledText:
        """A mention is a representation of the format ref + cat."""
        if self._styled_ref is None:
            text_style = get_config(configuration.title_text_style,
                                    fallback_value=text_styles.sans_serif_normal)
            self._styled_ref = StyledText(
                f'{self.ref + "" if self.ref is None else " "}{self.cat.natural_name}',
                text_style=text_style)
        return self._styled_ref

    @property
    def styled_title(self) -> StyledText:
        if self._styled_title is None:
            text_style = get_config(configuration.title_text_style,
                                    fallback_value=text_styles.sans_serif_normal)
            self._styled_title = StyledText(
                f'{self.cat.natural_name}{"" if self.ref is None else " " + self.ref}{"" if self.subtitle is None else " - " + self.subtitle}',
                text_style=text_style)
        return self._styled_title


class DashedName:
    """A dashed-name to provide more semantically meaningful names to symbolic-objcts in reports than symbols.

    Features:
    - Immutable
    """

    def __init__(self, dashed_named):
        verify(isinstance(dashed_named, str), 'dashed-name is not of type str.',
               dashed_named=dashed_named)
        # TODO: Clean string from non-alphanumeric, digits, dash characters, etc.
        self._dashed_name = dashed_named

    def __hash__(self):
        """"""
        return hash((self._dashed_name))

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    def rep(self, text_format: (None, TextFormat) = None) -> str:
        """Return the default representation.
        """
        return self.rep_dashed_name(text_format=text_format)

    def rep_dashed_name(self, text_format: (None, TextFormat) = None) -> str:
        """Return a dashed-name representation.
        """
        # TODO: Implement text_formats
        return self._dashed_name


class SymbolicObject:
    """
    Definition
    ----------
    A symbolic-objct is a python object instance that is assigned symbolic names,
    that is linked to a theory, but that is not necessarily constitutive of the theory.
    """

    def __init__(
            self,
            nameset: (None, str, NameSet),
            universe_of_discourse: (None, UniverseOfDiscourse),
            is_theory_foundation_system: bool = False,
            is_universe_of_discourse: bool = False,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: bool = False):
        echo = get_config(echo, configuration.echo_symbolic_objct, configuration.echo_default,
                          fallback_value=False)
        self._declarative_classes = frozenset()
        is_theory_foundation_system = False if is_theory_foundation_system is None else is_theory_foundation_system
        is_universe_of_discourse = False if is_universe_of_discourse is None else is_universe_of_discourse
        # By design, every symbolic-objct is a component of a theory,
        # unless it is itself a theory-foundation-system,
        # or it is itself a universe-of-discourse.
        assert is_universe_of_discourse or is_in_class(
            universe_of_discourse, classes.u)
        if not isinstance(nameset, NameSet):
            symbol = nameset if isinstance(nameset, StyledText) else None
            symbol = StyledText(plaintext=nameset,
                                text_style=text_styles.serif_italic) if isinstance(nameset,
                                                                                   str) else None
            symbol = StyledText(plaintext='o',
                                text_style=text_styles.serif_italic) if symbol is None else nameset
            index = universe_of_discourse.index_symbol(base=symbol)  # if auto_index else None
            nameset = NameSet(symbol=symbol, index=index)
        self._nameset = nameset
        self._title = title  # Header validation is implemented in parent classes with proper category.
        if isinstance(dashed_name, str):
            dashed_name = DashedName(dashed_name)
        self._dashed_name = dashed_name
        self.is_theory_foundation_system = is_theory_foundation_system
        self._declare_class_membership(classes.symbolic_objct)
        if not is_universe_of_discourse:
            self._universe_of_discourse = universe_of_discourse
            self._universe_of_discourse.cross_reference_symbolic_objct(o=self)
        else:
            self._universe_of_discourse = None
        if echo:
            repm.prnt(self.rep_declaration())

    def __hash__(self):
        # Symbols are unique within their universe-of-discourse,
        # thus hashing can be safely based on the key: U + symbol.
        # With a special case for the universe-of-discourse itself,
        # where hash of the symbol is sufficient.
        return hash(self.nameset) if is_in_class(self, classes.u) else hash(
            (self.universe_of_discourse, self.nameset))

    def __repr__(self):
        return self.rep_name()

    def __str__(self):
        return self.rep_name()

    @property
    def dashed_name(self) -> DashedName:
        return self._dashed_name

    @property
    def declarative_classes(self) -> frozenset[DeclarativeClass]:
        """The set of declarative-classes this symbolic-objct is a member of."""
        return self._declarative_classes

    def _declare_class_membership(self, c: DeclarativeClass):
        """During construction (__init__()), add the declarative-classes this symboli-objct is being made a member of."""
        if not hasattr(self, '_declarative_classes'):
            setattr(self, '_declarative_classes', frozenset())
        self._declarative_classes = self._declarative_classes.union({c})

    def echo(self):
        repm.prnt(self.rep())

    def is_declarative_class_member(self, c: DeclarativeClass) -> bool:
        """True if this symbolic-objct is a member of declarative-class 𝒞, False, otherwise."""
        if hasattr(self, '_declarative_classes'):
            return c in self._declarative_classes
        else:
            return False

    def is_in_class(self, c: DeclarativeClass) -> bool:
        """True if this symbolic-objct is a member of declarative-class 𝒞, False, otherwise.

        A shortcut for o.is_declarative_class_member(...)."""
        return self.is_declarative_class_member(c=c)

    def is_symbol_equivalent(self, o2) -> bool:
        """Returns true if this object and o2 are symbol-equivalent.

        Definition:
        -----------
        Two symbolic-objects o₁ and o₂ are symbol-equivalent if and only if:
         1. o₁ and o₂ have symbol-equivalent theories.¹
         2. o₁ and o₂ have equal symbols.²

        ¹. Theories are symbolic-objects. This recursive condition
           yields a complete path between the objects and the universe-of-discourse.
        ². Remember that every symbolic-object has a unique symbol in its parent theory.

        Note:
        -----
        The symbol-equivalence relation allows to compare any pair of symbolic-objcts, including:
         * Both theoretical and atheoretical objects.
         * Symbolic-objcts linked to distinct theories.
        """
        # A theoretical-object can only be compared with a theoretical-object
        assert isinstance(o2, SymbolicObject)
        if self is o2:
            # If the current symbolic-objct is referencing the same
            # python object instance, by definitions the two python references
            # are referencing the same object.
            return True
        if not self.universe_of_discourse.is_symbol_equivalent(
                o2.universe_of_discourse):
            return False
        if self.nameset != o2.nameset:
            return False
        return True

    def prnt(self, expand=False):
        repm.prnt(self.rep(expand=expand))

    def rep(self, text_format: (None, TextFormat) = None, expand: (None, bool) = None) -> str:
        # If a long-name is available, represent the objct as a reference.
        # Otherwise, represent it as a symbol.
        return self.nameset.rep(text_format=text_format)

    def rep_dashed_name(self, text_format: (None, TextFormat) = None) -> str:
        """"""
        if self.dashed_name is None:
            return ''
        return self.dashed_name.rep_dashed_name(text_format=text_format)

    def rep_declaration(self, text_format: (None, TextFormat) = None) -> str:
        return f'Let {self.rep_name(text_format=text_format)} be a symbolic-objct denoted as ⌜ {self.rep_name(text_format=text_format)} ⌝.'

    def rep_formula(self, text_format: (None, TextFormat) = None,
                    expand: (None, bool) = None) -> str:
        """If supported, return a formula representation,
        a symbolic representation otherwise.

        The objective of the repr_as_formula() method is to
        represent formulae and formula-statements not as symbols
        (e.g.: 𝜑₅) but as expanded formulae (e.g.: (4 > 3)).
        Most symbolic-objcts do not have a formula representation,
        where we fall back on symbolic representation.
        """
        return self.rep_name(text_format=text_format)

    def rep_fully_qualified_name(self, text_format: (None, TextFormat) = None) -> str:
        """"""
        fully_qualified_name = f'⌜{self.rep_dashed_name(text_format=text_format)}⌝ (⌜{self.rep_name(text_format=text_format)}⌝)' if self.dashed_name is not None else f'⌜{self.rep_name(text_format=text_format)}⌝'
        fully_qualified_name += f' entitled “{self.rep_title(text_format=text_format, cap=True)}”' if self.title is not None else ''
        return fully_qualified_name

    def rep_mention(self, text_format: (None, TextFormat) = None) -> str:
        return self.rep_name(
            text_format=text_format) if self.title is None else self.title.rep_mention(
            text_format=text_format)

    def rep_name(self, text_format: (None, TextFormat) = None) -> str:
        # global configuration
        # hide_index = \
        #    not is_in_class(self, classes.u) and \
        #    self.symbol.index == 1 and \
        #    not configuration.output_index_if_max_index_equal_1 and \
        #    not is_in_class(self, classes.universe_of_discourse) and \
        #    self.universe_of_discourse.get_symbol_max_index(self.symbol.base) == 1
        # return self.symbol.rep(hide_index=hide_index)
        return self.nameset.rep(text_format=text_format)

    def rep_ref(self, text_format: (None, TextFormat) = None, cap: (None, bool) = None) -> str:
        return self.rep_name(text_format=text_format) if self.title is None else self.title.rep_ref(
            text_format=text_format, cap=cap)

    def rep_reference(self, text_format: (None, TextFormat) = None,
                      cap: (None, bool) = None) -> str:
        global configuration
        if self.title is None:
            # If we have no long-name for this symbolic-objct,
            # we use the (mandatory) symbol as a fallback method.
            return self.rep_name(text_format=text_format)
        return self.title.rep_ref(text_format=text_format, cap=cap)

    def rep_title(self, text_format: (None, TextFormat) = None, cap: (None, bool) = None) -> str:
        global configuration
        if self.title is None:
            # If we have no long-name for this symbolic-objct,
            # we fallback on the (mandatory) symbol.
            return self.rep_name(text_format=text_format)
        return self.title.rep_title(text_format=text_format, cap=cap)

    def rep_title_2(self, text_format: (None, TextFormat) = None, cap: (None, bool) = None) -> str:
        return self.rep_name(
            text_format=text_format) if self.title is None else self.title.rep_title(
            text_format=text_format, cap=cap)

    @property
    def nameset(self) -> NameSet:
        """Every symbolic-object that is being referenced must be assigned a unique symbol in its universe-of-discourse."""
        return self._nameset

    @property
    def title(self) -> Title:
        return self._title

    @property
    def u(self):
        """This symbolic-object''s universe of discourse. Full name: o.universe_of_discourse."""
        return self.universe_of_discourse

    @property
    def universe_of_discourse(self):
        """This symbolic-object''s universe of discourse. Shortcut: o.u"""
        return self._universe_of_discourse


class TheoreticalObject(SymbolicObject):
    """
    Definition
    ----------
    Given a theory 𝒯, a theoretical-object ℴ is an object that:
     * is constitutive of 𝒯,
     * may be referenced in 𝒯 formulae (i.e. 𝒯 may "talk about" ℴ),
     * that may be but is not necessarily a statement in 𝒯 (e.g. it may be an invalid or inconsistent formula).

    The following are supported classes of theoretical-objects:
    * axiom
    * formula
    * lemma
    * proposition
    * relation
    * simple-object
    * theorem
    * theory
    * variable
    """

    def __init__(
            self,
            nameset: (None, str, NameSet),
            universe_of_discourse: UniverseOfDiscourse,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            is_theory_foundation_system: bool = False,
            echo: bool = False):
        # pseudo-class properties. these must be overwritten by
        # the parent constructor after calling __init__().
        # the rationale is that checking python types fails
        # miserably (e.g. because of context managers),
        # thus, implementing explicit functional-types will prove
        # more robust and allow for duck typing.
        super().__init__(
            nameset=nameset,
            universe_of_discourse=universe_of_discourse,
            is_theory_foundation_system=is_theory_foundation_system,
            title=title,
            dashed_name=dashed_name,
            echo=False)
        super()._declare_class_membership(classes.theoretical_objct)
        if echo:
            repm.prnt(self.rep_fully_qualified_name())

    def add_to_graph(self, g):
        """Add this theoretical object as a node in the target graph g.
        Recursively add directly linked objects unless they are already present in g.
        NetworkX automatically and quietly ignores nodes and edges that are already present."""
        g.add_node(self.rep_name())
        self.u.add_to_graph(g)

    def get_variable_ordered_set(self) -> tuple:
        """Return the ordered-set of free-variables contained in ⌜self⌝,
        ordered in canonical-order (TODO: add link to doc on canonical-order).

        This function recursively traverse formula components (relation + parameters)
        to compile the set of variables contained in o.

        Internally, it uses a mutable python list, which is natively ordered,
        to proxy an ordered-set. It then returns an immutable python tuple
        for stability.
        """
        ordered_set = list()
        self._get_variable_ordered_set(ordered_set)
        # Make the ordered-set proxy immutable.
        ordered_set = tuple(ordered_set)
        return ordered_set

    def _get_variable_ordered_set(self, ordered_set=None):
        """This private method uses a mutable python list,
        which is natively ordered, to proxy an ordered-set,
        and populate the variable oredered-set during formula traversal."""
        if is_in_class(self, classes.formula_statement):
            # Unpack the formula statement to
            # retrieve the variables contained in its formula.
            self.valid_proposition._get_variable_ordered_set(ordered_set)
        if is_in_class(self, classes.formula):
            self.relation._get_variable_ordered_set(ordered_set)
            # Uses for i in range() to preserve parameter order.
            for i in range(0, len(self.parameters)):
                self.parameters[i]._get_variable_ordered_set(ordered_set)
        elif is_in_class(self, classes.free_variable):
            if self not in ordered_set:
                ordered_set.append(self)

    def is_formula_equivalent_to(self, o2):
        """Returns true if this theoretical-obct and theoretical-obct o2 are formula-equivalent.

        Parameters:
        -----------
        o2 : TheoreticalObject
            The theoretical-object with which to verify formula-equivalence.

        Definition:
        -----------
        Two theoretical-obcts o1 and o₂ that are not both formulae,
        are formula-equivalent if and only if:
        Necessary conditions:
         1. o1 and o₂ are symbolic-equivalent.
        Unnecessary but valid conditions:
         2. o1 and o₂ are of the same theory class (simple-objct, relation, etc.)
         3. o1 and o₂ are constitutive of symbolic-equivalent theories.
         4. o1 and o₂ have equal defining-properties (e.g. arity for a relation).

        For the special case when o1 and o₂ are both formulae,
        cf. the overridden method Formula.is_formula_equivalent_to.

        Note:
        -----
        o1 and o₂ may be subject to identical theoretical constraints,
        that is to say they are theoretically-equivalent,
        but if they are defined with distinct symbols, they are not formula-equivalent.
        """
        return self.is_symbol_equivalent(o2)

    def is_masked_formula_similar_to(
            self,
            o2: (Formula, FormulaStatement, FreeVariable, Relation, SimpleObjct, TheoreticalObject),
            mask: (None, frozenset[FreeVariable]) = None) \
            -> bool:
        """Given two theoretical-objects o₁ (self) and o₂,
        and a finite set of variables 𝐌,
        return True if o₁ and o₂ are masked-formula-similar, False otherwise.

        Definition
        ----------
        Given two theoretical-objects o₁ (self) and o₂,
        and a finite set of variables 𝐌,
        o₁ and o₂ are masked-formula-similar if and only if:
         1. o₁ is formula-equivalent to o₂, including the special case
            when both o₁ and o₂ are symbolic-equivalent to a variable 𝐱 in 𝐌,
         2. or the weaker condition that strictly one theoretical-object o₁ or o₂
            is symbolic-equivalent to a variable 𝐱 in 𝐌,
            and, denoting the other object the variable-observed-value,
            every variable-observed-value of 𝐱 are formula-equivalent.
         3. or, if o₁ or o₂ are both formula, their components are masked-formula-similar.

        Note
        ----
        masked-formula-similitude is not a well-defined equivalence-class.
        In effect, equivalence-classes are reflexive, symmetric, and transitive.
        An obvious counterexample: (x + 1) ~ (5 + x).
        This is why it is called similitude and not equivalence.

        Parameters
        ----------
        o2 : TheoreticalObject
            A theoretical-object with which to verify masked-formula-similitude.

        mask: set
            Set of FreeVariable elements. If None, the empty set is assumed.

        """
        output, _values = self._is_masked_formula_similar_to(o2=o2, mask=mask)
        return output

    def _is_masked_formula_similar_to(
            self,
            o2: (Formula, FormulaStatement, FreeVariable, Relation, SimpleObjct, TheoreticalObject),
            mask: (None, frozenset[FreeVariable]) = None,
            _values: (None, dict) = None) \
            -> (bool, dict):
        """A "private" version of the is_masked_formula_similar_to method,
        with the "internal" parameter _values.

        Parameters
        ----------
        o2 : TheoreticalObject
            A theoretical-object with which to verify masked-formula-similitude.

        mask: set
            Set of FreeVariable elements. If None, the empty set is assumed.

        _values:
            Internal dict of FreeVariable values used to keep track
            of variable values consistency.
        """
        o1 = self
        # if is_in_class(o1, classes.formula_statement):
        #    # Unpack the formula-statement
        #    # to compare the formula it contains.
        #    o1 = o1.valid_proposition
        # if is_in_class(o2, classes.formula_statement):
        #    # Unpack the formula-statement
        #    # to compare the formula it contains.
        #    o2 = o2.valid_proposition
        mask = frozenset() if mask is None else mask
        _values = dict() if _values is None else _values
        if o1 is o2:
            # Trivial case.
            return True, _values
        if o1.is_formula_equivalent_to(o2):
            # Sufficient condition.
            return True, _values
        if isinstance(o1, (Formula, FormulaStatement)) and isinstance(o2,
                                                                      (Formula, FormulaStatement)):
            # When both o1 and o2 are formula,
            # verify that their components are masked-formula-similar.
            relation_output, _values = o1.relation._is_masked_formula_similar_to(
                o2=o2.relation, mask=mask, _values=_values)
            if not relation_output:
                return False, _values
            # Arities are necessarily equal.
            for i in range(len(o1.parameters)):
                parameter_output, _values = o1.parameters[
                    i]._is_masked_formula_similar_to(
                    o2=o2.parameters[i], mask=mask, _values=_values)
                if not parameter_output:
                    return False, _values
            return True, _values
        if o1 not in mask and o2 not in mask:
            # We know o1 and o2 are not formula-equivalent,
            # and we know they are not in the mask.
            return False, _values
        if o1 in mask:
            variable = o2
            newly_observed_value = o1
            if variable in _values:
                already_observed_value = _values[variable]
                if not newly_observed_value.is_formula_equivalent_to(
                        already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        if o2 in mask:
            variable = o1
            newly_observed_value = o2
            if variable in _values:
                already_observed_value = _values[variable]
                if not newly_observed_value.is_formula_equivalent_to(
                        already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        return True, _values

    def substitute(
            self, substitution_map, target_theory, lock_variable_scope=None):
        """Given a theoretical-objct o₁ (self),
        and a substitution map 𝐌,
        return a theoretical-objct o₂
        where all components, including o₂ itself,
        have been substituted if present in 𝐌.

        Note
        ----
        The scope of variables is locked to their most-parent formula.
        In consequence, and in order to generate valid formluae,
        substition must simultaneously substite all variables with
        new variables.

        Note
        ----
        The result of substitution depends on the order
        of traversal of o₁. The substitution() method
        uses the canonical-traversal-method which is:
        top-down, left-to-right, depth-first, relation-before-parameters.

        Parameters
        ----------
        substitution_map : dict
            A dictionary of theoretical-objct pairs (o, o'),
            where o is the original theoretical-objct in o₁,
            and o' is the substitute theoretical-objct in o₂.

        """
        lock_variable_scope = True if lock_variable_scope is None else lock_variable_scope
        substitution_map = dict() if substitution_map is None else substitution_map
        assert isinstance(substitution_map, dict)
        output = None
        for key, value in substitution_map.items():
            # FreeVariable instances may be of type contextlib._GeneratorContextManager
            # when used inside a with statement.
            pass
            # assert isinstance(key, TheoreticalObjct)  ##### XXXXX
            # verify(
            #    isinstance(value, (
            #    TheoreticalObjct, contextlib._GeneratorContextManager)),
            #    'The value component of this key/value pair in this '
            #    'substitution map is not an instance of TheoreticalObjct.',
            #    key=key, value=value, value_type=type(value), self2=self)
            # A formula relation cannot be replaced by a simple-objct.
            # But a simple-object could be replaced by a formula,
            # if that formula "yields" such simple-objects.
            # TODO: Implement clever rules here to avoid ill-formed formula,
            #   or let the formula constructor do the work.
            # assert type(key) == type(value) or isinstance(
            #    value, FreeVariable) or isinstance(
            #    key, FreeVariable)
            # If these are formula, their arity must be equal
            # to prevent the creation of an ill-formed formula.
            # NO, THIS IS WRONG. TODO: Re-analyze this point.
            # assert not isinstance(key, Formula) or key.arity == value.arity

        # Because the scope of variables is locked,
        # the substituted formula must create "duplicates" of all variables.
        variables_list = self.get_variable_ordered_set()
        for x in variables_list:
            if x not in substitution_map.keys():
                # Call declare_free_variable() instead of v()
                # to explicitly manage variables scope locking.
                x2 = self.universe_of_discourse.declare_free_variable(
                    x.nameset.nameset)
                substitution_map[x] = x2

        # Now we may proceed with substitution.
        if self in substitution_map:
            return substitution_map[self]
        elif isinstance(self, Formula):
            # If both key / value are formulae,
            #   we must check for formula-equivalence,
            #   rather than python-object-equality.
            for k, v in substitution_map.items():
                if self.is_formula_equivalent_to(k):
                    return v

            # If the formula itself is not matched,
            # the next step consist in decomposing it
            # into its constituent parts, i.e. relation and parameters,
            # to apply the substitution operation on these.
            relation = self.relation.substitute(
                substitution_map=substitution_map, target_theory=target_theory,
                lock_variable_scope=lock_variable_scope)
            parameters = tuple(
                p.substitute(
                    substitution_map=substitution_map,
                    target_theory=target_theory, lock_variable_scope=False) for
                p in
                self.parameters)
            phi = self.universe_of_discourse.f(
                relation, *parameters, lock_variable_scope=lock_variable_scope)
            return phi
        else:
            return self

    def iterate_relations(self, include_root: bool = True):
        """Iterate through this and all the theoretical-objcts it contains recursively, providing they are relations."""
        return (
            r for r in self.iterate_theoretical_objcts_references(include_root=include_root)
            if is_in_class(r, classes.relation))

    def iterate_theoretical_objcts_references(self, include_root: bool = True,
                                              visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it contains recursively."""
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})

    def contains_theoretical_objct(self, o: TheoreticalObject):
        """Return True if o is in this theory's hierarchy, False otherwise."""
        return o in self.iterate_theoretical_objcts_references(include_root=True)


def substitute_xy(o, x, y):
    """Return the result of a *substitution* of x with y on o."""
    verify(isinstance(o, TheoreticalObject), msg='o is not a TheoreticalObjct.')
    verify(isinstance(x, TheoreticalObject), msg='x is not a TheoreticalObjct.')
    verify(isinstance(y, TheoreticalObject), msg='y is not a TheoreticalObjct.')
    return o.substitute(substitution_map={x: y})


class FreeVariable(TheoreticalObject):
    """


    Defining properties:
    --------------------
    The defining-properties of a free-variable are:
     * Being a free-variable
     * The scope-formula of the free-variable
     * The index-position of the free-variable in its scope-formula
    """

    class Status(repm.ValueName):
        pass

    scope_initialization_status = Status('scope_initialization_status')
    closed_scope_status = Status('closed_scope_status')

    def __init__(
            self, nameset=None,
            universe_of_discourse=None, status=None, scope=None, echo=None):
        echo = get_config(echo, configuration.echo_free_variable_declaration,
                          configuration.echo_default,
                          fallback_value=False)
        status = FreeVariable.scope_initialization_status if status is None else status
        scope = frozenset() if scope is None else scope
        scope = {scope} if isinstance(scope, Formula) else scope
        verify(
            isinstance(scope, frozenset),
            'The scope of a FreeVariable must be of python type frozenset.')
        verify(
            isinstance(status, FreeVariable.Status),
            'The status of a FreeVariable must be of the FreeVariable.Status type.')
        self._status = status
        self._scope = scope
        assert isinstance(universe_of_discourse, UniverseOfDiscourse)
        if nameset is None:
            nameset = 'x'
        if isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            base = StyledText(nameset, text_styles.serif_bold)
            index = universe_of_discourse.index_symbol(base=base)
            nameset = NameSet(symbol=base, index=index)
        super().__init__(
            nameset=nameset,
            universe_of_discourse=universe_of_discourse, echo=False)
        # self.universe_of_discourse.cross_reference_variable(x=self)
        super()._declare_class_membership(declarative_class_list.free_variable)
        if echo:
            self.echo()

    def echo(self):
        self.rep_declaration()

    @property
    def scope(self):
        """The scope of a free variable is the set of the formula where the variable is used.

        :return:
        """
        return self._scope

    def lock_scope(self):
        # Support for the with pythonic syntax
        # Start building  variable scope
        verify(
            self._status == FreeVariable.scope_initialization_status,
            'The scope of an instance of FreeVariable can only be locked if it is open.')
        # Close variable scope
        self._status = FreeVariable.closed_scope_status

    def extend_scope(self, phi):
        # Support for the with pythonic syntax
        # Start building  variable scope
        verify(
            self._status == FreeVariable.scope_initialization_status,
            'The scope of an instance of FreeVariable can only be extended if it is open.')
        # Close variable scope
        verify(
            isinstance(phi, Formula),
            'Scope extensions of FreeVariable must be of type Formula.')
        self._scope = self._scope.union({phi})

    def is_masked_formula_similar_to(self, o2, mask, _values):
        # TODO: Re-implement this
        assert isinstance(o2, TheoreticalObject)
        if isinstance(o2, FreeVariable):
            if o2 in mask:
                # o2 is a variable, and it is present in the mask.
                # first, we must check if it is already in the dictionary of values.
                if o2 in _values:
                    # the value is already present in the dictionary.
                    known_value = _values[o2]
                    if known_value is self:
                        # the existing value matches the newly observed value.
                        # until there, masked-formula-similitude is preserved.
                        return True, _values
                    else:
                        # the existing value does not match the newly observed value.
                        # masked-formula-similitude is no longer preserved.
                        return False, _values
                else:
                    # the value is not present in the dictionary.
                    # until there, masked-formula-similitude is preserved.
                    _values[o2] = self
                    return True, _values
        if not isinstance(o2, SimpleObjct):
            # o1 (self) is a simple-objct, and o2 is something else.
            # in consequence, masked-formula-similitude is no longer preserved.
            return False, _values
        # o2 is not a variable.
        return self.is_formula_equivalent_to(o2), _values

    def rep_declaration(self, text_format: (None, TextFormat) = None):
        return f'Let {self.rep_name(text_format=text_format)} be a free-variable in {self.universe_of_discourse.rep_name(text_format=text_format)}'


class Formula(TheoreticalObject):
    """A formula is a theoretical-objct.
    It is also a tuple (U, r, p1, p1, p2, ..., pn)

    Definition
    ----------
    A formula 𝜑 is a tuple (◆, 𝒳) where:
     * ◆ is a relation.
     * 𝒳 is a finite tuple of parameters
       whose elements are theoretical-objects, possibly formulae.

    Defining properties:
    --------------------
    The defining-properties of a formula are:
     * Being a formula.
     * A relation r.
     * A finite tuple of parameters.

     To do list
     ----------
     - TODO: Question: supporting relation as subformula, where the subformula
        would be a function whose domain would be the class of relations,
        could be an interesting approach to extend the expressiveness of
        Punctilious as a formal language. Consider this in later developments.

    Attributes
    ----------
    relation : (Relation, FreeVariable)

    """

    function_call = repm.ValueName(
        'function-call')
    infix = repm.ValueName(
        'infix-operator')
    prefix = repm.ValueName(
        'prefix-operator')
    postfix = repm.ValueName(
        'postfix-operator')

    def __init__(
            self,
            relation: (Relation, FreeVariable),
            parameters: tuple,
            universe_of_discourse: UniverseOfDiscourse,
            nameset: (None, str, NameSet) = None,
            lock_variable_scope: bool = False,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """
        """
        echo = get_config(echo, configuration.echo_formula_declaration, configuration.echo_default,
                          fallback_value=False)
        self.free_variables = dict()  # TODO: Check how to make dict immutable after construction.
        # self.formula_index = theory.crossreference_formula(self)
        if nameset is None:
            symbol_base = '𝜑'
            nameset = NameSet(
                symbol=symbol_base, index=universe_of_discourse.index_symbol(
                    base=symbol_base))
        self.relation = relation
        parameters = parameters if isinstance(parameters, tuple) else tuple(
            [parameters])
        self.arity = len(parameters)
        verify(self.arity > 0,
               'The number of parameters in this formula is zero. 0-ary relations are currently not supported.')

        verify(
            is_in_class(relation, classes.free_variable) or
            self.relation.arity == self.arity,
            'The arity of this formula''s relation is inconsistent with the number of parameters in the formula.',
            relation=self.relation,
            parameters=parameters)
        self.parameters = parameters
        super().__init__(
            nameset=nameset,
            universe_of_discourse=universe_of_discourse,
            title=title,
            dashed_name=dashed_name,
            echo=False)
        super()._declare_class_membership(declarative_class_list.formula)
        universe_of_discourse.cross_reference_formula(self)
        verify(
            is_in_class(relation, classes.relation) or is_in_class(relation, classes.free_variable),
            'The relation of this formula is neither a relation, nor a '
            'free-variable.',
            formula=self, relation=relation)
        verify(
            relation.universe_of_discourse is self.universe_of_discourse,
            'The universe_of_discourse of the relation of this formula is '
            'distint from the formula unierse_of_disourse.',
            formula=self, relation=relation)
        self.cross_reference_variables()
        for p in parameters:
            verify(
                is_in_class(p, classes.theoretical_objct),
                'p is not a theoretical-objct.',
                slf=self, p=p)
            if is_in_class(p, classes.free_variable):
                p.extend_scope(self)
        if lock_variable_scope:
            self.lock_variable_scope()
        if echo:
            self.echo()

    def __repr__(self):
        return self.rep(expand=True)

    def __str__(self):
        return self.rep(expand=True)

    def crossreference_variable(self, x):
        """During construction, cross-reference a free-variable 𝓍
        with its parent formula if it is not already cross-referenced,
        and return its 0-based index in Formula.free_variables."""
        assert isinstance(x, FreeVariable)
        x.formula = self if x.formula is None else x.formula
        assert x.formula is self
        if x not in self.free_variables:
            self.free_variables = self.free_variables + tuple([x])
        return self.free_variables.index(x)

    def cross_reference_variables(self):
        # TODO: Iterate through formula filtering on variable placeholders.
        # TODO: Call cross_reference_variable on every variable placeholder.
        pass
        # assert False

    def echo(self):
        repm.prnt(self.rep_declaration())

    @property
    def is_proposition(self):
        """Tell if the formula is a logic-proposition.

        This property is directly inherited from the formula-is-proposition
        attribute of the formula's relation."""
        return self.relation.signal_proposition

    def is_formula_equivalent_to(self, o2: (TheoreticalObject, Statement, Formula)) -> bool:
        """Returns true if this formula and o2 are formula-equivalent.

        Definition:
        -----------
        A formula φ and a theoretical-object o₂ are formula-equivalent if and only if:
         1. o₂ is a formula.
         2. The relations of φ and o₂ are formula-equivalent.
         3. The parameter ordered tuples of φ and o₂ are pair-wise formula-equivalent.ᵃ

        ᵃ. See the special case of variables formula-equivalence.

        Note:
        -----
        Intuitively, formula-equivalence state that two formula express the
        same thing with the same symbols.
        For instance, formula (¬(True)) and (False) are not formula-equivalent,
        because the former expresses the negation of truth (which is equal to false),
        and the latter expresses falsehood "directly". Both formulae yield
        the same value, but are formulated in a different manned.
        It follows that two formula may yield equal values and not be formula-equivalent.
        But two formula that are formula-equivalent necessarily yield the same value.
        Finally, two formula may not be symbolically-equivalent while
        being formula-equivalent. Because formulae are theoretical-objects.
        and theoretical-objects are symbolic-objcts, formulae have unique symbols.

        To do list
        ----------
        We would not need the concept of formula-equivalence if we would
        forbid the instantiation of "duplicate" formulae in theories.
        TODO: Consider the pros and cons of forbiding "duplicate" formulae in theories
            and removing formula-equivalence as a concept from Punctilious.

        """
        # if o2 is a statement, unpack its embedded formula
        o2 = o2.valid_proposition if is_in_class(o2, classes.statement) else o2
        if self is o2:
            # Trivial case.
            return True
        if not isinstance(o2, Formula):
            return False
        if not self.relation.is_formula_equivalent_to(o2.relation):
            return False
        # Arities are necessarily equal.
        for i in range(len(self.parameters)):
            if not self.parameters[i].is_formula_equivalent_to(
                    o2.parameters[i]):
                return False
        return True

    def iterate_theoretical_objcts_references(self, include_root: bool = True,
                                              visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it contains recursively."""
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        if self.relation not in visited:
            yield self.relation
            visited.update({self.relation})
            yield from self.relation.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)
        for parameter in set(self.parameters).difference(visited):
            yield parameter
            visited.update({parameter})
            yield from parameter.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)

    def list_theoretical_objcts_recursively_OBSOLETE(self, ol: (None, frozenset) = None,
                                                     extension_limit: (None, Statement) = None):
        """Return a python frozenset of this formula and all theoretical_objcts it contains."""
        ol = frozenset() if ol is None else ol
        ol = ol.union({self})
        if self.relation not in ol:
            ol = ol.union(self.relation.list_theoretical_objcts_recursively_OBSOLETE(ol=ol))
        for p in self.parameters:
            if p not in ol:
                ol = ol.union(p.list_theoretical_objcts_recursively_OBSOLETE(ol=ol))
        return ol

    def lock_variable_scope(self):
        """Variable scope must be locked when the formula construction
        is completed."""
        variables_list = self.get_variable_ordered_set()
        for x in variables_list:
            x.lock_scope()

    def rep(self, text_format: (None, TextFormat) = None, expand: (None, bool) = None) -> str:
        expand = True if expand is None else expand
        assert isinstance(expand, bool)
        if expand:
            return self.rep_formula(text_format=text_format, expand=expand)
        else:
            return super().rep(text_format=text_format, expand=expand)

    def rep_as_function_call(self, text_format: (None, TextFormat) = None,
                             expand: (None, bool) = None) -> str:
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        expand = True if expand is None else expand
        assert isinstance(expand, bool)
        return f'{self.relation.rep_formula(text_format=text_format)}({", ".join([p.rep_formula(text_format=text_format) for p in self.parameters])})'

    def rep_as_infix_operator(self, text_format: (None, TextFormat) = None,
                              expand=(None, bool)) -> str:
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        expand = True if expand is None else expand
        assert self.relation.arity == 2
        return f'({self.parameters[0].rep(text_format=text_format, expand=expand)} {self.relation.rep_name(text_format=text_format)} {self.parameters[1].rep(text_format=text_format, expand=expand)})'

    def rep_as_postfix_operator(self, text_format: (None, TextFormat) = None, expand=None) -> str:
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        expand = True if expand is None else expand
        assert isinstance(expand, bool)
        assert self.relation.arity == 1
        return f'({self.parameters[0].rep(text_format=text_format, expand=expand)}){self.relation.rep_name(text_format=text_format)}'

    def rep_as_prefix_operator(self, text_format: (None, TextFormat) = None, expand=None) -> str:
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        expand = True if expand is None else expand
        verify(
            isinstance(expand, bool),
            'Method parameter "expand" is not an instance of bool.',
            self=self, expand=expand)
        verify(
            self.relation.arity == 1,
            'Attempt to represent prefix operator, but relation arity is not equal to 1.',
            self_relation=self.relation,
            parameters=self.parameters)
        return f'{self.relation.rep_formula(text_format=text_format)}({self.parameters[0].rep_formula(text_format=text_format, expand=expand)})'

    def rep_formula(self, text_format: (None, TextFormat) = None, expand: bool = True) -> str:
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        if is_in_class(self.relation, classes.free_variable):
            # If the relation of this formula is a free-variable,
            # it has no arity, neither a representation-mode.
            # In this situation, our design-choice is to
            # fallback on the function-call representation-mode.
            # In future developments, we may choose to allow
            # the "decoration" of free-variables with arity,
            # and presentation-mode to improve readability.
            return self.rep_as_function_call(text_format=text_format, expand=expand)
        else:
            match self.relation.formula_rep:
                case Formula.function_call:
                    return self.rep_as_function_call(text_format=text_format, expand=expand)
                case Formula.infix:
                    return self.rep_as_infix_operator(text_format=text_format, expand=expand)
                case Formula.prefix:
                    return self.rep_as_prefix_operator(text_format=text_format, expand=expand)
                case Formula.postfix:
                    return self.rep_as_postfix_operator(text_format=text_format, expand=expand)
                case _:
                    # Fallback notation.
                    return self.rep_as_function_call(text_format=text_format, expand=expand)

    def rep_declaration(self):
        return f'Let {self.rep_name()} be the formula {self.rep_formula(expand=True)} in {self.universe_of_discourse.rep_name()}.'


class SimpleObjctDict(collections.UserDict):
    """A dictionary that exposes well-known simple-objcts as properties.

    """

    def __init__(self, u: UniverseOfDiscourse):
        self.u = u
        super().__init__()
        # Well-known objects
        self._falsehood = None
        self._truth = None

    def declare(self,
                nameset: (None, str, NameSet) = None,
                dashed_name: (None, str, DashedName) = None,
                echo: (None, bool) = None) -> SimpleObjct:
        """Declare a new simple-objct in this universe-of-discourse.
        """
        return SimpleObjct(
            nameset=nameset,
            dashed_name=dashed_name,
            universe_of_discourse=self.u,
            echo=echo)

    @property
    def fals(self):
        """The well-known falsehood simple-objct.

        Unabridged property: universe_of_discourse.simple_objcts.falsehood

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.falsehood

    @property
    def falsehood(self):
        """The well-known falsehood simple-objct.

        Abridged property: u.o.fals

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._falsehood is None:
            self._falsehood = self.declare(
                nameset=NameSet(
                    symbol=StyledText(unicode='⊥', latex_math='\\bot'),
                    name=StyledText(plaintext='false'),
                    explicit_name=StyledText(plaintext='falsehood'),
                    index=None))
        return self._falsehood

    @property
    def tru(self):
        """The well-known truth simple-objct.

        Unabridged property: universe_of_discourse.simple_objcts.truth

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.truth

    @property
    def truth(self):
        """The well-known truth simple-objct.

        Abridged property: u.o.tru

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._truth is None:
            self._truth = self.declare(nameset=
            NameSet(
                symbol=StyledText(unicode='⊤', latex_math='\\top'),
                name=StyledText(plaintext='true'),
                explicit_name=StyledText(plaintext='truth'),
                index=None))
        return self._truth


class TitleCategory(repm.ValueName):
    def __init__(self, name, symbol_base, natural_name, abridged_name):
        self.symbol_base = symbol_base
        self.natural_name = natural_name
        self.abridged_name = abridged_name
        super().__init__(name)

    def __repr__(self):
        return self.rep(text_format=text_formats.plaintext)

    def __str__(self):
        return self.rep(text_format=text_formats.plaintext)

    def rep(self, text_format: (None, TextFormat) = None, cap: (None, bool) = None,
            expand: (None, bool) = None):
        # TODO: Implement text_format
        return self.natural_name


class TitleCategories(repm.ValueName):
    # axiom = TitleCategory('axiom', 's', 'axiom', 'axiom')
    axiom_declaration = TitleCategory('axiom_declaration', 's', 'axiom declaration', 'axiom decl.')
    axiom_inclusion = TitleCategory('axiom_inclusion', 's', 'axiom', 'axiom')
    corollary = TitleCategory('corollary', 's', 'corollary', 'cor.')
    definition = TitleCategory('definition', 's', 'definition', 'def.')
    definition_declaration = TitleCategory('definition_declaration', 's', 'definition declaration',
                                           'definition decl.')
    definition_inclusion = TitleCategory('definition_inclusion', 's', 'definition', 'definition')
    formal_definition = TitleCategory('formal_definition', 's', 'formal definition', 'def.')
    hypothesis = TitleCategory('hypothesis', 's', 'hypothesis', 'hyp.')
    inference_rule = TitleCategory('inference_rule', 's', 'inference rule', 'inference rule')
    inference_rule_inclusion = TitleCategory('inference_rule_inclusion', 's',
                                             'inference rule inclusion', 'i.-r.')
    inferred_proposition = ('inferred_proposition', 's', 'inferred-proposition')
    lemma = TitleCategory('lemma', 's', 'lemma', 'lem.')
    proposition = TitleCategory('proposition', 's', 'proposition', 'prop.')
    theorem = TitleCategory('theorem', 's', 'theorem', 'thrm.')
    theory_elaboration_sequence = TitleCategory('theory_elaboration_sequence', 't',
                                                'theory elaboration sequence',
                                                'theo.')
    comment = TitleCategory('comment', 's', 'comment', 'cmt.')
    note = TitleCategory('note', 's', 'note', 'note')
    remark = TitleCategory('remark', 's', 'remark', 'rmrk.')
    # Special categories
    uncategorized = TitleCategory('uncategorized', 's', 'uncategorized', 'uncat.')


title_categories = TitleCategories('title_categories')


class Statement(TheoreticalObject):
    """

    Definition
    ----------
    Given a theory 𝒯, a statement 𝒮 is a theoretical-object that:
     * announces some truth in 𝒯.

    There are three broad categories of statements:
    - contentual-statements (e.g. axiom-inclusion, definition-inclusion)
    - formula-statements
    - non-theoretical statements (decorative)

    For 𝒯 to be valid, all statements in 𝒯 must be valid.
    For 𝒯 to be consistent, all statements in 𝒯 must be consistent.
    etc.
    """

    def __init__(
            self,
            theory: TheoryElaborationSequence,
            category: TitleCategory,
            nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: bool = False):
        self._theory = theory
        echo = get_config(echo, configuration.echo_statement, configuration.echo_default,
                          fallback_value=False)
        universe_of_discourse = theory.universe_of_discourse
        self.statement_index = theory.crossreference_statement(self)
        self._category = category
        super().__init__(
            nameset=nameset,
            universe_of_discourse=universe_of_discourse,
            title=title,
            dashed_name=dashed_name,
            echo=False)
        super()._declare_class_membership(declarative_class_list.statement)
        if echo:
            self.echo()

    @property
    def category(self) -> TitleCategory:
        """The statement-category assigned to this statement.

        :return:
        """
        return self._category

    def echo(self):
        repm.prnt(self.rep_report())

    @abc.abstractmethod
    def rep_report(self):
        raise NotImplementedError('This is an abstract method.')

    @property
    def t(self) -> TheoryElaborationSequence:
        """The theory-elaboration-sequence that contains this statement.

        Unabridged property: statement.theory"""
        return self.theory

    @property
    def theory(self) -> TheoryElaborationSequence:
        """The theory-elaboration-sequence that contains this statement.

        Abridged property: s.t

        This property may only be set once. In effect, moving statements
        between theories would lead to unstable theories."""
        return self._theory

    @theory.setter
    def theory(self, t: TheoryElaborationSequence):
        verify(self._theory is None,
               '⌜theory⌝ property may only be set once.',
               slf=self, slf_theory=self._theory, t=t)
        self._theory = t

    @property
    def u(self) -> UniverseOfDiscourse:
        """The universe-of-discourse where this statement is declared.

        Unabridged property: statement.universe_of_discourse"""
        return self.universe_of_discourse

    @property
    def universe_of_discourse(self) -> UniverseOfDiscourse:
        """The universe-of-discourse where this statement is declared.

        Abridged property: s.u"""
        return self._universe_of_discourse


class AxiomDeclaration(TheoreticalObject):
    """The Axiom pythonic class models the elaboration of a _contentual_ _axiom_ in a _universe-of-discourse_.

    """

    def __init__(
            self,
            natural_language: str,
            u: UniverseOfDiscourse,
            nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            auto_index: (None, bool) = None,
            echo: (None, bool) = None):
        """

        :param natural_language: The axiom's content in natural-language.
        :param u: The universe-of-discourse.
        :param nameset:
        :param echo:
        """
        auto_index = get_config(auto_index, configuration.auto_index, fallback_value=False)
        echo = get_config(echo, configuration.echo_axiom_declaration, configuration.echo_default,
                          fallback_value=False)
        natural_language = natural_language.strip()
        verify(natural_language != '',
               'Parameter natural-language is an empty string (after trimming).')
        self.natural_language = natural_language
        if title is None:
            # Long-names are not a mandatory attribute,
            # it is available to improve readability in reports.
            title = Title(cat=title_categories.axiom_declaration)
        elif isinstance(title, str):
            title = Title(ref=title, cat=title_categories.axiom_declaration, subtitle=None)
        if isinstance(title, Title) and (
                title.cat is not title_categories.axiom_declaration or title.cat is None):
            title = Title(ref=title.ref, cat=title_categories.axiom_declaration,
                          subtitle=title.subtitle)
        # warnings.warn('A new long-name was generated to force its category property to: axiom.')
        super().__init__(
            universe_of_discourse=u, nameset=nameset, echo=False, title=title)
        super()._declare_class_membership(declarative_class_list.axiom)
        u.cross_reference_axiom(self)
        if echo:
            repm.prnt(self.rep_report())

    def rep_report(self, text_format: (None, TextFormat) = None, output_proofs: (None, bool) = True,
                   wrap: (None, bool) = True):
        """Return a representation that expresses and justifies the statement."""
        # TODO: Implement text_format.
        text = f'{self.title.rep_title(text_format=text_format, cap=True)} ({self.rep_name()}): “{self.natural_language}”.'
        if wrap:
            text = '\n'.join(textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))
        return text


class AxiomInclusion(Statement):
    """An axiom-inclusion (aka axiom-postulation) is defined as a pair (𝑡,𝑎),
    where 𝑡 is a theory-elaboration-sequence and 𝑎 is a contentual axiom.
    """

    def __init__(
            self,
            a: AxiomDeclaration,
            t: TheoryElaborationSequence,
            nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Include (postulate) an axiom in a theory-elaboration-sequence.
        """
        echo = get_config(echo, configuration.echo_axiom_inclusion, configuration.echo_default,
                          fallback_value=False)
        self._axiom = a
        if title is None:
            title = Title(cat=title_categories.axiom_inclusion)
        if isinstance(title, str):
            title = Title(
                ref=title,
                cat=title_categories.axiom_inclusion,
                subtitle=None
            )
        super().__init__(
            theory=t,
            category=title_categories.axiom_inclusion,
            nameset=nameset,
            title=title,
            dashed_name=dashed_name,
            echo=False)
        t.crossreference_axiom_inclusion(self)
        super()._declare_class_membership(declarative_class_list.axiom_inclusion)
        if echo:
            repm.prnt(self.rep_report())

    @property
    def a(self) -> AxiomDeclaration:
        """The axiom of an axiom-inclusion.

        Unabridged property: axiom_inclusion.axiom"""
        return self.axiom

    @property
    def axiom(self) -> AxiomDeclaration:
        """The axiom of an axiom-inclusion.

        Abridged property: a.a"""
        return self._axiom

    def rep_report(self, output_proofs: bool = True) -> str:
        """Return a representation that expresses and justifies the statement."""
        text = f'{self.rep_title(cap=True)}: “{self.axiom.natural_language}”'
        text = repm.wrap(text)
        if output_proofs:
            text2 = f'Let postulate {self.axiom.rep_fully_qualified_name()} in {self.theory.rep_reference()}.'
            text2 = repm.wrap(text2)
            text = text + '\n' + text2
        return text


class InferenceRuleInclusion(Statement):
    """An inference-rule inclusion (aka inference-rule allowance) in the current theory-elaboration.
    """

    def __init__(
            self,
            i: InferenceRuleDeclaration,
            t: TheoryElaborationSequence,
            nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Include (aka allow) an inference-rule in a theory-elaboration.
        """
        self._inference_rule = i
        if nameset is None:
            # If no symbol is passed as a parameter,
            # automated assignment of symbol is assumed.
            base = 's'
            index = t.universe_of_discourse.index_symbol(base=base)
            nameset = NameSet(s=base, index=index)
        if title is None:
            title = Title(ref=str(nameset.index), cat=title_categories.inference_rule_inclusion,
                          subtitle=None)
        if isinstance(title, str):
            title = Title(ref=title, cat=title_categories.inference_rule_inclusion,
                          subtitle=None)
        super().__init__(
            theory=t,
            category=title_categories.inference_rule_inclusion,
            nameset=nameset,
            title=title,
            dashed_name=dashed_name,
            echo=False)
        t.crossreference_inference_rule_inclusion(self)
        super()._declare_class_membership(declarative_class_list.inference_rule_inclusion)
        if echo:
            repm.prnt(self.rep_report())

    def infer_formula(self, *args, echo: (None, bool) = None):
        """

        :param args:
        :param echo:
        :return:
        """
        return self.inference_rule.infer_formula(*args, t=self.theory, echo=echo)

    def infer_statement(self,
                        *args,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        cat: (None, TitleCategory) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None):
        """

        :param args:
        :param echo:
        :return:
        """
        return self.inference_rule.infer_statement(*args, t=self.theory, nameset=nameset,
                                                   ref=ref, cat=cat, subtitle=subtitle, echo=echo)

    def verify_args(self, *args):
        """

        :param args:
        :return:
        """
        return self.inference_rule.verify_args(*args, t=self.theory)

    @property
    def i(self):
        """

        :return:
        """
        return self.inference_rule

    @property
    def inference_rule(self):
        return self._inference_rule

    def verify_compatibility(self, *args):
        return self.inference_rule.verify_args(*args, t=self.theory)

    def rep_report(self, output_proofs=True) -> str:
        """Return a representation that expresses and justifies the statement."""
        text = f'Let allow the {repm.serif_bold(self.inference_rule.title.reference)} inference-rule in {self.theory.rep_reference()}.'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))


class DefinitionDeclaration(TheoreticalObject):
    """The Definition pythonic class models the elaboration of a _contentual_ _definition_ in a _universe-of-discourse_.

    """

    def __init__(
            self,
            natural_language: str,
            u: UniverseOfDiscourse,
            auto_index=None,
            nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """

        :param natural_language: The definition's content in natural-language.
        :param u: The universe-of-discourse.
        :param nameset:
        :param echo:
        """
        auto_index = get_config(auto_index, configuration.auto_index, fallback_value=False)
        echo = get_config(echo, configuration.echo_definition_declaration,
                          configuration.echo_default,
                          fallback_value=False)
        natural_language = natural_language.strip()
        verify(natural_language != '',
               'Parameter natural-language is an empty string (after trimming).')
        self.natural_language = natural_language
        if title is None:
            # Long-names are not a mandatory attribute,
            # it is available to improve readability in reports.
            title = Title(cat=title_categories.definition_declaration)
        elif isinstance(title, str):
            title = Title(ref=title, cat=title_categories.definition_declaration, subtitle=None)
        if isinstance(title, Title) and (
                title.cat is not title_categories.definition_declaration or title.cat is None):
            title = Title(ref=title.ref, cat=title_categories.definition_declaration,
                          subtitle=title.subtitle)
        super().__init__(
            universe_of_discourse=u, nameset=nameset, title=title, dashed_name=dashed_name,
            echo=echo)
        super()._declare_class_membership(declarative_class_list.definition)
        u.cross_reference_definition(self)
        if echo:
            repm.prnt(self.rep_report())

    def rep_report(self, output_proofs=True, wrap: bool = True):
        """Return a representation that expresses and justifies the statement."""
        algebraic_name = '' if self.title is None else f' ({self.rep_name()})'
        text = f'{repm.serif_bold(self.rep_title(cap=True))}{algebraic_name}: “{self.natural_language}”'
        if wrap:
            text = '\n'.join(textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))
        return text


class DefinitionInclusion(Statement):
    """A definition-endorsement in the current theory-elaboration.
    """

    def __init__(
            self,
            d: DefinitionDeclaration,
            t: TheoryElaborationSequence,
            nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Endorsement (aka include, endorse) an definition in a theory-elaboration.
        """
        echo = get_config(echo, configuration.echo_definition_inclusion, configuration.echo_default,
                          fallback_value=False)
        self.definition = d
        t.crossreference_definition_endorsement(self)
        super().__init__(
            theory=t,
            category=title_categories.definition,
            nameset=nameset,
            title=title,
            dashed_name=dashed_name,
            echo=False)
        super()._declare_class_membership(declarative_class_list.definition_inclusion)
        if echo:
            repm.prnt(self.rep_report())

    def rep_report(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement."""
        text = f'{self.rep_title(cap=True)}: “{self.definition.natural_language}”'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))


class FormulaStatement(Statement):
    """

    Definition:
    -----------
    An formula-statement is a statement that expresses the validity of a formula in the parent theory.

    To do list
    ----------
    - TODO: Make FormulaStatement an abstract class

    """

    def __init__(
            self, theory: TheoryElaborationSequence, valid_proposition: Formula,
            nameset: (None, NameSet) = None, category: (None, TitleCategory) = None,
            title: (None, Title) = None, dashed_name: (None, DashedName) = None,
            echo=None):
        echo = get_config(echo, configuration.echo_statement, configuration.echo_default,
                          fallback_value=False)
        verify(
            theory.universe_of_discourse is valid_proposition.universe_of_discourse,
            'The universe-of-discourse of this formula-statement''s theory-elaboration is '
            'inconsistent with the universe-of-discourse of the valid-proposition of that formula-statement.')
        universe_of_discourse = theory.universe_of_discourse
        # Theory statements must be logical propositions.
        valid_proposition = unpack_formula(valid_proposition)
        verify(
            valid_proposition.is_proposition,
            'The formula of this statement is not propositional.')
        # TODO: Check that all components of the hypothetical-proposition
        #  are elements of the source theory-branch.
        self.valid_proposition = valid_proposition
        self.statement_index = theory.crossreference_statement(self)
        category = title_categories.proposition if category is None else category
        super().__init__(
            theory=theory, nameset=nameset, category=category,
            title=title, dashed_name=dashed_name,
            echo=False)
        # manage theoretical-morphisms
        self.morphism_output = None
        if self.valid_proposition.relation.signal_theoretical_morphism:
            # this formula-statement is a theoretical-morphism.
            # it follows that this statement "yields" new statements in the theory.
            assert self.valid_proposition.relation.implementation is not None
            self.morphism_output = Morphism(
                theory=theory, source_statement=self)
        super()._declare_class_membership(declarative_class_list.formula_statement)
        if echo:
            self.echo()

    def __repr__(self):
        return self.rep(expand=True)

    def __str__(self):
        return self.rep(expand=True)

    @property
    def parameters(self):
        """The parameters of a formula-statement
        are the parameters of the valid-proposition-formula it contains."""
        return self.valid_proposition.parameters

    @property
    def relation(self):
        """The relation of a formula-statement
        is the relation of the valid-proposition-formula it contains."""
        return self.valid_proposition.relation

    def is_formula_equivalent_to(self, o2):
        """Considering this formula-statement as a formula,
        that is the valid-proposition-formula it contains,
        check if it is formula-equivalent to o2."""
        return self.valid_proposition.is_formula_equivalent_to(o2)

    def iterate_theoretical_objcts_references(self, include_root: bool = True,
                                              visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it contains recursively."""
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        if self.valid_proposition not in visited:
            yield self.valid_proposition
            visited.update({self.valid_proposition})
            yield from self.valid_proposition.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)

    def list_theoretical_objcts_recursively_OBSOLETE(self, ol: (None, frozenset) = None,
                                                     extension_limit: (None, Statement) = None):
        """Return a python frozenset containing this formula-statement,
         and all theoretical_objcts it contains. If a statement-limit is provided,
         does not yield statements whose index is greater than the theoretical-objct."""
        ol = frozenset() if ol is None else ol
        if extension_limit is not None and \
                extension_limit.theory == self.theory and \
                extension_limit.statement_index >= self.statement_index:
            ol = ol.union({self})
            if self.valid_proposition not in ol:
                ol = ol.union(
                    self.valid_proposition.list_theoretical_objcts_recursively_OBSOLETE(ol=ol,
                                                                                        extension_limit=extension_limit))
        return ol

    def rep(self, text_format: (None, TextFormat) = None, expand: (None, bool) = None):
        if expand:
            return self.rep_formula(text_format=text_format, expand=expand)
        else:
            return super().rep(text_format=text_format, expand=expand)

    def rep_formula(self, text_format: (None, TextFormat) = None, expand: (None, bool) = None):
        return f'{self.valid_proposition.rep_formula(text_format=text_format, expand=expand)}'


class Morphism(FormulaStatement):
    """

    Definition:
    -----------
    A theoretical-morphism-statement, or morphism for short, aka syntactic-operation is a valid-proposition produced by a valid-morphism-formula.

    """

    def __init__(
            self, source_statement, nameset=None, theory=None,
            category=None):
        assert isinstance(theory, TheoryElaborationSequence)
        assert isinstance(source_statement, FormulaStatement)
        assert theory.contains_theoretical_objct(source_statement)
        self.source_statement = source_statement
        assert source_statement.valid_proposition.relation.signal_theoretical_morphism
        self.morphism_implementation = source_statement.valid_proposition.relation.implementation
        valid_proposition = self.morphism_implementation(
            self.source_statement.valid_proposition)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            nameset=nameset, category=category)

    def rep_report(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{repm.serif_bold(self.rep_name())}: {self.valid_proposition.rep_formula(expand=True)}'
        if output_proofs:
            output = output + self.rep_subreport()
        return output

    def rep_subreport(self):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'\n\t{repm.serif_bold("Derivation by theoretical-morphism / syntactic-operation")}'
        output = output + f'\n\t{self.source_statement.valid_proposition.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.source_statement.rep_name())}.'
        output = output + f'\n\t{self.valid_proposition.rep_formula(expand=True):<70} │ Output of {repm.serif_bold(self.source_statement.valid_proposition.relation.rep_name())} morphism.'
        return output


class PropositionStatement:
    """
    Definition
    ----------
    A proposition-statement 𝒮 is a tuple (𝒯, n, 𝜑, 𝒫) where:
    * 𝒯 is a theory
    * n is a natural number representing the unique position of 𝒮 in 𝒯
    * 𝜑 is a valid-formula in 𝒯 of the form ⟨◆, 𝒯, 𝜓⟩ where:
        * ◆ is a theoretical-relation
        * 𝜓 is a free-formula
    * 𝒫 is a proof of 𝜑's validity in 𝒯 solely based on predecessors of 𝒮
    """

    def __init__(self, theory, position, phi, proof):
        assert isinstance(theory, TheoryElaborationSequence)
        assert isinstance(position, int) and position > 0
        assert isinstance(phi, Formula)
        assert theory.contains_theoretical_objct(phi)
        assert isinstance(proof, Proof)
        assert theory.contains_theoretical_objct(proof)
        self.theory = theory
        self.position = position
        self.phi = phi
        self.proof = proof


class DirectDefinitionInference(FormulaStatement):
    """

    Definition:
    A theoretical-statement that states that x = some other theoretical-object.
    When an object is defined like this, it means that for every formula
    where x is present, the same formula with the substitution of x by x' can be substituted in all theories.
    TODO: QUESTION: Should we create a base "Alias" object that is distinct from simple-objct???
    XXXXXXX
    """

    def __init__(
            self,
            p: Formula,
            d: DefinitionInclusion,
            t: TheoryElaborationSequence,
            nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        echo = get_config(echo, configuration.echo_definition_direct_inference,
                          configuration.echo_default,
                          fallback_value=False)
        verify(
            t.contains_theoretical_objct(d),
            'The definition-endorsement ⌜d⌝ must be contained '
            'in the hierarchy of theory-elaboration ⌜t⌝.',
            d=d, t=t)
        verify(
            p.universe_of_discourse is t.universe_of_discourse,
            'The universe-of-discourse of the valid-proposition ⌜p⌝ must be '
            'consistent with the universe-of-discourse of theory-elaboration ⌜t⌝.',
            p=p, t=t)
        verify(
            p.relation is t.universe_of_discourse.r.equality,
            'The root relation of the valid-proposition ⌜p⌝ must be '
            'the well-known equality-relation ⌜=⌝ in the universe-of-discourse.',
            p=p, p_relation=p.relation)
        self.definition = d
        super().__init__(
            theory=t, valid_proposition=p,
            nameset=nameset, category=title_categories.formal_definition,
            title=title, dashed_name=dashed_name, echo=False)
        assert d.statement_index < self.statement_index
        super()._declare_class_membership(declarative_class_list.direct_definition_inference)
        if echo:
            repm.prnt(self.rep_report())

    def rep_report(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.rep_title(cap=True)}: {self.valid_proposition.rep_formula(expand=True)}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Derivation from natural language definition")}'
            output = output + f'\n\t{self.valid_proposition.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.definition.rep_name())}.'
        return output


universe_of_discourse_symbol_indexes = dict()


def index_universe_of_discourse_symbol(base):
    """Given a symbol-base S (i.e. an unindexed symbol), returns a unique integer n
    such that (S, n) is a unique identifier for this UniverseOfDiscourse.

    :param base: The symbol-base.
    :return:
    """
    global universe_of_discourse_symbol_indexes
    if base not in universe_of_discourse_symbol_indexes:
        universe_of_discourse_symbol_indexes[base] = 1
    else:
        universe_of_discourse_symbol_indexes[base] += 1
    return universe_of_discourse_symbol_indexes[base]


class InferenceRuleOBSOLETE:
    """
    TODO: Complete the implementation of InferenceRule, and make ModusPonens a subclass of it.
    TODO: Make InferenceRule itself a Formula with the Sequent operator ⊢.

    Attributes:
    -----------
        premises : tuple
            A tuple of formulae.
        conclusion: Formula
            The conclusion to be derived from the premises if they are true.
    """

    def __init__(self, premises, conclusion):
        self._premises = premises
        self._conclusion = conclusion

    @staticmethod
    def infer(*args, **kwargs):
        pass


class InferenceRuleDeclaration(TheoreticalObject):
    """An inference-rule object.

    If an inference-rule is allowed / included in a theory-elaboration,
    it allows to take a sequences of premise statements P1, P2, P3, ...
    of certain shapes,
    and infer a new statement C."""

    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 infer_formula: collections.abc.Callable,
                 verify_args: collections.abc.Callable,
                 nameset: (None, str, NameSet) = None,
                 title: (None, str, Title) = None,
                 dashed_name: (None, str, DashedName) = None, echo: (None, bool) = None):
        self._infer_formula = infer_formula
        self._verify_args = verify_args
        if nameset is None:
            # If no symbol is passed as a parameter,
            # automated assignment of symbol is assumed.
            symbol = 's'  # The general symbol base for statements.
            index = universe_of_discourse.index_symbol(base=symbol)
            nameset = NameSet(symbol=symbol, index=index)
        if title is None:
            title = Title(ref=str(nameset.index), cat=title_categories.inference_rule,
                          subtitle=None)
        if isinstance(title, str):
            title = Title(ref=title, cat=title_categories.inference_rule,
                          subtitle=None)
        super().__init__(universe_of_discourse=universe_of_discourse,
                         is_theory_foundation_system=False,
                         nameset=nameset, title=title, dashed_name=dashed_name, echo=False)
        super()._declare_class_membership(declarative_class_list.inference_rule)
        universe_of_discourse.cross_reference_inference_rule(self)
        if echo:
            self.echo()

    def echo(self):
        repm.prnt(self.rep_report())

    def infer_formula(self, *args, t: TheoryElaborationSequence, echo: (None, bool) = None,
                      **kwargs) -> Formula:
        """Apply this inference-rules on input statements and return the resulting statement."""
        phi = self._infer_formula(*args, t=t, **kwargs)
        if echo:
            repm.prnt(phi.rep_report())
        return phi

    def infer_statement(
            self,
            *args,
            t: TheoryElaborationSequence,
            nameset: (None, str, NameSet) = None,
            ref: (None, str) = None,
            cat: (None, TitleCategory) = None,
            subtitle: (None, str) = None,
            echo: (None, bool) = None, **kwargs) -> InferredStatement:
        """Apply this inference-rules on input statements and return the resulting statement."""
        return InferredStatement(*args, i=self, t=t, nameset=nameset, ref=ref, cat=cat,
                                 subtitle=subtitle,
                                 echo=echo,
                                 **kwargs)

    def verify_args(self, *args, t: TheoryElaborationSequence):
        """Verify the syntactical-compatibility of input statements and return True
        if they are compatible, False otherwise."""
        return self._verify_args(*args, t=t)


class AtheoreticalStatement(SymbolicObject):
    """
    Definition
    ----------
    An atheoretical-statement is a statement that is contained in a theory report
    for commentary / explanatory purposes, but that is not mathematically constitutive
    of the theory. Atheoretical-statements may be added and/or removed from a
    theory without any impact to the theory sequence of proofs.

    """

    def __init__(self, theory: TheoryElaborationSequence, nameset: (None, str, NameSet) = None,
                 title: (None, str, Title) = None, echo: (None, bool) = None):
        assert isinstance(theory, TheoryElaborationSequence)
        self.theory = theory
        super().__init__(universe_of_discourse=theory.universe_of_discourse, nameset=nameset,
                         title=title,
                         echo=echo)
        super()._declare_class_membership(classes.atheoretical_statement)


class Note(AtheoreticalStatement):
    """The Note pythonic-class models a note, comment, or remark in a theory.

    """

    def __init__(
            self, theory: TheoryElaborationSequence, content: str,
            nameset: (None, str, NameSet) = None,
            cat: (None, TitleCategory) = None, ref: (None, str) = None,
            subtitle: (None, str) = None,
            echo: (None, bool) = None):
        echo = get_config(echo, configuration.echo_note, configuration.echo_default,
                          fallback_value=False)
        verify(is_in_class(theory, classes.t),
               'theory is not a member of declarative-class theory.', theory=theory,
               slf=self)
        universe_of_discourse = theory.universe_of_discourse
        cat = title_categories.note if cat is None else cat
        self.statement_index = theory.crossreference_statement(self)
        self.theory = theory
        self.natural_language = content
        self.category = cat
        if nameset is None:
            nameset = NameSet(
                symbol=self.category.symbol_base, index=self.statement_index)
        ref = nameset.index if ref is None else ref
        title = Title(cat=cat, ref=ref, subtitle=subtitle)
        super().__init__(
            nameset=nameset,
            theory=theory,
            title=title,
            echo=False)
        if echo:
            self.echo()
        super()._declare_class_membership(declarative_class_list.note)

    def echo(self):
        repm.prnt(self.rep_report())

    def rep_title(self, cap=False):
        return self.title.rep_title(cap=cap)

    def rep_ref(self, cap=False):
        return self.title.rep_ref(cap=cap)

    def rep_report(self, output_proofs=True):
        """Return a representation of the note that may be included as a section in a report."""
        text = f'{repm.serif_bold(self.rep_title(cap=True))}: {self.natural_language}'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))


section_category = TitleCategory(
    name='section', symbol_base='§', natural_name='section', abridged_name='sect.')


class Section(AtheoreticalStatement):
    """A (leveled) section in a theory-elaboration-sequence.

    Sections allow to organize / structure (lengthy) theory-elaboration-sequences
    to improve readability.

    """

    def __init__(
            self,
            section_title: str,
            t: TheoryElaborationSequence,
            section_number: (None, int) = None,
            section_parent: (None, Section) = None,
            echo: (None, bool) = None):
        echo = get_config(echo, configuration.echo_note, configuration.echo_default,
                          fallback_value=False)
        self._section_title = section_title
        self._section_parent = section_parent
        self._section_level = 1 if section_parent is None else section_parent.section_level + 1
        if section_parent is not None:
            section_number = section_parent.get_next_section_number(section_number)
        else:
            section_number = t.get_next_section_number(section_number)
        self._section_number = section_number
        prefix = '' if section_parent is None else section_parent.section_reference + '.'
        self._section_reference = f'{prefix}{str(section_number)}'
        self.statement_index = t.crossreference_statement(self)
        self._max_subsection_number = 0
        self.category = section_category
        symbol = NameSet(
            symbol=self.category.symbol_base, index=self.statement_index)
        title = Title(ref=self._section_reference, cat=section_category,
                      subtitle=section_title)
        super().__init__(
            nameset=symbol,
            theory=t,
            echo=False)
        super()._declare_class_membership(declarative_class_list.note)
        if echo:
            self.echo()

    def echo(self):
        repm.prnt(self.rep_report())

    def get_next_section_number(self, section_number: int = None) -> int:
        if section_number is None:
            self._max_subsection_number += 1
        else:
            self._max_subsection_number = max([self._max_subsection_number + 1, section_number])
        return self._max_subsection_number

    @property
    def max_subsection_number(self) -> int:
        return self._max_subsection_number

    def rep_ref(self, cap=False) -> str:
        prefix = 'section' if self.section_level == 1 else 'sub-' * (
                self.section_level - 1) + 'section'
        text = f'{prefix}{repm.serif_bold(self.section_reference)}'
        return text

    def rep_report(self, output_proofs=True) -> str:
        text = f'{"#" * self.section_level} {repm.serif_bold(self.section_reference)} {repm.serif_bold(str(self.section_title).capitalize())}'
        text = repm.wrap(text)
        return text

    @property
    def section_level(self) -> int:
        return self._section_level

    @property
    def section_number(self) -> int:
        return self._section_number

    @property
    def section_reference(self) -> str:
        return self._section_reference

    @property
    def section_title(self) -> str:
        return self._section_title


class TheoryElaborationSequence(TheoreticalObject):
    """The TheoryElaboration pythonic class models a [theory-elaboration](theory-elaboration).

    """

    def __init__(
            self,
            u: UniverseOfDiscourse,
            nameset: (None, str, NameSet) = None,
            dashed_name: (None, str, DashedName) = None,
            title: (None, str, Title) = None,
            extended_theory: (None, TheoryElaborationSequence) = None,
            extended_theory_limit: (None, Statement) = None,
            stabilized: bool = False,
            echo: bool = None
    ):
        echo = get_config(echo, configuration.echo_theory_elaboration_sequence_declaration,
                          configuration.echo_default,
                          fallback_value=False)
        self._max_subsection_number = 0
        self._consistency = consistency_values.undetermined
        self._stabilized = False
        self.axiom_inclusions = tuple()
        self.definition_inclusions = tuple()
        self._inference_rule_inclusions = InferenceRuleInclusionDict(t=self)
        self.statements = tuple()
        self._extended_theory = extended_theory
        self._extended_theory_limit = extended_theory_limit
        self._commutativity_of_equality = None
        self._interpretation_disclaimer = False
        if nameset is None:
            symbol = StyledText(plaintext='T', text_style=text_styles.script_normal)
            index = u.index_symbol(base=symbol)
            nameset = NameSet(symbol=symbol, name='theory',
                              explicit_name='theory elaboration sequence', index=index)
        elif isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            index = u.index_symbol(base=nameset)
            nameset = NameSet(s=nameset, index=index)
        if title is None:
            title = Title(ref=str(nameset.index), cat=title_categories.theory_elaboration_sequence,
                          subtitle=None)
        elif isinstance(title, str):
            title = Title(ref=title, cat=title_categories.theory_elaboration_sequence,
                          subtitle=None)
        else:
            verify(
                title.category is None or title.category is title_categories.theory_elaboration_sequence,
                'The title category must be theory-elaboration-sequence.',
                title_category=title.category, title=title, slf=self)
            if title.category is None:
                title.category = title_categories.theory_elaboration_sequence
        super().__init__(
            nameset=nameset,
            is_theory_foundation_system=True if extended_theory is None else False,
            universe_of_discourse=u,
            dashed_name=dashed_name,
            title=title,
            echo=False)
        verify(is_in_class(u, classes.universe_of_discourse),
               'Parameter "u" is not a member of declarative-class universe-of-discourse.', u=u)
        verify(extended_theory is None or is_in_class(extended_theory, classes.theory_elaboration),
               'Parameter "extended_theory" is neither None nor a member of declarative-class theory.',
               u=u)
        verify(extended_theory_limit is None or
               (extended_theory is not None and
                is_in_class(extended_theory_limit, classes.statement) and
                extended_theory_limit in extended_theory.statements),
               'Parameter "theory_extension_statement_limit" is inconsistent.',
               u=u)
        super()._declare_class_membership(classes.theory_elaboration)
        if stabilized:
            # It is a design choice to stabilize the theory-elaboration
            # at the very end of construction (__init__()). Note that it
            # is thus possible to extend a theory and, for example,
            # add some new inference-rules by passing these instructions
            # to the constructor.
            self.stabilize()
        if echo:
            repm.prnt(self.rep_declaration())

    def assure_interpretation_disclaimer(self, echo: (None, bool) = None):
        """After the first usage of a contentual interpretation inference-rule,
        warns the user that no semantic verification is performed."""
        echo = get_config(echo, configuration.echo_default, fallback_value=False)
        if not self._interpretation_disclaimer:
            self.take_note(
                'By design, punctilious assures the syntactical correctness of theories and does not perform any '
                'semantic verification. Consequently, the usage of inference-rules that interpret content (i.e. '
                'axiom-interpretation and definition-interpretation) is critically dependent on the correctness of '
                'the content translation performed by the theory author, from axiom or definition natural language, '
                'to formulae.',
                subtitle='warning on content interpretation',
                echo=echo)
            self._interpretation_disclaimer = True

    @property
    def commutativity_of_equality(self):
        """Commutativity-of-equality is a fundamental theory property that enables
        support for SoET. None if the property is not equipped on
        the theory. An instance of FormalAxiom otherwise."""
        if self._commutativity_of_equality is not None:
            return self._commutativity_of_equality
        elif self.extended_theory is not None:
            return self.extended_theory.commutativity_of_equality
        else:
            return None

    @commutativity_of_equality.setter
    def commutativity_of_equality(self, p):
        verify(
            self._commutativity_of_equality is None,
            'A theory commutativity-of-equality property can only be set once '
            'to prevent inconsistency.')
        self._commutativity_of_equality = p

    def crossreference_axiom_inclusion(self, a):
        """During construction, cross-reference an axiom
        with its parent theory (if it is not already cross-referenced),
        and return its 0-based index in Theory.axioms."""
        assert isinstance(a, AxiomInclusion)
        if a not in self.axiom_inclusions:
            self.axiom_inclusions = self.axiom_inclusions + tuple(
                [a])
        return self.axiom_inclusions.index(a)

    def crossreference_definition_endorsement(self, d):
        """During construction, cross-reference an endorsement
        with its parent theory (if it is not already cross-referenced),
        and return its 0-based index in Theory.endorsements."""
        if d not in self.definition_inclusions:
            self.definition_inclusions = self.definition_inclusions + tuple(
                [d])
        return self.definition_inclusions.index(d)

    def crossreference_inference_rule_inclusion(self, i: InferenceRuleInclusion):
        """During construction, cross-reference an inference-rule
        with its parent theory-elaboration (if it is not already cross-referenced)."""
        if i not in self.inference_rule_inclusions:
            self.inference_rule_inclusions[i] = i
            return True
        else:
            return False

    def crossreference_statement(self, s):
        """During construction, cross-reference a statement 𝒮
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.statements."""
        assert isinstance(s, (Statement, Note, Section))
        # During construction (__init__()), the _theory property
        # may not be already set.
        # And calling crossreference_statement()
        # may be required before calling super(), in order to
        # retrieve the statement_index.
        # It follows that we cannot check the consistency of the
        # theory of the object under construction, like with:
        #   assert s.theory is self
        # It follows that we must fully delegate the responsibility
        # of theory consistency to the constructing object.
        if s not in self.statements:
            self.statements = self.statements + tuple([s])
        return self.statements.index(s)

    @property
    def extended_theory(self) -> (None, TheoryElaborationSequence):
        """None if this is a root theory, the theory that this theory extends otherwise."""
        return self._extended_theory

    @property
    def extended_theory_limit(self) -> (None, Statement):
        """If this is a limited extended-theory, the inclusive statement-limit of the inclusion."""
        return self._extended_theory_limit

    def get_next_section_number(self, section_number: int = None) -> int:
        if section_number is None:
            self._max_subsection_number += 1
        else:
            self._max_subsection_number = max([self._max_subsection_number + 1, section_number])
        return self._max_subsection_number

    @property
    def i(self):
        """Return the dictionary of inference-rule-inclusions contained in this theory-elaboration."""
        return self.inference_rule_inclusions

    @property
    def inference_rule_inclusions(self):
        """Return the dictionary of inference-rule-inclusions contained in this theory-elaboration."""
        return self._inference_rule_inclusions

    def iterate_theoretical_objcts_references(self, include_root: bool = True,
                                              visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it references recursively.

        Theoretical-objcts may contain references to multiple and diverse other theoretical-objcts. Do not confuse this iteration of all references with iterations of objects in the theory-chain.
        """
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        for statement in set(self.statements).difference(visited):
            if not is_in_class(statement, declarative_class_list.atheoretical_statement):
                yield statement
                visited.update({statement})
                yield from statement.iterate_theoretical_objcts_references(
                    include_root=False, visited=visited)
        if self.extended_theory is not None and self.extended_theory not in visited:
            # Iterate the extended-theory.
            if self.extended_theory_limit is not None:
                # The extended-theory is limited
                # i.e. this theory branched out before the end of the elaboration.
                # Thus, we must exclude statements that are posterior to the limit.
                # To do this, we simply black-list them
                # by including them in the visited set.
                black_list = (
                    statement
                    for statement in set(self.extended_theory.statements)
                    if statement.statement_index > self.extended_theory_limit.statement_index)
                visited.update(black_list)
            yield self.extended_theory
            visited.update({self.extended_theory})
            yield from self.extended_theory.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)

    def include_axiom(
            self, a: AxiomDeclaration, nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None) -> AxiomInclusion:
        """Postulate an axiom in this theory-elaboration (self)."""
        return AxiomInclusion(
            a=a, t=self, nameset=nameset, title=title, dashed_name=dashed_name, echo=echo)

    def include_definition(
            self, d: DefinitionDeclaration, nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None, echo: (None, bool) = None):
        """Include (aka endorse) a definition in this theory-elaboration (self)."""
        return DefinitionInclusion(
            d=d, t=self, nameset=nameset, title=title, dashed_name=dashed_name, echo=echo)

    def infer_by_substitution_of_equal_terms(
            self, original_expression, equality_statement, symbol=None,
            category=None, reference=None, title=None):
        """Infer a statement by applying the substitution-of-equal-terms (
        SoET) inference-rule.

        Let
        """
        return SubstitutionOfEqualTerms(
            original_expression=original_expression,
            equality_statement=equality_statement, nameset=symbol,
            category=category, theory=self, reference=reference, title=title)

    def iterate_statements_in_theory_chain(self):
        """Iterate through the (proven or sound) statements in the current theory-chain."""
        for t in self.iterate_theory_chain():
            for s in t.statements:
                yield s

    def iterate_theory_chain(self, visited: (None, set) = None):
        """Iterate over the theory-chain of this theory.


        The sequence is: this theory, this theory's extended-theory, the extended-theory's extended-theory, etc. until the root-theory is processes.

        Note:
        -----
        The theory-chain set is distinct from theory-dependency set.
        The theory-chain informs of the parent theories whose statements are considered valid in the current theory.
        Distinctively, theories may be referenced by meta-theorizing, or in hypothesis, or possibly other use cases.
        """
        visited = set() if visited is None else visited
        t = self
        while t is not None:
            yield t
            visited.update({t})
            if t.extended_theory is not None and t.extended_theory not in visited:
                t = t.extended_theory
            else:
                t = None

    def iterate_valid_propositions_in_theory_chain(self):
        """Iterate through the valid-propositions in the current theory-chain."""
        visited = set()
        for s in self.iterate_statements_in_theory_chain():
            if is_in_class(s, classes.formula_statement) and s.valid_proposition not in visited:
                yield s.valid_proposition
                visited.update({s.valid_proposition})

    @property
    def consistency(self) -> Consistency:
        """The currently proven consistency status of this theory.

        Possible values are:
        - proved-consistent,
        - proved-inconsistent,
        - undetermined."""
        return self._consistency

    @property
    def inconsistency_introduction_inference_rule_is_included(self):
        """True if the inconsistency-introduction inference-rule is included in this theory, False otherwise."""
        if self._includes_inconsistency_introduction_inference_rule is not None:
            return self._includes_inconsistency_introduction_inference_rule
        elif self.extended_theory is not None:
            return self.extended_theory.inconsistency_introduction_inference_rule_is_included
        else:
            return None

    def d(self, natural_language, symbol=None, reference=None, title=None):
        """Elaborate a new definition with natural-language. Shortcut function for
        t.elaborate_definition(...)."""
        return self.include_definition(
            natural_language=natural_language, nameset=symbol,
            reference=reference, title=title)

    def pose_hypothesis(
            self,
            hypothetical_proposition: Formula, nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None, dashed_name: (None, str, DashedName) = None,
            echo: bool = False) -> Hypothesis:
        """Pose a new hypothesis in the current theory."""
        return Hypothesis(
            t=self, hypothetical_formula=hypothetical_proposition,
            nameset=nameset, title=title, dashed_name=dashed_name,
            echo=echo)

    def rep_theory_report(self, output_proofs=True):
        """Return a representation that expresses and justifies the theory."""
        output = f'\n{repm.serif_bold(self.rep_name())}'
        output += f'\n{repm.serif_bold("Consistency:")} {str(self.consistency)}'
        output += f'\n{repm.serif_bold("Stabilized:")} {str(self.stabilized)}'
        output += f'\n{repm.serif_bold("Extended theory:")} {"N/A" if self.extended_theory is None else self.extended_theory.rep_fully_qualified_name()}'
        output += f'\n\n{repm.serif_bold("Simple-objct declarations:")}'
        # TODO: Limit the listed objects to those that are referenced by the theory,
        #   instead of outputting all objects in the universe-of-discourse.
        output = output + '\n' + '\n'.join(
            o.rep_declaration() for o in
            self.universe_of_discourse.simple_objcts.values())
        # Relation declarations
        relations = self.iterate_relations()
        arities = frozenset(r.arity for r in relations)
        for a in arities:
            output += repm.serif_bold(f'\n\n{rep_arity_as_text(a).capitalize()} relations:')
            for r_long_name in frozenset(
                    r.rep_fully_qualified_name() for r in relations if r.arity == a):
                output += '\n ⁃ ' + r_long_name
        output += f'\n\n{repm.serif_bold("Theory elaboration:")}'
        output = output + '\n\n' + '\n\n'.join(
            s.rep_report(output_proofs=output_proofs) for s in
            self.statements)
        return str(output)

    def soet(
            self, original_expression, equality_statement, symbol=None,
            category=None, reference=None, title=None):
        """Elaborate a new modus-ponens statement in the theory. Shortcut for
        ModusPonens(theory=t, ...)"""
        return self.infer_by_substitution_of_equal_terms(
            original_expression=original_expression,
            equality_statement=equality_statement, symbol=symbol,
            category=category, reference=reference, title=title)

    def prnt(self, output_proofs=True):
        repm.prnt(self.rep_theory_report(output_proofs=output_proofs))

    def prove_inconsistent(self, ii):
        verify(isinstance(ii, InconsistencyIntroductionStatement),
               'The ii statement is not of type InconsistencyIntroductionStatement.', ii=ii,
               theory=self)
        verify(ii in self.statements,
               'The ii statement is not a statement of this theory.', ii=ii, theory=self)
        self._consistency = consistency_values.proved_inconsistent

    def export_to_text(self, file_path, output_proofs=True):
        """Export this theory to a Unicode textfile."""
        text_file = open(file_path, 'w', encoding='utf-8')
        n = text_file.write(self.rep_theory_report(output_proofs=output_proofs))
        text_file.close()

    def open_section(self,
                     section_title: str,
                     section_number: (None, int) = None,
                     section_parent: (None, Section) = None,
                     echo: (None, bool) = None) -> Section:
        """Open a new section in the current theory-elaboration-sequence."""
        return Section(section_title=section_title, section_number=section_number,
                       section_parent=section_parent,
                       t=self,
                       echo=echo)

    def report_inconsistency_proof(self, proof: InferredStatement):
        verify(proof.t is self,
               'The theory of the ⌜proof⌝ is not the current theory ⌜self⌝.',
               proof_t=proof.t, proof=proof, slf=self)
        proof = unpack_formula(proof)
        verify(proof.relation is self.u.r.inconsistent,
               'The relation of the ⌜proof⌝ formula is not ⌜inconsistency⌝.',
               proof_relation=proof.relation, proof=proof, slf=self)
        verify(proof.parameters[0] is self,
               'The parameter of the ⌜proof⌝ formula is not the current theory ⌜self⌝.',
               proof_parameter=proof.parameters[0], proof=proof, slf=self)
        self._consistency = consistency_values.proved_inconsistent

    def rep_declaration(self) -> str:
        return f'Let {self.rep_fully_qualified_name()} be a theory-elaboration-sequence in {self.u.rep_name()}.'

    @property
    def stabilized(self):
        """Return the stabilized property of this theory-elaboration.
        """
        return self._stabilized

    def stabilize(self):
        verify(not self._stabilized,
               'This theory-elaboration is already stabilized.',
               severity=verification_severities.warning)
        self._stabilized = True

    def take_note(self, content: str, nameset: (None, str, NameSet) = None, ref: (None, str) = None,
                  cat: (None, TitleCategory) = None, subtitle: (None, str) = None,
                  echo: (None, bool) = None) -> Note:
        """Take a note, make a comment, or remark in this theory.

        Shortcut for u.take_note(theory=t, ...)

        :param content: The natural-language content of the note.
        :param nameset:
        :param ref:
        :param cat:
        :param subtitle:
        :param echo:
        :return:
        """
        return self.universe_of_discourse.take_note(t=self, content=content, nameset=nameset,
                                                    ref=ref, cat=cat,
                                                    subtitle=subtitle, echo=echo)

    @property
    def theoretical_objcts(self):
        list = set()
        for s in self.statements:
            list.add(s)
            if is_in_class(s, classes.formula):
                list.add()


class Hypothesis(Statement):
    def __init__(
            self, t: TheoryElaborationSequence, hypothetical_formula: Formula,
            nameset: (None, NameSet) = None,
            title: (None, Title) = None, dashed_name: (None, DashedName) = None,
            echo: bool = False):
        category = title_categories.hypothesis
        # TODO: Check that all components of the hypothetical-proposition
        #  are elements of the source theory-branch.
        verify(
            hypothetical_formula.is_proposition,
            'The hypothetical-formula is not a proposition.',
            hypothetical_formula=hypothetical_formula,
            slf=self)
        super().__init__(
            theory=t, category=category, nameset=nameset,
            title=title, dashed_name=dashed_name, echo=False)
        super()._declare_class_membership(declarative_class_list.hypothesis)
        self.hypothetical_proposition_formula = hypothetical_formula
        self.hypothetical_t = t.universe_of_discourse.t(
            extended_theory=t,
            extended_theory_limit=self
        )
        self.hypothetical_axiom = self.universe_of_discourse.declare_axiom(
            f'Assume {hypothetical_formula.rep_formula()} is true.')
        self.hypothetical_axiom_postulate = self.hypothetical_t.include_axiom(
            self.hypothetical_axiom)
        self.proposition = self.hypothetical_t.i.axiom_interpretation.infer_statement(
            self.hypothetical_axiom_postulate,
            hypothetical_formula)


class Proof:
    """TODO: Define the proof class"""

    def __init__(self):
        self.is_valid = True  # TODO: Develop the is_valid attribute


class Relation(TheoreticalObject):
    """
    Definition
    ----------
    A relation ◆ is a theoretical-object for formula.
    It assigns the following meaning to its composite formula 𝜑:
    𝜑 establishes a relation between its parameters.
    A relation ◆ has a fixed arity.

    Defining properties
    -------------------
     - Arity
     - Symbol

    Attributes
    ----------
    signal_proposition : bool
        True if the relation instance signals that formulae based on this relation are logical-propositions,
        i.e. the relation is a function whose domain is the set of truth values {True, False}.
        False otherwise.
        When True, the formula may be used as a theory-statement.

    signal_theoretical_morphism : bool
        True if the relation instance signals that formulae based on this relation are theoretical-morphisms.

    implementation : bool
        If the relation has an implementation, a reference to the python function.
    """

    def __init__(
            self, arity: int, nameset: (None, str, NameSet) = None, formula_rep=None,
            signal_proposition=None, signal_theoretical_morphism=None,
            implementation=None, universe_of_discourse=None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        echo = get_config(echo, configuration.echo_relation, configuration.echo_default,
                          fallback_value=False)
        assert isinstance(universe_of_discourse, UniverseOfDiscourse)
        signal_proposition = False if signal_proposition is None else signal_proposition
        signal_theoretical_morphism = False if signal_theoretical_morphism is None else signal_theoretical_morphism
        assert isinstance(signal_proposition, bool)
        assert isinstance(signal_theoretical_morphism, bool)
        self.formula_rep = Formula.function_call if formula_rep is None else formula_rep
        self.signal_proposition = signal_proposition
        self.signal_theoretical_morphism = signal_theoretical_morphism
        self.implementation = implementation
        assert arity is not None and isinstance(arity, int) and arity > 0
        self.arity = arity
        if nameset is None:
            nameset = configuration.default_relation_nameset
        super().__init__(
            universe_of_discourse=universe_of_discourse, nameset=nameset, dashed_name=dashed_name,
            echo=False)
        self.universe_of_discourse.cross_reference_relation(r=self)
        super()._declare_class_membership(classes.relation)
        if echo:
            self.echo()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((Relation, self.nameset, self.arity))

    def echo(self):
        repm.prnt(self.rep_declaration())

    def rep_declaration(self):
        output = f'Let {self.rep_fully_qualified_name()} be a {rep_arity_as_text(self.arity)} relation in {self.u.rep_name()}'
        output = output + f' (default notation: {self.formula_rep}).'
        return output


def rep_arity_as_text(n):
    match n:
        case 1:
            return 'unary'
        case 2:
            return 'binary'
        case 3:
            return 'ternary'
        case _:
            return f'{n}-ary'


class SimpleObjct(TheoreticalObject):
    """
    Definition
    ----------
    A simple-objct-component ℴ is a theoretical-object that has no special attribute,
    and whose sole function is to provide the meaning of being itself.
    """

    def __init__(
            self, universe_of_discourse: UniverseOfDiscourse,
            nameset: (None, str, NameSet) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        echo = get_config(echo, configuration.echo_simple_objct_declaration,
                          configuration.echo_default,
                          fallback_value=False)
        super().__init__(
            universe_of_discourse=universe_of_discourse, nameset=nameset,
            dashed_name=dashed_name, echo=False)
        self.universe_of_discourse.cross_reference_simple_objct(o=self)
        if echo:
            self.echo()

    def echo(self):
        repm.prnt(self.rep_declaration())

    def is_masked_formula_similar_to(self, o2, mask, _values):
        assert isinstance(o2, TheoreticalObject)
        if isinstance(o2, FreeVariable):
            if o2 in mask:
                # o2 is a variable, and it is present in the mask.
                # first, we must check if it is already in the dictionary of values.
                if o2 in _values:
                    # the value is already present in the dictionary.
                    known_value = _values[o2]
                    if known_value is self:
                        # the existing value matches the newly observed value.
                        # until there, masked-formula-similitude is preserved.
                        return True, _values
                    else:
                        # the existing value does not match the newly observed value.
                        # masked-formula-similitude is no longer preserved.
                        return False, _values
                else:
                    # the value is not present in the dictionary.
                    # until there, masked-formula-similitude is preserved.
                    _values[o2] = self
                    return True, _values
        if not isinstance(o2, SimpleObjct):
            # o1 (self) is a simple-objct, and o2 is something else.
            # in consequence, masked-formula-similitude is no longer preserved.
            return False, _values
        # o2 is not a variable.
        return self.is_formula_equivalent_to(o2), _values

    def rep_declaration(self):
        output = f'Let {self.rep_fully_qualified_name()} be a simple-objct in {self.u.rep_name()}.'
        return output


class SubstitutionOfEqualTerms(FormulaStatement):
    """
    TODO: Develop SubstitutionOfEqualTerms

    Definition:
    -----------
    A substitution-of-equal-terms is a valid rule-of-inference propositional-logic argument that,
    given a proposition (phi)
    given a proposition (x = y)
    infers the proposition (subst(phi, x, y))
    """

    symbol_base = '𝚂𝙾𝙴𝚃'

    def __init__(
            self, original_expression, equality_statement, nameset=None,
            category=None, theory=None, reference=None, title=None):
        category = title_categories.proposition if category is None else category
        # Check p_implies_q consistency
        assert isinstance(theory, TheoryElaborationSequence)
        assert isinstance(original_expression, FormulaStatement)
        assert theory.contains_theoretical_objct(original_expression)
        assert isinstance(equality_statement, FormulaStatement)
        assert theory.contains_theoretical_objct(equality_statement)
        assert equality_statement.valid_proposition.relation is theory.universe_of_discourse.r.equality
        left_term = equality_statement.valid_proposition.parameters[0]
        right_term = equality_statement.valid_proposition.parameters[1]
        self.original_expression = original_expression
        self.equality_statement = equality_statement
        substitution_map = {left_term: right_term}
        valid_proposition = original_expression.valid_proposition.substitute(
            substitution_map=substitution_map, target_theory=theory,
            lock_variable_scope=True)
        # Note: valid_proposition will be formula-equivalent to self,
        #   if there are no occurrences of left_term in original_expression.
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            category=category,
            nameset=nameset)

    def rep_report(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.rep_title(cap=True)}: {self.valid_proposition.rep_formula()}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Substitution of equal terms")}'
            output = output + f'\n\t{self.original_expression.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.original_expression.rep_ref())}.'
            output = output + f'\n\t{self.equality_statement.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.equality_statement.rep_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.rep_formula(expand=True):<70} │ ∎'
        return output


class Tuple(tuple):
    """Tuple subclasses the native tuple class.
    The resulting supports setattr, getattr, hasattr,
    which are convenient to create friendly programmatic shortcuts."""
    pass


class RelationDict(collections.UserDict):
    """A dictionary that exposes well-known relations as properties.

    """

    def __init__(self, u: UniverseOfDiscourse):
        self.u = u
        super().__init__()
        # Well-known objects
        self._biconditional = None
        self._conjunction = None
        self._disjunction = None
        self._equality = None
        self._inconsistent = None
        self._inequality = None
        self._implication = None
        self._negation = None

    def declare(self, arity: int, nameset: (None, str, NameSet) = None, formula_rep=None,
                signal_proposition=None,
                signal_theoretical_morphism=None,
                implementation=None, dashed_name: (None, str, DashedName) = None,
                echo: (None, bool) = None):
        """Declare a new relation in this universe-of-discourse.
        """
        return Relation(
            arity=arity,
            nameset=nameset, dashed_name=dashed_name,
            formula_rep=formula_rep,
            signal_proposition=signal_proposition,
            signal_theoretical_morphism=signal_theoretical_morphism,
            implementation=implementation,
            universe_of_discourse=self.u,
            echo=echo)

    @property
    def biconditional(self):
        """The well-known biconditional relation.

        Abridged property: u.r.iif

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._biconditional is None:
            self._biconditional = self.declare(
                2,
                NameSet(
                    symbol=StyledText(plaintext='<==>', unicode='⟺', latex_math='\\iff'),
                    name=StyledText(plaintext='biconditional'),
                    index=None),
                Formula.infix,
                signal_proposition=True, dashed_name='biconditional')
        return self._biconditional

    @property
    def conjunction(self):
        """The well-known conjunction relation.

        Abridged property: u.r.land

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._conjunction is None:
            self._conjunction = self.declare(
                2,
                NameSet(
                    symbol=StyledText(unicode='∧', latex_math='\\land'),
                    name=StyledText(plaintext='and'),
                    explicit_name=StyledText(plaintext='conjunction'),
                    index=None),
                Formula.infix,
                signal_proposition=True)
        return self._conjunction

    @property
    def disjunction(self):
        """The well-known disjunction relation.

        Abridged property: u.r.land

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._disjunction is None:
            self._disjunction = self.declare(
                2,
                NameSet(
                    symbol=StyledText(unicode='∨', latex_math='\\lor'),
                    name=StyledText(plaintext='or'),
                    explicit_name=StyledText(plaintext='disjunction'),
                    index=None),
                Formula.infix,
                signal_proposition=True)
        return self._disjunction

    @property
    def equal(self):
        """The well-known equality relation.

        Unabridged property: universe_of_discourse.relations.equality

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.equality

    @property
    def equality(self):
        """The well-known equality relation.

        Abridged property: u.r.equal

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._equality is None:
            self._equality = self.declare(
                2, NameSet('='), Formula.infix,
                signal_proposition=True, dashed_name='equality')
        return self._equality

    @property
    def inc(self):
        """The well-known (theory-)inconsistent relation.

        Unabridged property: u.r.inconsistent

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.inconsistent

    @property
    def implication(self):
        """The well-known implication relation.

        Abridged property: u.r.implies

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._implication is None:
            self._implication = self.declare(
                2,
                NameSet(
                    symbol=StyledText(plaintext='==>', unicode='⟹', latex_math=r'\implies'),
                    name=StyledText(plaintext='implies'),
                    explicit_name=StyledText(plaintext='implication'),
                    index=None),
                Formula.infix,
                signal_proposition=True)
        return self._implication

    @property
    def implies(self):
        """The well-known implication relation.

        Unabridged property: u.r.implication

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.implication

    @property
    def inconsistent(self):
        """The well-known (theory-)inconsistent relation.

        Abridged property: u.r.inc

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._inconsistent is None:
            self._inconsistent = self.declare(
                1,
                NameSet(
                    acronym=StyledText(plaintext='Inc'),
                    name=StyledText(plaintext='inconsistent'),
                    index=None),
                Formula.prefix,
                signal_proposition=True)
        return self._inconsistent

    @property
    def inequality(self):
        """The well-known inequality relation.

        Abridged property: u.r.neq

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._inequality is None:
            self._inequality = self.declare(
                2,
                NameSet(
                    symbol=StyledText(unicode='≠', latex_math='\\neq'),
                    acronym=StyledText(plaintext='neq'),
                    name=StyledText(plaintext='not equal'),
                    index=None),
                Formula.infix,
                signal_proposition=True)
        return self._inequality

    @property
    def land(self):
        """The well-known conjunction relation.

        Unabridged property: u.r.conjunction

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.conjunction

    @property
    def lnot(self):
        """The well-known negation relation.

        Abridged property: u.r.negation

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.negation

    @property
    def lor(self):
        """The well-known disjunction relation.

        Unabridged property: u.r.disjunction

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.disjunction

    @property
    def negation(self):
        """The well-known negation relation.

        Abridged property: u.r.lnot

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._negation is None:
            self._negation = self.declare(
                1,
                NameSet(
                    symbol=StyledText(unicode='¬', latex_math='\\neg'),
                    acronym=StyledText(plaintext='not'),
                    name=StyledText(plaintext='negation'),
                    index=None),
                Formula.prefix,
                signal_proposition=True)
        return self._negation

    @property
    def neq(self):
        """The well-known inequality relation.

        Unabridged property: u.r.inequality

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.inequality


class InferenceRuleDeclarationDict(collections.UserDict):
    """A dictionary that exposes well-known objects as properties.

    """

    def __init__(self, u: UniverseOfDiscourse):
        self.u = u
        super().__init__()
        # Well-known objects
        self._absorption = None
        self._axiom_interpretation = None
        self._biconditional_elimination_left = None
        self._biconditional_elimination_right = None
        self._biconditional_introduction = None
        self._conjunction_elimination_left = None
        self._conjunction_elimination_right = None
        self._conjunction_introduction = None
        self._definition_interpretation = None
        self._disjunction_elimination = None  # TODO: IMPLEMENT disjunction_elimination
        self._disjunction_introduction = None
        self._double_negation_elimination = None
        self._double_negation_introduction = None
        self._equality_commutativity = None
        self._equal_terms_substitution = None
        self._inconsistency_introduction = None
        self._modus_ponens = None
        self._variable_substitution = None

    @property
    def absorb(self) -> InferenceRuleDeclaration:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Unabridged property: u.i.absorption

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.absorption

    @property
    def absorption(self) -> InferenceRuleDeclaration:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Abridged property: u.i.absorb

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(p_implies_q: FormulaStatement, t: TheoryElaborationSequence) -> Formula:
            """

            :param p_implies_q: A formula-statement of the form: (P ⟹ Q).
            :param t: The current theory-elaboration-sequence.
            :return: The (proven) formula: (P ⟹ (P ∧ Q)).
            """
            p_implies_q = unpack_formula(p_implies_q)
            p = unpack_formula(p_implies_q.parameters[0])
            q = unpack_formula(p_implies_q.parameters[1])
            p_implies_p_and_q = t.u.f(t.u.r.implication, p, t.u.f(t.u.r.conjunction, p, q))
            return p_implies_p_and_q

        def verify_args(*args, t: TheoryElaborationSequence) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            phi = args[0]
            verify(
                t.contains_theoretical_objct(phi),
                'Statement ⌜phi⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                phi=phi, t=t, slf=self)
            phi = unpack_formula(phi)
            verify(
                phi.relation is t.u.r.implication,
                'The relation of formula ⌜phi⌝ must be an implication.',
                phi_relation=phi.relation, phi=phi, t=t, slf=self)
            return True

        if self._absorption is None:
            self._absorption = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('absorb', index=None),
                title='absorption',
                dashed_name=DashedName('absorption'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._absorption

    @property
    def axiom_interpretation(self) -> InferenceRuleDeclaration:
        """The axiom_interpretation inference-rule: 𝒜 ⊢ P.

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.

        Warning
        -------
        Axiom-interpretation is especially dangerous because, contrary to most inference-rules,
        it allows the introduction of arbitrary truthes in the theory. For this reason,
        one must be very attentive when applying this inference-rule to assure the resulting
        formula-statement complies / interprets properly its related contentual-axiom.
        """

        def infer_formula(a: AxiomInclusion, p: Formula, t: TheoryElaborationSequence) -> Formula:
            """Compute the formula that results from applying this inference-rule with those arguments.

            :param a: An axiom-inclusion in the theory-elaboration-sequence under consideration: 𝒜.
            :param p: A propositional formula: P.
            :param t: The current theory-elaboration-sequence.
            :return: (Formula) The inferred formula: P.
            """
            p = unpack_formula(p)
            return p

        def verify_args(a: AxiomInclusion, p: Formula, t: TheoryElaborationSequence) -> bool:
            """Verify if the arguments comply syntactically with the inference-rule.

            WARNING:
            --------
            No semantic operation is performed.

           :param a: An axiom-inclusion in the theory-elaboration-sequence under consideration: 𝒜.
            :param p: A propositional formula: P.
            :param t: The current theory-elaboration-sequence.
            :return: (bool) True if the inference-rule arguments comply syntactically
                with the inference-rule, False otherwise.
            """
            verify(
                is_in_class(a, classes.axiom_inclusion),
                '⌜a⌝ is not of declarative-class axiom-inclusion.',
                a=a, t=t, slf=self)
            verify(
                t.contains_theoretical_objct(a),
                '⌜a⌝ is not contained in ⌜t⌝.',
                a=a, t=t, slf=self)
            verify(
                is_in_class(p, classes.formula),
                '⌜p⌝ is not of declarative-class formula.',
                p=p, t=t, slf=self)
            verify(
                p.is_proposition,
                '⌜p⌝ is not propositional.',
                p=p, t=t, slf=self)
            # TODO: Add a verification step: the axiom is not locked.
            return True

        if self._axiom_interpretation is None:
            self._axiom_interpretation = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('𝙰𝙸', index=None),
                title='axiom interpretation',
                dashed_name=DashedName('axiom-interpretation'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._axiom_interpretation

    @property
    def bi(self) -> InferenceRuleDeclaration:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Unabridged property: u.i.biconditional_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_introduction

    @property
    def bel(self) -> InferenceRuleDeclaration:
        """The well-known biconditional-elimination (left) inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Abridged property: u.i.bel

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_elimination_left

    @property
    def ber(self) -> InferenceRuleDeclaration:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Abridged property: u.i.ber()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_elimination_right

    @property
    def biconditional_elimination_left(self) -> InferenceRuleDeclaration:
        """The well-known biconditional-elimination (left) inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Abridged property: u.i.bel

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(*args, t: TheoryElaborationSequence) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            phi = unpack_formula(args[0])
            # phi is a formula of the form P ⟺ Q
            # unpack the embedded formulae
            p = unpack_formula(phi.parameters[0])
            q = unpack_formula(phi.parameters[1])
            psi = t.u.f(t.u.r.implication, p, q)
            return psi

        def verify_args(*args, t: TheoryElaborationSequence) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            phi = args[0]
            verify(
                t.contains_theoretical_objct(phi),
                'Statement ⌜phi⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                phi=phi, t=t, slf=self)
            phi = unpack_formula(phi)
            verify(
                phi.relation is t.u.r.biconditional,
                'The relation of formula ⌜phi⌝ must be a biconditional.',
                phi_relation=phi.relation, phi=phi, t=t, slf=self)
            return True

        if self._biconditional_elimination_left is None:
            self._biconditional_elimination_left = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('bel', index=None),
                title='biconditional elimination (left)',
                dashed_name=DashedName('biconditional-elimination-left'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._biconditional_elimination_left

    @property
    def biconditional_elimination_right(self) -> InferenceRuleDeclaration:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Abridged property: u.i.ber()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(*args, t: TheoryElaborationSequence) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            phi = unpack_formula(args[0])
            # phi is a formula of the form P ⟺ Q
            # unpack the embedded formulae
            p = unpack_formula(phi.parameters[0])
            q = unpack_formula(phi.parameters[1])
            psi = t.u.f(t.u.r.implication, q, p)
            return psi

        def verify_compatibility(*args, t: TheoryElaborationSequence) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            phi = args[0]
            verify(
                t.contains_theoretical_objct(phi),
                'Statement ⌜phi⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                phi=phi, t=t, slf=self)
            phi = unpack_formula(phi)
            verify(
                phi.relation is t.u.r.biconditional,
                'The relation of formula ⌜phi⌝ must be a biconditional.',
                phi_relation=phi.relation, phi=phi, t=t, slf=self)
            return True

        if self._biconditional_elimination_right is None:
            self._biconditional_elimination_right = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('ber', index=None),
                title='biconditional elimination (right)',
                dashed_name=DashedName('biconditional-elimination-right'),
                infer_formula=infer_formula,
                verify_args=verify_compatibility)
        return self._biconditional_elimination_right

    @property
    def biconditional_introduction(self) -> InferenceRuleDeclaration:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Abridged property: u.i.bi

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(*args, t: TheoryElaborationSequence) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            q = unpack_formula(args[1])
            return t.u.f(t.u.r.biconditional, p, q)

        def verify_args(*args, t: TheoryElaborationSequence) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 2,
                'Exactly 2 items are expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p_implies_q = args[0]
            verify(
                t.contains_theoretical_objct(p_implies_q),
                'Statement ⌜p_implies_q⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                p_implies_q=p_implies_q, t=t, slf=self)
            p_implies_q = unpack_formula(p_implies_q)
            verify(
                p_implies_q.relation is t.u.r.implication,
                'The relation of formula ⌜p_implies_q⌝ must be an implication.',
                p_implies_q_relation=p_implies_q.relation, p_implies_q=p_implies_q, t=t, slf=self)
            q_implies_p = args[1]
            verify(
                t.contains_theoretical_objct(q_implies_p),
                'Statement ⌜q_implies_p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                q_implies_p=q_implies_p, t=t, slf=self)
            q_implies_p = unpack_formula(q_implies_p)
            verify(
                q_implies_p.relation is t.u.r.implication,
                'The relation of formula ⌜q_implies_p⌝ must be an implication.',
                q_implies_p_relation=p_implies_q.relation, q_implies_p=q_implies_p, t=t, slf=self)
            return True

        if self._biconditional_introduction is None:
            self._biconditional_introduction = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('bi', index=None),
                title='biconditional introduction',
                dashed_name=DashedName('biconditional-introduction'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._biconditional_introduction

    @property
    def cel(self) -> InferenceRuleDeclaration:
        """The well-known conjunction-elimination (left) inference-rule: P ∧ Q ⊢ P.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_elimination_left

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.conjunction_elimination_left

    @property
    def cer(self) -> InferenceRuleDeclaration:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_elimination_right

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.conjunction_elimination_right

    @property
    def ci(self) -> InferenceRuleDeclaration:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.conjunction_introduction

    @property
    def conjunction_elimination_left(self) -> InferenceRuleDeclaration:
        """The well-known conjunction-elimination (left) inference-rule: P ∧ Q ⊢ P.

        Abridged property: u.i.cel()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(*args, t: TheoryElaborationSequence) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            q = unpack_formula(p.parameters[0])
            return q

        def verify_compatibility(*args, t: TheoryElaborationSequence) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                args=args, t=t, slf=self)
            p = unpack_formula(p)
            verify(
                p.relation is t.u.r.conjunction,
                'The relation of formula ⌜p⌝ must be a conjunction.',
                p_relation=p.relation, p=p, t=t, slf=self)
            return True

        if self._conjunction_elimination_left is None:
            self._conjunction_elimination_left = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('cel', index=None),
                title='conjunction elimination (left)',
                dashed_name=DashedName('conjunction-elimination-left'),
                infer_formula=infer_formula,
                verify_args=verify_compatibility)
        return self._conjunction_elimination_left

    @property
    def conjunction_elimination_right(self) -> InferenceRuleDeclaration:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        Abridged property: u.i.cer()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(*args, t: TheoryElaborationSequence) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            r = unpack_formula(p.parameters[1])
            return r

        def verify_compatibility(*args, t: TheoryElaborationSequence) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                args=args, t=t, slf=self)
            p = unpack_formula(p)
            verify(
                p.relation is t.u.r.conjunction,
                'The relation of formula ⌜p⌝ must be a conjunction.',
                p_relation=p.relation, p=p, t=t, slf=self)
            return True

        if self._conjunction_elimination_right is None:
            self._conjunction_elimination_right = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('cer', index=None),
                title='conjunction elimination (right)',
                dashed_name=DashedName('conjunction-elimination-right'),
                infer_formula=infer_formula,
                verify_args=verify_compatibility)
        return self._conjunction_elimination_right

    @property
    def conjunction_introduction(self) -> InferenceRuleDeclaration:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Abridged property: u.i.ci

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(*args, t: TheoryElaborationSequence) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            q = unpack_formula(args[1])
            return t.u.f(t.u.r.land, p, q)

        def verify_args(*args, t: TheoryElaborationSequence) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 2,
                'Exactly 2 items are expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                p=p, t=t, slf=self)
            p = unpack_formula(p)
            q = args[1]
            verify(
                t.contains_theoretical_objct(q),
                'Statement ⌜q⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                q=q, t=t, slf=self)
            q = unpack_formula(q)
            return True

        if self._conjunction_introduction is None:
            self._conjunction_introduction = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('ci', index=None),
                title='conjunction introduction',
                dashed_name=DashedName('conjunction-introduction'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._conjunction_introduction

    @property
    def definition_interpretation(self) -> InferenceRuleDeclaration:
        """The definition_interpretation inference-rule: 𝒟 ⊢ (P = Q).

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.

        Warning
        -------
        Definition-interpretation is especially dangerous because, contrary to most inference-rules,
        it allows the introduction of arbitrary truthes in the theory. For this reason,
        one must be very attentive when applying this inference-rule to assure the resulting
        formula-statement complies / interprets properly its related contentual-definition.
        """

        def infer_formula(d: DefinitionInclusion, p_equal_q: Formula,
                          t: TheoryElaborationSequence) -> Formula:
            """Compute the formula that results from applying this inference-rule with those arguments.

            :param d: A definition-inclusion in the theory-elaboration-sequence under consideration: 𝒟.
            :param p_equal_q: A propositional formula of the form: (P = Q)
            :param t: The current theory-elaboration-sequence.
            :return: (Formula) The inferred formula: (P = Q).
            """
            p_equal_q = unpack_formula(p_equal_q)
            return p_equal_q

        def verify_args(d: DefinitionInclusion, p_equal_q: Formula,
                        t: TheoryElaborationSequence) -> bool:
            """Verify if the arguments comply syntactically with the inference-rule.

            WARNING:
            --------
            No semantic operation is performed.

            :param d: A definition-inclusion in the theory-elaboration-sequence under consideration: 𝒟.
            :param p_equal_q: A propositional formula of the form: (P = Q)
            :param t: The current theory-elaboration-sequence.
            :return: (Formula) The inferred formula: (P = Q).
            """
            verify(
                is_in_class(d, classes.definition_inclusion),
                '⌜d⌝ is not of declarative-class definition-inclusion.',
                d=d, t=t, slf=self)
            verify(
                t.contains_theoretical_objct(d),
                '⌜d⌝ is not contained in ⌜t⌝.',
                d=d, t=t, slf=self)
            verify(
                is_in_class(p_equal_q, classes.formula),
                '⌜p_equal_q⌝ is not of declarative-class formula.',
                p_equal_q=p_equal_q, d=d, t=t, slf=self)
            verify(
                p_equal_q.relation is t.u.r.equality,
                'The root relation of ⌜p_equal_q⌝ is not the equality relation.',
                p_equal_q_relation=p_equal_q.relation, p_equal_q=p_equal_q, d=d, t=t, slf=self)
            return True

        if self._definition_interpretation is None:
            self._definition_interpretation = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('𝙳𝙸', index=None),
                title='definition interpretation',
                dashed_name=DashedName('definition-interpretation'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._definition_interpretation

    @property
    def di(self) -> InferenceRuleDeclaration:
        """The well-known disjunction-introduction inference-rule: P ⊢ (P ∨ Q).

        Unabridged property: u.i.disjunction_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.disjunction_introduction

    @property
    def disjunction_introduction(self) -> InferenceRuleDeclaration:
        """The well-known disjunction-introduction inference-rule: P ⊢ (P ∨ Q).

        Abridged property: u.i.di

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(*args, t: TheoryElaborationSequence) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            q = unpack_formula(args[1])  # Note: q may be a formula, because q may be false.
            return t.u.f(t.u.r.disjunction, p, q)

        def verify_args(*args, t: TheoryElaborationSequence) -> bool:
            """

            :param args: A statement P, and a propositional-formula Q
            :param t:
            :return: The statement (P ∨ Q)
            """
            verify(
                len(args) == 2,
                'Exactly 2 items are expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                p=p, t=t, slf=self)
            p = unpack_formula(p)
            # Q may be a formula (i.e. it is not necessarily a statement),
            # because Q may be any propositional formula (i.e it may be false).
            q = unpack_formula(args[1])
            verify(
                q.is_proposition,
                'Statement ⌜q⌝ must be a logical-proposition formula (and not necessarily a statement).',
                q_is_proposition=q.is_proposition, q=q, p=p, t=t, slf=self)
            return True

        if self._disjunction_introduction is None:
            self._disjunction_introduction = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('di', index=None),
                title='disjunction introduction',
                dashed_name=DashedName('disjunction-introduction'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._disjunction_introduction

    @property
    def dne(self) -> InferenceRuleDeclaration:
        """The well-known double-negation-elimination inference-rule: ¬¬P ⊢ P.

        Original method: universe_of_discourse.inference_rules.double_negation_elimination

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.double_negation_elimination

    @property
    def dni(self) -> InferenceRuleDeclaration:
        """The well-known double-negation-introduction inference-rule: P ⊢ ¬¬P.

        Original method: universe_of_discourse.inference_rules.double_negation_introduction()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.double_negation_introduction

    @property
    def double_negation_elimination(self) -> InferenceRuleDeclaration:
        """The well-known double-negation-elimination inference-rule: ¬¬P ⊢ P.

        Abridged property: u.i.dne

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(*args, t: TheoryElaborationSequence) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            q = unpack_formula(p.parameters[0])
            r = unpack_formula(q.parameters[0])
            return r

        def verify_args(*args, t: TheoryElaborationSequence) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                args=args, t=t, slf=self)
            p = unpack_formula(p)
            verify(
                p.relation is t.u.r.lnot,
                'The relation of formula ⌜p⌝ must be a negation.',
                p_relation=p.relation, p=p, t=t, slf=self)
            q = unpack_formula(p.parameters[0])
            verify(
                q.relation is t.u.r.lnot,
                'The relation of formula ⌜q⌝ must be a negation.',
                q_relation=q.relation, q=q, p=p, t=t, slf=self)
            return True

        if self._double_negation_elimination is None:
            self._double_negation_elimination = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('dne', index=None),
                title='double negation elimination',
                dashed_name=DashedName('double-negation-elimination'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._double_negation_elimination

    @property
    def double_negation_introduction(self) -> InferenceRuleDeclaration:
        """The well-known double-negation-introduction inference-rule: P ⊢ ¬¬P.

        Abridged property: u.i.dni

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(*args, t: TheoryElaborationSequence) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            return t.u.f(t.u.r.lnot, t.u.f(t.u.r.lnot, p))

        def verify_args(*args, t: TheoryElaborationSequence) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                args=args, t=t, slf=self)
            return True

        if self._double_negation_introduction is None:
            self._double_negation_introduction = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('dni', index=None),
                title='double negation introduction',
                dashed_name=DashedName('double-negation-introduction'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._double_negation_introduction

    @property
    def ec(self) -> InferenceRuleDeclaration:
        """The equality-commutativity inference-rule: (P = Q) ⊢ (Q = P).

        Unabridged property: universe_of_discourse.inference_rules.equality_commutativity

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.equality_commutativity

    @property
    def equality_commutativity(self) -> InferenceRuleDeclaration:
        """The equality-commutativity inference-rule: (P = Q) ⊢ (Q = P).

        Abridged property: u.i.ec

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(p_equal_q: FormulaStatement, t: TheoryElaborationSequence) -> Formula:
            """

            :param p_equal_q: A formula-statement of the form: (P = Q)
            :param t:
            :return:
            """
            p_equal_q = unpack_formula(p_equal_q)
            p = p_equal_q.parameters[0]
            q = p_equal_q.parameters[1]
            return t.u.f(t.u.r.equality, q, p)

        def verify_args(p_equal_q: FormulaStatement, t: TheoryElaborationSequence) -> bool:
            """

            :param p_equal_q: A formula-statement of the form: (P = Q)
            :param t:
            :return: The formula (Q = P)
            """
            verify(
                is_in_class(p_equal_q, classes.formula_statement),
                '⌜p_equal_q⌝ is not of the declarative-class formula-statement.',
                p_equal_q=p_equal_q, t=t, slf=self)
            verify(
                t.contains_theoretical_objct(p_equal_q),
                'Statement ⌜p_equal_q⌝ is not contained in ⌜t⌝''s hierarchy.',
                p_equal_q=p_equal_q, t=t, slf=self)
            p_equal_q = unpack_formula(p_equal_q)
            verify(
                p_equal_q.relation is self.u.r.equality,
                'The root relation of formula ⌜p_equal_q⌝ is not the equality relation.',
                p_equal_q_relation=p_equal_q.relation, p_equal_q=p_equal_q, t=t, slf=self)
            return True

        if self._equality_commutativity is None:
            self._equality_commutativity = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('𝙴𝙲', index=None),
                title='equality commutativity',
                dashed_name=DashedName('equality-commutativity'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._equality_commutativity

    @property
    def inconsistency_introduction(self) -> InferenceRuleDeclaration:
        """The inconsistency-introduction inference-rule: (P ∧ ¬P) ⊢ Inc(t).

        Abridged property: u.i.ii

        Inconsistency-introduction is an extraordinary inference-rule
        because it proves that the theory is inconsistent. It follows
        that the corresponding statement: ⌜Inc(t)⌝ becomes paradoxically
        invalid as soon as it is expressed in the current theory. In
        fact, ⌜Inc(t)⌝ should rather be understood as a meta-statement
        about the theory. In future versions of punctilious we will consider
        stating ⌜Inc(t)⌝ in a distinct meta-theory.
        
        Once ⌜Inc(t)⌝ is stated, the ⌜consistency⌝ property of the 
        current theory is automatically changed to ⌜inconsistent⌝.

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(p: FormulaStatement, not_p: FormulaStatement,
                          t: TheoryElaborationSequence) -> Formula:
            """
            :param p: a formula-statement of the form: (P).
            :param not_p: a formula-statement of the form: (¬P).

            """
            inc = t.u.f(t.u.r.inconsistent, t)
            return inc

        def verify_args(p: FormulaStatement, not_p: FormulaStatement,
                        t: TheoryElaborationSequence) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(is_in_class(p, classes.formula_statement),
                   '⌜p⌝ is not of declarative-class formula-statement.',
                   p=p, t=t, slf=self)
            p = unpack_formula(p)
            verify(is_in_class(not_p, classes.formula_statement),
                   '⌜not_p⌝ is not of declarative-class formula-statement.',
                   not_p=not_p, t=t, slf=self)
            not_p_r = unpack_formula(not_p)
            verify(
                not_p_r.relation is t.u.r.negation,
                'The relation of formula ⌜not_p_r⌝ is not a negation.',
                not_p_r_relation=not_p_r.relation, not_p_r=not_p_r, t=t, slf=self)
            p_in_not_p = unpack_formula(not_p_r.parameters[0])
            verify(
                p_in_not_p.is_formula_equivalent_to(p),
                'The sub-formula ⌜p⌝ in ⌜not_p⌝ is not formula-equivalent to formula ⌜p⌝.',
                p_in_not_p=p_in_not_p.relation, not_p_r=not_p_r, t=t, slf=self)
            return True

        if self._inconsistency_introduction is None:
            self._inconsistency_introduction = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('Inc', index=None),
                title='inconsistency introduction',
                dashed_name=DashedName('inconsistency-introduction'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._inconsistency_introduction

    @property
    def ii(self) -> InferenceRuleDeclaration:
        """The inconsistency-introduction inference-rule: (P ∧ ¬P) ⊢ Inc(t).

            Unabridged property: universe_of_discourse.inference_rules.inconsistency_introduction

            Inconsistency-introduction is an extraordinary inference-rule
            because it proves that the theory is inconsistent. It follows
            that the corresponding statement: ⌜Inc(t)⌝ becomes paradoxically
            invalid as soon as it is expressed in the current theory. In
            fact, ⌜Inc(t)⌝ should rather be understood as a meta-statement
            about the theory. In future versions of punctilious we will consider
            stating ⌜Inc(t)⌝ in a distinct meta-theory.

            Once ⌜Inc(t)⌝ is stated, the ⌜consistency⌝ property of the
            current theory is automatically changed to ⌜inconsistent⌝.

            If the inference-rule does not exist in the universe-of-discourse,
            the inference-rule is automatically declared.
            """
        return self.inconsistency_introduction

    @property
    def modus_ponens(self) -> InferenceRuleDeclaration:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P' ⊢ Q'.

        Abridged property: u.i.mp

        The implication (P ⟹ Q) may contain free-variables. If such is the
        case, the resulting Q' is computed by extracting variable-values
        from P' and applying variable-substitution.

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(p_implies_q: FormulaStatement,
                          p: FormulaStatement,
                          t: TheoryElaborationSequence) -> Formula:
            """

            :param args: A statement (P ⟹ Q), and a statement P
            :param t:
            :return: A formula Q
            """
            p_implies_q = unpack_formula(p_implies_q)
            # p_prime = unpack_formula(p_implies_q.parameters[0])
            q = unpack_formula(p_implies_q.parameters[1])
            # p_prime = unpack_formula(p_prime)  # Received as a statement-parameter to prove that p is true in t.
            return q  # TODO: Provide support for statements that are atomic propositional formula, that is
            # without relation or where the objct is a 0-ary relation.

        def verify_args(p_implies_q: FormulaStatement,
                        p: FormulaStatement, t: TheoryElaborationSequence) -> bool:
            """

            :param args: A statement (P ⟹ Q), and a statement P
            :param t:
            :return: A formula Q
            """
            verify(is_in_class(p_implies_q, classes.formula_statement),
                   '⌜p_implies_q⌝ is not a formula-statement.',
                   p_implies_q=p_implies_q, slf=self)
            verify(is_in_class(p, classes.formula_statement),
                   '⌜p⌝ is not a formula-statement.',
                   p=p, slf=self)
            verify(
                t.contains_theoretical_objct(p_implies_q),
                'Statement ⌜p_implies_q⌝ is not contained in theory ⌜t⌝''s hierarchy.',
                p_implies_q=p_implies_q, t=t, slf=self)
            p_implies_q = unpack_formula(p_implies_q)
            verify(
                p_implies_q.relation is t.u.r.implication,
                'The relation of formula ⌜p_implies_q⌝ is not an implication.',
                p_implies_q_relation=p_implies_q.relation, p_implies_q=p_implies_q, t=t, slf=self)
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                p_prime=p, t=t, slf=self)
            p = unpack_formula(p)
            p_prime = unpack_formula(p_implies_q.parameters[0])
            # The antecedant of the implication may contain free-variables,
            # store these in a mask for masked-formula-similitude comparison.
            verify(
                p.is_formula_equivalent_to(p_prime),
                'Formula ⌜p_prime⌝ in statement ⌜p_implies_q⌝ must be formula-equivalent to statement ⌜p⌝.',
                p_implies_q=p_implies_q, p=p, p_prime=p_prime, t=t,
                slf=self)
            return True

        if self._modus_ponens is None:
            self._modus_ponens = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('mp', index=None),
                title='modus ponens',
                dashed_name=DashedName('modus-ponens'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._modus_ponens

    @property
    def mp(self) -> InferenceRuleDeclaration:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P ⊢ Q.

        Unabridged property: u.i.modus_ponens

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.modus_ponens

    @property
    def equal_terms_substitution(self) -> InferenceRuleDeclaration:
        """The equal-terms-substitution inference-rule: P, Q=R ⊢ P' where:
         - P is an input statement,
         - Q=R is an equality statement,
         - P' is a new formula identical to P except that occurrences of Q in P
           are substituted with R.

        Abridged property: u.i.eqs

        The algorithm for formula substitution is:
        - canonical-order (top-down, depth-first, left-to-right)
        - replace all occurrences until end of formula is reached

        TODO: QUESTION: substitution_of_equal_terms: Should we forbid the presence of Q in R or R in Q?

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(p: FormulaStatement, q_equal_r: FormulaStatement,
                          t: TheoryElaborationSequence) -> Formula:
            """

            :param p: ⌜ P ⌝  a formula-statement.
            :param q_equal_r: a formula-statement of the form: (Q = R).
            :return: (FormulaStatement) A formula-statement P' where occurrences of Q are replaced with R.
            """
            p = unpack_formula(p)
            q_equal_r = unpack_formula(q_equal_r)
            q = q_equal_r.parameters[0]
            r = q_equal_r.parameters[1]
            substitution_map = {q: r}
            p_prime = p.substitute(
                substitution_map=substitution_map, target_theory=t,
                lock_variable_scope=True)
            return p_prime  # TODO: Provide support for statements that are atomic propositional formula, that is without relation or where the objct is a 0-ary relation.

        def verify_args(p: FormulaStatement, q_equal_r: FormulaStatement,
                        t: TheoryElaborationSequence) -> bool:
            verify(is_in_class(p, classes.formula_statement),
                   '⌜p⌝ is not of the formula-statement declarative-class.',
                   p=p, slf=self, t=t)
            verify(t.contains_theoretical_objct(p),
                   '⌜p⌝ is not contained in theoretical-elaboration-sequence ⌜t⌝.',
                   p=p, slf=self, t=t)
            verify(is_in_class(q_equal_r, classes.formula_statement),
                   '⌜q_equal_r⌝ is not of the formula-statement declarative-class.',
                   q_equal_r=q_equal_r, slf=self, t=t)
            verify(t.contains_theoretical_objct(q_equal_r),
                   '⌜q_equal_r⌝ is not contained in theoretical-elaboration-sequence ⌜t⌝.',
                   q_equal_r=q_equal_r, slf=self, t=t)
            q_equal_r = unpack_formula(q_equal_r)
            verify(q_equal_r.relation is self.u.r.equality,
                   'The root relation of ⌜q_equal_r⌝ is not the equality relation.',
                   q_equal_r=q_equal_r, slf=self, t=t)
            return True

        if self._equal_terms_substitution is None:
            self._equal_terms_substitution = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('ets', index=None),
                title='equal terms substitution',
                dashed_name=DashedName('equal-terms-substitution'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._equal_terms_substitution

    @property
    def ets(self) -> InferenceRuleDeclaration:
        """An inference-rule: P, Q=R ⊢ P' where:
         - P is an input statement,
         - Q=R is an equality statement,
         - P' is a new formula identical to P except that occurences of Q in P
           are substituted with R.

        Unabridged property: universe_of_discourse.inference_rules.equal_terms_substitution

        The algorithm for formula substitution is:
        - canonical-order (top-down, depth-first, left-to-right)
        - replace all occurrences until end of formula is reached

        TODO: QUESTION: substitution_of_equal_terms: Should we forbid the presence of Q in R or R in Q?

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.equal_terms_substitution

    @property
    def variable_substitution(self) -> InferenceRuleDeclaration:
        """An inference-rule: P, X→Y ⊢ P' where:
         - P is an input statement,
         - X→Y is a mapping between the free-variables in P and their substitution values,
         - P' is a new formula identical to P except that free-variables have been
           substituted according to the X→Y mapping.

        In practice, the mapping X→Y is implicit. A sequence Y' of substitution values
        is provided as an input, where substitution values are indexed by the canonical-order
        of their corresponding free-variables in the ordered set of free-variables in P.

        Abridged property: u.i.vs

        Formal definition:
        Given a statement P whose formula contains an ordered set
        of n free-variables, ordered by their canonical order of
        appearance in the formula,
        given an ordered set of theoretical-objcts O of cardinality n,
        the _variable substitution_ _inference rule_ returns a new
        statement P' where all occurrences of variables in P were
        replaced by their corresponding substitution values in O.

        Warning:
        To avoid inconsistent theories, one must be cautious
        with variable manipulations. In effect, the proposition:
            ((2n + 4) = 2(n + 2))
        may lead to inconsistencies following variable-substitution
        because the variable n is not typed. On the contrary:
            (n ∈ ℕ) ⟹ ((2n + 4) = 2(n + 2))
        where n is constrained leads to consistent results.

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        def infer_formula(p, *y_sequence, t: TheoryElaborationSequence) -> Formula:
            """

            :param args: ⌜ P ⌝  a statement, o1, o2, ... theoretical-objcts in canonical order.
            :param t:
            :return: A formula P'
            """
            x_oset = unpack_formula(p).get_variable_ordered_set()
            x_y_map = dict((x, y) for x, y in zip(x_oset, y_sequence))
            p_prime = p.valid_proposition.substitute(substitution_map=x_y_map, target_theory=t)
            return p_prime  # TODO: Provide support for statements that are atomic propositional formula, that is without relation or where the objct is a 0-ary relation.

        def verify_args(p: FormulaStatement, *y_sequence, t: TheoryElaborationSequence) -> bool:
            verify(t.contains_theoretical_objct(p),
                   '⌜p⌝ is not contained in theoretical-elaboration-sequence ⌜t⌝.',
                   p=p, y_sequence=y_sequence, slf=self, t=t)
            x_oset = unpack_formula(p).get_variable_ordered_set()
            verify(len(x_oset) == len(y_sequence),
                   'The cardinality of the canonically ordered free-variables.')
            # Substitution objects in Y must be declared in U,
            # but they may not be referenced yet in T's extension.
            for y in y_sequence:
                verify(y.u is self.u,
                       '⌜y⌝ and ⌜self⌝ do not share the same universe-of-discourse.',
                       y=y, y_u=y.u, slf=self, slf_u=self.u)
            return True

        if self._variable_substitution is None:
            self._variable_substitution = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                nameset=NameSet('vs', index=None),
                title='variable substitution',
                dashed_name=DashedName('variable-substitution'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._variable_substitution

    @property
    def vs(self) -> InferenceRuleDeclaration:
        """An inference-rule: P ⊢ P'

        Abridged property: u.i.vs

        Formal definition:
        Given a statement P whose formula contains an ordered set
        of n free-variables, ordered by their canonical order of
        appearance in the formula,
        given an ordered set of theoretical-objcts O of cardinality n,
        the _variable substitution_ _inference rule_ returns a new
        statement P' where all occurrences of variables in P were
        replaced by their corresponding substitution values in O.

        Warning:
        To avoid inconsistent theories, one must be cautious
        with variable manipulations. In effect, the proposition:
            ((2n + 4) = 2(n + 2))
        may lead to inconsistencies following variable-substitution
        because the variable n is not typed. On the contrary:
            (n ∈ ℕ) ⟹ ((2n + 4) = 2(n + 2))
        where n is constrained leads to consistent results.

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.variable_substitution


class InferenceRuleInclusionDict(collections.UserDict):
    """A dictionary that exposes well-known objects as properties.

    """

    def __init__(self, t: TheoryElaborationSequence):
        self.t = t
        super().__init__()
        # Well-known objects
        self._absorption = None
        self._axiom_interpretation = None
        self._biconditional_elimination_left = None
        self._biconditional_elimination_right = None
        self._biconditional_introduction = None
        self._conjunction_elimination_left = None
        self._conjunction_elimination_right = None
        self._conjunction_introduction = None
        self._definition_interpretation = None
        self._disjunction_elimination = None  # TODO: IMPLEMENT disjunction_elimination
        self._disjunction_introduction = None
        self._double_negation_elimination = None
        self._double_negation_introduction = None
        self._equality_commutativity = None
        self._equal_terms_substitution = None
        self._inconsistency_introduction = None
        self._modus_ponens = None
        self._variable_substitution = None

    @property
    def absorb(self) -> InferenceRuleInclusion:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Unabridged property: u.i.absorption

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.absorption

    @property
    def absorption(self) -> InferenceRuleInclusion:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Abridged property: u.i.absorb

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._absorption is None:
            self._absorption = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.absorption,
                title='absorption')
        return self._absorption

    @property
    def axiom_interpretation(self) -> InferenceRuleInclusion:
        """The axiom_interpretation inference-rule: 𝒜 ⊢ P.

               If the well-known inference-rule does not exist in the universe-of-discourse,
               the inference-rule is automatically declared.

               Warning
               -------
               Axiom-interpretation is especially dangerous because, contrary to most inference-rules,
               it allows the introduction of arbitrary truthes in the theory. For this reason,
               one must be very attentive when applying this inference-rule to assure the resulting
               formula-statement complies / interprets properly its related contentual-axiom.
               """
        if self._axiom_interpretation is None:
            self._axiom_interpretation = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.axiom_interpretation,
                title='axiom interpretation')
        return self._axiom_interpretation

    @property
    def bel(self) -> InferenceRuleInclusion:
        """The well-known biconditional-elimination (left) inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Unabridged property: u.i.biconditional_elimination_left

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_elimination_left

    @property
    def ber(self) -> InferenceRuleInclusion:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Unabridged property: u.i.biconditional_elimination_right

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_elimination_right

    @property
    def bi(self) -> InferenceRuleInclusion:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Unabridged property: u.i.biconditional_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_introduction

    @property
    def biconditional_elimination_left(self) -> InferenceRuleInclusion:
        """The well-known biconditional-elimination (left) inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Abridged property: u.i.bel

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._biconditional_elimination_left is None:
            self._biconditional_elimination_left = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.biconditional_elimination_left,
                title='biconditional elimination (left)')
        return self._biconditional_elimination_left

    @property
    def biconditional_elimination_right(self) -> InferenceRuleInclusion:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Abridged property: u.i.ber()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._biconditional_elimination_right is None:
            self._biconditional_elimination_right = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.biconditional_elimination_right,
                title='biconditional elimination (right)')
        return self._biconditional_elimination_right

    @property
    def biconditional_introduction(self) -> InferenceRuleInclusion:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Abridged property: u.i.bi

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._biconditional_introduction is None:
            self._biconditional_introduction = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.biconditional_introduction,
                title='biconditional introduction')
        return self._biconditional_introduction

    @property
    def conjunction_elimination_left(self) -> InferenceRuleInclusion:
        """The well-known conjunction-elimination (left) inference-rule: P ∧ Q ⊢ P.

        Abridged property: t.i.cel()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._conjunction_elimination_left is None:
            self._conjunction_elimination_left = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.conjunction_elimination_left,
                title='conjunction elimination (left)')
        return self._conjunction_elimination_left

    @property
    def conjunction_elimination_right(self) -> InferenceRuleInclusion:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        Abridged property: t.i.cer

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._conjunction_elimination_right is None:
            self._conjunction_elimination_right = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.conjunction_elimination_right,
                title='conjunction elimination (right)')
        return self._conjunction_elimination_right

    @property
    def conjunction_introduction(self) -> InferenceRuleInclusion:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Abridged property: t.i.ci()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._conjunction_introduction is None:
            self._conjunction_introduction = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.conjunction_introduction,
                title='conjunction introduction')
        return self._conjunction_introduction

    @property
    def cel(self) -> InferenceRuleInclusion:
        """The well-known conjunction-elimination (left) inference-rule: P ∧ Q ⊢ P.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_elimination_left()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.conjunction_elimination_left

    @property
    def cer(self) -> InferenceRuleInclusion:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_elimination_right()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.conjunction_elimination_right

    @property
    def ci(self) -> InferenceRuleInclusion:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_introduction()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.conjunction_introduction

    @property
    def definition_interpretation(self) -> InferenceRuleInclusion:
        """The definition_interpretation inference-rule: 𝒟 ⊢ (P = Q).

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.

        Warning
        -------
        Axiom-interpretation is especially dangerous because, contrary to most inference-rules,
        it allows the introduction of arbitrary truthes in the theory. For this reason,
        one must be very attentive when applying this inference-rule to assure the resulting
        formula-statement complies / interprets properly its related contentual-definition.
        """
        if self._definition_interpretation is None:
            self._definition_interpretation = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.definition_interpretation,
                title='definition interpretation')
        return self._definition_interpretation

    @property
    def di(self) -> InferenceRuleInclusion:
        """The well-known disjunction-introduction inference-rule: P ⊢ (P ∨ Q).

        Unabridged property: u.i.disjunction_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.disjunction_introduction

    @property
    def disjunction_introduction(self) -> InferenceRuleInclusion:
        """The well-known disjunction-introduction inference-rule: P ⊢ (P ∨ Q).

        Abridged property: u.i.di

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._disjunction_introduction is None:
            self._disjunction_introduction = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.disjunction_introduction,
                title='disjunction introduction')
        return self._disjunction_introduction

    @property
    def dne(self) -> InferenceRuleInclusion:
        """The well-known double-negation-elimination inference-rule: ¬¬P ⊢ P.

        Original method: universe_of_discourse.inference_rules.double_negation_elimination()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.double_negation_elimination

    @property
    def dni(self) -> InferenceRuleInclusion:
        """The well-known double-negation-introduction inference-rule: P ⊢ ¬¬P.

        Original method: universe_of_discourse.inference_rules.double_negation_introduction()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.double_negation_introduction

    @property
    def double_negation_elimination(self) -> InferenceRuleInclusion:
        """The well-known double-negation-elimination inference-rule: ¬¬P ⊢ P.

        Abridged property: t.i.dne()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._double_negation_elimination is None:
            self._double_negation_elimination = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.double_negation_elimination,
                title='double negation elimination')
        return self._double_negation_elimination

    @property
    def double_negation_introduction(self) -> InferenceRuleInclusion:
        """The well-known double-negation-introduction inference-rule: P ⊢ ¬¬P.

        Abridged property: t.i.dni

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._double_negation_introduction is None:
            self._double_negation_introduction = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.double_negation_introduction,
                title='double negation introduction')
        return self._double_negation_introduction

    @property
    def ec(self) -> InferenceRuleInclusion:
        """The equality-commutativity inference-rule: (P = Q) ⊢ (Q = P).

        Unabridged property: theory_elaboration_sequence.inference_rules.equality_commutativity

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.equality_commutativity

    @property
    def equality_commutativity(self) -> InferenceRuleInclusion:
        """The equality-commutativity inference-rule: (P = Q) ⊢ (Q = P).

        Abridged property: t.i.ec

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._equality_commutativity is None:
            self._equality_commutativity = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.equality_commutativity,
                title='equality commutativity')
        return self._equality_commutativity

    @property
    def equal_terms_substitution(self) -> InferenceRuleInclusion:
        """The equal-terms-substitution inference-rule: P, Q=R ⊢ P' where:
                 - P is an input statement,
                 - Q=R is an equality statement,
                 - P' is a new formula identical to P except that occurrences of Q in P
                   are substituted with R.

                Abridged property: u.i.eqs

                The algorithm for formula substitution is:
                - canonical-order (top-down, depth-first, left-to-right)
                - replace all occurrences until end of formula is reached

                TODO: QUESTION: substitution_of_equal_terms: Should we forbid the presence of Q in R or R in Q?

                If the inference-rule does not exist in the universe-of-discourse,
                the inference-rule is automatically declared.
                """
        if self._equal_terms_substitution is None:
            self._equal_terms_substitution = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.equal_terms_substitution,
                title='equal terms substitution')
        return self._equal_terms_substitution

    @property
    def ets(self) -> InferenceRuleInclusion:
        """The equal-terms-substitution inference-rule: P, Q=R ⊢ P' where:
                         - P is an input statement,
                         - Q=R is an equality statement,
                         - P' is a new formula identical to P except that occurrences of Q in P
                           are substituted with R.

                        Abridged property: u.i.eqs

                        The algorithm for formula substitution is:
                        - canonical-order (top-down, depth-first, left-to-right)
                        - replace all occurrences until end of formula is reached

                        TODO: QUESTION: substitution_of_equal_terms: Should we forbid the presence of Q in R or R in Q?

                        If the inference-rule does not exist in the universe-of-discourse,
                        the inference-rule is automatically declared.
                        """
        return self.equal_terms_substitution

    @property
    def inconsistency_introduction(self) -> InferenceRuleInclusion:
        """The inconsistency-introduction inference-rule: (P ∧ ¬P) ⊢ Inc(t).

                Abridged property: t.i.ii

                Inconsistency-introduction is an extraordinary inference-rule
                because it proves that the theory is inconsistent. It follows
                that the corresponding statement: ⌜Inc(t)⌝ becomes paradoxically
                invalid as soon as it is expressed in the current theory. In
                fact, ⌜Inc(t)⌝ should rather be understood as a meta-statement
                about the theory. In future versions of punctilious we will consider
                stating ⌜Inc(t)⌝ in a distinct meta-theory.

                Once ⌜Inc(t)⌝ is stated, the ⌜consistency⌝ property of the
                current theory is automatically changed to ⌜inconsistent⌝.

                If the inference-rule does not exist in the universe-of-discourse,
                the inference-rule is automatically declared.
                """
        if self._inconsistency_introduction is None:
            self._inconsistency_introduction = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.inconsistency_introduction,
                title='inconsistency introduction')
        return self._inconsistency_introduction

    @property
    def ii(self) -> InferenceRuleInclusion:
        """The inconsistency-introduction inference-rule: (P ∧ ¬P) ⊢ Inc(t).

                Unabridged property: theory_elaboration_sequence.inference_rules.inconsistency_introduction

                Inconsistency-introduction is an extraordinary inference-rule
                because it proves that the theory is inconsistent. It follows
                that the corresponding statement: ⌜Inc(t)⌝ becomes paradoxically
                invalid as soon as it is expressed in the current theory. In
                fact, ⌜Inc(t)⌝ should rather be understood as a meta-statement
                about the theory. In future versions of punctilious we will consider
                stating ⌜Inc(t)⌝ in a distinct meta-theory.

                Once ⌜Inc(t)⌝ is stated, the ⌜consistency⌝ property of the
                current theory is automatically changed to ⌜inconsistent⌝.

                If the inference-rule does not exist in the universe-of-discourse,
                the inference-rule is automatically declared.
                """
        return self.inconsistency_introduction

    @property
    def modus_ponens(self) -> InferenceRuleInclusion:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P ⊢ Q.

        Abridged property: u.i.mp

        The implication (P ⟹ Q) may contain free-variables. If such is the
        case, the resulting Q' is computed by extracting variable-values
        from P' and applying variable-substitution.


        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._modus_ponens is None:
            self._modus_ponens = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.modus_ponens,
                title='modus ponens')
        return self._modus_ponens

    @property
    def mp(self) -> InferenceRuleInclusion:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P ⊢ Q.

        Unabridged property: u.i.modus_ponens

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.modus_ponens

    @property
    def variable_substitution(self) -> InferenceRuleInclusion:
        """An inference-rule: P, X→Y ⊢ P' where:
         - P is an input statement,
         - X→Y is a mapping between the free-variables in P and their substitution values,
         - P' is a new formula identical to P except that free-variables have been
           substituted according to the X→Y mapping.

        In practice, the mapping X→Y is implicit. A sequence Y' of substitution values
        is provided as an input, where substitution values are indexed by the canonical-order
        of their corresponding free-variables in the ordered set of free-variables in P.

        Abridged property: u.i.vs

        Formal definition:
        Given a statement P whose formula contains an ordered set
        of n free-variables, ordered by their canonical order of
        appearance in the formula,
        given an ordered set of theoretical-objcts O of cardinality n,
        the _variable substitution_ _inference rule_ returns a new
        statement P' where all occurrences of variables in P were
        replaced by their corresponding substitution values in O.

        Warning:
        To avoid inconsistent theories, one must be cautious
        with variable manipulations. In effect, the proposition:
            ((2n + 4) = 2(n + 2))
        may lead to inconsistencies following variable-substitution
        because the variable n is not typed. On the contrary:
            (n ∈ ℕ) ⟹ ((2n + 4) = 2(n + 2))
        where n is constrained leads to consistent results.

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._variable_substitution is None:
            self._variable_substitution = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.variable_substitution,
                title='variable substitution')
        return self._variable_substitution

    @property
    def vs(self) -> InferenceRuleInclusion:
        """An inference-rule: P, X→Y ⊢ P' where:
         - P is an input statement,
         - X→Y is a mapping between the free-variables in P and their substitution values,
         - P' is a new formula identical to P except that free-variables have been
           substituted according to the X→Y mapping.

        In practice, the mapping X→Y is implicit. A sequence Y' of substitution values
        is provided as an input, where substitution values are indexed by the canonical-order
        of their corresponding free-variables in the ordered set of free-variables in P.

        Unabridged property: universe_of_discourse.inference_rules.variable_substitution

        Formal definition:
        Given a statement P whose formula contains an ordered set
        of n free-variables, ordered by their canonical order of
        appearance in the formula,
        given an ordered set of theoretical-objcts O of cardinality n,
        the _variable substitution_ _inference rule_ returns a new
        statement P' where all occurrences of variables in P were
        replaced by their corresponding substitution values in O.

        Warning:
        To avoid inconsistent theories, one must be cautious
        with variable manipulations. In effect, the proposition:
            ((2n + 4) = 2(n + 2))
        may lead to inconsistencies following variable-substitution
        because the variable n is not typed. On the contrary:
            (n ∈ ℕ) ⟹ ((2n + 4) = 2(n + 2))
        where n is constrained leads to consistent results.

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.variable_substitution


class UniverseOfDiscourse(SymbolicObject):
    def __init__(self, nameset: (None, str, NameSet) = None,
                 dashed_name: (None, str, DashedName) = None,
                 echo: (None, bool) = None):
        echo = get_config(echo, configuration.echo_universe_of_discourse_declaration,
                          configuration.echo_default,
                          fallback_value=False)
        self.axioms = dict()
        self.definitions = dict()
        self.formulae = dict()
        self._inference_rules = InferenceRuleDeclarationDict(u=self)
        self._relations = RelationDict(u=self)
        self.theories = dict()
        self._simple_objcts = SimpleObjctDict(u=self)
        self.symbolic_objcts = dict()
        self.theories = dict()
        # self.variables = dict()
        # Unique name indexes
        self.symbol_indexes = dict()
        self.titles = dict()
        self.dashed_names = dict()

        if nameset is None:
            symbol = StyledText(plaintext='U', text_style=text_styles.script_normal)
            index = index_universe_of_discourse_symbol(base=symbol)
            nameset = NameSet(symbol=symbol, index=index)
        elif isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            index = index_universe_of_discourse_symbol(base=nameset)
            nameset = NameSet(s=nameset, index=index)
        # if dashed_name is None:
        #    dashed_name = f'universe-of-discourse-{str(symbol.index)}'
        super().__init__(
            is_universe_of_discourse=True,
            is_theory_foundation_system=False,
            nameset=nameset,
            dashed_name=dashed_name,
            universe_of_discourse=None,
            echo=False)
        super()._declare_class_membership(classes.universe_of_discourse)
        if echo:
            self.echo()

    @property
    def i(self):
        """A python dictionary of inference-rules contained in this universe-of-discourse,
        where well-known inference-rules are directly available as properties."""
        return self.inference_rules

    @property
    def inference_rules(self):
        """A python dictionary of inference-rules contained in this universe-of-discourse,
        where well-known inference-rules are directly available as properties."""
        return self._inference_rules

    @property
    def r(self) -> RelationDict:
        """A python dictionary of relations contained in this universe-of-discourse,
        where well-known relations are directly available as properties."""
        return self.relations

    @property
    def relations(self) -> RelationDict:
        """A python dictionary of relations contained in this universe-of-discourse,
        where well-known relations are directly available as properties."""
        return self._relations

    def cross_reference_axiom(self, a: AxiomDeclaration) -> bool:
        """Cross-references an axiom in this universe-of-discourse.

        :param a: an axiom.
        """
        verify(
            a.nameset not in self.axioms.keys() or a is self.axioms[a.nameset],
            'The symbol of parameter ⌜a⌝ is already referenced as a distinct axiom in this universe-of-discourse.',
            a=a,
            universe_of_discourse=self)
        if a not in self.axioms:
            self.axioms[a.nameset] = a
            return True
        else:
            return False

    def cross_reference_definition(self, d: DefinitionDeclaration) -> bool:
        """Cross-references a definition in this universe-of-discourse.

        :param d: a definition.
        """
        verify(
            d.nameset not in self.definitions.keys() or d is self.definitions[d.nameset],
            'The symbol of parameter ⌜d⌝ is already referenced as a distinct definition in this universe-of-discourse.',
            a=d,
            universe_of_discourse=self)
        if d not in self.definitions:
            self.definitions[d.nameset] = d
            return True
        else:
            return False

    def cross_reference_formula(self, phi: Formula):
        """Cross-references a formula in this universe-of-discourse.

        :param phi: a formula.
        """
        verify(
            is_in_class(phi, classes.formula),
            'Cross-referencing a formula in a universe-of-discourse requires '
            'an object of type Formula.',
            phi=phi, slf=self)
        verify(
            phi.nameset not in self.formulae.keys() or phi is self.formulae[
                phi.nameset],
            'Cross-referencing a formula in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.',
            phi_symbol=phi.nameset, phi=phi, slf=self)
        if phi not in self.formulae:
            self.formulae[phi.nameset] = phi

    def cross_reference_inference_rule(self, ir: InferenceRuleDeclaration) -> bool:
        """Cross-references an inference-rule in this universe-of-discourse.

        :param ir: an inference-rule.
        """
        verify(
            is_in_class(ir, classes.inference_rule),
            'Parameter ⌜ir⌝ is not an inference-rule.',
            ir=ir,
            universe_of_discourse=self)
        verify(
            ir.nameset not in self.inference_rules.keys() or ir is self.inference_rules[ir.nameset],
            'The symbol of parameter ⌜ir⌝ is already referenced as a distinct inference-rule in this universe-of-discourse.',
            ir=ir,
            universe_of_discourse=self)
        if ir not in self.inference_rules:
            self.inference_rules[ir.nameset] = ir
            return True
        else:
            return False

    def cross_reference_relation(self, r: Relation):
        """Cross-references a relation in this universe-of-discourse.

        :param r: a relation.
        """
        verify(
            isinstance(r, Relation),
            'Cross-referencing a relation in a universe-of-discourse requires '
            'an object of type Relation.')
        verify(
            r.nameset not in self.relations.keys() or r is self.relations[
                r.nameset],
            'Cross-referencing a relation in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.',
            r_symbol=r.nameset, r=r, slf=self)
        if r not in self.relations:
            self.relations[r.nameset] = r

    def cross_reference_simple_objct(self, o: SimpleObjct):
        """Cross-references a simple-objct in this universe-of-discourse.

        :param o: a simple-objct.
        """
        verify(
            isinstance(o, SimpleObjct),
            'Cross-referencing a simple-objct in a universe-of-discourse requires '
            'an object of type SimpleObjct.')
        verify(
            o.nameset not in self.simple_objcts.keys() or o is
            self.simple_objcts[
                o.nameset],
            'Cross-referencing a simple-objct in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.',
            o_symbol=o.nameset, o=o, slf=self)
        if o not in self.simple_objcts:
            self.simple_objcts[o.nameset] = o

    def cross_reference_symbolic_objct(self, o: SymbolicObject):
        """Cross-references a symbolic-objct in this universe-of-discourse.

        :param o: a symbolic-objct.
        """
        verify(
            is_in_class(o, classes.symbolic_objct),
            'Cross-referencing a symbolic-objct in a universe-of-discourse requires '
            'an object of type SymbolicObjct.',
            o=o, slf=self)
        verify(
            o.nameset not in self.symbolic_objcts.keys() or o is
            self.symbolic_objcts[
                o.nameset],
            'Cross-referencing a symbolic-objct in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.',
            o_symbol=o.nameset, o=o, slf=self)
        if o not in self.symbolic_objcts:
            self.symbolic_objcts[o.nameset] = o

    def cross_reference_theory(self, t: TheoryElaborationSequence):
        """Cross-references a theory in this universe-of-discourse.

        :param t: a formula.
        """
        verify(
            is_in_class(t, classes.theory_elaboration),
            'Cross-referencing a theory in a universe-of-discourse requires '
            'an object of type Theory.',
            t=t, slf=self)
        verify(
            t.nameset not in self.theories.keys() or t is self.theories[
                t.nameset],
            'Cross-referencing a theory in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.',
            t_symbol=t.nameset, t=t, slf=self)
        if t not in self.theories:
            self.theories[t.nameset] = t

    def declare_formula(
            self, relation: Relation, *parameters, nameset: (None, str, NameSet) = None,
            lock_variable_scope: (None, bool) = None, echo: (None, bool) = None):
        """Declare a new :term:`formula` in this universe-of-discourse.

        This method is a shortcut for Formula(universe_of_discourse=self, ...).

        A formula is *declared* in a theory, and not *stated*, because it is not a statement,
        i.e. it is not necessarily true in this theory.
        """
        phi = Formula(
            relation=relation, parameters=parameters,
            universe_of_discourse=self, nameset=nameset,
            lock_variable_scope=lock_variable_scope,
            echo=echo
        )
        return phi

    def declare_free_variable(self, symbol=None, echo=None):
        """Declare a free-variable in this universe-of-discourse.

        A shortcut function for FreeVariable(universe_of_discourse=u, ...)

        :param symbol:
        :return:
        """
        x = FreeVariable(
            universe_of_discourse=self, nameset=symbol,
            status=FreeVariable.scope_initialization_status, echo=echo)
        return x

    def declare_symbolic_objct(
            self, symbol=None):
        """"""
        return SymbolicObject(
            nameset=symbol,
            universe_of_discourse=self)

    def declare_theory(
            self,
            nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            extended_theory: (None, TheoryElaborationSequence) = None,
            extended_theory_limit: (None, Statement) = None,
            stabilized: bool = False,
            echo: bool = None):
        """Declare a new theory in this universe-of-discourse.

        Shortcut for Theory(universe_of_discourse, ...).

        :param nameset:
        :param is_theory_foundation_system:
        :param extended_theory:
        :return:
        """
        return TheoryElaborationSequence(
            u=self,
            nameset=nameset,
            title=title,
            dashed_name=dashed_name,
            extended_theory=extended_theory,
            extended_theory_limit=extended_theory_limit,
            stabilized=stabilized,
            echo=echo)

    def declare_axiom(
            self, natural_language: str, title: (None, str, Title) = None,
            nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """Elaborate a new axiom 𝑎 in this universe-of-discourse."""
        return AxiomDeclaration(
            u=self, natural_language=natural_language, title=title, nameset=nameset, echo=echo)

    def take_note(
            self, t: TheoryElaborationSequence, content: str, nameset: (None, str, NameSet) = None,
            cat: (None, TitleCategory) = None, ref: (None, str) = None,
            subtitle: (None, str) = None,
            echo: (None, bool) = None):
        """Take a note, make a comment, or remark.

        Shortcut for Note(theory=t, ...)

        :param t:
        :param content:
        :param nameset:
        :param cat:
        :param ref:
        :param subtitle:
        :param echo:
        :return:
        """
        verify(
            t.universe_of_discourse is self,
            'This universe-of-discourse 𝑢₁ (self) is distinct from the universe-of-discourse 𝑢₂ of the theory '
            'parameter 𝑡.')
        return Note(theory=t, content=content, nameset=nameset,
                    cat=cat, ref=ref, subtitle=subtitle, echo=echo)

    def echo(self):
        return repm.prnt(self.rep_declaration())

    def f(
            self, relation: (Relation, FreeVariable), *parameters,
            nameset: (None, str, NameSet) = None,
            lock_variable_scope: (None, bool) = None,
            echo: (None, bool) = None):
        """Declare a new formula in this universe-of-discourse.

        Shortcut for self.elaborate_formula(...)."""
        return self.declare_formula(
            relation, *parameters, nameset=nameset,
            lock_variable_scope=lock_variable_scope, echo=echo)

    def get_symbol_max_index(self, base):
        """Return the highest index for that symbol-base in the universe-of-discourse."""
        if base in self.symbol_indexes.keys():
            return self.symbol_indexes[base]
        else:
            return 0

    def index_symbol(self, base: NameSet) -> int:
        """Given a symbol-base S (i.e. an unindexed symbol), returns a unique integer n
        such that (S, n) is a unique identifier in this instance of UniverseOfDiscourse.

        :param base: The symbol-base.
        :return:
        """
        if base not in self.symbol_indexes:
            self.symbol_indexes[base] = 1
        else:
            self.symbol_indexes[base] += 1
        return self.symbol_indexes[base]

    def declare_definition(
            self,
            natural_language: str,
            nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Pose a new definition in the current universe-of-discourse.

        Shortcut for: u.pose_definition(...)"""
        return DefinitionDeclaration(
            natural_language=natural_language,
            u=self,
            nameset=nameset, title=title, dashed_name=dashed_name, echo=echo)

    @property
    def simple_objcts(self) -> SimpleObjctDict:
        """The collection of simple-objcts in this universe-of-discourse.

        Abridged version: u.o

        Well-known simple-objcts are exposed as python properties. In general, a well-known simple-objct is declared in the universe-of-discourse the first time its property is accessed.

        :return:
        """
        return self._simple_objcts

    @property
    def o(self) -> SimpleObjctDict:
        """The collection of simple-objcts in this universe-of-discourse.

        Unabridged version: universe_of_discourse.simple_objcts

        Well-known simple-objcts are exposed as python properties. In general, a well-known simple-objct is declared in the universe-of-discourse the first time its property is accessed.

        :return:
        """
        return self.simple_objcts

    def rep_declaration(self) -> str:
        return f'Let {self.rep_fully_qualified_name()} be a universe-of-discourse.'

    def so(self, symbol=None):
        return self.declare_symbolic_objct(
            symbol=symbol)

    def t(
            self,
            nameset: (None, str, NameSet) = None,
            title: (None, str, Title) = None,
            dashed_name: (None, str, DashedName) = None,
            extended_theory: (None, TheoryElaborationSequence) = None,
            extended_theory_limit: (None, Statement) = None,
            stabilized: bool = False,
            echo: bool = None):
        """Declare a new theory in this universe-of-discourse.

        Shortcut for self.declare_theory(...).

        :param nameset:
        :param is_theory_foundation_system:
        :param extended_theory:
        :return:
        """
        return self.declare_theory(
            nameset=nameset,
            title=title,
            dashed_name=dashed_name,
            extended_theory=extended_theory,
            extended_theory_limit=extended_theory_limit,
            stabilized=stabilized,
            echo=echo)

    # @FreeVariableContext()
    @contextlib.contextmanager
    def v(
            self, symbol=None, echo=None):
        """Declare a free-variable in this universe-of-discourse.

        This method is expected to be as in a with statement,
        it yields an instance of FreeVariable,
        and automatically lock the variable scope when the with left.
        Example:
            with u.v('x') as x, u.v('y') as y:
                # some code...

        To manage variable scope extensions and locking expressly,
        use declare_free_variable() instead.
        """
        # return self.declare_free_variable(symbol=symbol)
        x = FreeVariable(
            universe_of_discourse=self, nameset=symbol,
            status=FreeVariable.scope_initialization_status, echo=echo)
        yield x
        x.lock_scope()


class InferredStatement(FormulaStatement):
    """A statement inferred from an inference-rule in the current theory-elaboration.
    """

    def __init__(
            self,
            *parameters,
            i: InferenceRuleDeclaration,  # TODO: DESIGN-FLAW: PASS InferenceRuleInclusion instead
            t: TheoryElaborationSequence,
            nameset: (None, str, NameSet) = None,
            ref: (None, str) = None,
            cat: (None, TitleCategory) = None,
            subtitle: (None, str) = None,
            echo: (None, bool) = None):
        """Include (aka allow) an inference_rule in a theory-elaboration.
        """
        echo = get_config(echo, configuration.echo_inferred_statement, configuration.echo_statement,
                          fallback_value=False)
        cat = title_categories.proposition if cat is None else cat
        # TODO: Check that cat is a valid statement cat (prop., lem., cor., theorem)
        title = Title(ref=ref, cat=cat, subtitle=subtitle)
        self._inference_rule = i
        self._parameters = tuple(parameters)
        verify(
            self._inference_rule.verify_args(*parameters, t=t),
            'Parameters ⌜*args⌝ are not compatible with inference-rule ⌜self⌝',
            args=parameters, slf=self, t=t)
        valid_proposition = self._inference_rule.infer_formula(*parameters, t=t)
        super().__init__(
            theory=t,
            valid_proposition=valid_proposition,
            nameset=nameset,
            category=cat,
            title=title,
            echo=False)
        # t.crossreference_inferred_proposition(self)
        super()._declare_class_membership(declarative_class_list.inferred_proposition)
        if self.inference_rule is self.t.u.i.inconsistency_introduction and \
                self.valid_proposition.relation is self.t.u.r.inconsistent and \
                self.valid_proposition.parameters[0] is self.t:
            # This inferred-statement proves the inconsistency
            # of the current theory-elaboration-sequence.
            t.report_inconsistency_proof(proof=self)
        if echo:
            self.echo()
        if self.inference_rule is self.t.u.i.axiom_interpretation or \
                self.inference_rule is self.t.u.i.definition_interpretation:
            t.assure_interpretation_disclaimer(echo=echo)

    def echo(self):
        repm.prnt(self.rep_report())

    @property
    def parameters(self) -> tuple:
        return self._parameters

    @property
    def inference_rule(self) -> InferenceRuleDeclaration:
        """Return the inference-rule upon which this inference-rule-inclusion is based.
        """
        return self._inference_rule

    def rep_report(self, text_format: (None, TextFormat) = None, output_proofs=True) -> str:
        """Return a representation that expresses and justifies the statement."""
        text_format = get_config(text_format, configuration.text_format,
                                 fallback_value=text_formats.plaintext)
        cap = True
        output = f'{self.rep_title(text_format=text_format, cap=cap)} ({self.rep_name(text_format=text_format)}): {self.valid_proposition.rep_formula()}'
        output = repm.wrap(output)
        if output_proofs:
            output = output + f'\n\tBy the {self.inference_rule.title.rep_mention(text_format=text_format)} inference-rule:'
            if self.inference_rule is self.u.inference_rules.variable_substitution:
                # This is a special case for the variable-substitution inference-rule,
                # which receives arbitrary theoretical-objcts as the 2nd and
                # following parameters, to constitute a free-variable mappings.
                parameter = self.parameters[0]
                output = output + f'\n\t{parameter.rep_formula(text_format=text_format, expand=True):<70} │ Follows from {repm.serif_bold(parameter.rep_ref(text_format=text_format))}.'
                # Display the free-variables mapping.
                free_variables = self.parameters[0].get_variable_ordered_set()
                mapping = zip(free_variables, self.parameters[1:])
                mapping_text = '(' + ','.join(
                    f'{k.rep_name()} ↦ {v.rep_formula()}' for k, v in mapping) + ')'
                output = output + f'\n\t{mapping_text:<70} │ Given as parameters.'
            else:
                for i in range(len(self.parameters)):
                    parameter = self.parameters[i]
                    output = output + f'\n\t{parameter.rep_formula(text_format=text_format, expand=True):<70} │ Follows from {repm.serif_bold(parameter.rep_ref(text_format=text_format))}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.rep_formula(text_format=text_format, expand=True):<70} │ ∎'
        return output


def apply_negation(phi: Formula) -> Formula:
    """Apply negation to a formula phi."""
    return phi.u.f(phi.u.r.lnot, phi.u.f(phi.u.r.lnot, phi))


def apply_double_negation(phi: Formula) -> Formula:
    """Apply double-negation to a formula phi."""
    return apply_negation(apply_negation(phi))


class InconsistencyIntroductionStatement(FormulaStatement):
    """

    Requirements:
    -------------

    """

    def __init__(
            self, p, not_p, nameset=None, category=None, theory=None,
            title=None):
        if title is None:
            title = 'THEORY INCONSISTENCY'
        category = title_categories.proposition if category is None else category
        self.p = p
        self.not_p = not_p
        valid_proposition = InconsistencyIntroductionInferenceRuleOBSOLETE.execute_algorithm(
            theory=theory, p=p, not_p=not_p)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            category=category, title=title,
            nameset=nameset)
        # The theory is proved inconsistent!
        theory.prove_inconsistent(self)
        if configuration.warn_on_inconsistency:
            warnings.warn(f'{self.rep_report(output_proofs=True)}', InconsistencyWarning)

    def rep_report(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.rep_title(cap=True)}: {self.valid_proposition.rep_formula()}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Proof of inconsistency")}'
            output = output + f'\n\t{self.p.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.p.rep_ref())}.'
            output = output + f'\n\t{self.not_p.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.not_p.rep_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.rep_formula(expand=True):<70} │ ∎'
        return output


class InconsistencyIntroductionInferenceRuleOBSOLETE(InferenceRuleOBSOLETE):
    """An implementation of the inconsistency-introduction inference-rule."""

    @staticmethod
    def infer(
            theory, p, not_p, symbol=None, category=None,
            title=None):
        """"""
        return InconsistencyIntroductionStatement(
            p=p, not_p=not_p, nameset=symbol,
            category=category, theory=theory, title=title)

    @staticmethod
    def execute_algorithm(theory, p, not_p):
        """Execute the theory-inconsistency algorithm."""
        assert isinstance(theory, TheoryElaborationSequence)
        assert isinstance(p, FormulaStatement)
        verify(
            theory.contains_theoretical_objct(p),
            'The p of the theory-inconsistency is not contained in the '
            'theory hierarchy.',
            conditional=p, theory=theory)
        verify(
            theory.contains_theoretical_objct(not_p),
            'The not-p of the theory-inconsistency is not contained in the '
            'theory hierarchy.',
            antecedent=not_p, theory=theory)
        verify(not_p.valid_proposition.relation is theory.universe_of_discourse.relations.negation,
               'The relation of not_p is not the negation relation.')
        not_p_prime = theory.universe_of_discourse.f(
            theory.universe_of_discourse.relations.negation, p.valid_proposition)
        verify(not_p_prime.is_formula_equivalent_to(not_p.valid_proposition),
               'not_p is not formula-equialent to ¬(P).',
               p=p, not_p=not_p, not_p_prime=not_p_prime)
        # Build q by variable substitution
        valid_proposition = theory.universe_of_discourse.f(
            theory.universe_of_discourse.relations.inconsistent, theory)
        return valid_proposition

    @staticmethod
    def initialize(theory):
        a1 = theory.a()
        # TODO: Justify the inclusion of this inference-rule in the theory.


pass
