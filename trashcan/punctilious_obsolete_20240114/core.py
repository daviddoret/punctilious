from __future__ import annotations
# import dataclasses
import collections.abc
import textwrap
import typing
import warnings
import punctilious.repm as repm
import contextlib
import abc
import collections
import pyvis
# import unidecode
import punctilious.unicode_utilities as unicode_utilities
from punctilious.plaintext import Plaintext
from punctilious.unicode_utilities import Unicode2
import itertools


# import punctilious_obsolete_20240114.caller_info as caller_info


def prioritize_value(*args):
    """Return the first non-None object in ⌜*args⌝."""
    for a in args:
        if a is not None:
            return a
    return None


class ErrorCode:
    def __init__(self, code, title):
        self.code = code
        self.title = title

    def __repr__(self):
        return f'Error #{self.code}: "{self.title}"'

    def __str__(self):
        return f'Error #{self.code}: "{self.title}"'


class ErrorCodes:

    def __init__(self):
        self.error_001_base_error = ErrorCode(1, 'Base error')
        self.error_002_inference_premise_syntax_error = ErrorCode(2, 'Inference premise syntax error')
        self.error_003_inference_premise_validity_error = ErrorCode(3, 'Inference premise validity error')
        self.error_004_inadequate_universe_parameter = ErrorCode(4, 'Inadequate universe-of-discourse parameter')
        """A parameter was passed to a python function requiring a universe-of-discourse (UniverseOfDiscourse), but None or an instance of a non-supported class was received."""
        self.error_005_inadequate_theory_parameter = ErrorCode(4, 'Inadequate theory-derivation parameter')
        """A parameter was passed to a python function requiring a theory-derivation (TheoryElaborationSequence), but None or an instance of a non-supported class was received."""


error_codes = ErrorCodes()


class PunctiliousException(Exception):

    def __init__(self, error_code: ErrorCode, msg: str, **kwargs):
        if error_code is None:
            error_code = error_codes.error_001_base_error
        msg = f'{msg}\nError code: {error_code.code}.'
        msg = f'{msg}\nError title: {error_code.title}.'
        self.msg = msg
        self.error_code = error_code
        self.kwargs = kwargs
        super().__init__(msg)


def rep_composition(composition: collections.abc.Generator[Composable, Composable, bool] = None,
    encoding: (None, bool) = None, cap: (None, bool) = None, **kwargs) -> str:
    encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
    if composition is None:
        return ''
    else:
        representation = ''
        for item in composition:
            if item is None:
                return ''
            elif isinstance(item, typing.Generator):
                representation = representation + rep_composition(composition=item, encoding=encoding, cap=cap,
                    **kwargs)
                cap = False
            elif isinstance(item, Composable):
                representation = representation + item.rep(encoding=encoding, cap=cap)
                cap = False
            elif isinstance(item, str):
                representation = representation + item
                cap = False
            elif isinstance(item, int):
                representation = representation + str(item)
                cap = False
            elif isinstance(item, CompoundFormula):
                representation = representation + item.rep_formula(encoding=encoding)
                cap = False
            else:
                raise TypeError(f'Type ⌜{str(type(item))}⌝ is not supported in compositions.')
        return representation


class Encoding:
    """A supported data text format."""

    def __init__(self, name: str):
        self._name = name

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((Encoding, self._name))

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name


class Encodings:
    def __init__(self):
        self.latex = Encoding('latex')
        self.plaintext = Encoding('plaintext')
        self.unicode = Encoding('unicode')


encodings = Encodings()


class Composable(abc.ABC):
    """An object that is Composable is an object that may participate in a representation
    composition and may be represented."""

    def __str__(self):
        return self.rep(encoding=encodings.plaintext)

    @abc.abstractmethod
    def compose(self) -> collections.abc.Generator[Composable, None, None]:
        raise NotImplementedError('This method is not implemented.')

    def rep(self, encoding: (None, Encoding) = None, **args) -> str:
        composition = ''
        for item in self.compose():
            composition += item.rep(encoding=encoding, **args)
        return composition


class ComposableText(Composable):
    """A text is a string of text that:
    - is of a supported text_style,
    - may support one or several encodings."""

    def __init__(self, s: (None, str) = None, plaintext: (None, str, Plaintext) = None,
        unicode: (None, str, Unicode2) = None, latex: (None, str) = None):
        """

        :param s: A default undetermined string. Leave it to the constructor to infer its
        encoding (plaintext, unicode, ...).
        :param plaintext:
        :param unicode:
        :param latex:
        """
        self._plaintext = Plaintext(prioritize_value(plaintext, s, unicode))
        self._unicode = Unicode2(prioritize_value(unicode, s))
        self._latex = latex

    def __eq__(self, other: (None, object, ComposableText)) -> bool:
        """Two instances of TextStyle are equal if any of their formatted representation are
        equal and not None."""
        return type(self) is type(
            other) and self.plaintext == other.plaintext and self.unicode == other.unicode_extended and self.latex == other.latex

    def __hash__(self):
        """Two styled-texts are considered distinct if either their plaintext content or their
        style are distinct."""
        return hash((ComposableText, self._plaintext, self._unicode, self._latex))

    def __repr__(self):
        return f'⌜{self.rep(encoding=encodings.plaintext)}⌝'

    def compose(self) -> collections.abc.Generator[Composable, None, None]:
        yield self

    @property
    def latex(self) -> (None, str):
        return self._latex

    @property
    def plaintext(self) -> (None, Plaintext):
        return self._plaintext

    def rep(self, encoding: Encoding = encodings.plaintext, cap: bool = False):
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        match encoding:
            case encodings.plaintext:
                return self.rep_as_plaintext(cap=cap)
            case encodings.latex:
                return self.rep_as_latexmath(cap=cap)
            case encodings.unicode:
                return self.rep_as_unicode(cap=cap)
            case _:
                return self.rep_as_plaintext(cap=cap)

    def rep_as_latexmath(self, cap: bool = False):
        content = self._plaintext if self._latex is None else self._latex
        content = content.capitalize() if cap else content
        return content

    def rep_as_plaintext(self, cap: bool = False):
        content = self._plaintext
        content = content.capitalize() if cap else content
        return content

    def rep_as_unicode(self, cap: bool = False):
        content = self._plaintext if self._unicode is None else self._unicode
        content = content.capitalize() if cap else content
        return content

    @property
    def unicode(self) -> (None, Unicode2):
        return self._unicode


def yield_composition(*content, cap: (None, bool) = None, pre: (None, str, Composable) = None,
    post: (None, str, Composable) = None) -> collections.abc.Generator[Composable, Composable, bool]:
    """A utility function that simplifies yielding compositions.

    Only yield elements that are not None.
    Yield ⌜pre⌝ if there is at least one non-None element in ⌜*content⌝.
    Yield all elements of ⌜*content⌝.
    Yield ⌜post⌝ if there is at least one non-None element in ⌜*content⌝.
    """
    if content is not None and any(element is not None for element in content):
        yield from yield_composition(pre)
        for element in content:
            if isinstance(element, str):
                yield from ComposableText(s=element).compose()
            elif isinstance(element, StyledText):
                yield from element.compose(cap=cap)
            elif isinstance(element, Composable):
                yield from element.compose()
            elif isinstance(element, collections.abc.Generator):
                yield from element
            else:
                raise TypeError(f'Type ⌜{str(type(element))}⌝ is not supported.')
        yield from yield_composition(post)
        return True
    else:
        return False


def prioritize_composition(*content, cap: (None, bool) = None, pre: (None, str, Composable) = None,
    post: (None, str, Composable) = None) -> collections.abc.Generator[Composable, Composable, bool]:
    """Yield the composition of the first non-None element of *content.
    """
    if content is None:
        return False
    first_not_none = next((element for element in content if element is not None), None)
    something = yield from yield_composition(first_not_none, cap=cap, pre=pre, post=post)
    return something


class TextStyle:
    """A supported text style."""

    def __init__(self, name: str, start_tag: ComposableText, end_tag: ComposableText, unicode_map: dict = None,
        unicode_table_index: int = None):
        # TODO: Replace unicode_table_index with new parameter unicode_map,
        # this will allow to dedicate maps and better manage incomplete character sets,
        # such as subscript.
        self._name = name
        self._unicode_table_index = unicode_table_index
        self._unicode_map = unicode_map
        self._start_tag = start_tag
        self._end_tag = end_tag

    def __eq__(self, other):
        return type(other) is type(self) and hash(self) == hash(other)

    def __hash__(self):
        return hash((TextStyle, self._name))

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def end_tag(self):
        return self._end_tag

    @property
    def name(self):
        return self._name

    @property
    def start_tag(self):
        return self._start_tag

    @property
    def unicode_map(self):
        return self._unicode_map


class TextStyles:
    """Expose a catalog of supported text-styles."""

    def __init__(self):
        self._no_style = TextStyle(name='no-style',
            unicode_table_index=unicode_utilities.unicode_sans_serif_normal_index,
            start_tag=ComposableText(plaintext=''), end_tag=ComposableText(plaintext=''))
        self.double_struck = TextStyle(name='double-struck',
            unicode_table_index=unicode_utilities.unicode_double_struck_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathbb{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.fraktur_normal = TextStyle(name='fraktur-normal',
            unicode_table_index=unicode_utilities.unicode_fraktur_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathfrak{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.monospace = TextStyle(name='monospace', unicode_table_index=unicode_utilities.unicode_monospace_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathtt{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.sans_serif_bold = TextStyle(name='sans-serif-bold',
            unicode_table_index=unicode_utilities.unicode_sans_serif_bold_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\boldsymbol\\mathsf{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}}'))
        self.sans_serif_italic = TextStyle(name='sans-serif-italic',
            unicode_table_index=unicode_utilities.unicode_sans_serif_italic_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\text{\\sffamily{\\itshape{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}}}'))
        self.sans_serif_normal = TextStyle(name='sans-serif-normal',
            unicode_table_index=unicode_utilities.unicode_sans_serif_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathsf{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.script_normal = TextStyle(name='script-normal',
            unicode_table_index=unicode_utilities.unicode_script_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathcal{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.script_bold = TextStyle(name='script-bold',
            unicode_table_index=unicode_utilities.unicode_script_bold_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathcal{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.serif_bold = TextStyle(name='serif-bold', unicode_table_index=unicode_utilities.unicode_serif_bold_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathbf{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.serif_bold_italic = TextStyle(name='serif-bold-italic',
            unicode_table_index=unicode_utilities.unicode_serif_bold_italic_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathbold{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.serif_italic = TextStyle(name='serif-italic',
            unicode_table_index=unicode_utilities.unicode_serif_italic_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathit{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.serif_normal = TextStyle(name='serif-normal',
            unicode_table_index=unicode_utilities.unicode_serif_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathnormal{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.subscript = TextStyle(name='subscript', unicode_map=unicode_utilities.unicode_subscript_dictionary,
            start_tag=ComposableText(plaintext='_', unicode='', latex='_{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))

    @property
    def no_style(self):
        """The ⌜no_style⌝ text-style is a neutral style.
        Rendering defaults to sans-serif-normal.
        It is expected to be overriden by passing the text_style parameter to the rendering
        method."""
        return self._no_style


text_styles = TextStyles()


class TextDict:
    """Predefined texts are exposed in the TextDict. This should facilite internatiolization at a
    later stage.
    TODO: Merge this into the Locale.
    """

    def __init__(self):
        self.comma = ComposableText(plaintext=', ')
        self.empty_string = ComposableText(plaintext='')
        self.in2 = None
        self.let = None
        self.be = None
        self.be_a = None
        self.be_an = None
        self.colon = ComposableText(plaintext=':')
        self.period = ComposableText(plaintext='.')
        self.space = ComposableText(plaintext=' ')
        self.close_quasi_quote = ComposableText(plaintext='"', unicode='⌝', latex='\\right\\ulcorner')
        self.open_quasi_quote = ComposableText(plaintext='"', unicode='⌜', latex='\\left\\ulcorner')
        self.close_parenthesis = ComposableText(plaintext=')', latex='\\right)')
        self.open_parenthesis = ComposableText(plaintext='(', latex='\\left(')
        self.compound_formula_term_separator = ComposableText(plaintext=', ')
        self.the = None


text_dict = TextDict()


class ComposableBlock(Composable, abc.ABC):
    """A CompositionBlock is a composition that has a start_tag and an end_tag."""

    def __init__(self, start_tag: (None, ComposableText) = None, end_tag: (None, ComposableText) = None):
        self._start_tag = start_tag
        self._end_tag = end_tag

    def __repr__(self):
        return self.rep(encoding=encodings.plaintext)

    def __str__(self):
        return self.rep(encoding=encodings.plaintext)

    @abc.abstractmethod
    def compose(self) -> collections.abc.Generator[Composable, None, None]:
        raise NotImplementedError('This method is not implemented.')

    @property
    def end_tag(self):
        return self._end_tag

    def rep(self, encoding: (None, Encoding) = None, wrap: (None, bool) = None, **args) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        # Implement parameter wrap
        # wrap = get_config(wrap, configuration.wrap,
        #                  False)
        return ''.join(item.rep(encoding=encoding) for item in self.outer_composition)

    @property
    def start_tag(self):
        return self._start_tag


empty_string = ComposableText(plaintext='')


def composify(item: (None, str, int, ComposableText, ComposableBlock)) -> Composable:
    """Force conversion of item to Composable type."""
    if item is None:
        return ComposableText(s='')
    elif isinstance(item, str):
        return ComposableText(s=item)
    elif isinstance(item, int):
        return ComposableText(s=str(item))
    elif isinstance(item, Composable):
        return item
    else:
        raise TypeError('item is of unsupported type.')


class ComposableBlockLeaf(ComposableBlock):
    """An instance of CompositionLeafBlock is a composition string that start with a
    start-element, that contains a single leaf-element, and that ends with an end-element.
    """

    def __init__(self, content: (None, ComposableText) = None, start_tag: (None, ComposableText) = None,
        end_tag: (None, ComposableText) = None):
        self._content = composify(content)
        super().__init__(start_tag=start_tag, end_tag=end_tag)

    def compose(self) -> collections.abc.Generator[Composable, None, None]:
        if self._start_tag is not None:
            yield self._start_tag
        yield self._content
        if self._end_tag is not None:
            yield self._end_tag

    @property
    def content(self) -> Composable:
        return self._content

    @content.setter
    def content(self, content: (None, Composable)) -> None:
        self._content = content


class StyledText(ComposableBlockLeaf):
    """Text supporting multiple encodings (plaintext, Unicode, LaTeX math) and styles."""

    def __init__(self, s: (None, str) = None, text_style: (None, TextStyle) = None,
        plaintext: (None, str, Plaintext) = None, unicode: (None, str, Unicode2) = None, latex: (None, str) = None,
        cap: (None, bool) = None):
        """

        :param s: A string. Leave it to the constructor to interpret if it is plaintext or unicode.
        :param plaintext:
        :param unicode:
        :param latex:
        :param text_style:
        """
        self._text_style = prioritize_value(text_style, text_styles.sans_serif_normal)
        self._cap = prioritize_value(cap, False)
        if self._cap:
            # Forces capitalization of the first letter during construction.
            s = s if s is None else s.capitalize()
            plaintext = plaintext if plaintext is None else plaintext.capitalize()
            unicode = unicode if unicode is None else unicode.capitalize()
            latex = latex if latex is None else latex.capitalize()
        content = ComposableText(s=s, plaintext=plaintext, unicode=unicode, latex=latex)
        start_tag = self._text_style.start_tag
        end_tag = self._text_style.end_tag
        super().__init__(content=content, start_tag=start_tag, end_tag=end_tag)
        self._text_content = content

    def __eq__(self, other: (None, object, ComposableText)) -> bool:
        """Two instances of TextStyle are equal if any of their styled representation are equal
        and not None."""
        return type(self) is type(other) and self._content == other.content and self._text_style is other.text_style

    def __hash__(self):
        """Two styled-texts are considered distinct if either their plaintext content or their
        style are distinct."""
        return hash((ComposableText, self._content, self._text_style))

    def __repr__(self):
        return f'⌜{self.rep(encoding=encodings.plaintext)}⌝ [{self._text_style}]'

    def compose(self, text_style: (None, TextStyle) = None, cap: (None, bool) = None, **kwargs) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        """

        :param text_style: Override the text_style property of the StyledText instance.
        :param cap: Override the cap property of the StyledText instance.
        :param kwargs:
        :return: A composition of the StyledText instance.
        """
        if (cap is not None and cap != self._cap) or (text_style is not None and self._text_style is not text_style):
            # Return a close of ⌜self⌝ with the desired properties.
            # TODO: StyledText composition: possible bug in LaTeX rendering here.
            latex = None if self.latex is None else (self.latex.capitalize() if cap else self.latex)
            plaintext = None if self.plaintext is None else (self.plaintext.capitalize() if cap else self.plaintext)
            unicode = None if self.unicode is None else (self.unicode.capitalize() if cap else self.unicode)
            yield StyledText(latex=latex, plaintext=plaintext, unicode=unicode, text_style=self.text_style)
            return True
        else:
            yield self
            return True

    @property
    def latex(self) -> (None, str):
        return self._text_content.latex

    @property
    def plaintext(self) -> (None, Plaintext):
        return self._text_content.plaintext

    @property
    def unicode(self) -> (None, str):
        return self._text_content.unicode

    def rep(self, encoding: Encoding = encodings.plaintext, cap: bool = False, **kwargs):
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        match encoding:
            case encodings.plaintext:
                return self.rep_as_plaintext(cap=cap)
            case encodings.latex:
                return self.rep_as_latex(cap=cap)
            case encodings.unicode:
                return self.rep_as_unicode(cap=cap)
            case _:
                return self.rep_as_plaintext(cap=cap)

    def rep_as_latex(self, cap: bool = False):
        start_tag = self.start_tag.rep(encoding=encodings.latex)
        content = self._text_content.plaintext if self._text_content.latex is None else self._text_content.latex
        content = content.capitalize() if cap else content
        end_tag = self.end_tag.rep(encoding=encodings.latex)
        return start_tag + content + end_tag

    def rep_as_plaintext(self, cap: bool = False):
        content = self._text_content.plaintext
        content = content.capitalize() if cap else content
        return content

    def rep_as_unicode(self, cap: bool = False):
        content = self._text_content.plaintext if self._text_content.unicode is None else self._text_content.unicode
        content = content.capitalize() if cap else content
        return unicode_utilities.unicode_format(s=content, index=self.text_style._unicode_table_index,
            mapping=self.text_style.unicode_map)

    @property
    def text_content(self) -> ComposableText:
        return self._text_content

    @property
    def text_style(self) -> TextStyle:
        return self._text_style


class ComposableBlockSequence(ComposableBlock):
    """An instance of CompositionSequence is a composite string of representation that contains a
    sequence of composable elements.
    """

    def __init__(self, content: (None, list[ComposableBlock, ComposableText]) = None,
        start_tag: (None, ComposableText) = None, end_tag: (None, ComposableText) = None):
        self._content = list() if content is None else content
        super().__init__(start_tag=start_tag, end_tag=end_tag)

    def append(self, item: (None, ComposableText, ComposableBlock)) -> None:
        if item is not None:
            self._content.append(item)

    def compose(self) -> collections.abc.Generator[Composable, None, None]:
        """Yields the elements of the representable string, flattening all content."""
        if self._start_tag is not None:
            yield self._start_tag
        if self._content is not None:
            for sub_element in self._content:
                if isinstance(sub_element, ComposableBlock):
                    # Call the sub-generator
                    yield from sub_element.compose()
                else:
                    # This is a leaf (non-composable) element
                    yield sub_element
        if self._end_tag is not None:
            yield self._end_tag

    @property
    def content(self) -> (None, list):
        return self._content

    @content.setter
    def content(self, content: (None, list)) -> None:
        self._content = content

    def extend(self, iterable: (None, collections.abc.Iterable)):
        if iterable is not None:
            self.append(self.prepare_item(item) for item in iterable)

    def rep(self, encoding: (None, Encoding) = None, **kwargs) -> str:
        return rep_composition(self.compose(), encoding=encoding, **kwargs)


class QuasiQuotation(ComposableBlockSequence):
    """As a convention in Punctilious, quasi quotes are used to denote natural language.

    """

    def __init__(self, iterable: (None, collections.Iterable) = None) -> None:
        super().__init__(content=iterable, start_tag=QuasiQuotation._static_start_tag,
            end_tag=QuasiQuotation._static_end_tag)

    _static_end_tag = ComposableText(plaintext='"', unicode='⌝')

    _static_start_tag = ComposableText(plaintext='"', unicode='⌜')


class ParentheticalExpression(ComposableBlockSequence):
    """A parenthetical-expression is the representation of a formula or sub-formula where the
    content is included between an opening and closing parenthesis.

    """

    def __init__(self, iterable: (None, collections.Iterable) = None) -> None:
        super().__init__(content=iterable, start_tag=QuasiQuotation._static_start_tag,
            end_tag=QuasiQuotation._static_end_tag)

    _static_end_tag = ComposableText(plaintext=')', latex='\\right)')

    _static_start_tag = ComposableText(plaintext='(', unicode='\\left(')


class Paragraph(ComposableBlockSequence):
    def __init__(self, iterable: (None, collections.Iterable) = None) -> None:
        super().__init__(content=iterable, start_tag=Paragraph._static_start_tag, end_tag=Paragraph._static_end_tag)

    _static_end_tag = ComposableText(plaintext='\n\n', unicode='\n\n')

    _static_start_tag = ComposableText(plaintext='', unicode='')


class Index(ComposableBlockSequence):
    def __init__(self, iterable: (None, collections.Iterable) = None) -> None:
        super().__init__(iterable=iterable, start_tag=Paragraph._static_start_tag, end_tag=Paragraph._static_end_tag)

    _static_end_tag = ComposableText(latex='}', plaintext='', unicode='')

    _static_start_tag = ComposableText(latex='_{', plaintext='_', unicode='')

    def prepare_item(self, item: (None, str, int, ComposableText)) -> ComposableText:
        """Force conversion of item to StyledText to assure the internal consistency of the
        TextComposition."""
        if item is None:
            return text_dict.empty_string
        elif isinstance(item, str):
            if item == '':
                return text_dict.empty_string
            else:
                return ComposableText(plaintext=item, unicode=unicode_utilities.unicode_subscriptify(s=item))
        elif isinstance(item, ComposableText):
            return item
        else:
            raise TypeError('item is of unsupported type.')

    @property
    def content(self) -> StyledText:
        return self._content

    def rep(self, encoding: (None, Encoding) = None, **kwargs):
        return self.content.rep(encoding=encoding, cap=True)


class SansSerifBold(StyledText):
    def __init__(self, s: (str, None) = None, plaintext: (None, str, Plaintext) = None,
        unicode: (None, str, Unicode2) = None, latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.sans_serif_bold, plaintext=plaintext, unicode=unicode, latex=latex)


class Header(ComposableBlockSequence):
    def __init__(self, s: (str, None) = None, plaintext: (None, str, Plaintext) = None,
        unicode: (None, str, Unicode2) = None, latex: (None, str) = None, level: (None, int) = None) -> None:
        content = SansSerifBold(s=s, plaintext=plaintext, unicode=unicode, latex=latex)
        level = prioritize_value(level, 1)
        verify(assertion=0 < level < 4, msg='level is only supported between 1 and 3 inclusive.')
        self._level = level
        start_tag = None
        end_tag = None
        if level == 1:
            start_tag = ComposableText(plaintext='\n# ', unicode='\n# ', latex='\\section{')
            end_tag = ComposableText(plaintext='\n', unicode='\n', latex='}')
        elif level == 2:
            start_tag = ComposableText(plaintext='\n## ', unicode='\n## ', latex='\\subsection{')
            end_tag = ComposableText(plaintext='\n', unicode='\n', latex='}')
        elif level == 3:
            start_tag = ComposableText(plaintext='\n### ', unicode='\n### ', latex='\\subsubsection{')
            end_tag = ComposableText(plaintext='\n', unicode='\n', latex='}')
        super().__init__(content=[content], start_tag=start_tag, end_tag=end_tag)

    @property
    def level(self) -> int:
        return self.level


class SansSerifNormal(StyledText):
    def __init__(self, s: (str, None) = None, plaintext: (None, str, Plaintext) = None,
        unicode: (None, str, Unicode2) = None, latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.sans_serif_normal, plaintext=plaintext, unicode=unicode,
            latex=latex)


class SansSerifItalic(StyledText):
    def __init__(self, s: (str, None) = None, plaintext: (None, str, Plaintext) = None,
        unicode: (None, str, Unicode2) = None, latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.sans_serif_italic, plaintext=plaintext, unicode=unicode,
            latex=latex)


text_dict.in2 = SansSerifNormal(s='in')
text_dict.let = SansSerifNormal(s='let')
text_dict.be = SansSerifNormal(s='be')
text_dict.be_a = SansSerifNormal(s='be a')
text_dict.be_an = SansSerifNormal(s='be an')
text_dict.the = SansSerifNormal(s='the')


class ScriptNormal(StyledText):
    def __init__(self, plaintext: str, unicode: (None, str) = None, latex: (None, str) = None) -> None:
        super().__init__(text_style=text_styles.script_normal, plaintext=plaintext, unicode=unicode, latex=latex)


class SerifBoldItalic(StyledText):
    def __init__(self, s: (None, str) = None, plaintext: (None, str) = None, unicode: (None, str) = None,
        latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.serif_bold_italic, plaintext=plaintext, unicode=unicode,
            latex=latex)


class SerifItalic(StyledText):
    def __init__(self, s: (None, str) = None, plaintext: (None, str) = None, unicode: (None, str) = None,
        latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.serif_italic, plaintext=plaintext, unicode=unicode, latex=latex)


class SerifNormal(StyledText):
    def __init__(self, plaintext: str, unicode: (None, str) = None, latex: (None, str) = None) -> None:
        super().__init__(text_style=text_styles.serif_normal, plaintext=plaintext, unicode=unicode, latex=latex)


class Subscript(StyledText):
    def __init__(self, plaintext: str, unicode: (None, str) = None, latex: (None, str) = None) -> None:
        super().__init__(text_style=text_styles.subscript, plaintext=plaintext, unicode=unicode, latex=latex)


def wrap_text(text):
    """Wrap text for friendly rendering as text, e.g. in a console.

    :param text:
    :return:
    """
    return '\n'.join(textwrap.wrap(text=text, width=configuration.text_output_total_width, subsequent_indent=f'\t',
        break_on_hyphens=False, expand_tabs=True, tabsize=4))


class ProofFormat(repm.ValueName):
    pass


class ProofFormats(repm.ValueName):
    """A catalog of supported proof presentation formats."""

    def __init__(self, value_name: str) -> None:
        super().__init__(value_name=value_name)
        self._flow_chart_proof = ProofFormat('flow chart proof')
        self._formal_proof = ProofFormat('formal proof')
        self._paragraph_proof = ProofFormat('paragraph proof')
        self._two_column_proof = ProofFormat('two column proof')

    @property
    def flow_chart_proof(self) -> ProofFormat:
        return self._flow_chart_proof

    @property
    def formal_proof(self) -> ProofFormat:
        return self._formal_proof

    @property
    def paragraph_proof(self) -> ProofFormat:
        return self._paragraph_proof

    @property
    def two_column_proof(self) -> ProofFormat:
        return self._two_column_proof


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
        """A shortened representation composed as a subset of the name characters, e.g.: ⌜qed⌝,
        ⌜max⌝,⌜mp⌝."""
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
"""The catalog of the supported types of names / symbolic representations used to identify 
objects."""


def equal_not_none(s1: (None, str), s2: (None, str)):
    """Compare 2 strings are return if they are equal, unless either or both are None."""
    return False if s1 is None or s2 is None else s1 == s2


def subscriptify(text: (str, ComposableText) = '', encoding: Encoding = encodings.plaintext):
    encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
    if text is None:
        return ''
    match encoding:
        case encodings.plaintext:
            return text
        case encodings.unicode:
            if isinstance(text, ComposableText):
                # The Unicode set of subscript characters is very limited,
                # subscriptification must be executed on the plaintext value
                # of the Unicode string.
                text = text.rep_as_plaintext()
            return unicode_utilities.unicode_subscriptify(text)
        case encodings.latex:
            return f'_{{{text}}}'
        case _:
            return text


class Locale:
    def __init__(self, name: str):
        self._name = name
        self._paragraph_end = None
        self._paragraph_start = None
        self._qed = None

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @property
    @abc.abstractmethod
    def paragraph_end(self) -> StyledText:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def paragraph_start(self) -> StyledText:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def qed(self) -> StyledText:
        raise NotImplementedError()


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


def verify(assertion: bool, msg: str, severity: VerificationSeverity = verification_severities.error,
    raise_exception: bool = True, error_code: (None, ErrorCode) = None, **kwargs) -> tuple[bool, (None, str)]:
    if not assertion:
        contextual_information = ''
        for key, value in kwargs.items():
            value_as_string = f'(str conversion failure of type {str(type(value))})'
            if value is None:
                value = 'None'
            else:
                try:
                    value_as_string = str(value)
                finally:
                    pass
            contextual_information += f'\n  {key}: {value_as_string}'
        report = f'\n\nMessage:\n{msg}\n\nContextual information:{contextual_information}\n\nSeverity: {str(severity).upper()}'
        # repm.prnt(report)
        if severity is verification_severities.warning:
            raise Exception("oops")
            warnings.warn(report)
        raise_exception = prioritize_value(raise_exception, configuration.raise_exception_on_verification_error, True)
        if severity is verification_severities.error:
            if raise_exception:
                raise PunctiliousException(error_code=error_code, msg=report, **kwargs)
            else:
                return False, report
    else:
        return True, None


class InconsistencyWarning(UserWarning):
    pass


class Configuration:
    """Configuration settings.

    This class allows the storage of all punctilious_obsolete_20240114 configuration and preference settings.

    """

    def __init__(self):
        self.echo_inference_rule_declaration = None
        self.default_inference_rule_symbol = None
        self.auto_index = None
        self.default_axiom_declaration_symbol = None
        self.default_axiom_inclusion_symbol = None
        self.default_constant_symbol = None
        self.default_definition_declaration_symbol = None
        self.default_definition_inclusion_symbol = None
        self.default_formula_symbol = None
        self.default_variable_symbol = None
        self.default_parent_hypothesis_statement_symbol = None
        self.default_child_hypothesis_theory_symbol = None
        self.default_inference_rule_declaration_symbol = None
        self.default_inference_rule_inclusion_symbol = None
        self.default_note_symbol = None
        self.default_connective_symbol = None
        self.default_statement_symbol = None
        self.default_symbolic_object_symbol = None
        self.default_theory_symbol = None
        self.echo_axiom_declaration = None
        self.echo_axiom_inclusion = None
        self._echo_default = None
        self.echo_definition_declaration = None
        self.echo_definition_inclusion = None
        self.echo_definition_direct_inference = None
        self.echo_formula_declaration = None
        self.echo_hypothesis = None
        self.echo_inferred_statement = None
        self.echo_note = None
        self.echo_connective = None
        self.echo_simple_objct_declaration = None
        self.echo_statement = None
        self.echo_proof = None
        self.echo_symbolic_objct = None
        self.echo_theory_derivation_declaration = None
        self.echo_universe_of_discourse_declaration = None
        self.echo_variable_declaration = None
        self.echo_encoding = None
        self.locale = None
        self.output_index_if_max_index_equal_1 = None
        self.raise_exception_on_verification_error = None
        self.title_text_style = None
        self.encoding = None
        self.text_output_indent = None
        self.two_columns_proof_left_column_width = None
        self.two_columns_proof_right_column_width = None
        self.text_output_total_width = None
        self.warn_on_inconsistency = None

    @property
    def echo_default(self) -> (None, bool):
        return self._echo_default

    @echo_default.setter
    def echo_default(self, value: (None, bool)):
        self._echo_default = value


configuration = Configuration()


class PyvisConfiguration:
    """pyvis theory is used to build graphs as interactive HTML pages.
    This class stores the corresponding configuration settings."""

    def __init__(self):
        self.axiom_inclusion_args = {'shape': 'box', 'color': '#81C784'}
        self.definition_inclusion_args = {'shape': 'box', 'color': '#90CAF9'}
        self.inferred_statement_args = {'shape': 'box', 'color': '#FFF59D'}
        self.label_wrap_size = 20
        self.title_wrap_size = 32


pyvis_configuration = PyvisConfiguration()


def unpack_formula(o: (Formula, CompoundFormula, FormulaStatement)) -> CompoundFormula:
    """Receive a formula and unpack its formula if it is a statement that contains a
    formula."""
    u: UniverseOfDiscourse = o.u
    verify(is_declaratively_member_of_class(u=u, phi=o, c=u.c2.formula), 'Parameter ⌜o⌝ must a formula.', o=o)
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


class DeclarativeClass_OBSOLETE(repm.ValueName):
    """The DeclarativeClass python class models a declarative-class."""

    def __init__(self, name, natural_language_name, python_type: [None, type] = None):
        self._natural_language_name = natural_language_name
        self._python_type = python_type
        super().__init__(name)

    @property
    def natural_language_name(self) -> str:
        return self._natural_language_name

    @property
    def python_type(self) -> [None, type]:
        return self._python_type


def is_derivably_member_of_class(u: UniverseOfDiscourse, phi: FlexibleFormula, c: ClassDeclaration) -> bool:
    """Returns True if and only if phi has been proved / derived as being a member of class c in the minimal metatheory
    of u.

    Note: when False is returned, this functions does not tell if phi is a member of c. In effect, it may be
    provable (derivable) that phi is a member of c, even though that derivation has not been performed yet
    in the minimal metatheory of u. But if the statement (phi is-a c) has been derived in the minimal metatheory of u,
    stating that phi is a member of c is a valid statement.
    """
    phi_is_a_c = phi | u.c1.is_a | c
    is_valid = is_declaratively_member_of_class(u=u, phi=phi, c=c)
    if is_valid:
        return is_valid
    else:
        is_valid, _, _ = verify_formula_statement(t=u.metatheory.t, input_value=phi_is_a_c, arg='phi_is_a_c',
            raise_exception=False)
        return is_valid


def is_declaratively_member_of_class(u: UniverseOfDiscourse, phi: FlexibleFormula, c: ClassDeclaration) -> bool:
    """Returns True if and only if phi is declaratively a member of class c. Returns False otherwise.

    Note: when False is returned, this functions does not tell if phi is a member of c. In effect, phi may be a
    member of c by theoretical derivation, and not by declaration. But if phi is a member of c because of the
    declaration of phi in u, stating that phi is a member of c is a valid statement.

    See also: function is_proved_member_of_class()

    See minimal-metatheory for more details."""

    # BUG: verify_formula unpacks the inferred_statement internal formula.
    # but we don't want to do that, because we may want to test
    # that the object is of the class inferred_statement!
    # There is an ambiguity here, between "formula" as the generic
    # object of all Punctilious data model, and "formula" as
    # a syntactic construction.
    _, phi, _ = verify_formula(u=u, input_value=phi, arg='phi', unpack_statement=False)
    _, c, _ = verify_class(u=u, c=c, arg='c')
    phi: Formula
    c: ClassDeclaration
    if c.python_class is not None and isinstance(phi, c.python_class):
        # This class-declaration has a python class linked to it
        # that models the declaration of objects of that class.
        # If phi is a python object that is an instance of that python class,
        # it follows that the mathematical object phi is provably a member of the corresponding mathematical calss.
        # TODO: Should we populate a statement in the metatheory? Or make it a configuration setting and a parameter?
        return True
    else:
        return False


def is_declaratively_member_of_class_universe_of_discourse(u: UniverseOfDiscourse) -> bool:
    """Returns True if and only if u is a universe-of-discourse.

    Granted, this function looks a bit stupid. Its rationale is to complement
    function is_declaratively_member_of_class(phi, c) for the special case where
    c is the class universe-of-discourse. In effect, universes-of-discourse
    do not (necessarily) have a parent universe-of-discourse.
    """
    if isinstance(u, UniverseOfDiscourse):
        return True
    else:
        return False


# def is_in_class_OBSOLETE(o: Formula, c: DeclarativeClass_OBSOLETE) -> bool:
#    """Return True if o is a member of the declarative-class c, False otherwise.
#    :param o: An arbitrary python object.
#    :param c: A declarative-class.
#    :return: (bool).
#   """
#    verify(o is not None, 'o is None.', o=o, c=c)
#    # verify(hasattr(o, 'is_in_class'), 'o does not have attribute is_in_class.', o=o, c=c)
#    verify(callable(getattr(o, 'is_in_class_OBSOLETE')), 'o.is_in_class() is not callable.', o=o, c=c)
#    return o.is_in_class_OBSOLETE(c)


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
    """The NoNameSolutionException is the exception that is raised when a NameSet cannot be
    represented because no representation was found for the required Encoding."""

    def __init__(self, nameset, encoding):
        self.nameset = nameset
        self.encoding = encoding

    def __str__(self):
        return f'The nameset ⌜{repr(self.nameset)}⌝ contains no representation for the ⌜' \
               f'{self.encoding}⌝ text-format.'


class NameSet(Composable):
    """A set of qualified names used to identify an object.

    TODO: Enhancement: for connectives in particular, add a verb NameType (e.g. implies).
    """

    def __init__(self, s: (None, str) = None, symbol: (None, str, StyledText) = None,
        index: (None, int, str, ComposableText) = None, namespace: (None, SymbolicObject) = None,
        dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
        abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
        explicit_name: (None, str, StyledText) = None, paragraph_header: (None, ParagraphHeader) = None,
        ref: (None, str) = None, subtitle: (None, str, ComposableText) = None):
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
        # Symbolic names
        if isinstance(symbol, str):
            symbol = StyledText(s=symbol, text_style=text_styles.serif_italic)
        self._symbol = symbol
        # TODO: In NameSet.__init__, retrieve index_as_int when index is not an int
        self._index_as_int = index if isinstance(index, int) else None
        if isinstance(index, str):
            index = Subscript(plaintext=index)
        elif isinstance(index, int):
            index = Subscript(plaintext=str(index))
        self._index = index
        self._namespace = namespace
        if isinstance(dashed_name, str):
            dashed_name = SerifItalic(s=dashed_name)
        self._dashed_name = dashed_name if isinstance(dashed_name, StyledText) else StyledText(s=dashed_name,
            text_style=text_styles.serif_italic) if isinstance(dashed_name, str) else None
        verify(self.symbol is not None, msg='The symbol of this nameset is None.', slf=self)
        # Natural names
        if isinstance(acronym, str):
            acronym = SansSerifNormal(acronym)
        self._acronym = acronym
        if isinstance(abridged_name, str):
            abridged_name = SansSerifNormal(abridged_name)
        self._abridged_name = abridged_name
        if isinstance(name, str):
            name = SansSerifNormal(name)
        self._name = name
        if isinstance(explicit_name, str):
            explicit_name = SansSerifNormal(explicit_name)
        self._explicit_name = explicit_name
        # Section reference names
        if isinstance(ref, str):
            ref = SansSerifBold(ref)
        self._ref = ref
        if paragraph_header is None:
            paragraph_header = paragraph_headers.uncategorized
        self._paragraph_header = paragraph_header
        self._subtitle = subtitle

    def __eq__(self, other):
        """Two NameSets n and m are equal if their (symbol, index) pairs are equal.
        """
        return type(self) is type(other) and self.symbol == other.symbol and self.index == other.index

    def __hash__(self):
        return hash((NameSet, self.symbol, self.index))

    def __repr__(self):
        return self.rep_symbol()

    def __str__(self):
        return self.rep_symbol()

    @property
    def acronym(self) -> ComposableText:
        return self._acronym

    def compose(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        something = yield from self.compose_symbol(pre=pre, post=post)
        return something

    def compose_accurate_name(self, cap: (None, bool) = None, pre: (None, str, Composable) = None,
        post: (None, str, Composable) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        """Composes the most least unambiguous natural-language name in the nameset.
        """
        something = yield from yield_composition(
            prioritize_value(self._explicit_name, self._name, self._abridged_name, self._acronym), cap=cap, pre=pre,
            post=post)
        return something

    def compose_abridged_name(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        if self._abridged_name is None:
            return False
        else:
            something = yield from yield_composition(self._abridged_name, pre=pre, post=post)
            return something

    def compose_acronym(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        if self._acronym is None:
            return False
        else:
            something = yield from yield_composition(self._acronym, pre=pre, post=post)
            return something

    def compose_paragraph_header_unabridged(self, cap: (None, bool) = None, pre: (None, str, Composable) = None,
        post: (None, str, Composable) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        if self._paragraph_header is None:
            return False
        else:
            something = yield from yield_composition(self.paragraph_header.natural_name, cap=cap, pre=pre, post=post)
            return something

    def compose_paragraph_header_abridged(self, cap: (None, bool) = None, pre: (None, str, Composable) = None,
        post: (None, str, Composable) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        if self._paragraph_header is None:
            return False
        else:
            something = yield from yield_composition(self._paragraph_header.abridged_name, cap=cap, pre=pre, post=post)
            return something

    def compose_compact_name(self, cap: (None, bool) = None, pre: (None, str, Composable) = None,
        post: (None, str, Composable) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        """Composes the most compact / shortest name in the nameset.
        """
        something = yield from yield_composition(
            prioritize_value(self._abridged_name, self._acronym, self._name, self._explicit_name), cap=cap, pre=pre,
            post=post)
        return something

    def compose_conventional_name(self, cap: (None, bool) = None, pre: (None, str, Composable) = None,
        post: (None, str, Composable) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        """Composes the most conventional / frequently-used name in the nameset.
        """
        something = yield from yield_composition(
            prioritize_value(self._name, self._abridged_name, self._acronym, self._explicit_name), cap=cap, pre=pre,
            post=post)
        return something

    def compose_dashed_name(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        if self._dashed_name is None:
            return False
        else:
            something = yield from yield_composition(self._dashed_name, pre=pre, post=post)
            return something

    def compose_explicit_name(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        if self._explicit_name is None:
            return False
        else:
            something = yield from yield_composition(self._explicit_name, pre=pre, post=post)
            return something

    def compose_index(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        if self._symbol is None:
            return False
        else:
            something = yield from yield_composition(self._index, pre=pre, post=post)
            return something

    def compose_name(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        if self._name is None:
            return False
        else:
            something = yield from yield_composition(self._name, pre=pre, post=post)
            return something

    def compose_qualified_symbol(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        """Composes: ⌜[dashed-name] ([symbol])⌝, or ⌜[symbol]⌝ if dashed-name is None. The
        rationale is to enrich the symbol with a more meaningful dashed-name if it is available."""
        if self._dashed_name is None:
            # Representation of the form: [symbol][index]
            yield from self.compose_symbol(pre=pre, post=post)
            return True
        else:
            # Representation of the form: [dashed-named] ([symbol][index])
            yield from yield_composition(pre)
            yield from self.compose_dashed_name()
            yield from self.compose_symbol(pre=' (', post=')')
            yield from yield_composition(post)
            return True

    def compose_ref(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, None, None]:
        if self._ref is None:
            return False
        else:
            something = yield from yield_composition(self._ref, pre=pre, post=post)
            return something

    def compose_ref_link(self, cap: (None, bool) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        output1 = yield from self.compose_paragraph_header_abridged(cap=cap)
        pre = text_dict.space if output1 else None
        output2 = yield from self.compose_ref(pre=pre)
        pre = ' (' if output1 or output2 else None
        post = ')' if output1 or output2 else None
        output3 = yield from self.compose_symbol(pre=pre, post=post)
        return True

    def compose_subtitle(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        if self._subtitle is None:
            return False
        else:
            something = yield from yield_composition(self._subtitle, pre=pre, post=post)
            return something

    def compose_symbol(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
        collections.abc.Generator[Composable, Composable, bool]:
        if self._symbol is None:
            return False
        else:
            something = yield from yield_composition(self._symbol, self.compose_index(), pre=pre, post=post)
            return something

    def compose_title(self, cap: (None, bool) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        output1 = yield from self.compose_paragraph_header_unabridged(cap=cap)
        pre = text_dict.space if output1 else None
        output2 = yield from self.compose_ref(pre=pre)
        yield SansSerifNormal(' (')
        if self.namespace is not None:
            yield from self.namespace.compose_symbol()
            yield SansSerifNormal('.')
        yield from self.compose_symbol()
        yield SansSerifNormal(')')
        yield from self.compose_subtitle(pre=' - ')
        return True

    @property
    def dashed_name(self) -> StyledText:
        return self._dashed_name

    @property
    def explicit_name(self) -> ComposableText:
        return self._explicit_name

    @property
    def index(self) -> str:
        return self._index

    @property
    def index_as_int(self) -> int:
        """Especially for auto-indexing purposes, exposes the index as an int if it is an int."""
        return self._index_as_int

    def is_base_symbol_equivalent(self, symbol: FlexibleSymbol):
        """Return True if two NameSet instances have equal base symbols, False otherwise."""
        _, symbol, _ = verify_symbol(input_value=symbol)
        return self.symbol == symbol.symbol

    def is_qualified_symbol_equivalent(self, symbol: FlexibleSymbol):
        _, symbol, _ = verify_symbol(input_value=symbol)
        """Return True if two NameSet instances have equal base symbols, and complementary symbolic properties such 
        as index, False otherwise."""
        # TODO: Provide support for exponent, etc.
        return self.is_base_symbol_equivalent(symbol) and self.index == symbol.index

    @property
    def name(self) -> StyledText:
        return self._name

    @property
    def namespace(self) -> SymbolicObject:
        """TODO: Cross-referencing the parent object in the nameset attribute is ugly,
        the approach is wrong, correct this.

        :return:
        """
        return self._namespace

    @property
    def paragraph_header(self) -> ParagraphHeader:
        """The category of this statement."""
        return self._paragraph_header

    @paragraph_header.setter
    def paragraph_header(self, paragraph_header: ParagraphHeader):
        """TODO: Remove this property setter to only set property values at init-time,
        and make the hash stable. This quick-fix was necessary while migrating from
        the old approach that used the obsolete Title class."""
        self._paragraph_header = paragraph_header

    @property
    def ref(self) -> str:
        """Unabridged name."""
        return self._ref

    @ref.setter
    def ref(self, ref: str):
        """TODO: Remove this property setter to only set property values at init-time,
        and make the hash stable. This quick-fix was necessary while migrating from
        the old approach that used the obsolete Title class."""
        self._ref = ref

    def rep(self, encoding: (None, Encoding) = None, **kwargs) -> str:
        """Return the default representation for this python obje.

        :return:
        """
        return f'{self.rep_symbol(encoding=encoding)}'

    def rep_abridged_name(self, cap: (None, bool) = None, encoding: (None, Encoding) = None) -> (None, str):
        """Return a string that represent the object as an acronym."""
        return rep_composition(composition=self.compose_abridged_name(), encoding=encoding)

    def rep_accurate_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None):
        """Returns the most accurate (longest) possible name in the nameset for the required
        text-format.

        Order of priority:
        1) explicit-name
        2) name
        3) acronym
        4) symbol
        """
        return rep_composition(composition=self.compose_accurate_name(), encoding=encoding, cap=cap)

    def rep_acronym(self, encoding: (None, Encoding) = None, compose: bool = False) -> (None, str):
        """Return a string that represent the object as an acronym."""
        return rep_composition(composition=self.compose_acronym(), encoding=encoding)

    def rep_compact_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None):
        """Returns the shortest possible name in the nameset for the required text-format.

        Order of priority:
        1) symbol
        2) acronym
        3) name
        4) explicit-name
        """
        return rep_composition(composition=self.compose_compact_name(), encoding=encoding, cap=cap)

    def rep_conventional_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None):
        """Returns the most conventional (default) possible name in the nameset for the required
        text-format.

        Order of priority:
        2) name
        3) acronym
        4) symbol
        1) explicit-name
        """
        return rep_composition(composition=self.compose_conventional_name(), encoding=encoding, cap=cap)

    def rep_dashed_name(self, encoding: (None, Encoding) = None, compose: bool = False) -> (None, str):
        return rep_composition(composition=self.compose_dashed_name(), encoding=encoding)

    def rep_explicit_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> (None, str):
        """Return a string that represent the object as an explicit name."""
        return rep_composition(composition=self.compose_explicit_name(), encoding=encoding, cap=cap)

    def rep_fully_qualified_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None,
        compose: bool = False):
        conventional = self.rep_conventional_name(encoding=encoding, cap=cap)
        sym = self.rep_symbol(encoding=encoding)
        rep = ComposableBlockSequence()
        rep.append(conventional)
        if conventional != sym:
            rep.append(' (')
            rep.append(sym)
            rep.append(')')
        if not compose:
            rep = rep.rep(encoding=encoding)
        return rep

    def rep_mention(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        """A mention of the form: [symbol] [unabridged-category]
        """
        rep = ''
        if self._name is not None:
            rep = rep + self.rep_name(encoding=encoding, cap=cap)
        rep = rep + ' '
        rep = rep + StyledText(s='(', text_style=text_styles.sans_serif_bold).rep(encoding=encoding)
        rep = rep + self.rep_symbol(encoding=encoding)
        rep = rep + StyledText(s=')', text_style=text_styles.sans_serif_bold).rep(encoding=encoding)
        rep = '' if self._paragraph_header is None else StyledText(s=self.paragraph_header.natural_name,
            text_style=text_styles.sans_serif_bold).rep(encoding=encoding, cap=cap)
        return rep

    def rep_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> (None, str):
        """Return a string that represent the object as a plain name."""
        return rep_composition(composition=self.compose_name(), encoding=encoding, cap=cap)

    def rep_ref(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        return rep_composition(composition=self.compose_ref(), encoding=encoding, cap=cap)

    def rep_symbol(self, encoding: (None, Encoding) = None, **kwargs) -> (None, str):
        """Return a string that represent the object as a symbol."""
        return rep_composition(composition=self.compose_symbol(), encoding=encoding, **kwargs)

    def rep_title(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        """A title of the form: [unabridged-category] [reference] ([symbol]) - [subtitle]
        """
        return rep_composition(composition=self.compose_title(cap=cap), encoding=encoding)

    @property
    def subtitle(self) -> str:
        """A conditional complement to the automatically structured title."""
        return self._subtitle

    @subtitle.setter
    def subtitle(self, subtitle: str):
        """TODO: Remove this property setter to only set property values at init-time,
        and make the hash stable. This quick-fix was necessary while migrating from
        the old approach that used the obsolete Title class."""
        self._subtitle = subtitle

    @property
    def symbol(self) -> ComposableText:
        """The symbol core glyph.

        :return: (StyledText) The symbol core glyph.
        """
        return self._symbol

    def to_dict(self):
        return {'symbol':    self._symbol, 'acronym': self._acronym, 'name': self._name,
            'explicit_name': self._explicit_name}


class DashedName:
    """A dashed-name to provide more semantically meaningful names to symbolic-objcts in reports
    than symbols.

    Features:
    - Immutable
    """

    def __init__(self, dashed_named):
        verify(isinstance(dashed_named, str), 'dashed-name is not of type str.', dashed_named=dashed_named)
        # TODO: Clean string from non-alphanumeric, digits, dash characters, etc.
        self._dashed_name = dashed_named

    def __hash__(self):
        """"""
        return hash((self._dashed_name))

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    def rep(self, encoding: (None, Encoding) = None) -> str:
        """Return the default representation.
        """
        return self.rep_dashed_name(encoding=encoding)

    def rep_dashed_name(self, encoding: (None, Encoding) = None) -> str:
        """Return a dashed-name representation.
        """
        # TODO: Implement encodings
        return self._dashed_name


class SymbolicObject(abc.ABC):
    """
    Definition
    ----------
    A symbolic-objct is a python object instance that is assigned symbolic names,
    that is linked to a theory, but that is not necessarily constitutive of the theory.
    """

    def __init__(self, u: UniverseOfDiscourse, is_theory_foundation_system: bool = False,
        is_universe_of_discourse: bool = False, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, namespace: (None, SymbolicObject) = None,
        dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
        abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
        explicit_name: (None, str, StyledText) = None, paragraph_header: (None, ParagraphHeader) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_symbolic_objct, configuration.echo_default, False)
        auto_index = prioritize_value(auto_index, configuration.auto_index, True)
        # self._declarative_classes = frozenset()
        is_theory_foundation_system = False if is_theory_foundation_system is None else is_theory_foundation_system
        is_universe_of_discourse = False if is_universe_of_discourse is None else is_universe_of_discourse
        symbol = SerifItalic(symbol) if isinstance(symbol, str) else symbol
        symbol = configuration.default_symbolic_object_symbol if symbol is None else symbol
        if u is not None:
            index = u.symbolic_objects.index_symbol(symbol=symbol) if (index is None and auto_index) else index
        if paragraph_header is None:
            paragraph_header = paragraph_headers.uncategorized
        nameset = NameSet(symbol=symbol, index=index, namespace=namespace, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, paragraph_header=paragraph_header,
            ref=ref, subtitle=subtitle)
        self._nameset = nameset
        self.is_theory_foundation_system = is_theory_foundation_system
        if not is_universe_of_discourse:
            self._u = u
        else:
            self._u = None
        if u is not None:
            u.symbolic_objects.add_symbolic_object(symbolic_object=self)
        if echo:
            repm.prnt(self.rep_report())

    def __eq__(self, other):
        """python equality is implemented as strict object equality, but not as symbolic equivalence."""
        return hash(self) == hash(other)

    def __hash__(self):
        """Because our intention is to allow distinct formulae to have identical (non-unique) names, to have no or
        multiple names, the only underlying identifier we can rely on is the native python id function."""
        return hash(id(self))

    def __repr__(self):
        return self.rep_symbol(encoding=encodings.plaintext)

    def __str__(self):
        return self.rep_symbol(encoding=encodings.plaintext)

    def compose(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose()
        return True

    def compose_class(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield SerifItalic(plaintext='symbolic-object')
        return True

    def compose_dashed_name(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_dashed_name()
        return output

    def compose_paragraph_header_unabridged(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_paragraph_header_unabridged()
        return output

    def compose_ref(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_ref()
        return output

    def compose_ref_link(self, cap: (None, bool) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_ref_link(cap=cap)
        return output

    def compose_report(self, close_punctuation: Composable = None, cap: (None, bool) = None, proof: (None, bool) = None,
        **kwargs) -> collections.abc.Generator[Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        yield from text_dict.let.compose(cap=cap)
        yield text_dict.space
        yield text_dict.open_quasi_quote
        yield from self.compose_symbol()
        yield text_dict.close_quasi_quote
        yield text_dict.space
        yield text_dict.be_a
        yield text_dict.space
        yield from self.compose_class()
        yield text_dict.space
        yield text_dict.in2
        yield text_dict.space
        yield from self.u.compose_symbol()
        yield prioritize_value(close_punctuation, text_dict.period)
        return True

    def compose_symbol(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_symbol()
        return output

    def compose_title(self, cap: (None, bool) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_title(cap=cap)
        return output

    def echo(self):
        repm.prnt(self.rep())

    def is_base_symbol_equivalent(self, o2: FlexibleSymbol) -> bool:
        """Return True if this object and o2 are base-symbol-equivalent, False otherwise.
        """
        # A formula can only be compared with a formula
        return self.nameset.is_base_symbol_equivalent(o2)

    def is_qualified_symbol_equivalent(self, o2: FlexibleSymbol) -> bool:
        """Return True if this object and o2 are qualified-symbol-equivalent, False otherwise.
        """
        # A formula can only be compared with a formula
        return self.nameset.is_qualified_symbol_equivalent(o2)

    def prnt(self, encoding: (None, Encoding) = None, expand=False):
        repm.prnt(self.nameset.rep(encoding=encoding, expand=expand))

    @property
    def ref(self) -> (None, str):
        return self.nameset.ref

    def rep(self, encoding: (None, Encoding) = None, **kwargs) -> str:
        return rep_composition(composition=self.compose(), encoding=encoding, **kwargs)

    def rep_dashed_name(self, encoding: (None, Encoding) = None) -> str:
        return self.nameset.rep_dashed_name(encoding=encoding)

    def rep_formula(self, encoding: (None, Encoding) = None, expand: (None, bool) = None) -> str:
        """If supported, return a formula representation,
        a symbolic representation otherwise.

        The objective of the repr_as_formula() method is to
        represent formulae and formula-statements not as symbols
        (e.g.: 𝜑₅) but as expanded formulae (e.g.: (4 > 3)).
        Most symbolic-objcts do not have a formula representation,
        where we fall back on symbolic representation.
        """
        return self.rep_symbol(encoding=encoding)

    def rep_fully_qualified_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None,
        compose: bool = False) -> str:
        """"""
        return self.nameset.rep_fully_qualified_name(encoding=encoding, cap=cap, compose=compose)

    def rep_mention(self, encoding: (None, Encoding) = None, cap: bool = False) -> str:
        return self.nameset.rep_mention(encoding=encoding, cap=cap)

    def rep_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        return self.nameset.rep_name(encoding=encoding, cap=cap)

    def rep_ref(self, encoding: (None, Encoding) = None, cap: bool = False) -> str:
        return self.nameset.rep_ref(encoding=encoding, cap=cap)

    def rep_report(self, encoding: (None, Encoding) = None, proof: (None, bool) = None,
        wrap: (None, bool) = None) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        output = rep_composition(composition=self.compose_report(proof=proof), encoding=encoding)
        return output

    def rep_symbol(self, encoding: (None, Encoding) = None) -> str:
        return self._nameset.rep_symbol(encoding=encoding)

    def rep_title(self, encoding: (None, Encoding) = None, cap: bool = False) -> str:
        return self._nameset.rep_title(encoding=encoding, cap=cap)

    @property
    def nameset(self) -> NameSet:
        """Every symbolic-object that is being referenced must be assigned a unique symbol in its
        universe-of-discourse."""
        return self._nameset

    @property
    def u(self):
        """The universe of discourse containing this object."""
        return self._u


class InfixPartialFormula:
    """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
    This is accomplished by re-purposing the | operator,
    overloading the __or__() method that is called when | is used,
    and glueing all this together with the InfixPartialFormula class.
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __or__(self, other=None):
        """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
        This is accomplished by re-purposing the | operator,
        overloading the __or__() method that is called when | is used,
        and glueing all this together with the InfixPartialFormula class.
        """
        # print(f'IPF.__or__: self = {self}, other = {other}')
        connective = self.b
        first_term = self.a
        second_term = other
        return self.a.u.declare_compound_formula(connective, first_term, second_term)

    def __str__(self):
        return f'InfixPartialFormula(a = {self.a}, b = {self.b})'

    # def __ror__(self, other=None):  #    """Hack to provide support for pseudo-infix notation, as in: p |implies| q.  #    """  #    print(f'IPF.__ror__: self = {self}, other = {other}')  #    if not isinstance(other, InfixPartialFormula):  #        return InfixPartialFormula(a=self, b=other)  # return self.a.u.declare_compound_formula(self.b, self.a, other)  #    else:  #        verify(assertion=1 == 2, msg='failed infix notation', slf_a=self.a, slf_b=self.b)  #        return self.a.u.declare_compound_formula(self.a, self.b, self)


class TheoreticalClass(type):
    """A meta-class for python classes that implement formulas in the punctilious_obsolete_20240114 data-model.

    TODO: This is just an idea to facilitate the programmatical discovery of the data-model,
    an idea to be investigated further.
    """

    def __init__(cls, name, bases, attrs):
        attrs['some_custom_attribute'] = 'This is a custom class attribute.'
        super().__init__(name, bases, attrs)


def iterate_formula_data_model_components(u: UniverseOfDiscourse, phi: Formula, yield_parent_constant: bool = True,
    recurse_constant_value: bool = True, yield_parent_compound_formula: bool = True,
    recurse_compound_formula_connective: bool = True, recurse_compound_formula_terms: bool = True,
    yield_parent_statement: bool = True, recurse_statement_proposition: bool = True,
    yield_classes: (None, tuple) = None) -> Generator[FlexibleFormula, None, None]:
    """Iterate through the data-model components of a formula in canonical-order.

    This is a general-purpose iterator. The function allows to select which properties of the
    data-model must be recursively visited by the iteration, and which classes of objects must be yield."""
    _, phi, _ = verify_formula(u=u, input_value=phi, arg='phi')
    if isinstance(phi, ConstantDeclaration):
        if yield_parent_constant and (yield_classes is None or isinstance(phi, yield_classes)):
            yield phi
            if recurse_constant_value:
                yield from iterate_formula_data_model_components(u=u, phi=phi.value,
                    yield_parent_constant=yield_parent_constant, recurse_constant_value=recurse_constant_value,
                    yield_parent_compound_formula=yield_parent_compound_formula,
                    recurse_compound_formula_connective=recurse_compound_formula_connective,
                    recurse_compound_formula_terms=recurse_compound_formula_terms,
                    yield_parent_statement=yield_parent_statement,
                    recurse_statement_proposition=recurse_statement_proposition, yield_classes=yield_classes)
    elif isinstance(phi, FormulaStatement):
        if yield_parent_statement and (yield_classes is None or isinstance(phi, yield_classes)):
            yield phi
        if recurse_statement_proposition:
            yield from iterate_formula_data_model_components(u=u, phi=phi.valid_proposition,
                yield_parent_constant=yield_parent_constant, recurse_constant_value=recurse_constant_value,
                yield_parent_compound_formula=yield_parent_compound_formula,
                recurse_compound_formula_connective=recurse_compound_formula_connective,
                recurse_compound_formula_terms=recurse_compound_formula_terms,
                yield_parent_statement=yield_parent_statement,
                recurse_statement_proposition=recurse_statement_proposition, yield_classes=yield_classes)
    elif isinstance(phi, CompoundFormula):
        if yield_parent_compound_formula and (yield_classes is None or isinstance(phi, yield_classes)):
            yield phi
        if recurse_compound_formula_connective:
            yield from iterate_formula_data_model_components(u=u, phi=phi.connective,
                yield_parent_constant=yield_parent_constant, recurse_constant_value=recurse_constant_value,
                yield_parent_compound_formula=yield_parent_compound_formula,
                recurse_compound_formula_connective=recurse_compound_formula_connective,
                recurse_compound_formula_terms=recurse_compound_formula_terms,
                yield_parent_statement=yield_parent_statement,
                recurse_statement_proposition=recurse_statement_proposition, yield_classes=yield_classes)
        if recurse_compound_formula_terms:
            for p in phi.terms:
                yield from iterate_formula_data_model_components(u=u, phi=p,
                    yield_parent_constant=yield_parent_constant, recurse_constant_value=recurse_constant_value,
                    yield_parent_compound_formula=yield_parent_compound_formula,
                    recurse_compound_formula_connective=recurse_compound_formula_connective,
                    recurse_compound_formula_terms=recurse_compound_formula_terms,
                    yield_parent_statement=yield_parent_statement,
                    recurse_statement_proposition=recurse_statement_proposition, yield_classes=yield_classes)
    else:
        if yield_classes is None or isinstance(phi, yield_classes):
            yield phi


def iterate_formula_alpha_equivalence_components(u: UniverseOfDiscourse, phi: FlexibleFormula) -> Generator[
    FlexibleFormula, None, None]:
    """Iterate through the components of a formula that are alpha-equivalence meaningful, in canonical-order."""
    yield from (
        iterate_formula_data_model_components(u=u, phi=phi, yield_parent_constant=False, recurse_constant_value=True,
            yield_parent_compound_formula=False, recurse_compound_formula_connective=True,
            recurse_compound_formula_terms=True, yield_parent_statement=False, recurse_statement_proposition=True,
            yield_classes=None))


def formula_alpha_contains(u: UniverseOfDiscourse, phi: FlexibleFormula, psi: FlexibleFormula):
    """Returns True if phi contains a component that is alpha-equivalent to psi, including the extreme case where phi is alpha-equivalent to psi."""
    _, phi, _ = verify_formula(u=u, input_value=phi, arg='phi')
    _, psi, _ = verify_formula(u=u, input_value=psi, arg='psi')
    if is_alpha_equivalent_to(u=u, phi=phi, psi=psi):
        return True
    for component in iterate_formula_data_model_components(u=u, phi=phi, yield_parent_constant=False,
        recurse_constant_value=True, recurse_compound_formula_connective=True, recurse_compound_formula_terms=True,
        recurse_statement_proposition=True, yield_classes=None):
        if is_alpha_equivalent_to(u=u, phi=component, psi=psi):
            return True
    return False


def get_formula_unique_variable_ordered_set(u: UniverseOfDiscourse, phi: FlexibleFormula) -> tuple[FreeVariable]:
    """Return the ordered-set of unique variables contained in ⌜self⌝,
    ordered in canonical-order (TODO: add link to doc on canonical-order),
    and excluding variables contained in object-reference statements (TODO: document object-reference mechanim and
    reference doc here).
    """
    _, phi, _ = verify_formula(u=u, input_value=phi, arg='phi')
    phi: Formula

    ordered_set: list[FreeVariable] = list()
    before_element: Formula = None
    for element in iterate_formula_alpha_equivalence_components(u=u, phi=phi):
        if isinstance(element, FreeVariable):
            if element not in ordered_set:
                if before_element is not u.c1.object_reference:
                    # Exception: if the variable is referenced as an object,
                    # do not close its scope automatically.
                    ordered_set.append(element)
        before_element = element
    # Make the ordered-set proxy immutable.
    ordered_set: tuple[FreeVariable] = tuple(ordered_set)
    return ordered_set


def is_alpha_equivalent_to(u: UniverseOfDiscourse, phi: FlexibleFormula, psi: FlexibleFormula) -> bool:
    """Return True if phi is :ref:alpha-equivalent`<alpha_equivalence_math_concept>` to psi.

    :param phi: Another formula.
    :return:
    """
    _, phi, _ = verify_formula(u=u, input_value=phi, arg='phi')
    phi: Formula
    _, psi, _ = verify_formula(u=u, input_value=psi, arg='psi')
    psi: Formula

    phi_variables: tuple[FreeVariable] = get_formula_unique_variable_ordered_set(u=u, phi=phi)
    psi_variables: tuple[FreeVariable] = get_formula_unique_variable_ordered_set(u=u, phi=psi)

    if len(phi_variables) != len(psi_variables):
        return False

    phi_generator = iterate_formula_alpha_equivalence_components(u=u, phi=phi)
    psi_generator = iterate_formula_alpha_equivalence_components(u=u, phi=psi)

    before_phi_element: Formula = None
    before_psi_element: Formula = None

    for phi_element, psi_element in itertools.zip_longest(phi_generator, psi_generator, fillvalue=None):
        # print(f'{phi_element}|{psi_element}')
        if phi_element is None or psi_element is None:
            # If phi and psi do not contain the same number of symbols,
            # the are not alpha-equivalent.
            return False
        if type(phi_element) is not type(psi_element):
            # If a symbol in phi is of a different class
            # than its corresponding symbol in psi,
            # phi and psi are not alpha-equivalent.
            return False
        if isinstance(phi_element, FreeVariable) and isinstance(psi_element, FreeVariable):
            # print(f'{phi_variables.index(phi_element)}|{psi_variables.index(psi_element)}')
            if before_psi_element is u.c1.object_reference and before_phi_element is u.c1.object_reference:
                # The variables are referenced as objects, we can compare them directly.
                if phi_element is not psi_element:
                    return False
            elif before_psi_element is not u.c1.object_reference and before_phi_element is not u.c1.object_reference:
                if phi_variables.index(phi_element) != psi_variables.index(psi_element):
                    # Variables are only compared by their position in the formula.
                    return False
            else:
                # One variable is referenced as an object and the other is used as a variable,
                # this is not alpha-equivalent.
                return False
        elif phi_element is not psi_element:
            return False
        before_phi_element = phi_element
        before_psi_element = psi_element

    # If all the above checks passed successfuly,
    # phi and psi are alpha-equivalent.
    return True


def is_alpha_equivalent_to_iterable(u: UniverseOfDiscourse, phi: typing.Iterable[FlexibleFormula],
    psi: typing.Iterable[FlexibleFormula]) -> bool:
    """See function is_alpha_equivalent_to."""
    return (is_alpha_equivalent_to(u=u, phi=phi_element, psi=psi_element) for (phi_element, psi_element) in
        itertools.zip_longest(phi, psi, fillvalue=None))


class Formula(SymbolicObject):
    """
    Definition
    ----------
    A formula phi is an object that may be referenced in compound-formulas.

    The following are supported classes of formula:
    * axiom
    * formula
    * lemma
    * proposition
    * connective
    * simple-object
    * theorem
    * theory
    * variable
    """

    def __init__(self, u: UniverseOfDiscourse, is_universe_of_discourse: (None, bool) = None,
        is_theory_foundation_system: bool = False, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, namespace: (None, SymbolicObject) = None,
        dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
        abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
        explicit_name: (None, str, StyledText) = None, paragraph_header: (None, ParagraphHeader) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):
        super().__init__(u=u, is_universe_of_discourse=is_universe_of_discourse,
            is_theory_foundation_system=is_theory_foundation_system, symbol=symbol, index=index, auto_index=auto_index,
            namespace=namespace, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, echo=False)
        self._collections = frozenset()  # TODO: Probably an OBSOLETE member
        if not isinstance(self, UniverseOfDiscourse):
            # The universe-of-discourse is the only object that may not
            # be contained in a universe-of-discourse.
            # All other objects must be contained in a universe-of-discourse.
            verify_universe_of_discourse(u=u)
            u.phi.declare_formula_instance(phi=self)
        if echo:
            repm.prnt(self.rep_fully_qualified_name())

    def __and__(self, other=None):
        """Hack to provide support for pseudo-postfix notation, as in: p & ++.
        This is accomplished by re-purposing the & operator,
        overloading the __and__() method that is called when & is used,
        and gluing all this together.
        """
        # print(f'TO.__and__: self = {self}, other = {other}')
        ok: bool
        formula: (None, CompoundFormula)
        msg: (None, str)
        ok, formula, msg = verify_formula(u=self.u, input_value=(other, self), raise_exception=True)
        return formula

    def __call__(self, *terms):
        """Hack to provide support for direct function-call notation, as in: p(x).
        """
        # print(f'TO.__call__: self = {self}, terms = {terms}')
        ok: bool
        formula: (None, CompoundFormula)
        msg: (None, str)
        ok, formula, msg = verify_formula(u=self.u, input_value=(self, *terms), raise_exception=True)
        return formula

    def __eq__(self, other):
        """To start with, we implement a super restrictive python equality function,
        that assures that two objects are equal if and only if
        they are the same python object in memory.
        """
        return hash(self) == hash(other)

    def __hash__(self):
        """To start with, we implement a super restrictive python hash function,
        that assures that two objects have the same hash value if and only if
        they are the same python object in memory."""
        return hash((type(self), id(self)))

    def __xor__(self, other=None):
        """Hack to provide support for pseudo-prefix notation, as in: neg ^ p.
        This is accomplished by re-purposing the ^ operator,
        overloading the __xor__() method that is called when ^ is used,
        and gluing all this together.
        """
        # print(f'TO.__xor__: self = {self}, other = {other}')
        ok: bool
        formula: (None, CompoundFormula)
        msg: (None, str)
        ok, formula, msg = verify_formula(u=self.u, input_value=(self, other), raise_exception=True)
        return formula

    def __or__(self, other=None):
        """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
        This is accomplished by re-purposing the | operator,
        overloading the __or__() method that is called when | is used,
        and gluing all this together with the InfixPartialFormula class.
        """
        # print(f'TO.__or__: self = {self}, other = {other}')
        if not isinstance(other, InfixPartialFormula):
            return InfixPartialFormula(a=self, b=other)
        else:
            # return self.u.declare_compound_formula(self, other.a, other.b)
            ok: bool
            formula: (None, CompoundFormula)
            msg: (None, str)
            ok, formula, msg = verify_formula(u=self.u, input_value=(self, other.a, other.b), raise_exception=True)
            return formula

    def add_to_graph(self, g):
        """Add this theoretical object as a node in the target graph g.
        Recursively add directly linked objects unless they are already present in g.
        NetworkX automatically and quietly ignores nodes and edges that are already present."""
        g.add_node(self.rep_name())
        self.u.add_to_graph(g)

    def is_declaratively_member_of_class(self, c: ClassDeclaration) -> bool:
        return is_declaratively_member_of_class(u=self.u, phi=self, c=c)

    def is_derivably_member_of_class(self, c: ClassDeclaration) -> bool:
        return is_derivably_member_of_class(u=self.u, phi=self, c=c)

    def is_formula_syntactically_equivalent_to(self, phi: FlexibleFormula) -> bool:
        """Returns true if ⌜self⌝ is formula-syntactically-equivalent to ⌜o2⌝.

        Parameters:
        -----------
        o2 : Formula
            The formula with which to verify formula-equivalence.

        """
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        return self is phi

    def is_masked_formula_similar_to(self, phi: FlexibleFormula, mask: (None, frozenset[FreeVariable]) = None) -> bool:
        """Given two formulas o₁ (self) and o₂,
        and a finite set of variables 𝐌,
        return True if o₁ and o₂ are masked-formula-similar, False otherwise.

        Definition
        ----------
        Given two formulas o₁ (self) and o₂,
        and a finite set of variables 𝐌,
        o₁ and o₂ are masked-formula-similar if and only if:
         1. o₁ is formula-syntactically-equivalent to o₂, including the special case
            when both o₁ and o₂ are symbolic-equivalent to a variable 𝐱 in 𝐌,
         2. or the weaker condition that strictly one formula o₁ or o₂
            is symbolic-equivalent to a variable 𝐱 in 𝐌,
            and, denoting the other object the variable-observed-value,
            every variable-observed-value of 𝐱 are formula-syntactically-equivalent.
         3. or, if o₁ or o₂ are both formula, their components are masked-formula-similar.

        Note
        ----
        masked-formula-similitude is not a well-defined equivalence-class.
        In effect, equivalence-classes are reflexive, symmetric, and transitive.
        An obvious counterexample: (x + 1) ~ (5 + x).
        This is why it is called similitude and not equivalence.

        Parameters
        ----------
        phi : Formula
            A formula with which to verify masked-formula-similitude.

        mask: set
            Set of FreeVariable elements. If None, the empty set is assumed.

        """
        output, _values = self._is_masked_formula_similar_to(phi=phi, mask=mask)
        return output

    def _is_masked_formula_similar_to(self,
        phi: (CompoundFormula, FormulaStatement, FreeVariable, Connective, SimpleObjct, Formula),
        mask: (None, frozenset[FreeVariable]) = None, _values: (None, dict) = None) -> (bool, dict):
        """A "private" version of the is_masked_formula_similar_to method,
        with the "internal" term _values.

        Parameters
        ----------
        phi : Formula
            A formula with which to verify masked-formula-similitude.

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
        if o1 is phi:
            # Trivial case.
            return True, _values
        if o1.is_formula_syntactically_equivalent_to(phi=phi):
            # Sufficient condition.
            return True, _values
        if isinstance(o1, (CompoundFormula, FormulaStatement)) and isinstance(phi, (CompoundFormula, FormulaStatement)):
            # When both o1 and o2 are formula,
            # verify that their components are masked-formula-similar.
            connective_output, _values = o1.connective._is_masked_formula_similar_to(phi=phi.connective, mask=mask,
                _values=_values)
            if not connective_output:
                return False, _values
            # Arities are necessarily equal.
            if o1.connective is self.u.c1.object_reference:
                # The unary object-reference is a special case,
                # we are referencing objects (especially variables).
                # Instead of recursively calling is_masked_formula_similar_to(),
                # we test for alpha-equivalence.
                phi_variable = o1.terms[0]
                psi_variable = phi.terms[0]
                term_output = is_alpha_equivalent_to(u=u, phi=phi_variable, psi=psi_variable)
                if not term_output:
                    return False, _values
            else:
                for i in range(len(o1.terms)):
                    term_output, _values = o1.terms[i]._is_masked_formula_similar_to(phi=phi.terms[i], mask=mask,
                        _values=_values)
                    if not term_output:
                        return False, _values
                return True, _values
        if o1 not in mask and phi not in mask:
            # We know o1 and o2 are not formula-syntactically-equivalent,
            # and we know they are not in the mask.
            return False, _values
        if o1 in mask:
            variable = phi
            newly_observed_value = o1
            if variable in _values:
                already_observed_value = _values[variable]
                if not newly_observed_value.is_formula_syntactically_equivalent_to(phi=already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        if phi in mask:
            variable = o1
            newly_observed_value = phi
            if variable in _values:
                already_observed_value = _values[variable]
                if not newly_observed_value.is_formula_syntactically_equivalent_to(phi=already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        return True, _values

    @property
    @abc.abstractmethod
    def is_strictly_propositional(self) -> bool:
        """Informs if a formula is propositional.

        :return: True if the formula is propositional, False otherwise.
        """
        raise NotImplementedError(
            'The is_strictly_propositional property is abstract, it must be implemented by the child class.')

    def substitute(self, substitution_map: dict, lock_variable_scope=None,
        substitute_constants_with_values: bool = True):
        """Given a formula o₁ (self),
        and a substitution map 𝐌,
        return a formula o₂
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
        top-down, left-to-right, depth-first, connective-before-terms.

        Parameters
        ----------
        substitution_map : dict
            A dictionary of formula pairs (o, o'),
            where o is the original formula in o₁,
            and o' is the substitute formula in o₂.

        """
        # TODO: substitute() method: add a data validation step to verify that variables are in the same universe as the root formula.
        lock_variable_scope = True if lock_variable_scope is None else lock_variable_scope
        substitution_map = dict() if substitution_map is None else substitution_map
        assert isinstance(substitution_map, dict)
        output = None
        for key, value in substitution_map.items():
            # FreeVariable instances may be of type contextlib._GeneratorContextManager
            # when used inside a with statement.
            pass  # assert isinstance(key, TheoreticalObjct)  ##### XXXXX  # verify(  #  #  #  #  # isinstance(value, (  #    TheoreticalObjct, contextlib._GeneratorContextManager)),  #    'The value component of this key/value pair in this '  #    'substitution map is  #    not an instance of TheoreticalObjct.',  #    key=key, value=value,  #    value_type=type(value), self2=self)  # A formula connective cannot be replaced by  #    a simple-objct.  # But a simple-object could be replaced by a formula,  # if that formula "yields" such simple-objects.  # TODO: Implement clever rules here  #  to avoid ill-formed formula,  #   or let the formula constructor do the work.  #  #  assert type(key) == type(value) or isinstance(  #    value, FreeVariable) or  #  #  #  isinstance(  #    key, FreeVariable)  # If these are formula, their arity must be  #  equal  # to prevent the creation of an ill-formed formula.  # NO, THIS IS WRONG.  #  TODO: Re-analyze this point.  # assert not isinstance(key, Formula) or key.arity  #   == value.arity
        # Because the scope of variables is locked, the substituted formula must create "duplicates" of all variables.
        # During this process, we reuse the variable symbols, but we let auto-indexing re-numbering the new variables.
        # During this process, we must of course assure the consistency of the is_strictly_propositional property.
        variables_list = get_formula_unique_variable_ordered_set(u=self.u, phi=self)
        # self.get_unique_variable_ordered_set(substitute_constants_with_values=substitute_constants_with_values))
        x: FreeVariable
        for x in variables_list:
            variable_is_strictly_propositional: bool = x.is_strictly_propositional
            if x not in substitution_map.keys():
                # Call declare_variable() instead of v()
                # to explicitly manage variables scope locking.
                x2 = self.u.declare_variable(symbol=x.nameset.symbol,
                    is_strictly_propositional=variable_is_strictly_propositional)
                substitution_map[x] = x2

        # Now we may proceed with substitution.
        if self in substitution_map:
            return substitution_map[self]
        elif isinstance(self, CompoundFormula):
            # If both key / value are formulae,
            #   we must check for formula-equivalence,
            #   rather than python-object-equality.
            for k, v in substitution_map.items():
                if self.is_formula_syntactically_equivalent_to(phi=k):
                    return v

            # If the formula itself is not matched,
            # the next step consist in decomposing it
            # into its constituent parts, i.e. connective and terms,
            # to apply the substitution operation on these.
            connective = self.connective.substitute(substitution_map=substitution_map,
                lock_variable_scope=lock_variable_scope)
            terms = tuple(
                p.substitute(substitution_map=substitution_map, lock_variable_scope=False) for p in self.terms)
            phi = self.u.declare_compound_formula(connective, *terms, lock_variable_scope=lock_variable_scope)
            return phi
        else:
            return self

    def iterate_connectives(self, include_root: bool = True):
        """Iterate through this and all the formulas it contains recursively, providing
        they are connectives."""
        return (r for r in self.iterate_theoretical_objcts_references(include_root=include_root) if
            r.is_derivably_member_of_class(c=self.u.c2.connective))

    def iterate_theoretical_objcts_references(self, include_root: bool = True, visited: (None, set) = None,
        substitute_constants_with_values: bool = True, substitute_statements_with_formula: bool = True,
        substitute_formula_with_components: bool = True):
        """Iterate through this and all the formulas it contains recursively.
        """
        # TODO: Merge methods iterate_statements_in_theory_chain and iterate_theoretical_objcts_references
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[Composable, None, None]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        pass

    def export_interactive_graph(self, output_path: str, pyvis_graph: (None, pyvis.network) = None,
        encoding: (None, Encoding) = None, label_wrap_size: (None, int) = None,
        title_wrap_size: (None, int) = None) -> None:
        """Export a formula as a statement dependency graph in an HTML page with
        visJS, thanks to the pyvis theory."""
        pyvis_graph = prioritize_value(pyvis_graph, pyvis.network.Network(directed=True))
        label_wrap_size = prioritize_value(label_wrap_size, pyvis_configuration.label_wrap_size)
        title_wrap_size = prioritize_value(title_wrap_size, pyvis_configuration.title_wrap_size)
        pyvis_graph: pyvis.network.Network
        node_id = self.rep_symbol(encoding=encodings.plaintext)
        if node_id not in pyvis_graph.get_nodes():
            kwargs = None
            if is_in_class_OBSOLETE(self, classes_OBSOLETE.axiom_inclusion):
                self: AxiomInclusion
                kwargs = pyvis_configuration.axiom_inclusion_args
                ref = '' if self.ref is None else f'({self.rep_ref(encoding=encoding)}) '
                bold = True if ref != '' else False
                node_label = f'{self.rep_symbol(encoding=encoding)} {ref}: ' \
                             f'{self.rep_natural_language(encoding=encoding)}'
                if label_wrap_size is not None:
                    node_label = '\n'.join(textwrap.wrap(text=node_label, width=label_wrap_size))
                pyvis_graph.add_node(node_id, label=node_label, **kwargs)
            elif is_in_class_OBSOLETE(self, classes_OBSOLETE.definition_inclusion):
                self: DefinitionInclusion
                kwargs = pyvis_configuration.definition_inclusion_args
                ref = '' if self.ref is None else f'({self.rep_ref(encoding=encoding)}) '
                bold = True if ref != '' else False
                node_label = f'{self.rep_symbol(encoding=encoding)} {ref}: ' \
                             f'{self.rep_natural_language(encoding=encoding)}'
                if label_wrap_size is not None:
                    node_label = '\n'.join(textwrap.wrap(text=node_label, width=label_wrap_size))
                pyvis_graph.add_node(node_id, label=node_label, **kwargs)
            elif is_in_class_OBSOLETE(self, classes_OBSOLETE.inferred_proposition):
                self: InferredStatement
                kwargs = pyvis_configuration.inferred_statement_args
                ref = '' if self.ref is None else f'({self.rep_ref(encoding=encoding)}) '
                bold = True if ref != '' else False
                node_label = f'{self.rep_symbol(encoding=encoding)} {ref}: ' \
                             f'{self.rep_formula(encoding=encoding)}'
                if label_wrap_size is not None:
                    node_label = '\n'.join(textwrap.wrap(text=node_label, width=label_wrap_size))
                node_title = self.rep_report(encoding=encoding, proof=True)
                if title_wrap_size is not None:
                    node_title = '\n'.join(textwrap.wrap(text=node_title, width=title_wrap_size))
                pyvis_graph.add_node(node_id, label=node_label, title=node_title, labelHighlightBold=bold, **kwargs)
                for term in self.terms:
                    if isinstance(term, tuple):
                        # variable-substitution uses a tuple as term.
                        for x in term:
                            x.export_interactive_graph(output_path=None, pyvis_graph=pyvis_graph, encoding=encoding,
                                label_wrap_size=label_wrap_size, title_wrap_size=title_wrap_size)
                            term_node_id = x.rep_symbol(encoding=encodings.plaintext)
                            if term_node_id in pyvis_graph.get_nodes():
                                pyvis_graph.add_edge(source=term_node_id, to=node_id)
                    else:
                        term.export_interactive_graph(output_path=None, pyvis_graph=pyvis_graph, encoding=encoding,
                            label_wrap_size=label_wrap_size, title_wrap_size=title_wrap_size)
                        term_node_id = term.rep_symbol(encoding=encodings.plaintext)
                        if term_node_id in pyvis_graph.get_nodes():
                            pyvis_graph.add_edge(source=term_node_id, to=node_id)
        if is_derivably_member_of_class(u=self.u, phi=self, c=self.u.c2.theory_derivation):
            self: TheoryDerivation
            for statement in self.statements:
                # Bug fix: sections should not be Formulas but DecorativeObjects!
                if not isinstance(statement, Section):
                    statement.export_interactive_graph(output_path=None, pyvis_graph=pyvis_graph, encoding=encoding,
                        label_wrap_size=label_wrap_size, title_wrap_size=title_wrap_size)
        if output_path is not None:
            pyvis_graph.options.physics.solver = 'barnesHut'
            pyvis_graph.options.physics.barnesHut.gravitationalConstant = -5900
            pyvis_graph.options.physics.barnesHut.centralGravity = 0.35
            pyvis_graph.options.physics.barnesHut.springLength = 50
            pyvis_graph.options.physics.barnesHut.springConstant = 0.08
            pyvis_graph.options.physics.barnesHut.damping = 0.38
            pyvis_graph.options.physics.barnesHut.avoidOverlap = 0.49
            pyvis_graph.toggle_physics(True)
            # pyvis_graph.show_buttons(filter_=['physics'])
            pyvis_graph.save_graph(output_path)

    def compose_formula(self) -> collections.abc.Generator[Composable, None, None]:
        yield from self.compose_symbol()

    def rep_formula(self, encoding: (None, Encoding) = None, expand: (None, bool) = None) -> str:
        """Return a formula representation, which is equivalent to a symbolic representation for
        non-formula objects.
        """
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_formula(), encoding=encoding)


def substitute_xy(o, x, y):
    """Return the result of a *substitution* of x with y on o."""
    verify(isinstance(o, Formula), msg='o is not a TheoreticalObjct.')
    verify(isinstance(x, Formula), msg='x is not a TheoreticalObjct.')
    verify(isinstance(y, Formula), msg='y is not a TheoreticalObjct.')
    return o.substitute(substitution_map={x: y})


class Variable(Formula):
    """For future development."""
    pass


class BoundVariable(Variable):
    """For future development."""
    pass


class FreeVariable(Variable):
    """

    The defining-properties of a variable are:
     - Being an instance of the Variable class
     - The scope-formula of the variable
     - The index-position of the variable in its scope-formula
    """

    class Status(repm.ValueName):
        pass

    scope_initialization_status = Status('scope_initialization_status')
    closed_scope_status = Status('closed_scope_status')

    def __init__(self, u: UniverseOfDiscourse, status: (None, FreeVariable.Status) = None,
        scope: (None, CompoundFormula, typing.FrozenSet[CompoundFormula]) = None,
        symbol: (None, str, StyledText) = None, index: (None, int) = None, auto_index: (None, bool) = None,
        dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
        abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
        explicit_name: (None, str, StyledText) = None, is_strictly_propositional: (None, bool) = None,
        echo: (None, bool) = None) -> None:
        echo = prioritize_value(echo, configuration.echo_variable_declaration, configuration.echo_default, False)
        status = prioritize_value(status, FreeVariable.scope_initialization_status)
        scope = prioritize_value(scope, frozenset())
        self._is_strictly_propositional = prioritize_value(is_strictly_propositional, False)
        scope = {scope} if isinstance(scope, CompoundFormula) else scope
        verify(isinstance(scope, frozenset), 'The scope of a FreeVariable must be of python type frozenset.')
        verify(isinstance(status, FreeVariable.Status),
            'The status of a FreeVariable must be of the FreeVariable.Status type.')
        self._status = status
        self._scope = scope
        assert isinstance(u, UniverseOfDiscourse)
        symbol = prioritize_value(symbol, configuration.default_variable_symbol)
        if isinstance(symbol, str):
            # By default, variables are represented in bold style.
            symbol = StyledText(plaintext=symbol, text_style=text_styles.serif_bold)
        super().__init__(u=u, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=False)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.variable)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='variable')

    def echo(self):
        self.rep_report()

    def extend_scope(self, phi):
        # Support for the with pythonic syntax
        # Start building  variable scope
        verify(self._status == FreeVariable.scope_initialization_status,
            'The scope of an instance of FreeVariable can only be extended if it is open.', phi=phi, self2=self)
        # Close variable scope
        verify(isinstance(phi, CompoundFormula), 'Scope extensions of FreeVariable must be of type Formula.')
        self._scope = self._scope.union({phi})

    def is_masked_formula_similar_to(self, phi, mask, _values):
        assert isinstance(phi, Formula)
        if isinstance(phi, FreeVariable):
            if phi in mask:
                # o2 is a variable, and it is present in the mask.
                # first, we must check if it is already in the dictionary of values.
                if phi in _values:
                    # the value is already present in the dictionary.
                    known_value = _values[phi]
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
                    _values[phi] = self
                    return True, _values
        if not isinstance(phi, SimpleObjct):
            # o1 (self) is a simple-objct, and o2 is something else.
            # in consequence, masked-formula-similitude is no longer preserved.
            return False, _values
        # o2 is not a variable.
        return self.is_formula_syntactically_equivalent_to(phi=phi), _values

    @property
    def is_strictly_propositional(self) -> bool:
        """A variable is denoted as propositional if a strict constraint is imposed on the objects it may be substituted with, that is only propositional objects.

        When a variable is declared as propositional, punctilious_obsolete_20240114 assures through data-validation that it is never substituted by a non-propositional object.
        """
        return self._is_strictly_propositional

    def lock_scope(self):
        # Support for the "with u.v:" pythonic syntax.
        # If the variable scope was already closed, this method has no effect.
        self._status = FreeVariable.closed_scope_status

    def rep_report(self, encoding: (None, Encoding) = None, proof: (None, bool) = None):
        return f'Let {self.rep_name(encoding=encoding)} be a variable in ' \
               f'{self.u.rep_name(encoding=encoding)}' + '\n'

    @property
    def scope(self):
        """The scope of a free variable is the set of the formula where the variable is used.

        :return:
        """
        return self._scope


class ConstantDeclaration(Formula):
    def __init__(self, value: FlexibleFormula, u: UniverseOfDiscourse, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, echo: (None, bool) = None):
        """
        """
        echo = prioritize_value(echo, configuration.echo_formula_declaration, configuration.echo_default, False)
        if isinstance(symbol, str):
            symbol = SerifNormal(symbol)
        if symbol is None:
            symbol = configuration.default_constant_symbol
        self._value = value
        super().__init__(symbol=symbol, auto_index=auto_index, index=index, u=u, echo=False)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.constant_declaration)
        u.cross_reference_constant_OBSOLETE(self)
        verify(assertion=value.u is self.u,
            msg=f'The universe-of-discourse ⌜{self.u}⌝ of the constant ⌜{self}⌝ is inconsistent with the universe-of-discourse of its value ⌜{value}⌝.')
        if echo:
            self.echo()

    def __repr__(self):
        return self.rep(expand=True)

    def __str__(self):
        return self.rep(expand=True)

    def compose(self, **kwargs) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_constant_declaration(o=self)
        return output

    def is_strictly_propositional(self) -> bool:
        return self.value.is_strictly_propositional

    def iterate_theoretical_objcts_references(self, include_root: bool = True, visited: (None, set) = None,
        substitute_constants_with_values: bool = True):
        """Iterate through this and all the formulas it contains recursively."""
        # TODO: Merge methods iterate_statements_in_theory_chain and iterate_theoretical_objcts_references
        visited = set() if visited is None else visited
        if substitute_constants_with_values:
            yield from self.value.iterate_theoretical_objcts_references(include_root=include_root, visited=visited,
                substitute_constants_with_values=substitute_constants_with_values)
        else:
            if include_root and self not in visited:
                yield self
                visited.update({self})

    @property
    def value(self) -> Formula:
        return self._value


class CompoundFormula(Formula):
    """A compoud-formula is a formula.
    It is also a tuple (U, r, p1, p1, p2, ..., pn)

    Definition
    ----------
    A formula 𝜑 is a tuple (◆, 𝒳) where:
     * ◆ is a connective.
     * 𝒳 is a finite tuple of terms
       whose elements are formulas, possibly formulae.

    Defining properties:
    --------------------
    The defining-properties of a formula are:
     * Being a formula.
     * A connective r.
     * A finite tuple of terms.

     To do list
     ----------
     - TODO: Question: supporting connective as subformula, where the subformula
        would be a function whose domain would be the class of connectives,
        could be an interesting approach to extend the expressiveness of
        Punctilious as a formal language. Consider this in later developments.

    Attributes
    ----------
    connective : (Connective, FreeVariable)

    """

    function_call = repm.ValueName('function-call')
    infix = repm.ValueName('infix-operator')
    prefix = repm.ValueName('prefix-operator')
    postfix = repm.ValueName('postfix-operator')
    collection = repm.ValueName('collection-operator')

    def __init__(self, connective: (Connective, FreeVariable), terms: tuple, u: UniverseOfDiscourse,
        symbol: (None, str, StyledText) = None, index: (None, int) = None, auto_index: (None, bool) = None,
        lock_variable_scope: bool = False, echo: (None, bool) = None):
        """
        """
        echo = prioritize_value(echo, configuration.echo_formula_declaration, configuration.echo_default, False)
        self.variables = dict()  # TODO: Check how to make dict immutable after construction.
        # self.formula_index = theory.crossreference_formula(self)
        if symbol is None:
            symbol = configuration.default_formula_symbol
        # if nameset is None:
        #    symbol = configuration.default_formula_symbol
        #    index = u.index_symbol(symbol=symbol)
        #    nameset = NameSet(symbol=symbol, index=index)
        # if isinstance(nameset, str):
        #    # If symbol was passed as a string,
        #    # assume the base was passed without index.
        #    # TODO: Analyse the string if it ends with index in subscript characters.
        #    symbol = StyledText(plaintext=nameset, text_style=text_styles.serif_italic)
        #    index = u.index_symbol(symbol=symbol)
        #    nameset = NameSet(symbol=symbol, index=index)
        self.connective = connective
        terms = terms if isinstance(terms, tuple) else tuple([terms])
        # verify(assertion=len(terms) > 0,
        #     msg='Ill-formed formula error. The number of terms in this formula is zero. 0-ary connectives are currently not supported. Use a simple-object instead.',
        #     severity=verification_severities.error, raise_exception=True, connective=self.connective,
        #     len_terms=len(terms))
        if not is_declaratively_member_of_class(u=u, phi=self.connective, c=u.c2.free_variable):
            # if not is_in_class_OBSOLETE(self.connective, classes_OBSOLETE.variable):
            verify(self.connective.arity is None or self.connective.arity == len(terms),
                msg=f'Ill-formed formula error. Connective ⌜{self.connective}⌝ is defined with a fixed arity constraint of {self.connective.arity} but the number of terms provided to construct this formula is {len(terms)}.',
                severity=verification_severities.error, raise_exception=True, connective=self.connective,
                connective_arity=self.connective.arity, len_terms=len(terms), terms=terms)
            verify(self.connective.min_arity is None or self.connective.min_arity >= len(terms),
                msg=f'Ill-formed formula error. Connective ⌜{self.connective}⌝ is defined with a minimum arity constraint of {self.connective.min_arity} but the number of terms provided to construct this formula is {len(terms)}.',
                severity=verification_severities.error, raise_exception=True, connective=self.connective,
                connective_min_arity=self.connective.min_arity, len_terms=len(terms), terms=terms)
            verify(assertion=self.connective.max_arity is None or self.connective.max_arity >= len(terms),
                msg=f'Ill-formed formula error. Connective ⌜{self.connective}⌝ is defined with a maximum arity constraint of {self.connective.max_arity} but the number of terms provided to construct this formula is {len(terms)}.',
                severity=verification_severities.error, raise_exception=True, connective=self.connective,
                connective_max_arity=self.connective.max_arity, len_terms=len(terms), terms=terms)
        self.arity = len(terms)
        self.terms = terms
        # super().__init__(nameset=nameset, u=u, echo=False)
        super().__init__(symbol=symbol, index=index, auto_index=auto_index, u=u, echo=False)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.compound_formula)
        verify(assertion=is_declaratively_member_of_class(u=self.u, phi=connective,
            c=self.u.c2.connective) or is_declaratively_member_of_class(u=self.u, phi=connective,
            c=self.u.c2.free_variable), msg='The connective of this formula is neither a connective, nor a variable.',
            formula=self, connective=connective)
        verify(assertion=connective.u is self.u,
            msg=f'The universe-of-discourse ⌜{connective.u}⌝ of the connective in the formula is inconsistent with the universe-of-discourse ⌜{self.u}⌝ of the formula.',
            formula=self, connective=connective)
        self.cross_reference_variables()
        for p in terms:
            verify_formula(u=self.u, input_value=p, arg='p')
            if is_declaratively_member_of_class(u=self.u, phi=p,
                c=self.u.c2.free_variable) and self.connective is not self.u.c1.object_reference:
                # if is_in_class_OBSOLETE(p, classes_OBSOLETE.variable) and self.connective is not
                # self.u.c1.object_reference:
                p.extend_scope(self)
            verify(p.u is self.u,
                f'The universe-of-discourse ⌜p_u⌝ of the term ⌜p⌝ in the formula ⌜formula⌝ is inconsistent with the universe-of-discourse ⌜formula_u⌝ of the formula.',
                p=p, p_u=p.u, formula=self, formula_u=self.u)
        if lock_variable_scope:
            self.lock_variable_scope()
        if echo:
            self.echo()

    def __repr__(self):
        return self.rep(expand=True)

    def __str__(self):
        return self.rep(expand=True)

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='formula')

    def compose_collection_operator(self) -> collections.abc.Generator[Composable, None, None]:
        global text_dict
        start: StyledText = prioritize_value(self.connective.collection_start, text_dict.open_parenthesis)
        sep: StyledText = prioritize_value(self.connective.collection_separator, text_dict.comma)
        end: StyledText = prioritize_value(self.connective.collection_end, text_dict.close_parenthesis)
        yield start
        first_p: bool = True
        for p in self.terms:
            if not first_p:
                yield sep
            else:
                first_p = False
            yield from p.compose_formula()
        yield end

    def compose_formula(self) -> collections.abc.Generator[Composable, None, None]:
        # if is_in_class_OBSOLETE(self.connective, classes_OBSOLETE.variable):
        if is_declaratively_member_of_class(u=self.u, phi=self.connective, c=self.u.c2.free_variable):
            # If the connective of this formula is a variable,
            # it has no arity, neither a representation-mode.
            # In this situation, our design-choice is to
            # fallback on the function-call representation-mode.
            # In future developments, we may choose to allow
            # the "decoration" of variables with arity,
            # and presentation-mode to improve readability.
            yield from self.compose_function_call()
        else:
            match self.connective.formula_rep:
                case CompoundFormula.function_call:
                    yield from self.compose_function_call()
                case CompoundFormula.infix:
                    yield from self.compose_infix_operator()
                case CompoundFormula.prefix:
                    yield from self.compose_prefix_operator()
                case CompoundFormula.postfix:
                    yield from self.compose_postfix_operator()
                case CompoundFormula.collection:
                    yield from self.compose_collection_operator()
                case _:
                    # Fallback notation.
                    yield from self.compose_function_call()

    def compose_function_call(self) -> collections.abc.Generator[Composable, None, None]:
        global text_dict
        yield from self.connective.compose_formula()
        yield text_dict.open_parenthesis
        first_item = True
        for p in self.terms:
            if not first_item:
                yield text_dict.compound_formula_term_separator
            yield from p.compose_formula()
            first_item = False
        yield text_dict.close_parenthesis

    def compose_infix_operator(self) -> collections.abc.Generator[Composable, None, None]:
        verify(assertion=self.connective.arity == 2,
            msg='Connective is not binary, formula-representation-style is infix.', connective=self.connective,
            slf=self)
        global text_dict
        yield text_dict.open_parenthesis
        yield from self.terms[0].compose_formula()
        yield text_dict.space
        yield from self.connective.compose_formula()
        yield text_dict.space
        yield from self.terms[1].compose_formula()
        yield text_dict.close_parenthesis

    def compose_postfix_operator(self) -> collections.abc.Generator[Composable, None, None]:
        verify(assertion=len(self.terms) == 1,
            msg='Postfix-operator formula representation is used but arity is not equal to 1', slf=self)
        global text_dict
        yield text_dict.open_parenthesis
        yield from self.terms[0].compose_formula()
        yield text_dict.close_parenthesis
        yield from self.connective.compose_formula()

    def compose_prefix_operator(self) -> collections.abc.Generator[Composable, None, None]:
        verify(assertion=len(self.terms) == 1,
            msg='Prefix-operator formula representation is used but arity is not equal to 1', slf=self)
        global text_dict
        yield from self.connective.compose_formula()
        yield text_dict.open_parenthesis
        yield from self.terms[0].compose_formula()
        yield text_dict.close_parenthesis

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[Composable, None, None]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        global text_dict
        yield text_dict.let
        yield text_dict.space
        yield from self.compose_symbol()
        yield text_dict.space
        yield text_dict.be
        yield text_dict.space
        yield text_dict.the
        yield text_dict.space
        yield from self.compose_class()
        yield text_dict.space
        yield from self.compose_formula()
        yield text_dict.space
        yield text_dict.in2
        yield text_dict.space
        yield from self.u.compose_symbol()
        yield text_dict.period

    def crossreference_variable(self, x):
        """During construction, cross-reference a variable 𝓍
        with its parent formula if it is not already cross-referenced,
        and return its 0-based index in Formula.variables."""
        assert isinstance(x, FreeVariable)
        x.formula = self if x.formula is None else x.formula
        assert x.formula is self
        if x not in self.variables:
            self.variables = self.variables + tuple([x])
        return self.variables.index(x)

    def cross_reference_variables(self):
        # TODO: Iterate through formula filtering on variable placeholders.
        # TODO: Call cross_reference_variable on every variable placeholder.
        pass  # assert False

    def echo(self):
        repm.prnt(self.rep_report())

    def is_formula_syntactically_equivalent_to(self, phi: FlexibleFormula) -> bool:
        """Return true if ⌜self⌝ is formula-syntactically-equivalent to ⌜o2⌝.

        Parameters:
        -----------
        o2 : Formula
            The formula with which to verify formula-equivalence.

        """
        if self is phi:
            return True
        # if o2 is a formula-statement, retrieve its formula.
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        # phi = phi.valid_proposition if is_in_class(phi, classes.formula_statement) else phi
        if self is phi:
            # Trivial case.
            return True
        if not isinstance(phi, CompoundFormula):
            return False
        if not self.connective.is_formula_syntactically_equivalent_to(phi=phi.connective):
            return False
        # Arities are necessarily equal.
        for i in range(len(self.terms)):
            if not self.terms[i].is_formula_syntactically_equivalent_to(phi=phi.terms[i]):
                return False
        return True

    @property
    def is_strictly_propositional(self) -> bool:
        """Tell if the formula is a logic-proposition.

        This property is directly inherited from the formula-is-proposition
        attribute of the formula's connective."""
        # if is_in_class_OBSOLETE(self.connective, classes_OBSOLETE.variable):
        if is_declaratively_member_of_class(u=self.u, phi=self.connective, c=self.u.c2.free_variable):
            # TODO: IDEA: Is it a good idea to equip FreeVariable with a strictly-proposition property?
            return False
        else:
            return self.connective.signal_proposition

    def iterate_theoretical_objcts_references(self, include_root: bool = True, visited: (None, set) = None,
        substitute_constants_with_values: bool = True):
        """Iterate through this and all the formulas it contains recursively."""
        # TODO: Merge methods iterate_statements_in_theory_chain and iterate_theoretical_objcts_references
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        if self.connective not in visited:
            yield self.connective
            visited.update({self.connective})
            yield from self.connective.iterate_theoretical_objcts_references(include_root=False, visited=visited,
                substitute_constants_with_values=substitute_constants_with_values)
        for term in set(self.terms).difference(visited):
            yield term
            visited.update({term})
            yield from term.iterate_theoretical_objcts_references(include_root=False, visited=visited,
                substitute_constants_with_values=substitute_constants_with_values)

    def list_theoretical_objcts_recursively_OBSOLETE(self, ol: (None, frozenset) = None,
        extension_limit: (None, Statement) = None):
        """Return a python frozenset of this formula and all theoretical_objcts it contains."""
        ol = frozenset() if ol is None else ol
        ol = ol.union({self})
        if self.connective not in ol:
            ol = ol.union(self.connective.list_theoretical_objcts_recursively_OBSOLETE(ol=ol))
        for p in self.terms:
            if p not in ol:
                ol = ol.union(p.list_theoretical_objcts_recursively_OBSOLETE(ol=ol))
        return ol

    def lock_variable_scope(self, substitute_constants_with_values: bool = True):
        """Variable scope must be locked when the formula construction
        is completed."""
        variables_list = get_formula_unique_variable_ordered_set(u=self.u, phi=self)
        # variables_list = self.get_unique_variable_ordered_set(
        #    substitute_constants_with_values=substitute_constants_with_values)
        for x in variables_list:
            x.lock_scope()

    def rep(self, encoding: (None, Encoding) = None, expand: (None, bool) = None) -> str:
        expand = True if expand is None else expand
        assert isinstance(expand, bool)
        if expand:
            return self.rep_formula(encoding=encoding, expand=expand)
        else:
            return super().rep(encoding=encoding, expand=expand)

    def rep_function_call(self, encoding: (None, Encoding) = None, expand: (None, bool) = None) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_function_call(), encoding=encoding)

    def rep_infix_operator(self, encoding: (None, Encoding) = None, expand=(None, bool), **kwargs) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_infix_operator(), encoding=encoding)

    def rep_postfix_operator(self, encoding: (None, Encoding) = None, expand=None) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_postfix_operator(), encoding=encoding)

    def rep_as_prefix_operator(self, encoding: (None, Encoding) = None, expand=None) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_prefix_operator(), encoding=encoding)

    def rep_formula(self, encoding: (None, Encoding) = None, expand: bool = True) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_formula(), encoding=encoding)


class ParagraphHeader(repm.ValueName):
    """TODO: Replace this with ComposableText"""

    def __init__(self, name, symbol_base, natural_name, abridged_name):
        self.symbol_base = symbol_base
        if isinstance(natural_name, str):
            natural_name = SansSerifBold(natural_name)
        self.natural_name = natural_name
        if isinstance(abridged_name, str):
            abridged_name = SansSerifBold(abridged_name)
        self.abridged_name = abridged_name
        super().__init__(name)

    def __repr__(self):
        return self.rep(encoding=encodings.plaintext)

    def __str__(self):
        return self.rep(encoding=encodings.plaintext)

    def rep(self, encoding: (None, Encoding) = None, cap: (None, bool) = None, expand: (None, bool) = None):
        # TODO: Implement encoding
        return self.natural_name


class ParagraphHeaders(repm.ValueName):
    # axiom = TitleCategory('axiom', 's', 'axiom', 'axiom')
    axiom_declaration = ParagraphHeader('axiom_declaration', 'a', SansSerifBold('axiom'), 'axiom')
    axiom_inclusion = ParagraphHeader('axiom_inclusion', 's', SansSerifBold('axiom'), 'axiom')
    axiom_schema_declaration = ParagraphHeader('axiom_schema_declaration', 'a', SansSerifBold('axiom schema'),
        'axiom schema')
    axiom_schema_inclusion = ParagraphHeader('axiom_schema_inclusion', 's', SansSerifBold('axiom schema'),
        'axiom schema')
    corollary = ParagraphHeader('corollary', 's', 'corollary', 'cor.')
    definition_declaration = ParagraphHeader('definition_declaration', 'd', SansSerifBold('definition'), 'def.')
    definition_inclusion = ParagraphHeader('definition_inclusion', 's', SansSerifBold('definition'), 'def.')
    hypothesis = ParagraphHeader('hypothesis', 'H', 'hypothesis', 'hyp.')
    inference_rule_declaration = ParagraphHeader('inference_rule', 'I', 'inference rule', 'inference rule')
    inference_rule_inclusion = ParagraphHeader('inference_rule_inclusion', 'I', 'inference rule', 'inference rule')
    inferred_proposition = ('inferred_proposition', 's', 'inferred-proposition')
    lemma = ParagraphHeader('lemma', 's', 'lemma', 'lem.')
    proposition = ParagraphHeader('proposition', 's', 'proposition', 'prop.')
    connective_declaration = ParagraphHeader('connective_declaration', 's', 'proposition', 'prop.')
    theorem = ParagraphHeader('theorem', 's', 'theorem', 'thrm.')
    theory_derivation = ParagraphHeader('theory_derivation', 't', 'theory derivation sequence', 'theo.')
    informal_definition = ParagraphHeader('informal definition', StyledText(plaintext='note', unicode='🗅'),
        'informal definition', 'inf. def.')
    comment = ParagraphHeader('comment', StyledText(plaintext='note', unicode='🗅'), 'comment', 'cmt.')
    note = ParagraphHeader('note', StyledText(plaintext='note', unicode='🗅'), 'note', 'note')
    remark = ParagraphHeader('remark', StyledText(plaintext='note', unicode='🗅'), 'remark', 'rmrk.')
    warning = ParagraphHeader('warning', StyledText(plaintext='warning', unicode='🗅'), 'warning', 'warning')
    # Special categories
    uncategorized = ParagraphHeader('uncategorized', 's', 'uncategorized', 'uncat.')
    informal_assumption = ParagraphHeader('informal assumption',
        StyledText(plaintext='informal assumption', unicode='🗅'), 'informal assumption', 'informal assumption')
    informal_proposition = ParagraphHeader('informal proposition',
        StyledText(plaintext='informal proposition', unicode='🗅'), 'informal proposition', 'informal proposition')
    informal_proof = ParagraphHeader('informal proof', StyledText(plaintext='informal proof', unicode='🗅'),
        'informal proof', 'informal proof')


paragraph_headers = ParagraphHeaders('paragraph_headers')


class Statement(Formula):
    """

    Definition
    ----------
    Given a theory 𝒯, a statement 𝒮 is a formula that:
     * announces some truth in 𝒯.

    There are three broad categories of statements:
    - contentual-statements (e.g. axiom-inclusion, definition-inclusion)
    - formula-statements
    - non-theoretical statements (decorative)

    For 𝒯 to be valid, all statements in 𝒯 must be valid.
    For 𝒯 to be consistent, all statements in 𝒯 must be consistent.
    etc.
    """

    def __init__(self, theory: TheoryDerivation, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, echo: (None, bool) = None):
        self._theory = theory
        echo = prioritize_value(echo, configuration.echo_statement, configuration.echo_default, False)
        u = theory.u
        self.statement_index = theory.crossreference_statement(self)
        self._paragraph_header = paragraph_header
        namespace = self._theory  # TODO: Cross-referencing the theory symbol as the nameset of
        # the statement is ugly, there's something wrong with the data model, correct it.
        super().__init__(u=u, symbol=symbol, index=index, auto_index=auto_index, namespace=namespace,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, echo=echo)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.statement)
        if echo:
            self.echo()

    @property
    def paragraph_header(self) -> ParagraphHeader:
        """The statement-category assigned to this statement.

        :return:
        """
        return self._paragraph_header

    @abc.abstractmethod
    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        raise NotImplementedError('This is an abstract method.')

    def echo(self):
        repm.prnt(self.rep_report())

    @property
    def t(self) -> TheoryDerivation:
        """The theory-derivation that contains this statement.

        Unabridged property: statement.theory"""
        return self.theory

    @property
    def theory(self) -> TheoryDerivation:
        """The theory-derivation that contains this statement.

        Abridged property: s.t

        This property may only be set once. In effect, moving statements
        between theory would lead to unstable theory."""
        return self._theory

    @theory.setter
    def theory(self, t: TheoryDerivation):
        verify(self._theory is None, '⌜theory⌝ property may only be set once.', slf=self, slf_theory=self._theory, t=t)
        self._theory = t

    @property
    def u(self) -> UniverseOfDiscourse:
        """The universe-of-discourse where this statement is declared.

        Unabridged property: statement.universe_of_discourse"""
        return self._u


class AxiomDeclaration(Formula):
    """The Axiom pythonic class models the elaboration of a _contentual_ _axiom_ in a
    _universe-of-discourse_.

    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, natural_language: (str, StyledText), u: UniverseOfDiscourse,
        symbol: (None, str, StyledText) = None, index: (None, int) = None, auto_index: (None, bool) = None,
        dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
        abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
        explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
        subtitle: (None, str, StyledText) = None, paragraph_header: (None, ParagraphHeader) = None,
        echo: (None, bool) = None):
        """

        :param natural_language: The axiom's content in natural-language.
        :param u: The universe-of-discourse.
        :param nameset:
        :param echo:
        """
        echo = prioritize_value(echo, configuration.echo_axiom_declaration, configuration.echo_default, False)
        if isinstance(natural_language, str):
            natural_language = natural_language.strip()
            verify(natural_language != '', 'Parameter natural-language is an empty string (after trimming).')
            natural_language = SansSerifItalic(natural_language)
        self._natural_language = natural_language
        paragraph_header = prioritize_value(paragraph_header, paragraph_headers.axiom_declaration)
        verify(
            assertion=paragraph_header is paragraph_headers.axiom_declaration or paragraph_header is paragraph_headers.axiom_schema_declaration,
            msg='paragraph-header must be either axiom-declaration, or axiom-schema-declaration.',
            paragraph_header=paragraph_header)
        symbol = prioritize_value(symbol, configuration.default_axiom_declaration_symbol)
        super().__init__(u=u, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, paragraph_header=paragraph_header, echo=False)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.axiom)
        u.a.declare_instance(a=self)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='axiom')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_axiom_declaration(o=self)
        return output

    def compose_natural_language(self) -> collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        yield text_dict.open_quasi_quote
        yield self.natural_language
        yield text_dict.close_quasi_quote
        return True

    def echo(self):
        repm.prnt(self.rep_report())

    def is_strictly_propositional(self) -> bool:
        """An axiom-declaration is not propositional by definition. Distinctively, it is possible to infer propositional statements from an axiom-declaration, cf. axiom-interpretation."""
        return False

    @property
    def natural_language(self) -> StyledText:
        return self._natural_language

    def rep_natural_language(self, encoding: (None, Encoding) = None, wrap: bool = None) -> str:
        return rep_composition(composition=self.compose_natural_language(), encoding=encoding, wrap=wrap)


class AxiomInclusion(Statement):
    """This python class models the inclusion of an :ref:`axiom<axiom_math_concept>` as a valid in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, a: AxiomDeclaration, t: TheoryDerivation, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_axiom_inclusion, configuration.echo_default, False)
        self._a = a
        self._locked = False
        t.crossreference_definition_endorsement(self)
        paragraph_header = prioritize_value(paragraph_header, paragraph_headers.axiom_inclusion)
        verify(
            assertion=paragraph_header is paragraph_headers.axiom_inclusion or paragraph_header is paragraph_headers.axiom_schema_inclusion,
            msg='paragraph-header must be either axiom-inclusion, or axiom-schema-inclusion.',
            paragraph_header=paragraph_header)
        symbol = prioritize_value(symbol, configuration.default_axiom_inclusion_symbol)
        super().__init__(theory=t, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, echo=False)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.axiom_inclusion)
        if echo:
            self.echo()

    @property
    def a(self) -> AxiomDeclaration:
        """The axiom of an axiom-inclusion.

        Unabridged property: axiom_inclusion.axiom"""
        return self.axiom

    @property
    def axiom(self) -> AxiomDeclaration:
        """The axiom of an axiom-inclusion.

        Abridged property: a.a"""
        return self._a

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='axiom-inclusion')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_axiom_inclusion_report(o=self, proof=proof)
        return output

    @property
    def is_strictly_propositional(self) -> bool:
        """By definition, an axiom-inclusion is not a propositional object."""
        return False

    @property
    def locked(self) -> bool:
        """When an axiom or definition is locked, the usage of the axiom-interpretation, respectively the definition-interpretation, inference-rule is no longer authorized on that axiom.

        A theory author should lock axioms and definitions once all axiom-interpretations, respectively definition-interpretations, have been derived from them. This protects the theory-derivation from the introduction of inconsistent statements.

        A theory author is of course free to unlock axiom-inclusions, the goal of this feature is not to make it technically impossible to re-interpret axioms and definitions, but rather to act as a strong reminder and prevent mistakes.
        """
        return self._locked

    @locked.setter
    def locked(self, v):
        self._locked = v

    def rep_natural_language(self, encoding: (None, Encoding) = None, wrap: bool = True) -> str:
        return self._a.rep_natural_language(encoding=encoding, wrap=wrap)


class InferenceRuleInclusion(Statement):
    """This python abstract class models the :ref:`inclusion<object_inclusion_math_concept>` of an :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>`.

    """

    def __init__(self, i: InferenceRuleDeclaration, t: TheoryDerivation, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        nameset: (None, str, NameSet) = None, echo: (None, bool) = None, proof: (None, bool) = None):
        verify_theory_derivation(input_value=t, arg='t')
        self._inference_rule = i
        paragraph_header = paragraph_headers.inference_rule_inclusion
        symbol = prioritize_value(symbol, configuration.default_inference_rule_inclusion_symbol)
        super().__init__(theory=t, paragraph_header=paragraph_headers, symbol=symbol, index=index,
            auto_index=auto_index, echo=False)
        t.crossreference_inference_rule_inclusion(self)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.inference_rule_inclusion)
        echo = prioritize_value(echo, configuration.echo_inference_rule_inclusion, configuration.echo_inclusion,
            configuration.echo_default, False)
        if echo:
            proof = prioritize_value(proof, configuration.echo_proof, True)
            repm.prnt(self.rep_report(proof=proof))

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        """This python method yields the default mathematical-class of the object in the *punctilious_obsolete_20240114* data model.
        """
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='inference-rule')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_inference_rule_inclusion_report(i=self, proof=proof)
        return output

    @property
    def definition(self) -> CompoundFormula:
        """This python property returns a formal definition of the object.

        :return: a formula.
        """
        return self.i.definition

    @property
    @abc.abstractmethod
    def check_premises_validity(self, **kwargs) -> bool:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        raise NotImplementedError(
            'The ⌜check_premises_validity⌝ method is abstract. It must be implemented in the child class.')

    @property
    @abc.abstractmethod
    def construct_formula(self, **kwargs) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        raise NotImplementedError(
            'The ⌜construct_formula⌝ method is abstract. It must be implemented in the child class.')

    @property
    @abc.abstractmethod
    def infer_formula_statement(self, *args, **kwargs) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        raise NotImplementedError(
            'The ⌜infer_formula_statement⌝ method is abstract. It must be implemented in the child class.')

    @property
    def is_strictly_propositional(self) -> bool:
        """By definition, an inference-rule-inclusion is not a propositional object."""
        return False

    @property
    @abc.abstractmethod
    def check_premises_validity(self, **kwargs):
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        raise NotImplementedError(
            'The ⌜check_inference_validity⌝ method is abstract. It must be implemented in the child class.')

    @property
    def i(self):
        """

        :return:
        """
        return self.inference_rule

    @property
    def inference_rule(self):
        return self._inference_rule

    # def verify_compatibility(self, *args):  #    return self.inference_rule.check_inference_validity(*args, t=self.theory)


class DefinitionDeclaration(Formula):
    """The Definition pythonic class models the elaboration of a _contentual_ _definition_ in a
    _universe-of-discourse_.

    """

    # class Premises(typing.NamedTuple):
    #    p_implies_q: FlexibleFormula

    def __init__(self, natural_language: str, u: UniverseOfDiscourse, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, echo: (None, bool) = None):
        """

        :param natural_language: The definition's content in natural-language.
        :param u: The universe-of-discourse.
        :param nameset:
        :param echo:
        """
        echo = prioritize_value(echo, configuration.echo_definition_declaration, configuration.echo_default, False)
        if isinstance(natural_language, str):
            natural_language = natural_language.strip()
            verify(natural_language != '', 'Parameter natural-language is an empty string (after trimming).')
            natural_language = SansSerifItalic(natural_language)
        self._natural_language = natural_language
        paragraph_header = prioritize_value(paragraph_header, paragraph_headers.definition_declaration)
        symbol = prioritize_value(symbol, configuration.default_definition_declaration_symbol)
        super().__init__(u=u, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, paragraph_header=paragraph_header, echo=False)
        u.d.declare_instance(d=self)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='definition')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_definition_declaration(o=self)
        return output

    def compose_natural_language(self) -> collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        yield text_dict.open_quasi_quote
        yield self.natural_language
        yield text_dict.close_quasi_quote
        return True

    def echo(self):
        repm.prnt(self.rep_report())

    def is_strictly_propositional(self) -> bool:
        """A definition-declaration is not propositional by definition. Distinctively, it is possible to infer propositional statements from a definition-declaration, cf. definition-interpretation."""
        return False

    @property
    def natural_language(self) -> (None, str):
        """The content of the axiom in natural-language."""
        return self._natural_language

    def rep_natural_language(self, encoding: (None, Encoding) = None, wrap: bool = None) -> str:
        return rep_composition(composition=self.compose_natural_language(), encoding=encoding, wrap=wrap)


class DefinitionInclusion(Statement):
    """This python class models the inclusion of a :ref:`definition<definition_math_concept>` as a valid in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, d: DefinitionDeclaration, t: TheoryDerivation, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):
        """Endorsement (aka include, endorse) an definition in a theory-elaboration.
        """
        echo = prioritize_value(echo, configuration.echo_definition_inclusion, configuration.echo_default, False)
        self._d = d
        self._locked = False
        t.crossreference_definition_endorsement(self)
        cat = paragraph_headers.definition_inclusion
        symbol = prioritize_value(symbol, configuration.default_definition_inclusion_symbol)
        super().__init__(theory=t, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, paragraph_header=cat,
            ref=ref, subtitle=subtitle, echo=False)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.definition_inclusion)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='definition-inclusion')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_definition_inclusion_report(o=self, proof=proof)
        return output

    @property
    def d(self):
        return self._d

    def echo(self):
        repm.prnt(self.rep_report())

    @property
    def locked(self) -> bool:
        """When an axiom or definition is locked, the usage of the axiom-interpretation, respectively the definition-interpretation, inference-rule is no longer authorized on that axiom.

        A theory author should lock axioms and definitions once all axiom-interpretations, respectively definition-interpretations, have been derived from them. This protects the theory-derivation from the introduction of inconsistent statements.

        A theory author is of course free to unlock axiom-inclusions, the goal of this feature is not to make it technically impossible to re-interpret axioms and definitions, but rather to act as a strong reminder and prevent mistakes.
        """
        return self._locked

    @locked.setter
    def locked(self, v):
        self._locked = v

    @property
    def is_strictly_propositional(self) -> bool:
        """By definition, a definition-inclusion is not a propositional object."""
        return False

    def rep_natural_language(self, encoding: (None, Encoding) = None, wrap: bool = True) -> str:
        return self._d.rep_natural_language(encoding=encoding, wrap=wrap)


class FormulaStatement(Statement):
    """

    Definition:
    -----------
    An formula-statement is a statement that expresses the validity of a formula in the parent
    theory.

    To do list
    ----------
    - TODO: Make FormulaStatement an abstract class

    """

    def __init__(self, theory: TheoryDerivation, valid_proposition: CompoundFormula,
        symbol: (None, str, StyledText) = None, index: (None, int) = None, auto_index: (None, bool) = None,
        dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
        abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
        explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
        subtitle: (None, str, StyledText) = None, paragraphe_header: (None, ParagraphHeader) = None,
        echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_statement, configuration.echo_default, False)
        verify(assertion=theory.u is valid_proposition.u,
            msg='The universe-of-discourse of this formula-statement''s theory-elaboration is '
                'inconsistent with the universe-of-discourse of the valid-proposition of that '
                'formula-statement.')
        u = theory.u
        # Theory statements must be logical propositions.
        valid_proposition = unpack_formula(valid_proposition)
        verify(valid_proposition.is_strictly_propositional, 'The formula of this statement is not propositional.')
        # TODO: Check that all components of the hypothetical-proposition
        #  are elements of the source theory-branch.
        self.valid_proposition = valid_proposition
        self.statement_index = theory.crossreference_statement(self)
        paragraphe_header = prioritize_value(paragraphe_header, paragraph_headers.proposition)
        # TODO: Check that cat is a valid statement cat (prop., lem., cor., theorem)
        symbol = prioritize_value(symbol, configuration.default_statement_symbol)
        super().__init__(theory=theory, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, paragraph_header=paragraphe_header, echo=False)
        # manage theoretical-morphisms
        self.morphism_output = None
        if self.valid_proposition.connective.signal_theoretical_morphism:
            # this formula-statement is a theoretical-morphism.
            # it follows that this statement "yields" new statements in the theory.
            assert self.valid_proposition.connective.implementation is not None
            self.morphism_output = Morphism(theory=theory, source_statement=self)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.formula_statement)
        if echo:
            self.echo()

    def __repr__(self):
        return self.rep(expand=True)

    def __str__(self):
        return self.rep(expand=True)

    def alpha_contains(self, psi: FlexibleFormula) -> bool:
        return formula_alpha_contains(u=self.u, phi=self, psi=psi)

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='formula-statement')

    @property
    def connective(self):
        """The connective of a formula-statement
        is the connective of the valid-proposition-formula it contains."""
        return self.valid_proposition.connective

    @property
    def terms(self):
        """The terms of a formula-statement
        are the terms of the valid-proposition-formula it contains."""
        return self.valid_proposition.terms

    def is_formula_syntactically_equivalent_to(self, phi: FlexibleFormula) -> bool:
        """Return true if ⌜self⌝ is formula-syntactically-equivalent to ⌜o2⌝.

        Parameters:
        -----------
        o2 : Formula
            The formula with which to verify formula-equivalence.

        """
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        if self is phi:
            return True
        return self.valid_proposition.is_formula_syntactically_equivalent_to(phi=phi)

    def iterate_theoretical_objcts_references(self, include_root: bool = True, visited: (None, set) = None,
        substitute_constants_with_values: bool = True):
        """Iterate through this and all the formulas it contains recursively."""
        # TODO: Merge methods iterate_statements_in_theory_chain and iterate_theoretical_objcts_references
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        if self.valid_proposition not in visited:
            yield self.valid_proposition
            visited.update({self.valid_proposition})
            yield from self.valid_proposition.iterate_theoretical_objcts_references(include_root=False, visited=visited,
                substitute_constants_with_values=substitute_constants_with_values)

    def list_theoretical_objcts_recursively_OBSOLETE(self, ol: (None, frozenset) = None,
        extension_limit: (None, Statement) = None):
        """Return a python frozenset containing this formula-statement,
         and all theoretical_objcts it contains. If a statement-limit is provided,
         does not yield statements whose index is greater than the formula."""
        ol = frozenset() if ol is None else ol
        if extension_limit is not None and extension_limit.theory == self.theory and extension_limit.statement_index >= self.statement_index:
            ol = ol.union({self})
            if self.valid_proposition not in ol:
                ol = ol.union(self.valid_proposition.list_theoretical_objcts_recursively_OBSOLETE(ol=ol,
                    extension_limit=extension_limit))
        return ol

    def rep(self, encoding: (None, Encoding) = None, expand: (None, bool) = None):
        if expand:
            return self.rep_formula(encoding=encoding, expand=expand)
        else:
            return super().rep(encoding=encoding, expand=expand)

    def rep_formula(self, encoding: (None, Encoding) = None, expand: (None, bool) = None):
        return f'{self.valid_proposition.rep_formula(encoding=encoding, expand=expand)}'


class Morphism(FormulaStatement):
    """

    Definition:
    -----------
    A theoretical-morphism-statement, or morphism for short, aka syntactic-operation is a
    valid-proposition produced by a valid-morphism-formula.

    """

    def __init__(self, source_statement, nameset=None, theory=None, paragraphe_header=None):
        assert isinstance(theory, TheoryDerivation)
        assert isinstance(source_statement, FormulaStatement)
        assert theory.contains_statement_in_theory_chain(phi=source_statement)
        self.source_statement = source_statement
        assert source_statement.valid_proposition.connective.signal_theoretical_morphism
        self.morphism_implementation = source_statement.valid_proposition.connective.implementation
        valid_proposition = self.morphism_implementation(self.source_statement.valid_proposition)
        super().__init__(theory=theory, valid_proposition=valid_proposition, nameset=nameset,
            paragraphe_header=paragraphe_header)

    def rep_report(self, proof: (None, bool) = None) -> str:
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{repm.serif_bold(self.rep_name())}: ' \
                 f'{self.valid_proposition.rep_formula(expand=True)}'
        if proof:
            output = output + self.rep_subreport()
        return output + f'\n'

    def rep_subreport(self):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'\n\t' \
                 f'{repm.serif_bold("Derivation by theoretical-morphism / syntactic-operation")}'
        output = output + f'\n\t' \
                          f'{self.source_statement.valid_proposition.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.source_statement.rep_symbol())}.'
        output = output + f'\n\t{self.valid_proposition.rep_formula(expand=True):<70} │ Output of ' \
                          f'{repm.serif_bold(self.source_statement.valid_proposition.connective.rep_symbol())} morphism.'
        return output


class PropositionStatement:
    """
    Definition
    ----------
    A proposition-statement 𝒮 is a tuple (𝒯, n, 𝜑, 𝒫) where:
    * 𝒯 is a theory
    * n is a natural number representing the unique position of 𝒮 in 𝒯
    * 𝜑 is a valid-formula in 𝒯 of the form ⟨◆, 𝒯, 𝜓⟩ where:
        * ◆ is a theoretical-connective
        * 𝜓 is a free-formula
    * 𝒫 is a proof of 𝜑's validity in 𝒯 solely based on predecessors of 𝒮
    """

    def __init__(self, theory, position, phi, proof):
        assert isinstance(theory, TheoryDerivation)
        assert isinstance(position, int) and position > 0
        assert isinstance(phi, CompoundFormula)
        assert theory.contains_statement_in_theory_chain(phi=phi)
        assert isinstance(proof, Proof)
        verify(assertion=theory.contains_statement_in_theory_chain(phi=proof))
        self.theory = theory
        self.position = position
        self.phi = phi
        self.proof = proof


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


class InferenceRuleDeclaration(Formula):
    """This python abstract class models the :ref:`declaration<object_declaration_math_concept>` of an :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>`.

    """

    def __init__(self, u: UniverseOfDiscourse, definition: (None, CompoundFormula) = None,
        compose_paragraph_proof_method: (None, collections.abc.Callable) = None, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):
        self._definition = definition
        self._compose_paragraph_proof_method = compose_paragraph_proof_method
        symbol = prioritize_value(symbol, configuration.default_inference_rule_symbol)
        paragraph_header = paragraph_headers.inference_rule_declaration
        super().__init__(u=u, is_theory_foundation_system=False, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, echo=False)
        u.i.declare_instance(i=self)
        echo = prioritize_value(echo, configuration.echo_inference_rule_declaration, configuration.echo_declaration,
            configuration.echo_default, False)
        if echo:
            self.echo()

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_inference_rule_declaration(i=self)
        return output

    def compose_paragraph_proof(self, **kwargs) -> collections.abc.Generator[Composable, Composable, bool]:
        """This python method yields a :ref:`paragraph-proof<paragraph_proof_math_concept>` that demonstrates the validity of the object.

        This method should be overridden by specialized inference-rule classes to provide accurate proofs.
        """
        output = yield from configuration.locale.compose_inferred_statement_paragraph_proof(o=self)
        return output

    @property
    @abc.abstractmethod
    def construct_formula(self, **kwargs) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        raise NotImplementedError(
            'The ⌜construct_formula⌝ method is abstract. It must be implemented in the child class.')

    @property
    def definition(self) -> CompoundFormula:
        """This python property returns a formal definition of the object.

        :return: a formula.
        """
        return self._definition

    def echo(self):
        """This python method prints the object to the console (sys.stdout).

        :return:
        """
        repm.prnt(self.rep_report())

    @property
    def is_strictly_propositional(self) -> bool:
        """By definition, an inference-rule-declaration is not a propositional object."""
        return False


class AbsorptionDeclaration(InferenceRuleDeclaration):
    """This python class models the declaration of the :ref:`absorption<absorption_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .

    TODO: AbsorptionDeclaration: Add a data validation step to assure that terms p and q are propositional.
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'absorption'
        abridged_name = None
        auto_index = False
        dashed_name = 'absorption'
        explicit_name = 'absorption inference rule'
        name = 'absorption'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = u.c1.tupl(p | u.c1.implies | q) | u.c1.proves | (p | u.c1.implies | (p | u.c1.land | q))
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_implies_q = p | u.c1.implies | q
            self.term_p_implies_q_mask = frozenset([p, q])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_implies_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_implies_q, _ = verify_formula(arg='p_implies_q', input_value=p_implies_q, u=self.u,
            form=self.term_p_implies_q, mask=self.term_p_implies_q_mask, raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        p: CompoundFormula = p_implies_q.terms[0]  # TODO: Use composed type hints
        q: CompoundFormula = p_implies_q.terms[1]  # TODO: Use composed type hints
        output: CompoundFormula = p | self.u.c1.implies | (p | self.u.c1.land | q)
        return output


class AxiomInterpretationDeclaration(InferenceRuleDeclaration):
    """This python class models the :ref:`declaration<object_declaration_math_concept>` of the :ref:`axiom-interpretation<axiom_interpretation_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>`.

    Inherits from :ref:`InferenceRuleDeclaration<inference_rule_declaration_python_class>` .

    TODO: AxiomInterpretation (Declaration and Inclusion): Add a data validation step to assure that term p is propositional.
    TODO: AxiomInterpretation (Declaration and Inclusion): Add a verification step: the axiom is not locked.

    """

    class Premises(typing.NamedTuple):
        """This python NamedTuple is used behind the scene as a data structure to manipulate the premises required by the :ref:`inference-rule<inference_rule_math_concept>` .
        """
        a: FlexibleAxiom
        p: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'axiom-interpretation'
        acronym = 'ai'
        abridged_name = None
        auto_index = False
        dashed_name = 'axiom-interpretation'
        explicit_name = 'axiom interpretation inference rule'
        name = 'axiom interpretation'
        with u.with_variable(symbol=StyledText(plaintext='A', text_style=text_styles.script_bold),
            auto_index=False) as a, u.with_variable(symbol='P', auto_index=False) as p:
            definition = u.c1.tupl(a, p) | u.c1.proves | p
        with u.with_variable(symbol=StyledText(plaintext='A', text_style=text_styles.script_bold),
            auto_index=False) as a:
            self.term_a = a
            self.term_a_mask = frozenset([a])
        with u.with_variable(symbol='P', auto_index=False) as p:
            self.term_p = p
            self.term_p_mask = frozenset([p])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, a: FlexibleAxiom, p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, a, _ = verify_axiom_declaration(arg='a', input_value=a, u=self.u, raise_exception=True,
            error_code=error_code)
        _, p, _ = verify_formula(arg='p', input_value=p, u=self.u, raise_exception=True, error_code=error_code)
        p: CompoundFormula
        # TODO: Bug #217: assure that atomic formula are supported by verify_formula and verify_formula_statements #217
        # validate_formula does not support basic masks like: ⌜P⌝ where P is a variable.
        # validate_formula(u=self.u, input_value=p, form=self.i.term_p,
        #    mask=self.i.term_p_mask)
        output: CompoundFormula = p
        return output


class BiconditionalElimination1Declaration(InferenceRuleDeclaration):
    """This python class models the declaration of the :ref:`absorption<absorption_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .

    Acronym: be1.
    """

    class Premises(typing.NamedTuple):
        p_iff_q: FormulaStatement

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'biconditional-elimination-1'
        auto_index = False
        dashed_name = 'biconditional-elimination-1'
        acronym = 'be1'
        abridged_name = None
        explicit_name = 'biconditional elimination #1 inference rule'
        name = 'biconditional elimination #1'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = ((p | u.c1.iff | q) | u.c1.proves | (p | u.c1.implies | q))
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_iff_q = p | u.c1.iff | q
            self.term_p_iff_q_mask = frozenset([p, q])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_iff_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_iff_q, _ = verify_formula(arg='p_iff_q', input_value=p_iff_q, u=self.u, form=self.term_p_iff_q,
            mask=self.term_p_iff_q_mask, raise_exception=True, error_code=error_code)
        p_iff_q: CompoundFormula
        p: CompoundFormula = p_iff_q.terms[0]
        q: CompoundFormula = p_iff_q.terms[1]
        output: CompoundFormula = (p | self.u.c1.implies | q)
        return output


class BiconditionalElimination2Declaration(InferenceRuleDeclaration):
    """The well-known biconditional elimination #1 inference rule: P ⟺ Q ⊢ Q ⟹ P.

    Acronym: ber.
    """

    class Premises(typing.NamedTuple):
        p_iff_q: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'biconditional-elimination-2'
        auto_index = False
        dashed_name = 'biconditional-elimination-2'
        acronym = 'be2'
        abridged_name = None
        explicit_name = 'biconditional elimination #2 inference rule'
        name = 'biconditional elimination #2'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = ((p | u.c1.iff | q) | u.c1.proves | (q | u.c1.implies | p))
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_iff_q = p | u.c1.iff | q
            self.term_p_iff_q_mask = frozenset([p, q])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_iff_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_iff_q, _ = verify_formula(arg='p_iff_q', input_value=p_iff_q, u=self.u, form=self.term_p_iff_q,
            mask=self.term_p_iff_q_mask, raise_exception=True, error_code=error_code)
        p_iff_q: CompoundFormula
        p: CompoundFormula = p_iff_q.terms[0]
        q: CompoundFormula = p_iff_q.terms[1]
        output: CompoundFormula = (q | self.u.c1.implies | p)
        return output


class BiconditionalIntroductionDeclaration(InferenceRuleDeclaration):
    """The well-known biconditional introduction inference rule: (P ⟹ Q), (Q ⟹ P) ⊢ (P ⟺ Q)

    Acronym: bi.
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula
        q_implies_p: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'biconditional-introduction'
        auto_index = False
        dashed_name = 'biconditional-introduction'
        acronym = 'bi'
        abridged_name = None
        explicit_name = 'biconditional introduction inference rule'
        name = 'biconditional introduction'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = u.c1.tupl(p | u.c1.implies | q, q | u.c1.implies | p) | u.c1.proves | (p | u.c1.iff | q)
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_implies_q = p | u.c1.implies | q
            self.term_p_implies_q_mask = frozenset([p, q])
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_q_implies_p = q | u.c1.implies | p
            self.term_q_implies_p_mask = frozenset([p, q])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_implies_q: FlexibleFormula, q_implies_p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_implies_q, _ = verify_formula(arg='p_implies_q', input_value=p_implies_q, u=self.u,
            form=self.term_p_implies_q, mask=self.term_p_implies_q_mask, raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, q_implies_p, _ = verify_formula(arg='q_implies_p', input_value=q_implies_p, u=self.u,
            form=self.term_q_implies_p, mask=self.term_q_implies_p_mask, raise_exception=True, error_code=error_code)
        q_implies_p: CompoundFormula
        p_implies_q__p: CompoundFormula = p_implies_q.terms[0]
        p_implies_q__q: CompoundFormula = p_implies_q.terms[1]
        q_implies_p__q: CompoundFormula = q_implies_p.terms[0]
        q_implies_p__p: CompoundFormula = q_implies_p.terms[1]
        verify(assertion=p_implies_q__p.is_formula_syntactically_equivalent_to(phi=q_implies_p__p),
            msg='The ⌜p⌝ in ⌜p_implies_q⌝ is not syntactically-equivalent to the ⌜p⌝ in  ⌜q_implies_p⌝.',
            severity=verification_severities.error, raise_exception=True, p_implies_q=p_implies_q,
            p_implies_q__p=p_implies_q__p, q_implies_p=q_implies_p, q_implies_p__p=q_implies_p__p)
        verify(assertion=p_implies_q__q.is_formula_syntactically_equivalent_to(phi=q_implies_p__q),
            msg='The ⌜q⌝ in ⌜p_implies_q⌝ is not syntactically-equivalent to the ⌜q⌝ in  ⌜q_implies_p⌝.',
            severity=verification_severities.error, raise_exception=True, p_implies_q=p_implies_q,
            p_implies_q__q=p_implies_q__q, q_implies_p=q_implies_p, q_implies_p__q=q_implies_p__q)
        output: CompoundFormula = p_implies_q__p | self.u.c1.iff | p_implies_q__q
        return output


class ConjunctionElimination1Declaration(InferenceRuleDeclaration):
    """The well-known conjunction elimination #1 inference rule: P ⟺ Q ⊢ P ⟹ Q.

    Acronym: cel.
    """

    class Premises(typing.NamedTuple):
        p_and_q: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'conjunction-elimination-1'
        auto_index = False
        dashed_name = 'conjunction-elimination-1'
        acronym = 'ce1'
        abridged_name = None
        explicit_name = 'conjunction elimination #1 inference rule'
        name = 'conjunction elimination #1'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = ((p | u.c1.land | q) | u.c1.proves | p)
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_and_q = p | u.c1.land | q
            self.term_p_and_q_mask = frozenset([p, q])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_and_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_and_q, _ = verify_formula(arg='p_and_q', input_value=p_and_q, u=self.u, form=self.term_p_and_q,
            mask=self.term_p_and_q_mask, raise_exception=True, error_code=error_code)
        p_and_q: CompoundFormula
        p: CompoundFormula = p_and_q.terms[0]
        output: CompoundFormula = p
        return output


class ConjunctionElimination2Declaration(InferenceRuleDeclaration):
    """The well-known conjunction elimination #2 inference rule: P ⟺ Q ⊢ Q ⟹ P.

    Acronym: cer.

    :param p_land_q: A formula-statement of the form: (P ⋀ Q).
    :param t: The current theory-derivation.
    :return: The (proven) formula: Q.
    """

    class Premises(typing.NamedTuple):
        p_and_q: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'conjunction-elimination-2'
        auto_index = False
        dashed_name = 'conjunction-elimination-2'
        acronym = 'ce2'
        abridged_name = None
        explicit_name = 'conjunction elimination #2 inference rule'
        name = 'conjunction elimination #2'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = ((p | u.c1.land | q) | u.c1.proves | q)
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_and_q = p | u.c1.land | q
            self.term_p_and_q_mask = frozenset([p, q])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_and_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_and_q, _ = verify_formula(arg='p_and_q', input_value=p_and_q, u=self.u, form=self.term_p_and_q,
            mask=self.term_p_and_q_mask, raise_exception=True, error_code=error_code)
        p_and_q: CompoundFormula
        q: CompoundFormula = p_and_q.terms[1]
        output: CompoundFormula = q
        return output


class ConjunctionIntroductionDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`conjunction-introduction<conjunction_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p: FlexibleFormula
        q: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'conjunction-introduction'
        acronym = 'ci'
        abridged_name = None
        auto_index = False
        dashed_name = 'conjunction-introduction'
        explicit_name = 'conjunction introduction inference rule'
        name = 'conjunction introduction'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = u.c1.tupl(p, q) | u.c1.proves | (p | u.c1.land | q)
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p: FlexibleFormula, q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p, _ = verify_formula(arg='p', input_value=p, u=self.u, raise_exception=True, error_code=error_code)
        p: CompoundFormula
        _, q, _ = verify_formula(arg='q', input_value=q, u=self.u, raise_exception=True, error_code=error_code)
        q: CompoundFormula
        output: CompoundFormula = p | self.u.c1.land | q
        return output


class ConstructiveDilemmaDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`constructive-dilemma<constructive_dilemma_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    # TODO: BUG #218: It seems that ConstructiveDilemmaDeclaration is ill-defined. Review the litterature and assure that it is properly defined. As is it is synonymous to conjunction-introduction, this doesn't make sense.

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula
        r_implies_s: FlexibleFormula
        p_or_r: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'constructive-dilemma'
        acronym = 'cd'
        abridged_name = None
        auto_index = False
        dashed_name = 'constructive-dilemma'
        explicit_name = 'constructive dilemma inference rule'
        name = 'constructive dilemma'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q, u.with_variable(
            symbol='R') as r, u.with_variable(symbol='S') as s:
            definition = u.c1.tupl((p | u.c1.implies | q), (r | u.c1.implies | s), (p | u.c1.lor | r)) | u.c1.proves | (
                q | u.c1.lor | s)
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_implies_q = p | u.c1.implies | q
            self.term_p_implies_q_mask = frozenset([p, q])
        with u.with_variable(symbol='R') as r, u.with_variable(symbol='S') as s:
            self.term_r_implies_s = r | u.c1.implies | s
            self.term_r_implies_s_mask = frozenset([r, s])
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='R') as r:
            self.term_p_or_r = p | u.c1.lor | r
            self.term_p_or_r_mask = frozenset([p, r])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_implies_q: FlexibleFormula, r_implies_s: FlexibleFormula,
        p_or_r: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_implies_q, _ = verify_formula(arg='p_implies_q', input_value=p_implies_q, u=self.u,
            form=self.term_p_implies_q, mask=self.term_p_implies_q_mask, raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, r_implies_s, _ = verify_formula(arg='r_implies_s', input_value=r_implies_s, u=self.u,
            form=self.term_r_implies_s, mask=self.term_r_implies_s_mask, raise_exception=True, error_code=error_code)
        r_implies_s: CompoundFormula
        _, p_or_r, _ = verify_formula(arg='p_or_r', input_value=p_or_r, u=self.u, form=self.term_p_or_r,
            mask=self.term_p_or_r_mask, raise_exception=True, error_code=error_code)
        p_or_r: CompoundFormula
        p__in__p_implies_q: CompoundFormula = p_implies_q.terms[0]
        p__in__p_or_r: CompoundFormula = p_or_r.terms[0]
        verify(assertion=p__in__p_implies_q.is_formula_syntactically_equivalent_to(phi=p__in__p_or_r),
            msg=f'The ⌜p⌝({p__in__p_implies_q}) in the formula argument ⌜p_implies_q⌝({p_implies_q}) is not syntaxically-equivalent to the ⌜p⌝({p__in__p_or_r}) in the formula argument ⌜p_or_r⌝({p_or_r})',
            raise_exception=True, error_code=error_code)
        r__in__r_implies_s: CompoundFormula = r_implies_s.terms[0]
        r__in__p_or_r: CompoundFormula = p_or_r.terms[1]
        verify(assertion=r__in__r_implies_s.is_formula_syntactically_equivalent_to(phi=r__in__p_or_r),
            msg=f'The ⌜r⌝({r__in__r_implies_s}) in the formula argument ⌜r_implies_s⌝({r_implies_s}) is not syntaxically-equivalent to the ⌜r⌝({r__in__p_or_r}) in the formula argument ⌜p_or_r⌝({p_or_r})',
            raise_exception=True, error_code=error_code)
        q: CompoundFormula = p_implies_q.terms[1]
        s: CompoundFormula = r_implies_s.terms[1]
        output: CompoundFormula = q | self.u.c1.lor | s
        return output


class DefinitionInterpretationDeclaration(InferenceRuleDeclaration):
    """This python class models the :ref:`declaration<object_declaration_math_concept>` of the :ref:`definition-interpretation<definition_interpretation_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>`.

    Inherits from :ref:`InferenceRuleDeclaration<inference_rule_declaration_python_class>` .

    TODO: DefinitionInterpretation (Declaration and Inclusion): Add a data validation step to assure that term p is propositional.
    TODO: DefinitionInterpretation (Declaration and Inclusion): Add a verification step: the axiom is not locked.

    """

    class Premises(typing.NamedTuple):
        """This python NamedTuple is used behind the scene as a data structure to manipulate the premises required by the :ref:`inference-rule<inference_rule_math_concept>` .
        """
        d: FlexibleDefinition
        x: FlexibleFormula
        y: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'definition-interpretation'
        acronym = 'di'
        abridged_name = None
        auto_index = False
        dashed_name = 'definition-interpretation'
        explicit_name = 'definition interpretation inference rule'
        name = 'definition interpretation'
        with u.with_variable(symbol=StyledText(plaintext='D', text_style=text_styles.script_bold),
            auto_index=False) as d, u.with_variable(symbol='x', auto_index=False) as x, u.with_variable(symbol='y',
            auto_index=False) as y:
            # Feature #216: provide support for n-ary connectives
            # Provide support for n-ary connectives. First need: sequent-comma, or collection-comma.
            # definition = u.r.sequent_comma(d, x, y) | u.r.proves | (x | u.r.equal | y)
            # Meanwhile, I use combined 2-ary formulae:
            definition = d | u.c1.tupl | (x | u.c1.tupl | y) | u.c1.proves | (x | u.c1.equal | y)
        with u.with_variable(symbol=StyledText(plaintext='D', text_style=text_styles.script_bold),
            auto_index=False) as d:
            self.term_d = d
            self.term_d_mask = frozenset([d])
        with u.with_variable(symbol='x', auto_index=False) as x:
            self.term_x = x
            self.term_x_mask = frozenset([x])
        with u.with_variable(symbol='y', auto_index=False) as y:
            self.term_y = y
            self.term_y_mask = frozenset([y])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, d: DefinitionInclusion, x: FlexibleFormula, y: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        ok: bool
        output: CompoundFormula
        msg: (None, str)
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, d, _ = verify_definition_declaration(arg='d', input_value=d, u=self.u, raise_exception=True,
            error_code=error_code)
        _, x, _ = verify_formula(arg='x', input_value=x, u=self.u, raise_exception=True, error_code=error_code)
        x: CompoundFormula
        _, y, _ = verify_formula(arg='y', input_value=y, u=self.u, raise_exception=True, error_code=error_code)
        y: CompoundFormula
        output: CompoundFormula = x | self.u.c1.equal | y
        return output


class DestructiveDilemmaDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`destructive-dilemma<destructive_dilemma_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula
        r_implies_s: FlexibleFormula
        not_q_or_not_s: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'destructive-dilemma'
        acronym = 'dd'
        abridged_name = None
        auto_index = False
        dashed_name = 'destructive-dilemma'
        explicit_name = 'destructive dilemma inference rule'
        name = 'destructive dilemma'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q, u.with_variable(
            symbol='R') as r, u.with_variable(symbol='S') as s:
            definition = u.c1.tupl((p | u.c1.implies | q), (r | u.c1.implies | s), (p | u.c1.lor | r)) | u.c1.proves | (
                q | u.c1.lor | s)
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_implies_q = p | u.c1.implies | q
            self.term_p_implies_q_mask = frozenset([p, q])
        with u.with_variable(symbol='R') as r, u.with_variable(symbol='S') as s:
            self.term_r_implies_s = r | u.c1.implies | s
            self.term_r_implies_s_mask = frozenset([r, s])
        with u.with_variable(symbol='Q') as q, u.with_variable(symbol='S') as s:
            self.term_not_q_or_not_s = u.c1.lnot(q) | u.c1.lor | u.c1.lnot(s)
            self.term_not_q_or_not_s_mask = frozenset([q, s])
            super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
                acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_implies_q: FlexibleFormula, r_implies_s: FlexibleFormula,
        not_q_or_not_s: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_implies_q, _ = verify_formula(arg='p_implies_q', input_value=p_implies_q, u=self.u,
            form=self.term_p_implies_q, mask=self.term_p_implies_q_mask, raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, r_implies_s, _ = verify_formula(arg='r_implies_s', input_value=r_implies_s, u=self.u,
            form=self.term_r_implies_s, mask=self.term_r_implies_s_mask, raise_exception=True, error_code=error_code)
        r_implies_s: CompoundFormula
        _, not_q_or_not_s, _ = verify_formula(arg='not_q_or_not_s', input_value=not_q_or_not_s, u=self.u,
            form=self.term_not_q_or_not_s, mask=self.term_not_q_or_not_s_mask, raise_exception=True,
            error_code=error_code)
        not_q_or_not_s: CompoundFormula
        q__in__p_implies_q: CompoundFormula = p_implies_q.terms[1]
        q__in__not_q_or_not_s: CompoundFormula = not_q_or_not_s.terms[0].terms[0]
        verify(assertion=q__in__p_implies_q.is_formula_syntactically_equivalent_to(phi=q__in__p_implies_q),
            msg=f'The ⌜q⌝({q__in__p_implies_q}) in the formula argument ⌜p_implies_q⌝({p_implies_q}) is not syntaxically-equivalent to the ⌜q⌝({q__in__not_q_or_not_s}) in the formula argument ⌜not_q_or_not_s⌝({not_q_or_not_s})',
            raise_exception=True, error_code=error_code)
        s__in__r_implies_s: CompoundFormula = r_implies_s.terms[1]
        s__in__not_q_or_not_s: CompoundFormula = not_q_or_not_s.terms[1].terms[0]
        verify(assertion=s__in__r_implies_s.is_formula_syntactically_equivalent_to(phi=s__in__not_q_or_not_s),
            msg=f'The ⌜s⌝({s__in__r_implies_s}) in the formula argument ⌜r_implies_s⌝({r_implies_s}) is not syntaxically-equivalent to the ⌜s⌝({s__in__not_q_or_not_s}) in the formula argument ⌜not_q_or_not_s⌝({not_q_or_not_s})',
            raise_exception=True, error_code=error_code)
        p: CompoundFormula = p_implies_q.terms[0]
        r: CompoundFormula = r_implies_s.terms[0]
        output: CompoundFormula = self.u.c1.lnot(p) | self.u.c1.lor | self.u.c1.lnot(r)
        return output


class DisjunctionIntroduction1Declaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`disjunction-introduction-1<disjunction_introduction_1_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p: FlexibleFormula
        q: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'disjunction-introduction-1'
        acronym = 'di1'
        abridged_name = None
        auto_index = False
        dashed_name = 'disjunction-introduction-1'
        explicit_name = 'disjunction introduction #1 inference rule'
        name = 'disjunction introduction #1'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = (p | u.c1.proves | (q | u.c1.lor | p))
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p: FlexibleFormula, q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p, _ = verify_formula(arg='p', input_value=p, u=self.u, raise_exception=True, error_code=error_code)
        p: CompoundFormula
        _, q, _ = verify_formula(arg='q', input_value=q, u=self.u, raise_exception=True, error_code=error_code)
        q: CompoundFormula
        output: CompoundFormula = q | self.u.c1.lor | p
        return output


class DisjunctionIntroduction2Declaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`disjunction-introduction-2<disjunction_introduction_2_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p: FlexibleFormula
        q: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'disjunction-introduction-2'
        acronym = 'di2'
        abridged_name = None
        auto_index = False
        dashed_name = 'disjunction-introduction-2'
        explicit_name = 'disjunction introduction #2 inference rule'
        name = 'disjunction introduction #2'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = (p | u.c1.proves | (p | u.c1.lor | q))
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p: FlexibleFormula, q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p, _ = verify_formula(arg='p', input_value=p, u=self.u, raise_exception=True, error_code=error_code)
        p: CompoundFormula
        _, q, _ = verify_formula(arg='q', input_value=q, u=self.u, raise_exception=True, error_code=error_code)
        q: CompoundFormula
        output: CompoundFormula = p | self.u.c1.lor | q
        return output


class DisjunctiveResolutionDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`disjunctive-resolution<disjunctive_resolution_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_or_q: FlexibleFormula
        not_p_or_r: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'disjunctive-resolution'
        acronym = 'dr'
        abridged_name = None
        auto_index = False
        dashed_name = 'disjunctive-resolution'
        explicit_name = 'disjunctive resolution inference rule'
        name = 'disjunctive resolution'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q, u.with_variable(symbol='R') as r:
            definition = (
                ((p | u.c1.lor | q) | u.c1.tupl | (u.c1.lnot(p) | u.c1.lor | r)) | u.c1.proves | (p | u.c1.lor | r))
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_or_q = p | u.c1.lor | q
            self.term_p_or_q_mask = frozenset([p, q])
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='R') as r:
            self.term_not_p_or_r = u.c1.lnot(p) | u.c1.lor | r
            self.term_not_p_or_r_mask = frozenset([p, r])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_or_q: FlexibleFormula, not_p_or_r: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_or_q, _ = verify_formula(arg='p_or_q', input_value=p_or_q, u=self.u, form=self.term_p_or_q,
            mask=self.term_p_or_q_mask, raise_exception=True, error_code=error_code)
        p_or_q: CompoundFormula
        _, not_p_or_r, _ = verify_formula(arg='not_p_or_r', input_value=not_p_or_r, u=self.u, form=self.term_not_p_or_r,
            mask=self.term_not_p_or_r_mask, raise_exception=True, error_code=error_code)
        not_p_or_r: CompoundFormula
        p__in__p_or_q: CompoundFormula = p_or_q.terms[0]
        p__in__not_p_or_r: CompoundFormula = not_p_or_r.terms[0].terms[0]
        verify(assertion=p__in__p_or_q.is_formula_syntactically_equivalent_to(phi=p__in__not_p_or_r),
            msg=f'The ⌜p⌝({p__in__p_or_q}) in the formula argument ⌜p_or_q⌝({p_or_q}) is not syntaxically-equivalent to the ⌜p⌝({p__in__not_p_or_r}) in the formula argument ⌜not_p_or_r⌝({not_p_or_r})',
            raise_exception=True, error_code=error_code)
        q: CompoundFormula = p_or_q.terms[1]
        r: CompoundFormula = not_p_or_r.terms[1]
        output: CompoundFormula = q | self.u.c1.lor | r
        return output


class DisjunctiveSyllogism1Declaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`disjunctive-syllogism-1<disjunctive_syllogism_1_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_or_q: FlexibleFormula
        not_p: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'disjunctive-syllogism-1'
        acronym = 'ds'
        abridged_name = None
        auto_index = False
        dashed_name = 'disjunctive-syllogism-1'
        explicit_name = 'disjunctive syllogism inference rule'
        name = 'disjunctive syllogism'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = (((p | u.c1.lor | q) | u.c1.tupl | u.c1.lnot(p)) | u.c1.proves | (q))
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_or_q = p | u.c1.lor | q
            self.term_p_or_q_mask = frozenset([p, q])
        with u.with_variable(symbol='P') as p:
            self.term_not_p = u.c1.lnot(p)
            self.term_not_p_mask = frozenset([p])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_or_q: FlexibleFormula, not_p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_or_q, _ = verify_formula(arg='p_or_q', input_value=p_or_q, u=self.u, form=self.term_p_or_q,
            mask=self.term_p_or_q_mask, raise_exception=True, error_code=error_code)
        p_or_q: CompoundFormula
        _, not_p, _ = verify_formula(arg='not_p', input_value=not_p, u=self.u, form=self.term_not_p,
            mask=self.term_not_p_mask, raise_exception=True, error_code=error_code)
        not_p: CompoundFormula
        p__in__p_or_q: CompoundFormula = p_or_q.terms[0]
        p__in__not_p: CompoundFormula = not_p.terms[0]
        verify(assertion=p__in__p_or_q.is_formula_syntactically_equivalent_to(phi=p__in__not_p),
            msg=f'The ⌜p⌝({p__in__p_or_q}) in the formula argument ⌜p_or_q⌝({p_or_q}) is not syntaxically-equivalent to the ⌜p⌝({p__in__not_p}) in the formula argument ⌜not_p⌝({not_p})',
            raise_exception=True, error_code=error_code)
        q: CompoundFormula = p_or_q.terms[1]
        output: CompoundFormula = q
        return output


class DisjunctiveSyllogism2Declaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`disjunctive-syllogism-2<disjunctive_syllogism_2_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_or_q: FlexibleFormula
        not_q: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'disjunctive-syllogism-2'
        acronym = 'ds'
        abridged_name = None
        auto_index = False
        dashed_name = 'disjunctive-syllogism-2'
        explicit_name = 'disjunctive syllogism inference rule'
        name = 'disjunctive syllogism'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = (((p | u.c1.lor | q) | u.c1.tupl | u.c1.lnot(p)) | u.c1.proves | (q))
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_or_q = p | u.c1.lor | q
            self.term_p_or_q_mask = frozenset([p, q])
        with u.with_variable(symbol='Q') as q:
            self.term_not_q = u.c1.lnot(q)
            self.term_not_q_mask = frozenset([q])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_or_q: FlexibleFormula, not_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_or_q, _ = verify_formula(arg='p_or_q', input_value=p_or_q, u=self.u, form=self.term_p_or_q,
            mask=self.term_p_or_q_mask, raise_exception=True, error_code=error_code)
        p_or_q: CompoundFormula
        _, not_q, _ = verify_formula(arg='not_q', input_value=not_q, u=self.u, form=self.term_not_q,
            mask=self.term_not_q_mask, raise_exception=True, error_code=error_code)
        not_q: CompoundFormula
        q__in__p_or_q: CompoundFormula = p_or_q.terms[1]
        q__in__not_q: CompoundFormula = not_q.terms[0]
        verify(assertion=q__in__p_or_q.is_formula_syntactically_equivalent_to(phi=q__in__not_q),
            msg=f'The ⌜p⌝({q__in__p_or_q}) in the formula argument ⌜p_or_q⌝({p_or_q}) is not syntaxically-equivalent to the ⌜p⌝({q__in__not_q}) in the formula argument ⌜not_q⌝({not_q})',
            raise_exception=True, error_code=error_code)
        q: CompoundFormula = p_or_q.terms[0]
        output: CompoundFormula = q
        return output


class DoubleNegationEliminationDeclaration(InferenceRuleDeclaration):
    """The well-known double negation elimination #1 inference rule: ¬(¬(P)) ⊢ P.

    Acronym: cer.

    :param p_land_q: A formula-statement of the form: (P ⋀ Q).
    :param t: The current theory-derivation.
    :return: The (proven) formula: Q.
    """

    class Premises(typing.NamedTuple):
        not_not_p: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'double-negation-elimination'
        auto_index = False
        dashed_name = 'double-negation-elimination'
        acronym = 'dne'
        abridged_name = None
        explicit_name = 'double negation elimination inference rule'
        name = 'double negation elimination'
        with u.with_variable(symbol='P') as p:
            definition = (u.c1.lnot(u.c1.lnot(p)) | u.c1.proves | p)
        with u.with_variable(symbol='P') as p:
            self.term_not_not_p = u.c1.lnot(u.c1.lnot(p))
            self.term_not_not_p_mask = frozenset([p])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, not_not_p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, not_not_p, _ = verify_formula(arg='not_not_p', input_value=not_not_p, u=self.u, form=self.term_not_not_p,
            mask=self.term_not_not_p_mask, raise_exception=True, error_code=error_code)
        not_not_p: CompoundFormula
        p: CompoundFormula = not_not_p.terms[0].terms[0]
        output: CompoundFormula = p
        return output


class DoubleNegationIntroductionDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`double-negation-introduction<double_negation_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'double-negation-introduction'
        auto_index = False
        dashed_name = 'double-negation-introduction'
        acronym = 'dni'
        abridged_name = None
        explicit_name = 'double negation introduction inference rule'
        name = 'double negation introduction'
        with u.with_variable(symbol='P') as p:
            definition = (p | u.c1.proves | u.c1.lnot(u.c1.lnot(p)))
        with u.with_variable(symbol='P') as p:
            self.term_p = p
            self.term_p_mask = frozenset([p])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p, _ = verify_formula(arg='p', input_value=p, u=self.u, raise_exception=True, error_code=error_code)
        p: CompoundFormula
        not_not_p: CompoundFormula = self.u.c1.lnot(self.u.c1.lnot(p))
        output: CompoundFormula = not_not_p
        return output


class EqualityCommutativityDeclaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        x_equal_y: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'equality-commutativity'
        acronym = 'ec'
        abridged_name = None
        auto_index = False
        dashed_name = 'equality-commutativity'
        explicit_name = 'equality commutativity inference rule'
        name = 'equality commutativity'
        with u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
            definition = (x | u.c1.equal | y) | u.c1.proves | (y | u.c1.equal | x)
        with u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
            self.term_x_equal_y = x | u.c1.equal | y
            self.term_x_equal_y_mask = frozenset([x, y])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, x_equal_y: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, x_equal_y, _ = verify_formula(arg='x_equal_y', input_value=x_equal_y, u=self.u, form=self.term_x_equal_y,
            mask=self.term_x_equal_y_mask, raise_exception=True, error_code=error_code)
        x_equal_y: CompoundFormula
        x__in__x_equal_y: CompoundFormula = x_equal_y.terms[0]
        y__in__x_equal_y: CompoundFormula = x_equal_y.terms[1]
        output: CompoundFormula = y__in__x_equal_y | self.u.c1.equal | x__in__x_equal_y
        return output


class EqualTermsSubstitutionDeclaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        p: FlexibleFormula
        x_equal_y: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'equal-terms-substitution'
        acronym = 'ets'
        abridged_name = None
        auto_index = False
        dashed_name = 'equal-terms-substitution'
        explicit_name = 'equal terms substitution inference rule'
        name = 'equal terms substitution'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q, u.with_variable(
            symbol='x') as x, u.with_variable(symbol='y') as y:
            definition = (p | u.c1.tupl | (x | u.c1.equal | y)) | u.c1.proves | q
        with u.with_variable(symbol='P') as p:
            self.term_p = p
            self.term_p_mask = frozenset([p])
        with u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
            self.term_x_equal_y = x | u.c1.equal | y
            self.term_x_equal_y_mask = frozenset([x, y])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p: FlexibleFormula, x_equal_y: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p, _ = verify_formula(arg='p', input_value=p, u=self.u, raise_exception=True, error_code=error_code)
        p: CompoundFormula
        _, x_equal_y, _ = verify_formula(arg='x_equal_y', input_value=x_equal_y, u=self.u, form=self.term_x_equal_y,
            mask=self.term_x_equal_y_mask, raise_exception=True, error_code=error_code)
        x_equal_y: CompoundFormula
        x__in__x_equal_y: CompoundFormula = x_equal_y.terms[0]
        y__in__x_equal_y: CompoundFormula = x_equal_y.terms[1]
        substitution_map = {x__in__x_equal_y: y__in__x_equal_y}
        q: CompoundFormula = p.substitute(substitution_map=substitution_map, lock_variable_scope=True)
        output: CompoundFormula = q
        return output


class HypotheticalSyllogismDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`hypothetical-syllogism<hypothetical_syllogism_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula
        q_implies_r: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'hypothetical-syllogism'
        acronym = 'hs'
        abridged_name = None
        auto_index = False
        dashed_name = 'hypothetical-syllogism'
        explicit_name = 'hypothetical syllogism inference rule'
        name = 'hypothetical syllogism'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q, u.with_variable(symbol='R') as r:
            definition = u.c1.tupl((p | u.c1.implies | q), (q | u.c1.implies | r)) | u.c1.proves | (p | u.c1.land | r)
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_implies_q = p | u.c1.implies | q
            self.term_p_implies_q_mask = frozenset([p, q])
        with u.with_variable(symbol='Q') as q, u.with_variable(symbol='R') as r:
            self.term_q_implies_r = q | u.c1.implies | r
            self.term_q_implies_r_mask = frozenset([q, r])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_implies_q: FlexibleFormula, q_implies_r: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_implies_q, _ = verify_formula(arg='p_implies_q', input_value=p_implies_q, u=self.u,
            form=self.term_p_implies_q, mask=self.term_p_implies_q_mask, raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, q_implies_r, _ = verify_formula(arg='q_implies_r', input_value=q_implies_r, u=self.u,
            form=self.term_q_implies_r, mask=self.term_q_implies_r_mask, raise_exception=True, error_code=error_code)
        q_implies_r: CompoundFormula
        q__in__p_implies_q: CompoundFormula = p_implies_q.terms[1]
        q__in__q_implies_r: CompoundFormula = q_implies_r.terms[0]
        verify(assertion=q__in__p_implies_q.is_formula_syntactically_equivalent_to(phi=q__in__q_implies_r),
            msg=f'The ⌜q⌝({q__in__p_implies_q}) in the formula argument ⌜p_implies_q⌝({p_implies_q}) is not syntaxically-equivalent to the ⌜q⌝({q__in__q_implies_r}) in the formula argument ⌜q_implies_r⌝({q_implies_r})',
            raise_exception=True, error_code=error_code)
        output: CompoundFormula = p_implies_q.terms[0] | self.u.c1.implies | q_implies_r.terms[1]
        return output


class InconsistencyIntroduction1Declaration(InferenceRuleDeclaration):
    """P ⋀ not P: inconsistency"""

    class Premises(typing.NamedTuple):
        p: FlexibleFormula
        not_p: FlexibleFormula
        t: TheoryDerivation

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'inconsistency-introduction-1'
        acronym = 'ii1'
        abridged_name = None
        auto_index = False
        dashed_name = 'inconsistency-introduction-1'
        explicit_name = 'inconsistency introduction #1 inference rule'
        name = 'inconsistency introduction #1'
        # definition = StyledText(plaintext='(P, not(P)) |- (T)', unicode='(𝑷, ¬(𝑷)) ⊢ 𝐼𝑛𝑐(𝓣)')
        with u.with_variable(symbol='P') as p, u.with_variable(
            symbol=StyledText(s='T', text_style=text_styles.script_normal)) as t:
            definition = (p | u.c1.tupl | (u.c1.lnot(p))) | u.c1.proves | u.c1.inc(t)
        with u.with_variable(symbol='P') as p:
            self.term_p = p
            self.term_p_mask = frozenset([p])
        with u.with_variable(symbol='P') as p:
            self.term_not_p = u.c1.lnot(p)
            self.term_not_p_mask = frozenset([p])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p: FlexibleFormula, not_p: FlexibleFormula, t: TheoryDerivation) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p, _ = verify_formula(arg='p', input_value=p, u=self.u, raise_exception=True, error_code=error_code)
        p: CompoundFormula
        _, not_p, _ = verify_formula(arg='not_p', input_value=not_p, u=self.u, form=self.term_not_p,
            mask=self.term_not_p_mask, raise_exception=True, error_code=error_code)
        not_p: CompoundFormula
        p__in__not_p: CompoundFormula = not_p.terms[0]
        verify(assertion=p.is_formula_syntactically_equivalent_to(phi=p__in__not_p),
            msg=f'The formula argument ⌜p⌝({p}) is not syntaxically-equivalent to the ⌜p⌝({p__in__not_p}) in the formula argument ⌜not_q⌝({not_p})',
            raise_exception=True, error_code=error_code)
        verify(assertion=isinstance(t, TheoryDerivation), msg=f'The argument ⌜t⌝({t}) is not a theory-derivation.',
            raise_exception=True, error_code=error_code)
        output: CompoundFormula = self.u.c1.inc(t)
        return output


class InconsistencyIntroduction2Declaration(InferenceRuleDeclaration):
    """P = Q ⋀ P neq Q: inconsistency """

    class Premises(typing.NamedTuple):
        x_equal_y: FlexibleFormula
        x_unequal_y: FlexibleFormula
        t: TheoryDerivation

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'inconsistency-introduction-2'
        acronym = 'ii2'
        abridged_name = None
        auto_index = False
        dashed_name = 'inconsistency-introduction-2'
        explicit_name = 'inconsistency introduction #2 inference rule'
        name = 'inconsistency introduction #2'
        # definition = StyledText(plaintext='((P = Q), (P neq Q)) |- Inc(T)',unicode='((𝑷 = 𝑸), (𝑷 ≠ 𝑸)) ⊢ 𝐼𝑛𝑐(𝒯)')
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q, u.with_variable(
            symbol=StyledText(s='T', text_style=text_styles.script_normal)) as t:
            definition = ((p | u.c1.equal | q) | u.c1.tupl | (p | u.c1.unequal | q)) | u.c1.proves | u.c1.inc(t)
        with u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
            self.term_x_equal_y = x | u.c1.equal | y
            self.term_x_equal_y_mask = frozenset([x, y])
        with u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
            self.term_x_unequal_y = x | u.c1.unequal | y
            self.term_x_unequal_y_mask = frozenset([x, y])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, x_equal_y: FlexibleFormula, x_unequal_y: FlexibleFormula,
        t: TheoryDerivation) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, x_equal_y, _ = verify_formula(arg='x_equal_y', input_value=x_equal_y, u=self.u, form=self.term_x_equal_y,
            mask=self.term_x_equal_y_mask, raise_exception=True, error_code=error_code)
        x_equal_y: CompoundFormula
        _, x_unequal_y, _ = verify_formula(arg='x_unequal_y', input_value=x_unequal_y, u=self.u,
            form=self.term_x_unequal_y, mask=self.term_x_unequal_y_mask, raise_exception=True, error_code=error_code)
        x_unequal_y: CompoundFormula
        x__in__x_equal_y: CompoundFormula = x_equal_y.terms[0]
        x__in__x_unequal_y: CompoundFormula = x_unequal_y.terms[0]
        verify(assertion=x__in__x_equal_y.is_formula_syntactically_equivalent_to(phi=x__in__x_unequal_y),
            msg=f'The ⌜x⌝({x__in__x_equal_y}) in the formula argument ⌜x_equal_y⌝({x_equal_y}) is not syntaxically-equivalent to the ⌜x⌝({x__in__x_unequal_y}) in the formula argument ⌜x_unequal_y⌝({x_unequal_y})',
            raise_exception=True, error_code=error_code)
        y__in__x_equal_y: CompoundFormula = x_equal_y.terms[1]
        y__in__x_unequal_y: CompoundFormula = x_unequal_y.terms[1]
        verify(assertion=y__in__x_equal_y.is_formula_syntactically_equivalent_to(phi=y__in__x_unequal_y),
            msg=f'The ⌜y⌝({y__in__x_equal_y}) in the formula argument ⌜x_equal_y⌝({x_equal_y}) is not syntaxically-equivalent to the ⌜y⌝({y__in__x_unequal_y}) in the formula argument ⌜y_unequal_y⌝({x_unequal_y})',
            raise_exception=True, error_code=error_code)
        verify(assertion=isinstance(t, TheoryDerivation), msg=f'The argument ⌜t⌝({t}) is not a theory-derivation.',
            raise_exception=True, error_code=error_code)
        output: CompoundFormula = self.u.c1.inc(t)
        return output


class InconsistencyIntroduction3Declaration(InferenceRuleDeclaration):
    """P neq P: inconsistency """

    class Premises(typing.NamedTuple):
        x_unequal_x: FlexibleFormula
        t: TheoryDerivation

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'inconsistency-introduction-3'
        acronym = 'ii3'
        abridged_name = None
        auto_index = False
        dashed_name = 'inconsistency-introduction-3'
        explicit_name = 'inconsistency introduction #3 inference rule'
        name = 'inconsistency introduction #3'
        # definition = StyledText(plaintext='(P neq P) |- Inc(T)', unicode='(𝑷 ≠ 𝑷) ⊢ Inc(𝒯)')
        with u.with_variable(symbol='P') as p, u.with_variable(
            symbol=StyledText(s='T', text_style=text_styles.script_normal)) as t:
            definition = (p | u.c1.unequal | p) | u.c1.proves | u.c1.inc(t)
        with u.with_variable(symbol='x') as x:
            self.term_x_unequal_x = x | u.c1.unequal | x
            self.term_x_unequal_x_mask = frozenset([x])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, x_unequal_x: FlexibleFormula, t: TheoryDerivation) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, x_unequal_x, _ = verify_formula(arg='x_unequal_x', input_value=x_unequal_x, u=self.u,
            form=self.term_x_unequal_x, mask=self.term_x_unequal_x_mask, raise_exception=True, error_code=error_code)
        x_unequal_x: CompoundFormula
        verify(assertion=isinstance(t, TheoryDerivation), msg=f'The argument ⌜t⌝({t}) is not a theory-derivation.',
            raise_exception=True, error_code=error_code)
        output: CompoundFormula = self.u.c1.inc(t)
        return output


class ModusPonensDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`modus-ponens<modus_ponens_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula
        p: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'modus-ponens'
        acronym = 'mp'
        abridged_name = None
        auto_index = False
        dashed_name = 'modus-ponens'
        explicit_name = 'modus ponens inference rule'
        name = 'modus ponens'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = ((p | u.c1.implies | q) | u.c1.tupl | p) | u.c1.proves | q
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_implies_q = p | u.c1.implies | q
            self.term_p_implies_q_mask = frozenset([p, q])
        with u.with_variable(symbol='P') as p:
            self.term_p = p
            self.term_p_mask = frozenset([p])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_implies_q: FlexibleFormula, p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_implies_q, _ = verify_formula(arg='p_implies_q', input_value=p_implies_q, u=self.u,
            form=self.term_p_implies_q, mask=self.term_p_implies_q_mask, raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, p, _ = verify_formula(arg='p', input_value=p, u=self.u, raise_exception=True, error_code=error_code)
        p: CompoundFormula
        p__in__p_implies_q: CompoundFormula = p_implies_q.terms[0]
        # TODO: A situation that may be difficult to troubleshoot is when two objects (e.g. variables) are given identical symbols. In this situation, the error message will look weird. To facilitate troubleshotting, we should highlight objects having the same names.
        verify(assertion=is_alpha_equivalent_to(u=self.u, phi=p__in__p_implies_q, psi=p),
            msg=f'The ⌜p⌝({p__in__p_implies_q}) in the formula argument ⌜p_implies_q⌝({p_implies_q}) is not alpha-equivalent to the formula argument ⌜p⌝({p})',
            raise_exception=True, error_code=error_code)
        q__in__p_implies_q: CompoundFormula = p_implies_q.terms[1]
        output: CompoundFormula = q__in__p_implies_q
        return output


class ModusTollensDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`modus-tollens<modus_tollens_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula
        not_q: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = u
        symbol = 'modus-tollens'
        acronym = 'mt'
        abridged_name = None
        auto_index = False
        dashed_name = 'modus-tollens'
        explicit_name = 'modus tollens inference rule'
        name = 'modus tollens'
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            definition = ((p | u.c1.implies | q) | u.c1.tupl | u.c1.lnot(q)) | u.c1.proves | u.c1.lnot(p)
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='Q') as q:
            self.term_p_implies_q = p | u.c1.implies | q
            self.term_p_implies_q_mask = frozenset([p, q])
        with u.with_variable(symbol='Q') as q:
            self.term_not_q = u.c1.lnot(q)
            self.term_not_q_mask = frozenset([q])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_implies_q: FlexibleFormula, not_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p_implies_q, _ = verify_formula(arg='p_implies_q', input_value=p_implies_q, u=self.u,
            form=self.term_p_implies_q, mask=self.term_p_implies_q_mask, raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, not_q, _ = verify_formula(arg='not_q', input_value=not_q, u=self.u, form=self.term_not_q,
            mask=self.term_not_q_mask, raise_exception=True, error_code=error_code)
        not_q: CompoundFormula
        q__in__p_implies_q: CompoundFormula = p_implies_q.terms[1]
        q__in__not_q: CompoundFormula = not_q.terms[0]
        verify(assertion=q__in__p_implies_q.is_formula_syntactically_equivalent_to(phi=q__in__not_q),
            msg=f'The ⌜q⌝({q__in__p_implies_q}) in the formula argument ⌜p_implies_q⌝({p_implies_q}) is not syntaxically-equivalent to the ⌜q⌝({q__in__not_q}) in formula argument ⌜not_q⌝({not_q})',
            raise_exception=True, error_code=error_code)
        p__in__p_implies_q: CompoundFormula = p_implies_q.terms[0]
        output: CompoundFormula = self.u.c1.lnot(p__in__p_implies_q)
        return output


class ProofByContradiction1Declaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        h: FlexibleFormula
        inc_h: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'proof-by-contradiction-1'
        acronym = 'pbc1'
        auto_index = False
        dashed_name = 'proof-by-contradiction-1'
        explicit_name = 'proof by contradiction #1 inference rule'
        name = 'proof by contradiction #1'
        with u.with_variable(symbol='H') as h, u.with_variable(symbol='P') as p:
            definition = u.c1.tupl(h | u.c1.formulates | u.c1.lnot(p), u.c1.inc(h)) | u.c1.proves | p
        with u.with_variable(symbol='P') as p:
            self.term_not_p = u.c1.lnot(p)
            self.term_not_p_mask = frozenset([p])
        with u.with_variable(symbol='H') as h:
            self.term_h = h
            self.term_h_mask = frozenset([h])
        with u.with_variable(symbol='H') as h:
            self.term_inc_h = u.c1.inc(h)
            self.term_inc_h_mask = frozenset([h])

        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        verify(assertion=isinstance(h, Hypothesis), msg=f'⌜h⌝({h}) is not an hypothesis', raise_exception=True,
            error_code=error_code)
        h: Hypothesis
        _, not_p, _ = verify_formula(arg='h.not_p', input_value=h.hypothesis_formula, u=self.u, form=self.term_not_p,
            mask=self.term_not_p_mask, raise_exception=True, error_code=error_code)
        not_p: CompoundFormula
        _, inc_h, _ = verify_formula(arg='inc_h', input_value=inc_h, u=self.u, form=self.term_inc_h,
            mask=self.term_inc_h_mask, raise_exception=True, error_code=error_code)
        h__in__inc_h: CompoundFormula = inc_h.terms[0]
        verify(assertion=is_derivably_member_of_class(u=self.u, phi=h__in__inc_h, c=self.u.c2.theory_derivation),
            msg=f'The ⌜h⌝({h__in__inc_h}) in the formula argument ⌜inc_h⌝({inc_h}) is not a theory-derivation. A typical mistake is to pass the hypothesis instead of the hypothesis child theory as the argument.',
            raise_exception=True, error_code=error_code)
        verify(assertion=h__in__inc_h.is_formula_syntactically_equivalent_to(phi=h.child_theory),
            msg=f'The ⌜h⌝({h__in__inc_h}) in the formula argument ⌜inc_h⌝({inc_h}) is not syntaxically-equivalent to the formula argument ⌜h⌝({h})',
            raise_exception=True, error_code=error_code)
        p__in__not_p: CompoundFormula = not_p.terms[0]
        output: CompoundFormula = p__in__not_p
        return output


class ProofByContradiction2Declaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        h: FlexibleFormula
        inc_h: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'proof-by-contradiction-2'
        acronym = 'pbc2'
        auto_index = False
        dashed_name = 'proof-by-contradiction-2'
        explicit_name = 'proof by contradiction #2 inference rule'
        name = 'proof by contradiction #2'
        # definition = '(𝓗 𝑎𝑠𝑠𝑢𝑚𝑒 (𝑷 ≠ 𝑸), 𝐼𝑛𝑐(𝓗)) ⊢ (𝑷 = 𝑸)'
        with u.with_variable(symbol='H') as h, u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
            definition = u.c1.tupl(h | u.c1.formulates | (x | u.c1.unequal | y), u.c1.inc(h)) | u.c1.proves | (
                x | u.c1.equal | y)
        with  u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
            self.term_x_unequal_y = (x | u.c1.unequal | y)
            self.term_x_unequal_y_mask = frozenset([x, y])
        with u.with_variable(symbol='H') as h:
            self.term_h = h
            self.term_h_mask = frozenset([h])
        with u.with_variable(symbol='H') as h:
            self.term_inc_h = u.c1.inc(h)
            self.term_inc_h_mask = frozenset([h])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        verify(assertion=isinstance(h, Hypothesis), msg=f'⌜h⌝({h}) is not an hypothesis', raise_exception=True,
            error_code=error_code)
        h: Hypothesis
        _, x_unequal_y, _ = verify_formula(arg='h.x_unequal_y', input_value=h.hypothesis_formula, u=self.u,
            form=self.term_x_unequal_y, mask=self.term_x_unequal_y_mask, raise_exception=True, error_code=error_code)
        x_unequal_y: CompoundFormula
        _, inc_h, _ = verify_formula(arg='inc_h', input_value=inc_h, u=self.u, form=self.term_inc_h,
            mask=self.term_inc_h_mask, raise_exception=True, error_code=error_code)
        h__in__inc_h: CompoundFormula = inc_h.terms[0]
        verify(assertion=is_derivably_member_of_class(u=self.u, phi=h__in__inc_h, c=self.u.c2.theory_derivation),
            msg=f'The ⌜h⌝({h__in__inc_h}) in the formula argument ⌜inc_h⌝({inc_h}) is not a theory-derivation. A typical mistake is to pass the hypothesis instead of the hypothesis child theory as the argument.',
            raise_exception=True, error_code=error_code)
        verify(assertion=h__in__inc_h.is_formula_syntactically_equivalent_to(phi=h.child_theory),
            msg=f'The ⌜h⌝({h__in__inc_h}) in the formula argument ⌜inc_h⌝({inc_h}) is not syntaxically-equivalent to the formula argument ⌜h⌝({h})',
            raise_exception=True, error_code=error_code)
        x__in__x_unequal_y: CompoundFormula = x_unequal_y.terms[0]
        y__in__x_unequal_y: CompoundFormula = x_unequal_y.terms[1]
        output: CompoundFormula = x__in__x_unequal_y | self.u.c1.equal | y__in__x_unequal_y
        return output


class ProofByRefutation1Declaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        h: FlexibleFormula
        inc_h: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'proof-by-refutation-1'
        acronym = 'pbr1'
        auto_index = False
        dashed_name = 'proof-by-refutation-1'
        explicit_name = 'proof by refutation #1 inference rule'
        name = 'proof by refutation #1'
        # definition = '(𝓗 𝑎𝑠𝑠𝑢𝑚𝑒 𝑷, 𝐼𝑛𝑐(𝓗)) ⊢ ¬𝑷'
        with u.with_variable(symbol='H') as h, u.with_variable(symbol='P') as p:
            definition = u.c1.tupl(h | u.c1.formulates | p, u.c1.inc(h)) | u.c1.proves | u.c1.lnot(p)
        with u.with_variable(symbol='P') as p:
            self.term_p = p
            self.term_p_mask = frozenset([p])
        with u.with_variable(symbol='H') as h:
            self.term_h = h
            self.term_h_mask = frozenset([h])
        with u.with_variable(symbol='H') as h:
            self.term_inc_h = u.c1.inc(h)
            self.term_inc_h_mask = frozenset([h])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        verify(assertion=isinstance(h, Hypothesis), msg=f'⌜h⌝({h}) is not an hypothesis', raise_exception=True,
            error_code=error_code)
        h: Hypothesis
        _, p, _ = verify_formula(arg='h.p', input_value=h.hypothesis_formula, u=self.u, raise_exception=True,
            error_code=error_code)
        p: CompoundFormula
        _, inc_h, _ = verify_formula(arg='inc_h', input_value=inc_h, u=self.u, form=self.term_inc_h,
            mask=self.term_inc_h_mask, raise_exception=True, error_code=error_code)
        h__in__inc_h: CompoundFormula = inc_h.terms[0]
        verify(assertion=is_derivably_member_of_class(u=self.u, phi=h__in__inc_h, c=self.u.c2.theory_derivation),
            msg=f'The ⌜h⌝({h__in__inc_h}) in the formula argument ⌜inc_h⌝({inc_h}) is not a theory-derivation. A typical mistake is to pass the hypothesis instead of the hypothesis child theory as the argument.',
            raise_exception=True, error_code=error_code)
        verify(assertion=h__in__inc_h.is_formula_syntactically_equivalent_to(phi=h.child_theory),
            msg=f'The ⌜h⌝({h__in__inc_h}) in the formula argument ⌜inc_h⌝({inc_h}) is not syntaxically-equivalent to the formula argument ⌜h⌝({h})',
            raise_exception=True, error_code=error_code)
        output: CompoundFormula = self.u.c1.lnot(p)
        return output


class ProofByRefutation2Declaration(InferenceRuleDeclaration):
    """This python class models the inclusion of :ref:`proof-by-refutation-2<proof_by_refutation_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        h: FlexibleFormula
        inc_h: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'proof-by-refutation-2'
        acronym = 'pbr2'
        auto_index = False
        dashed_name = 'proof-by-refutation-2'
        explicit_name = 'proof by refutation #2 inference rule'
        name = 'proof by refutation #2'
        # definition = '(𝓗 𝑎𝑠𝑠𝑢𝑚𝑒 (𝑷 = 𝑸), 𝐼𝑛𝑐(𝓗)) ⊢ (𝑷 ≠ 𝑸)'
        with u.with_variable(symbol='H') as h, u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
            definition = u.c1.tupl(h | u.c1.formulates | (x | u.c1.equal | y), u.c1.inc(h)) | u.c1.proves | (
                x | u.c1.unequal | y)
        with  u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
            self.term_x_equal_y = (x | u.c1.equal | y)
            self.term_x_equal_y_mask = frozenset([x, y])
        with u.with_variable(symbol='H') as h:
            self.term_h = h
            self.term_h_mask = frozenset([h])
        with u.with_variable(symbol='H') as h:
            self.term_inc_h = u.c1.inc(h)
            self.term_inc_h_mask = frozenset([h])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        verify(assertion=isinstance(h, Hypothesis), msg=f'⌜h⌝({h}) is not an hypothesis', raise_exception=True,
            error_code=error_code)
        h: Hypothesis
        _, x_equal_y, _ = verify_formula(arg='h.x_equal_y', input_value=h.hypothesis_formula, u=self.u,
            form=self.term_x_equal_y, mask=self.term_x_equal_y_mask, raise_exception=True, error_code=error_code)
        x_equal_y: CompoundFormula
        _, inc_h, _ = verify_formula(arg='inc_h', input_value=inc_h, u=self.u, form=self.term_inc_h,
            mask=self.term_inc_h_mask, raise_exception=True, error_code=error_code)
        h__in__inc_h: CompoundFormula = inc_h.terms[0]
        verify(assertion=is_derivably_member_of_class(u=self.u, phi=h__in__inc_h, c=self.u.c2.theory_derivation),
            msg=f'The ⌜h⌝({h__in__inc_h}) in the formula argument ⌜inc_h⌝({inc_h}) is not a theory-derivation. A typical mistake is to pass the hypothesis instead of the hypothesis child theory as the argument.',
            raise_exception=True, error_code=error_code)
        verify(assertion=h__in__inc_h.is_formula_syntactically_equivalent_to(phi=h.child_theory),
            msg=f'The ⌜h⌝({h__in__inc_h}) in the formula argument ⌜inc_h⌝({inc_h}) is not syntaxically-equivalent to the formula argument ⌜h⌝({h})',
            raise_exception=True, error_code=error_code)
        x__in__x_equal_y: CompoundFormula = x_equal_y.terms[0]
        y__in__x_equal_y: CompoundFormula = x_equal_y.terms[1]
        output: CompoundFormula = x__in__x_equal_y | self.u.c1.unequal | y__in__x_equal_y
        return output


class VariableSubstitutionDeclaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        p: FlexibleFormula
        phi: FlexibleFormula

    def __init__(self, u: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'variable-substitution'
        acronym = 'vs'
        abridged_name = None
        auto_index = False
        dashed_name = 'variable-substitution'
        explicit_name = 'variable substitution inference rule'
        name = 'variable substitution'
        # definition = StyledText(plaintext='(P, Phi) |- P\'', unicode='(P, 𝛷) ⊢ P\'')
        with u.with_variable(symbol='P') as p, u.with_variable(symbol='O') as o, u.with_variable(symbol='Q') as q:
            definition = (p | u.c1.tupl | o) | u.c1.proves | q
        with u.with_variable(symbol='P') as p:
            self.term_p = p
            self.term_p_mask = frozenset([p])
        with u.with_variable(symbol=StyledText(text_style=text_styles.sans_serif_bold, plaintext='Phi', unicode='Φ',
            latex='\Phi')) as phi:
            # TODO: VariableSubstitutionDeclaration: Provide a standard library of greek letters.
            # TODO: VariableSubstitutionDeclaration: Enrich how inference-rule terms may be defined to allow an expression like (v1, v2, ..., v3) using collection-defined-by-extension with n elements.
            self.term_phi = u.c1.tupl
            self.term_phi_mask = frozenset([phi])
        super().__init__(definition=definition, u=u, symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p: FlexibleFormula, phi: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_002_inference_premise_syntax_error
        _, p, _ = verify_formula(arg='p', input_value=p, u=self.u, raise_exception=True, error_code=error_code)
        p: CompoundFormula
        _, phi, _ = verify_formula(arg='phi', input_value=phi, u=self.u, raise_exception=True, error_code=error_code)
        phi: CompoundFormula
        # See the TO DO above.
        # Currently this type of term cannot be expressed with a form and mask.
        # In consequence we must check its syntax consistency here in an ad hoc manner.
        verify(assertion=isinstance(phi, CompoundFormula) and phi.connective is self.u.c1.tupl,
            msg=f'The argument ⌜phi⌝({phi}) is not a mathematical tuple (u.r.tupl) of formulas.', raise_exception=True,
            error_code=error_code)
        x_oset = get_formula_unique_variable_ordered_set(u=self.u, phi=p)
        verify(assertion=len(phi.terms) == len(x_oset),
            msg=f'The number of formulas in the collection argument ⌜phi⌝({phi}) is not equal to the number of variables in the propositional formula ⌜p⌝{p}.',
            raise_exception=True, error_code=error_code)
        x_y_map = dict((x, y) for x, y in zip(x_oset, phi.terms))
        output: CompoundFormula = p.substitute(substitution_map=x_y_map)
        # TODO: VariableSubstitutionDeclaration.construct_formula(): change the following verification step. the construct_formula() may generate a formula that is only possibly propositional. but the check_premises_validity() method must require strict-propositionality.
        verify(assertion=output.is_strictly_propositional,
            msg=f'The formula ({output}) resulting from the application of the variable-substitution inference-rule is not strictly-propositional.',
            raise_exception=True, error_code=error_code)
        return output


class AtheoreticalStatement(SymbolicObject):
    """
    Definition
    ----------
    An atheoretical-statement is a statement that is contained in a theory report
    for commentary / explanatory purposes, but that is not mathematically constitutive
    of the theory. Atheoretical-statements may be added and/or removed from a
    theory without any impact to the theory sequence of proofs.

    """

    def __init__(self, theory: TheoryDerivation, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
        subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):
        self.theory = theory
        super().__init__(u=theory.u, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=paragraph_header, ref=ref, subtitle=subtitle,
            echo=echo)  # super()._declare_class_membership_OBSOLETE(classes_OBSOLETE.atheoretical_statement)


class NoteInclusion(AtheoreticalStatement):
    """The Note pythonic-class models a note, comment, or remark in a theory.

    """

    def __init__(self, t: TheoryDerivation, content: str, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
        subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):

        echo = prioritize_value(echo, configuration.echo_note, configuration.echo_default, False)
        verify(assertion=is_derivably_member_of_class(u=t.u, phi=t, c=t.u.c2.theory_derivation),
            msg='theory is not a member of declarative-class theory.', t=t, slf=self)
        u = t.u
        paragraph_header = paragraph_headers.note if paragraph_header is None else paragraph_header
        #  self.statement_index = theory.crossreference_statement(self)
        self.theory = t
        if isinstance(content, str):
            content = SansSerifNormal(content)
        self._natural_language = content
        self.category = paragraph_header
        symbol = prioritize_value(symbol, paragraph_header.symbol_base)
        super().__init__(theory=t, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, echo=False)
        if echo:
            self.echo()  # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.note)

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='note')

    def compose_content(self) -> collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        yield self.natural_language
        return True

    def compose_report(self, proof: (None, bool) = None, **kwargs):
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_note_report(o=self, proof=proof)
        return output

    def echo(self):
        repm.prnt(self.rep_report())

    @property
    def natural_language(self) -> str:
        """Return the content of the note in natural-language."""
        return self._natural_language


section_category = ParagraphHeader(name='section', symbol_base='§', natural_name='section', abridged_name='sect.')


class Section(AtheoreticalStatement):
    """A (leveled) section in a theory-derivation.

    Sections allow to organize / structure (lengthy) theory-derivations
    to improve readability.

    """

    def __init__(self, section_title: str, t: TheoryDerivation, section_number: (None, int) = None,
        section_parent: (None, Section) = None, numbering: (None, bool) = None, echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_note, configuration.echo_default, False)
        numbering = prioritize_value(numbering, True)
        self._section_title = section_title
        self._section_parent = section_parent
        self._section_level = 1 if section_parent is None else section_parent.section_level + 1
        if section_parent is not None:
            section_number = section_parent.get_next_section_number(section_number)
        else:
            section_number = t.get_next_section_number(section_number)
        self._section_number = section_number
        self._numbering = numbering
        prefix = '' if section_parent is None else section_parent.section_reference + '.'
        self._section_reference = f'{prefix}{str(section_number)}'
        self.statement_index = t.crossreference_statement(self)
        self._max_subsection_number = 0
        self.category = section_category
        index = self.statement_index
        symbol = self.category.symbol_base
        super().__init__(symbol=symbol, index=index, theory=t, echo=False)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.note)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, Composable, bool]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='section')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        yield '#' * self.section_level  # This is only valid for plaintext and unicode, not latex
        yield text_dict.space
        if self.numbering:
            yield from SansSerifBold(self.section_reference).compose()
            yield ': '
        yield from SansSerifBold(str(self.section_title).capitalize()).compose()
        return True

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

    @property
    def numbering(self) -> bool:
        return self._numbering

    def rep_ref(self, cap=False) -> str:
        prefix = 'section' if self.section_level == 1 else 'sub-' * (self.section_level - 1) + 'section'
        text = f'{prefix}{repm.serif_bold(self.section_reference)}'
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


class TheoryDerivation(Formula):
    """The TheoryElaboration pythonic class models a [theory-elaboration](theory-elaboration).

    """

    def __init__(self, u: UniverseOfDiscourse, symbol: (None, str, StyledText) = None, index: (None, int, str) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str) = None, name: (None, str) = None,
        explicit_name: (None, str) = None, ref: (None, str) = None, subtitle: (None, str) = None,
        extended_theory: (None, TheoryDerivation) = None, extended_theory_limit: (None, Statement) = None,
        stabilized: bool = False, echo: bool = None):
        echo = prioritize_value(echo, configuration.echo_theory_derivation_declaration, configuration.echo_default,
            False)
        verify_universe_of_discourse(u=u)
        self._max_subsection_number = 0
        self._consistency = consistency_values.undetermined
        self._stabilized = False
        self.axiom_inclusions = tuple()
        self.definition_inclusions = tuple()
        self._inference_rule_inclusions = InferenceRuleInclusionCollection(t=self)
        self.statements = tuple()
        self._extended_theory = extended_theory
        self._extended_theory_limit = extended_theory_limit
        self._interpretation_disclaimer = False
        symbol = prioritize_value(symbol, configuration.default_theory_symbol)
        super().__init__(symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name, name=name,
            explicit_name=explicit_name, paragraph_header=paragraph_headers.theory_derivation,
            is_theory_foundation_system=True if extended_theory is None else False, u=u, echo=False)
        if extended_theory is not None:
            verify(is_derivably_member_of_class(u=u, phi=extended_theory, c=u.c2.theory_derivation),
                'Parameter "extended_theory" is neither None nor a member of declarative-class theory.', u=u)
            verify(extended_theory_limit is None or (is_declaratively_member_of_class(u=u, phi=extended_theory_limit,
                c=u.c2.statement) and extended_theory_limit in extended_theory.statements),
                'Parameter "theory_extension_statement_limit" is inconsistent.', u=u)
        u.t.declare_instance(t=self)
        if stabilized:
            # It is a design choice to stabilize the theory-elaboration
            # at the very end of construction (__init__()). Note that it
            # is thus possible to extend a theory and, for example,
            # add some new inference-rules by passing these instructions
            # to the constructor.
            self.stabilize()
        if echo:
            self.echo()

    def assure_interpretation_disclaimer(self, echo: (None, bool) = None):
        """After the first usage of a contentual interpretation inference-rule,
        warns the user that no semantic verification is performed."""
        echo = prioritize_value(echo, configuration.echo_default, False)
        if not self._interpretation_disclaimer:
            self.take_note('By design, punctilious_obsolete_20240114 assures the syntactical correctness of theories, '
                           'but does not perform any '
                           'semantic verification. Therefore, the usage of inference-rules that interpret '
                           'natural content (i.e. '
                           'axiom-interpretation and definition-interpretation) is critically dependent on '
                           'the correctness of '
                           'the content translation performed by the theory author, from axiom or definition '
                           'natural language, '
                           'to formulae.', paragraph_header=paragraph_headers.warning, echo=echo)
            self._interpretation_disclaimer = True

    def compose_article(self, proof: (None, bool) = None) -> collections.abc.Generator[Composable, Composable, bool]:
        """Return a representation that expresses and justifies the theory."""
        # TODO: compose_article: move this outside of the theory
        output = yield from configuration.locale.compose_theory_article(t=self, proof=proof)
        return output

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='theory-derivation')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_theory_declaration(t=self)
        return output

    def crossreference_axiom_inclusion(self, a):
        """During construction, cross-reference an axiom
        with its parent theory (if it is not already cross-referenced),
        and return its 0-based index in Theory.axioms."""
        assert isinstance(a, AxiomInclusion)
        if a not in self.axiom_inclusions:
            self.axiom_inclusions = self.axiom_inclusions + tuple([a])
        return self.axiom_inclusions.index(a)

    def crossreference_definition_endorsement(self, d):
        """During construction, cross-reference an endorsement
        with its parent theory (if it is not already cross-referenced),
        and return its 0-based index in Theory.endorsements."""
        if d not in self.definition_inclusions:
            self.definition_inclusions = self.definition_inclusions + tuple([d])
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
        assert isinstance(s, (Statement, NoteInclusion, Section))
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

    def echo(self):
        repm.prnt(self.rep_report())

    @property
    def extended_theory(self) -> (None, TheoryDerivation):
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
        """Return the dictionary of inference-rule-inclusions contained in this
theory-elaboration."""
        return self.inference_rule_inclusions

    @property
    def inference_rule_inclusions(self):
        """Return the dictionary of inference-rule-inclusions contained in this
        theory-elaboration."""
        return self._inference_rule_inclusions

    def is_formula_syntactically_equivalent_to(self, phi: FlexibleFormula) -> bool:
        """Returns true if ⌜self⌝ is formula-syntactically-equivalent to ⌜o2⌝.

        Parameters:
        -----------
        o2 : Formula
            The formula with which to verify formula-equivalence.

        """
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        return self is phi

    @property
    def is_strictly_propositional(self) -> bool:
        """By definition, a theory-derivation is not a propositional object."""
        return False

    def iterate_theoretical_objcts_references(self, include_root: bool = True, visited: (None, set) = None,
        substitute_constants_with_values: bool = True):
        """Iterate through this and all the formulas it references recursively.

        Theoretical-objcts may contain references to multiple and diverse other formulas. Do not confuse this iteration of all references with iterations of objects in the theory-chain.

        :term include_root:
        :term visited:
        :return:
        """
        # TODO: Merge methods iterate_statements_in_theory_chain and iterate_theoretical_objcts_references
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        for statement in set(self.statements).difference(visited):
            if not isinstance(statement, AtheoreticalStatement):
                yield statement
                visited.update({statement})
                yield from statement.iterate_theoretical_objcts_references(include_root=False, visited=visited,
                    substitute_constants_with_values=substitute_constants_with_values)
        if self.extended_theory is not None and self.extended_theory not in visited:
            # Iterate the extended-theory.
            if self.extended_theory_limit is not None:
                # The extended-theory is limited
                # i.e. this theory branched out before the end of the elaboration.
                # Thus, we must exclude statements that are posterior to the limit.
                # To do this, we simply black-list them
                # by including them in the visited set.
                black_list = (statement for statement in set(self.extended_theory.statements) if
                    statement.statement_index > self.extended_theory_limit.statement_index)
                visited.update(black_list)
            yield self.extended_theory
            visited.update({self.extended_theory})
            yield from self.extended_theory.iterate_theoretical_objcts_references(include_root=False, visited=visited,
                substitute_constants_with_values=substitute_constants_with_values)

    def include_axiom(self, a: AxiomDeclaration, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, echo: (None, bool) = None) -> AxiomInclusion:
        """Include an axiom in this theory-derivation."""
        return AxiomInclusion(a=a, t=self, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, paragraph_header=paragraph_header, echo=echo)

    def include_definition(self, d: DefinitionDeclaration, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        echo: (None, bool) = None) -> DefinitionInclusion:
        """Include a definition in this theory-derivation."""
        return DefinitionInclusion(d=d, t=self, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle, echo=echo)

    def iterate_statements_in_theory_chain(self, formula_syntactic_equivalence_filter: (None, CompoundFormula) = None,
        formula_alpha_equivalence_filter: (None, CompoundFormula) = None):
        """Iterate through the (proven or sound) statements in the current theory-chain.

        :param formula_syntactic_equivalence_filter: (conditional) Filters on formula-statements that are formula-syntactically-equivalent.
        :return:
        """
        # TODO: Merge methods iterate_statements_in_theory_chain and iterate_theoretical_objcts_references
        # TODO: This iterator function does not support theory_extension_limit which is mandatory when posing hypothesis.
        if formula_syntactic_equivalence_filter is not None:
            _, formula_syntactic_equivalence_filter, _ = verify_formula(u=self.u,
                input_value=formula_syntactic_equivalence_filter, raise_exception=True)
        for t in self.iterate_theory_chain():
            for s in t.statements:
                if not isinstance(s, AtheoreticalStatement):
                    # Getting read of non-sense objects such as section, etc.
                    if (formula_syntactic_equivalence_filter is not None and s.is_formula_syntactically_equivalent_to(
                        formula_syntactic_equivalence_filter)) or (
                        formula_alpha_equivalence_filter is not None and is_alpha_equivalent_to(u=self.u,
                        phi=formula_alpha_equivalence_filter, psi=s)) or (
                        formula_syntactic_equivalence_filter is None and formula_alpha_equivalence_filter is None):
                        # if formula_syntactic_equivalence_filter is None or (is_declaratively_member_of_class(u=self.u, phi=s,
                        #    c=self.u.c2.formula_statement) and s.is_formula_syntactically_equivalent_to(
                        #    formula_syntactic_equivalence_filter)):
                        # if formula is None or (is_in_class_OBSOLETE(s,
                        #    classes_OBSOLETE.formula_statement) and s.is_formula_syntactically_equivalent_to(formula)):
                        yield s

    def iterate_theory_chain(self, visited: (None, set) = None):
        """Iterate over the theory-chain of this theory.

        The sequence is : this theory, this theory's extended-theory, the extended-theory's
        extended-theory, etc. until the root-theory is processes.

        Note
        -----

        The theory-chain set is distinct from theory-dependency set.
        The theory-chain informs of the parent theory whose statements are considered
        valid in the current theory.
        Distinctively, theory may be referenced by meta-theorizing, or in hypothesis,
        or possibly other use cases.
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
            if is_in_class_OBSOLETE(s, classes_OBSOLETE.formula_statement) and s.valid_proposition not in visited:
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

    def contains_statement_in_theory_chain(self, phi: FlexibleStatement):
        """Returns True if this theory-derivation contains phi in its theory-chain, False otherwise."""
        # _, phi, _ = verify_formula_statement(t=self, input_value=phi, arg='phi', raise_exception=True)
        # return any(self.iterate_statements_in_theory_chain(formula_alpha_equivalence_filter=phi))
        return any(psi for psi in self.iterate_theoretical_objcts_references() if
            is_alpha_equivalent_to(u=self.u, phi=phi, psi=psi))

    @property
    def inconsistency_introduction_inference_rule_is_included(self):
        """True if the inconsistency-introduction inference-rule is included in this theory,
        False otherwise."""
        if self._includes_inconsistency_introduction_inference_rule is not None:
            return self._includes_inconsistency_introduction_inference_rule
        elif self.extended_theory is not None:
            return self.extended_theory.inconsistency_introduction_inference_rule_is_included
        else:
            return None

    def d(self, natural_language, symbol=None, reference=None, title=None):
        """Elaborate a new definition with natural-language. Shortcut function for
        t.elaborate_definition(...)."""
        return self.include_definition(natural_language=natural_language, nameset=symbol, reference=reference,
            title=title)

    def get_first_syntactically_equivalent_statement(self, formula: CompoundFormula):
        """Given a formula, return the first statement that is syntactically-equivalent with it, or None if none are found.

        :param formula:
        :return:
        """
        return next(self.iterate_statements_in_theory_chain(formula_syntactic_equivalence_filter=formula), None)

    def pose_hypothesis(self, hypothesis_formula: CompoundFormula, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        echo: (None, bool) = None) -> Hypothesis:
        """Pose a new hypothesis in the current theory."""
        _, hypothesis_formula, _ = verify_formula(u=self.u, input_value=hypothesis_formula)
        return Hypothesis(t=self, hypothesis_formula=hypothesis_formula, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle, echo=echo)

    def prnt(self, proof: (None, bool) = None):
        repm.prnt(self.rep_report(proof=proof))

    def prove_inconsistent(self, ii):
        verify(isinstance(ii, InconsistencyIntroductionStatement),
            'The ii statement is not of type InconsistencyIntroductionStatement.', ii=ii, theory=self)
        verify(ii in self.statements, 'The ii statement is not a statement of this theory.', ii=ii, theory=self)
        self._consistency = consistency_values.proved_inconsistent

    def export_article_to_file(self, file_path, proof: (None, bool) = None, encoding: (None, Encoding) = None):
        """Export this theory to a Unicode textfile."""
        text_file = open(file_path, 'w', encoding='utf-8')
        n = text_file.write(self.rep_article(encoding=encoding, proof=proof))
        text_file.close()

    def open_section(self, section_title: str, section_number: (None, int) = None,
        section_parent: (None, Section) = None, numbering: (None, bool) = None, echo: (None, bool) = None) -> Section:
        """Open a new section in the current theory-derivation."""
        return Section(section_title=section_title, section_number=section_number, section_parent=section_parent,
            numbering=numbering, t=self, echo=echo)

    def rep_article(self, encoding: (None, Encoding) = None, proof: (None, bool) = None) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_article(proof=proof), encoding=encoding)

    def report_inconsistency_proof(self, proof: InferredStatement):
        """This method is called by InferredStatement.__init__() when the inferred-statement
         proves the inconsistency of a theory."""
        verify(is_declaratively_member_of_class(u=self.u, phi=proof, c=self.u.c2.inferred_statement),
            '⌜proof⌝ must be an inferred-statement.', proof=proof, slf=self)
        proof: CompoundFormula
        proof = unpack_formula(proof)
        verify(proof.connective is self.u.c1.inconsistency,
            'The connective of the ⌜proof⌝ formula must be ⌜inconsistency⌝.', proof_connective=proof.connective,
            proof=proof, slf=self)
        verify(proof.terms[0] is self, 'The term of the ⌜proof⌝ formula must be the current theory, i.e. ⌜self⌝.',
            proof_term=proof.terms[0], proof=proof, slf=self)
        self._consistency = consistency_values.proved_inconsistent

    @property
    def stabilized(self):
        """Return the stabilized property of this theory-elaboration.
        """
        return self._stabilized

    def stabilize(self):
        verify(not self._stabilized, 'This theory-elaboration is already stabilized.',
            severity=verification_severities.warning)
        self._stabilized = True

    def take_note(self, content: str, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
        subtitle: (None, str, StyledText) = None, echo: (None, bool) = None) -> NoteInclusion:
        """Take a note, make a comment, or remark in this theory.
        """
        return self.u.take_note(t=self, content=content, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, echo=echo)

    @property
    def theoretical_objcts(self):
        list = set()
        for s in self.statements:
            list.add(s)
            if is_in_class_OBSOLETE(s, classes_OBSOLETE.compound_formula):
                list.add()


class Hypothesis(Statement):
    # TODO: QUESTION: Hypothesis class: consider a data model modification where Hypothesis would be split into a Declaration in the universe and an Inclusion in a Theory.
    def __init__(self, t: TheoryDerivation, hypothesis_formula: CompoundFormula, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):
        paragraph_header = paragraph_headers.hypothesis
        # TODO: Check that all components of the hypothetical-proposition
        #  are elements of the source theory-branch.
        symbol = prioritize_value(symbol, configuration.default_parent_hypothesis_statement_symbol)
        super().__init__(theory=t, symbol=symbol, index=index, auto_index=auto_index, paragraph_header=paragraph_header,
            subtitle=subtitle, dashed_name=dashed_name, echo=False)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.hypothesis)
        self._hypothesis_formula = hypothesis_formula
        # When a hypothesis is posed in a theory 𝒯₁,
        # ...the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        self._hypothesis_axiom_declaration = self.u.a.declare(
            f'By hypothesis, assume {hypothesis_formula.rep_formula()} is true.', echo=echo)
        # ...a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        self._hypothesis_child_theory = t.u.t.declare(extended_theory=t, extended_theory_limit=self,
            symbol=configuration.default_child_hypothesis_theory_symbol, echo=echo)
        # ...the axiom is included in 𝒯₂,
        self._hypothesis_axiom_inclusion_in_child_theory = self.hypothesis_child_theory.include_axiom(
            a=self.hypothesis_axiom_declaration, echo=echo)
        # ...and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂.
        self._hypothesis_statement_in_child_theory = self.hypothesis_child_theory.i.axiom_interpretation.infer_formula_statement(
            self.hypothesis_axiom_inclusion_in_child_theory, hypothesis_formula, echo=echo)
        verify(assertion=hypothesis_formula.is_strictly_propositional,
            msg='The hypothetical-formula is not strictly-propositional.', hypothetical_formula=hypothesis_formula,
            slf=self)
        echo = prioritize_value(echo, configuration.echo_hypothesis, configuration.echo_inferred_statement, False)
        if echo:
            self.echo()

    @property
    def child_theory(self) -> TheoryDerivation:
        """A shortcut for self.hypothesis_child_theory"""
        return self.hypothesis_child_theory

    @property
    def child_statement(self) -> InferredStatement:
        """A shortcut for self.hypothesis_statement_in_child_theory"""
        return self._hypothesis_statement_in_child_theory

    def compose_class(self) -> collections.abc.Generator[Composable, Composable, True]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='hypothesis')
        return True

    def compose_report(self, proof: (None, bool) = None, **kwargs):
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_parent_hypothesis_statement_report(o=self, proof=proof)
        return output

    def echo(self):
        repm.prnt(self.rep_report())

    @property
    def hypothesis_axiom_declaration(self) -> AxiomDeclaration:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothesis_axiom_declaration

    @property
    def hypothesis_axiom_inclusion_in_child_theory(self) -> AxiomInclusion:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothesis_axiom_inclusion_in_child_theory

    @property
    def hypothesis_formula(self) -> CompoundFormula:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothesis_formula

    @property
    def hypothesis_statement_in_child_theory(self) -> InferredStatement:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothesis_statement_in_child_theory

    @property
    def hypothesis_child_theory(self) -> TheoryDerivation:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothesis_child_theory

    @property
    def is_strictly_propositional(self) -> bool:
        """The hypothesis object by itself is not a propositional object,
        not to be confused with the hypothesis formula."""
        return False


class Connective(Formula):
    """The declaration of a connective in the universe-of-discourse.
    """

    def __init__(self, u: UniverseOfDiscourse, arity: (None, int) = None, min_arity: (None, int) = None,
        max_arity: (None, int) = None, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, formula_rep=None, signal_proposition=None, signal_theoretical_morphism=None,
        implementation=None, collection_start: (None, StyledText) = None,
        collection_separator: (None, StyledText) = None, collection_end: (None, StyledText) = None,
        dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
        abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
        explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
        subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):
        """

        :param u:
        :param arity: A fixed arity constraint for well-formed formula. Formulae based on this connective with distinct arity are ill-formed. Equivalent to passing the same value to both min_arity, and max_arity.
        :param min_arity: A fixed minimum (inclusive) arity constraint for well-formed formula. Formulae based on this connective with lesser arity are ill-formed.
        :param max_arity: A fixed maximum (inclusive) arity constraint for well-formed formula. Formulae based on this connective with greater arity are ill-formed.
        :param symbol:
        :param index:
        :param auto_index:
        :param formula_rep: The default representation method for formulae based on this connective, including: function-call, infix-operator, postfix-operator, and collection.
        :param signal_proposition:
        :param signal_theoretical_morphism:
        :param implementation:
        :param collection_start: If representation of formulae based on this connective should support collection style, the starting element (e.g. an opening parenthesis).
        :param collection_separator: If representation of formulae based on this connective should support collection style, the separator element (e.g. a comma).
        :param collection_end: If representation of formulae based on this connective should support collection style, the ending element (e.g. an closing parenthesis).
        :param dashed_name:
        :param acronym:
        :param abridged_name:
        :param name:
        :param explicit_name:
        :param ref:
        :param subtitle:
        :param nameset:
        :param echo:
        """
        echo = prioritize_value(echo, configuration.echo_connective, configuration.echo_default, False)
        auto_index = prioritize_value(auto_index, configuration.auto_index, True)
        assert isinstance(u, UniverseOfDiscourse)
        signal_proposition = False if signal_proposition is None else signal_proposition
        signal_theoretical_morphism = False if signal_theoretical_morphism is None else signal_theoretical_morphism
        assert isinstance(signal_proposition, bool)
        assert isinstance(signal_theoretical_morphism, bool)
        cat = paragraph_headers.connective_declaration
        self.formula_rep = CompoundFormula.function_call if formula_rep is None else formula_rep
        self.signal_proposition = signal_proposition
        self.signal_theoretical_morphism = signal_theoretical_morphism
        self.implementation = implementation
        self.arity = arity
        self.min_arity = min_arity
        self.max_arity = max_arity
        self.collection_start = collection_start
        self.collection_separator = collection_separator
        self.collection_end = collection_end
        symbol = configuration.default_connective_symbol if symbol is None else symbol
        super().__init__(u=u, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, paragraph_header=cat,
            ref=ref, subtitle=subtitle, echo=False)
        self.u.c1.declare_instance(c=self)
        if echo:
            self.echo()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((Connective, self.nameset, self.arity))

    def compose_class(self) -> collections.abc.Generator[Composable, Composable, bool]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='connective')
        return True

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        global text_dict
        yield SansSerifNormal('Let ')
        yield text_dict.open_quasi_quote
        yield from self.compose_symbol()
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be a ')
        yield rep_arity_as_text(self.arity)
        yield text_dict.space
        yield SerifItalic('connective')
        yield SansSerifNormal(' in ')
        yield from self.u.compose_symbol()
        yield SansSerifNormal(' (default notation: ')
        yield SansSerifNormal(str(self.formula_rep))
        yield SansSerifNormal(').')
        return True

    def echo(self):
        repm.prnt(self.rep_report())

    def is_strictly_propositional(self) -> bool:
        "A connective is not a propositional object by definition. But note that formulae based on a connective are propositional if the connective signals a proposition."
        return False


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


class SimpleObjct(Formula):
    """
    Definition
    ----------
    A simple-objct-component ℴ is a formula that has no special attribute,
    and whose sole function is to provide the meaning of being itself.

    TODO: SimpleObjct: By design, a SimpleObjct should also be a Formula. As an immediate measure, I implement the method is_syntactic_equivalent() to make it compatible, but the data model should be improved.
    """

    def __init__(self, u: UniverseOfDiscourse, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_simple_objct_declaration, configuration.echo_default, False)
        super().__init__(u=u, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, echo=False)
        self.u.o.declare_instance(o=self)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='simple-object')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_simple_objct_declaration(o=self)
        return output

    def echo(self):
        repm.prnt(self.rep_report())

    def is_masked_formula_similar_to_OBSOLETE(self, phi, mask, _values):
        # TODO: Remove this method and use only a central method on Formula.
        assert isinstance(phi, Formula)
        if isinstance(phi, FreeVariable):
            if phi in mask:
                # o2 is a variable, and it is present in the mask.
                # first, we must check if it is already in the dictionary of values.
                if phi in _values:
                    # the value is already present in the dictionary.
                    known_value = _values[phi]
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
                    _values[phi] = self
                    return True, _values
        if not isinstance(phi, SimpleObjct):
            # o1 (self) is a simple-objct, and o2 is something else.
            # in consequence, masked-formula-similitude is no longer preserved.
            return False, _values
        # o2 is not a variable.
        return self.is_formula_syntactically_equivalent_to(phi), _values

    def is_strictly_propositional(self) -> bool:
        """A simple-object if propositional if and only if it is truth or the falsehood."""
        if self is self.u.o.truth or self is self.u.o.falsehood:
            return True
        else:
            return False


class ClassDeclaration(Formula):
    """Initially developed to support metatheoretic statements such as p is-a
    propositional-variable.
    """

    def __init__(self, u: UniverseOfDiscourse, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, python_class: (None, type) = None, is_class_of_class: (None, bool) = None,
        echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_simple_objct_declaration, configuration.echo_default, False)
        super().__init__(u=u, symbol=symbol, index=index, auto_index=auto_index, echo=False)
        self._python_class = python_class
        self._is_class_of_class = is_class_of_class
        u.c2.declare_instance(c=self)
        self._internal_container = frozenset()
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        yield SerifItalic(plaintext='class')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_class_declaration(o=self)
        return output

    def echo(self):
        repm.prnt(self.rep_report())

    @property
    def is_class_of_class(self) -> bool:
        return self._is_class_of_class

    def is_strictly_propositional(self) -> bool:
        # OBSOLETE PROPERTY
        return False

    @property
    def python_class(self) -> (None, type):
        """Some python classes model the declaration of objects in a universe-of-discourse.
        These are object-declaration classes.
        Object-declaration classes often declare objects of a certain class c.
        This property returns the python object-declaration class that models c.

        :return:
        """
        return self._python_class


class SymbolicObjectAccretor(set, abc.ABC):
    """A basic collection that does not allow the removal of symbols."""

    def __init__(self, container: (None, SymbolicObject)):
        self._container = container
        super().__init__()

    def add(self, symbolic_object: object):
        if isinstance(symbolic_object, SymbolicObject):
            self.add_symbolic_object(symbolic_object)
        else:
            raise Exception('This class only supports adding elements of the SymbolicObject type.')

    def add_symbolic_object(self, symbolic_object: SymbolicObject):
        self.verify(symbolic_object=symbolic_object)
        if symbolic_object not in self:
            # For symbols, python-equality is strict object instance equality.
            # We add the object to the collection only if it is not already there.
            super().add(symbolic_object)
        return symbolic_object

    @property
    def container(self) -> SymbolicObject:
        return self._container

    def get_base_symbol_max_index(self, symbol: FlexibleSymbol) -> int:
        """Return the highest index for that base symbol in the collection."""
        _, symbol, _ = verify_symbol(input_value=symbol)
        equivalent_symbols = tuple((symbolic_object.nameset.index_as_int for symbolic_object in self if
            symbolic_object.is_base_symbol_equivalent(symbol) and symbolic_object.nameset.index_as_int is not None))
        return max(equivalent_symbols, default=0)

    def index_symbol(self, symbol: (str, StyledText)) -> int:
        """Given a symbol-base S (i.e. an unindexed symbol), returns a unique integer n
        such that (S, n) is a unique identifier in this instance of UniverseOfDiscourse.

        :param symbol: The symbol-base.
        :return:
        """
        if isinstance(symbol, str):
            # The default symbol format is sans-serif italic.
            symbol = SansSerifItalic(symbol)
        return self.get_base_symbol_max_index(symbol) + 1

    def remove(self, element: object):
        raise Exception('This class forbids the removal of elements.')

    def verify(self, symbolic_object: SymbolicObject, raise_exception: bool = True) -> (bool, Formula, str):
        """This method is called before adding new elements. It is expected to raise an exception if the element does
         not meet the requirements for the collection."""
        if not isinstance(symbolic_object, SymbolicObject):
            msg: str = 'symbolic_object is not of type SymbolicObject.'
            if raise_exception:
                raise Exception(msg)
            else:
                return False, None, msg
        return True, symbolic_object, str


class FormulaAccretor(set, abc.ABC):
    """A basic collection that does not allow the removal of elements."""

    def __init__(self, container: (None, Formula)):
        self._container = container
        super().__init__()

    def add(self, element: object):
        if isinstance(element, Formula):
            self.add_formula(element)
        else:
            raise Exception('This class only supports adding elements of the Formula type.')

    def add_formula(self, phi: Formula):
        self.verify(phi=phi)
        if phi in self:
            # phi == some existing element of the collection.
            # but it may be that phi *is* not that element.
            # in this particular situation,
            # we retrieve and return the existing element,
            # and discard the original *phi* argument.
            phi = next((element for element in self if element == phi), None)
        else:
            super().add(phi)
        return phi

    @property
    def container(self) -> Formula:
        return self._container

    def remove(self, element: object):
        raise Exception('This class forbids the removal of elements.')

    def verify(self, phi: FlexibleFormula, raise_exception: bool = True) -> (bool, Formula, str):
        """This method is called before adding new elements. It is expected to raise an exception if the element does
         not meet the requirements for the collection."""
        if not isinstance(phi, Formula):
            msg: str = 'phi is not of type Formula.'
            if raise_exception:
                raise Exception(msg)
            else:
                return False, None, msg
        return True, phi, str


class MultiverseFormulaAccretor(FormulaAccretor):
    def __init__(self):
        super().__init__(container=None)

    def create(self, symbol: (None, str, StyledText) = None, index: (None, int, str) = None,
        auto_index: (None, bool) = None, echo: (None, bool) = None) -> UniverseOfDiscourse:
        u: UniverseOfDiscourse = UniverseOfDiscourse(symbol=symbol, index=index, auto_index=auto_index, echo=echo)
        # contrary to formula, we do not substitute the instance of universe-of-discourse:
        # u = self.declare_instance(u=u)
        return u

    def create_instance(self, u: UniverseOfDiscourse) -> UniverseOfDiscourse:
        u = super().add_formula(phi=u)
        return u

    def verify(self, phi: FlexibleFormula, raise_exception: bool = True) -> (bool, Formula, str):
        """This method is called before adding new elements."""
        if not isinstance(phi, UniverseOfDiscourse):
            msg: str = 'phi is not of type UniverseOfDiscourse.'
            if raise_exception:
                raise Exception(msg)
            else:
                return False, None, msg
        return True, phi, str


multiverse = MultiverseFormulaAccretor()


class UniverseOfDiscourseSymbolicObjectAccretor(SymbolicObjectAccretor):
    """A basic collection that does not allow the removal of elements."""

    def __init__(self, u: UniverseOfDiscourse):
        self._u = u
        super().__init__(container=u)

    def declare_symbolic_object_instance(self, symbolic_object: SymbolicObject) -> SymbolicObject:
        return super().add_symbolic_object(symbolic_object=symbolic_object)

    @property
    def u(self) -> UniverseOfDiscourse:
        return self._u

    def verify(self, symbolic_object: SymbolicObject, raise_exception: bool = True):
        ok: bool
        msg: str
        ok, phi, msg = verify_symbolic_object(u=self.u, input_value=symbolic_object, raise_exception=raise_exception)
        return ok, phi, msg


class UniverseOfDiscourseFormulaAccretor(FormulaAccretor):
    """A basic collection that does not allow the removal of elements."""

    def __init__(self, u: UniverseOfDiscourse):
        self._u = u
        super().__init__(container=u)

    def declare_formula_instance(self, phi: Formula) -> Formula:
        return super().add_formula(phi=phi)

    @property
    def u(self) -> UniverseOfDiscourse:
        return self._u

    def verify(self, phi: FlexibleFormula, raise_exception: bool = True):
        ok: bool
        msg: str
        ok, phi, msg = verify_formula(u=self.u, input_value=phi, raise_exception=raise_exception)
        return ok, phi, msg


class SimpleObjctDict(UniverseOfDiscourseFormulaAccretor):

    def __init__(self, u: UniverseOfDiscourse):
        super().__init__(u=u)
        # Well-known objects
        self._falsehood = None
        self._truth = None

    def declare(self, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        echo: (None, bool) = None) -> SimpleObjct:
        return SimpleObjct(symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref, subtitle=subtitle, u=self.u,
            echo=echo)

    def declare_instance(self, o: SimpleObjct) -> SimpleObjct:
        return super().add_formula(phi=o)

    @property
    def fals(self):
        return self.falsehood

    @property
    def falsehood(self):
        if self._falsehood is None:
            self._falsehood = self.declare(nameset=NameSet(
                symbol=StyledText(unicode='⊥', latex='\\bot', plaintext='false', text_style=text_styles.serif_normal),
                name=ComposableText(plaintext='false'), explicit_name=ComposableText(plaintext='falsehood'),
                index=None))
        return self._falsehood

    @property
    def connective(self):
        if self._connective is None:
            self._connective = self.declare(symbol='connective', name='connective', auto_index=False,
                abridged_name='rel.')
        return self._connective

    @property
    def tru(self):
        return self.truth

    @property
    def truth(self):
        if self._truth is None:
            self._truth = self.declare(nameset=NameSet(
                symbol=StyledText(unicode='⊤', latex='\\top', plaintext='true', text_style=text_styles.serif_normal),
                name=ComposableText(plaintext='true'), explicit_name=ComposableText(plaintext='truth'), index=None))
        return self._truth

    def verify_element(self, phi: FlexibleFormula):
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        verify(assertion=is_declaratively_member_of_class(u=self.u, phi=phi, c=self.u.c2.simple_object),
            msg='phi is not a simple-object')


class AxiomDeclarationAccretor(UniverseOfDiscourseFormulaAccretor):
    """A collection of axiom-declarations.
    It is exposed as the a property on the UniverseOfDiscourse class.

    """

    def __init__(self, u: UniverseOfDiscourse):
        super().__init__(u=u)

    def declare(self, natural_language: str, symbol: (None, str, StyledText) = None, index: (None, int, str) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, echo: (None, bool) = None) -> AxiomDeclaration:
        """:ref:`Declare<object_declaration_math_concept>` a new axiom in this universe-of-discourse.
        """
        return AxiomDeclaration(u=self.u, natural_language=natural_language, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle, paragraph_header=paragraph_header, echo=echo)

    def declare_instance(self, a: AxiomDeclaration) -> AxiomDeclaration:
        return super().add_formula(phi=a)

    def verify_element(self, phi: FlexibleFormula):
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        verify(assertion=is_declaratively_member_of_class(u=self.u, phi=phi, c=self.u.c2.axiom_declaration),
            msg='phi is not an axiom-declaration')


class DefinitionDeclarationAccretor(UniverseOfDiscourseFormulaAccretor):
    """A collection of definition-declarations.
    It is exposed as the d property on the UniverseOfDiscourse class.

    """

    def __init__(self, u: UniverseOfDiscourse):
        super().__init__(u=u)

    def declare(self, natural_language: str, symbol: (None, str, StyledText) = None, index: (None, int, str) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, echo: (None, bool) = None) -> DefinitionDeclaration:
        """:ref:`Declare<object_declaration_math_concept>` a new definition in this universe-of-discourse.
        """
        d: DefinitionDeclaration = DefinitionDeclaration(u=self.u, natural_language=natural_language, symbol=symbol,
            index=index, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name,
            name=name, explicit_name=explicit_name, ref=ref, subtitle=subtitle, paragraph_header=paragraph_header,
            echo=echo)
        d = self.declare_instance(d=d)  # Return the existing definition if there is an definition a' such that a' == a.
        return d

    def declare_instance(self, d: DefinitionDeclaration) -> DefinitionDeclaration:
        d = super().add_formula(phi=d)
        return d

    def verify_element(self, phi: FlexibleFormula):
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        verify(assertion=is_declaratively_member_of_class(u=self.u, phi=phi, c=self.u.c2.definition_declaration),
            msg='phi is not an definition-declaration')


class TheoryDerivationDeclarationAccretor(UniverseOfDiscourseFormulaAccretor):
    """A collection of theory-derivation declarations.
    It is exposed as the t property on the UniverseOfDiscourse class.

    """

    def __init__(self, u: UniverseOfDiscourse):
        super().__init__(u=u)

    def declare(self, extended_theory: (None, TheoryDerivation) = None, extended_theory_limit: (None, Statement) = None,
        stabilized: bool = False, symbol: (None, str, StyledText) = None, index: (None, int, str) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        echo: (None, bool) = None) -> TheoryDerivation:
        """:ref:`Declare<object_declaration_math_concept>` a new axiom in this universe-of-discourse.
        """
        t: TheoryDerivation = TheoryDerivation(u=self.u, extended_theory=extended_theory,
            extended_theory_limit=extended_theory_limit, stabilized=stabilized, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, echo=echo)
        t = self.declare_instance(t=t)  # Return the existing axiom if there is an axiom a' such that a' == a.
        return t

    def declare_instance(self, t: TheoryDerivation) -> TheoryDerivation:
        t = super().add_formula(phi=t)
        return t

    def verify_element(self, phi: FlexibleFormula):
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        verify(assertion=is_declaratively_member_of_class(u=self.u, phi=phi, c=self.u.c2.theory_derivation),
            msg='phi is not an axiom-declaration')


class ClassDeclarationAccretor(UniverseOfDiscourseFormulaAccretor):
    """A collection of class-declarations that exposes some well-known classes.
    It is exposed as the c2 property on the UniverseOfDiscourse class.

    """

    def __init__(self, u: UniverseOfDiscourse):
        super().__init__(u=u)
        self._atheoretical_statement = None
        self._axiom_declaration = None
        self._axiom_inclusion = None
        self._class2 = None
        self._class_of_class_is_declared = False
        self._compound_formula = None
        self._connective = None
        self._constant_declaration = None
        self._definition_declaration = None
        self._definition_inclusion = None
        self._formula = None
        self._formula_statement = None
        self._free_variable = None
        self._inference_rule = None
        self._inferred_statement = None
        self._simple_object = None
        self._statement = None
        self._theory_derivation = None
        self._universe_of_discourse = None

    @property
    def atheoretical_statement(self) -> ClassDeclaration:
        """The atheoretical-statement class."""
        if self._atheoretical_statement is None:
            self._atheoretical_statement = self.declare(symbol='atheoretical-statement', auto_index=False,
                python_class=AtheoreticalStatement, is_class_of_class=False)
        return self._atheoretical_statement

    @property
    def axiom_declaration(self) -> ClassDeclaration:
        """The axiom-declaration class."""
        if self._axiom_declaration is None:
            self._axiom_declaration = self.declare(symbol='axiom-declaration', auto_index=False,
                python_class=AxiomDeclaration, is_class_of_class=False)
        return self._axiom_declaration

    @property
    def class2(self) -> ClassDeclaration:
        """The class class."""
        if self._class2 is None:
            self._class2 = self.declare(symbol='class', auto_index=False, python_class=ClassDeclaration,
                is_class_of_class=True)
        return self._class2

    @property
    def compound_formula(self) -> ClassDeclaration:
        """The compound-formula class."""
        if self._compound_formula is None:
            self._compound_formula = self.declare(symbol='compound-formula', auto_index=False,
                python_class=ClassDeclaration, is_class_of_class=False)
        return self._compound_formula

    @property
    def connective(self) -> ClassDeclaration:
        """The connective class."""
        if self._connective is None:
            self._connective = self.declare(symbol='connective', auto_index=False, python_class=Connective,
                is_class_of_class=False)
        return self._connective

    @property
    def constant_declaration(self) -> ClassDeclaration:
        """The constant-declaration class."""
        if self._constant_declaration is None:
            self._constant_declaration = self.declare(symbol='constant-declaration', auto_index=False,
                python_class=ConstantDeclaration, is_class_of_class=False)
        return self._constant_declaration

    def declare(self, symbol: (None, str, StyledText) = None, index: (None, int, str) = None,
        auto_index: (None, bool) = None, python_class: (None, type) = None, is_class_of_class: (None, bool) = None,
        echo: (None, bool) = None) -> ClassDeclaration:
        c: ClassDeclaration = ClassDeclaration(u=self.u, symbol=symbol, index=index, auto_index=auto_index,
            python_class=python_class, is_class_of_class=is_class_of_class, echo=echo)
        if not c.is_class_of_class:
            # There is a special case with the class of class.
            # In effect, we cannot call twice the declare_instance
            # method because we check that it is only declared once.
            c = self.declare_instance(c=c)  # Return the existing class if there is a class c' such that c' == c.
        return c

    def declare_instance(self, c: ClassDeclaration) -> ClassDeclaration:
        c = super().add_formula(phi=c)
        return c

    @property
    def definition_declaration(self) -> ClassDeclaration:
        """The definition-declaration class."""
        if self._definition_declaration is None:
            self._definition_declaration = self.declare(symbol='definition-declaration', auto_index=False,
                python_class=DefinitionDeclaration, is_class_of_class=False)
        return self._definition_declaration

    @property
    def formula(self) -> ClassDeclaration:
        """The formula class."""
        if self._formula is None:
            self._formula = self.declare(symbol='formula', auto_index=False, python_class=Formula,
                is_class_of_class=False)
        return self._formula

    @property
    def formula_statement(self) -> ClassDeclaration:
        """The formula-statement class."""
        if self._formula_statement is None:
            self._formula_statement = self.declare(symbol='formula-statement', auto_index=False, python_class=Formula,
                is_class_of_class=False)
        return self._formula_statement

    @property
    def free_variable(self) -> ClassDeclaration:
        """The free-variable class."""
        if self._free_variable is None:
            self._free_variable = self.declare(symbol='free-variable', auto_index=False, python_class=FreeVariable,
                is_class_of_class=False)
        return self._free_variable

    @property
    def inference_rule(self) -> ClassDeclaration:
        """The inference-rule class."""
        if self._inference_rule is None:
            self._inference_rule = self.declare(symbol='inference-rule', auto_index=False,
                python_class=InferenceRuleDeclaration, is_class_of_class=False)
        return self._inference_rule

    @property
    def inferred_statement(self) -> ClassDeclaration:
        """The inferred-statement class."""
        if self._inferred_statement is None:
            self._inferred_statement = self.declare(symbol='inferred-statement', auto_index=False,
                python_class=InferredStatement, is_class_of_class=False)
        return self._inferred_statement

    @property
    def simple_object(self) -> ClassDeclaration:
        """The simple-object class."""
        if self._simple_object is None:
            self._simple_object = self.declare(symbol='simple-object', auto_index=False, python_class=SimpleObjct,
                is_class_of_class=False)
        return self._simple_object

    @property
    def statement(self) -> ClassDeclaration:
        """The statement class."""
        if self._statement is None:
            self._statement = self.declare(symbol='statement', auto_index=False, python_class=Statement,
                is_class_of_class=False)
        return self._statement

    @property
    def theory_derivation(self) -> ClassDeclaration:
        """The theory-derivation class."""
        if self._theory_derivation is None:
            self._theory_derivation = self.declare(symbol='theory-derivation', auto_index=False,
                python_class=TheoryDerivation, is_class_of_class=False)
        return self._theory_derivation

    @property
    def universe_of_discourse(self) -> ClassDeclaration:
        """The universe-of-discourse class."""
        if self._universe_of_discourse is None:
            self._universe_of_discourse = self.declare(symbol='universe-of-discourse', auto_index=False,
                python_class=UniverseOfDiscourse, is_class_of_class=False)
        return self._universe_of_discourse

    def verify_element(self, phi: FlexibleFormula):
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        if phi.is_class_of_class:
            if not self._class_of_class_is_declared:
                # The class of class is a special case. In effect, it cannot verify
                # that it is of the class "class of class", because the "class of class"
                # is not yet contained in the u.c2 collection of classes.
                # Making this verification would lead to an infinite loop.
                # In consequence we relax the verification step for this special case,
                # but only for the initial creation of the class of class.
                self._class_of_class_is_declared = True
            else:
                raise Exception('The class-of-class is already declared.')
        else:
            verify(assertion=is_declaratively_member_of_class(u=self.u, phi=phi, c=self.u.c2.class2),
                msg='phi is not a class')


# class Tuple(tuple):
#  """Tuple subclasses the native tuple class.
#    The resulting supports setattr, getattr, hasattr,
#    which are convenient to create friendly programmatic shortcuts."""
#  pass


class ConnectiveAccretor(UniverseOfDiscourseFormulaAccretor):
    """A dictionary that exposes well-known connectives as properties.

    """

    def __init__(self, u: UniverseOfDiscourse):
        super().__init__(u=u)
        # Well-known objects
        self._addition = None
        self._biconditional = None
        self._conjunction = None
        self._disjunction = None
        self._equality = None
        self._formulates = None
        self._inconsistency = None
        self._inequality = None
        self._implication = None
        self._is_a = None
        self._map = None
        self._negation = None
        self._object_reference = None
        self._subtraction = None
        self._syntactic_entailment = None
        self._tupl = None

    @property
    def addition(self):
        """The well-known addition connective.

        Abridged property: u.r.plus

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._addition is None:
            self._addition = self.declare(arity=2, formula_rep=CompoundFormula.infix, signal_proposition=True,
                symbol=SerifItalic(plaintext='+', unicode='+', latex='+'), auto_index=False, dashed_name='addition',
                name='addition')
        return self._addition

    @property
    def biconditional(self):
        """The well-known biconditional connective.

        Abridged property: u.r.iif

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._biconditional is None:
            self._biconditional = self.declare(arity=2, formula_rep=CompoundFormula.infix, signal_proposition=True,
                symbol=SerifItalic(plaintext='<==>', unicode='⟺', latex='\\iff'), auto_index=False,
                dashed_name='biconditional', name='biconditional')
        return self._biconditional

    @property
    def conjunction(self):
        """The well-known conjunction connective.

        Abridged property: u.r.land

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._conjunction is None:
            self._conjunction = self.declare(arity=2, formula_rep=CompoundFormula.infix, signal_proposition=True,
                symbol=SerifItalic(plaintext='and', unicode='∧', latex='\\land'), auto_index=False, name='and',
                explicit_name='conjunction')
        return self._conjunction

    def declare(self, arity: (None, int) = None, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, formula_rep=None, signal_proposition=None, signal_theoretical_morphism=None,
        implementation=None, min_arity: (None, int) = None, max_arity: (None, int) = None,
        collection_start: (None, str, StyledText) = None, collection_separator: (None, str, StyledText) = None,
        collection_end: (None, str, StyledText) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):
        """Declare a new connective in this universe-of-discourse.
        """
        c: Connective = Connective(arity=arity, min_arity=min_arity, max_arity=max_arity, formula_rep=formula_rep,
            collection_start=collection_start, collection_separator=collection_separator, collection_end=collection_end,
            signal_proposition=signal_proposition, signal_theoretical_morphism=signal_theoretical_morphism,
            implementation=implementation, u=self.u, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle, echo=echo)
        c = self.declare_instance(c=c)  # Return the existing axiom if there is an axiom a' such that a' == a.
        return c

    def declare_instance(self, c: Connective) -> Connective:
        c = super().add_formula(phi=c)
        return c

    @property
    def disjunction(self):
        """The well-known disjunction connective.

        Abridged property: u.r.lor

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._disjunction is None:
            self._disjunction = self.declare(arity=2, formula_rep=CompoundFormula.infix, signal_proposition=True,
                auto_index=False, symbol=SerifItalic(unicode='∨', latex='\\lor', plaintext='or'), name='or',
                explicit_name='disjunction')
        return self._disjunction

    @property
    def eq(self):
        """The well-known equality connective.

        Unabridged property: universe_of_discourse.connectives.equality

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.equality

    @property
    def equal(self):
        """The well-known equality connective.

        Unabridged property: universe_of_discourse.connectives.equality

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.equality

    @property
    def equality(self):
        """The well-known equality connective.

        Abridged property: u.r.equal

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._equality is None:
            self._equality = self.declare(arity=2, formula_rep=CompoundFormula.infix, signal_proposition=True,
                symbol='=', auto_index=False, dashed_name='equality')
        return self._equality

    @property
    def formulates(self):
        """a meta-theory connective stating that an hypothesis theory-derivation H formulates an hypothesis propositional formula P, and only P.

        H formulate P
        where:
        H is an hypothesis theory-derivation,
        P is the formulated hypothesis of H

        H formulate P is True if and only if P is the (only) formulated hypothesis of H
        """
        if self._formulates is None:
            self._formulates = self.declare(arity=2, formula_rep=CompoundFormula.infix, signal_proposition=True,
                symbol=SerifItalic(plaintext='formulate', unicode='formulate', latex='\\operatorname{formulate}'),
                auto_index=False, dashed_name='formulate', name='formulate')
        return self._formulates

    @property
    def inc(self):
        """The well-known (theory-)inconsistent connective.

        Unabridged property: u.r.inconsistent

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.inconsistency

    @property
    def iff(self):
        return self.biconditional

    @property
    def implication(self):
        """The well-known implication connective.

        Abridged property: u.r.implies

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._implication is None:
            self._implication = self.declare(arity=2, formula_rep=CompoundFormula.infix, signal_proposition=True,
                symbol=SerifItalic(plaintext='implies', unicode='⊃', latex=r'\supset'), auto_index=False,
                name='implication', explicit_name='logical implication')
        return self._implication

    @property
    def implies(self):
        """The well-known implication connective.

        Unabridged property: u.r.implication

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.implication

    @property
    def inconsistency(self):
        """The well-known (theory-)inconsistent connective.

        By convention:
        - inc(T) means that theory-derivation T is inconsistent.

        Abridged property: u.r.inc

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._inconsistency is None:
            self._inconsistency = self.declare(arity=1, formula_rep=CompoundFormula.function_call,
                signal_proposition=True, symbol='Inc', auto_index=False, acronym='inc.', name='inconsistent')
        return self._inconsistency

    @property
    def inequality(self):
        """The well-known inequality connective.

        Abridged property: u.r.neq

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._inequality is None:
            self._inequality = self.declare(arity=2, formula_rep=CompoundFormula.infix, signal_proposition=True,
                symbol=SerifItalic(plaintext='neq', unicode='≠', latex='\\neq'), auto_index=False, acronym='neq',
                name='not equal')
        return self._inequality

    @property
    def is_a(self):
        if self._is_a is None:
            self._is_a = self.declare(arity=2, formula_rep=CompoundFormula.infix, signal_proposition=True,
                symbol=SerifItalic(plaintext='is-a', unicode='is-a', latex='is-a'), auto_index=False, acronym=None,
                name='is a')
        return self._is_a

    @property
    def land(self):
        """The well-known conjunction connective.

        Unabridged property: u.r.conjunction

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.conjunction

    @property
    def lnot(self):
        """The well-known negation connective.

        Abridged property: u.r.negation

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.negation

    @property
    def lor(self):
        """The well-known disjunction connective.

        Unabridged property: u.r.disjunction

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.disjunction

    @property
    def map(self):
        """The well-known map connective.

        Abridged property: u.r.map

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._map is None:
            self._map = self.declare(arity=1, formula_rep=CompoundFormula.prefix, signal_proposition=True,
                symbol=SerifItalic(plaintext='-->', unicode='\u2192', latex='\\rightarrow'), auto_index=False,
                name='map')
        return self._map

    @property
    def negation(self):
        """The well-known negation connective.

        Abridged property: u.r.lnot

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._negation is None:
            self._negation = self.declare(arity=1, formula_rep=CompoundFormula.prefix, signal_proposition=True,
                symbol=SerifItalic(plaintext='not', unicode='¬', latex='\\neg'), auto_index=False, abridged_name='not',
                name='negation')
        return self._negation

    @property
    def neq(self):
        """The well-known inequality connective.

        Unabridged property: u.r.inequality

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.inequality

    @property
    def minus(self):
        return self.subtraction

    @property
    def object_reference(self):
        """A unary connective to reference variables as objects in formulas, without using them.

    Default composition:
     ⌜x⌝
    Where x is a variable.

    Example:
      ⌜x⌝ is-a natural-number
      x > 4
    """
        if self._object_reference is None:
            self._object_reference = self.declare(formula_rep=CompoundFormula.collection,
                collection_start=text_dict.open_quasi_quote, collection_separator=text_dict.comma,
                collection_end=text_dict.close_quasi_quote, signal_proposition=True, symbol='object-reference',
                auto_index=False, dashed_name='object-reference', name='object reference',
                explicit_name='object reference')
        return self._object_reference

    @property
    def plus(self):
        return self.addition

    @property
    def proves(self):
        """The well-known syntactic-entailment connective.

        Unabridged property: u.r.syntactic_entailment

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.syntactic_entailment

    @property
    def subtraction(self):
        """The well-known subtraction connective.

        Abridged property: u.r.minus

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._subtraction is None:
            self._subtraction = self.declare(arity=2, formula_rep=CompoundFormula.infix, signal_proposition=True,
                symbol=SerifItalic(plaintext='-', unicode='-', latex='-'), auto_index=False, dashed_name='subtraction',
                name='subtraction')
        return self._subtraction

    @property
    def tupl(self):
        """Expresses an ordered sequence of theoretical objects defined by extension.
        Notation is comma separator.
        Name tupl to avoid a name conflict with python tuple class.
        """
        global text_dict
        if self._tupl is None:
            self._tupl = self.declare(formula_rep=CompoundFormula.collection, collection_start=text_dict.empty_string,
                collection_separator=text_dict.comma, collection_end=text_dict.empty_string, signal_proposition=True,
                symbol='tuple', auto_index=False, dashed_name='tuple', name='tuple', explicit_name='tuple')
        return self._tupl

    @property
    def syntactic_entailment(self):
        """The well-known syntactic-entailment connective.

        Abridged property: u.r.proves

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._syntactic_entailment is None:
            self._syntactic_entailment = self.declare(arity=2, formula_rep=CompoundFormula.infix,
                signal_proposition=True, symbol=SerifItalic(plaintext='|-', unicode='⊢', latex='\\vdash'),
                auto_index=False, dashed_name='syntactic-entailment', abridged_name='proves',
                name='syntactic entailment')
        return self._syntactic_entailment

    @property
    def unequal(self):
        """The well-known inequality connective.

        Unabridged property: u.r.inequality

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.inequality

    def verify_element(self, phi: FlexibleFormula):
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        verify(assertion=is_declaratively_member_of_class(u=self.u, phi=phi, c=self.u.c2.connective),
            msg='phi is not a connective')


class ConstantDeclarationDict(collections.UserDict):
    """A dictionary that exposes well-known constants as properties.
    It is exposed as the c property on the UniverseOfDiscourse class.

    """

    def __init__(self, u: UniverseOfDiscourse):
        self.u = u
        super().__init__()

    def declare(self, value: FlexibleFormula, symbol: (None, str, StyledText) = None, index: (None, int, str) = None,
        auto_index: (None, bool) = None, echo: (None, bool) = None) -> ConstantDeclaration:
        return ConstantDeclaration(u=self.u, value=value, symbol=symbol, index=index, auto_index=auto_index, echo=echo)


FlexibleAxiom = typing.Union[AxiomDeclaration, AxiomInclusion, str]
"""A flexible composite data type to pass axioms as arguments.

"""

FlexibleDefinition = typing.Union[DefinitionDeclaration, DefinitionInclusion, str]
"""A flexible composite data type to pass definitions as arguments.

"""

FlexibleFormula = typing.Union[Formula, FormulaStatement, CompoundFormula, tuple, list]
"""See validate_flexible_statement_formula() for details."""

FlexibleSymbol = typing.Union[str, SymbolicObject, StyledText]


def verify_axiom_declaration(u: UniverseOfDiscourse, input_value: FlexibleAxiom, arg: (None, str) = None,
    raise_exception: bool = True, error_code: (None, ErrorCode) = None) -> tuple[
    bool, (None, AxiomDeclaration), (None, str)]:
    ok: bool = True
    axiom_declaration: (None, AxiomDeclaration) = None
    msg: (None, str)

    if isinstance(input_value, AxiomDeclaration):
        axiom_declaration = input_value
    elif isinstance(input_value, AxiomInclusion):
        # Unpack the axiom-declaration from the axiom-inclusion.
        input_value: AxiomInclusion
        axiom_declaration: AxiomDeclaration = input_value.a
    elif isinstance(input_value, str):
        # Assume the string is the axiom expressed in natural language.
        # TODO: Find the matching axiom from u.
        raise NotImplementedError('Feature not implemented yet, sorry')
    else:
        ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=False,
            msg=f'The axiom {"" if arg is None else "passed as argument " + "".join(["⌜", arg, "⌝ "])}is not of a supported pythonic type.',
            input_value=input_value, input_value_type=type(input_value), u=u)
        if not ok:
            return ok, None, msg

    ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=axiom_declaration is not None,
        msg=f'The axiom {"" if arg is None else "passed as argument " + "".join(["⌜", arg, "⌝ "])}is None.',
        axiom_declaration=axiom_declaration, axiom_declaration_u=axiom_declaration.u, u=u)
    if not ok:
        return ok, None, msg

    ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=axiom_declaration.u is u,
        msg=f'The universe-of-discourse ⌜{axiom_declaration.u}⌝ passed as argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}is distinct from the universe-of-discourse ⌜{u}⌝.',
        axiom_declaration=axiom_declaration, axiom_declaration_u=axiom_declaration.u, u=u)
    if not ok:
        return ok, None, msg

    return ok, axiom_declaration, msg


def verify_axiom_inclusion(t: TheoryDerivation, input_value: FlexibleAxiom, arg: (None, str) = None,
    raise_exception: bool = True, error_code: (None, ErrorCode) = None) -> tuple[
    bool, (None, AxiomInclusion), (None, str)]:
    ok: bool = True
    axiom_inclusion: (None, AxiomInclusion) = None
    msg: (None, str)
    if isinstance(input_value, AxiomInclusion):
        axiom_inclusion = input_value
    elif isinstance(input_value, AxiomDeclaration):
        # TODO: Find if there is an inclusion for that axiom in t.
        raise NotImplementedError(
            'This is an axiom-declaration, not an axiom-inclusion. Punctilious enhancement to be considered for future development: automatically check if an axiom-inclusion is present in the current theory-derivation for that axiom-declaration.')
    elif isinstance(input_value, str):
        # Assume the string is the axiom expressed in natural language.
        # TODO: Find the matching axiom from u.
        raise NotImplementedError('Feature not implemented yet, sorry')
    else:
        ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=False,
            msg=f'The axiom {"" if arg is None else "passed as argument " + "".join(["⌜", arg, "⌝ "])}is not of pythonic type FlexibleAxiom.',
            input_value=input_value, input_value_type=type(input_value))
        if not ok:
            return ok, None, msg
    return ok, axiom_inclusion, None


def verify_definition_declaration(u: UniverseOfDiscourse, input_value: FlexibleDefinition, arg: (None, str) = None,
    raise_exception: bool = True, error_code: (None, ErrorCode) = None) -> tuple[
    bool, (None, DefinitionDeclaration), (None, str)]:
    ok: bool = True
    definition_declaration: (None, DefinitionDeclaration) = None
    msg: (None, str)

    if isinstance(input_value, DefinitionDeclaration):
        definition_declaration = input_value
    elif isinstance(input_value, DefinitionInclusion):
        # Unpack the definition-declaration from the definition-inclusion.
        input_value: DefinitionInclusion
        definition_declaration: DefinitionDeclaration = input_value.d
    elif isinstance(input_value, str):
        # Assume the string is the definition expressed in natural language.
        # TODO: Find the matching definition from u.
        raise NotImplementedError('Feature not implemented yet, sorry')
    else:
        ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=False,
            msg=f'The definition {"" if arg is None else "passed as argument " + "".join(["⌜", arg, "⌝ "])}is not of a supported pythonic type.',
            input_value=input_value, input_value_type=type(input_value), u=u)
        if not ok:
            return ok, None, msg

    ok, msg = verify(raise_exception=raise_exception, error_code=error_code,
        assertion=definition_declaration is not None,
        msg=f'The definition {"" if arg is None else "passed as argument " + "".join(["⌜", arg, "⌝ "])}is None.',
        definition_declaration=definition_declaration, definition_declaration_u=definition_declaration.u, u=u)
    if not ok:
        return ok, None, msg

    ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=definition_declaration.u is u,
        msg=f'The universe-of-discourse ⌜{definition_declaration.u}⌝ passed as argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}is distinct from the universe-of-discourse ⌜{u}⌝.',
        definition_declaration=definition_declaration, definition_declaration_u=definition_declaration.u, u=u)
    if not ok:
        return ok, None, msg

    return ok, definition_declaration, msg


def verify_definition_inclusion(t: TheoryDerivation, input_value: FlexibleDefinition, arg: (None, str) = None,
    raise_exception: bool = True, error_code: (None, ErrorCode) = None) -> tuple[
    bool, (None, DefinitionInclusion), (None, str)]:
    ok: bool = True
    definition_inclusion: (None, DefinitionInclusion) = None
    msg: (None, str)
    if isinstance(input_value, DefinitionInclusion):
        definition_inclusion = input_value
    elif isinstance(input_value, DefinitionDeclaration):
        # TODO: Find if there is an inclusion for that definition in t.
        raise NotImplementedError('Feature not implemented yet, sorry')
    elif isinstance(input_value, str):
        # Assume the string is the definition expressed in natural language.
        # TODO: Find the matching definition from u.
        raise NotImplementedError('Feature not implemented yet, sorry')
    else:
        ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=False,
            msg=f'The definition {"" if arg is None else "passed as argument " + "".join(["⌜", arg, "⌝ "])}is not of pythonic type FlexibleDefinition.',
            input_value=input_value, input_value_type=type(input_value))
        if not ok:
            return ok, None, msg
    return ok, definition_inclusion, None


def verify_class(u: UniverseOfDiscourse, c: FlexibleFormula, arg: (None, str) = None, raise_exception: bool = True,
    error_code: (None, ErrorCode) = None) -> tuple[bool, (None, ClassDeclaration), (None, str)]:
    ok: bool
    formula: (None, Formula) = None
    msg: (None, str) = None
    if isinstance(c, ClassDeclaration):
        # the input is of python type ClassDeclaration.
        ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=c.u is u,
            msg=f'The universe-of-discourse ⌜{u}⌝ is distinct from the universe-of-discourse ⌜{c.u}⌝ '
                f' of the class ⌜{c}⌝.', c=c, u=u)
        return ok, c, msg
    else:
        verify(raise_exception=raise_exception, error_code=error_code, assertion=False,
            msg=f'The argument ⌜{arg}⌝ is not of python class ClassDeclaration.', c=c, u=u)
        return False, None, msg


def verify_symbol(input_value: FlexibleSymbol, arg: (None, str) = None, raise_exception: bool = True,
    error_code: (None, ErrorCode) = None) -> tuple[bool, (None, NameSet), (None, str)]:
    ok: bool
    msg: (None, str)
    if isinstance(input_value, str):
        input_value = NameSet(symbol=SerifItalic(input_value))
    elif isinstance(input_value, SymbolicObject):
        input_value = input_value.nameset
    elif isinstance(input_value, StyledText):
        input_value = NameSet(symbol=input_value)
    ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=isinstance(input_value, NameSet),
        msg=f'⌜{input_value}⌝ of pythonic type ⌜{type(input_value).__name__}⌝'
            f'{"" if arg is None else "".join([" passed as argument ⌜", arg, "⌝"])}'
            f' could not be coerced to a NameSet instance.', argument=input_value)
    return ok, input_value, msg


def verify_symbolic_object(u: UniverseOfDiscourse, input_value: SymbolicObject, arg: (None, str) = None,
    raise_exception: bool = True, error_code: (None, ErrorCode) = None) -> tuple[
    bool, (None, SymbolicObject), (None, str)]:
    ok: bool
    msg: (None, str)
    ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=input_value.u is u,
        msg=f'The universe-of-discourse ⌜{input_value.u}⌝ of the symbolic-object ⌜{input_value.u}⌝{"" if arg is None else "".join([" passed as argument ⌜", arg, "⌝"])} is not the expected universe-of-discourse python instance ⌜{u}⌝.',
        argument=input_value, u=u)
    return ok, input_value, msg


def verify_formula(u: UniverseOfDiscourse, input_value: FlexibleFormula, arg: (None, str) = None,
    form: (None, FlexibleFormula) = None, mask: (None, frozenset[FreeVariable]) = None,
    is_strictly_propositional: (None, bool) = None, raise_exception: bool = True, error_code: (None, ErrorCode) = None,
    unpack_statement: bool = True) -> tuple[bool, (None, Formula), (None, str)]:
    """Many punctilious_obsolete_20240114 pythonic methods or functions expect some formula as input terms. This function assures that the input value is a proper formula and that it is consistent with possible contraints imposed on that formula.

    If ⌜input_value⌝ is of type formula, it is already well typed.

    If ⌜argument⌝ is of type iterable, such as tuple, e.g.: (implies, q, p), we assume it is a formula in the form (connective, a1, a2, ... an) where ai are arguments.

    Note that this is complementary with the pseudo-infix notation, which uses the __or__ method and | operator to transform: p |r| q to (r, p, q).

    :param u:
    :param input_value:
    :param arg:
    :param form:
    :param mask:
    :param is_strictly_propositional:
    :param raise_exception:
    :param error_code:
    :param unpack_statement: if input_value is a statement, return its internal formula instead of the statement
    object itself. Default: True.
    :return:
    """
    ok: bool
    formula: (None, Formula) = None
    msg: (None, str) = None
    if isinstance(input_value, CompoundFormula):
        # the input is already correctly typed as a Formula.
        formula = input_value
    elif isinstance(input_value, FormulaStatement):
        # the input is typed as a FormulaStatement,
        # we must unpack it to retrieve its internal Formula.
        if unpack_statement:
            formula = input_value.valid_proposition
        else:
            formula = input_value
    elif isinstance(input_value, ConstantDeclaration):
        # the input is typed as a ConstantDeclaration,
        # we must unpack it to retrieve its internal Formula.
        formula = input_value.value
    elif isinstance(input_value, tuple):
        # the input is a tuple,
        # assuming a data structure of the form:
        # (connective, argument_1, argument_2, ..., argument_n)
        # where the connective and/or the arguments may be variables.
        formula = u.declare_compound_formula(input_value[0], *input_value[1:])
    elif isinstance(input_value, Formula):
        # the input is typed as an individual formula.
        # this is a meta-theory formula, i.e. it is a formula
        # whose object is a formula.
        formula = input_value
    else:
        # the input argument could not be interpreted as a formula
        value_string: str
        try:
            value_string = str(input_value)
        except:
            value_string = 'string conversion failure'
        ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=False,
            msg=f'The argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}could not be interpreted as a Formula. Its type was {str(type(input_value))}, and its value was ⌜{value_string}⌝.',
            argument=input_value, u=u)
        if not ok:
            return ok, None, msg
    if form is not None:
        ok, form, msg = verify_formula(u=u, input_value=form,
            raise_exception=True)  # The form itself may be a flexible formula.
        if not ok:
            verify(raise_exception=raise_exception, error_code=error_code, assertion=False,
                msg=f'The form ⌜{form}⌝ passed to verify the structure of formula ⌜{formula}⌝ is not a proper formula.',
                argument=input_value, u=u, form=form, mask=mask)
        form: CompoundFormula
        is_of_form: bool = form.is_masked_formula_similar_to(phi=formula, mask=mask)
        if not is_of_form:
            # a certain form is required for the formula,
            # and the form of the formula does not match that required form.
            variables_string: str
            if mask is None:
                variables_string = ''
            elif len(mask) == 1:
                variables_string = ', where ' + ', '.join(
                    [variable.rep(encoding=encodings.plaintext) for variable in mask]) + ' is a variable'
            else:
                variables_string = ', where ' + ', '.join(
                    [variable.rep(encoding=encodings.plaintext) for variable in mask]) + ' are variables'
            ok, msg = verify(raise_exception=raise_exception, error_code=error_code, assertion=False,
                msg=f'The formula ⌜{formula}⌝ passed as argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}is not of the required form ⌜{form}⌝{variables_string}.',
                argument=input_value, u=u, form=form, mask=mask)
            if not ok:
                return ok, None, msg

    verify(
        assertion=is_strictly_propositional is None or is_strictly_propositional == formula.is_strictly_propositional,
        msg=f'The formula ⌜{formula}⌝ passed as argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}is {"" if formula.is_strictly_propositional else "not "}strictly-propositional.',
        raise_exception=raise_exception, error_code=error_code)

    return True, formula, None


def verify_formula_statement(t: TheoryDerivation, input_value: FlexibleFormula, arg: (None, str) = None,
    form: (None, FlexibleFormula) = None, mask: (None, frozenset[FreeVariable]) = None,
    is_strictly_propositional: (None, bool) = None, raise_exception: bool = True,
    error_code: (None, ErrorCode) = None) -> tuple[bool, (None, FormulaStatement), (None, str)]:
    """Many punctilious_obsolete_20240114 pythonic methods expect some FormulaStatement as input terms (e.g. the infer_statement() of inference-rules). This is syntactically robust, but it may read theory code less readable. In effect, one must store all formula-statements in variables to reuse them in formula. If the number of formula-statements get large, readability suffers. To provide a friendler interface for humans, we allow passing formula-statements as formula, tuple, and lists and apply the following interpretation rules:

    If ⌜argument⌝ is of type iterable, such as tuple, e.g.: (implies, q, p), we assume it is a formula in the form (connective, a1, a2, ... an) where ai are arguments.

    Note that this is complementary with the pseudo-infix notation, which transforms: p |implies| q into a formula.

    :param t:
    :param arity:
    :param input_value:
    :return:
    """

    formula_ok: bool
    msg: (None, str)
    formula_statement: (None, FormulaStatement) = None
    formula: (None, CompoundFormula) = None
    u: UniverseOfDiscourse = t.u

    if isinstance(input_value, FormulaStatement):
        formula_statement: FormulaStatement = input_value
    else:
        # ⌜argument⌝ is not a statement-formula.
        # But it is expected to be interpretable first as a formula, and then as a formula-statement.
        formula_ok, formula, msg = verify_formula(arg=arg, u=u, input_value=input_value, form=None, mask=None,
            raise_exception=raise_exception, error_code=error_code)
        if not formula_ok:
            return formula_ok, None, msg
        formula: CompoundFormula
        # We only received a formula, not a formula-statement.
        # Since we require a formula-statement,
        # we attempt to automatically retrieve the first occurrence
        # of a formula-statement in ⌜t⌝ that is
        # syntactically-equivalent to ⌜argument⌝.
        formula_statement: FormulaStatement = t.get_first_syntactically_equivalent_statement(formula=input_value)
        formula_ok, msg = verify(raise_exception=raise_exception, error_code=error_code,
            assertion=formula_statement is not None,
            msg=f'The formula ⌜{formula}⌝ passed as argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}is not a formula-statement in theory-derivation ⌜{t}⌝.',
            formula=formula, t=t)
        if not formula_ok:
            return formula_ok, None, msg

    # At this point we have a properly typed FormulaStatement.

    # Special case to support class membership for metatheory.
    # The formula (x is-a c) where x is a formula and c is a class is a special case.
    # In effect, by axiom a1 of the minimal metatheory, (x is-a c) is
    # valid if x was declared as a member of c.
    # We treat this as a special case in such a way as to NOT make it
    # necessary to populate all (x is-a c) statements in the metatheory.
    if isinstance(formula, CompoundFormula) and formula.connective is u.c1.is_a and formula.arity == 2:
        formula: CompoundFormula
        # This is a formula of the form (x is-a c).
        # We must check now that c is a class.
        c: Formula = formula.terms[1]
        _, c, _ = verify_class(u=u, c=c, arg='c')
        c: ClassDeclaration
        if isinstance(c, ClassDeclaration):
            c: ClassDeclaration
            if is_declaratively_member_of_class(u=u, phi=formula.terms[0], c=c):
                return True, formula, None

    formula_ok, msg = verify(raise_exception=raise_exception, error_code=error_code,
        assertion=t.contains_statement_in_theory_chain(phi=formula_statement),
        msg=f'The formula-statement {formula_statement} passed as argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}is not contained in the theory-derivation ⌜{t}⌝.',
        formula=formula, t=t)

    if not formula_ok:
        return formula_ok, None, msg

    # Validate the form, etc. of the underlying formula.
    formula: CompoundFormula = formula_statement.valid_proposition
    formula_ok, formula, msg = verify_formula(u=u, input_value=formula, arg=arg, form=form, mask=mask,
        raise_exception=raise_exception, error_code=error_code)
    if not formula_ok:
        return formula_ok, None, msg

    return True, formula_statement, msg


def verify_hypothesis(t: TheoryDerivation, input_value: FlexibleFormula, arg: (None, str) = None,
    hypothesis_form: (None, FlexibleFormula) = None, hypothesis_mask: (None, frozenset[FreeVariable]) = None,
    is_strictly_propositional: (None, bool) = None, raise_exception: bool = True,
    error_code: (None, ErrorCode) = None) -> tuple[bool, (None, Hypothesis), (None, str)]:
    formula_ok: bool
    msg: (None, str) = None
    u: UniverseOfDiscourse = t.u
    verify(raise_exception=raise_exception, error_code=error_code,
        assertion=input_value is not None and isinstance(input_value, Hypothesis),
        msg=f'The formula ⌜{arg}⌝⌜({input_value}) is not an hypothesis.', arg=arg, input_value=input_value, t=t, u=u)
    hypothesis: Hypothesis = input_value
    verify(raise_exception=raise_exception, error_code=error_code,
        assertion=t.contains_statement_in_theory_chain(phi=hypothesis),
        msg=f'The hypothesis ⌜{arg}⌝⌜({hypothesis}) is not contained in theory-derivation ⌜t⌝({t}).', arg=arg,
        hypothesis=hypothesis, t=t, u=u)
    verify(raise_exception=raise_exception, error_code=error_code,
        assertion=hypothesis.hypothesis_child_theory.extended_theory is t,
        msg=f'The hypothesis ⌜{arg}⌝⌜({hypothesis}) does not extend theory-derivation ⌜t⌝({t}).', arg=arg,
        hypothesis=hypothesis, t=t, u=u)
    verify_formula(u=u, input_value=hypothesis.hypothesis_formula, arg='{arg}.hypothesis_formula', form=hypothesis_form,
        mask=hypothesis_mask, is_strictly_propositional=is_strictly_propositional, raise_exception=raise_exception,
        error_code=error_code)
    return True, hypothesis, msg


def complement_error(context: (None, ErrorCode, frozenset[ErrorCode]),
    complement: (None, ErrorCode, frozenset[ErrorCode])):
    """Enrich some error-codes with complementary error-codes to provide more accurate context for the troubleshooting of python exceptions and warnings."""
    context: frozenset = frozenset() if context is None else context if isinstance(context, frozenset) else frozenset(
        context)
    complement: frozenset = frozenset() if complement is None else complement if isinstance(complement,
        frozenset) else frozenset(context)
    output: frozenset = context.union(complement)
    return output


def verify_universe_of_discourse(u: (None, FlexibleFormula), arg: str = 'u', raise_exception: bool = True,
    error_code: (None, ErrorCode, frozenset[ErrorCode]) = None) -> tuple[
    bool, (None, DefinitionInclusion), (None, str)]:
    """A data-validation function that verifies the adequacy of a universe-of-discourse mandatory term."""
    ok: bool = True
    msg: (None, str)
    error_code: frozenset[ErrorCode] = complement_error(context=error_code,
        complement=error_codes.error_004_inadequate_universe_parameter)
    ok, msg = verify(assertion=is_declaratively_member_of_class_universe_of_discourse(u=u),
        raise_exception=raise_exception, error_code=error_code,
        msg=f'Argument {arg}=⌜{repr(u)}⌝ of type {repr(type(u))} could not be resolved to a universe-of-discourse of '
            f'python type UniverseOfDiscourse.', input_value=u, input_value_type=type(u))
    if ok:
        u: UniverseOfDiscourse = u
        return True, u, None
    else:
        return False, None, msg


def verify_theory_derivation(input_value: (None, FlexibleFormula), arg: str, raise_exception: bool = True,
    error_code: (None, ErrorCode, frozenset[ErrorCode]) = None) -> tuple[
    bool, (None, DefinitionInclusion), (None, str)]:
    """A data-validation function that verifies the adequacy of a theory-derivation mandatory term."""
    ok: bool = True
    msg: (None, str)
    error_code: frozenset[ErrorCode] = complement_error(context=error_code,
        complement=error_codes.error_005_inadequate_theory_parameter)
    ok, msg = verify(assertion=input_value is not None and isinstance(input_value, TheoryDerivation),
        raise_exception=raise_exception, error_code=error_code,
        msg=f'Python variable {arg}=⌜{repr(input_value)}⌝ of type {repr(type(input_value))} could not be resolved to an instance of TheoryElaborationSequence.',
        input_value=input_value, input_value_type=type(input_value))
    if ok:
        t: TheoryDerivation = input_value
        return True, t, None
    else:
        return False, None, msg


class InferenceRuleDeclarationAccretor(UniverseOfDiscourseFormulaAccretor):
    """This python class models the collection of :ref:`inference-rules<inference_rule_math_concept>` :ref:`declared<object_declaration_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>`.

    In complement, it conveniently exposes as python properties a catalog of natively supported :ref:`inference-rules<inference_rule_math_concept>` that are automatically :ref:`declared<object_declaration_math_concept>` in the :ref:`universe-of-discourse<universe_of_discourse_math_concept>` when they are accessed for the first time.
    """

    def __init__(self, u: UniverseOfDiscourse):
        super().__init__(u=u)
        # Well-known objects
        self._absorption = None
        self._axiom_interpretation = None
        self._biconditional_elimination_1 = None
        self._biconditional_elimination_2 = None
        self._biconditional_introduction = None
        self._conjunction_elimination_1 = None
        self._conjunction_elimination_2 = None
        self._conjunction_introduction = None
        self._constructive_dilemma = None
        self._definition_interpretation = None
        self._destructive_dilemma = None
        self._disjunction_elimination = None
        self._disjunction_introduction_1 = None
        self._disjunction_introduction_2 = None
        self._disjunctive_resolution = None
        self._disjunctive_syllogism_1 = None
        self._disjunctive_syllogism_2 = None
        self._double_negation_elimination = None
        self._double_negation_introduction = None
        self._equality_commutativity = None
        self._equal_terms_substitution = None
        self._hypothetical_syllogism = None
        self._inconsistency_introduction_1 = None
        self._inconsistency_introduction_2 = None
        self._inconsistency_introduction_3 = None
        self._modus_ponens = None
        self._modus_tollens = None
        self._proof_by_contradiction_1 = None
        self._proof_by_contradiction_2 = None
        self._proof_by_refutation_1 = None
        self._proof_by_refutation_2 = None
        self._variable_substitution = None

    @property
    def absorb(self) -> AbsorptionDeclaration:
        return self.absorption

    @property
    def absorption(self) -> AbsorptionDeclaration:
        if self._absorption is None:
            i: AbsorptionDeclaration = AbsorptionDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._absorption = i
        return self._absorption

    @property
    def axiom_interpretation(self) -> AxiomInterpretationDeclaration:
        if self._axiom_interpretation is None:
            i: AxiomInterpretationDeclaration = AxiomInterpretationDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._axiom_interpretation = i
        return self._axiom_interpretation

    @property
    def bel(self) -> BiconditionalElimination1Declaration:
        return self.biconditional_elimination_1

    @property
    def ber(self) -> BiconditionalElimination2Declaration:
        return self.biconditional_elimination_2

    @property
    def bi(self) -> BiconditionalIntroductionDeclaration:
        return self.biconditional_introduction

    @property
    def biconditional_elimination_1(self) -> BiconditionalElimination1Declaration:
        if self._biconditional_elimination_1 is None:
            i: BiconditionalElimination1Declaration = BiconditionalElimination1Declaration(u=self.u)
            self.declare_instance(i=i)
            self._biconditional_elimination_1 = i
        return self._biconditional_elimination_1

    @property
    def biconditional_elimination_2(self) -> BiconditionalElimination2Declaration:
        if self._biconditional_elimination_2 is None:
            i: BiconditionalElimination2Declaration = BiconditionalElimination2Declaration(u=self.u)
            self.declare_instance(i=i)
            self._biconditional_elimination_2 = i
        return self._biconditional_elimination_2

    @property
    def biconditional_introduction(self) -> BiconditionalIntroductionDeclaration:
        if self._biconditional_introduction is None:
            i: BiconditionalIntroductionDeclaration = BiconditionalIntroductionDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._biconditional_introduction = i
        return self._biconditional_introduction

    @property
    def cd(self) -> ConstructiveDilemmaDeclaration:
        return self.constructive_dilemma

    @property
    def cel(self) -> ConjunctionElimination1Declaration:
        return self.conjunction_elimination_1

    @property
    def cer(self) -> ConjunctionElimination2Declaration:
        return self.conjunction_elimination_2

    @property
    def ci(self) -> ConjunctionIntroductionDeclaration:
        return self.conjunction_introduction

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='inference-rule')

    @property
    def conjunction_elimination_1(self) -> ConjunctionElimination1Declaration:
        # TODO: inference-rule: conjunction_elimination_1: Migrate to specialized classes

        if self._conjunction_elimination_1 is None:
            i: ConjunctionElimination1Declaration = (ConjunctionElimination1Declaration(u=self.u))
            self.declare_instance(i=i)
            self._conjunction_elimination_1 = i
        return self._conjunction_elimination_1

    @property
    def conjunction_elimination_2(self) -> ConjunctionElimination2Declaration:
        if self._conjunction_elimination_2 is None:
            i: ConjunctionElimination2Declaration = ConjunctionElimination2Declaration(u=self.u)
            self.declare_instance(i=i)
            self._conjunction_elimination_2 = i
        return self._conjunction_elimination_2

    @property
    def conjunction_introduction(self) -> ConjunctionIntroductionDeclaration:
        if self._conjunction_introduction is None:
            i: ConjunctionIntroductionDeclaration = ConjunctionIntroductionDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._conjunction_introduction = i
        return self._conjunction_introduction

    @property
    def constructive_dilemma(self) -> ConstructiveDilemmaDeclaration:
        if self._constructive_dilemma is None:
            i: ConstructiveDilemmaDeclaration = ConstructiveDilemmaDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._constructive_dilemma = i
        return self._constructive_dilemma

    def declare(self) -> InferenceRuleDeclaration:
        # Return the existing inference-rule if there is an inference-rule i' such that i' == i.
        raise Exception('Not implemented yet, sorry.')

    def declare_instance(self, i: InferenceRuleDeclaration) -> InferenceRuleDeclaration:
        i = super().add_formula(phi=i)
        return i

    @property
    def definition_interpretation(self) -> DefinitionInterpretationDeclaration:
        if self._definition_interpretation is None:
            i: DefinitionInterpretationDeclaration = DefinitionInterpretationDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._definition_interpretation = i
        return self._definition_interpretation

    @property
    def destructive_dilemma(self) -> DestructiveDilemmaDeclaration:
        if self._destructive_dilemma is None:
            i: DestructiveDilemmaDeclaration = DestructiveDilemmaDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._destructive_dilemma = i
        return self._destructive_dilemma

    @property
    def dil(self) -> DisjunctionIntroduction1Declaration:
        return self.disjunction_introduction_1

    @property
    def dir(self) -> DisjunctionIntroduction2Declaration:
        return self.disjunction_introduction_2

    @property
    def disjunction_introduction_1(self) -> DisjunctionIntroduction1Declaration:
        if self._disjunction_introduction_1 is None:
            i: DisjunctionIntroduction1Declaration = DisjunctionIntroduction1Declaration(u=self.u)
            self.declare_instance(i=i)
            self._disjunction_introduction_1 = i
        return self._disjunction_introduction_1

    @property
    def disjunction_introduction_2(self) -> DisjunctionIntroduction2Declaration:
        if self._disjunction_introduction_2 is None:
            i: DisjunctionIntroduction2Declaration = DisjunctionIntroduction2Declaration(u=self.u)
            self.declare_instance(i=i)
            self._disjunction_introduction_2 = i
        return self._disjunction_introduction_2

    @property
    def disjunctive_resolution(self) -> DisjunctiveResolutionDeclaration:
        if self._disjunctive_resolution is None:
            i: DisjunctiveResolutionDeclaration = DisjunctiveResolutionDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._disjunctive_resolution = i
        return self._disjunctive_resolution

    @property
    def disjunctive_syllogism_1(self) -> DisjunctiveSyllogism1Declaration:
        if self._disjunctive_syllogism_1 is None:
            i: DisjunctiveSyllogism1Declaration = DisjunctiveSyllogism1Declaration(u=self.u)
            self.declare_instance(i=i)
            self._disjunctive_syllogism_1 = i
        return self._disjunctive_syllogism_1

    @property
    def disjunctive_syllogism_2(self) -> DisjunctiveSyllogism2Declaration:
        if self._disjunctive_syllogism_2 is None:
            i: DisjunctiveSyllogism2Declaration = DisjunctiveSyllogism2Declaration(u=self.u)
            self.declare_instance(i=i)
            self._disjunctive_syllogism_2 = i
        return self._disjunctive_syllogism_2

    @property
    def dne(self) -> DoubleNegationEliminationDeclaration:
        return self.double_negation_elimination

    @property
    def dni(self) -> DoubleNegationIntroductionDeclaration:
        return self.double_negation_introduction

    @property
    def double_negation_elimination(self) -> DoubleNegationEliminationDeclaration:
        if self._double_negation_elimination is None:
            i: DoubleNegationEliminationDeclaration = DoubleNegationEliminationDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._double_negation_elimination = i
        return self._double_negation_elimination

    @property
    def double_negation_introduction(self) -> DoubleNegationIntroductionDeclaration:
        if self._double_negation_introduction is None:
            i: DoubleNegationIntroductionDeclaration = DoubleNegationIntroductionDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._double_negation_introduction = i
        return self._double_negation_introduction

    @property
    def ec(self) -> EqualityCommutativityDeclaration:
        return self.equality_commutativity

    @property
    def equality_commutativity(self) -> EqualityCommutativityDeclaration:
        if self._equality_commutativity is None:
            i: EqualityCommutativityDeclaration = EqualityCommutativityDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._equality_commutativity = i
        return self._equality_commutativity

    @property
    def equal_terms_substitution(self) -> EqualTermsSubstitutionDeclaration:
        if self._equal_terms_substitution is None:
            i: EqualTermsSubstitutionDeclaration = EqualTermsSubstitutionDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._equal_terms_substitution = i
        return self._equal_terms_substitution

    @property
    def ets(self) -> EqualTermsSubstitutionDeclaration:
        return self.equal_terms_substitution

    @property
    def hypothetical_syllogism(self) -> HypotheticalSyllogismDeclaration:
        if self._hypothetical_syllogism is None:
            i: HypotheticalSyllogismDeclaration = HypotheticalSyllogismDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._hypothetical_syllogism = i
        return self._hypothetical_syllogism

    @property
    def hs(self) -> HypotheticalSyllogismDeclaration:
        return self.hypothetical_syllogism

    @property
    def ii1(self) -> InconsistencyIntroduction1Declaration:
        return self.inconsistency_introduction_1

    @property
    def ii2(self) -> InconsistencyIntroduction2Declaration:
        return self.inconsistency_introduction_2

    @property
    def ii3(self) -> InconsistencyIntroduction3Declaration:
        return self.inconsistency_introduction_3

    @property
    def inconsistency_introduction_1(self) -> InconsistencyIntroduction1Declaration:
        if self._inconsistency_introduction_1 is None:
            i: InconsistencyIntroduction1Declaration = InconsistencyIntroduction1Declaration(u=self.u)
            self.declare_instance(i=i)
            self._inconsistency_introduction_1 = i
        return self._inconsistency_introduction_1

    @property
    def inconsistency_introduction_2(self) -> InconsistencyIntroduction2Declaration:
        if self._inconsistency_introduction_2 is None:
            i: InconsistencyIntroduction2Declaration = InconsistencyIntroduction2Declaration(u=self.u)
            self.declare_instance(i=i)
            self._inconsistency_introduction_2 = i
        return self._inconsistency_introduction_2

    @property
    def inconsistency_introduction_3(self) -> InconsistencyIntroduction3Declaration:
        if self._inconsistency_introduction_3 is None:
            i: InconsistencyIntroduction3Declaration = InconsistencyIntroduction3Declaration(u=self.u)
            self.declare_instance(i=i)
            self._inconsistency_introduction_3 = i
        return self._inconsistency_introduction_3

    @property
    def is_strictly_propositional(self) -> bool:
        """By definition, an inference-rule-declaration is not a propositional object."""
        return False

    @property
    def modus_ponens(self) -> ModusPonensDeclaration:
        if self._modus_ponens is None:
            i: ModusPonensDeclaration = ModusPonensDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._modus_ponens = i
        return self._modus_ponens

    @property
    def modus_tollens(self) -> ModusTollensDeclaration:
        if self._modus_tollens is None:
            i: ModusTollensDeclaration = ModusTollensDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._modus_tollens = i
        return self._modus_tollens

    @property
    def mp(self) -> ModusPonensDeclaration:
        return self.modus_ponens

    @property
    def mt(self) -> ModusTollensDeclaration:
        return self.modus_tollens

    @property
    def pbc1(self) -> ProofByContradiction1Declaration:
        return self.proof_by_contradiction_1

    @property
    def pbc2(self) -> ProofByContradiction2Declaration:
        return self.proof_by_contradiction_2

    @property
    def pbr(self) -> ProofByRefutation1Declaration:
        return self.proof_by_refutation_1

    @property
    def proof_by_contradiction_1(self) -> ProofByContradiction1Declaration:
        if self._proof_by_contradiction_1 is None:
            i: ProofByContradiction1Declaration = ProofByContradiction1Declaration(u=self.u)
            self.declare_instance(i=i)
            self._proof_by_contradiction_1 = i
        return self._proof_by_contradiction_1

    @property
    def proof_by_contradiction_2(self) -> ProofByContradiction2Declaration:
        if self._proof_by_contradiction_2 is None:
            i: ProofByContradiction2Declaration = ProofByContradiction2Declaration(u=self.u)
            self.declare_instance(i=i)
            self._proof_by_contradiction_2 = i
        return self._proof_by_contradiction_2

    @property
    def proof_by_refutation_1(self) -> ProofByRefutation1Declaration:
        if self._proof_by_refutation_1 is None:
            i: ProofByRefutation1Declaration = ProofByRefutation1Declaration(u=self.u)
            self.declare_instance(i=i)
            self._proof_by_refutation_1 = i
        return self._proof_by_refutation_1

    @property
    def proof_by_refutation_2(self) -> ProofByRefutation2Declaration:
        if self._proof_by_refutation_2 is None:
            i: ProofByRefutation2Declaration = ProofByRefutation2Declaration(u=self.u)
            self.declare_instance(i=i)
            self._proof_by_refutation_2 = i
        return self._proof_by_refutation_2

    @property
    def variable_substitution(self) -> VariableSubstitutionDeclaration:
        if self._variable_substitution is None:
            i: VariableSubstitutionDeclaration = VariableSubstitutionDeclaration(u=self.u)
            self.declare_instance(i=i)
            self._variable_substitution = i
        return self._variable_substitution

    def verify_element(self, phi: InferenceRuleDeclaration):
        _, phi, _ = verify_formula(u=self.u, input_value=phi, arg='phi')
        verify(assertion=is_declaratively_member_of_class(u=self.u, phi=phi, c=self.u.c2.inference_rule),
            msg='phi is not an inference-rule')

    @property
    def vs(self) -> VariableSubstitutionDeclaration:
        return self.variable_substitution


class AbsorptionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`absorption<absorption_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.absorption
        dashed_name = 'absorption'
        abridged_name = 'absorp.'
        name = 'absorption'
        explicit_name = 'absorption inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p_implies_q: FlexibleFormula) -> typing.Tuple[
        bool, AbsorptionDeclaration.Premises]:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements.
        _, p_implies_q, _ = verify_formula_statement(t=self.t, input_value=p_implies_q, form=self.i.term_p_implies_q,
            mask=self.i.term_p_implies_q_mask, is_strictly_propositional=True, raise_exception=True,
            error_code=error_code)
        # The method either raises an exception during validation, or return True.
        valid_premises: AbsorptionDeclaration.Premises = AbsorptionDeclaration.Premises(p_implies_q=p_implies_q)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_absorption_paragraph_proof(o=o)
        return output

    def construct_formula(self, p_implies_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(p_implies_q=p_implies_q)

    @property
    def i(self) -> AbsorptionDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: AbsorptionDeclaration = super().i
        return i

    def infer_formula_statement(self, p_implies_q: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_implies_q=p_implies_q)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class AxiomInterpretationInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`axiom-interpretation<axiom_interpretation_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .

    Inherits from :ref:`InferenceRuleInclusion<inference_rule_inclusion_python_class>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.axiom_interpretation
        dashed_name = 'axiom-interpretation'
        acronym = 'ai'
        abridged_name = None
        name = 'axiom interpretation'
        explicit_name = 'axiom interpretation inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, a: FlexibleAxiom, p: FlexibleFormula) -> typing.Tuple[
        bool, AxiomInterpretationDeclaration.Premises]:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements.
        _, a, _ = verify_axiom_inclusion(arg='a', t=self.t, input_value=a, raise_exception=True, error_code=error_code)
        verify(assertion=not a.locked,
            msg=f'The axiom-inclusion argument ⌜a⌝({a}) is locked, new interpretations are not authorized.',
            severity=verification_severities.error, raise_exception=True, error_code=error_code, a=a)
        _, p, _ = verify_formula(arg='p', u=self.u, input_value=p, is_strictly_propositional=True, raise_exception=True,
            error_code=error_code)
        # TODO: BUG: validate_formula does not support basic masks like: ⌜P⌝ where P is a variable.
        # validate_formula(u=self.u, input_value=p, form=self.i.term_p,
        #    mask=self.i.term_p_mask)
        # The method either raises an exception during validation, or return True.
        valid_premises: AxiomInterpretationDeclaration.Premises = AxiomInterpretationDeclaration.Premises(a=a, p=p)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """Overrides the generic paragraph proof method."""
        output = yield from configuration.locale.compose_axiom_interpretation_paragraph_proof(o=o)
        return output

    def construct_formula(self, a: FlexibleAxiom, p: FlexibleFormula, echo: (None, bool) = None) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(a=a, p=p)

    @property
    def i(self) -> AxiomInterpretationDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: AxiomInterpretationDeclaration = super().i
        return i

    def infer_formula_statement(self, a: FlexibleAxiom, p: FlexibleFormula, lock: bool = True, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        :param a:
        :param p:
        :param lock: Locks the definition-inclusion to forbid additional interpretations.
        :param ref:
        :param paragraph_header:
        :param subtitle:
        :param echo:
        :return:
        """
        premises = self.i.Premises(a=a, p=p)
        s: InferredStatement = InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)
        if lock:
            a.locked = lock
        return s


class BiconditionalElimination1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`biconditional-elimination-1<biconditional_elimination_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.biconditional_elimination_1
        dashed_name = 'biconditional-elimination-1'
        acronym = 'be1'
        abridged_name = None
        name = 'biconditional elimination #1'
        explicit_name = 'biconditional elimination #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p_iff_q: FlexibleFormula) -> typing.Tuple[
        bool, BiconditionalElimination1Declaration.Premises]:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements.
        _, p_iff_q, _ = verify_formula_statement(t=self.t, input_value=p_iff_q, form=self.i.term_p_iff_q,
            mask=self.i.term_p_iff_q_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        # The method either raises an exception during validation, or return True.
        valid_premises: BiconditionalElimination1Declaration.Premises = BiconditionalElimination1Declaration.Premises(
            p_iff_q=p_iff_q)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_biconditional_elimination_1_paragraph_proof(o=o)
        return output

    def construct_formula(self, p_iff_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(p_iff_q=p_iff_q)

    @property
    def i(self) -> BiconditionalElimination1Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: BiconditionalElimination1Declaration = super().i
        return i

    def infer_formula_statement(self, p_iff_q: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_iff_q=p_iff_q)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class BiconditionalElimination2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`biconditional-elimination-2<biconditional_elimination_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.biconditional_elimination_2
        dashed_name = 'biconditional-elimination-2'
        acronym = 'be2'
        abridged_name = None
        name = 'biconditional elimination #2'
        explicit_name = 'biconditional elimination #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p_iff_q: FlexibleFormula) -> typing.Tuple[
        bool, BiconditionalElimination2Declaration.Premises]:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements.
        _, p_iff_q, _ = verify_formula_statement(t=self.t, input_value=p_iff_q, form=self.i.term_p_iff_q,
            mask=self.i.term_p_iff_q_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        # The method either raises an exception during validation, or return True.
        valid_premises: BiconditionalElimination2Declaration.Premises = BiconditionalElimination2Declaration.Premises(
            p_iff_q=p_iff_q)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_biconditional_elimination_2_paragraph_proof(o=o)
        return output

    def construct_formula(self, p_iff_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(p_iff_q=p_iff_q)

    @property
    def i(self) -> BiconditionalElimination1Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: BiconditionalElimination1Declaration = super().i
        return i

    def infer_formula_statement(self, p_iff_q: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_iff_q=p_iff_q)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class BiconditionalIntroductionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`biconditional-introduction<biconditional_introduction_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.biconditional_introduction
        dashed_name = 'biconditional-introduction'
        acronym = 'bi'
        abridged_name = None
        name = 'biconditional introduction'
        explicit_name = 'biconditional introduction inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p_implies_q: FlexibleFormula, q_implies_p: FlexibleFormula) -> typing.Tuple[
        bool, BiconditionalIntroductionDeclaration.Premises]:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_implies_q, _ = verify_formula_statement(arg='p_implies_q', t=self.t, input_value=p_implies_q,
            form=self.i.term_p_implies_q, mask=self.i.term_p_implies_q_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        _, q_implies_p, _ = verify_formula_statement(arg='q_implies_p', t=self.t, input_value=q_implies_p,
            form=self.i.term_q_implies_p, mask=self.i.term_q_implies_p_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        # The method either raises an exception during validation, or return True.
        valid_premises: BiconditionalIntroductionDeclaration.Premises = BiconditionalIntroductionDeclaration.Premises(
            p_implies_q=p_implies_q, q_implies_p=q_implies_p)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_biconditional_introduction_paragraph_proof(o=o)
        return output

    def construct_formula(self, p_implies_q: FlexibleFormula, q_implies_p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(p_implies_q=p_implies_q, q_implies_p=q_implies_p)

    @property
    def i(self) -> BiconditionalIntroductionDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: BiconditionalIntroductionDeclaration = super().i
        return i

    def infer_formula_statement(self, p_implies_q: FlexibleFormula, q_implies_p: FlexibleFormula,
        ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_implies_q=p_implies_q, q_implies_p=q_implies_p)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ConjunctionElimination1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`conjunction-elimination-1<conjunction_elimination_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.conjunction_elimination_1
        dashed_name = 'conjunction-elimination-1'
        acronym = 'ce1'
        abridged_name = None
        name = 'conjunction elimination #1'
        explicit_name = 'conjunction elimination #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p_and_q: FlexibleFormula) -> typing.Tuple[
        bool, ConjunctionElimination1Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_and_q, _ = verify_formula_statement(arg='p_and_q', t=self.t, input_value=p_and_q, form=self.i.term_p_and_q,
            mask=self.i.term_p_and_q_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        # The method either raises an exception during validation, or return True.
        valid_premises: ConjunctionElimination1Declaration.Premises = ConjunctionElimination1Declaration.Premises(
            p_and_q=p_and_q)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_conjunction_elimination_1_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> ConjunctionElimination1Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: ConjunctionElimination1Declaration = super().i
        return i

    def construct_formula(self, p_and_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p_and_q=p_and_q)

    def infer_formula_statement(self, p_and_q: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_and_q=p_and_q)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ConjunctionElimination2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`conjunction-elimination-2<conjunction_elimination_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.conjunction_elimination_2
        dashed_name = 'conjunction-elimination-2'
        acronym = 'bel'
        abridged_name = 'conj. elim. right'
        name = 'conjunction elimination #2'
        explicit_name = 'conjunction elimination #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_conjunction_elimination_2_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, p_and_q: FlexibleFormula) -> typing.Tuple[
        bool, ConjunctionElimination2Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_and_q, _ = verify_formula_statement(arg='p_and_q', t=self.t, input_value=p_and_q, form=self.i.term_p_and_q,
            mask=self.i.term_p_and_q_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        # The method either raises an exception during validation, or return True.
        valid_premises: ConjunctionElimination2Declaration.Premises = ConjunctionElimination2Declaration.Premises(
            p_and_q=p_and_q)
        return True, valid_premises

    @property
    def i(self) -> ConjunctionElimination2Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: ConjunctionElimination2Declaration = super().i
        return i

    def construct_formula(self, p_and_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p_and_q=p_and_q)

    def infer_formula_statement(self, p_and_q: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_and_q=p_and_q)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ConjunctionIntroductionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`conjunction-introduction<conjunction_introduction_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.conjunction_introduction
        dashed_name = 'conjunction-introduction'
        acronym = 'ci'
        abridged_name = 'conj.-intro.'
        name = 'conjunction introduction'
        explicit_name = 'conjunction introduction inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p: FlexibleFormula, q: FlexibleFormula) -> typing.Tuple[
        bool, ConjunctionIntroductionDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p, _ = verify_formula_statement(arg='p', t=self.t, input_value=p, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        _, q, _ = verify_formula_statement(arg='q', t=self.t, input_value=q, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        # The method either raises an exception during validation, or return True.
        valid_premises: ConjunctionIntroductionDeclaration.Premises = ConjunctionIntroductionDeclaration.Premises(p=p,
            q=q)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """Composes the paragraph-proof of inferred-statements based on the :ref:`conjunction-introduction<conjunction_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` ."""
        output = yield from configuration.locale.compose_conjunction_introduction_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> ConjunctionIntroductionDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: ConjunctionIntroductionDeclaration = super().i
        return i

    def construct_formula(self, p: FlexibleFormula, q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p=p, q=q)

    def infer_formula_statement(self, p: FlexibleFormula, q: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p=p, q=q)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ConstructiveDilemmaInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`constructive-dilemma<constructive_dilemma_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.constructive_dilemma
        dashed_name = 'constructive-dilemma'
        acronym = 'cd'
        abridged_name = None
        name = 'constructive dilemma'
        explicit_name = 'constructive dilemma inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p_implies_q: FlexibleFormula, r_implies_s: FlexibleFormula,
        p_or_r: FlexibleFormula) -> typing.Tuple[bool, ConstructiveDilemmaDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_implies_q, _ = verify_formula_statement(arg='p_implies_q', t=self.t, input_value=p_implies_q,
            form=self.i.term_p_implies_q, mask=self.i.term_p_implies_q_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, r_implies_s, _ = verify_formula_statement(arg='r_implies_s', t=self.t, input_value=r_implies_s,
            form=self.i.term_r_implies_s, mask=self.i.term_r_implies_s_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        r_implies_s: CompoundFormula
        _, p_or_r, _ = verify_formula_statement(arg='p_or_r', t=self.t, input_value=p_or_r, form=self.i.term_p_or_r,
            mask=self.i.term_p_or_r_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        p_or_r: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: ConstructiveDilemmaDeclaration.Premises = ConstructiveDilemmaDeclaration.Premises(
            p_implies_q=p_implies_q, r_implies_s=r_implies_s, p_or_r=p_or_r)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_constructive_dilemma_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> ConstructiveDilemmaDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: ConstructiveDilemmaDeclaration = super().i
        return i

    def construct_formula(self, p_implies_q: FlexibleFormula, r_implies_s: FlexibleFormula,
        p_or_r: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p_implies_q=p_implies_q, r_implies_s=r_implies_s, p_or_r=p_or_r)

    def infer_formula_statement(self, p_implies_q: FlexibleFormula, r_implies_s: FlexibleFormula,
        p_or_r: FlexibleFormula, ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
        subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_implies_q=p_implies_q, r_implies_s=r_implies_s, p_or_r=p_or_r)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class DefinitionInterpretationInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`definition-interpretation<definition_interpretation_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .

    Inherits from :ref:`InferenceRuleInclusion<inference_rule_inclusion_python_class>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.definition_interpretation
        dashed_name = 'definition-interpretation'
        acronym = 'di'
        abridged_name = None
        name = 'definition interpretation'
        explicit_name = 'definition interpretation inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, d: FlexibleDefinition, x: FlexibleFormula, y: FlexibleFormula) -> typing.Tuple[
        bool, DefinitionInterpretationDeclaration.Premises]:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements.
        _, d, _ = verify_definition_inclusion(arg='d', t=self.t, input_value=d, raise_exception=True,
            error_code=error_code)
        verify(assertion=not d.locked,
            msg=f'The definition-inclusion argument ⌜d⌝({d}) is locked, new interpretations are not authorized.',
            severity=verification_severities.error, raise_exception=True, error_code=error_code, d=d)
        _, x, _ = verify_formula(arg='x', u=self.u, input_value=x, raise_exception=True, error_code=error_code)
        _, y, _ = verify_formula(arg='y', u=self.u, input_value=y, raise_exception=True, error_code=error_code)
        # The method either raises an exception during validation, or return True.
        valid_premises: DefinitionInterpretationDeclaration.Premises = DefinitionInterpretationDeclaration.Premises(d=d,
            x=x, y=y)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """Overrides the generic paragraph proof method."""
        output = yield from configuration.locale.compose_definition_interpretation_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> DefinitionInterpretationDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: DefinitionInterpretationDeclaration = super().i
        return i

    def construct_formula(self, d: FlexibleDefinition, x: FlexibleFormula, y: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(d=d, x=x, y=y)

    def infer_formula_statement(self, d: FlexibleDefinition, x: FlexibleFormula, y: FlexibleFormula, lock: bool = True,
        ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        :param d:
        :param x:
        :param y:
        :param lock: Locks the definition-inclusion to forbid additional interpretations.
        :param ref:
        :param paragraph_header:
        :param subtitle:
        :param echo:
        :return:
        """
        premises = self.i.Premises(d=d, x=x, y=y)
        s: InferredStatement = InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)
        if lock:
            d.locked = lock
        return s


class DestructiveDilemmaInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`destructive-dilemma<destructive_dilemma_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.destructive_dilemma
        dashed_name = 'destructive-dilemma'
        acronym = 'dd'
        abridged_name = None
        name = 'destructive dilemma'
        explicit_name = 'destructive dilemma inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_destructive_dilemma_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, p_implies_q: FlexibleFormula, r_implies_s: FlexibleFormula,
        not_q_or_not_s: FlexibleFormula) -> typing.Tuple[bool, DestructiveDilemmaDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_implies_q, _ = verify_formula_statement(arg='p_implies_q', t=self.t, input_value=p_implies_q,
            form=self.i.term_p_implies_q, mask=self.i.term_p_implies_q_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, r_implies_s, _ = verify_formula_statement(arg='r_implies_s', t=self.t, input_value=r_implies_s,
            form=self.i.term_r_implies_s, mask=self.i.term_r_implies_s_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        r_implies_s: CompoundFormula
        _, not_q_or_not_s, _ = verify_formula_statement(arg='not_q_or_not_s', t=self.t, input_value=not_q_or_not_s,
            form=self.i.term_not_q_or_not_s, mask=self.i.term_not_q_or_not_s_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        not_q_or_not_s: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: DestructiveDilemmaDeclaration.Premises = DestructiveDilemmaDeclaration.Premises(
            p_implies_q=p_implies_q, r_implies_s=r_implies_s, not_q_or_not_s=not_q_or_not_s)
        return True, valid_premises

    @property
    def i(self) -> DestructiveDilemmaDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: DestructiveDilemmaDeclaration = super().i
        return i

    def construct_formula(self, p_implies_q: FlexibleFormula, r_implies_s: FlexibleFormula,
        not_q_or_not_s: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p_implies_q=p_implies_q, r_implies_s=r_implies_s, not_q_or_not_s=not_q_or_not_s)

    def infer_formula_statement(self, p_implies_q: FlexibleFormula, r_implies_s: FlexibleFormula,
        not_q_or_not_s: FlexibleFormula, ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
        subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_implies_q=p_implies_q, r_implies_s=r_implies_s, not_q_or_not_s=not_q_or_not_s)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class DisjunctionIntroduction1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`disjunction-introduction-1<disjunction_introduction_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.disjunction_introduction_1
        dashed_name = 'disjunction-introduction-1'
        acronym = 'di1'
        abridged_name = None
        name = 'disjunction introduction #1'
        explicit_name = 'disjunction introduction #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """Composes the paragraph-proof of inferred-statements based on the :ref:`disjunction-introduction-1<disjunction_introduction_1_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` ."""
        output = yield from configuration.locale.compose_disjunction_introduction_1_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, p: FlexibleFormula, q: FlexibleFormula) -> typing.Tuple[
        bool, ConjunctionIntroductionDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p, _ = verify_formula_statement(arg='p', t=self.t, input_value=p, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        _, q, _ = verify_formula(arg='q', u=self.u, input_value=q, is_strictly_propositional=True, raise_exception=True,
            error_code=error_code)
        # The method either raises an exception during validation, or return True.
        valid_premises: ConjunctionIntroductionDeclaration.Premises = ConjunctionIntroductionDeclaration.Premises(p=p,
            q=q)
        return True, valid_premises

    @property
    def i(self) -> DisjunctionIntroduction1Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: DisjunctionIntroduction1Declaration = super().i
        return i

    def construct_formula(self, p: FlexibleFormula, q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p=p, q=q)

    def infer_formula_statement(self, p: FlexibleFormula, q: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p=p, q=q)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class DisjunctionIntroduction2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`disjunction-introduction-2<disjunction_introduction_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.disjunction_introduction_2
        dashed_name = 'disjunction-introduction-2'
        acronym = 'di2'
        abridged_name = None
        name = 'disjunction introduction #2'
        explicit_name = 'disjunction introduction #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """Composes the paragraph-proof of inferred-statements based on the :ref:`disjunction-introduction-2<disjunction_introduction_2_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` ."""
        output = yield from configuration.locale.compose_disjunction_introduction_2_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, p: FlexibleFormula, q: FlexibleFormula) -> typing.Tuple[
        bool, ConjunctionIntroductionDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p, _ = verify_formula_statement(arg='p', t=self.t, input_value=p, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        _, q, _ = verify_formula(arg='q', u=self.u, input_value=q, is_strictly_propositional=True, raise_exception=True,
            error_code=error_code)
        # The method either raises an exception during validation, or return True.
        valid_premises: ConjunctionIntroductionDeclaration.Premises = ConjunctionIntroductionDeclaration.Premises(p=p,
            q=q)
        return True, valid_premises

    @property
    def i(self) -> DisjunctionIntroduction2Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: DisjunctionIntroduction2Declaration = super().i
        return i

    def construct_formula(self, p: FlexibleFormula, q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p=p, q=q)

    def infer_formula_statement(self, p: FlexibleFormula, q: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p=p, q=q)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class DisjunctiveResolutionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`disjunctive-resolution<disjunctive_resolution_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.disjunctive_resolution
        dashed_name = 'disjunctive-resolution'
        acronym = 'dr'
        abridged_name = None
        name = 'disjunctive resolution'
        explicit_name = 'disjunctive resolution inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p_or_q: FlexibleFormula, not_p_or_r: FlexibleFormula) -> typing.Tuple[
        bool, ConstructiveDilemmaDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_or_q, _ = verify_formula_statement(arg='p_or_q', t=self.t, input_value=p_or_q, form=self.i.term_p_or_q,
            mask=self.i.term_p_or_q_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        p_or_q: CompoundFormula
        _, not_p_or_r, _ = verify_formula_statement(arg='not_p_or_r', t=self.t, input_value=not_p_or_r,
            form=self.i.term_not_p_or_r, mask=self.i.term_not_p_or_r_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        not_p_or_r: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: DisjunctiveResolutionDeclaration.Premises = DisjunctiveResolutionDeclaration.Premises(
            p_or_q=p_or_q, not_p_or_r=not_p_or_r)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_disjunctive_resolution_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> DisjunctiveResolutionDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: DisjunctiveResolutionDeclaration = super().i
        return i

    def construct_formula(self, p_or_q: FlexibleFormula, not_p_or_r: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p_or_q=p_or_q, not_p_or_r=not_p_or_r)

    def infer_formula_statement(self, p_or_q: FlexibleFormula, not_p_or_r: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_or_q=p_or_q, not_p_or_r=not_p_or_r)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class DisjunctiveSyllogism1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`disjunctive-syllogism-1<disjunctive_syllogism_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.disjunctive_syllogism_1
        dashed_name = 'disjunctive-syllogism-1'
        acronym = 'ds'
        abridged_name = None
        name = 'disjunctive syllogism'
        explicit_name = 'disjunctive syllogism inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_disjunctive_syllogism_1_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, p_or_q: FlexibleFormula, not_p: FlexibleFormula) -> typing.Tuple[
        bool, DisjunctiveSyllogism1Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_or_q, _ = verify_formula_statement(arg='p_or_q', t=self.t, input_value=p_or_q, form=self.i.term_p_or_q,
            mask=self.i.term_p_or_q_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        not_p: CompoundFormula
        _, not_p, _ = verify_formula_statement(arg='not_p', t=self.t, input_value=not_p, form=self.i.term_not_p,
            mask=self.i.term_not_p_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        not_p: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: DisjunctiveSyllogism1Declaration.Premises = DisjunctiveSyllogism1Declaration.Premises(
            p_or_q=p_or_q, not_p=not_p)
        return True, valid_premises

    @property
    def i(self) -> DisjunctiveSyllogism1Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: DisjunctiveSyllogism1Declaration = super().i
        return i

    def construct_formula(self, p_or_q: FlexibleFormula, not_p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p_or_q=p_or_q, not_p=not_p)

    def infer_formula_statement(self, p_or_q: FlexibleFormula, not_p: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_or_q=p_or_q, not_p=not_p)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class DisjunctiveSyllogism2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`disjunctive-syllogism-1<disjunctive_syllogism_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.disjunctive_syllogism_2
        dashed_name = 'disjunctive-syllogism-2'
        acronym = 'ds'
        abridged_name = None
        name = 'disjunctive syllogism'
        explicit_name = 'disjunctive syllogism inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_disjunctive_syllogism_2_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, p_or_q: FlexibleFormula, not_q: FlexibleFormula) -> typing.Tuple[
        bool, DisjunctiveSyllogism2Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_or_q, _ = verify_formula_statement(arg='p_or_q', t=self.t, input_value=p_or_q, form=self.i.term_p_or_q,
            mask=self.i.term_p_or_q_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        p_or_q: CompoundFormula
        _, not_q, _ = verify_formula_statement(arg='not_q', t=self.t, input_value=not_q, form=self.i.term_not_q,
            mask=self.i.term_not_q_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        not_q: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: DisjunctiveSyllogism1Declaration.Premises = DisjunctiveSyllogism2Declaration.Premises(
            p_or_q=p_or_q, not_q=not_q)
        return True, valid_premises

    @property
    def i(self) -> DisjunctiveSyllogism2Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: DisjunctiveSyllogism2Declaration = super().i
        return i

    def construct_formula(self, p_or_q: FlexibleFormula, not_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p_or_q=p_or_q, not_q=not_q)

    def infer_formula_statement(self, p_or_q: FlexibleFormula, not_q: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_or_q=p_or_q, not_q=not_q)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class DoubleNegationEliminationInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`double-negation-elimination<double_negation_elimination_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.double_negation_elimination
        dashed_name = 'double-negation-elimination'
        acronym = 'dne'
        abridged_name = 'double neg. elim.'
        name = 'double negation elimination'
        explicit_name = 'double negation elimination inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_double_negation_elimination_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, not_not_p: FlexibleFormula) -> typing.Tuple[
        bool, DoubleNegationEliminationDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, not_not_p, _ = verify_formula_statement(arg='not_not_p', t=self.t, input_value=not_not_p,
            form=self.i.term_not_not_p, mask=self.i.term_not_not_p_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        not_not_p: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: DoubleNegationEliminationDeclaration.Premises = DoubleNegationEliminationDeclaration.Premises(
            not_not_p=not_not_p)
        return True, valid_premises

    @property
    def i(self) -> DoubleNegationEliminationDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: DoubleNegationEliminationDeclaration = super().i
        return i

    def construct_formula(self, not_not_p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(not_not_p=not_not_p)

    def infer_formula_statement(self, not_not_p: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(not_not_p=not_not_p)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class DoubleNegationIntroductionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`double-negation-introduction<double_negation_introduction_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.double_negation_introduction
        dashed_name = 'double-negation-introduction'
        acronym = 'dni'
        abridged_name = 'double neg. intro.'
        name = 'double negation introduction'
        explicit_name = 'double negation introduction inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """Composes the paragraph-proof of inferred-statements based on the :ref:`double-negation-introduction<double_negation_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` ."""
        output = yield from configuration.locale.compose_double_negation_introduction_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, p: FlexibleFormula) -> typing.Tuple[
        bool, DoubleNegationIntroductionDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p, _ = verify_formula_statement(arg='p', t=self.t, input_value=p, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        p: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: DoubleNegationIntroductionDeclaration.Premises = DoubleNegationIntroductionDeclaration.Premises(
            p=p)
        return True, valid_premises

    @property
    def i(self) -> DoubleNegationIntroductionDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: DoubleNegationIntroductionDeclaration = super().i
        return i

    def construct_formula(self, p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p=p)

    def infer_formula_statement(self, p: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p=p)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class EqualityCommutativityInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`equality-commutativity<equality_commutativity_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.equality_commutativity
        dashed_name = 'equality-commutativity'
        acronym = 'ec'
        abridged_name = None
        name = 'equality commutativity'
        explicit_name = 'equality commutativity inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_equality_commutativity_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, x_equal_y: FlexibleFormula) -> typing.Tuple[
        bool, EqualityCommutativityDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, x_equal_y, _ = verify_formula_statement(arg='x_equal_y', t=self.t, input_value=x_equal_y,
            form=self.i.term_x_equal_y, mask=self.i.term_x_equal_y_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        x_equal_y: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: EqualityCommutativityDeclaration.Premises = EqualityCommutativityDeclaration.Premises(
            x_equal_y=x_equal_y)
        return True, valid_premises

    @property
    def i(self) -> EqualityCommutativityDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: EqualityCommutativityDeclaration = super().i
        return i

    def construct_formula(self, x_equal_y: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(x_equal_y=x_equal_y)

    def infer_formula_statement(self, x_equal_y: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(x_equal_y=x_equal_y)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class EqualTermsSubstitutionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`equal-terms-substitution<equal_terms_substitution_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.equal_terms_substitution
        dashed_name = 'equal-terms-substitution'
        acronym = 'ets'
        abridged_name = None
        name = 'equal terms substitution'
        explicit_name = 'equal terms substitution inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_equal_terms_substitution_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, p: FlexibleFormula, x_equal_y: FlexibleFormula) -> typing.Tuple[
        bool, EqualTermsSubstitutionDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p, _ = verify_formula_statement(arg='p', t=self.t, input_value=p, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        p: CompoundFormula
        _, x_equal_y, _ = verify_formula_statement(arg='x_equal_y', t=self.t, input_value=x_equal_y,
            form=self.i.term_x_equal_y, mask=self.i.term_x_equal_y_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        x_equal_y: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: EqualTermsSubstitutionDeclaration.Premises = EqualTermsSubstitutionDeclaration.Premises(p=p,
            x_equal_y=x_equal_y)
        return True, valid_premises

    @property
    def i(self) -> EqualTermsSubstitutionDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: EqualTermsSubstitutionDeclaration = super().i
        return i

    def construct_formula(self, p: FlexibleFormula, x_equal_y: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p=p, x_equal_y=x_equal_y)

    def infer_formula_statement(self, p: FlexibleFormula, x_equal_y: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p=p, x_equal_y=x_equal_y)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class HypotheticalSyllogismInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`hypothetical-syllogism<hypothetical_syllogism_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.hypothetical_syllogism
        dashed_name = 'hypothetical-syllogism'
        acronym = 'hs'
        abridged_name = None
        name = 'hypothetical syllogism'
        explicit_name = 'hypothetical syllogism inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_hypothetical_syllogism_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, p_implies_q: FlexibleFormula, q_implies_r: FlexibleFormula) -> typing.Tuple[
        bool, HypotheticalSyllogismDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_implies_q, _ = verify_formula_statement(arg='p_implies_q', t=self.t, input_value=p_implies_q,
            form=self.i.term_p_implies_q, mask=self.i.term_p_implies_q_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, q_implies_r, _ = verify_formula_statement(arg='q_implies_r', t=self.t, input_value=q_implies_r,
            form=self.i.term_q_implies_r, mask=self.i.term_q_implies_r_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        q_implies_r: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: HypotheticalSyllogismDeclaration.Premises = HypotheticalSyllogismDeclaration.Premises(
            p_implies_q=p_implies_q, q_implies_r=q_implies_r)
        return True, valid_premises

    @property
    def i(self) -> HypotheticalSyllogismDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: HypotheticalSyllogismDeclaration = super().i
        return i

    def construct_formula(self, p_implies_q: FlexibleFormula, q_implies_r: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p_implies_q=p_implies_q, q_implies_r=q_implies_r)

    def infer_formula_statement(self, p_implies_q: FlexibleFormula, q_implies_r: FlexibleFormula,
        ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_implies_q=p_implies_q, q_implies_r=q_implies_r)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class InconsistencyIntroduction1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`inconsistency-introduction-1<inconsistency_introduction_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.inconsistency_introduction_1
        dashed_name = 'inconsistency-introduction-1'
        acronym = 'ii1'
        abridged_name = None
        name = 'inconsistency introduction #1'
        explicit_name = 'inconsistency introduction #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_inconsistency_introduction_1_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, p: FlexibleFormula, not_p: FlexibleFormula, t: TheoryDerivation) -> typing.Tuple[
        bool, InconsistencyIntroduction1Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p, _ = verify_formula_statement(arg='p', t=t, input_value=p, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        p: CompoundFormula
        _, not_p, _ = verify_formula_statement(arg='not_p', t=t, input_value=not_p, form=self.i.term_not_p,
            mask=self.i.term_not_p_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        not_p: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: InconsistencyIntroduction1Declaration.Premises = InconsistencyIntroduction1Declaration.Premises(
            p=p, not_p=not_p, t=t)
        return True, valid_premises

    @property
    def i(self) -> InconsistencyIntroduction1Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: InconsistencyIntroduction1Declaration = super().i
        return i

    def construct_formula(self, p: FlexibleFormula, not_p: FlexibleFormula, t: TheoryDerivation) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p=p, not_p=not_p, t=t)

    def infer_formula_statement(self, p: FlexibleFormula, not_p: FlexibleFormula, t: TheoryDerivation,
        ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p=p, not_p=not_p, t=t)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class InconsistencyIntroduction2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`inconsistency-introduction-2<inconsistency_introduction_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.inconsistency_introduction_2
        dashed_name = 'inconsistency-introduction-2'
        acronym = 'ii2'
        abridged_name = None
        name = 'inconsistency introduction #2'
        explicit_name = 'inconsistency introduction #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_inconsistency_introduction_2_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, x_equal_y: FlexibleFormula, x_unequal_y: FlexibleFormula, t: TheoryDerivation) -> \
        typing.Tuple[bool, InconsistencyIntroduction2Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, x_equal_y, _ = verify_formula_statement(arg='x_equal_y', t=t, input_value=x_equal_y,
            form=self.i.term_x_equal_y, mask=self.i.term_x_equal_y_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        x_equal_y: CompoundFormula
        _, x_unequal_y, _ = verify_formula_statement(arg='x_unequal_y', t=t, input_value=x_unequal_y,
            form=self.i.term_x_unequal_y, mask=self.i.term_x_unequal_y_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        x_unequal_y: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: InconsistencyIntroduction2Declaration.Premises = InconsistencyIntroduction2Declaration.Premises(
            x_equal_y=x_equal_y, x_unequal_y=x_unequal_y, t=t)
        return True, valid_premises

    @property
    def i(self) -> InconsistencyIntroduction2Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: InconsistencyIntroduction2Declaration = super().i
        return i

    def construct_formula(self, x_equal_y: FlexibleFormula, x_unequal_y: FlexibleFormula,
        t: TheoryDerivation) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(x_equal_y=x_equal_y, x_unequal_y=x_unequal_y, t=t)

    def infer_formula_statement(self, x_equal_y: FlexibleFormula, x_unequal_y: FlexibleFormula, t: TheoryDerivation,
        ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(x_equal_y=x_equal_y, x_unequal_y=x_unequal_y, t=t)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class InconsistencyIntroduction3Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`inconsistency-introduction-3<inconsistency_introduction_3_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.inconsistency_introduction_3
        dashed_name = 'inconsistency-introduction-3'
        acronym = 'ii3'
        abridged_name = None
        name = 'inconsistency introduction #3'
        explicit_name = 'inconsistency introduction #3 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_inconsistency_introduction_3_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, x_unequal_x: FlexibleFormula, t: TheoryDerivation) -> typing.Tuple[
        bool, InconsistencyIntroduction3Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, x_unequal_x, _ = verify_formula_statement(arg='x_unequal_x', t=t, input_value=x_unequal_x,
            form=self.i.term_x_unequal_x, mask=self.i.term_x_unequal_x_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        x_unequal_x: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: InconsistencyIntroduction3Declaration.Premises = InconsistencyIntroduction3Declaration.Premises(
            x_unequal_x=x_unequal_x, t=t)
        return True, valid_premises

    @property
    def i(self) -> InconsistencyIntroduction3Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: InconsistencyIntroduction3Declaration = super().i
        return i

    def construct_formula(self, x_unequal_x: FlexibleFormula, t: TheoryDerivation) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(x_unequal_x=x_unequal_x, t=t)

    def infer_formula_statement(self, x_unequal_x: FlexibleFormula, t: TheoryDerivation, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(x_unequal_x=x_unequal_x, t=t)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ModusPonensInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`modus-ponens<modus_ponens_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.modus_ponens
        dashed_name = 'modus-ponens'
        acronym = 'mp'
        abridged_name = None
        name = 'modus ponens'
        explicit_name = 'modus ponens inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p_implies_q: FlexibleFormula, p: FlexibleFormula) -> typing.Tuple[
        bool, ModusPonensDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_implies_q, _ = verify_formula_statement(arg='p_implies_q', t=self.t, input_value=p_implies_q,
            form=self.i.term_p_implies_q, mask=self.i.term_p_implies_q_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, p, _ = verify_formula_statement(arg='p', t=self.t, input_value=p, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        p: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: ModusPonensDeclaration.Premises = ModusPonensDeclaration.Premises(p_implies_q=p_implies_q, p=p)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_modus_ponens_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> ModusPonensDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: ModusPonensDeclaration = super().i
        return i

    def construct_formula(self, p_implies_q: FlexibleFormula, p: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p_implies_q=p_implies_q, p=p)

    def infer_formula_statement(self, p_implies_q: FlexibleFormula, p: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_implies_q=p_implies_q, p=p)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ModusTollensInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`modus-tollens<modus_tollens_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.modus_tollens
        dashed_name = 'modus-tollens'
        acronym = 'mt'
        abridged_name = None
        name = 'modus tollens'
        explicit_name = 'modus tollens inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p_implies_q: FlexibleFormula, not_q: FlexibleFormula) -> typing.Tuple[
        bool, ModusTollensDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p_implies_q, _ = verify_formula_statement(arg='p_implies_q', t=self.t, input_value=p_implies_q,
            form=self.i.term_p_implies_q, mask=self.i.term_p_implies_q_mask, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        p_implies_q: CompoundFormula
        _, not_q, _ = verify_formula_statement(arg='not_q', t=self.t, input_value=not_q, form=self.i.term_not_q,
            mask=self.i.term_not_q_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        not_q: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: ModusTollensDeclaration.Premises = ModusTollensDeclaration.Premises(p_implies_q=p_implies_q,
            not_q=not_q)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_modus_tollens_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> ModusTollensDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: ModusTollensDeclaration = super().i
        return i

    def construct_formula(self, p_implies_q: FlexibleFormula, not_q: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p_implies_q=p_implies_q, not_q=not_q)

    def infer_formula_statement(self, p_implies_q: FlexibleFormula, not_q: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_implies_q=p_implies_q, not_q=not_q)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ProofByContradiction1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`proof-by-contradiction-1<proof_by_contradiction_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.proof_by_contradiction_1
        dashed_name = 'proof-by-contradiction-1'
        acronym = 'pbc1'
        abridged_name = None
        name = 'proof by contradiction #1'
        explicit_name = 'proof by contradiction #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> typing.Tuple[
        bool, ProofByContradiction1Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, h, _ = verify_hypothesis(arg='h', t=self.t, input_value=h, hypothesis_form=self.i.term_not_p,
            hypothesis_mask=self.i.term_not_p_mask, is_strictly_propositional=True, raise_exception=True,
            error_code=error_code)
        h: Hypothesis
        _, inc_h, _ = verify_formula_statement(arg='inc_h', t=self.t, input_value=inc_h, form=self.i.term_inc_h,
            mask=self.i.term_inc_h_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        inc_h: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: ProofByContradiction1Declaration.Premises = ProofByContradiction1Declaration.Premises(h=h,
            inc_h=inc_h)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_proof_by_contradiction_1_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> ProofByContradiction1Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: ProofByContradiction1Declaration = super().i
        return i

    def construct_formula(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(h=h, inc_h=inc_h)

    def infer_formula_statement(self, h: FlexibleFormula, inc_h: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(h=h, inc_h=inc_h)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ProofByContradiction2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`proof-by-contradiction-2<proof_by_contradiction_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.proof_by_contradiction_2
        dashed_name = 'proof-by-contradiction-2'
        acronym = 'pbc2'
        abridged_name = None
        name = 'proof by contradiction #2'
        explicit_name = 'proof by contradiction #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> typing.Tuple[
        bool, ProofByContradiction2Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, h, _ = verify_hypothesis(arg='h', t=self.t, input_value=h, hypothesis_form=self.i.term_x_unequal_y,
            hypothesis_mask=self.i.term_x_unequal_y_mask, is_strictly_propositional=True, raise_exception=True,
            error_code=error_code)
        h: Hypothesis
        _, inc_h, _ = verify_formula_statement(arg='inc_h', t=self.t, input_value=inc_h, form=self.i.term_inc_h,
            mask=self.i.term_inc_h_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        inc_h: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: ProofByContradiction2Declaration.Premises = ProofByContradiction2Declaration.Premises(h=h,
            inc_h=inc_h)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_proof_by_contradiction_2_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> ProofByContradiction2Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: ProofByContradiction2Declaration = super().i
        return i

    def construct_formula(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(h=h, inc_h=inc_h)

    def infer_formula_statement(self, h: FlexibleFormula, inc_h: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(h=h, inc_h=inc_h)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ProofByRefutation1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`proof-by-refutation-1<proof_by_refutation_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.proof_by_refutation_1
        dashed_name = 'proof-by-refutation-1'
        acronym = 'pbr1'
        abridged_name = None
        name = 'proof by refutation #1'
        explicit_name = 'proof by refutation #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> typing.Tuple[
        bool, ProofByRefutation1Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, h, _ = verify_hypothesis(arg='h', t=self.t, input_value=h, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        h: Hypothesis
        _, inc_h, _ = verify_formula_statement(arg='inc_h', t=self.t, input_value=inc_h, form=self.i.term_inc_h,
            mask=self.i.term_inc_h_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        inc_h: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: ProofByRefutation1Declaration.Premises = ProofByRefutation1Declaration.Premises(h=h,
            inc_h=inc_h)
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_proof_by_refutation_1_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> ProofByRefutation1Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: ProofByRefutation1Declaration = super().i
        return i

    def construct_formula(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(h=h, inc_h=inc_h)

    def infer_formula_statement(self, h: FlexibleFormula, inc_h: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(h=h, inc_h=inc_h)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ProofByRefutation2Inclusion(InferenceRuleInclusion):
    """

    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.proof_by_refutation_2
        dashed_name = 'proof-by-refutation-2'
        acronym = 'pbr2'
        abridged_name = None
        name = 'proof by refutation #2'
        explicit_name = 'proof by refutation #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_proof_by_refutation_2_paragraph_proof(o=o)
        return output

    def check_premises_validity(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> typing.Tuple[
        bool, ProofByRefutation2Declaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, h, _ = verify_hypothesis(arg='h', t=self.t, input_value=h, hypothesis_form=self.i.term_x_equal_y,
            hypothesis_mask=self.i.term_x_equal_y_mask, is_strictly_propositional=True, raise_exception=True,
            error_code=error_code)
        h: Hypothesis
        _, inc_h, _ = verify_formula_statement(arg='inc_h', t=self.t, input_value=inc_h, form=self.i.term_inc_h,
            mask=self.i.term_inc_h_mask, is_strictly_propositional=True, raise_exception=True, error_code=error_code)
        inc_h: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: ProofByRefutation2Declaration.Premises = ProofByRefutation2Declaration.Premises(h=h,
            inc_h=inc_h)
        return True, valid_premises

    @property
    def i(self) -> ProofByRefutation2Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: ProofByRefutation2Declaration = super().i
        return i

    def construct_formula(self, h: FlexibleFormula, inc_h: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(h=h, inc_h=inc_h)

    def infer_formula_statement(self, h: FlexibleFormula, inc_h: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(h=h, inc_h=inc_h)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class VariableSubstitutionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`variable-substitution<variable_substitution_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>` .
    """

    def __init__(self, t: TheoryDerivation, echo: (None, bool) = None, proof: (None, bool) = None):
        i = t.u.i.variable_substitution
        dashed_name = 'variable-substitution'
        acronym = 'vs'
        abridged_name = None
        name = 'variable substitution'
        explicit_name = 'variable substitution inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p: FlexibleFormula, phi: FlexibleFormula) -> typing.Tuple[
        bool, VariableSubstitutionDeclaration.Premises]:
        error_code: ErrorCode = error_codes.error_003_inference_premise_validity_error
        # Validate that expected formula-statements are formula-statements in the current theory.
        _, p, _ = verify_formula_statement(arg='p', t=self.t, input_value=p, is_strictly_propositional=True,
            raise_exception=True, error_code=error_code)
        p: CompoundFormula
        # The method either raises an exception during validation, or return True.
        valid_premises: VariableSubstitutionDeclaration.Premises = VariableSubstitutionDeclaration.Premises(p=p,
            phi=phi)
        # TODO: VariableSubstitutionInclusion().check_premises_validity(): Add a verification or warning step: the variable is not locked.
        return True, valid_premises

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[Composable, Composable, bool]:
        """Overrides the generic paragraph proof method."""
        output = yield from configuration.locale.compose_variable_substitution_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> VariableSubstitutionDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: VariableSubstitutionDeclaration = super().i
        return i

    def construct_formula(self, p: FlexibleFormula, phi: FlexibleFormula) -> CompoundFormula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return self.i.construct_formula(p=p, phi=phi)

    def infer_formula_statement(self, p: FlexibleFormula, phi: FlexibleFormula, ref: (None, str) = None,
        paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
        echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p=p, phi=phi)
        return InferredStatement(i=self, premises=premises, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class InferenceRuleInclusionCollection(collections.UserDict):
    """This python class models the collection of :ref:`inference-rules<inference_rule_math_concept>` :ref:`included<object_inclusion_math_concept>` in a :ref:`theory-derivation<theory_derivation_math_concept>`.

    In complement, it conveniently exposes as python properties a catalog of natively supported :ref:`inference-rules<inference_rule_math_concept>` that are automatically :ref:`included<object_inclusion_math_concept>` in the :ref:`theory-derivation<theory_derivation_math_concept>` when they are accessed for the first time.

    """

    def __init__(self, t: TheoryDerivation):
        self.t = t
        super().__init__()
        # Well-known objects
        self._absorption = None
        self._axiom_interpretation = None
        self._biconditional_elimination_1 = None
        self._biconditional_elimination_2 = None
        self._biconditional_introduction = None
        self._conjunction_elimination_1 = None
        self._conjunction_elimination_2 = None
        self._conjunction_introduction = None
        self._constructive_dilemma = None
        self._definition_interpretation = None
        self._destructive_dilemma = None
        self._disjunction_elimination = None
        self._disjunction_introduction_1 = None
        self._disjunction_introduction_2 = None
        self._disjunctive_resolution = None
        self._disjunctive_syllogism_1 = None
        self._disjunctive_syllogism_2 = None
        self._double_negation_elimination = None
        self._double_negation_introduction = None
        self._equality_commutativity = None
        self._equal_terms_substitution = None
        self._hypothetical_syllogism = None
        self._inconsistency_introduction_1 = None
        self._inconsistency_introduction_2 = None
        self._inconsistency_introduction_3 = None
        self._modus_ponens = None
        self._modus_tollens = None
        self._proof_by_contradiction_1 = None
        self._proof_by_contradiction_2 = None
        self._proof_by_refutation_1 = None
        self._proof_by_refutation_2 = None
        self._variable_substitution = None

    @property
    def absorb(self) -> AbsorptionInclusion:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Unabridged property: u.i.absorption

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.absorption

    @property
    def absorption(self) -> AbsorptionInclusion:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Abridged property: u.i.absorb

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._absorption is None:
            self._absorption = AbsorptionInclusion(t=self.t)
        return self._absorption

    @property
    def axiom_interpretation(self) -> AxiomInterpretationInclusion:
        """The axiom_interpretation inference-rule: 𝒜 ⊢ P.

               If the well-known inference-rule does not exist in the universe-of-discourse,
               the inference-rule is automatically declared.

               .. include:: ../../include/interpretative_inference_rule_warning.rstinc
               """
        if self._axiom_interpretation is None:
            self._axiom_interpretation = AxiomInterpretationInclusion(t=self.t)
        return self._axiom_interpretation

    @property
    def bel(self) -> BiconditionalElimination1Inclusion:
        """The well-known biconditional-elimination #1 inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Unabridged property: u.i.biconditional_elimination_1

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_elimination_1

    @property
    def ber(self) -> InferenceRuleInclusion:
        """The well-known biconditional-elimination #2 inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Unabridged property: u.i.biconditional_elimination_2

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_elimination_2

    @property
    def bi(self) -> BiconditionalIntroductionInclusion:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Unabridged property: u.i.biconditional_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_introduction

    @property
    def biconditional_elimination_1(self) -> BiconditionalElimination1Inclusion:
        """The well-known biconditional-elimination #1 inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Abridged property: u.i.bel

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._biconditional_elimination_1 is None:
            self._biconditional_elimination_1 = BiconditionalElimination1Inclusion(t=self.t)
        return self._biconditional_elimination_1

    @property
    def biconditional_elimination_2(self) -> BiconditionalElimination2Inclusion:
        """The well-known biconditional-elimination #2 inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Abridged property: u.i.ber()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._biconditional_elimination_1 is None:
            self._biconditional_elimination_1 = BiconditionalElimination2Inclusion(t=self.t)
        return self._biconditional_elimination_1

    @property
    def biconditional_introduction(self) -> BiconditionalIntroductionInclusion:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Abridged property: u.i.bi

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._biconditional_introduction is None:
            self._biconditional_introduction = BiconditionalIntroductionInclusion(t=self.t)
        return self._biconditional_introduction

    @property
    def cd(self) -> ConstructiveDilemmaInclusion:
        """The well-known constructive-dilemma inference-rule

        Unabridged property: universe_of_discourse.inference_rule.constructive_dilemma(...)

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.constructive_dilemma

    @property
    def cel(self) -> ConjunctionElimination1Declaration:
        """The well-known conjunction-elimination #1 inference-rule: (P ∧ Q) ⊢ P.

        Unabridged property: universe_of_discourse.inference_rule.conjunction_elimination_1()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.conjunction_elimination_1

    @property
    def cer(self) -> ConjunctionElimination2Inclusion:
        """The well-known conjunction-elimination #2 inference-rule: P ∧ Q ⊢ Q.

        Unabridged property: universe_of_discourse.inference_rule.conjunction_elimination_2()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.conjunction_elimination_2

    @property
    def ci(self) -> ConjunctionIntroductionInclusion:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Unabridged property: universe_of_discourse.inference_rule.conjunction_introduction()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.conjunction_introduction

    @property
    def conjunction_elimination_1(self) -> ConjunctionElimination1Inclusion:
        """The well-known conjunction-elimination #1 inference-rule: P ∧ Q ⊢ P.

        Abridged property: t.i.cel()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._conjunction_elimination_1 is None:
            self._conjunction_elimination_1 = ConjunctionElimination1Inclusion(t=self.t)
        return self._conjunction_elimination_1

    @property
    def conjunction_elimination_2(self) -> ConjunctionElimination2Inclusion:
        """The well-known conjunction-elimination #2 inference-rule: P ∧ Q ⊢ Q.

        Abridged property: t.i.cer

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._conjunction_elimination_2 is None:
            self._conjunction_elimination_2 = ConjunctionElimination2Inclusion(t=self.t)
        return self._conjunction_elimination_2

    @property
    def conjunction_introduction(self) -> ConjunctionIntroductionInclusion:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Abridged property: t.i.ci()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._conjunction_introduction is None:
            self._conjunction_introduction = ConjunctionIntroductionInclusion(t=self.t)
        return self._conjunction_introduction

    @property
    def constructive_dilemma(self) -> ConstructiveDilemmaInclusion:
        """The well-known constructive-dilemma inference-rule

        Abridged property: t.i.cd()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._constructive_dilemma is None:
            self._constructive_dilemma = ConstructiveDilemmaInclusion(t=self.t)
        return self._constructive_dilemma

    @property
    def definition_interpretation(self) -> DefinitionInterpretationInclusion:
        """The definition_interpretation inference-rule: 𝒟 ⊢ (P = Q).

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.

        .. include:: ../../include/interpretative_inference_rule_warning.rstinc
        """
        if self._definition_interpretation is None:
            self._definition_interpretation = DefinitionInterpretationInclusion(t=self.t)
        return self._definition_interpretation

    @property
    def destructive_dilemma(self) -> DestructiveDilemmaInclusion:
        """The well-known destructive-dilemma inference-rule

        Abridged property: t.i.cd()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._destructive_dilemma is None:
            self._destructive_dilemma = DestructiveDilemmaInclusion(t=self.t)
        return self._destructive_dilemma

    @property
    def di1(self) -> DisjunctionIntroduction1Inclusion:
        return self.disjunction_introduction_1

    @property
    def di2(self) -> DisjunctionIntroduction2Inclusion:
        return self.disjunction_introduction_2

    @property
    def disjunction_introduction_1(self) -> DisjunctionIntroduction1Inclusion:
        if self._disjunction_introduction_1 is None:
            self._disjunction_introduction_1 = DisjunctionIntroduction1Inclusion(t=self.t)
        return self._disjunction_introduction_1

    @property
    def disjunction_introduction_2(self) -> DisjunctionIntroduction2Inclusion:
        if self._disjunction_introduction_2 is None:
            self._disjunction_introduction_2 = DisjunctionIntroduction2Inclusion(t=self.t)
        return self._disjunction_introduction_2

    @property
    def disjunctive_resolution(self) -> DisjunctiveResolutionInclusion:
        if self._disjunctive_resolution is None:
            self._disjunctive_resolution = DisjunctiveResolutionInclusion(t=self.t)
        return self._disjunctive_resolution

    @property
    def disjunctive_syllogism_1(self) -> DisjunctiveSyllogism1Inclusion:
        if self._disjunctive_syllogism_1 is None:
            self._disjunctive_syllogism_1 = DisjunctiveSyllogism1Inclusion(t=self.t)
        return self._disjunctive_syllogism_1

    @property
    def disjunctive_syllogism_2(self) -> DisjunctiveSyllogism2Inclusion:
        if self._disjunctive_syllogism_2 is None:
            self._disjunctive_syllogism_2 = DisjunctiveSyllogism2Inclusion(t=self.t)
        return self._disjunctive_syllogism_2

    @property
    def dne(self) -> DoubleNegationEliminationInclusion:
        return self.double_negation_elimination

    @property
    def dni(self) -> DoubleNegationIntroductionInclusion:
        return self.double_negation_introduction

    @property
    def double_negation_elimination(self) -> DoubleNegationEliminationInclusion:
        """The well-known double-negation-elimination inference-rule: ¬¬P ⊢ P.

        Abridged property: t.i.dne()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._double_negation_elimination is None:
            self._double_negation_elimination = DoubleNegationEliminationInclusion(t=self.t)
        return self._double_negation_elimination

    @property
    def double_negation_introduction(self) -> DoubleNegationIntroductionInclusion:
        """The well-known double-negation-introduction inference-rule: P ⊢ ¬¬P.

        Abridged property: t.i.dni

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._double_negation_introduction is None:
            self._double_negation_introduction = DoubleNegationIntroductionInclusion(t=self.t)
        return self._double_negation_introduction

    @property
    def ec(self) -> EqualityCommutativityInclusion:
        return self.equality_commutativity

    @property
    def equality_commutativity(self) -> EqualityCommutativityInclusion:
        if self._equality_commutativity is None:
            self._equality_commutativity = EqualityCommutativityInclusion(t=self.t)
        return self._equality_commutativity

    @property
    def equal_terms_substitution(self) -> EqualTermsSubstitutionInclusion:
        if self._equal_terms_substitution is None:
            self._equal_terms_substitution = EqualTermsSubstitutionInclusion(t=self.t)
        return self._equal_terms_substitution

    @property
    def ets(self) -> EqualTermsSubstitutionInclusion:
        return self.equal_terms_substitution

    @property
    def hypothetical_syllogism(self) -> HypotheticalSyllogismInclusion:
        if self._hypothetical_syllogism is None:
            self._hypothetical_syllogism = HypotheticalSyllogismInclusion(t=self.t)
        return self._hypothetical_syllogism

    @property
    def hs(self) -> HypotheticalSyllogismInclusion:
        return self.hypothetical_syllogism

    @property
    def inconsistency_introduction_1(self) -> InconsistencyIntroduction1Inclusion:
        if self._inconsistency_introduction_1 is None:
            self._inconsistency_introduction_1 = InconsistencyIntroduction1Inclusion(t=self.t)
        return self._inconsistency_introduction_1

    @property
    def inconsistency_introduction_2(self) -> InconsistencyIntroduction2Inclusion:
        if self._inconsistency_introduction_2 is None:
            self._inconsistency_introduction_2 = InconsistencyIntroduction2Inclusion(t=self.t)
        return self._inconsistency_introduction_2

    @property
    def inconsistency_introduction_3(self) -> InconsistencyIntroduction3Inclusion:
        if self._inconsistency_introduction_3 is None:
            self._inconsistency_introduction_3 = InconsistencyIntroduction3Inclusion(t=self.t)
        return self._inconsistency_introduction_3

    @property
    def ii1(self) -> InconsistencyIntroduction1Inclusion:
        return self.inconsistency_introduction_1

    @property
    def ii2(self) -> InconsistencyIntroduction2Inclusion:
        return self.inconsistency_introduction_2

    @property
    def ii3(self) -> InconsistencyIntroduction3Inclusion:
        return self.inconsistency_introduction_3

    @property
    def modus_ponens(self) -> ModusPonensInclusion:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P ⊢ Q.

        Abridged property: u.i.mp

        The implication (P ⟹ Q) may contain variables. If such is the
        case, the resulting Q' is computed by extracting variable-values
        from P' and applying variable-substitution.


        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._modus_ponens is None:
            self._modus_ponens = ModusPonensInclusion(t=self.t)
        return self._modus_ponens

    @property
    def modus_tollens(self) -> ModusTollensInclusion:
        if self._modus_tollens is None:
            self._modus_tollens = ModusTollensInclusion(t=self.t)
        return self._modus_tollens

    @property
    def mp(self) -> ModusPonensInclusion:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P ⊢ Q.

        Unabridged property: u.i.modus_ponens

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.modus_ponens

    @property
    def mt(self) -> ModusTollensInclusion:
        return self.tollus_ponens

    @property
    def pbc(self) -> ProofByContradiction1Inclusion:
        """

        Unabridged property: u.i.proof_by_contradiction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.proof_by_contradiction_1

    @property
    def pbr(self) -> ProofByRefutation1Inclusion:
        """

        Unabridged property: u.i.proof_by_refutation

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.proof_by_refutation_1

    @property
    def proof_by_contradiction_1(self) -> ProofByContradiction1Inclusion:
        """

        Abridged property: u.i.pbc

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._proof_by_contradiction_1 is None:
            self._proof_by_contradiction_1 = ProofByContradiction1Inclusion(t=self.t)
        return self._proof_by_contradiction_1

    @property
    def proof_by_contradiction_2(self) -> ProofByContradiction2Inclusion:
        if self._proof_by_contradiction_2 is None:
            self._proof_by_contradiction_2 = ProofByContradiction2Inclusion(t=self.t)
        return self._proof_by_contradiction_2

    @property
    def proof_by_refutation_1(self) -> ProofByRefutation1Inclusion:
        """

        Abridged property: u.i.pbr

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._proof_by_refutation_1 is None:
            self._proof_by_refutation_1 = ProofByRefutation1Inclusion(t=self.t)
        return self._proof_by_refutation_1

    @property
    def proof_by_refutation_2(self) -> ProofByRefutation2Inclusion:
        if self._proof_by_refutation_2 is None:
            self._proof_by_refutation_2 = ProofByRefutation2Inclusion(t=self.t)
        return self._proof_by_refutation_2

    @property
    def variable_substitution(self) -> VariableSubstitutionInclusion:
        """
        """
        if self._variable_substitution is None:
            self._variable_substitution = VariableSubstitutionInclusion(t=self.t)
        return self._variable_substitution

    @property
    def vs(self) -> VariableSubstitutionInclusion:

        return self.variable_substitution


class UniverseOfDiscourse(Formula):
    """This python class models a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    def __init__(self, symbol: (None, str, StyledText) = None, dashed_name: (None, str, StyledText) = None,
        name: (None, str, ComposableText) = None, echo: (None, bool) = None):
        global multiverse
        echo = prioritize_value(echo, configuration.echo_universe_of_discourse_declaration, configuration.echo_default,
            False)
        self._a = AxiomDeclarationAccretor(u=self)
        self._c1 = ConnectiveAccretor(u=self)
        self._c2 = ClassDeclarationAccretor(u=self)
        self._c3 = ConstantDeclarationDict(u=self)
        self._d = DefinitionDeclarationAccretor(u=self)
        self._i = InferenceRuleDeclarationAccretor(u=self)
        self._o = SimpleObjctDict(u=self)
        self._phi = UniverseOfDiscourseFormulaAccretor(u=self)
        self._simple_objcts = SimpleObjctDict(u=self)
        self._symbolic_objects = UniverseOfDiscourseSymbolicObjectAccretor(u=self)
        self._t = TheoryDerivationDeclarationAccretor(u=self)
        # self.variables = dict()
        # Unique name indexes
        # self.symbol_indexes = dict()
        # self.titles = dict()
        self._metatheory = None
        symbol = prioritize_value(symbol, StyledText(plaintext='U', text_style=text_styles.script_normal))
        dashed_name = prioritize_value(symbol,
            StyledText(plaintext='universe-of-discourse-', text_style=text_styles.serif_italic))
        index = prioritize_value(symbol, index_universe_of_discourse_symbol(base=symbol))
        super().__init__(is_universe_of_discourse=True, is_theory_foundation_system=False, u=None, echo=False)
        multiverse.create_instance(u=self)
        # super()._declare_class_membership_OBSOLETE(classes_OBSOLETE.universe_of_discourse)
        if echo:
            self.echo()

    @property
    def a(self) -> AxiomDeclarationAccretor:
        """The collection of axioms declared in this universe-of-discourse."""
        return self._a

    @property
    def c1(self) -> ConnectiveAccretor:
        """A python dictionary of connectives contained in this universe-of-discourse,
        where well-known connectives are directly available as properties."""
        return self._c1

    @property
    def c2(self) -> ClassDeclarationAccretor:
        """The collection of classes declared in this universe-of-discourse."""
        return self._c2

    @property
    def c3(self) -> ConstantDeclarationDict:
        """The collection of constants declared in this universe-of-discourse."""
        return self._c3

    def compose_class(self) -> collections.abc.Generator[Composable, Composable, bool]:
        yield SerifItalic(plaintext='universe-of-discourse')
        return True

    def compose_creation(self) -> collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        yield SansSerifNormal('Let ')
        yield text_dict.open_quasi_quote
        yield from self.nameset.compose_symbol()
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be a ')
        yield from self.compose_class()
        # TODO: UniverseOfDiscourse.compose_creation: adapt the method for universe declaration to add "in Ux", referencing the parent / meta universe.
        yield text_dict.period
        return True

    def cross_reference_constant_OBSOLETE(self, c: ConstantDeclaration) -> bool:
        """Cross-references a constant in this universe-of-discourse.

        :parameter c: a constant-declaration.
        """
        if c not in self.c3:
            self.c3[c.nameset] = c
            return True
        else:
            return False

    @property
    def d(self) -> DefinitionDeclarationAccretor:
        """The collection of axioms declared in this universe-of-discourse."""
        return self._d

    def declare_compound_formula(self, connective: Connective, *terms, lock_variable_scope: (None, bool) = None,
        symbol: (None, str, StyledText) = None, index: (None, int) = None, auto_index: (None, bool) = None,
        echo: (None, bool) = None):
        """Declare a new formula in this universe-of-discourse.

        This method is a shortcut for Formula(universe_of_discourse=self, . . d.).

        A formula is *declared* in a theory, and not *stated*, because it is not a statement,
        i.e. it is not necessarily true in this theory.
        """
        phi = CompoundFormula(connective=connective, terms=terms, u=self, lock_variable_scope=lock_variable_scope,
            symbol=symbol, index=index, auto_index=auto_index, echo=echo)
        return phi

    def declare_variable(self, symbol: (None, str, StyledText) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        is_strictly_propositional: (None, bool) = None, echo: (None, bool) = None):
        """Declare a variable in this universe-of-discourse.

        A shortcut function for FreeVariable(universe_of_discourse=u, ...)

        :param symbol:
        :return:
        """
        x = FreeVariable(u=self, symbol=symbol, status=FreeVariable.scope_initialization_status,
            is_strictly_propositional=is_strictly_propositional, echo=echo)
        return x

    def declare_symbolic_objct(self, symbol: (None, str, StyledText) = None, index: (None, int, str) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        nameset: (None, str, NameSet) = None, echo: (None, bool) = None) -> SymbolicObject:
        return SymbolicObject(u=self, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, echo=echo)

    def declare_theory(self, symbol: (None, str, StyledText) = None, index: (None, int, str) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str) = None, name: (None, str) = None,
        explicit_name: (None, str) = None, ref: (None, str) = None, subtitle: (None, str) = None,
        extended_theory: (None, TheoryDerivation) = None, extended_theory_limit: (None, Statement) = None,
        stabilized: bool = False, echo: bool = None):
        """Declare a new theory in this universe-of-discourse.

        Shortcut for Theory(u, ...).

        :param nameset:
        :param is_theory_foundation_system:
        :param extended_theory:
        :return:
        """
        return TheoryDerivation(u=self, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            name=name, explicit_name=explicit_name, ref=ref, subtitle=subtitle, extended_theory=extended_theory,
            extended_theory_limit=extended_theory_limit, stabilized=stabilized, echo=echo)

    def echo(self):
        return repm.prnt(self.rep_creation(cap=True))

    @property
    def i(self) -> InferenceRuleDeclarationAccretor:
        """The (possibly empty) collection of :ref:`inference-rules<inference_rule_math_concept>` declared in this in this :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .

        Abridged name: i
        """
        return self._i

    @property
    def is_strictly_propositional(self) -> bool:
        return False

    @property
    def metatheory(self) -> PunctiliousMinimalMetatheory:
        """A minimal metatheory for this universe-of-discourse."""
        if self._metatheory is None:
            self._metatheory = PunctiliousMinimalMetatheory(u=self)

        return self._metatheory

    @property
    def o(self) -> SimpleObjctDict:
        """The (possibly empty) collection of simple-objects declared in this in this universe-of-discourse.

        Unabridged name: simple_objcts

        Well-known simple-objcts are exposed as python properties. In general, a well-known
        simple-objct is declared in the universe-of-discourse the first time its property is
        accessed.
        """
        return self._o

    @property
    def phi(self) -> UniverseOfDiscourseFormulaAccretor:
        return self._phi

    def rep_creation(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        return rep_composition(composition=self.compose_creation(), encoding=encoding, cap=cap)

    @property
    def simple_objcts(self) -> SimpleObjctDict:
        """The collection of simple-objcts in this universe-of-discourse.

        Abridged version: u.o

        Well-known simple-objcts are exposed as python properties. In general, a well-known
        simple-objct is declared in the universe-of-discourse the first time its property is
        accessed.

        :return:
        """
        return self._simple_objcts

    def so(self, symbol=None):
        return self.declare_symbolic_objct(symbol=symbol)

    @property
    def symbolic_objects(self) -> UniverseOfDiscourseSymbolicObjectAccretor:
        """The collection of axioms declared in this universe-of-discourse."""
        return self._symbolic_objects

    def take_note(self, t: TheoryDerivation, content: str, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
        subtitle: (None, str, StyledText) = None, echo: (None, bool) = None):
        """Take a note, make a comment, or remark."""
        verify(t.u is self, 'This universe-of-discourse 𝑢₁ (self) is distinct from the universe-of-discourse 𝑢₂ '
                            'of the theory '
                            'term 𝑡.')

        return NoteInclusion(t=t, content=content, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, echo=echo)

    @property
    def t(self) -> TheoryDerivationDeclarationAccretor:
        """The collection of theory-derivations declared in this universe-of-discourse."""
        return self._t

    # @FreeVariableContext()
    @contextlib.contextmanager
    def with_variable(self, symbol: (None, str, StyledText) = None, index: (None, int) = None,
        auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None, echo: (None, bool) = None):
        """Declare a variable in this universe-of-discourse.

        This method is expected to be as in a with statement,
        it yields an instance of FreeVariable,
        and automatically lock the variable scope when the with left.

        Example: with u.v('x') as x, u.v('y') as y:
        some code...

        To manage variable scope extensions and locking expressly,
        use declare_variable() instead.
        """
        status = FreeVariable.scope_initialization_status
        x = FreeVariable(u=self, status=status, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo)
        yield x
        x.lock_scope()


def create_universe_of_discourse(name: (None, str, ComposableText) = None,
    echo: (None, bool) = None) -> UniverseOfDiscourse:
    """Create a new universe of discourse.
    """
    return UniverseOfDiscourse(name=name, echo=echo)


class InferredStatement(FormulaStatement):
    """A statement inferred from an inference-rule in the current theory-elaboration.
    """

    def __init__(self, i: InferenceRuleInclusion, premises: typing.NamedTuple, symbol: (None, str, StyledText) = None,
        index: (None, int) = None, auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
        acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
        name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
        ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
        paragraph_header: (None, ParagraphHeader) = None, echo: (None, bool) = None, echo_proof: (None, bool) = None):
        """Include (aka allow) an inference_rule in a theory-elaboration.
        """
        echo = prioritize_value(echo, configuration.echo_inferred_statement, configuration.echo_statement,
            configuration.echo_default, False)
        t: TheoryDerivation = i.t
        self._inference_rule = i
        # Verify if premises are syntaxically correct, and construct the resulting formula at the same time.
        # If syntaxically incorrect, raise a Punctilious Exception and stop processing.
        # If syntaxically correct, complete the inference process.
        valid_proposition = self._inference_rule.construct_formula(**premises._asdict())
        # Check if the premises are valid.
        # If they are not, raise a Punctilious Exception and stop processing.
        # If they are, complete the inference process.
        # Note that the newly returned premises object will be correctly typed,
        # i.e. valid formulae were replaced with formula-statements.
        ok: bool
        ok, premises = self._inference_rule.check_premises_validity(**premises._asdict())
        self._premises = premises
        super().__init__(theory=t, valid_proposition=valid_proposition, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle, paragraphe_header=paragraph_header, echo=False)
        # super()._declare_class_membership_OBSOLETE(declarative_class_list_OBSOLETE.inferred_proposition)
        if self.valid_proposition.connective is self.t.u.c1.inconsistency and is_derivably_member_of_class(u=self.u,
            phi=self.valid_proposition.terms[0], c=self.u.c2.theory_derivation):
            # This inferred-statement proves the inconsistency of its argument,
            # its argument is a theory-derivation (i.e. it is not a variable),
            # it follows that we must change the consistency attribute of that theory.
            inconsistent_theory: TheoryDerivation
            inconsistent_theory = self.valid_proposition.terms[0]
            inconsistent_theory.report_inconsistency_proof(proof=self)
        if echo:
            self.echo(proof=echo_proof)
        if self.inference_rule is self.t.u.i.axiom_interpretation or self.inference_rule is self.t.u.i.definition_interpretation:
            t.assure_interpretation_disclaimer(echo=echo)

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='inferred-statement')

    def compose_report(self, proof: (None, bool) = None, **kwargs):
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_inferred_statement_report(o=self, proof=proof)
        return output

    def echo(self, proof: (None, bool) = None):
        proof = prioritize_value(proof, configuration.echo_proof, True)
        repm.prnt(self.rep_report(proof=proof))

    @property
    def is_strictly_propositional(self) -> bool:
        """By definition, an inferred statement is propositional."""
        return True

    @property
    def terms(self) -> tuple:
        return self._premises

    @property
    def inference_rule(self) -> InferenceRuleDeclaration:
        """Return the inference-rule upon which this inference-rule-inclusion is based.
        """
        return self._inference_rule


def rep_two_columns_proof_item(left: str, right: str) -> str:
    """Format a two-columns proof row.
    TODO: Implement logic for plaintext, unicode and latex.
    """
    left_column_width = prioritize_value(configuration.two_columns_proof_left_column_width, 67)
    right_column_width = prioritize_value(configuration.two_columns_proof_right_column_width, 30)
    report = textwrap.wrap(text=left, width=left_column_width, break_on_hyphens=False)
    report = [line.ljust(left_column_width, ' ') + ' | ' for line in report]
    report[len(report) - 1] = report[len(report) - 1] + right
    report = '\n'.join(report)
    return report + '\n'


def rep_two_columns_proof_end(left: str) -> str:
    """Format the end of a two-columns proof
    TODO: Implement logic for plaintext, unicode and latex.
    """
    left_column_width = prioritize_value(configuration.two_columns_proof_left_column_width, 67)
    right_column_width = prioritize_value(configuration.two_columns_proof_right_column_width, 30)
    report = ''.ljust(left_column_width + 1, '─') + '┤ ' + '\n'
    report = report + rep_two_columns_proof_item(left=left, right='∎')
    return report


def apply_negation(phi: CompoundFormula) -> CompoundFormula:
    """Apply negation to a formula phi."""
    return phi.u.declare_compound_formula(phi.u.c1.lnot, phi.u.declare_compound_formula(phi.u.c1.lnot, phi))


def apply_double_negation(phi: CompoundFormula) -> CompoundFormula:
    """Apply double-negation to a formula phi."""
    return apply_negation(apply_negation(phi))


class InconsistencyIntroductionStatement(FormulaStatement):
    """

    Requirements:
    -------------

    """

    def __init__(self, p, not_p, nameset=None, paragraphe_header=None, theory=None, title=None):
        if title is None:
            title = 'THEORY INCONSISTENCY'
        paragraphe_header = paragraph_headers.proposition if paragraphe_header is None else paragraphe_header
        self.p = p
        self.not_p = not_p
        valid_proposition = InconsistencyIntroductionInferenceRuleOBSOLETE.execute_algorithm(theory=theory, p=p,
            not_p=not_p)
        super().__init__(theory=theory, valid_proposition=valid_proposition, paragraphe_header=paragraphe_header,
            title=title, nameset=nameset)
        # The theory is proved inconsistent!
        theory.prove_inconsistent(self)
        if configuration.warn_on_inconsistency:
            warnings.warn(f'{self.rep_report(proof=True)}', InconsistencyWarning)

    def rep_report(self, proof: (None, bool) = None):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.rep_title(cap=True)}: {self.valid_proposition.rep_formula()}'
        if proof:
            output = output + f'\n\t{repm.serif_bold("Proof of inconsistency")}'
            output = output + f'\n\t{self.p.rep_formula(expand=True):<70} │ Follows from ' \
                              f'{repm.serif_bold(self.p.rep_ref())}.'
            output = output + f'\n\t{self.not_p.rep_formula(expand=True):<70} │ Follows from ' \
                              f'{repm.serif_bold(self.not_p.rep_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.rep_formula(expand=True):<70} │ ∎'
        return output + f'\n'


def reset_configuration(configuration: Configuration) -> None:
    configuration.auto_index = None
    configuration._echo_default = False
    configuration.default_axiom_declaration_symbol = ScriptNormal('A')
    configuration.default_axiom_inclusion_symbol = SerifItalic('A')
    configuration.default_constant_symbol = SerifNormal(plaintext='c', unicode='c')
    configuration.default_definition_declaration_symbol = ScriptNormal('D')
    configuration.default_definition_inclusion_symbol = SerifItalic('D')
    configuration.default_formula_symbol = SerifItalic(plaintext='phi', unicode='𝜑')
    configuration.default_variable_symbol = StyledText(plaintext='x', text_style=text_styles.serif_bold)
    configuration.default_parent_hypothesis_statement_symbol = SerifItalic('H')
    configuration.default_child_hypothesis_theory_symbol = ScriptNormal('H')
    configuration.default_inference_rule_declaration_symbol = SerifItalic('I')
    configuration.default_inference_rule_inclusion_symbol = SerifItalic('I')
    configuration.default_note_symbol = SerifItalic('note')
    configuration.default_connective_symbol = SerifItalic('r')
    configuration.default_statement_symbol = SerifItalic('P')
    configuration.default_symbolic_object_symbol = SerifItalic('o')
    configuration.default_theory_symbol = ScriptNormal('T')
    configuration.echo_axiom_declaration = False
    configuration.echo_axiom_inclusion = True
    configuration.echo_declaration = None
    configuration.echo_definition_declaration = False
    configuration.echo_definition_inclusion = True
    configuration.echo_definition_direct_inference = None
    configuration.echo_encoding = None
    configuration.echo_formula_declaration = False  # In general, this is too verbose.
    configuration.echo_variable_declaration = False
    configuration.echo_hypothesis = None
    configuration.echo_inclusion = None
    configuration.echo_inference_rule_declaration = False
    configuration.echo_inference_rule_inclusion = True
    configuration.echo_inferred_statement = True
    configuration.echo_note = True
    configuration.echo_proof = True
    configuration.echo_connective = None
    configuration.echo_simple_objct_declaration = None
    configuration.echo_statement = True
    configuration.echo_symbolic_objct = None
    configuration.echo_theory_derivation_declaration = None
    configuration.echo_universe_of_discourse_declaration = None
    configuration.output_index_if_max_index_equal_1 = False
    configuration.raise_exception_on_verification_error = True
    configuration.title_text_style = text_styles.sans_serif_bold
    configuration.encoding = encodings.unicode
    configuration.text_output_indent = 2
    configuration.two_columns_proof_left_column_width = 67
    configuration.two_columns_proof_right_column_width = 30
    configuration.text_output_total_width = 100
    configuration.warn_on_inconsistency = True


reset_configuration(configuration=configuration)


class TheoryPackage:
    def __init__(self, u: UniverseOfDiscourse):
        self._u = u

    @property
    def u(self) -> UniverseOfDiscourse:
        return self._u


class PunctiliousMinimalMetatheory(TheoryPackage):
    """A minimal metatheory for universe-of-discourses and classes."""

    def __init__(self, u: (None, UniverseOfDiscourse) = None):
        if u is None:
            u = UniverseOfDiscourse()
        super().__init__(u=u)
        # Naming conventions in MGZ21
        t = self.u.t.declare(symbol='minimal-metatheory', index=0, dashed_name='minimal-metatheory',
            name='minimal metatheory', explicit_name='punctilious_obsolete_20240114 minimal metatheory')
        self._t = t

        # Axiom: a1
        a1_natural_language = """When an object is declared in the universe-of-discourse, it may be assigned some 
        classes. In such circumstances, we say that the object is declaratively a member of that class. Usually this is 
        introduced by some written statement such as 'Let x be a c1, c2, ..., cn.' where x 
        is a designation for the newly declared object, and c1, c2, ..., cn are designations of the classes assigned 
        to the object. When an object x has been declared and assigned a class c, it follows that the statement x 
        is-a c is a valid statement."""
        self._a1_declaration = u.a.declare(symbol='a', index=1, natural_language=a1_natural_language)
        self._a1_inclusion = t.include_axiom(symbol='a', index=1, a=self._a1_declaration)

        t.take_note('While the positive statement x is-a c is valid if the object x was declared and assigned the '
                    'class c, note that it is not possible to infer that not(x is-a c) if the object x was declared '
                    'and not assigned class c. In effect, it may be the case that object x is still a member of c'
                    'but not because it was declared as such, but by theoretical derivation.')

    @property
    def a1(self) -> AxiomInclusion:
        return self._a1_inclusion

    @property
    def t(self) -> TheoryDerivation:
        return self._t


class Article:
    """TODO: Article: for future development."""

    def __init__(self):
        self._elements = []

    def write_element(self, element: SymbolicObject):
        self._elements.append(element)


class DeclarativeClassList_OBSOLETE(repm.ValueName):
    """The idea of this class is to expose programmatically the data-model of punctilious_obsolete_20240114. To be reworked, this is messy.

    TODO: Replace this class with the new minimal-metatheory approach.
    """

    def __init__(self, name, natural_language_name):
        super().__init__(name)
        self.atheoretical_statement = DeclarativeClass_OBSOLETE('atheoretical_statement', 'atheoretical-statement',
            python_type=AtheoreticalStatement)
        self.axiom_inclusion = DeclarativeClass_OBSOLETE('axiom_inclusion', 'axiom-inclusion',
            python_type=AxiomInclusion)
        self.constant_declaration = DeclarativeClass_OBSOLETE('constant_declaration', 'constant-declaration',
            python_type=ConstantDeclaration)
        self.definition_inclusion = DeclarativeClass_OBSOLETE('definition_inclusion', 'definition-inclusion',
            python_type=DefinitionInclusion)
        self.axiom_interpretation_declaration = DeclarativeClass_OBSOLETE('axiom_interpretation_declaration',
            'axiom-interpretation-declaration', python_type=AxiomInterpretationDeclaration)
        self.axiom_interpretation_inclusion = DeclarativeClass_OBSOLETE('axiom_interpretation_inclusion',
            'axiom-interpretation-inclusion', python_type=AxiomInterpretationInclusion)
        self.direct_definition_inference = DeclarativeClass_OBSOLETE('direct_definition_inference',
            'direct-definition-inference')
        self.compound_formula = DeclarativeClass_OBSOLETE('compound_formula', 'compound-formula',
            python_type=CompoundFormula)
        self.formula_statement = DeclarativeClass_OBSOLETE('formula_statement', 'formula-statement',
            python_type=FormulaStatement)
        self.variable = DeclarativeClass_OBSOLETE('variable', 'variable', python_type=FreeVariable)
        self.hypothesis = DeclarativeClass_OBSOLETE('hypothesis', 'hypothesis', python_type=Hypothesis)
        self.inference_rule_inclusion = DeclarativeClass_OBSOLETE('inference_rule_inclusion',
            'inference-rule-inclusion')
        self.inferred_proposition = DeclarativeClass_OBSOLETE('inferred_proposition', 'inferred-proposition')
        self.note = DeclarativeClass_OBSOLETE('note', 'note')
        self.proposition = DeclarativeClass_OBSOLETE('proposition', 'proposition')
        self.simple_objct = DeclarativeClass_OBSOLETE('simple_objct', 'simple-objct', python_type=SimpleObjct)
        self.statement = DeclarativeClass_OBSOLETE('statement', 'statement')
        self.symbolic_objct = DeclarativeClass_OBSOLETE('symbolic_objct', 'symbolic-objct')
        self.formula = DeclarativeClass_OBSOLETE('formula', 'formula', python_type=Formula)
        # Shortcuts
        self.dai = self.axiom_interpretation_declaration
        self.ddi = self.direct_definition_inference
        self.f = self.compound_formula


"""A list of well-known declarative-classes."""
declarative_class_list_OBSOLETE = DeclarativeClassList_OBSOLETE('declarative_class_list', 'declarative-class-list')

"""A list of well-known declarative-classes. A shortcut for p.declarative_class_list."""
classes_OBSOLETE = declarative_class_list_OBSOLETE

pass
