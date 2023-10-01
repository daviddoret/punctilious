from __future__ import annotations
import dataclasses
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


# import punctilious.caller_info as caller_info


def prioritize_value(*args):
    """Return the first non-None object in ⌜*args⌝."""
    for a in args:
        if a is not None:
            return a
    return None


class PunctiliousException(Exception):
    def __init__(self, msg, **kwargs):
        self.msg = msg
        self.kwargs = kwargs


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
                representation = representation + rep_composition(composition=item,
                    encoding=encoding, cap=cap, **kwargs)
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
            elif isinstance(item, Formula):
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
            other) and self.plaintext == other.plaintext and self.unicode == other.unicode and self.latex == other.latex

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
        post: (None, str, Composable) = None) -> collections.abc.Generator[
    Composable, Composable, bool]:
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
        post: (None, str, Composable) = None) -> collections.abc.Generator[
    Composable, Composable, bool]:
    """Yield the composition of the first non-None element of *content.
    """
    if content is None:
        return False
    first_not_none = next((element for element in content if element is not None), None)
    something = yield from yield_composition(first_not_none, cap=cap, pre=pre, post=post)
    return something


class TextStyle:
    """A supported text style."""

    def __init__(self, name: str, start_tag: ComposableText, end_tag: ComposableText,
            unicode_map: dict = None, unicode_table_index: int = None):
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
        self.monospace = TextStyle(name='fraktur-normal',
            unicode_table_index=unicode_utilities.unicode_fraktur_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathfrak{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.monospace = TextStyle(name='monospace',
            unicode_table_index=unicode_utilities.unicode_monospace_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathtt{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.sans_serif_bold = TextStyle(name='sans-serif-bold',
            unicode_table_index=unicode_utilities.unicode_sans_serif_bold_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\boldsymbol\\mathsf{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}}'))
        self.sans_serif_italic = TextStyle(name='sans-serif-italic',
            unicode_table_index=unicode_utilities.unicode_sans_serif_italic_index,
            start_tag=ComposableText(plaintext='', unicode='',
                latex='\\text{\\sffamily{\\itshape{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}}}'))
        self.sans_serif_normal = TextStyle(name='sans-serif-normal',
            unicode_table_index=unicode_utilities.unicode_sans_serif_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathsf{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.script_normal = TextStyle(name='script-normal',
            unicode_table_index=unicode_utilities.unicode_script_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathcal{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.serif_bold = TextStyle(name='serif-bold',
            unicode_table_index=unicode_utilities.unicode_serif_bold_index,
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
        self.subscript = TextStyle(name='subscript',
            unicode_map=unicode_utilities.unicode_subscript_dictionary,
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
        self.close_quasi_quote = ComposableText(plaintext='"', unicode='⌝',
            latex='\\right\\ulcorner')
        self.open_quasi_quote = ComposableText(plaintext='"', unicode='⌜', latex='\\left\\ulcorner')
        self.close_parenthesis = ComposableText(plaintext=')', latex='\\right)')
        self.open_parenthesis = ComposableText(plaintext='(', latex='\\left(')
        self.formula_parameter_separator = ComposableText(plaintext=', ')
        self.the = None


text_dict = TextDict()


class ComposableBlock(Composable, abc.ABC):
    """A CompositionBlock is a composition that has a start_tag and an end_tag."""

    def __init__(self, start_tag: (None, ComposableText) = None,
            end_tag: (None, ComposableText) = None):
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

    def __init__(self, content: (None, ComposableText) = None,
            start_tag: (None, ComposableText) = None, end_tag: (None, ComposableText) = None):
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
            plaintext: (None, str, Plaintext) = None, unicode: (None, str, Unicode2) = None,
            latex: (None, str) = None, cap: (None, bool) = None):
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
        return type(self) is type(
            other) and self._content == other.content and self._text_style is other.text_style

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
        if (cap is not None and cap != self._cap) or (
                text_style is not None and self._text_style is not text_style):
            # Return a close of ⌜self⌝ with the desired properties.
            # TODO: StyledText composition: possible bug in LaTeX rendering here.
            latex = None if self.latex is None else (self.latex.capitalize() if cap else self.latex)
            plaintext = None if self.plaintext is None else (
                self.plaintext.capitalize() if cap else self.plaintext)
            unicode = None if self.unicode is None else (
                self.unicode.capitalize() if cap else self.unicode)
            yield StyledText(latex=latex, plaintext=plaintext, unicode=unicode,
                text_style=self.text_style)
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
        return unicode_utilities.unicode_format(s=content,
            index=self.text_style._unicode_table_index, mapping=self.text_style.unicode_map)

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
        super().__init__(content=iterable, start_tag=Paragraph._static_start_tag,
            end_tag=Paragraph._static_end_tag)

    _static_end_tag = ComposableText(plaintext='\n\n', unicode='\n\n')

    _static_start_tag = ComposableText(plaintext='', unicode='')


class Index(ComposableBlockSequence):
    def __init__(self, iterable: (None, collections.Iterable) = None) -> None:
        super().__init__(iterable=iterable, start_tag=Paragraph._static_start_tag,
            end_tag=Paragraph._static_end_tag)

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
                return ComposableText(plaintext=item,
                    unicode=unicode_utilities.unicode_subscriptify(s=item))
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
        super().__init__(s=s, text_style=text_styles.sans_serif_bold, plaintext=plaintext,
            unicode=unicode, latex=latex)


class Header(ComposableBlockSequence):
    def __init__(self, s: (str, None) = None, plaintext: (None, str, Plaintext) = None,
            unicode: (None, str, Unicode2) = None, latex: (None, str) = None,
            level: (None, int) = None) -> None:
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
            start_tag = ComposableText(plaintext='\n### ', unicode='\n### ',
                latex='\\subsubsection{')
            end_tag = ComposableText(plaintext='\n', unicode='\n', latex='}')
        super().__init__(content=[content], start_tag=start_tag, end_tag=end_tag)

    @property
    def level(self) -> int:
        return self.level


class SansSerifNormal(StyledText):
    def __init__(self, s: (str, None) = None, plaintext: (None, str, Plaintext) = None,
            unicode: (None, str, Unicode2) = None, latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.sans_serif_normal, plaintext=plaintext,
            unicode=unicode, latex=latex)


class SansSerifItalic(StyledText):
    def __init__(self, s: (str, None) = None, plaintext: (None, str, Plaintext) = None,
            unicode: (None, str, Unicode2) = None, latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.sans_serif_italic, plaintext=plaintext,
            unicode=unicode, latex=latex)


text_dict.in2 = SansSerifNormal(s='in')
text_dict.let = SansSerifNormal(s='let')
text_dict.be = SansSerifNormal(s='be')
text_dict.be_a = SansSerifNormal(s='be a')
text_dict.be_an = SansSerifNormal(s='be an')
text_dict.the = SansSerifNormal(s='the')


class ScriptNormal(StyledText):
    def __init__(self, plaintext: str, unicode: (None, str) = None,
            latex: (None, str) = None) -> None:
        super().__init__(text_style=text_styles.script_normal, plaintext=plaintext, unicode=unicode,
            latex=latex)


class SerifBoldItalic(StyledText):
    def __init__(self, s: (None, str) = None, plaintext: (None, str) = None,
            unicode: (None, str) = None, latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.serif_bold_italic, plaintext=plaintext,
            unicode=unicode, latex=latex)


class SerifItalic(StyledText):
    def __init__(self, s: (None, str) = None, plaintext: (None, str) = None,
            unicode: (None, str) = None, latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.serif_italic, plaintext=plaintext,
            unicode=unicode, latex=latex)


class SerifNormal(StyledText):
    def __init__(self, plaintext: str, unicode: (None, str) = None,
            latex: (None, str) = None) -> None:
        super().__init__(text_style=text_styles.serif_normal, plaintext=plaintext, unicode=unicode,
            latex=latex)


class Subscript(StyledText):
    def __init__(self, plaintext: str, unicode: (None, str) = None,
            latex: (None, str) = None) -> None:
        super().__init__(text_style=text_styles.subscript, plaintext=plaintext, unicode=unicode,
            latex=latex)


def wrap_text(text):
    """Wrap text for friendly rendering as text, e.g. in a console.

    :param text:
    :return:
    """
    return '\n'.join(textwrap.wrap(text=text, width=configuration.text_output_total_width,
        subsequent_indent=f'\t', break_on_hyphens=False, expand_tabs=True, tabsize=4))


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


def verify(assertion, msg, severity: VerificationSeverity = verification_severities.error,
        raise_exception: bool = True, **kwargs) -> tuple[bool, (None, str)]:
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
            contextual_information += f'\n{key}: {value_as_string}'
        report = f'{str(severity).upper()}: {msg}\nContextual information:{contextual_information}'
        repm.prnt(report)
        if severity is verification_severities.warning:
            warnings.warn(report)
        raise_exception = prioritize_value(raise_exception,
            configuration.raise_exception_on_verification_error, True)
        if severity is verification_severities.error:
            if raise_exception:
                raise PunctiliousException(msg=report, **kwargs)
            else:
                return False, report
    else:
        return True, None


class InconsistencyWarning(UserWarning):
    pass


class Configuration:
    """Configuration settings.

    This class allows the storage of all punctilious configuration and preference settings.

    """

    def __init__(self):
        self.auto_index = None
        self.default_axiom_declaration_symbol = None
        self.default_axiom_inclusion_symbol = None
        self.default_definition_declaration_symbol = None
        self.default_definition_inclusion_symbol = None
        self.default_formula_symbol = None
        self.default_free_variable_symbol = None
        self.default_parent_hypothesis_statement_symbol = None
        self.default_child_hypothesis_theory_symbol = None
        self.default_inference_rule_declaration_symbol = None
        self.default_inference_rule_inclusion_symbol = None
        self.default_note_symbol = None
        self.default_relation_symbol = None
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
        self.echo_relation = None
        self.echo_simple_objct_declaration = None
        self.echo_statement = None
        self.echo_proof = None
        self.echo_symbolic_objct = None
        self.echo_theory_elaboration_sequence_declaration = None
        self.echo_universe_of_discourse_declaration = None
        self.echo_free_variable_declaration = None
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


def unpack_formula(o: (TheoreticalObject, Formula, FormulaStatement)) -> Formula:
    """Receive a theoretical-objct and unpack its formula if it is a statement that contains a
    formula."""
    verify(is_in_class(o, classes.theoretical_objct),
        'Parameter ⌜o⌝ must be an element of the theoretical-objct declarative-class.', o=o)
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


def is_in_class(o: TheoreticalObject, c: DeclarativeClass) -> bool:
    """Return True if o is a member of the declarative-class c, False otherwise.

    :param o: An arbitrary python object.
    :param c: A declarative-class.
    :return: (bool).
    """
    verify(o is not None, 'o is None.', o=o, c=c)
    # verify(hasattr(o, 'is_in_class'), 'o does not have attribute is_in_class.', o=o, c=c)
    verify(callable(getattr(o, 'is_in_class')), 'o.is_in_class() is not callable.', o=o, c=c)
    return o.is_in_class(c)


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

    TODO: Enhancement: for relations in particular, add a verb NameType (e.g. implies).
    """

    def __init__(self, s: (None, str) = None, symbol: (None, str, StyledText) = None,
            index: (None, int, str, ComposableText) = None,
            namespace: (None, SymbolicObject) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str) = None,
            subtitle: (None, str, ComposableText) = None):
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
        self._dashed_name = dashed_name if isinstance(dashed_name, StyledText) else StyledText(
            s=dashed_name, text_style=text_styles.serif_italic) if isinstance(dashed_name,
            str) else None
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
        return type(self) is type(
            other) and self.symbol == other.symbol and self.index == other.index

    def __hash__(self):
        return hash((NameSet, self.symbol, self.index))

    def __repr__(self):
        return self.rep_symbol()

    def __str__(self):
        return self.rep_symbol()

    @property
    def acronym(self) -> ComposableText:
        return self._acronym

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

    def compose(self, pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        something = yield from self.compose_symbol(pre=pre, post=post)
        return something

    def compose_accurate_name(self, cap: (None, bool) = None, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Composes the most least unambiguous natural-language name in the nameset.
        """
        something = yield from yield_composition(
            prioritize_value(self._explicit_name, self._name, self._abridged_name, self._acronym),
            cap=cap, pre=pre, post=post)
        return something

    def compose_abridged_name(self, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        if self._abridged_name is None:
            return False
        else:
            something = yield from yield_composition(self._abridged_name, pre=pre, post=post)
            return something

    def compose_acronym(self, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        if self._acronym is None:
            return False
        else:
            something = yield from yield_composition(self._acronym, pre=pre, post=post)
            return something

    def compose_paragraph_header_unabridged(self, cap: (None, bool) = None,
            pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        if self._paragraph_header is None:
            return False
        else:
            something = yield from yield_composition(self.paragraph_header.natural_name, cap=cap,
                pre=pre, post=post)
            return something

    def compose_paragraph_header_abridged(self, cap: (None, bool) = None,
            pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        if self._paragraph_header is None:
            return False
        else:
            something = yield from yield_composition(self._paragraph_header.abridged_name, cap=cap,
                pre=pre, post=post)
            return something

    def compose_compact_name(self, cap: (None, bool) = None, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Composes the most compact / shortest name in the nameset.
        """
        something = yield from yield_composition(
            prioritize_value(self._abridged_name, self._acronym, self._name, self._explicit_name),
            cap=cap, pre=pre, post=post)
        return something

    def compose_conventional_name(self, cap: (None, bool) = None,
            pre: (None, str, Composable) = None, post: (None, str, Composable) = None) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        """Composes the most conventional / frequently-used name in the nameset.
        """
        something = yield from yield_composition(
            prioritize_value(self._name, self._abridged_name, self._acronym, self._explicit_name),
            cap=cap, pre=pre, post=post)
        return something

    def compose_dashed_name(self, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        if self._dashed_name is None:
            return False
        else:
            something = yield from yield_composition(self._dashed_name, pre=pre, post=post)
            return something

    def compose_explicit_name(self, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        if self._explicit_name is None:
            return False
        else:
            something = yield from yield_composition(self._explicit_name, pre=pre, post=post)
            return something

    def compose_index(self, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        if self._symbol is None:
            return False
        else:
            something = yield from yield_composition(self._index, pre=pre, post=post)
            return something

    def compose_name(self, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        if self._name is None:
            return False
        else:
            something = yield from yield_composition(self._name, pre=pre, post=post)
            return something

    def compose_qualified_symbol(self, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
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

    def compose_ref(self, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, None, None]:
        if self._ref is None:
            return False
        else:
            something = yield from yield_composition(self._ref, pre=pre, post=post)
            return something

    def compose_ref_link(self, cap: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        global text_dict
        output1 = yield from self.compose_paragraph_header_abridged(cap=cap)
        pre = text_dict.space if output1 else None
        output2 = yield from self.compose_ref(pre=pre)
        pre = ' (' if output1 or output2 else None
        post = ')' if output1 or output2 else None
        output3 = yield from self.compose_symbol(pre=pre, post=post)
        return True

    def compose_subtitle(self, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        if self._subtitle is None:
            return False
        else:
            something = yield from yield_composition(self._subtitle, pre=pre, post=post)
            return something

    def compose_symbol(self, pre: (None, str, Composable) = None,
            post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        if self._symbol is None:
            return False
        else:
            something = yield from yield_composition(self._symbol, self.compose_index(), pre=pre,
                post=post)
            return something

    def compose_title(self, cap: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
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
    def explicit_name(self) -> ComposableText:
        return self._explicit_name

    @property
    def index(self) -> str:
        return self._index

    @property
    def index_as_int(self) -> int:
        """Especially for auto-indexing purposes, exposes the index as an int if it is an int."""
        return self._index_as_int

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

    def rep_abridged_name(self, cap: (None, bool) = None, encoding: (None, Encoding) = None) -> (
            None, str):
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
        return rep_composition(composition=self.compose_conventional_name(), encoding=encoding,
            cap=cap)

    def rep_dashed_name(self, encoding: (None, Encoding) = None, compose: bool = False) -> (
            None, str):
        return rep_composition(composition=self.compose_dashed_name(), encoding=encoding)

    def rep_explicit_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> (
            None, str):
        """Return a string that represent the object as an explicit name."""
        return rep_composition(composition=self.compose_explicit_name(), encoding=encoding, cap=cap)

    def rep_fully_qualified_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None,
            compose: bool = False):
        conventional = self.rep_conventional_name(encoding=encoding, cap=cap)
        sym = self.rep_symbol(encoding=encoding)
        rep = ComposableBlockSequence()
        rep.append(conventional)
        if conventional != sym:
            rep.append('(')
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
        rep = '' if self._paragraph_header is None else StyledText(
            s=self.paragraph_header.natural_name, text_style=text_styles.sans_serif_bold).rep(
            encoding=encoding, cap=cap)
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

    def __init__(self, universe_of_discourse: UniverseOfDiscourse,
            is_theory_foundation_system: bool = False, is_universe_of_discourse: bool = False,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, namespace: (None, SymbolicObject) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_symbolic_objct, configuration.echo_default,
            False)
        auto_index = prioritize_value(auto_index, configuration.auto_index, True)
        self._declarative_classes = frozenset()
        is_theory_foundation_system = False if is_theory_foundation_system is None else is_theory_foundation_system
        is_universe_of_discourse = False if is_universe_of_discourse is None else is_universe_of_discourse
        if nameset is None:
            symbol = configuration.default_symbolic_object_symbol if symbol is None else symbol
            if isinstance(symbol, str):
                symbol = SerifItalic(symbol)
            index = universe_of_discourse.index_symbol(symbol=symbol) if (
                    index is None and auto_index) else index
            if paragraph_header is None:
                paragraph_header = paragraph_headers.uncategorized
            nameset = NameSet(symbol=symbol, index=index, namespace=namespace,
                dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
                explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref,
                subtitle=subtitle)
        if isinstance(nameset, str):
            symbol = StyledText(plaintext=nameset, text_style=text_styles.serif_italic)
            index = universe_of_discourse.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index, namespace=namespace,
                dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
                explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref,
                subtitle=subtitle)
        self._nameset = nameset
        self.is_theory_foundation_system = is_theory_foundation_system
        self._declare_class_membership(classes.symbolic_objct)
        if not is_universe_of_discourse:
            self._universe_of_discourse = universe_of_discourse
            self._universe_of_discourse.cross_reference_symbolic_objct(o=self)
        else:
            self._universe_of_discourse = None
        if echo:
            repm.prnt(self.rep_report())

    def __hash__(self):
        # Symbols are unique within their universe-of-discourse,
        # thus hashing can be safely based on the key: U + symbol.
        # With a special case for the universe-of-discourse itself,
        # where hash of the symbol is sufficient.
        return hash(self.nameset) if is_in_class(self, classes.u) else hash(
            (self.universe_of_discourse, self.nameset))

    # def __lt__(self, other):
    #    """WARNING: Only used for support with the sorted() function, no intention to transmit
    #    any mathematical meaning."""
    #    return str(self) < str(other)

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

    def compose_paragraph_header_unabridged(self) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from self.nameset.compose_paragraph_header_unabridged()
        return output

    def compose_ref(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_ref()
        return output

    def compose_ref_link(self, cap: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from self.nameset.compose_ref_link(cap=cap)
        return output

    def compose_report(self, close_punctuation: Composable = None, cap: (None, bool) = None,
            proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        yield from text_dict.let.compose(cap=cap)  # TODO: Support cap parameter
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
        yield from self.universe_of_discourse.compose_symbol()
        yield prioritize_value(close_punctuation, text_dict.period)
        return True

    def compose_symbol(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_symbol()
        return output

    def compose_title(self, cap: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from self.nameset.compose_title(cap=cap)
        return output

    @property
    def declarative_classes(self) -> frozenset[DeclarativeClass]:
        """The set of declarative-classes this symbolic-objct is a member of."""
        return self._declarative_classes

    def _declare_class_membership(self, c: DeclarativeClass):
        """During construction (__init__()), add the declarative-classes this symboli-objct is
        being made a member of."""
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
         1. o₁ and o₂ have symbol-equivalent theory.¹
         2. o₁ and o₂ have equal symbols.²

        ¹. Theories are symbolic-objects. This recursive condition
           yields a complete path between the objects and the universe-of-discourse.
        ². Remember that every symbolic-object has a unique symbol in its parent theory.

        Note:
        -----
        The symbol-equivalence relation allows to compare any pair of symbolic-objcts, including:
         * Both theoretical and atheoretical objects.
         * Symbolic-objcts linked to distinct theory.
        """
        # A theoretical-object can only be compared with a theoretical-object
        assert isinstance(o2, SymbolicObject)
        if self is o2:
            # If the current symbolic-objct is referencing the same
            # python object instance, by definitions the two python references
            # are referencing the same object.
            return True
        if not self.universe_of_discourse.is_symbol_equivalent(o2.universe_of_discourse):
            return False
        if self.nameset != o2.nameset:
            return False
        return True

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
        """This symbolic-object''s universe of discourse. Full name: o.universe_of_discourse."""
        return self.universe_of_discourse

    @property
    def universe_of_discourse(self):
        """This symbolic-object''s universe of discourse. Shortcut: o.u"""
        return self._universe_of_discourse


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
        relation = self.b
        first_parameter = self.a
        second_parameter = other
        return self.a.u.f(relation, first_parameter, second_parameter)

    def __str__(self):
        return f'InfixPartialFormula(a = {self.a}, b = {self.b})'

    # def __ror__(self, other=None):  #    """Hack to provide support for pseudo-infix notation, as in: p |implies| q.  #    """  #    print(f'IPF.__ror__: self = {self}, other = {other}')  #    if not isinstance(other, InfixPartialFormula):  #        return InfixPartialFormula(a=self, b=other)  # return self.a.u.f(self.b, self.a, other)  #    else:  #        verify(assertion=1 == 2, msg='failed infix notation', slf_a=self.a, slf_b=self.b)  #        return self.a.u.f(self.a, self.b, self)


class TheoreticalObject(SymbolicObject):
    """
    Definition
    ----------
    Given a theory 𝒯, a theoretical-object ℴ is an object that:
     * is constitutive of 𝒯,
     * may be referenced in 𝒯 formulae (i.e. 𝒯 may "talk about" ℴ),
     * that may be but is not necessarily a statement in 𝒯 (e.g. it may be an invalid or
     inconsistent formula).

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

    def __init__(self, universe_of_discourse: UniverseOfDiscourse,
            is_theory_foundation_system: bool = False, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            namespace: (None, SymbolicObject) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        # pseudo-class properties. these must be overwritten by
        # the parent constructor after calling __init__().
        # the rationale is that checking python types fails
        # miserably (e.g. because of context managers),
        # thus, implementing explicit functional-types will prove
        # more robust and allow for duck typing.
        super().__init__(universe_of_discourse=universe_of_discourse,
            is_theory_foundation_system=is_theory_foundation_system, symbol=symbol, index=index,
            auto_index=auto_index, namespace=namespace, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, nameset=nameset,
            echo=False)
        super()._declare_class_membership(classes.theoretical_objct)
        if echo:
            repm.prnt(self.rep_fully_qualified_name())

    def __and__(self, other=None):
        """Hack to provide support for pseudo-postfix notation, as in: p & ++.
        This is accomplished by re-purposing the & operator,
        overloading the __and__() method that is called when & is used,
        and gluing all this together.
        """
        # print(f'TO.__and__: self = {self}, other = {other}')
        return verify_formula(u=self.u, input_value=(other, self))

    def __call__(self, *parameters):
        """Hack to provide support for direct function-call notation, as in: p(x).
        """
        # print(f'TO.__call__: self = {self}, parameters = {parameters}')
        ok: bool
        formula: (None, Formula)
        msg: (None, str)
        ok, formula, msg = verify_formula(u=self.u, input_value=(self, *parameters),
            raise_exception=True)
        return formula

    def __xor__(self, other=None):
        """Hack to provide support for pseudo-prefix notation, as in: neg ^ p.
        This is accomplished by re-purposing the ^ operator,
        overloading the __xor__() method that is called when ^ is used,
        and gluing all this together.
        """
        # print(f'TO.__xor__: self = {self}, other = {other}')
        ok: bool
        formula: (None, Formula)
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
            # return self.u.f(self, other.a, other.b)
            ok: bool
            formula: (None, Formula)
            msg: (None, str)
            ok, formula, msg = verify_formula(u=self.u, input_value=(self, other.a, other.b),
                raise_exception=True)
            return formula

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

    def is_formula_syntactically_equivalent_to(self, o2: TheoreticalObject) -> bool:
        """Returns true if ⌜self⌝ is formula-syntactically-equivalent to ⌜o2⌝.

        Parameters:
        -----------
        o2 : TheoreticalObject
            The theoretical-object with which to verify formula-equivalence.

        """
        return self is o2

    def is_masked_formula_similar_to(self,
            o2: (Formula, FormulaStatement, FreeVariable, Relation, SimpleObjct, TheoreticalObject),
            mask: (None, frozenset[FreeVariable]) = None) -> bool:
        """Given two theoretical-objects o₁ (self) and o₂,
        and a finite set of variables 𝐌,
        return True if o₁ and o₂ are masked-formula-similar, False otherwise.

        Definition
        ----------
        Given two theoretical-objects o₁ (self) and o₂,
        and a finite set of variables 𝐌,
        o₁ and o₂ are masked-formula-similar if and only if:
         1. o₁ is formula-syntactically-equivalent to o₂, including the special case
            when both o₁ and o₂ are symbolic-equivalent to a variable 𝐱 in 𝐌,
         2. or the weaker condition that strictly one theoretical-object o₁ or o₂
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
        o2 : TheoreticalObject
            A theoretical-object with which to verify masked-formula-similitude.

        mask: set
            Set of FreeVariable elements. If None, the empty set is assumed.

        """
        output, _values = self._is_masked_formula_similar_to(o2=o2, mask=mask)
        return output

    def _is_masked_formula_similar_to(self,
            o2: (Formula, FormulaStatement, FreeVariable, Relation, SimpleObjct, TheoreticalObject),
            mask: (None, frozenset[FreeVariable]) = None, _values: (None, dict) = None) -> (
            bool, dict):
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
        if o1.is_formula_syntactically_equivalent_to(o2):
            # Sufficient condition.
            return True, _values
        if isinstance(o1, (Formula, FormulaStatement)) and isinstance(o2,
                (Formula, FormulaStatement)):
            # When both o1 and o2 are formula,
            # verify that their components are masked-formula-similar.
            relation_output, _values = o1.relation._is_masked_formula_similar_to(o2=o2.relation,
                mask=mask, _values=_values)
            if not relation_output:
                return False, _values
            # Arities are necessarily equal.
            for i in range(len(o1.parameters)):
                parameter_output, _values = o1.parameters[i]._is_masked_formula_similar_to(
                    o2=o2.parameters[i], mask=mask, _values=_values)
                if not parameter_output:
                    return False, _values
            return True, _values
        if o1 not in mask and o2 not in mask:
            # We know o1 and o2 are not formula-syntactically-equivalent,
            # and we know they are not in the mask.
            return False, _values
        if o1 in mask:
            variable = o2
            newly_observed_value = o1
            if variable in _values:
                already_observed_value = _values[variable]
                if not newly_observed_value.is_formula_syntactically_equivalent_to(
                        already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        if o2 in mask:
            variable = o1
            newly_observed_value = o2
            if variable in _values:
                already_observed_value = _values[variable]
                if not newly_observed_value.is_formula_syntactically_equivalent_to(
                        already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        return True, _values

    def substitute(self, substitution_map, target_theory, lock_variable_scope=None):
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
            pass  # assert isinstance(key, TheoreticalObjct)  ##### XXXXX  # verify(  #  #  #  #  # isinstance(value, (  #    TheoreticalObjct, contextlib._GeneratorContextManager)),  #    'The value component of this key/value pair in this '  #    'substitution map is  #    not an instance of TheoreticalObjct.',  #    key=key, value=value,  #    value_type=type(value), self2=self)  # A formula relation cannot be replaced by  #    a simple-objct.  # But a simple-object could be replaced by a formula,  # if that formula "yields" such simple-objects.  # TODO: Implement clever rules here  #  to avoid ill-formed formula,  #   or let the formula constructor do the work.  #  #  assert type(key) == type(value) or isinstance(  #    value, FreeVariable) or  #  #  #  isinstance(  #    key, FreeVariable)  # If these are formula, their arity must be  #  equal  # to prevent the creation of an ill-formed formula.  # NO, THIS IS WRONG.  #  TODO: Re-analyze this point.  # assert not isinstance(key, Formula) or key.arity  #   == value.arity

        # Because the scope of variables is locked,
        # the substituted formula must create "duplicates" of all variables.
        variables_list = self.get_variable_ordered_set()
        for x in variables_list:
            if x not in substitution_map.keys():
                # Call declare_free_variable() instead of v()
                # to explicitly manage variables scope locking.
                x2 = self.universe_of_discourse.declare_free_variable(x.nameset.nameset)
                substitution_map[x] = x2

        # Now we may proceed with substitution.
        if self in substitution_map:
            return substitution_map[self]
        elif isinstance(self, Formula):
            # If both key / value are formulae,
            #   we must check for formula-equivalence,
            #   rather than python-object-equality.
            for k, v in substitution_map.items():
                if self.is_formula_syntactically_equivalent_to(k):
                    return v

            # If the formula itself is not matched,
            # the next step consist in decomposing it
            # into its constituent parts, i.e. relation and parameters,
            # to apply the substitution operation on these.
            relation = self.relation.substitute(substitution_map=substitution_map,
                target_theory=target_theory, lock_variable_scope=lock_variable_scope)
            parameters = tuple(
                p.substitute(substitution_map=substitution_map, target_theory=target_theory,
                    lock_variable_scope=False) for p in self.parameters)
            phi = self.universe_of_discourse.f(relation, *parameters,
                lock_variable_scope=lock_variable_scope)
            return phi
        else:
            return self

    def iterate_relations(self, include_root: bool = True):
        """Iterate through this and all the theoretical-objcts it contains recursively, providing
        they are relations."""
        return (r for r in self.iterate_theoretical_objcts_references(include_root=include_root) if
            is_in_class(r, classes.relation))

    def iterate_theoretical_objcts_references(self, include_root: bool = True,
            visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it contains recursively.
        """
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})

    def contains_theoretical_objct(self, o: TheoreticalObject):
        """Return True if o is in this theory's hierarchy, False otherwise.
        """
        return o in self.iterate_theoretical_objcts_references(include_root=True)

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, None, None]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        pass

    def export_interactive_graph(self, output_path: str, pyvis_graph: (None, pyvis.network) = None,
            encoding: (None, Encoding) = None, label_wrap_size: (None, int) = None,
            title_wrap_size: (None, int) = None) -> None:
        """Export a theoretical-object as a statement dependency graph in an HTML page with
        visJS, thanks to the pyvis theory."""
        pyvis_graph = prioritize_value(pyvis_graph, pyvis.network.Network(directed=True))
        label_wrap_size = prioritize_value(label_wrap_size, pyvis_configuration.label_wrap_size)
        title_wrap_size = prioritize_value(title_wrap_size, pyvis_configuration.title_wrap_size)
        pyvis_graph: pyvis.network.Network
        node_id = self.rep_symbol(encoding=encodings.plaintext)
        if node_id not in pyvis_graph.get_nodes():
            kwargs = None
            if is_in_class(self, classes.axiom_inclusion):
                self: AxiomInclusion
                kwargs = pyvis_configuration.axiom_inclusion_args
                ref = '' if self.ref is None else f'({self.rep_ref(encoding=encoding)}) '
                bold = True if ref != '' else False
                node_label = f'{self.rep_symbol(encoding=encoding)} {ref}: ' \
                             f'{self.rep_natural_language(encoding=encoding)}'
                if label_wrap_size is not None:
                    node_label = '\n'.join(textwrap.wrap(text=node_label, width=label_wrap_size))
                pyvis_graph.add_node(node_id, label=node_label, **kwargs)
            elif is_in_class(self, classes.definition_inclusion):
                self: DefinitionInclusion
                kwargs = pyvis_configuration.definition_inclusion_args
                ref = '' if self.ref is None else f'({self.rep_ref(encoding=encoding)}) '
                bold = True if ref != '' else False
                node_label = f'{self.rep_symbol(encoding=encoding)} {ref}: ' \
                             f'{self.rep_natural_language(encoding=encoding)}'
                if label_wrap_size is not None:
                    node_label = '\n'.join(textwrap.wrap(text=node_label, width=label_wrap_size))
                pyvis_graph.add_node(node_id, label=node_label, **kwargs)
            elif is_in_class(self, classes.inferred_proposition):
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
                pyvis_graph.add_node(node_id, label=node_label, title=node_title,
                    labelHighlightBold=bold, **kwargs)
                for parameter in self.parameters:
                    if isinstance(parameter, tuple):
                        # variable-substitution uses a tuple as parameter.
                        for x in parameter:
                            x.export_interactive_graph(output_path=None, pyvis_graph=pyvis_graph,
                                encoding=encoding, label_wrap_size=label_wrap_size,
                                title_wrap_size=title_wrap_size)
                            parameter_node_id = x.rep_symbol(encoding=encodings.plaintext)
                            if parameter_node_id in pyvis_graph.get_nodes():
                                pyvis_graph.add_edge(source=parameter_node_id, to=node_id)
                    else:
                        parameter.export_interactive_graph(output_path=None,
                            pyvis_graph=pyvis_graph, encoding=encoding,
                            label_wrap_size=label_wrap_size, title_wrap_size=title_wrap_size)
                        parameter_node_id = parameter.rep_symbol(encoding=encodings.plaintext)
                        if parameter_node_id in pyvis_graph.get_nodes():
                            pyvis_graph.add_edge(source=parameter_node_id, to=node_id)
        if is_in_class(self, classes.theory_elaboration):
            self: TheoryElaborationSequence
            for statement in self.statements:
                # Bug fix: sections should not be TheoreticalObjects but DecorativeObjects!
                if not isinstance(statement, Section):
                    statement.export_interactive_graph(output_path=None, pyvis_graph=pyvis_graph,
                        encoding=encoding, label_wrap_size=label_wrap_size,
                        title_wrap_size=title_wrap_size)
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

    def __init__(self, u: UniverseOfDiscourse, status: (None, FreeVariable.Status) = None,
            scope: (None, Formula, typing.FrozenSet[Formula]) = None,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None) -> None:
        echo = prioritize_value(echo, configuration.echo_free_variable_declaration,
            configuration.echo_default, False)
        status = prioritize_value(status, FreeVariable.scope_initialization_status)
        scope = prioritize_value(scope, frozenset())
        scope = {scope} if isinstance(scope, Formula) else scope
        verify(isinstance(scope, frozenset),
            'The scope of a FreeVariable must be of python type frozenset.')
        verify(isinstance(status, FreeVariable.Status),
            'The status of a FreeVariable must be of the FreeVariable.Status type.')
        self._status = status
        self._scope = scope
        assert isinstance(u, UniverseOfDiscourse)
        if symbol is None:
            symbol = configuration.default_free_variable_symbol
            index = u.index_symbol(symbol=symbol)
        if isinstance(symbol, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            symbol = StyledText(plaintext=symbol, text_style=text_styles.serif_bold)
            if index is None and auto_index:
                index = u.index_symbol(symbol=symbol)
        super().__init__(universe_of_discourse=u, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, nameset=nameset, echo=False)
        # self.universe_of_discourse.cross_reference_variable(x=self)
        super()._declare_class_membership(declarative_class_list.free_variable)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='free-variable')

    def echo(self):
        self.rep_report()

    @property
    def scope(self):
        """The scope of a free variable is the set of the formula where the variable is used.

        :return:
        """
        return self._scope

    def lock_scope(self):
        # Support for the with pythonic syntax
        # Start building  variable scope
        verify(self._status == FreeVariable.scope_initialization_status,
            'The scope of an instance of FreeVariable can only be locked if it is open.')
        # Close variable scope
        self._status = FreeVariable.closed_scope_status

    def extend_scope(self, phi):
        # Support for the with pythonic syntax
        # Start building  variable scope
        verify(self._status == FreeVariable.scope_initialization_status,
            'The scope of an instance of FreeVariable can only be extended if it is open.')
        # Close variable scope
        verify(isinstance(phi, Formula),
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
        return self.is_formula_syntactically_equivalent_to(o2), _values

    def rep_report(self, encoding: (None, Encoding) = None, proof: (None, bool) = None):
        return f'Let {self.rep_name(encoding=encoding)} be a free-variable in ' \
               f'{self.universe_of_discourse.rep_name(encoding=encoding)}' + '\n'


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

    function_call = repm.ValueName('function-call')
    infix = repm.ValueName('infix-operator')
    prefix = repm.ValueName('prefix-operator')
    postfix = repm.ValueName('postfix-operator')

    def __init__(self, relation: (Relation, FreeVariable), parameters: tuple,
            universe_of_discourse: UniverseOfDiscourse, nameset: (None, str, NameSet) = None,
            lock_variable_scope: bool = False, dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """
        """
        echo = prioritize_value(echo, configuration.echo_formula_declaration,
            configuration.echo_default, False)
        self.free_variables = dict()  # TODO: Check how to make dict immutable after construction.
        # self.formula_index = theory.crossreference_formula(self)
        if nameset is None:
            symbol = configuration.default_formula_symbol
            index = universe_of_discourse.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index)
        if isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            symbol = StyledText(plaintext=nameset, text_style=text_styles.serif_italic)
            index = universe_of_discourse.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index)
        self.relation = relation
        parameters = parameters if isinstance(parameters, tuple) else tuple([parameters])
        verify(assertion=len(parameters) > 0,
            msg='Ill-formed formula error. The number of parameters in this formula is zero. 0-ary relations are currently not supported. Use a simple-object instead.',
            severity=verification_severities.error, raise_exception=True, relation=self.relation,
            len_parameters=len(parameters))
        verify(assertion=self.relation.arity is None or self.relation.arity == len(parameters),
            msg=f'Ill-formed formula error. Relation ⌜{self.relation}⌝ is defined with a fixed arity constraint of {self.relation.arity} but the number of parameters provided to construct this formula is {len(parameters)}.',
            severity=verification_severities.error, raise_exception=True, relation=self.relation,
            relation_arity=self.relation.arity, len_parameters=len(parameters),
            parameters=parameters)
        verify(
            assertion=self.relation.min_arity is None or self.relation.min_arity >= len(parameters),
            msg=f'Ill-formed formula error. Relation ⌜{self.relation}⌝ is defined with a minimum arity constraint of {self.relation.min_arity} but the number of parameters provided to construct this formula is {len(parameters)}.',
            severity=verification_severities.error, raise_exception=True, relation=self.relation,
            relation_min_arity=self.relation.min_arity, len_parameters=len(parameters),
            parameters=parameters)
        verify(
            assertion=self.relation.max_arity is None or self.relation.max_arity >= len(parameters),
            msg=f'Ill-formed formula error. Relation ⌜{self.relation}⌝ is defined with a maximum arity constraint of {self.relation.max_arity} but the number of parameters provided to construct this formula is {len(parameters)}.',
            severity=verification_severities.error, raise_exception=True, relation=self.relation,
            relation_max_arity=self.relation.max_arity, len_parameters=len(parameters),
            parameters=parameters)
        self.arity = len(parameters)
        self.parameters = parameters
        super().__init__(nameset=nameset, universe_of_discourse=universe_of_discourse, echo=False)
        super()._declare_class_membership(declarative_class_list.formula)
        universe_of_discourse.cross_reference_formula(self)
        verify(
            is_in_class(relation, classes.relation) or is_in_class(relation, classes.free_variable),
            'The relation of this formula is neither a relation, nor a '
            'free-variable.', formula=self, relation=relation)
        verify(relation.universe_of_discourse is self.universe_of_discourse,
            f'The universe-of-discourse ⌜{relation.u}⌝ of the relation in the formula ⌜{self}⌝ is inconsistent with the universe-of-discourse ⌜{self.u}⌝ of the formula.',
            formula=self, relation=relation)
        self.cross_reference_variables()
        for p in parameters:
            verify(is_in_class(p, classes.theoretical_objct), 'p is not a theoretical-objct.',
                formula=self, p=p)
            if is_in_class(p, classes.free_variable):
                p.extend_scope(self)
            verify(p.u is self.universe_of_discourse,
                f'The universe-of-discourse ⌜{p.u}⌝ of the parameter ⌜{p}⌝ in the formula ⌜{self}⌝ is inconsistent with the universe-of-discourse ⌜{self.u}⌝ of the formula.',
                formula=self, p=p)
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
        pass  # assert False

    def echo(self):
        repm.prnt(self.rep_report())

    @property
    def is_proposition(self):
        """Tell if the formula is a logic-proposition.

        This property is directly inherited from the formula-is-proposition
        attribute of the formula's relation."""
        return self.relation.signal_proposition

    def is_formula_syntactically_equivalent_to(self, o2: TheoreticalObject) -> bool:
        """Return true if ⌜self⌝ is formula-syntactically-equivalent to ⌜o2⌝.

        Parameters:
        -----------
        o2 : TheoreticalObject
            The theoretical-object with which to verify formula-equivalence.

        """
        # if o2 is a formula-statement, retrieve its formula.
        o2 = o2.valid_proposition if is_in_class(o2, classes.formula_statement) else o2
        if self is o2:
            # Trivial case.
            return True
        if not isinstance(o2, Formula):
            return False
        if not self.relation.is_formula_syntactically_equivalent_to(o2.relation):
            return False
        # Arities are necessarily equal.
        for i in range(len(self.parameters)):
            if not self.parameters[i].is_formula_syntactically_equivalent_to(o2.parameters[i]):
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
            yield from self.relation.iterate_theoretical_objcts_references(include_root=False,
                visited=visited)
        for parameter in set(self.parameters).difference(visited):
            yield parameter
            visited.update({parameter})
            yield from parameter.iterate_theoretical_objcts_references(include_root=False,
                visited=visited)

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

    def rep(self, encoding: (None, Encoding) = None, expand: (None, bool) = None) -> str:
        expand = True if expand is None else expand
        assert isinstance(expand, bool)
        if expand:
            return self.rep_formula(encoding=encoding, expand=expand)
        else:
            return super().rep(encoding=encoding, expand=expand)

    def compose_function_call(self) -> collections.abc.Generator[Composable, None, None]:
        global text_dict
        yield from self.relation.compose_formula()
        yield text_dict.open_parenthesis
        first_item = True
        for p in self.parameters:
            if not first_item:
                yield text_dict.formula_parameter_separator
            yield from p.compose_formula()
            first_item = False
        yield text_dict.close_parenthesis

    def rep_function_call(self, encoding: (None, Encoding) = None,
            expand: (None, bool) = None) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_function_call(), encoding=encoding)

    def compose_infix_operator(self) -> collections.abc.Generator[Composable, None, None]:
        verify(assertion=self.relation.arity == 2,
            msg='Relation is not binary, formula-representation-style is infix.',
            relation=self.relation, slf=self)
        global text_dict
        yield text_dict.open_parenthesis
        yield from self.parameters[0].compose_formula()
        yield text_dict.space
        yield from self.relation.compose_formula()
        yield text_dict.space
        yield from self.parameters[1].compose_formula()
        yield text_dict.close_parenthesis

    def rep_infix_operator(self, encoding: (None, Encoding) = None, expand=(None, bool),
            **kwargs) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_infix_operator(), encoding=encoding)

    def compose_postfix_operator(self) -> collections.abc.Generator[Composable, None, None]:
        verify(assertion=len(self.parameters) == 1,
            msg='Postfix-operator formula representation is used but arity is not equal to 1',
            slf=self)
        global text_dict
        yield text_dict.open_parenthesis
        yield from self.parameters[0].compose_formula()
        yield text_dict.close_parenthesis
        yield from self.relation.compose_formula()

    def rep_postfix_operator(self, encoding: (None, Encoding) = None, expand=None) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_postfix_operator(), encoding=encoding)

    def compose_prefix_operator(self) -> collections.abc.Generator[Composable, None, None]:
        verify(assertion=len(self.parameters) == 1,
            msg='Prefix-operator formula representation is used but arity is not equal to 1',
            slf=self)
        global text_dict
        yield from self.relation.compose_formula()
        yield text_dict.open_parenthesis
        yield from self.parameters[0].compose_formula()
        yield text_dict.close_parenthesis

    def rep_as_prefix_operator(self, encoding: (None, Encoding) = None, expand=None) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_prefix_operator(), encoding=encoding)

    def compose_formula(self) -> collections.abc.Generator[Composable, None, None]:
        if is_in_class(self.relation, classes.free_variable):
            # If the relation of this formula is a free-variable,
            # it has no arity, neither a representation-mode.
            # In this situation, our design-choice is to
            # fallback on the function-call representation-mode.
            # In future developments, we may choose to allow
            # the "decoration" of free-variables with arity,
            # and presentation-mode to improve readability.
            yield from self.compose_function_call()
        else:
            match self.relation.formula_rep:
                case Formula.function_call:
                    yield from self.compose_function_call()
                case Formula.infix:
                    yield from self.compose_infix_operator()
                case Formula.prefix:
                    yield from self.compose_prefix_operator()
                case Formula.postfix:
                    yield from self.compose_postfix_operator()
                case _:
                    # Fallback notation.
                    yield from self.compose_function_call()

    def rep_formula(self, encoding: (None, Encoding) = None, expand: bool = True) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_formula(), encoding=encoding)

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='formula')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, None, None]:
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
        yield from self.universe_of_discourse.compose_symbol()
        yield text_dict.period


class SimpleObjctDict(collections.UserDict):

    def __init__(self, u: UniverseOfDiscourse):
        self.u = u
        super().__init__()
        # Well-known objects
        self._falsehood = None
        self._relation = None
        self._truth = None

    def declare(self, symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None) -> SimpleObjct:
        return SimpleObjct(symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle, nameset=nameset,
            universe_of_discourse=self.u, echo=echo)

    @property
    def fals(self):
        return self.falsehood

    @property
    def falsehood(self):
        if self._falsehood is None:
            self._falsehood = self.declare(nameset=NameSet(
                symbol=StyledText(unicode='⊥', latex='\\bot', plaintext='false',
                    text_style=text_styles.serif_normal), name=ComposableText(plaintext='false'),
                explicit_name=ComposableText(plaintext='falsehood'), index=None))
        return self._falsehood

    @property
    def relation(self):
        if self._relation is None:
            self._relation = self.declare(symbol='relation', name='relation', auto_index=False,
                abridged_name='rel.')
        return self._relation

    @property
    def tru(self):
        return self.truth

    @property
    def truth(self):
        if self._truth is None:
            self._truth = self.declare(nameset=NameSet(
                symbol=StyledText(unicode='⊤', latex='\\top', plaintext='true',
                    text_style=text_styles.serif_normal), name=ComposableText(plaintext='true'),
                explicit_name=ComposableText(plaintext='truth'), index=None))
        return self._truth


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

    def rep(self, encoding: (None, Encoding) = None, cap: (None, bool) = None,
            expand: (None, bool) = None):
        # TODO: Implement encoding
        return self.natural_name


class ParagraphHeaders(repm.ValueName):
    # axiom = TitleCategory('axiom', 's', 'axiom', 'axiom')
    axiom_declaration = ParagraphHeader('axiom_declaration', 'a', SansSerifBold('axiom'), 'axiom')
    axiom_inclusion = ParagraphHeader('axiom_inclusion', 's', SansSerifBold('axiom'), 'axiom')
    axiom_schema_declaration = ParagraphHeader('axiom_schema_declaration', 'a',
        SansSerifBold('axiom schema'), 'axiom schema')
    axiom_schema_inclusion = ParagraphHeader('axiom_schema_inclusion', 's',
        SansSerifBold('axiom schema'), 'axiom schema')
    corollary = ParagraphHeader('corollary', 's', 'corollary', 'cor.')
    definition_declaration = ParagraphHeader('definition_declaration', 'd',
        SansSerifBold('definition'), 'def.')
    definition_inclusion = ParagraphHeader('definition_inclusion', 's', SansSerifBold('definition'),
        'def.')
    hypothesis = ParagraphHeader('hypothesis', 'H', 'hypothesis', 'hyp.')
    inference_rule_declaration = ParagraphHeader('inference_rule', 'I', 'inference rule',
        'inference rule')
    inference_rule_inclusion = ParagraphHeader('inference_rule_inclusion', 'I', 'inference rule',
        'inference rule')
    inferred_proposition = ('inferred_proposition', 's', 'inferred-proposition')
    lemma = ParagraphHeader('lemma', 's', 'lemma', 'lem.')
    proposition = ParagraphHeader('proposition', 's', 'proposition', 'prop.')
    relation_declaration = ParagraphHeader('relation_declaration', 's', 'proposition', 'prop.')
    theorem = ParagraphHeader('theorem', 's', 'theorem', 'thrm.')
    theory_elaboration_sequence = ParagraphHeader('theory_elaboration_sequence', 't',
        'theory elaboration sequence', 'theo.')
    informal_definition = ParagraphHeader('informal definition',
        StyledText(plaintext='note', unicode='🗅'), 'informal definition', 'inf. def.')
    comment = ParagraphHeader('comment', StyledText(plaintext='note', unicode='🗅'), 'comment',
        'cmt.')
    note = ParagraphHeader('note', StyledText(plaintext='note', unicode='🗅'), 'note', 'note')
    remark = ParagraphHeader('remark', StyledText(plaintext='note', unicode='🗅'), 'remark', 'rmrk.')
    warning = ParagraphHeader('warning', StyledText(plaintext='warning', unicode='🗅'), 'warning',
        'warning')
    # Special categories
    uncategorized = ParagraphHeader('uncategorized', 's', 'uncategorized', 'uncat.')
    informal_assumption = ParagraphHeader('informal assumption',
        StyledText(plaintext='informal assumption', unicode='🗅'), 'informal assumption',
        'informal assumption')
    informal_proposition = ParagraphHeader('informal proposition',
        StyledText(plaintext='informal proposition', unicode='🗅'), 'informal proposition',
        'informal proposition')
    informal_proof = ParagraphHeader('informal proof',
        StyledText(plaintext='informal proof', unicode='🗅'), 'informal proof', 'informal proof')


paragraph_headers = ParagraphHeaders('paragraph_headers')


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

    def __init__(self, theory: TheoryElaborationSequence, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            paragraph_header: (None, ParagraphHeader) = None, echo: (None, bool) = None):
        self._theory = theory
        echo = prioritize_value(echo, configuration.echo_statement, configuration.echo_default,
            False)
        universe_of_discourse = theory.universe_of_discourse
        self.statement_index = theory.crossreference_statement(self)
        self._paragraph_header = paragraph_header
        namespace = self._theory  # TODO: Cross-referencing the theory symbol as the nameset of
        # the statement is ugly, there's something wrong with the data model, correct it.
        super().__init__(universe_of_discourse=universe_of_discourse, symbol=symbol, index=index,
            auto_index=auto_index, namespace=namespace, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, nameset=nameset,
            echo=echo)
        super()._declare_class_membership(declarative_class_list.statement)
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
    def t(self) -> TheoryElaborationSequence:
        """The theory-elaboration-sequence that contains this statement.

        Unabridged property: statement.theory"""
        return self.theory

    @property
    def theory(self) -> TheoryElaborationSequence:
        """The theory-elaboration-sequence that contains this statement.

        Abridged property: s.t

        This property may only be set once. In effect, moving statements
        between theory would lead to unstable theory."""
        return self._theory

    @theory.setter
    def theory(self, t: TheoryElaborationSequence):
        verify(self._theory is None, '⌜theory⌝ property may only be set once.', slf=self,
            slf_theory=self._theory, t=t)
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
    """The Axiom pythonic class models the elaboration of a _contentual_ _axiom_ in a
    _universe-of-discourse_.

    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, natural_language: (str, StyledText), u: UniverseOfDiscourse,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """

        :param natural_language: The axiom's content in natural-language.
        :param u: The universe-of-discourse.
        :param nameset:
        :param echo:
        """
        echo = prioritize_value(echo, configuration.echo_axiom_declaration,
            configuration.echo_default, False)
        if isinstance(natural_language, str):
            natural_language = natural_language.strip()
            verify(natural_language != '',
                'Parameter natural-language is an empty string (after trimming).')
            natural_language = SansSerifItalic(natural_language)
        self._natural_language = natural_language
        paragraph_header = prioritize_value(paragraph_header, paragraph_headers.axiom_declaration)
        verify(
            assertion=paragraph_header is paragraph_headers.axiom_declaration or paragraph_header is paragraph_headers.axiom_schema_declaration,
            msg='paragraph-header must be either axiom-declaration, or axiom-schema-declaration.',
            paragraph_header=paragraph_header)
        if nameset is None and symbol is None:
            symbol = configuration.default_axiom_declaration_symbol
        super().__init__(universe_of_discourse=u, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle,
            paragraph_header=paragraph_header, nameset=nameset, echo=False)
        super()._declare_class_membership(declarative_class_list.axiom)
        u.cross_reference_axiom(self)
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

    @property
    def natural_language(self) -> StyledText:
        return self._natural_language

    def rep_natural_language(self, encoding: (None, Encoding) = None, wrap: bool = None) -> str:
        return rep_composition(composition=self.compose_natural_language(), encoding=encoding,
            wrap=wrap)


class AxiomInclusion(Statement):
    """This python class models the inclusion of an :ref:`axiom<axiom_math_concept>` as a valid in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, a: AxiomDeclaration, t: TheoryElaborationSequence,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_axiom_inclusion,
            configuration.echo_default, False)
        self._axiom = a
        t.crossreference_definition_endorsement(self)
        paragraph_header = prioritize_value(paragraph_header, paragraph_headers.axiom_inclusion)
        verify(
            assertion=paragraph_header is paragraph_headers.axiom_inclusion or paragraph_header is paragraph_headers.axiom_schema_inclusion,
            msg='paragraph-header must be either axiom-inclusion, or axiom-schema-inclusion.',
            paragraph_header=paragraph_header)
        if nameset is None and symbol is None:
            symbol = configuration.default_axiom_inclusion_symbol
        super().__init__(theory=t, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref,
            subtitle=subtitle, nameset=nameset, echo=False)
        super()._declare_class_membership(declarative_class_list.axiom_inclusion)
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
        return self._axiom

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

    def rep_natural_language(self, encoding: (None, Encoding) = None, wrap: bool = True) -> str:
        return self._axiom.rep_natural_language(encoding=encoding, wrap=wrap)


class InferenceRuleInclusion(Statement):
    """This python abstract class models the :ref:`inclusion<object_inclusion_math_concept>` of an :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>`.

    """

    def __init__(self, i: InferenceRuleDeclaration, t: TheoryElaborationSequence,
            symbol: (None, str, StyledText) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None,
            proof: (None, bool) = None):
        self._inference_rule = i
        paragraph_header = paragraph_headers.inference_rule_inclusion
        if symbol is None:
            symbol = configuration.default_inference_rule_inclusion_symbol if symbol is None else symbol
            index = t.universe_of_discourse.index_symbol(symbol=symbol)
        super().__init__(theory=t, paragraph_header=paragraph_headers, symbol=symbol, index=index,
            nameset=nameset, echo=False)
        t.crossreference_inference_rule_inclusion(self)
        super()._declare_class_membership(declarative_class_list.inference_rule_inclusion)
        echo = prioritize_value(echo, configuration.echo_inference_rule_inclusion,
            configuration.echo_inclusion, configuration.echo_default, False)
        if echo:
            proof = prioritize_value(proof, configuration.echo_proof, True)
            repm.prnt(self.rep_report(proof=proof))

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        """This python method yields the default mathematical-class of the object in the *punctilious* data model.
        """
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='inference-rule')

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_inference_rule_inclusion_report(i=self,
            proof=proof)
        return output

    @property
    def definition(self) -> Formula:
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
    def construct_formula(self, **kwargs) -> Formula:
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

    def verify_compatibility(self, *args):
        return self.inference_rule.check_inference_validity(*args, t=self.theory)


class DefinitionDeclaration(TheoreticalObject):
    """The Definition pythonic class models the elaboration of a _contentual_ _definition_ in a
    _universe-of-discourse_.

    """

    # class Premises(typing.NamedTuple):
    #    p_implies_q: FlexibleFormula

    def __init__(self, natural_language: str, u: UniverseOfDiscourse,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None):
        """

        :param natural_language: The definition's content in natural-language.
        :param u: The universe-of-discourse.
        :param nameset:
        :param echo:
        """
        echo = prioritize_value(echo, configuration.echo_definition_declaration,
            configuration.echo_default, False)
        if isinstance(natural_language, str):
            natural_language = natural_language.strip()
            verify(natural_language != '',
                'Parameter natural-language is an empty string (after trimming).')
            natural_language = SansSerifItalic(natural_language)
        self._natural_language = natural_language
        cat = paragraph_headers.definition_declaration
        if nameset is None and symbol is None:
            symbol = configuration.default_definition_declaration_symbol
        super().__init__(universe_of_discourse=u, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, paragraph_header=cat, ref=ref, subtitle=subtitle,
            nameset=nameset, echo=False)
        super()._declare_class_membership(declarative_class_list.definition)
        u.cross_reference_definition(self)
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

    @property
    def natural_language(self) -> (None, str):
        """The content of the axiom in natural-language."""
        return self._natural_language

    def rep_natural_language(self, encoding: (None, Encoding) = None, wrap: bool = None) -> str:
        return rep_composition(composition=self.compose_natural_language(), encoding=encoding,
            wrap=wrap)


class DefinitionInclusion(Statement):
    """This python class models the inclusion of a :ref:`definition<definition_math_concept>` as a valid in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, d: DefinitionDeclaration, t: TheoryElaborationSequence,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None):
        """Endorsement (aka include, endorse) an definition in a theory-elaboration.
        """
        echo = prioritize_value(echo, configuration.echo_definition_inclusion,
            configuration.echo_default, False)
        self._definition = d
        t.crossreference_definition_endorsement(self)
        cat = paragraph_headers.definition_inclusion
        if nameset is None and symbol is None:
            symbol = configuration.default_definition_inclusion_symbol
        super().__init__(theory=t, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, paragraph_header=cat, ref=ref, subtitle=subtitle,
            nameset=nameset, echo=False)
        super()._declare_class_membership(declarative_class_list.definition_inclusion)
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
        output = yield from configuration.locale.compose_definition_inclusion_report(o=self,
            proof=proof)
        return output

    @property
    def definition(self):
        return self._definition

    def echo(self):
        repm.prnt(self.rep_report())

    def rep_natural_language(self, encoding: (None, Encoding) = None, wrap: bool = True) -> str:
        return self._definition.rep_natural_language(encoding=encoding, wrap=wrap)


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

    def __init__(self, theory: TheoryElaborationSequence, valid_proposition: Formula,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            paragraphe_header: (None, ParagraphHeader) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_statement, configuration.echo_default,
            False)
        verify(assertion=theory.universe_of_discourse is valid_proposition.universe_of_discourse,
            msg='The universe-of-discourse of this formula-statement''s theory-elaboration is '
                'inconsistent with the universe-of-discourse of the valid-proposition of that '
                'formula-statement.')
        universe_of_discourse = theory.universe_of_discourse
        # Theory statements must be logical propositions.
        valid_proposition = unpack_formula(valid_proposition)
        verify(valid_proposition.is_proposition,
            'The formula of this statement is not propositional.')
        # TODO: Check that all components of the hypothetical-proposition
        #  are elements of the source theory-branch.
        self.valid_proposition = valid_proposition
        self.statement_index = theory.crossreference_statement(self)
        paragraphe_header = prioritize_value(paragraphe_header, paragraph_headers.proposition)
        # TODO: Check that cat is a valid statement cat (prop., lem., cor., theorem)
        if nameset is None and symbol is None:
            symbol = configuration.default_statement_symbol
        super().__init__(theory=theory, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle, nameset=nameset,
            paragraph_header=paragraphe_header, echo=False)
        # manage theoretical-morphisms
        self.morphism_output = None
        if self.valid_proposition.relation.signal_theoretical_morphism:
            # this formula-statement is a theoretical-morphism.
            # it follows that this statement "yields" new statements in the theory.
            assert self.valid_proposition.relation.implementation is not None
            self.morphism_output = Morphism(theory=theory, source_statement=self)
        super()._declare_class_membership(declarative_class_list.formula_statement)
        if echo:
            self.echo()

    def __repr__(self):
        return self.rep(expand=True)

    def __str__(self):
        return self.rep(expand=True)

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='formula-statement')

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

    def is_formula_syntactically_equivalent_to(self, o2: TheoreticalObject) -> bool:
        """Return true if ⌜self⌝ is formula-syntactically-equivalent to ⌜o2⌝.

        Parameters:
        -----------
        o2 : TheoreticalObject
            The theoretical-object with which to verify formula-equivalence.

        """
        return self.valid_proposition.is_formula_syntactically_equivalent_to(o2)

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
        if extension_limit is not None and extension_limit.theory == self.theory and extension_limit.statement_index >= self.statement_index:
            ol = ol.union({self})
            if self.valid_proposition not in ol:
                ol = ol.union(
                    self.valid_proposition.list_theoretical_objcts_recursively_OBSOLETE(ol=ol,
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
        assert isinstance(theory, TheoryElaborationSequence)
        assert isinstance(source_statement, FormulaStatement)
        assert theory.contains_theoretical_objct(source_statement)
        self.source_statement = source_statement
        assert source_statement.valid_proposition.relation.signal_theoretical_morphism
        self.morphism_implementation = source_statement.valid_proposition.relation.implementation
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
                          f'{repm.serif_bold(self.source_statement.valid_proposition.relation.rep_symbol())} morphism.'
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


class InferenceRuleDeclaration(TheoreticalObject):
    """This python abstract class models the :ref:`declaration<object_declaration_math_concept>` of an :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>`.

    """

    def __init__(self, universe_of_discourse: UniverseOfDiscourse,
            definition: (None, Formula) = None,
            compose_paragraph_proof_method: (None, collections.abc.Callable) = None,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None):
        self._definition = definition
        self._compose_paragraph_proof_method = compose_paragraph_proof_method
        if nameset is None and symbol is None:
            symbol = configuration.default_inference_rule_symbol
        paragraph_header = paragraph_headers.inference_rule_declaration
        super().__init__(universe_of_discourse=universe_of_discourse,
            is_theory_foundation_system=False, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref,
            subtitle=subtitle, nameset=nameset, echo=False)
        super()._declare_class_membership(declarative_class_list.inference_rule)
        universe_of_discourse.cross_reference_inference_rule(self)
        echo = prioritize_value(echo, configuration.echo_inference_rule_declaration,
            configuration.echo_declaration, configuration.echo_default, False)
        if echo:
            self.echo()

    def compose_report(self, proof: (None, bool) = None, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """
        .. include:: ../../include/compose_report_python_method.rstinc

        """
        output = yield from configuration.locale.compose_inference_rule_declaration(i=self)
        return output

    def compose_paragraph_proof(self, **kwargs) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """This python method yields a :ref:`paragraph-proof<paragraph_proof_math_concept>` that demonstrates the validity of the object.

        This method should be overridden by specialized inference-rule classes to provide accurate proofs.
        """
        output = yield from configuration.locale.compose_inferred_statement_paragraph_proof(o=self)
        return output

    @property
    def definition(self) -> Formula:
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
    @abc.abstractmethod
    def construct_formula(self, **kwargs) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        raise NotImplementedError(
            'The ⌜construct_formula⌝ method is abstract. It must be implemented in the child class.')


class AbsorptionDeclaration(InferenceRuleDeclaration):
    """This python class models the declaration of the :ref:`absorption<absorption_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .

    TODO: AbsorptionDeclaration: Add a data validation step to assure that parameters p and q are propositional.
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'absorption'
        abridged_name = None
        auto_index = False
        dashed_name = 'absorption'
        explicit_name = 'absorption inference rule'
        name = 'absorption'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = (p | u.r.implies | q) | u.r.proves | (p | u.r.implies | (p | u.r.land | q))
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            self.parameter_p_implies_q = p | u.r.implies | q
            self.parameter_p_implies_q_mask = frozenset([p, q])
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_implies_q: FlexibleFormula) -> (None, Formula):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        ok: bool
        msg: (None, msg)
        ok, p_implies_q, msg = verify_formula(arg='p_implies_q', input_value=p_implies_q, u=self.u,
            form=self.parameter_p_implies_q, mask=self.parameter_p_implies_q_mask,
            raise_exception=True)
        p_implies_q: Formula
        p: Formula = p_implies_q.parameters[0]  # TODO: Use composed type hints
        q: Formula = p_implies_q.parameters[1]  # TODO: Use composed type hints
        output: Formula = p | self.u.r.implies | (p | self.u.r.land | q)
        return output


class AxiomInterpretationDeclaration(InferenceRuleDeclaration):
    """This python class models the :ref:`declaration<object_declaration_math_concept>` of the :ref:`axiom-interpretation<axiom_interpretation_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>`.

    Inherits from :ref:`InferenceRuleDeclaration<inference_rule_declaration_python_class>` .

    TODO: AxiomInterpretation (Declaration and Inclusion): Add a data validation step to assure that parameter p is propositional.
    TODO: AxiomInterpretation (Declaration and Inclusion): Add a verification step: the axiom is not locked.

    """

    class Premises(typing.NamedTuple):
        """This python NamedTuple is used behind the scene as a data structure to manipulate the premises required by the :ref:`inference-rule<inference_rule_math_concept>` .
        """
        a: AxiomInclusion
        p: FormulaStatement

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'axiom-interpretation'
        acronym = 'ai'
        abridged_name = None
        auto_index = False
        dashed_name = 'axiom-interpretation'
        explicit_name = 'axiom interpretation inference rule'
        name = 'axiom interpretation'
        with u.v(symbol=ScriptNormal('A')) as a, u.v(symbol='P') as p:
            definition = (a | u.r.sequent_comma | p) | u.r.proves | p
        with u.v(symbol=ScriptNormal('A')) as a:
            self.parameter_a = a
            self.parameter_a_mask = frozenset([a])
        with u.v(symbol='P') as p:
            self.parameter_p = p
            self.parameter_p_mask = frozenset([p])
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, a: AxiomInclusion, p: FlexibleFormula) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # TODO: NICETOHAVE: AxiomInterpretationDeclaration: replace this verify statement with a generic validate_axiom_inclusion function.
        ok: bool
        p: (None, Formula)
        msg: (None, str)
        verify(assertion=isinstance(a, AxiomInclusion),
            msg=f'⌜{a}⌝ passed as premise ⌜a⌝ is not an axiom-inclusion.', a=a)
        ok, p, msg = verify_formula(arg='p', input_value=p, u=self.u, raise_exception=True)
        # TODO: Bug #217: assure that atomic formula are supported by verify_formula and verify_formula_statements #217
        # validate_formula does not support basic masks like: ⌜P⌝ where P is a free-variable.
        # validate_formula(u=self.u, input_value=p, form=self.i.parameter_p,
        #    mask=self.i.parameter_p_mask)
        output: Formula = p
        return output


class BiconditionalElimination1Declaration(InferenceRuleDeclaration):
    """This python class models the declaration of the :ref:`absorption<absorption_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .

    Acronym: be1.
    """

    class Premises(typing.NamedTuple):
        p_iff_q: FormulaStatement

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'biconditional-elimination-1'
        auto_index = False
        dashed_name = 'biconditional-elimination-1'
        acronym = 'be1'
        abridged_name = None
        explicit_name = 'biconditional elimination #1 inference rule'
        name = 'biconditional elimination #1'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.iff | q) | u.r.proves | (p | u.r.implies | q))
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            self.parameter_p_iff_q = p | u.r.iff | q
            self.parameter_p_iff_q_mask = frozenset([p, q])
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_iff_q: FormulaStatement = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        ok: bool
        msg: (None, msg)
        ok, p_iff_q, msg = verify_formula(arg='p_iff_q', input_value=p_iff_q, u=self.u,
            form=self.parameter_p_iff_q, mask=self.parameter_p_iff_q_mask, raise_exception=True)
        p_iff_q: Formula
        p: Formula = p_iff_q.parameters[0]
        q: Formula = p_iff_q.parameters[1]
        output = (p | self.u.r.implies | q)
        return output


class BiconditionalElimination2Declaration(InferenceRuleDeclaration):
    """The well-known biconditional elimination #1 inference rule: P ⟺ Q ⊢ Q ⟹ P.

    Acronym: ber.
    """

    class Premises(typing.NamedTuple):
        p_iff_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'biconditional-elimination-2'
        auto_index = False
        dashed_name = 'biconditional-elimination-2'
        acronym = 'be2'
        abridged_name = None
        explicit_name = 'biconditional elimination #2 inference rule'
        name = 'biconditional elimination #2'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.iff | q) | u.r.proves | (q | u.r.implies | p))
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            self.parameter_p_iff_q = p | u.r.iff | q
            self.parameter_p_iff_q_mask = frozenset([p, q])
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_iff_q: FormulaStatement = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        ok: bool
        msg: (None, msg)
        ok, p_iff_q, msg = verify_formula(arg='p_iff_q', input_value=p_iff_q, u=self.u,
            form=self.parameter_p_iff_q, mask=self.parameter_p_iff_q_mask, raise_exception=True)
        p_iff_q: Formula
        p: Formula = p_iff_q.parameters[0]
        q: Formula = p_iff_q.parameters[1]
        output = (q | self.u.r.implies | p)
        return output


class BiconditionalIntroductionDeclaration(InferenceRuleDeclaration):
    """The well-known biconditional introduction inference rule: (P ⟹ Q), (Q ⟹ P) ⊢ (P ⟺ Q)

    Acronym: bi.
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula
        q_implies_p: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'biconditional-introduction'
        auto_index = False
        dashed_name = 'biconditional-introduction'
        acronym = 'bi'
        abridged_name = None
        explicit_name = 'biconditional introduction inference rule'
        name = 'biconditional introduction'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = (((p | u.r.implies | q) | u.r.sequent_comma | (
                    q | u.r.implies | p)) | u.r.proves | (p | u.r.iff | q))
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            self.parameter_p_implies_q = p | u.r.implies | q
            self.parameter_p_implies_q_mask = frozenset([p, q])
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            self.parameter_q_implies_p = q | u.r.iff | p
            self.parameter_q_implies_p_mask = frozenset([p, q])
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, p_iff_q: FormulaStatement = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        ok: bool
        msg: (None, msg)
        ok, p_implies_q, msg = verify_formula(arg='p_implies_q', input_value=p_implies_q, u=self.u,
            form=self.parameter_p_implies_q, mask=self.parameter_p_implies_q_mask,
            raise_exception=True)
        p_implies_q: Formula
        ok, q_implies_p, msg = verify_formula(arg='q_implies_p', input_value=q_implies_p, u=self.u,
            form=self.parameter_q_implies_p, mask=self.parameter_q_implies_p_mask,
            raise_exception=True)
        q_implies_p: Formula
        p_implies_q__p: Formula = p_implies_q.parameters[0]
        # TODO: Do not is but use is_syntactically_equivalent instead.
        verify(assertion=p_implies_q.parameters[0] is p_implies_q.parameters[1], msg='The ⌜p⌝ in ',
            severity=verification_severities.error, raise_exception=True)
        p: Formula = p_implies_q.parameters[0]
        q: Formula = p_implies_q.parameters[1]
        output = (q | self.u.r.implies | p)
        return output


class ConjunctionElimination1Declaration(InferenceRuleDeclaration):
    """The well-known conjunction elimination #1 inference rule: P ⟺ Q ⊢ P ⟹ Q.

    Acronym: cel.
    """

    class Premises(typing.NamedTuple):
        p_and_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'conjunction-elimination-1'
        auto_index = False
        dashed_name = 'conjunction-elimination-1'
        acronym = 'ce1'
        abridged_name = None
        explicit_name = 'conjunction elimination #1 inference rule'
        name = 'conjunction elimination #1'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.land | q) | u.r.proves | p)
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p_and_q: FormulaStatement = None, t: TheoryElaborationSequence = None,
            echo: (None, bool) = None, **kwargs) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = unpack_formula(p_and_q).parameters[0]
        return p


class ConjunctionElimination2Declaration(InferenceRuleDeclaration):
    """The well-known conjunction elimination #2 inference rule: P ⟺ Q ⊢ Q ⟹ P.

    Acronym: cer.

    :param p_land_q: A formula-statement of the form: (P ⋀ Q).
    :param t: The current theory-elaboration-sequence.
    :return: The (proven) formula: Q.
    """

    class Premises(typing.NamedTuple):
        p_and_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'conjunction-elimination-2'
        auto_index = False
        dashed_name = 'conjunction-elimination-2'
        acronym = 'ce2'
        abridged_name = None
        explicit_name = 'conjunction elimination #2 inference rule'
        name = 'conjunction elimination #2'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.land | q) | u.r.proves | q)
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p_and_q: FormulaStatement = None, t: TheoryElaborationSequence = None,
            echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p_and_q = verify_formula(u=t.u, arity=2, input_value=p_and_q)
        q = p_and_q.parameters[1]
        return q


class ConjunctionIntroductionDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`conjunction-introduction<conjunction_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p: FlexibleFormula
        q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'conjunction-introduction'
        acronym = 'ci'
        abridged_name = None
        auto_index = False
        dashed_name = 'conjunction-introduction'
        explicit_name = 'conjunction introduction inference rule'
        name = 'conjunction introduction'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.sequent_comma | q) | u.r.proves | (p | u.r.land | q))
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: FormulaStatement, q: FormulaStatement, t: TheoryElaborationSequence,
            echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=t.u, arity=None, input_value=p)
        q = verify_formula(u=t.u, arity=None, input_value=q)
        return p | t.u.r.land | q


class ConstructiveDilemmaDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`constructive-dilemma<constructive_dilemma_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    # TODO: BUG #218: It seems that ConstructiveDilemmaDeclaration is ill-defined. Review the litterature and assure that it is properly defined. As is it is synonymous to conjunction-introduction, this doesn't make sense.

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula
        r_implies_s: FlexibleFormula
        p_or_r: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'constructive-dilemma'
        acronym = 'cd'
        abridged_name = None
        auto_index = False
        dashed_name = 'constructive-dilemma'
        explicit_name = 'constructive dilemma inference rule'
        name = 'constructive dilemma'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q, u.v(symbol='R') as r, u.v(symbol='S') as s:
            # TODO: FEATURE #216: Review this definition once sequence-comma supports n-ary components.
            definition = ((p | u.r.implies | q) | u.r.sequent_comma | (
                    (r | u.r.implies | s) | u.r.sequent_comma | (p | u.r.lor | r))) | u.r.proves | (
                                 q | u.r.lor | s)
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p_implies_q: FormulaStatement, r_implies_s: FormulaStatement,
            p_or_r: FormulaStatement, t: TheoryElaborationSequence,
            echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p_implies_q = verify_formula(u=t.u, arity=None, input_value=p_implies_q)
        r_implies_s = verify_formula(u=t.u, arity=None, input_value=r_implies_s)
        p_or_r = verify_formula(u=t.u, arity=None, input_value=p_or_r)
        return p | t.u.r.land | q

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_constructive_dilemma_paragraph_proof(o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement, q: FormulaStatement,
            t: TheoryElaborationSequence) -> bool:
        """ """
        p = verify_formula_statement(t=t, arity=None, input_value=p)
        q = verify_formula_statement(t=t, arity=None, input_value=q)
        verify(t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.', p=p, t=t, slf=self)
        verify(t.contains_theoretical_objct(q),
            'Statement ⌜q⌝ must be contained in theory ⌜t⌝''s hierarchy.', q=q, t=t, slf=self)
        return True


class DefinitionInterpretationDeclaration(InferenceRuleDeclaration):
    """This python class models the :ref:`declaration<object_declaration_math_concept>` of the :ref:`definition-interpretation<definition_interpretation_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>`.

    Inherits from :ref:`InferenceRuleDeclaration<inference_rule_declaration_python_class>` .

    TODO: DefinitionInterpretation (Declaration and Inclusion): Add a data validation step to assure that parameter p is propositional.
    TODO: DefinitionInterpretation (Declaration and Inclusion): Add a verification step: the axiom is not locked.

    """

    class Premises(typing.NamedTuple):
        """This python NamedTuple is used behind the scene as a data structure to manipulate the premises required by the :ref:`inference-rule<inference_rule_math_concept>` .
        """
        d: DefinitionInclusion
        x_equal_y: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'definition-interpretation'
        acronym = 'di'
        abridged_name = None
        auto_index = False
        dashed_name = 'definition-interpretation'
        explicit_name = 'definition interpretation inference rule'
        name = 'definition interpretation'
        with u.v(symbol=ScriptNormal('D')) as d, u.v(symbol='x') as x, u.v(symbol='y') as y:
            # Feature #216: provide support for n-ary relations
            # Provide support for n-ary relations. First need: sequent-comma, or collection-comma.
            # definition = u.r.sequent_comma(d, x, y) | u.r.proves | (x | u.r.equal | y)
            # Meanwhile, I use combined 2-ary formulae:
            definition = d | u.r.sequent_comma | (x | u.r.sequent_comma | y) | u.r.proves | (
                    x | u.r.equal | y)
        with u.v(symbol=ScriptNormal('D')) as d:
            self.parameter_d = d
            self.parameter_d_mask = frozenset([d])
        with u.v(symbol='x') as x:
            self.parameter_x = x
            self.parameter_x_mask = frozenset([x])
        with u.v(symbol='y') as y:
            self.parameter_y = y
            self.parameter_y_mask = frozenset([y])
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def construct_formula(self, d: DefinitionInclusion, x: FlexibleFormula,
            y: FlexibleFormula) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # TODO: NICETOHAVE: DefinitionInterpretationDeclaration: replace this verify statement with a generic validate_definition_inclusion function.
        ok: bool
        output: Formula
        msg: (None, str)
        verify(assertion=isinstance(d, DefinitionInclusion),
            msg=f'⌜{d}⌝ passed as premise ⌜d⌝ is not a definition-inclusion.', d=d)
        ok, x, msg = verify_formula(arg='x', input_value=x, u=self.u, raise_exception=True)
        ok, y, msg = verify_formula(arg='y', input_value=y, u=self.u, raise_exception=True)
        # TODO: BUG: validate_formula does not support basic masks like: ⌜P⌝ where P is a free-variable.
        # validate_formula(u=self.u, input_value=p, form=self.i.parameter_p,
        #    mask=self.i.parameter_p_mask)
        output: Formula = x | self.u.r.equal | y
        return output


class DestructiveDilemmaDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`destructive-dilemma<destructive_dilemma_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'destructive-dilemma'
        acronym = 'dd'
        abridged_name = None
        auto_index = False
        dashed_name = 'destructive-dilemma'
        explicit_name = 'destructive dilemma inference rule'
        name = 'destructive dilemma'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.sequent_comma | q) | u.r.proves | (p | u.r.land | q))
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: FormulaStatement, q: FormulaStatement, t: TheoryElaborationSequence,
            echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=t.u, arity=None, input_value=p)
        q = verify_formula(u=t.u, arity=None, input_value=q)
        return p | t.u.r.land | q


class DisjunctionIntroduction1Declaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`disjunction-introduction-1<disjunction_introduction_1_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'disjunction-introduction-1'
        acronym = 'di1'
        abridged_name = None
        auto_index = False
        dashed_name = 'disjunction-introduction-1'
        explicit_name = 'disjunction introduction #1 inference rule'
        name = 'disjunction introduction #1'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = (p | u.r.proves | (q | u.r.lor | p))
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: FormulaStatement, q: (Formula, FormulaStatement),
            t: TheoryElaborationSequence, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=t.u, arity=None, input_value=p)
        q = verify_formula(u=t.u, arity=None, input_value=q)
        return q | t.u.r.lor | p


class DisjunctionIntroduction2Declaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`disjunction-introduction-2<disjunction_introduction_2_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'disjunction-introduction-2'
        acronym = 'di2'
        abridged_name = None
        auto_index = False
        dashed_name = 'disjunction-introduction-2'
        explicit_name = 'disjunction introduction #2 inference rule'
        name = 'disjunction introduction #2'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = (p | u.r.proves | (p | u.r.lor | q))
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: FormulaStatement, q: (Formula, FormulaStatement),
            t: TheoryElaborationSequence, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=t.u, arity=None, input_value=p)
        q = verify_formula(u=t.u, arity=None, input_value=q)
        return p | t.u.r.lor | q


class DisjunctiveResolutionDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`disjunctive-resolution<disjunctive_resolution_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'disjunctive-resolution'
        acronym = 'dr'
        abridged_name = None
        auto_index = False
        dashed_name = 'disjunctive-resolution'
        explicit_name = 'disjunctive resolution inference rule'
        name = 'disjunctive resolution'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.sequent_comma | q) | u.r.proves | (p | u.r.land | q))
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: FormulaStatement, q: FormulaStatement, t: TheoryElaborationSequence,
            echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=t.u, arity=None, input_value=p)
        q = verify_formula(u=t.u, arity=None, input_value=q)
        return p | t.u.r.land | q


class DisjunctiveSyllogismDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`disjunctive-syllogism<disjunctive_syllogism_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'disjunctive-syllogism'
        acronym = 'ds'
        abridged_name = None
        auto_index = False
        dashed_name = 'disjunctive-syllogism'
        explicit_name = 'disjunctive syllogism inference rule'
        name = 'disjunctive syllogism'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.sequent_comma | q) | u.r.proves | (p | u.r.land | q))
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: FormulaStatement, q: FormulaStatement, t: TheoryElaborationSequence,
            echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=t.u, arity=None, input_value=p)
        q = verify_formula(u=t.u, arity=None, input_value=q)
        return p | t.u.r.land | q


class DoubleNegationEliminationDeclaration(InferenceRuleDeclaration):
    """The well-known double negation elimination #1 inference rule: ¬(¬(P)) ⊢ P.

    Acronym: cer.

    :param p_land_q: A formula-statement of the form: (P ⋀ Q).
    :param t: The current theory-elaboration-sequence.
    :return: The (proven) formula: Q.
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'double-negation-elimination'
        auto_index = False
        dashed_name = 'double-negation-elimination'
        acronym = 'dne'
        abridged_name = None
        explicit_name = 'double negation elimination inference rule'
        name = 'double negation elimination'
        with u.v(symbol='P') as p:
            definition = (u.r.lnot(u.r.lnot(p)) | u.r.proves | p)
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, not_not_p: (None, Formula) = None, t: TheoryElaborationSequence = None,
            echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        not_not_p: Formula = verify_formula(u=t.u, arity=1, input_value=not_not_p)
        not_p: Formula = not_not_p.parameters[0]
        p: Formula = not_p.parameters[0]
        return p


class DoubleNegationIntroductionDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`double-negation-introduction<double_negation_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'double-negation-introduction'
        auto_index = False
        dashed_name = 'double-negation-introduction'
        acronym = 'dni'
        abridged_name = None
        explicit_name = 'double negation introduction inference rule'
        name = 'double negation introduction'
        with u.v(symbol='P') as p:
            definition = (p | u.r.proves | u.r.lnot(u.r.lnot(p)))
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: (None, Formula, FormulaStatement) = None,
            t: TheoryElaborationSequence = None, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p: Formula = verify_formula(arg='p', u=t.u, arity=1, input_value=p)
        not_not_p: Formula = t.u.r.lnot(t.u.r.lnot(p))
        return not_not_p


class EqualityCommutativityDeclaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'equality-commutativity'
        acronym = 'ec'
        abridged_name = None
        auto_index = False
        dashed_name = 'equality-commutativity'
        explicit_name = 'equality commutativity inference rule'
        name = 'equality commutativity'
        with u.v(symbol='x') as x, u.v(symbol='y') as y:
            definition = (x | u.r.equal | y) | u.r.proves | (y | u.r.equal | x)
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, x_equal_y: (None, FormulaStatement) = None,
            t: TheoryElaborationSequence = None, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        x_equal_y: Formula
        x_equal_y = unpack_formula(x_equal_y)
        x = x_equal_y.parameters[0]
        y = x_equal_y.parameters[1]
        return t.u.f(t.u.r.equality, y, x)


class EqualTermsSubstitutionDeclaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'equal-terms-substitution'
        acronym = 'ets'
        abridged_name = None
        auto_index = False
        dashed_name = 'equal-terms-substitution'
        explicit_name = 'equal terms substitution inference rule'
        name = 'equal terms substitution'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q, u.v(symbol='x') as x, u.v(symbol='y') as y:
            definition = (p | u.r.sequent_comma | (x | u.r.equal | y)) | u.r.proves | q
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: FormulaStatement = None, x_equal_y: FormulaStatement = None,
            t: TheoryElaborationSequence = None, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p: Formula
        x_equal_y: Formula
        p = unpack_formula(p)
        x_equal_y = unpack_formula(x_equal_y)
        q = x_equal_y.parameters[0]
        r = x_equal_y.parameters[1]
        substitution_map = {q: r}
        p_prime = p.substitute(substitution_map=substitution_map, target_theory=t,
            lock_variable_scope=True)
        return p_prime  # TODO: EqualTermsSubstitution: Provide support for statements that are  # atomic propositional formula, that is without relation or where the objct is a 0-ary  #  # relation.


class HypotheticalSyllogismDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`hypothetical-syllogism<hypothetical_syllogism_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` as valid in the target :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'hypothetical-syllogism'
        acronym = 'hs'
        abridged_name = None
        auto_index = False
        dashed_name = 'hypothetical-syllogism'
        explicit_name = 'hypothetical syllogism inference rule'
        name = 'hypothetical syllogism'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.sequent_comma | q) | u.r.proves | (p | u.r.land | q))
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: FormulaStatement, q: FormulaStatement, t: TheoryElaborationSequence,
            echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=t.u, arity=None, input_value=p)
        q = verify_formula(u=t.u, arity=None, input_value=q)
        return p | t.u.r.land | q


class InconsistencyIntroduction1Declaration(InferenceRuleDeclaration):
    """P ⋀ not P: inconsistency"""

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'inconsistency-introduction-1'
        acronym = 'ii1'
        abridged_name = None
        auto_index = False
        dashed_name = 'inconsistency-introduction-1'
        explicit_name = 'inconsistency introduction #1 inference rule'
        name = 'inconsistency introduction #1'
        definition = StyledText(plaintext='(P, not(P)) |- (T)', unicode='(𝑷, ¬(𝑷)) ⊢ 𝐼𝑛𝑐(𝓣)')
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: FormulaStatement = None, not_p: FormulaStatement = None,
            inconsistent_theory: TheoryElaborationSequence = None,
            t: TheoryElaborationSequence = None, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = unpack_formula(p)
        not_p = unpack_formula(not_p)
        return t.u.f(t.u.r.inconsistency, inconsistent_theory)


class InconsistencyIntroduction2Declaration(InferenceRuleDeclaration):
    """P = Q ⋀ P neq Q: inconsistency """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'inconsistency-introduction-2'
        acronym = 'ii2'
        abridged_name = None
        auto_index = False
        dashed_name = 'inconsistency-introduction-2'
        explicit_name = 'inconsistency introduction #2 inference rule'
        name = 'inconsistency introduction #2'
        definition = StyledText(plaintext='((P = Q), (P neq Q)) |- Inc(T)',
            unicode='((𝑷 = 𝑸), (𝑷 ≠ 𝑸)) ⊢ 𝐼𝑛𝑐(𝒯)')
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, x_eq_y: FormulaStatement = None, x_neq_y: FormulaStatement = None,
            inconsistent_theory: TheoryElaborationSequence = None,
            t: TheoryElaborationSequence = None, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        x_eq_y = unpack_formula(x_eq_y)
        x_neq_y = unpack_formula(x_neq_y)
        return t.u.f(t.u.r.inconsistency, inconsistent_theory)


class InconsistencyIntroduction3Declaration(InferenceRuleDeclaration):
    """P neq P: inconsistency """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'inconsistency-introduction-3'
        acronym = 'ii3'
        abridged_name = None
        auto_index = False
        dashed_name = 'inconsistency-introduction-3'
        explicit_name = 'inconsistency introduction #3 inference rule'
        name = 'inconsistency introduction #3'
        definition = StyledText(plaintext='(P neq P) |- Inc(T)', unicode='(𝑷 ≠ 𝑷) ⊢ Inc(𝒯)')
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p_neq_p: FormulaStatement = None,
            inconsistent_theory: TheoryElaborationSequence = None,
            t: TheoryElaborationSequence = None, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p_neq_p = verify_formula(u=self.u, arity=2, input_value=p_neq_p)
        return t.u.f(t.u.r.inconsistency, inconsistent_theory)


class ModusPonensDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`modus-ponens<modus_ponens_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'modus-ponens'
        acronym = 'mp'
        abridged_name = None
        auto_index = False
        dashed_name = 'modus-ponens'
        explicit_name = 'modus ponens inference rule'
        name = 'modus ponens'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.implies | p) | u.r.sequent_comma | p) | u.r.proves | q
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p_implies_q: FormulaStatement, p: FormulaStatement,
            t: TheoryElaborationSequence, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p_implies_q = verify_formula(u=self.u, arity=2, input_value=p_implies_q)
        q = verify_formula(u=self.u, arity=2, input_value=p_implies_q.parameters[1])
        return q


class ModusTollensDeclaration(InferenceRuleDeclaration):
    """The declaration of the :ref:`modus-tollens<modus_tollens_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        u: UniverseOfDiscourse = universe_of_discourse
        symbol = 'modus-tollens'
        acronym = 'mt'
        abridged_name = None
        auto_index = False
        dashed_name = 'modus-tollens'
        explicit_name = 'modus tollens inference rule'
        name = 'modus tollens'
        with u.v(symbol='P') as p, u.v(symbol='Q') as q:
            definition = ((p | u.r.implies | p) | u.r.sequent_comma | p) | u.r.proves | q
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p_implies_q: FormulaStatement, p: FormulaStatement,
            t: TheoryElaborationSequence, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p_implies_q = verify_formula(u=self.u, arity=2, input_value=p_implies_q)
        q = verify_formula(u=self.u, arity=2, input_value=p_implies_q.parameters[1])
        return q


class ProofByContradiction1Declaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'proof-by-contradiction'
        acronym = 'pbc'
        auto_index = False
        dashed_name = 'proof-by-contradiction'
        explicit_name = 'proof by contradiction inference rule'
        name = 'proof by contradiction'
        definition = StyledText(plaintext='(H assume not(P), P, Inc(H)) |- P',
            unicode='(𝓗 𝑎𝑠𝑠𝑢𝑚𝑒 ¬𝑷, 𝑷, 𝐼𝑛𝑐(𝓗)) ⊢ 𝑷')
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, not_p_hypothesis: Hypothesis, inc_hypothesis: FormulaStatement,
            t: TheoryElaborationSequence, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        not_p = not_p_hypothesis.hypothesis_formula
        p = not_p.parameters[0]
        return p


class ProofByContradiction2Declaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'proof-by-contradiction-2'
        acronym = 'pbc2'
        auto_index = False
        dashed_name = 'proof-by-contradiction-2'
        explicit_name = 'proof by contradiction #2 inference rule'
        name = 'proof by contradiction #2'
        definition = '(𝓗 𝑎𝑠𝑠𝑢𝑚𝑒 (𝑷 ≠ 𝑸), 𝐼𝑛𝑐(𝓗)) ⊢ (𝑷 = 𝑸)'
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, x_neq_y_hypothesis: Hypothesis, inc_hypothesis: FormulaStatement,
            t: TheoryElaborationSequence, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        x_neq_y = x_neq_y_hypothesis.hypothesis_formula
        x = x_neq_y.parameters[0]
        y = x_neq_y.parameters[1]
        # Alternatively: not(x = y)
        return t.u.f(t.u.r.equality, x, y)


class ProofByRefutation1Declaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'proof-by-refutation'
        acronym = 'pbr'
        auto_index = False
        dashed_name = 'proof-by-refutation'
        explicit_name = 'proof by refutation inference rule'
        name = 'proof by refutation'
        definition = '(𝓗 𝑎𝑠𝑠𝑢𝑚𝑒 𝑷, 𝐼𝑛𝑐(𝓗)) ⊢ ¬𝑷'
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p_hypothesis: Hypothesis, inc_hypothesis: FormulaStatement,
            t: TheoryElaborationSequence, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = p_hypothesis.hypothesis_formula
        not_p = t.u.f(t.u.r.negation, p)
        return not_p


class ProofByRefutation2Declaration(InferenceRuleDeclaration):
    """This python class models the inclusion of :ref:`proof-by-refutation-2<proof_by_refutation_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'proof-by-refutation-2'
        acronym = 'pbr2'
        auto_index = False
        dashed_name = 'proof-by-refutation-2'
        explicit_name = 'proof by refutation #2 inference rule'
        name = 'proof by refutation #2'
        definition = '(𝓗 𝑎𝑠𝑠𝑢𝑚𝑒 (𝑷 = 𝑸), 𝐼𝑛𝑐(𝓗)) ⊢ (𝑷 ≠ 𝑸)'
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p_eq_q_hypothesis: Hypothesis, inc_hypothesis: FormulaStatement,
            t: TheoryElaborationSequence, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p_eq_q = p_eq_q_hypothesis.hypothesis_formula
        p_neq_q = t.u.f(t.u.r.inequality, p_eq_q.parameters[0], p_eq_q.parameters[1])
        return p_neq_q


class VariableSubstitutionDeclaration(InferenceRuleDeclaration):
    class Premises(typing.NamedTuple):
        p_implies_q: FlexibleFormula

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, echo: (None, bool) = None):
        symbol = 'variable-substitution'
        acronym = 'vs'
        abridged_name = None
        auto_index = False
        dashed_name = 'variable-substitution'
        explicit_name = 'variable substitution inference rule'
        name = 'variable substitution'
        definition = StyledText(plaintext='(P, Phi) |- P\'', unicode='(P, 𝛷) ⊢ P\'')
        super().__init__(definition=definition, universe_of_discourse=universe_of_discourse,
            symbol=symbol, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo)

    def infer_formula(self, p: FormulaStatement, phi: (None, tuple[TheoreticalObject]),
            t: TheoryElaborationSequence, echo: (None, bool) = None, **kwargs) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        x_oset = unpack_formula(p).get_variable_ordered_set()
        x_y_map = dict((x, y) for x, y in zip(x_oset, phi))
        p_prime = p.valid_proposition.substitute(substitution_map=x_y_map, target_theory=t)
        return p_prime


class AtheoreticalStatement(SymbolicObject):
    """
    Definition
    ----------
    An atheoretical-statement is a statement that is contained in a theory report
    for commentary / explanatory purposes, but that is not mathematically constitutive
    of the theory. Atheoretical-statements may be added and/or removed from a
    theory without any impact to the theory sequence of proofs.

    """

    def __init__(self, theory: TheoryElaborationSequence, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        self.theory = theory
        super().__init__(universe_of_discourse=theory.universe_of_discourse, symbol=symbol,
            index=index, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, nameset=nameset,
            echo=echo)
        super()._declare_class_membership(classes.atheoretical_statement)


class NoteInclusion(AtheoreticalStatement):
    """The Note pythonic-class models a note, comment, or remark in a theory.

    """

    def __init__(self, t: TheoryElaborationSequence, content: str,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):

        echo = prioritize_value(echo, configuration.echo_note, configuration.echo_default, False)
        verify(is_in_class(t, classes.t), 'theory is not a member of declarative-class theory.',
            t=t, slf=self)
        universe_of_discourse = t.universe_of_discourse
        paragraph_header = paragraph_headers.note if paragraph_header is None else paragraph_header
        #  self.statement_index = theory.crossreference_statement(self)
        self.theory = t
        if isinstance(content, str):
            content = SansSerifNormal(content)
        self._natural_language = content
        self.category = paragraph_header
        if nameset is None and symbol is None:
            # symbol = self.category.symbol_base
            symbol = paragraph_header.symbol_base
            index = universe_of_discourse.index_symbol(symbol=symbol) if auto_index else index
        if isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            symbol = StyledText(plaintext=nameset, text_style=text_styles.serif_italic)
            index = universe_of_discourse.index_symbol(symbol=symbol) if auto_index else index
        super().__init__(theory=t, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref,
            subtitle=subtitle, nameset=nameset, echo=False)
        if echo:
            self.echo()
        super()._declare_class_membership(declarative_class_list.note)

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


section_category = ParagraphHeader(name='section', symbol_base='§', natural_name='section',
    abridged_name='sect.')


class Section(AtheoreticalStatement):
    """A (leveled) section in a theory-elaboration-sequence.

    Sections allow to organize / structure (lengthy) theory-elaboration-sequences
    to improve readability.

    """

    def __init__(self, section_title: str, t: TheoryElaborationSequence,
            section_number: (None, int) = None, section_parent: (None, Section) = None,
            numbering: (None, bool) = None, echo: (None, bool) = None):
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
        symbol = NameSet(symbol=self.category.symbol_base, index=self.statement_index)
        super().__init__(nameset=symbol, theory=t, echo=False)
        super()._declare_class_membership(declarative_class_list.note)
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
        prefix = 'section' if self.section_level == 1 else 'sub-' * (
                self.section_level - 1) + 'section'
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


class TheoryElaborationSequence(TheoreticalObject):
    """The TheoryElaboration pythonic class models a [theory-elaboration](theory-elaboration).

    """

    def __init__(self, u: UniverseOfDiscourse, symbol: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            subtitle: (None, str) = None, extended_theory: (None, TheoryElaborationSequence) = None,
            extended_theory_limit: (None, Statement) = None, stabilized: bool = False,
            echo: bool = None):
        echo = prioritize_value(echo, configuration.echo_theory_elaboration_sequence_declaration,
            configuration.echo_default, False)
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
        if nameset is None:
            symbol = prioritize_value(symbol, configuration.default_theory_symbol)
            index = u.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index)
        elif isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            symbol = StyledText(plaintext=nameset, text_style=text_styles.script_normal)
            index = u.index_symbol(symbol=symbol)
            nameset = NameSet(s=symbol, index=index)
        nameset.paragraph_header = paragraph_headers.theory_elaboration_sequence
        nameset.ref = ref
        nameset.subtitle = subtitle
        super().__init__(nameset=nameset, paragraph_header=nameset.paragraph_header,
            is_theory_foundation_system=True if extended_theory is None else False,
            universe_of_discourse=u, echo=False)
        verify(is_in_class(u, classes.universe_of_discourse),
            'Parameter "u" is not a member of declarative-class universe-of-discourse.', u=u)
        verify(extended_theory is None or is_in_class(extended_theory, classes.theory_elaboration),
            'Parameter "extended_theory" is neither None nor a member of declarative-class theory.',
            u=u)
        verify(extended_theory_limit is None or (
                extended_theory is not None and is_in_class(extended_theory_limit,
            classes.statement) and extended_theory_limit in extended_theory.statements),
            'Parameter "theory_extension_statement_limit" is inconsistent.', u=u)
        super()._declare_class_membership(classes.theory_elaboration)
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
            self.take_note(
                'By design, punctilious assures the syntactical correctness of theories, '
                'but does not perform any '
                'semantic verification. Therefore, the usage of inference-rules that interpret '
                'natural content (i.e. '
                'axiom-interpretation and definition-interpretation) is critically dependent on '
                'the correctness of '
                'the content translation performed by the theory author, from axiom or definition '
                'natural language, '
                'to formulae.', paragraph_header=paragraph_headers.warning, echo=echo)
            self._interpretation_disclaimer = True

    def compose_article(self, proof: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Return a representation that expresses and justifies the theory."""
        # TODO: compose_article: move this outside of the theory
        output = yield from configuration.locale.compose_theory_article(t=self, proof=proof)
        return output

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='theory-elaboration-sequence')

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
        """Return the dictionary of inference-rule-inclusions contained in this
theory-elaboration."""
        return self.inference_rule_inclusions

    @property
    def inference_rule_inclusions(self):
        """Return the dictionary of inference-rule-inclusions contained in this
        theory-elaboration."""
        return self._inference_rule_inclusions

    def iterate_theoretical_objcts_references(self, include_root: bool = True,
            visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it references recursively.

        Theoretical-objcts may contain references to multiple and diverse other theoretical-objcts. Do not confuse this iteration of all references with iterations of objects in the theory-chain.

        :parameter include_root:
        :parameter visited:
        :return:
        """
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        for statement in set(self.statements).difference(visited):
            if not is_in_class(statement, declarative_class_list.atheoretical_statement):
                yield statement
                visited.update({statement})
                yield from statement.iterate_theoretical_objcts_references(include_root=False,
                    visited=visited)
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
            yield from self.extended_theory.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)

    def include_axiom(self, a: AxiomDeclaration, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            paragraph_header: (None, ParagraphHeader) = None,
            echo: (None, bool) = None) -> AxiomInclusion:
        """Include an axiom in this theory-elaboration-sequence."""
        return AxiomInclusion(a=a, t=self, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle,
            paragraph_header=paragraph_header, nameset=nameset, echo=echo)

    def include_definition(self, d: DefinitionDeclaration, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None) -> DefinitionInclusion:
        """Include a definition in this theory-elaboration-sequence."""
        return DefinitionInclusion(d=d, t=self, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle, nameset=nameset, echo=echo)

    def iterate_statements_in_theory_chain(self, formula: (None, Formula) = None):
        """Iterate through the (proven or sound) statements in the current theory-chain.

        :param formula: (conditional) Filters on formula-statements that are formula-syntactically-equivalent.
        :return:
        """
        if formula is not None:
            formula = verify_formula(u=self.u, arity=None, input_value=formula)
        for t in self.iterate_theory_chain():
            for s in t.statements:
                if formula is None or (is_in_class(s,
                        classes.formula_statement) and s.is_formula_syntactically_equivalent_to(
                    formula)):
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
        return self.include_definition(natural_language=natural_language, nameset=symbol,
            reference=reference, title=title)

    def get_first_syntactically_equivalent_statement(self, formula: (None, Formula) = None):
        """Given a formula, return the first statement that is syntactically-equivalent with it, or None if none are found.

        :param formula:
        :return:
        """
        return next(self.iterate_statements_in_theory_chain(formula=formula), None)

    def pose_hypothesis(self, hypothesis_formula: Formula, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None) -> Hypothesis:
        """Pose a new hypothesis in the current theory."""
        hypothesis_formula = verify_formula(u=self.u, arity=None, input_value=hypothesis_formula)
        return Hypothesis(t=self, hypothesis_formula=hypothesis_formula, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, nameset=nameset, echo=echo)

    def prnt(self, proof: (None, bool) = None):
        repm.prnt(self.rep_report(proof=proof))

    def prove_inconsistent(self, ii):
        verify(isinstance(ii, InconsistencyIntroductionStatement),
            'The ii statement is not of type InconsistencyIntroductionStatement.', ii=ii,
            theory=self)
        verify(ii in self.statements, 'The ii statement is not a statement of this theory.', ii=ii,
            theory=self)
        self._consistency = consistency_values.proved_inconsistent

    def export_article_to_file(self, file_path, proof: (None, bool) = None,
            encoding: (None, Encoding) = None):
        """Export this theory to a Unicode textfile."""
        text_file = open(file_path, 'w', encoding='utf-8')
        n = text_file.write(self.rep_article(encoding=encoding, proof=proof))
        text_file.close()

    def open_section(self, section_title: str, section_number: (None, int) = None,
            section_parent: (None, Section) = None, numbering: (None, bool) = None,
            echo: (None, bool) = None) -> Section:
        """Open a new section in the current theory-elaboration-sequence."""
        return Section(section_title=section_title, section_number=section_number,
            section_parent=section_parent, numbering=numbering, t=self, echo=echo)

    def rep_article(self, encoding: (None, Encoding) = None, proof: (None, bool) = None) -> str:
        encoding = prioritize_value(encoding, configuration.encoding, encodings.plaintext)
        return rep_composition(composition=self.compose_article(proof=proof), encoding=encoding)

    def report_inconsistency_proof(self, proof: InferredStatement):
        """This method is called by InferredStatement.__init__() when the inferred-statement
         proves the inconsistency of a theory."""
        verify(is_in_class(proof, classes.inferred_proposition),
            '⌜proof⌝ must be an inferred-statement.', proof=proof, slf=self)
        proof: Formula
        proof = unpack_formula(proof)
        verify(proof.relation is self.u.r.inconsistency,
            'The relation of the ⌜proof⌝ formula must be ⌜inconsistency⌝.',
            proof_relation=proof.relation, proof=proof, slf=self)
        verify(proof.parameters[0] is self,
            'The parameter of the ⌜proof⌝ formula must be the current theory, i.e. ⌜self⌝.',
            proof_parameter=proof.parameters[0], proof=proof, slf=self)
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

    def take_note(self, content: str, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None) -> NoteInclusion:
        """Take a note, make a comment, or remark in this theory.
        """
        return self.universe_of_discourse.take_note(t=self, content=content, symbol=symbol,
            index=index, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, nameset=nameset,
            echo=echo)

    @property
    def theoretical_objcts(self):
        list = set()
        for s in self.statements:
            list.add(s)
            if is_in_class(s, classes.formula):
                list.add()


class Hypothesis(Statement):
    def __init__(self, t: TheoryElaborationSequence, hypothesis_formula: Formula,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None):
        paragraph_header = paragraph_headers.hypothesis
        # TODO: Check that all components of the hypothetical-proposition
        #  are elements of the source theory-branch.
        verify(hypothesis_formula.is_proposition, 'The hypothetical-formula is not a proposition.',
            hypothetical_formula=hypothesis_formula, slf=self)
        if isinstance(symbol, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            symbol = StyledText(plaintext=symbol, text_style=text_styles.serif_italic)
            index = t.u.index_symbol(symbol=symbol)
        elif symbol is None:
            symbol = configuration.default_parent_hypothesis_statement_symbol
            index = t.u.index_symbol(symbol=symbol)

        super().__init__(theory=t, symbol=symbol, index=index, paragraph_header=paragraph_header,
            nameset=nameset, subtitle=subtitle, dashed_name=dashed_name, echo=False)
        super()._declare_class_membership(declarative_class_list.hypothesis)
        self._hypothesis_formula = hypothesis_formula
        # When a hypothesis is posed in a theory 𝒯₁,
        # ...the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        self._hypothesis_axiom_declaration = self.universe_of_discourse.declare_axiom(
            f'By hypothesis, assume {hypothesis_formula.rep_formula()} is true.', echo=echo)
        # ...a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        self._hypothesis_child_theory = t.universe_of_discourse.t(extended_theory=t,
            extended_theory_limit=self, symbol=configuration.default_child_hypothesis_theory_symbol,
            echo=echo)
        # ...the axiom is included in 𝒯₂,
        self._hypothesis_axiom_inclusion_in_child_theory = self.hypothesis_child_theory.include_axiom(
            a=self.hypothesis_axiom_declaration, echo=echo)
        # ...and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂.
        self._hypothesis_statement_in_child_theory = self.hypothesis_child_theory.i.axiom_interpretation.infer_formula_statement(
            self.hypothesis_axiom_inclusion_in_child_theory, hypothesis_formula, echo=echo)
        echo = prioritize_value(echo, configuration.echo_hypothesis,
            configuration.echo_inferred_statement, False)
        if echo:
            self.echo()

    @property
    def child_theory(self) -> TheoryElaborationSequence:
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
        output = yield from configuration.locale.compose_parent_hypothesis_statement_report(o=self,
            proof=proof)
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
    def hypothesis_formula(self) -> Formula:
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
    def hypothesis_child_theory(self) -> TheoryElaborationSequence:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothesis_child_theory


class Relation(TheoreticalObject):
    """The Relation pythonic class is the implementation of the relation theoretical-object.
    """

    def __init__(self, universe_of_discourse: UniverseOfDiscourse, arity: (None, int) = None,
            min_arity: (None, int) = None, max_arity: (None, int) = None,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, formula_rep=None, signal_proposition=None,
            signal_theoretical_morphism=None, implementation=None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """

        :param universe_of_discourse:
        :param arity: A fixed arity constraint for well-formed formula. Formulae based on this relation with distinct arity are ill-formed. Equivalent to passing the same value to both min_arity, and max_arity.
        :param min_arity: A fixed minimum (inclusive) arity constraint for well-formed formula. Formulae based on this relation with lesser arity are ill-formed.
        :param max_arity: A fixed maximum (inclusive) arity constraint for well-formed formula. Formulae based on this relation with greater arity are ill-formed.
        :param symbol:
        :param index:
        :param auto_index:
        :param formula_rep:
        :param signal_proposition:
        :param signal_theoretical_morphism:
        :param implementation:
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
        echo = prioritize_value(echo, configuration.echo_relation, configuration.echo_default,
            False)
        auto_index = prioritize_value(auto_index, configuration.auto_index, True)
        assert isinstance(universe_of_discourse, UniverseOfDiscourse)
        signal_proposition = False if signal_proposition is None else signal_proposition
        signal_theoretical_morphism = False if signal_theoretical_morphism is None else signal_theoretical_morphism
        assert isinstance(signal_proposition, bool)
        assert isinstance(signal_theoretical_morphism, bool)
        cat = paragraph_headers.relation_declaration
        self.formula_rep = Formula.function_call if formula_rep is None else formula_rep
        self.signal_proposition = signal_proposition
        self.signal_theoretical_morphism = signal_theoretical_morphism
        self.implementation = implementation
        self.arity = arity
        self.min_arity = min_arity
        self.max_arity = max_arity
        if nameset is None:
            symbol = configuration.default_relation_symbol if symbol is None else symbol
            index = universe_of_discourse.index_symbol(symbol=symbol) if auto_index else index
            nameset = NameSet(symbol=symbol, index=index, dashed_name=dashed_name, acronym=acronym,
                abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                paragraph_header=cat, ref=ref, subtitle=subtitle)
        super().__init__(universe_of_discourse=universe_of_discourse, nameset=nameset, echo=False)
        self.universe_of_discourse.cross_reference_relation(r=self)
        super()._declare_class_membership(classes.relation)
        if echo:
            self.echo()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((Relation, self.nameset, self.arity))

    def compose_class(self) -> collections.abc.Generator[Composable, Composable, bool]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='relation')
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
        yield SerifItalic('relation')
        yield SansSerifNormal(' in ')
        yield from self.universe_of_discourse.compose_symbol()
        yield SansSerifNormal(' (default notation: ')
        yield SansSerifNormal(str(self.formula_rep))
        yield SansSerifNormal(').')
        return True

    def echo(self):
        repm.prnt(self.rep_report())


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

    TODO: SimpleObjct: By design, a SimpleObjct should also be a Formula. As an immediate measure, I implement the method is_syntactic_equivalent() to make it compatible, but the data model should be improved.
    """

    def __init__(self, universe_of_discourse: UniverseOfDiscourse,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_simple_objct_declaration,
            configuration.echo_default, False)
        super().__init__(universe_of_discourse=universe_of_discourse, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, nameset=nameset, echo=False)
        self.universe_of_discourse.cross_reference_simple_objct(o=self)
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
        return self.is_formula_syntactically_equivalent_to(o2), _values


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

    def __init__(self, original_expression, equality_statement, nameset=None,
            paragraphe_header=None, theory=None, reference=None, title=None):
        paragraphe_header = paragraph_headers.proposition if paragraphe_header is None else paragraphe_header
        # Check p_implies_q consistency
        assert isinstance(theory, TheoryElaborationSequence)
        assert isinstance(original_expression, FormulaStatement)
        assert theory.contains_theoretical_objct(original_expression)
        assert isinstance(equality_statement, FormulaStatement)
        assert theory.contains_theoretical_objct(equality_statement)
        assert equality_statement.valid_proposition.relation is theory.universe_of_discourse.r.inequality
        left_term = equality_statement.valid_proposition.parameters[0]
        right_term = equality_statement.valid_proposition.parameters[1]
        self.original_expression = original_expression
        self.equality_statement = equality_statement
        substitution_map = {left_term: right_term}
        valid_proposition = original_expression.valid_proposition.substitute(
            substitution_map=substitution_map, target_theory=theory, lock_variable_scope=True)
        # Note: valid_proposition will be formula-syntactically-equivalent to self,
        #   if there are no occurrences of left_term in original_expression.
        super().__init__(theory=theory, valid_proposition=valid_proposition,
            paragraphe_header=paragraphe_header, nameset=nameset)

    def rep_report(self, proof: (None, bool) = None):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.rep_title(cap=True)}: {self.valid_proposition.rep_formula()}'
        if proof:
            output = output + f'\n\t{repm.serif_bold("Substitution of equal terms")}'
            output = output + f'\n\t{self.original_expression.rep_formula(expand=True):<70} │ ' \
                              f'Follows from {repm.serif_bold(self.original_expression.rep_ref())}.'
            output = output + f'\n\t{self.equality_statement.rep_formula(expand=True):<70} │ ' \
                              f'Follows from {repm.serif_bold(self.equality_statement.rep_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.rep_formula(expand=True):<70} │ ∎'
        return output + f'\n'


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
        self._sequent_comma = None
        self._conjunction = None
        self._disjunction = None
        self._equality = None
        self._inconsistency = None
        self._inequality = None
        self._implication = None
        self._is_a = None
        self._map = None
        self._negation = None
        self._syntactic_entailment = None

    def declare(self, arity: int, symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, formula_rep=None, signal_proposition=None,
            signal_theoretical_morphism=None, implementation=None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """Declare a new relation in this universe-of-discourse.
        """
        return Relation(arity=arity, formula_rep=formula_rep, signal_proposition=signal_proposition,
            signal_theoretical_morphism=signal_theoretical_morphism, implementation=implementation,
            universe_of_discourse=self.u, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle, nameset=nameset, echo=echo)

    @property
    def biconditional(self):
        """The well-known biconditional relation.

        Abridged property: u.r.iif

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._biconditional is None:
            self._biconditional = self.declare(arity=2, formula_rep=Formula.infix,
                signal_proposition=True,
                symbol=SerifItalic(plaintext='<==>', unicode='⟺', latex='\\iff'), auto_index=False,
                dashed_name='biconditional', name='biconditional')
        return self._biconditional

    @property
    def conjunction(self):
        """The well-known conjunction relation.

        Abridged property: u.r.land

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._conjunction is None:
            self._conjunction = self.declare(arity=2, formula_rep=Formula.infix,
                signal_proposition=True,
                symbol=SerifItalic(plaintext='and', unicode='∧', latex='\\land'), auto_index=False,
                name='and', explicit_name='conjunction')
        return self._conjunction

    @property
    def disjunction(self):
        """The well-known disjunction relation.

        Abridged property: u.r.land

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._disjunction is None:
            self._disjunction = self.declare(arity=2, formula_rep=Formula.infix,
                signal_proposition=True, auto_index=False,
                symbol=SerifItalic(unicode='∨', latex='\\lor', plaintext='or'), name='or',
                explicit_name='disjunction')
        return self._disjunction

    @property
    def eq(self):
        """The well-known equality relation.

        Unabridged property: universe_of_discourse.relations.equality

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.equality

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
            self._equality = self.declare(arity=2, formula_rep=Formula.infix,
                signal_proposition=True, symbol='=', auto_index=False, dashed_name='equality')
        return self._equality

    @property
    def inc(self):
        """The well-known (theory-)inconsistent relation.

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
        """The well-known implication relation.

        Abridged property: u.r.implies

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._implication is None:
            self._implication = self.declare(arity=2, formula_rep=Formula.infix,
                signal_proposition=True,
                symbol=SerifItalic(plaintext='==>', unicode='⟹', latex=r'\implies'),
                auto_index=False, name='implication', explicit_name='logical implication')
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
    def inconsistency(self):
        """The well-known (theory-)inconsistent relation.

        Abridged property: u.r.inc

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._inconsistency is None:
            self._inconsistency = self.declare(arity=1, formula_rep=Formula.prefix,
                signal_proposition=True, symbol='Inc', auto_index=False, acronym='inc.',
                name='inconsistent')
        return self._inconsistency

    @property
    def inequality(self):
        """The well-known inequality relation.

        Abridged property: u.r.neq

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._inequality is None:
            self._inequality = self.declare(arity=2, formula_rep=Formula.infix,
                signal_proposition=True,
                symbol=SerifItalic(plaintext='neq', unicode='≠', latex='\\neq'), auto_index=False,
                acronym='neq', name='not equal')
        return self._inequality

    @property
    def is_a(self):
        if self._is_a is None:
            self._is_a = self.declare(arity=2, formula_rep=Formula.infix, signal_proposition=True,
                symbol=SerifItalic(plaintext='is-a', unicode='is-a', latex='is-a'),
                auto_index=False, acronym=None, name='is a')
        return self._is_a

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
    def map(self):
        """The well-known map relation.

        Abridged property: u.r.map

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._map is None:
            self._map = self.declare(arity=1, formula_rep=Formula.prefix, signal_proposition=True,
                symbol=SerifItalic(plaintext='-->', unicode='\u2192', latex='\\rightarrow'),
                auto_index=False, name='map')
        return self._map

    @property
    def negation(self):
        """The well-known negation relation.

        Abridged property: u.r.lnot

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._negation is None:
            self._negation = self.declare(arity=1, formula_rep=Formula.prefix,
                signal_proposition=True,
                symbol=SerifItalic(plaintext='not', unicode='¬', latex='\\neg'), auto_index=False,
                abridged_name='not', name='negation')
        return self._negation

    @property
    def neq(self):
        """The well-known inequality relation.

        Unabridged property: u.r.inequality

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.inequality

    @property
    def proves(self):
        """The well-known syntactic-entailment relation.

        Unabridged property: u.r.syntactic_entailment

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.syntactic_entailment

    @property
    def sequent_comma(self):
        """Initially needed to express the collection of premises in inference-rule formula definitions.

        For the time being it is sufficient to implement it as a binary relation,
        because our initial catalog of inference rules have one or two premises.
        But at a later point, we will need to implement (0-n)-ary relations.
        """
        if self._sequent_comma is None:
            self._sequent_comma = self.declare(arity=2, formula_rep=Formula.infix,
                signal_proposition=True, symbol=SerifItalic(plaintext=',', unicode=',', latex=','),
                auto_index=False, dashed_name='sequent-comma', name='sequent comma',
                explicit_name='sequent calculus comma')
        return self._sequent_comma

    @property
    def syntactic_entailment(self):
        """The well-known syntactic-entailment relation.

        Abridged property: u.r.proves

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._syntactic_entailment is None:
            self._syntactic_entailment = self.declare(arity=2, formula_rep=Formula.infix,
                signal_proposition=True,
                symbol=SerifItalic(plaintext='|-', unicode='⊢', latex='\\vdash'), auto_index=False,
                dashed_name='syntactic-entailment', abridged_name='proves',
                name='syntactic entailment')
        return self._syntactic_entailment


FlexibleFormula = typing.Union[FormulaStatement, Formula, tuple, list]
"""See validate_flexible_statement_formula() for details."""


def verify_formula(u: UniverseOfDiscourse, input_value: FlexibleFormula, arg: (None, str) = None,
        form: (None, FlexibleFormula) = None, mask: (None, frozenset[FreeVariable]) = None,
        raise_exception: bool = True) -> tuple[bool, (None, Formula), (None, str)]:
    """Many punctilious pythonic methods or functions expect some formula as input parameters. This function assures that the input value is a proper formula and that it is consistent with possible contraints imposed on that formula.

    If ⌜input_value⌝ is of type formula, it is already well typed.

    If ⌜argument⌝ is of type statement-variable, retrieve its valid-proposition property.

    If ⌜argument⌝ is of type iterable, such as tuple, e.g.: (implies, q, p), we assume it is a formula in the form (relation, a1, a2, ... an) where ai are arguments.

    Note that this is complementary with the pseudo-infix notation, which uses the __or__ method and | operator to transform: p |r| q to (r, p, q).

    :param t:
    :param input_value:
    :return:
    """
    ok: bool
    formula: (None, Formula) = None
    msg: (None, str) = None
    if isinstance(input_value, Formula):
        # the input is already correctly typed as a Formula.
        formula = input_value
    elif isinstance(input_value, FormulaStatement):
        # the input is typed as a FormulaStatement,
        # we must unpack it to retrieve its internal Formula.
        formula = input_value.valid_proposition
    elif isinstance(input_value, tuple):
        # the input is a tuple,
        # assuming a data structure of the form:
        # (relation, argument_1, argument_2, ..., argument_n)
        # where the relation and/or the arguments may be free-variables.
        formula = u.f(input_value[0], *input_value[1:])
    else:
        # the input argument could not be interpreted as a formula
        value_string: str
        try:
            value_string = str(input_value)
        except:
            value_string = 'string conversion failure'
        ok, msg = verify(raise_exception=raise_exception, assertion=False,
            msg=f'The argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}could not be interpreted as a Formula. Its type was {str(type(input_value))}, and its value was ⌜{value_string}⌝.',
            argument=input_value, u=u)
        if not ok:
            return ok, None, msg

    # Note: it is not necessary to verify that the universe
    # of the formula relation is consistent with the universe of the formula,
    # because this is already verified in the formula constructor.
    # Note: it is not necessary to verify that the universe
    # of the formula parameters are consistent with the universe of the formula,
    # because this is already verified in the formula constructor.
    if form is not None:
        ok, form, msg = verify_formula(u=u, input_value=form,
            raise_exception=True)  # The form itself may be a flexible formula.
        if not ok:
            verify(raise_exception=raise_exception, assertion=False,
                msg=f'The form ⌜{form}⌝ passed to verify the structure of formula ⌜{formula}⌝ is not a proper formula.',
                argument=input_value, u=u, form=form, mask=mask)
        form: Formula
        is_of_form: bool = form.is_masked_formula_similar_to(o2=formula, mask=mask)
        if not is_of_form:
            # a certain form is required for the formula,
            # and the form of the formula does not match that required form.
            free_variables_string: str
            if mask is None:
                free_variables_string = ''
            elif len(mask) == 1:
                free_variables_string = ', where ' + ', '.join(
                    [free_variable.rep(encoding=encodings.plaintext) for free_variable in
                        mask]) + ' is a free-variable'
            else:
                free_variables_string = ', where ' + ', '.join(
                    [free_variable.rep(encoding=encodings.plaintext) for free_variable in
                        mask]) + ' are free-variables'
            ok, msg = verify(raise_exception=raise_exception, assertion=False,
                msg=f'The formula ⌜{formula}⌝ passed as argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}is not of the required form ⌜{form}⌝{free_variables_string}.',
                argument=input_value, u=u, form=form, mask=mask)
            if not ok:
                return ok, None, msg
    return True, formula, None


def verify_formula_statement(t: TheoryElaborationSequence, input_value: FlexibleFormula,
        arg: (None, str) = None, form: (None, FlexibleFormula) = None,
        mask: (None, frozenset[FreeVariable]) = None, raise_exception: bool = True) -> tuple[
    bool, (None, FormulaStatement), (None, str)]:
    """Many punctilious pythonic methods expect some FormulaStatement as input parameters (e.g. the infer_statement() of inference-rules). This is syntactically robust, but it may read theory code less readable. In effect, one must store all formula-statements in variables to reuse them in formula. If the number of formula-statements get large, readability suffers. To provide a friendler interface for humans, we allow passing formula-statements as formula, tuple, and lists and apply the following interpretation rules:

    If ⌜argument⌝ is of type iterable, such as tuple, e.g.: (implies, q, p), we assume it is a formula in the form (relation, a1, a2, ... an) where ai are arguments.

    Note that this is complementary with the pseudo-infix notation, which transforms: p |implies| q into a formula.

    :param t:
    :param arity:
    :param input_value:
    :return:
    """

    formula_ok: bool
    msg: (None, str)
    formula_statement: (None, FormulaStatement) = None
    formula: (None, Formula) = None
    u: UniverseOfDiscourse = t.u

    if isinstance(input_value, FormulaStatement):
        formula_statement = input_value
    else:
        # ⌜argument⌝ is not a statement-formula.
        # But it is expected to be interpretable first as a formula, and then as a formula-statement.
        formula_ok, formula, msg = verify_formula(arg=arg, u=u, input_value=input_value, form=None,
            mask=None, arity=None)
        if not formula_ok:
            return formula_ok, None, msg
        formula: Formula
        # We only received a formula, not a formula-statement.
        # Since we require a formula-statement,
        # we attempt to automatically retrieve the first occurrence
        # of a formula-statement in ⌜t⌝ that is
        # syntactically-equivalent to ⌜argument⌝.
        formula_statement = t.get_first_syntactically_equivalent_statement(formula=input_value)
        formula_ok, msg = verify(input_value is not None,
            f'The formula ⌜{formula}⌝ passed as argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}is not a formula-statement in theory-elaboration-sequence ⌜{t}⌝.',
            formula=formula, t=t)
        if not formula_ok:
            return formula_ok, None, msg

    # At this point we have a properly typed FormulaStatement.
    formula_ok, msg = verify(formula_statement.t is t,
        f'The theory-elaboration-sequence ⌜{formula_statement.t}⌝ of the formula-statement {formula_statement} passed as argument {"" if arg is None else "".join(["⌜", arg, "⌝ "])}is not consistent with the theory-elaboration-sequence ⌜{t}⌝.',
        formula=formula, t=t)
    if not formula_ok:
        return formula_ok, None, msg

    # Validate the form, etc. of the underlying formula.
    formula = input_value.valid_proposition
    formula_ok, formula, msg = verify_formula(u=u, input_value=formula, arg=arg, form=form,
        mask=mask)
    if not formula_ok:
        return formula_ok, None, msg

    return True, formula_statement, msg


class InferenceRuleDeclarationCollection(collections.UserDict):
    """This python class models the collection of :ref:`inference-rules<inference_rule_math_concept>` :ref:`declared<object_declaration_math_concept>` in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>`.

    In complement, it conveniently exposes as python properties a catalog of natively supported :ref:`inference-rules<inference_rule_math_concept>` that are automatically :ref:`declared<object_declaration_math_concept>` in the :ref:`universe-of-discourse<universe_of_discourse_math_concept>` when they are accessed for the first time.
    """

    def __init__(self, u: UniverseOfDiscourse):
        self.u = u
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
        self._definition_interpretation = None
        self._disjunction_elimination = None
        self._disjunction_introduction_1 = None
        self._disjunction_introduction_2 = None
        self._double_negation_elimination = None
        self._double_negation_introduction = None
        self._equality_commutativity = None
        self._equal_terms_substitution = None
        self._inconsistency_introduction_1 = None
        self._inconsistency_introduction_2 = None
        self._inconsistency_introduction_3 = None
        self._modus_ponens = None
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
            self._absorption = AbsorptionDeclaration(universe_of_discourse=self.u)
        return self._absorption

    @property
    def axiom_interpretation(self) -> AxiomInterpretationDeclaration:
        if self._axiom_interpretation is None:
            self._axiom_interpretation = AxiomInterpretationDeclaration(
                universe_of_discourse=self.u)
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
            self._biconditional_elimination_1 = BiconditionalElimination1Declaration(
                universe_of_discourse=self.u)
        return self._biconditional_elimination_1

    @property
    def biconditional_elimination_2(self) -> BiconditionalElimination2Declaration:
        if self._biconditional_elimination_2 is None:
            self._biconditional_elimination_2 = BiconditionalElimination2Declaration(
                universe_of_discourse=self.u)
        return self._biconditional_elimination_2

    @property
    def biconditional_introduction(self) -> BiconditionalIntroductionDeclaration:
        if self._biconditional_introduction is None:
            self._biconditional_introduction = BiconditionalIntroductionDeclaration(
                universe_of_discourse=self.u)
        return self._biconditional_introduction

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
            self._conjunction_elimination_1 = ConjunctionElimination1Declaration(
                universe_of_discourse=self.u)
        return self._conjunction_elimination_1

    @property
    def conjunction_elimination_2(self) -> ConjunctionElimination2Declaration:
        if self._conjunction_elimination_2 is None:
            self._conjunction_elimination_2 = ConjunctionElimination2Declaration(
                universe_of_discourse=self.u)
        return self._conjunction_elimination_2

    @property
    def conjunction_introduction(self) -> ConjunctionIntroductionDeclaration:
        if self._conjunction_introduction is None:
            self._conjunction_introduction = ConjunctionIntroductionDeclaration(
                universe_of_discourse=self.u)
        return self._conjunction_introduction

    @property
    def definition_interpretation(self) -> DefinitionInterpretationDeclaration:
        if self._definition_interpretation is None:
            self._definition_interpretation = DefinitionInterpretationDeclaration(
                universe_of_discourse=self.u)
        return self._definition_interpretation

    @property
    def dil(self) -> DisjunctionIntroduction1Declaration:
        return self.disjunction_introduction_1

    @property
    def dir(self) -> DisjunctionIntroduction2Declaration:
        return self.disjunction_introduction_2

    @property
    def disjunction_introduction_1(self) -> DisjunctionIntroduction1Declaration:
        if self._disjunction_introduction_1 is None:
            self._disjunction_introduction_1 = DisjunctionIntroduction1Declaration(
                universe_of_discourse=self.u)
        return self._disjunction_introduction_1

    @property
    def disjunction_introduction_2(self) -> DisjunctionIntroduction2Declaration:
        if self._disjunction_introduction_2 is None:
            self._disjunction_introduction_2 = DisjunctionIntroduction2Declaration(
                universe_of_discourse=self.u)
        return self._disjunction_introduction_2

    @property
    def dne(self) -> DoubleNegationEliminationDeclaration:
        return self.double_negation_elimination

    @property
    def dni(self) -> DoubleNegationIntroductionDeclaration:
        return self.double_negation_introduction

    @property
    def double_negation_elimination(self) -> DoubleNegationEliminationDeclaration:
        if self._double_negation_elimination is None:
            self._double_negation_elimination = DoubleNegationEliminationDeclaration(
                universe_of_discourse=self.u)
        return self._double_negation_elimination

    @property
    def double_negation_introduction(self) -> DoubleNegationIntroductionDeclaration:
        if self._double_negation_introduction is None:
            self._double_negation_introduction = DoubleNegationIntroductionDeclaration(
                universe_of_discourse=self.u)
        return self._double_negation_introduction

    @property
    def ec(self) -> EqualityCommutativityDeclaration:
        return self.equality_commutativity

    @property
    def equality_commutativity(self) -> EqualityCommutativityDeclaration:
        if self._equality_commutativity is None:
            self._equality_commutativity = EqualityCommutativityDeclaration(
                universe_of_discourse=self.u)
        return self._equality_commutativity

    @property
    def equal_terms_substitution(self) -> EqualTermsSubstitutionDeclaration:
        if self._equal_terms_substitution is None:
            self._equal_terms_substitution = EqualTermsSubstitutionDeclaration(
                universe_of_discourse=self.u)
        return self._equal_terms_substitution

    @property
    def ets(self) -> EqualTermsSubstitutionDeclaration:
        return self.equal_terms_substitution

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
            self._inconsistency_introduction_1 = InconsistencyIntroduction1Declaration(
                universe_of_discourse=self.u)
        return self._inconsistency_introduction_1

    @property
    def inconsistency_introduction_2(self) -> InconsistencyIntroduction2Declaration:
        if self._inconsistency_introduction_2 is None:
            self._inconsistency_introduction_2 = InconsistencyIntroduction2Declaration(
                universe_of_discourse=self.u)
        return self._inconsistency_introduction_2

    @property
    def inconsistency_introduction_3(self) -> InconsistencyIntroduction3Declaration:
        if self._inconsistency_introduction_3 is None:
            self._inconsistency_introduction_3 = InconsistencyIntroduction3Declaration(
                universe_of_discourse=self.u)
        return self._inconsistency_introduction_3

    @property
    def modus_ponens(self) -> ModusPonensDeclaration:
        if self._modus_ponens is None:
            self._modus_ponens = ModusPonensDeclaration(universe_of_discourse=self.u)
        return self._modus_ponens

    @property
    def mp(self) -> InferenceRuleDeclaration:
        return self.modus_ponens

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
            self._proof_by_contradiction_1 = ProofByContradiction1Declaration(
                universe_of_discourse=self.u)
        return self._proof_by_contradiction_1

    @property
    def proof_by_contradiction_2(self) -> ProofByContradiction2Declaration:
        if self._proof_by_contradiction_2 is None:
            self._proof_by_contradiction_2 = ProofByContradiction2Declaration(
                universe_of_discourse=self.u)
        return self._proof_by_contradiction_2

    @property
    def proof_by_refutation_1(self) -> ProofByRefutation1Declaration:
        if self._proof_by_refutation_1 is None:
            self._proof_by_refutation_1 = ProofByRefutation1Declaration(
                universe_of_discourse=self.u)
        return self._proof_by_refutation_1

    @property
    def proof_by_refutation_2(self) -> ProofByRefutation2Declaration:
        if self._proof_by_refutation_2 is None:
            self._proof_by_refutation_2 = ProofByRefutation2Declaration(
                universe_of_discourse=self.u)
        return self._proof_by_refutation_2

    @property
    def variable_substitution(self) -> VariableSubstitutionDeclaration:
        if self._variable_substitution is None:
            self._variable_substitution = VariableSubstitutionDeclaration(
                universe_of_discourse=self.u)
        return self._variable_substitution

    @property
    def vs(self) -> VariableSubstitutionDeclaration:
        return self.variable_substitution


class AbsorptionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`absorption<absorption_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.absorption
        dashed_name = 'absorption'
        abridged_name = 'absorp.'
        name = 'absorption'
        explicit_name = 'absorption inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, echo=echo, proof=proof)

    def check_premises_validity(self, p_implies_q: FlexibleFormula,
            raise_exception: bool = True) -> bool:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        # Validate that expected formula-statements are formula-statements.
        formula_ok, _, _ = verify_formula_statement(t=self.t, input_value=p_implies_q,
            form=self.i.parameter_p_implies_q, mask=self.i.parameter_p_implies_q_mask,
            raise_exception=raise_exception)
        # The method either raises an exception during validation, or return True.
        return formula_ok

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_absorption_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> AbsorptionDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: AbsorptionDeclaration = super().i
        return i

    def construct_formula(self, p_implies_q: FlexibleFormula) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(p_implies_q=p_implies_q)

    def infer_formula_statement(self, p_implies_q: FlexibleFormula = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_implies_q=p_implies_q)
        return InferredStatement(i=self, premises=premises, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class AxiomInterpretationInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`axiom-interpretation<axiom_interpretation_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .

    Inherits from :ref:`InferenceRuleInclusion<inference_rule_inclusion_python_class>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.axiom_interpretation
        dashed_name = 'axiom-interpretation'
        acronym = 'ai'
        abridged_name = None
        name = 'axiom interpretation'
        explicit_name = 'axiom interpretation inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def check_premises_validity(self, a: AxiomInclusion, p: FlexibleFormula,
            raise_exception: bool = True) -> tuple[bool, (None, str)]:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        ok: bool
        msg: (None, str)
        # Validate that expected formula-statements are formula-statements.
        # TODO: NICETOHAVE: AxiomInterpretationInclusion: replace these verify statements with a generic validate_axiom_inclusion function.
        ok, msg = verify(raise_exception=raise_exception, assertion=isinstance(a, AxiomInclusion),
            msg=f'⌜{a}⌝ passed as argument ⌜a⌝ is not an axiom-inclusion.', a=a)
        if not ok:
            return ok, msg
        ok, msg = verify(raise_exception=raise_exception,
            assertion=self.t.contains_theoretical_objct(a),
            msg=f'⌜{a}⌝ passed as argument ⌜a⌝ is not contained in theory-elaboration-sequence ⌜{self.t}⌝.',
            a=a)
        if not ok:
            return ok, msg
        ok, formula, msg = verify_formula(raise_exception=raise_exception, u=self.u, input_value=p)
        if not ok:
            return ok, msg
        # TODO: BUG: validate_formula does not support basic masks like: ⌜P⌝ where P is a free-variable.
        # validate_formula(u=self.u, input_value=p, form=self.i.parameter_p,
        #    mask=self.i.parameter_p_mask)
        return True, None

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Overrides the generic paragraph proof method."""
        output = yield from configuration.locale.compose_axiom_interpretation_paragraph_proof(o=o)
        return output

    @property
    def i(self) -> AxiomInterpretationDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: AxiomInterpretationDeclaration = super().i
        return i

    def construct_formula(self, a: (None, AxiomInclusion) = None, p: (None, FlexibleFormula) = None,
            echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(a=a, p=p)

    def infer_formula_statement(self, a: (None, AxiomInclusion) = None,
            p: (None, FlexibleFormula) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(a=a, p=p)
        return InferredStatement(i=self, premises=premises, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class BiconditionalElimination1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`biconditional-elimination-1<biconditional_elimination_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.biconditional_elimination_1
        dashed_name = 'biconditional-elimination-1'
        acronym = 'be1'
        abridged_name = None
        name = 'biconditional elimination #1'
        explicit_name = 'biconditional elimination #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def check_premises_validity(self, p_iff_q: FlexibleFormula,
            raise_exception: bool = True) -> bool:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        # Validate that expected formula-statements are formula-statements.
        formula_ok, _, _ = verify_formula_statement(t=self.t, input_value=p_iff_q,
            form=self.i.parameter_p_iff_q, mask=self.i.parameter_p_iff_q_mask,
            raise_exception=raise_exception)
        # The method either raises an exception during validation, or return True.
        return formula_ok

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_biconditional_elimination_1_paragraph_proof(
            o=o)
        return output

    @property
    def i(self) -> BiconditionalElimination1Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: BiconditionalElimination1Declaration = super().i
        return i

    def construct_formula(self, p_iff_q: FlexibleFormula) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(p_iff_q=p_iff_q)

    def infer_formula_statement(self, p_iff_q: FlexibleFormula = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_iff_q=p_iff_q)
        return InferredStatement(i=self, premises=premises, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class BiconditionalElimination2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`biconditional-elimination-2<biconditional_elimination_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.biconditional_elimination_2
        dashed_name = 'biconditional-elimination-2'
        acronym = 'be2'
        abridged_name = None
        name = 'biconditional elimination #2'
        explicit_name = 'biconditional elimination #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def check_premises_validity(self, p_iff_q: FlexibleFormula,
            raise_exception: bool = True) -> bool:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        # Validate that expected formula-statements are formula-statements.
        formula_ok, _, _ = verify_formula_statement(t=self.t, input_value=p_iff_q,
            form=self.i.parameter_p_iff_q, mask=self.i.parameter_p_iff_q_mask,
            raise_exception=raise_exception)
        # The method either raises an exception during validation, or return True.
        return formula_ok

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_biconditional_elimination_2_paragraph_proof(
            o=o)
        return output

    @property
    def i(self) -> BiconditionalElimination1Declaration:
        """Override the base class i property with a specialized inherited class type."""
        i: BiconditionalElimination1Declaration = super().i
        return i

    def construct_formula(self, p_iff_q: FlexibleFormula) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(p_iff_q=p_iff_q)

    def infer_formula_statement(self, p_iff_q: FlexibleFormula = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(p_iff_q=p_iff_q)
        return InferredStatement(i=self, premises=premises, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class BiconditionalIntroductionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`biconditional-introduction<biconditional_introduction_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.biconditional_introduction
        dashed_name = 'biconditional-introduction'
        acronym = 'bi'
        abridged_name = None
        name = 'biconditional introduction'
        explicit_name = 'biconditional introduction inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_biconditional_introduction_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p_implies_q: FormulaStatement = None,
            q_implies_p: FormulaStatement = None, t: TheoryElaborationSequence = None) -> bool:
        p_implies_q = verify_formula_statement(t=t, arity=2, input_value=p_implies_q)
        verify(t.contains_theoretical_objct(p_implies_q),
            'Statement ⌜p_implies_q⌝ must be contained in theory ⌜t⌝.', p_implies_q=p_implies_q,
            t=t, slf=self)
        q_implies_p = verify_formula_statement(t=t, arity=2, input_value=q_implies_p)
        verify(t.contains_theoretical_objct(q_implies_p),
            'Statement ⌜q_implies_p⌝ must be contained in theory ⌜t⌝.', q_implies_p=q_implies_p,
            t=t, slf=self)
        p_implies_q: Formula = verify_formula(u=t.u, arity=2, input_value=p_implies_q)
        q_implies_p: Formula = verify_formula(u=t.u, arity=2, input_value=q_implies_p)
        verify(p_implies_q.relation is t.u.r.implication,
            'The relation of formula ⌜p_implies_q⌝ must be an implication.',
            p_implies_q_relation=p_implies_q.relation, p_implies_q=p_implies_q, t=t, slf=self)
        verify(q_implies_p.relation is t.u.r.implication,
            'The relation of formula ⌜q_implies_p⌝ must be an implication.',
            q_implies_p_relation=p_implies_q.relation, q_implies_p=q_implies_p, t=t, slf=self)

        verify(p_implies_q.parameters[0].is_formula_syntactically_equivalent_to(
            q_implies_p.parameters[1]),
            'The p of the ⌜p_implies_q⌝ formula must be formula-syntactically-equivalent to the p of '
            '⌜q_implies_p⌝ formula.', p_implies_q=p_implies_q, q_implies_p=q_implies_p, t=t,
            slf=self)
        verify(p_implies_q.parameters[1].is_formula_syntactically_equivalent_to(
            q_implies_p.parameters[0]),
            'The q of the ⌜p_implies_q⌝ formula must be formula-syntactically-equivalent to the q of '
            '⌜q_implies_p⌝ formula.', p_implies_q=p_implies_q, q_implies_p=q_implies_p, t=t,
            slf=self)
        return True

    def infer_formula(self, p_implies_q: (tuple, Formula, FormulaStatement) = None,
            q_implies_p: (tuple, Formula, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p_iff_q, echo=echo)

    def infer_formula_statement(self, p_implies_q: (tuple, Formula, FormulaStatement) = None,
            q_implies_p: (tuple, Formula, FormulaStatement) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        return super().infer_formula_statement(p_implies_q, q_implies_p, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class ConjunctionElimination1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`conjunction-elimination-1<conjunction_elimination_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_elimination_1
        dashed_name = 'conjunction-elimination-1'
        acronym = 'ce1'
        abridged_name = None
        name = 'conjunction elimination #1'
        explicit_name = 'conjunction elimination #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_conjunction_elimination_1_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p_land_q: FormulaStatement = None,
            t: TheoryElaborationSequence = None) -> bool:
        verify(t.contains_theoretical_objct(p_land_q),
            'Statement ⌜p_land_q⌝ must be contained in theory ⌜t⌝''s hierarchy.', p_land_q=p_land_q,
            t=t, slf=self)
        verify(p_land_q.relation is t.u.r.conjunction,
            'The relation of formula ⌜p_land_q⌝ must be a conjunction.',
            p_land_q_relation=p_land_q.relation, p_land_q=p_land_q, t=t, slf=self)
        return True

    def infer_formula(self, p_and_q: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p_and_q, echo=echo)

    def infer_formula_statement(self, p_and_q: (None, FormulaStatement) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        return super().infer_formula_statement(p_and_q, ref=ref, paragraph_header=paragraph_header,
            subtitle=subtitle, echo=echo)


class ConjunctionElimination2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`conjunction-elimination-2<conjunction_elimination_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_elimination_2
        dashed_name = 'conjunction-elimination-2'
        acronym = 'bel'
        abridged_name = 'conj. elim. right'
        name = 'conjunction elimination #2'
        explicit_name = 'conjunction elimination #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_conjunction_elimination_2_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p_land_q: FormulaStatement = None,
            t: TheoryElaborationSequence = None) -> bool:
        verify(t.contains_theoretical_objct(p_land_q),
            'Statement ⌜p_land_q⌝ must be contained in theory ⌜t⌝''s hierarchy.', p_land_q=p_land_q,
            t=t, slf=self)
        verify(p_land_q.relation is t.u.r.conjunction,
            'The relation of formula ⌜p_land_q⌝ must be a conjunction.',
            p_land_q_relation=p_land_q.relation, p_land_q=p_land_q, t=t, slf=self)
        return True

    def infer_formula(self, p_and_q: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p_and_q, echo=echo)

    def infer_formula_statement(self, p_and_q: (None, FormulaStatement) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        return super().infer_formula_statement(p_and_q, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class ConjunctionIntroductionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`conjunction-introduction<conjunction_introduction_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_introduction
        dashed_name = 'conjunction-introduction'
        acronym = 'ci'
        abridged_name = 'conj.-intro.'
        name = 'conjunction introduction'
        explicit_name = 'conjunction introduction inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Composes the paragraph-proof of inferred-statements based on the :ref:`conjunction-introduction<conjunction_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` ."""
        output = yield from configuration.locale.compose_conjunction_introduction_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement, q: FormulaStatement,
            t: TheoryElaborationSequence) -> bool:
        """Verify the correctness of the parameters provided to the :ref:`double-negation-introduction<double_negation_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` .

        :param p: (mandatory) A formula-statement of the form :math:`P` .
        :param q: (mandatory) A formula-statement of the form :math:`Q` .
        :param t: (mandatory) The target theory-elaboration-sequence that must contain :math:`P` .

        :return: True (bool) if the parameters are correct.
        """
        p = verify_formula_statement(t=t, arity=None, input_value=p)
        q = verify_formula_statement(t=t, arity=None, input_value=q)
        verify(t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.', p=p, t=t, slf=self)
        verify(t.contains_theoretical_objct(q),
            'Statement ⌜q⌝ must be contained in theory ⌜t⌝''s hierarchy.', q=q, t=t, slf=self)
        return True

    def infer_formula(self, p: (None, Formula, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        ok: bool
        msg: (None, str)
        ok, p, msg = verify_formula(u=self.t.u, arity=None, input_value=p)
        ok, q, msg = verify_formula(u=self.t.u, arity=None, input_value=q)
        return super().infer_formula(p, q, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        q = verify_formula_statement(t=self.t, arity=None, input_value=q)
        return super().infer_formula_statement(p, q, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class ConstructiveDilemmaInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`constructive-dilemma<constructive_dilemma_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_introduction
        dashed_name = 'constructive-dilemma'
        acronym = 'cd'
        abridged_name = None
        name = 'constructive dilemma'
        explicit_name = 'constructive dilemma inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def infer_formula(self, p: (None, Formula, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=self.t.u, arity=None, input_value=p)
        q = verify_formula(u=self.t.u, arity=None, input_value=q)
        return super().infer_formula(p, q, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        q = verify_formula_statement(t=self.t, arity=None, input_value=q)
        return super().infer_formula_statement(p, q, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class DefinitionInterpretationInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`definition-interpretation<definition_interpretation_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .

    Inherits from :ref:`InferenceRuleInclusion<inference_rule_inclusion_python_class>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.definition_interpretation
        dashed_name = 'definition-interpretation'
        acronym = 'di'
        abridged_name = None
        name = 'definition interpretation'
        explicit_name = 'definition interpretation inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def check_premises_validity(self, d: DefinitionInclusion, x: FlexibleFormula,
            y: FlexibleFormula, raise_exception: bool = True) -> tuple[bool, (None, str)]:
        """
        .. include:: ../../include/check_premises_validity_python_method.rstinc

        """
        ok: bool
        msg: (None, str)
        # Validate that expected formula-statements are formula-statements.
        # TODO: NICETOHAVE: DefinitionInterpretationInclusion: replace these verify statements with a generic validate_definition_inclusion function.
        ok, msg = verify(raise_exception=raise_exception,
            assertion=isinstance(d, DefinitionInclusion),
            msg=f'⌜{d}⌝ passed as argument ⌜d⌝ is not a definition-inclusion.', d=d)
        if not ok:
            return ok, msg
        ok, msg = verify(raise_exception=raise_exception,
            assertion=self.t.contains_theoretical_objct(d),
            msg=f'⌜{d}⌝ passed as argument ⌜d⌝ is not contained in theory-elaboration-sequence ⌜{self.t}⌝.',
            d=d)
        if not ok:
            return ok, msg
        ok, x, msg = verify_formula(arg='x', input_value=x, u=self.u, raise_exception=True)
        if not ok:
            return ok, msg
        ok, y, msg = verify_formula(arg='y', input_value=y, u=self.u, raise_exception=True)
        if not ok:
            return ok, msg
        return True, None

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Overrides the generic paragraph proof method."""
        output = yield from configuration.locale.compose_definition_interpretation_paragraph_proof(
            o=o)
        return output

    @property
    def i(self) -> DefinitionInterpretationDeclaration:
        """Override the base class i property with a specialized inherited class type."""
        i: DefinitionInterpretationDeclaration = super().i
        return i

    def construct_formula(self, d: (None, DefinitionInclusion) = None,
            x_equal_y: (None, FlexibleFormula) = None, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        # Call back the infer_formula method on the inference-rule declaration class.
        return self.i.construct_formula(d=d, x_equal_y=x_equal_y)

    def infer_formula_statement(self, d: (None, DefinitionInclusion) = None,
            x_equal_y: (None, FlexibleFormula) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        premises = self.i.Premises(d=d, x_equal_y=x_equal_y)
        return InferredStatement(i=self, premises=premises, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class DestructiveDilemmaInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`destructive-dilemma<destructive_dilemma_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_introduction
        dashed_name = 'destructive-dilemma'
        acronym = 'dd'
        abridged_name = None
        name = 'destructive dilemma'
        explicit_name = 'destructive dilemma inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.destructive_dilemma_introduction_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement, q: FormulaStatement,
            t: TheoryElaborationSequence) -> bool:
        """ """
        p = verify_formula_statement(t=t, arity=None, input_value=p)
        q = verify_formula_statement(t=t, arity=None, input_value=q)
        verify(t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.', p=p, t=t, slf=self)
        verify(t.contains_theoretical_objct(q),
            'Statement ⌜q⌝ must be contained in theory ⌜t⌝''s hierarchy.', q=q, t=t, slf=self)
        return True

    def infer_formula(self, p: (None, Formula, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=self.t.u, arity=None, input_value=p)
        q = verify_formula(u=self.t.u, arity=None, input_value=q)
        return super().infer_formula(p, q, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        q = verify_formula_statement(t=self.t, arity=None, input_value=q)
        return super().infer_formula_statement(p, q, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class DisjunctionIntroduction1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`disjunction-introduction-1<disjunction_introduction_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.disjunction_introduction_1
        dashed_name = 'disjunction-introduction-1'
        acronym = 'di1'
        abridged_name = None
        name = 'disjunction introduction #1'
        explicit_name = 'disjunction introduction #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Composes the paragraph-proof of inferred-statements based on the :ref:`disjunction-introduction-1<disjunction_introduction_1_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` ."""
        output = yield from configuration.locale.compose_disjunction_introduction_1_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement, q: (Formula, FormulaStatement),
            t: TheoryElaborationSequence) -> bool:
        """Verify the correctness of the parameters provided to the :ref:`double-negation-introduction<double_negation_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` .

        :param p: (mandatory) A formula-statement of the form :math:`P` .
        :param q: (mandatory) A formula of the form :math:`Q` .
        :param t: (mandatory) The target theory-elaboration-sequence that must contain :math:`P` .

        :return: True (bool) if the parameters are correct.
        """
        p = verify_formula_statement(t=t, arity=None, input_value=p)
        q = verify_formula(u=t.u, arity=None, input_value=q)
        verify(t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.', p=p, t=t, slf=self)
        return True

    def infer_formula(self, p: (None, Formula, FormulaStatement) = None,
            q: (None, Formula, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=self.t.u, arity=None, input_value=p)
        q = verify_formula(u=self.t.u, arity=None, input_value=q)
        return super().infer_formula(p, q, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            q: (None, Formula, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        q = verify_formula(u=self.u, arity=None, input_value=q)
        return super().infer_formula_statement(p, q, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class DisjunctionIntroduction2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`disjunction-introduction-2<disjunction_introduction_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.disjunction_introduction_2
        dashed_name = 'disjunction-introduction-2'
        acronym = 'di2'
        abridged_name = None
        name = 'disjunction introduction #2'
        explicit_name = 'disjunction introduction #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Composes the paragraph-proof of inferred-statements based on the :ref:`disjunction-introduction-2<disjunction_introduction_2_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` ."""
        output = yield from configuration.locale.compose_disjunction_introduction_2_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement, q: (Formula, FormulaStatement),
            t: TheoryElaborationSequence) -> bool:
        """Verify the correctness of the parameters provided to the :ref:`double-negation-introduction<double_negation_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` .

        :param p: (mandatory) A formula-statement of the form :math:`P` .
        :param q: (mandatory) A formula of the form :math:`Q` .
        :param t: (mandatory) The target theory-elaboration-sequence that must contain :math:`P` .

        :return: True (bool) if the parameters are correct.
        """
        p = verify_formula_statement(t=t, arity=None, input_value=p)
        q = verify_formula(u=t.u, arity=None, input_value=q)
        verify(t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.', p=p, t=t, slf=self)
        return True

    def infer_formula(self, p: (None, Formula, FormulaStatement) = None,
            q: (None, Formula, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=self.t.u, arity=None, input_value=p)
        q = verify_formula(u=self.t.u, arity=None, input_value=q)
        return super().infer_formula(p, q, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            q: (None, Formula, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        q = verify_formula(u=self.u, arity=None, input_value=q)
        return super().infer_formula_statement(p, q, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class DisjunctiveResolutionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`disjunctive-resolution<disjunctive_resolution_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_introduction
        dashed_name = 'disjunctive-resolution'
        acronym = 'dr'
        abridged_name = None
        name = 'disjunctive resolution'
        explicit_name = 'disjunctive resolution inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_disjunctive_resolution_paragraph_proof(o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement, q: FormulaStatement,
            t: TheoryElaborationSequence) -> bool:
        """ """
        p = verify_formula_statement(t=t, arity=None, input_value=p)
        q = verify_formula_statement(t=t, arity=None, input_value=q)
        verify(t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.', p=p, t=t, slf=self)
        verify(t.contains_theoretical_objct(q),
            'Statement ⌜q⌝ must be contained in theory ⌜t⌝''s hierarchy.', q=q, t=t, slf=self)
        return True

    def infer_formula(self, p: (None, Formula, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=self.t.u, arity=None, input_value=p)
        q = verify_formula(u=self.t.u, arity=None, input_value=q)
        return super().infer_formula(p, q, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        q = verify_formula_statement(t=self.t, arity=None, input_value=q)
        return super().infer_formula_statement(p, q, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class DisjunctiveSyllogismInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`disjunctive-syllogism<disjunctive_syllogism_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_introduction
        dashed_name = 'disjunctive-syllogism'
        acronym = 'ds'
        abridged_name = None
        name = 'disjunctive syllogism'
        explicit_name = 'disjunctive syllogism inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_disjunctive_syllogism_paragraph_proof(o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement, q: FormulaStatement,
            t: TheoryElaborationSequence) -> bool:
        """ """
        p = verify_formula_statement(t=t, arity=None, input_value=p)
        q = verify_formula_statement(t=t, arity=None, input_value=q)
        verify(t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.', p=p, t=t, slf=self)
        verify(t.contains_theoretical_objct(q),
            'Statement ⌜q⌝ must be contained in theory ⌜t⌝''s hierarchy.', q=q, t=t, slf=self)
        return True

    def infer_formula(self, p: (None, Formula, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=self.t.u, arity=None, input_value=p)
        q = verify_formula(u=self.t.u, arity=None, input_value=q)
        return super().infer_formula(p, q, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        q = verify_formula_statement(t=self.t, arity=None, input_value=q)
        return super().infer_formula_statement(p, q, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class DoubleNegationEliminationInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`double-negation-elimination<double_negation_elimination_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.double_negation_elimination
        dashed_name = 'double-negation-elimination'
        acronym = 'dne'
        abridged_name = 'double neg. elim.'
        name = 'double negation elimination'
        explicit_name = 'double negation elimination inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_double_negation_elimination_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, not_not_p: FormulaStatement = None,
            t: TheoryElaborationSequence = None) -> bool:
        not_not_p: FormulaStatement = verify_formula_statement(t=t, arity=1, input_value=not_not_p)
        verify(assertion=t.contains_theoretical_objct(not_not_p),
            msg='Statement ⌜not_not_p⌝ must be contained in ⌜t⌝.', not_not_p=not_not_p, t=t,
            slf=self)
        verify(assertion=not_not_p.valid_proposition.relation is t.u.r.negation,
            msg='The parent formula in ⌜not_not_p⌝ must have ⌜negation⌝ relation.',
            not_not_p=not_not_p, t=t, slf=self)
        not_p: Formula = not_not_p.valid_proposition.parameters[0]
        not_p: Formula = verify_formula(u=t.u, arity=1, input_value=not_p)
        verify(assertion=not_p.relation is t.u.r.negation,
            msg='The child formula in ⌜not_not_p⌝ must have ⌜negation⌝ relation.', not_not_p=not_p,
            t=t, slf=self)
        return True

    def infer_formula(self, not_not_p: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(not_not_p, echo=echo)

    def infer_formula_statement(self, not_not_p: (None, FormulaStatement) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        not_not_p = verify_formula_statement(t=self.t, arity=1, input_value=not_not_p)
        return super().infer_formula_statement(not_not_p, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class DoubleNegationIntroductionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`double-negation-introduction<double_negation_introduction_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.double_negation_introduction
        dashed_name = 'double-negation-introduction'
        acronym = 'dni'
        abridged_name = 'double neg. intro.'
        name = 'double negation introduction'
        explicit_name = 'double negation introduction inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Composes the paragraph-proof of inferred-statements based on the :ref:`double-negation-introduction<double_negation_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` ."""
        output = yield from configuration.locale.compose_double_negation_introduction_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement = None,
            t: TheoryElaborationSequence = None) -> bool:
        p: FormulaStatement = verify_formula_statement(t=t, arity=1, input_value=p)
        """Verify the correctness of the parameters provided to the :ref:`double-negation-introduction<double_negation_introduction_math_inference_rule>` :ref:`inference-rule<inference_rule_math_concept>` .

        :param p: (mandatory) A formula-statement of the form: :math:`P` .

        :return: True (bool) if the parameters are correct.
        """
        verify(assertion=t.contains_theoretical_objct(p),
            msg='Statement ⌜p⌝ must be contained in ⌜t⌝.', p=p, t=t, slf=self)
        return True

    def infer_formula(self, p: (None, Formula, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p = verify_formula_statement(arg='p', t=self.t, arity=1, input_value=p)
        return super().infer_formula_statement(p, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class EqualityCommutativityInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`equality-commutativity<equality_commutativity_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.equality_commutativity
        dashed_name = 'equality-commutativity'
        acronym = 'ec'
        abridged_name = None
        name = 'equality commutativity'
        explicit_name = 'equality commutativity inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_equality_commutativity_paragraph_proof(o=o)
        return output

    def check_inference_validity(self, x_equal_y: (None, FormulaStatement) = None,
            t: TheoryElaborationSequence = None) -> bool:
        verify(is_in_class(x_equal_y, classes.formula_statement),
            '⌜x_equal_y⌝ is not of the declarative-class formula-statement.', p_eq_q=x_equal_y, t=t,
            slf=self)
        verify(t.contains_theoretical_objct(x_equal_y),
            'Statement ⌜x_equal_y⌝ is not contained in ⌜t⌝''s hierarchy.', p_eq_q=x_equal_y, t=t,
            slf=self)
        x_equal_y = unpack_formula(x_equal_y)
        verify(x_equal_y.relation is self.u.r.equality,
            'The root relation of formula ⌜x_equal_y⌝ is not the equality relation.',
            p_eq_q_relation=x_equal_y.relation, p_eq_q=x_equal_y, t=t, slf=self)
        return True

    def infer_formula(self, x_equal_y: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(x_equal_y, echo=echo)

    def infer_formula_statement(self, x_equal_y: (None, FormulaStatement) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        return super().infer_formula_statement(x_equal_y, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class EqualTermsSubstitutionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`equal-terms-substitution<equal_terms_substitution_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.equal_terms_substitution
        dashed_name = 'equal-terms-substitution'
        acronym = 'ets'
        abridged_name = None
        name = 'equal terms substitution'
        explicit_name = 'equal terms substitution inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_equal_terms_substitution_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement = None,
            x_equal_y: FormulaStatement = None, t: TheoryElaborationSequence = None) -> bool:
        verify(is_in_class(p, classes.formula_statement), '⌜p⌝ must be a formula-statement.', p=p,
            slf=self, t=t)
        verify(t.contains_theoretical_objct(p), '⌜p⌝ must be in theory-elaboration-sequence ⌜t⌝.',
            p=p, slf=self, t=t)
        verify(is_in_class(x_equal_y, classes.formula_statement),
            '⌜x_equal_y⌝ is not of the formula-statement declarative-class.', q_equal_r=x_equal_y,
            slf=self, t=t)
        verify(t.contains_theoretical_objct(x_equal_y),
            '⌜x_equal_y⌝ is not contained in theoretical-elaboration-sequence ⌜t⌝.',
            q_equal_r=x_equal_y, slf=self, t=t)
        x_equal_y = unpack_formula(x_equal_y)
        verify(x_equal_y.relation is self.u.r.equality,
            'The root relation of ⌜x_equal_y⌝ is not the equality relation.', q_equal_r=x_equal_y,
            slf=self, t=t)
        return True

    def infer_formula(self, p: (None, FormulaStatement) = None,
            q_equal_r: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p, q_equal_r, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            x_equal_y: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        return super().infer_formula_statement(p, x_equal_y, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class HypotheticalSyllogismInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`hypothetical-syllogism<hypothetical_syllogism_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_introduction
        dashed_name = 'hypothetical-syllogism'
        acronym = 'hs'
        abridged_name = None
        name = 'hypothetical syllogism'
        explicit_name = 'hypothetical syllogism inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """ """
        output = yield from configuration.locale.compose_hypothetical_syllogism_paragraph_proof(o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement, q: FormulaStatement,
            t: TheoryElaborationSequence) -> bool:
        """ """
        p = verify_formula_statement(t=t, arity=None, input_value=p)
        q = verify_formula_statement(t=t, arity=None, input_value=q)
        verify(t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.', p=p, t=t, slf=self)
        verify(t.contains_theoretical_objct(q),
            'Statement ⌜q⌝ must be contained in theory ⌜t⌝''s hierarchy.', q=q, t=t, slf=self)
        return True

    def infer_formula(self, p: (None, Formula, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        p = verify_formula(u=self.t.u, arity=None, input_value=p)
        q = verify_formula(u=self.t.u, arity=None, input_value=q)
        return super().infer_formula(p, q, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            q: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        q = verify_formula_statement(t=self.t, arity=None, input_value=q)
        return super().infer_formula_statement(p, q, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class InconsistencyIntroduction1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`inconsistency-introduction-1<inconsistency_introduction_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.inconsistency_introduction_1
        dashed_name = 'inconsistency-introduction-1'
        acronym = 'ii1'
        abridged_name = None
        name = 'inconsistency introduction #1'
        explicit_name = 'inconsistency introduction #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_inconsistency_introduction_1_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p: FormulaStatement = None, not_p: FormulaStatement = None,
            inconsistent_theory: TheoryElaborationSequence = None,
            t: TheoryElaborationSequence = None) -> bool:
        verify(inconsistent_theory.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜inconsistent_theory⌝''s hierarchy.', p=p,
            inconsistent_theory=inconsistent_theory, slf=self)
        verify(inconsistent_theory.contains_theoretical_objct(not_p),
            'Statement ⌜not_p⌝ must be contained in theory ⌜inconsistent_theory⌝''s hierarchy.',
            not_p=not_p, inconsistent_theory=inconsistent_theory, slf=self)
        verify(not_p.relation is not_p.theory.universe_of_discourse.relations.negation,
            'The relation of statement ⌜not_p⌝ must be ⌜negation⌝.', not_p=not_p,
            inconsistent_theory=inconsistent_theory, slf=self)
        not_p_formula = not_p.valid_proposition
        p_in_not_p = not_p_formula.parameters[0]
        verify(p_in_not_p.is_formula_syntactically_equivalent_to(p),
            'The sub-formula (parameter) ⌜p⌝ in ⌜not_p⌝ must be formula-syntactically-equivalent to ⌜p⌝.',
            not_p=not_p, p_in_not_p=p_in_not_p, p=p, slf=self)
        return True

    def infer_formula(self, p: (None, FormulaStatement) = None,
            not_p: (None, FormulaStatement) = None,
            inconsistent_theory: (None, TheoryElaborationSequence) = None,
            t: (None, TheoryElaborationSequence) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p, not_p, inconsistent_theory, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            not_p: (None, FormulaStatement) = None,
            inconsistent_theory: (None, TheoryElaborationSequence) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        if inconsistent_theory is None and p.t is not_p.t:
            # The inconsistent_theory can be unambiguously defaulted
            # when both p and not_p are contained in the same theory.
            inconsistent_theory = p.t
        return super().infer_formula_statement(p, not_p, inconsistent_theory, nameset=nameset,
            ref=ref, paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class InconsistencyIntroduction2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`inconsistency-introduction-2<inconsistency_introduction_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.inconsistency_introduction_2
        dashed_name = 'inconsistency-introduction-2'
        acronym = 'ii2'
        abridged_name = None
        name = 'inconsistency introduction #2'
        explicit_name = 'inconsistency introduction #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_inconsistency_introduction_2_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, x_eq_y: FormulaStatement = None,
            x_neq_y: FormulaStatement = None, inconsistent_theory: TheoryElaborationSequence = None,
            t: TheoryElaborationSequence = None) -> bool:
        verify(inconsistent_theory.contains_theoretical_objct(x_eq_y),
            'Statement ⌜x_eq_y⌝ must be contained in ⌜inconsistent_theory⌝.', p_eq_q=x_eq_y,
            inconsistent_theory=inconsistent_theory, slf=self)
        verify(inconsistent_theory.contains_theoretical_objct(x_neq_y),
            'Statement ⌜x_neq_y⌝ must be contained in ⌜inconsistent_theory⌝.', p_neq_q=x_neq_y,
            inconsistent_theory=inconsistent_theory, slf=self)
        verify(x_eq_y.relation is x_eq_y.theory.universe_of_discourse.relations.equality,
            'The relation of statement ⌜x_eq_y⌝ must be ⌜equality⌝.', p_neq_q=x_neq_y,
            inconsistent_theory=inconsistent_theory, slf=self)
        verify(x_neq_y.relation is x_neq_y.theory.universe_of_discourse.relations.inequality,
            'The relation of statement ⌜x_neq_y⌝ must be ⌜inequality⌝.', p_neq_q=x_neq_y,
            inconsistent_theory=inconsistent_theory, slf=self)
        verify(x_eq_y.valid_proposition.parameters[0].is_formula_syntactically_equivalent_to(
            x_neq_y.valid_proposition.parameters[0]),
            'The ⌜x⌝ in ⌜x_eq_y⌝ must be formula-syntactically-equivalent to the ⌜x⌝ in ⌜x_neq_y⌝.',
            p_eq_q=x_eq_y, p_neq_q=x_neq_y, inconsistent_theory=inconsistent_theory, slf=self)
        verify(x_eq_y.valid_proposition.parameters[1].is_formula_syntactically_equivalent_to(
            x_neq_y.valid_proposition.parameters[1]),
            'The ⌜y⌝ in ⌜x_eq_y⌝ must be formula-syntactically-equivalent to the ⌜y⌝ in ⌜x_neq_y⌝.',
            p_eq_q=x_eq_y, p_neq_q=x_neq_y, inconsistent_theory=inconsistent_theory, slf=self)
        return True

    def infer_formula(self, x_eq_y: (None, FormulaStatement) = None,
            x_neq_y: (None, FormulaStatement) = None,
            inconsistent_theory: (None, TheoryElaborationSequence) = None,
            t: (None, TheoryElaborationSequence) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(x_eq_y, x_neq_y, inconsistent_theory, echo=echo)

    def infer_formula_statement(self, x_eq_y: (None, FormulaStatement) = None,
            x_neq_y: (None, FormulaStatement) = None,
            inconsistent_theory: (None, TheoryElaborationSequence) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        if inconsistent_theory is None and x_eq_y.t is x_neq_y.t:
            # The inconsistent_theory can be unambiguously defaulted
            # when both p and not_p are contained in the same theory.
            inconsistent_theory = x_eq_y.t
        x_eq_y = verify_formula_statement(t=inconsistent_theory, arity=2, input_value=x_eq_y)
        x_neq_y = verify_formula_statement(t=inconsistent_theory, arity=2, input_value=x_neq_y)
        return super().infer_formula_statement(x_eq_y, x_neq_y, inconsistent_theory,
            nameset=nameset, ref=ref, paragraph_header=paragraph_header, subtitle=subtitle,
            echo=echo)


class InconsistencyIntroduction3Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`inconsistency-introduction-3<inconsistency_introduction_3_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.inconsistency_introduction_3
        dashed_name = 'inconsistency-introduction-3'
        acronym = 'ii3'
        abridged_name = None
        name = 'inconsistency introduction #3'
        explicit_name = 'inconsistency introduction #3 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_inconsistency_introduction_3_paragraph_proof(
            o=o)
        return output

    def check_inference_validity(self, p_neq_p: FormulaStatement = None,
            inconsistent_theory: TheoryElaborationSequence = None,
            t: TheoryElaborationSequence = None) -> bool:
        verify(inconsistent_theory.contains_theoretical_objct(p_neq_p),
            'Statement ⌜p_neq_p⌝ must be contained in theory ⌜inconsistent_theory⌝''s hierarchy.',
            p_neq_p=p_neq_p, inconsistent_theory=inconsistent_theory, slf=self)
        verify(p_neq_p.relation is p_neq_p.theory.universe_of_discourse.relations.inequality,
            'The relation of statement ⌜p_neq_p⌝ must be ⌜inequality⌝.', p_neq_p=p_neq_p,
            inconsistent_theory=inconsistent_theory, slf=self)
        verify(p_neq_p.valid_proposition.parameters[0].is_formula_syntactically_equivalent_to(
            p_neq_p.valid_proposition.parameters[1]),
            'The two ⌜p⌝ terms in  ⌜p_neq_p⌝ must be formula-syntactically-equivalent.',
            p_neq_p=p_neq_p, inconsistent_theory=inconsistent_theory, slf=self)
        return True

    def infer_formula(self, p_neq_p: (None, FormulaStatement) = None,
            inconsistent_theory: (None, TheoryElaborationSequence) = None,
            t: (None, TheoryElaborationSequence) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p_neq_p, inconsistent_theory, echo=echo)

    def infer_formula_statement(self, p_neq_p: (None, FormulaStatement) = None,
            inconsistent_theory: (None, TheoryElaborationSequence) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        if inconsistent_theory is None:
            # The inconsistent_theory can be unambiguously defaulted
            # when all terms are contained in the same theory.
            inconsistent_theory = p_neq_p.t
        return super().infer_formula_statement(p_neq_p, inconsistent_theory, nameset=nameset,
            ref=ref, paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class ModusPonensInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`modus-ponens<modus_ponens_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.modus_ponens
        dashed_name = 'modus-ponens'
        acronym = 'mp'
        abridged_name = None
        name = 'modus ponens'
        explicit_name = 'modus ponens inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def check_inference_validity(self, p_implies_q: FormulaStatement, p: FormulaStatement,
            t: TheoryElaborationSequence) -> bool:
        """

        :param args: A statement (P ⟹ Q), and a statement P
        :param t:
        :return: A formula Q
        """
        p_implies_q = verify_formula_statement(t=t, arity=2, input_value=p_implies_q)
        p = verify_formula_statement(t=t, arity=2, input_value=p)
        verify(t.contains_theoretical_objct(p_implies_q),
            'Statement ⌜p_implies_q⌝ is not contained in theory ⌜t⌝''s hierarchy.',
            p_implies_q=p_implies_q, t=t, slf=self)
        p_implies_q = unpack_formula(p_implies_q)
        verify(p_implies_q.relation is t.u.r.implication,
            'The relation of formula ⌜p_implies_q⌝ is not an implication.',
            p_implies_q_relation=p_implies_q.relation, p_implies_q=p_implies_q, t=t, slf=self)
        verify(t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.', p_prime=p, t=t, slf=self)
        p = unpack_formula(p)
        p_prime = unpack_formula(p_implies_q.parameters[0])
        # The antecedant of the implication may contain free-variables,
        # store these in a mask for masked-formula-similitude comparison.
        verify(p.is_formula_syntactically_equivalent_to(p_prime),
            'Formula ⌜p_prime⌝ in statement ⌜p_implies_q⌝ must be formula-syntactically-equivalent to statement '
            '⌜p⌝.', p_implies_q=p_implies_q, p=p, p_prime=p_prime, t=t, slf=self)
        return True

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_modus_ponens_paragraph_proof(o=o)
        return output

    def infer_formula(self, p_implies_q: (tuple, Formula, FormulaStatement) = None,
            p: (tuple, Formula, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p_implies_q, p, echo=echo)

    def infer_formula_statement(self, p_implies_q: (None, FormulaStatement) = None,
            p: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p_implies_q = verify_formula_statement(t=self.t, arity=2, input_value=p_implies_q)
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        return super().infer_formula_statement(p_implies_q, p, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class ModusTollensInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`modus-tollens<modus_tollens_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.modus_ponens
        dashed_name = 'modus-tollens'
        acronym = 'mt'
        abridged_name = None
        name = 'modus tollens'
        explicit_name = 'modus tollens inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def check_inference_validity(self, p_implies_q: FormulaStatement, p: FormulaStatement,
            t: TheoryElaborationSequence) -> bool:
        """

        :param args: A statement (P ⟹ Q), and a statement P
        :param t:
        :return: A formula Q
        """
        p_implies_q = verify_formula_statement(t=t, arity=2, input_value=p_implies_q)
        p = verify_formula_statement(t=t, arity=2, input_value=p)
        verify(t.contains_theoretical_objct(p_implies_q),
            'Statement ⌜p_implies_q⌝ is not contained in theory ⌜t⌝''s hierarchy.',
            p_implies_q=p_implies_q, t=t, slf=self)
        p_implies_q = unpack_formula(p_implies_q)
        verify(p_implies_q.relation is t.u.r.implication,
            'The relation of formula ⌜p_implies_q⌝ is not an implication.',
            p_implies_q_relation=p_implies_q.relation, p_implies_q=p_implies_q, t=t, slf=self)
        verify(t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.', p_prime=p, t=t, slf=self)
        p = unpack_formula(p)
        p_prime = unpack_formula(p_implies_q.parameters[0])
        # The antecedant of the implication may contain free-variables,
        # store these in a mask for masked-formula-similitude comparison.
        verify(p.is_formula_syntactically_equivalent_to(p_prime),
            'Formula ⌜p_prime⌝ in statement ⌜p_implies_q⌝ must be formula-syntactically-equivalent to statement '
            '⌜p⌝.', p_implies_q=p_implies_q, p=p, p_prime=p_prime, t=t, slf=self)
        return True

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_modus_tollens_paragraph_proof(o=o)
        return output

    def infer_formula(self, p_implies_q: (tuple, Formula, FormulaStatement) = None,
            p: (tuple, Formula, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p_implies_q, p, echo=echo)

    def infer_formula_statement(self, p_implies_q: (None, FormulaStatement) = None,
            p: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p_implies_q = verify_formula_statement(t=self.t, arity=2, input_value=p_implies_q)
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        return super().infer_formula_statement(p_implies_q, p, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class ProofByContradiction1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`proof-by-contradiction-1<proof_by_contradiction_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.proof_by_contradiction_1
        dashed_name = 'proof-by-contradiction-1'
        acronym = 'pbc1'
        abridged_name = None
        name = 'proof by contradiction #1'
        explicit_name = 'proof by contradiction #1 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def check_inference_validity(self, not_p_hypothesis: Hypothesis,
            inc_hypothesis: InferredStatement, t: TheoryElaborationSequence,
            echo: (None, bool) = None) -> bool:
        """

        :param not_p_hypothesis: The hypothesis-statement in the parent theory.
        :param inc_hypothesis: The contradiction-statement Inc(Tn) where Tn is the hypothesis-theory.
        :param t: The current (parent) theory.
        :param echo:
        :return:
        """
        verify(is_in_class(not_p_hypothesis, classes.hypothesis), '⌜not_p⌝ must be an hypothesis.',
            not_p=not_p_hypothesis, slf=self)
        verify(is_in_class(inc_hypothesis, classes.inferred_proposition),
            '⌜inc_not_p⌝ must be an inferred-statement.', inc_not_p=inc_hypothesis, slf=self)
        verify(t.contains_theoretical_objct(not_p_hypothesis), '⌜not_p⌝ must be in theory ⌜t⌝.',
            not_p=not_p_hypothesis, t=t, slf=self)
        verify(not_p_hypothesis.hypothesis_child_theory.extended_theory is t,
            '⌜not_p.hypothetical_theory⌝ must extend the parent theory ⌜t⌝.',
            not_p_hypothetical_theory=not_p_hypothesis.hypothesis_child_theory,
            not_p=not_p_hypothesis, t=t, slf=self)
        verify(inc_hypothesis.relation is t.u.relations.inconsistency,
            '⌜inc_not_p.relation⌝ must be of form (Inc(Hn)).',
            inc_not_p_relation=inc_hypothesis.relation, inc_not_p=inc_hypothesis, t=t, slf=self)
        verify(inc_hypothesis.valid_proposition.parameters[
                   0] is not_p_hypothesis.hypothesis_child_theory,
            '⌜inc_not_p⌝ must be of form (Inc(Hn)) where parameter[0] Hn is the '
            'hypothetical-theory.',
            inc_not_p_parameters_0=inc_hypothesis.valid_proposition.parameters[0],
            not_p_hypothetical_theory=not_p_hypothesis.hypothesis_child_theory, t=t, slf=self)
        return True

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_proof_by_contradiction_1_paragraph_proof(
            o=o)
        return output

    def infer_formula(self, not_p_hypothesis: (None, Hypothesis) = None,
            inc_hypothesis: (None, FormulaStatement) = None, echo: (None, bool) = None) -> Formula:
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(not_p_hypothesis, inc_hypothesis, echo=echo)

    def infer_formula_statement(self, not_p_hypothesis: (None, FormulaStatement) = None,
            inc_hypothesis: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        return super().infer_formula_statement(not_p_hypothesis, inc_hypothesis, nameset=nameset,
            ref=ref, paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class ProofByContradiction2Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`proof-by-contradiction-2<proof_by_contradiction_2_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.proof_by_contradiction_2
        dashed_name = 'proof-by-contradiction-2'
        acronym = 'pbc2'
        abridged_name = None
        name = 'proof by contradiction #2'
        explicit_name = 'proof by contradiction #2 inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def check_inference_validity(self, x_neq_y_hypothesis: Hypothesis,
            inc_hypothesis: InferredStatement, t: TheoryElaborationSequence,
            echo: (None, bool) = None) -> bool:
        """

        :param x_neq_y_hypothesis: The hypothesis-statement in the parent theory.
        :param inc_hypothesis: The contradiction-statement Inc(Tn) where Tn is the hypothesis-theory.
        :param t: The current (parent) theory.
        :param echo:
        :return:

        TODO: ProofByContradiction2Declaration.verify_args(): Make systematic verifications. I doubt it is still possible to call the method with wrong parameters.
        """
        inc_hypothesis: InferredStatement = verify_formula_statement(t=t, arity=1,
            input_value=inc_hypothesis)
        verify(is_in_class(x_neq_y_hypothesis, classes.hypothesis),
            '⌜x_neq_y_hypothesis⌝ must be an hypothesis.', p_neq_q=x_neq_y_hypothesis, slf=self)
        verify(t.contains_theoretical_objct(x_neq_y_hypothesis), '⌜x_neq_y⌝ must be in theory ⌜t⌝.',
            p_neq_q=x_neq_y_hypothesis, t=t, slf=self)
        verify(x_neq_y_hypothesis.hypothesis_child_theory.extended_theory is t,
            '⌜x_neq_y_hypothesis.hypothesis_child_theory⌝ must extend the parent theory ⌜t⌝.',
            p_neq_q_hypothetical_theory=x_neq_y_hypothesis.hypothesis_child_theory,
            p_neq_q=x_neq_y_hypothesis, t=t, slf=self)
        verify(inc_hypothesis.valid_proposition.relation is t.u.relations.inconsistency,
            '⌜inc_hypothesis.relation⌝ must be the inconsistency relation.',
            inc_hypothesis_relation=inc_hypothesis.relation, inc_hypothesis=inc_hypothesis, t=t,
            slf=self)
        inc_hypothesis_hypothesis: Hypothesis = inc_hypothesis.valid_proposition.parameters[0]
        x_neq_y_prime: FormulaStatement = inc_hypothesis.parameters[1]
        verify(x_neq_y_hypothesis.child_statement.is_formula_syntactically_equivalent_to(
            x_neq_y_prime),
            '⌜x_neq_y⌝ must be formula-syntactically-equivalent to ⌜x_neq_y⌝ in ⌜inc_x_neq_y⌝.',
            x_neq_y_hypothesis=x_neq_y_hypothesis, x_neq_y_prime=x_neq_y_prime, t=t, slf=self)
        return True

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_proof_by_contradiction_2_paragraph_proof(
            o=o)
        return output

    def infer_formula(self, x_neq_y_hypothesis: (None, Hypothesis) = None,
            inc_hypothesis: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(x_neq_y_hypothesis, inc_hypothesis, echo=echo)

    def infer_formula_statement(self, x_neq_y_hypothesis: (None, FormulaStatement) = None,
            inc_hypothesis: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        return super().infer_formula_statement(x_neq_y_hypothesis, inc_hypothesis, nameset=nameset,
            ref=ref, paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class ProofByRefutation1Inclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`proof-by-refutation-1<proof_by_refutation_1_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.proof_by_refutation_1
        dashed_name = 'proof-by-refutation'
        acronym = 'pbr'
        abridged_name = None
        name = 'proof by refutation'
        explicit_name = 'proof by refutation inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def check_inference_validity(self, p_hypothesis: Hypothesis, inc_hypothesis: InferredStatement,
            t: TheoryElaborationSequence, echo: (None, bool) = None) -> bool:
        """

        :param p_hypothesis: The hypothesis-statement in the parent theory.
        :param inc_hypothesis: The refutation-statement Inc(Tn) where Tn is the hypothesis-theory.
        :param t: The current (parent) theory.
        :param echo:
        :return:
        """
        verify(is_in_class(p_hypothesis, classes.hypothesis), '⌜p⌝ must be an hypothesis.',
            p=p_hypothesis, slf=self)
        verify(is_in_class(inc_hypothesis, classes.inferred_proposition),
            '⌜inc_p⌝ must be an inferred-statement.', inc_p=inc_hypothesis, slf=self)
        verify(t.contains_theoretical_objct(p_hypothesis), '⌜p⌝ must be in theory ⌜t⌝.',
            p=p_hypothesis, t=t, slf=self)
        verify(p_hypothesis.hypothesis_child_theory.extended_theory is t,
            '⌜p.hypothetical_theory⌝ must extend the parent theory ⌜t⌝.',
            p_hypothetical_theory=p_hypothesis.hypothesis_child_theory, p=p_hypothesis, t=t,
            slf=self)
        verify(inc_hypothesis.relation is t.u.relations.inconsistency,
            '⌜inc_p.relation⌝ must be of form (Inc(Hn)).', inc_p_relation=inc_hypothesis.relation,
            inc_p=inc_hypothesis, t=t, slf=self)
        verify(
            inc_hypothesis.valid_proposition.parameters[0] is p_hypothesis.hypothesis_child_theory,
            '⌜inc_p⌝ must be of form (Inc(Hn)) where parameter[0] Hn is the hypothetical-theory.',
            inc_p_parameters_0=inc_hypothesis.valid_proposition.parameters[0],
            p_hypothetical_theory=p_hypothesis.hypothesis_child_theory, t=t, slf=self)
        # TODO: ProofByContradictionDeclaration.verify_args: check that the parent theory is
        #  stable???
        # TODO: ProofByContradictionDeclaration.verify_args: check that the hypothetical-theory
        #  is stable
        return True

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_proof_by_refutation_1_paragraph_proof(o=o)
        return output

    def infer_formula(self, p_hypothesis: (None, Hypothesis) = None,
            inc_hypothesis: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p_hypothesis, inc_hypothesis, echo=echo)

    def infer_formula_statement(self, p_hypothesis: (None, FormulaStatement) = None,
            inc_hypothesis: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        return super().infer_formula_statement(p_hypothesis, inc_hypothesis, nameset=nameset,
            ref=ref, paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class ProofByRefutation2Inclusion(InferenceRuleInclusion):
    """

    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.proof_by_refutation_2
        dashed_name = 'proof-by-refutation-of-equality'
        acronym = 'pbre'
        abridged_name = None
        name = 'proof by refutation of equality'
        explicit_name = 'proof by refutation of equality inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_proof_by_refutation_2_paragraph_proof(o=o)
        return output

    def check_inference_validity(self, p_eq_q_hypothesis: Hypothesis,
            inc_hypothesis: InferredStatement, t: TheoryElaborationSequence,
            echo: (None, bool) = None) -> bool:
        """

        :param p_eq_q_hypothesis: The hypothesis-statement in the parent theory.
        :param inc_hypothesis: The refutation-statement Inc(Tn) where Tn is the hypothesis-theory.
        :param t: The current (parent) theory.
        :param echo:
        :return:
        """
        verify(is_in_class(p_eq_q_hypothesis, classes.hypothesis), '⌜p⌝ must be an hypothesis.',
            p=p_eq_q_hypothesis, slf=self)
        verify(is_in_class(inc_hypothesis, classes.inferred_proposition),
            '⌜inc_p⌝ must be an inferred-statement.', inc_p=inc_hypothesis, slf=self)
        verify(t.contains_theoretical_objct(p_eq_q_hypothesis), '⌜p⌝ must be in theory ⌜t⌝.',
            p=p_eq_q_hypothesis, t=t, slf=self)
        verify(p_eq_q_hypothesis.hypothesis_child_theory.extended_theory is t,
            '⌜p.hypothetical_theory⌝ must extend the parent theory ⌜t⌝.',
            p_hypothetical_theory=p_eq_q_hypothesis.hypothesis_child_theory, p=p_eq_q_hypothesis,
            t=t, slf=self)
        verify(inc_hypothesis.valid_proposition.relation is t.u.relations.inconsistency,
            '⌜inc_p.relation⌝ must be of form (Inc(Hn)).',
            inc_p_relation=inc_hypothesis.valid_proposition.relation, inc_p=inc_hypothesis, t=t,
            slf=self)
        # TODO: ProofByContradictionDeclaration.verify_args: check that the parent theory is
        #  stable???
        # TODO: ProofByContradictionDeclaration.verify_args: check that the hypothetical-theory
        #  is stable
        return True

    def infer_formula(self, x_eq_y_hypothesis: (None, Hypothesis) = None,
            inc_hypothesis: (None, FormulaStatement) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(x_eq_y_hypothesis, inc_hypothesis, echo=echo)

    def infer_formula_statement(self, x_eq_y_hypothesis: (None, FormulaStatement) = None,
            inc_hypothesis: (None, FormulaStatement) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None, echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        return super().infer_formula_statement(x_eq_y_hypothesis, inc_hypothesis, nameset=nameset,
            ref=ref, paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class VariableSubstitutionInclusion(InferenceRuleInclusion):
    """This python class models the inclusion of :ref:`variable-substitution<variable_substitution_math_inference_rule>` as a valid :ref:`inference-rule<inference_rule_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` .
    """

    def __init__(self, t: TheoryElaborationSequence, echo: (None, bool) = None,
            proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.variable_substitution
        dashed_name = 'variable-substitution'
        acronym = 'vs'
        abridged_name = None
        name = 'variable substitution'
        explicit_name = 'variable substitution inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, echo=echo,
            proof=proof)

    def check_inference_validity(self, p: FormulaStatement, phi: (None, tuple[TheoreticalObject]),
            t: TheoryElaborationSequence, echo: (None, bool) = None, **kwargs) -> bool:
        """Verify if the arguments comply syntactically with the inference-rule.
        """
        verify(is_in_class(p, classes.formula_statement), '⌜p⌝ must be a formula-statement.', p=p,
            t=t, slf=self)
        verify(t.contains_theoretical_objct(p), '⌜p⌝ must be contained in ⌜t⌝.', p=p, t=t, slf=self)
        verify(isinstance(phi, tuple), '⌜phi⌝ must be a tuple.', phi=phi, t=t, slf=self)
        x_oset = unpack_formula(p).get_variable_ordered_set()
        verify(len(x_oset) == len(phi),
            'The cardinality of the canonically ordered free-variables.')
        # Substitution objects in Y must be declared in U,
        # but they may not be referenced yet in T's extension.
        for y in phi:
            verify(isinstance(y, TheoreticalObject), '⌜y⌝ in ⌜phi⌝ must be a theoretical-object.',
                y=y, t=t, slf=self)
            verify(y.u is self.u, '⌜y⌝ and ⌜self⌝ do not share the same universe-of-discourse.',
                y=y, y_u=y.u, slf=self, slf_u=self.u)

        # TODO: Add a verification step: the variable is not locked.
        return True

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Overrides the generic paragraph proof method."""
        output = yield from configuration.locale.compose_variable_substitution_paragraph_proof(o=o)
        return output

    def infer_formula(self, p: (None, FormulaStatement) = None,
            phi: (None, tuple[TheoreticalObject]) = None, echo: (None, bool) = None):
        """
        .. include:: ../../include/construct_formula_python_method.rstinc

        """
        return super().infer_formula(p, phi, echo=echo)

    def infer_formula_statement(self, p: (None, FormulaStatement) = None,
            phi: (None, TheoreticalObject, tuple[TheoreticalObject]) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            paragraph_header: (None, ParagraphHeader) = None, subtitle: (None, str) = None,
            echo: (None, bool) = None) -> InferredStatement:
        """
        .. include:: ../../include/infer_formula_statement_python_method.rstinc

        """
        p = verify_formula_statement(t=self.t, arity=None, input_value=p)
        if isinstance(phi, TheoreticalObject):
            # If phi is passed as an theoretical-object,
            # embed it into a tuple as we expect tuple[TheoreticalObject] as input type.
            phi = tuple([phi])
        return super().infer_formula_statement(p, phi, nameset=nameset, ref=ref,
            paragraph_header=paragraph_header, subtitle=subtitle, echo=echo)


class InferenceRuleInclusionCollection(collections.UserDict):
    """This python class models the collection of :ref:`inference-rules<inference_rule_math_concept>` :ref:`included<object_inclusion_math_concept>` in a :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>`.

    In complement, it conveniently exposes as python properties a catalog of natively supported :ref:`inference-rules<inference_rule_math_concept>` that are automatically :ref:`included<object_inclusion_math_concept>` in the :ref:`theory-elaboration-sequence<theory_elaboration_sequence_math_concept>` when they are accessed for the first time.

    """

    def __init__(self, t: TheoryElaborationSequence):
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
        self._definition_interpretation = None
        self._disjunction_elimination = None  # TODO: IMPLEMENT disjunction_elimination
        self._disjunction_introduction_1 = None
        self._disjunction_introduction_2 = None
        self._double_negation_elimination = None
        self._double_negation_introduction = None
        self._equality_commutativity = None
        self._equal_terms_substitution = None
        self._inconsistency_introduction_1 = None
        self._inconsistency_introduction_2 = None
        self._inconsistency_introduction_3 = None
        self._modus_ponens = None
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

        The implication (P ⟹ Q) may contain free-variables. If such is the
        case, the resulting Q' is computed by extracting variable-values
        from P' and applying variable-substitution.


        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._modus_ponens is None:
            self._modus_ponens = ModusPonensInclusion(t=self.t)
        return self._modus_ponens

    @property
    def mp(self) -> ModusPonensInclusion:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P ⊢ Q.

        Unabridged property: u.i.modus_ponens

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.modus_ponens

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


class UniverseOfDiscourse(SymbolicObject):
    """This python class models a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .
    """

    def __init__(self, nameset: (None, str, NameSet) = None, symbol: (None, str, StyledText) = None,
            dashed_name: (None, str, StyledText) = None, name: (None, str, ComposableText) = None,
            echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_universe_of_discourse_declaration,
            configuration.echo_default, False)
        self.axioms = dict()
        self.definitions = dict()
        self.formulae = dict()
        self._inference_rules = InferenceRuleDeclarationCollection(u=self)
        self._relations = RelationDict(u=self)
        self.theories = dict()
        self._simple_objcts = SimpleObjctDict(u=self)
        self.symbolic_objcts = dict()
        self.theories = dict()
        # self.variables = dict()
        # Unique name indexes
        # self.symbol_indexes = dict()
        # self.titles = dict()

        if nameset is None:
            symbol = prioritize_value(symbol,
                StyledText(plaintext='U', text_style=text_styles.script_normal))
            dashed_name = prioritize_value(symbol,
                StyledText(plaintext='universe-of-discourse-', text_style=text_styles.serif_italic))
            index = index_universe_of_discourse_symbol(base=symbol)
            nameset = NameSet(symbol=symbol, dashed_name=dashed_name, index=index, name=name)
        elif isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            index = index_universe_of_discourse_symbol(base=nameset)
            nameset = NameSet(s=nameset, index=index, name=name)
        super().__init__(is_universe_of_discourse=True, is_theory_foundation_system=False,
            nameset=nameset, universe_of_discourse=None, echo=False)
        super()._declare_class_membership(classes.universe_of_discourse)
        if echo:
            self.echo()

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

    def cross_reference_axiom(self, a: AxiomDeclaration) -> bool:
        """Cross-references an axiom in this universe-of-discourse.

        :parameter a: an axiom-declaration.
        """
        verify(a.nameset not in self.axioms.keys() or a is self.axioms[a.nameset],
            'The symbol of parameter ⌜a⌝ is already referenced as a distinct axiom in this '
            'universe-of-discourse.', a=a, universe_of_discourse=self)
        if a not in self.axioms:
            self.axioms[a.nameset] = a
            return True
        else:
            return False

    def cross_reference_definition(self, d: DefinitionDeclaration) -> bool:
        """Cross-references a definition in this universe-of-discourse.

        :parameter d: a definition.
        """
        verify(d.nameset not in self.definitions.keys() or d is self.definitions[d.nameset],
            'The symbol of parameter ⌜d⌝ is already referenced as a distinct definition in this '
            'universe-of-discourse.', a=d, universe_of_discourse=self)
        if d not in self.definitions:
            self.definitions[d.nameset] = d
            return True
        else:
            return False

    def cross_reference_formula(self, phi: Formula):
        """Cross-references a formula in this universe-of-discourse.

        :param phi: a formula.
        """
        verify(is_in_class(phi, classes.formula),
            'Cross-referencing a formula in a universe-of-discourse requires '
            'an object of type Formula.', phi=phi, slf=self)
        verify(phi.nameset not in self.formulae.keys() or phi is self.formulae[phi.nameset],
            'Cross-referencing a formula in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.', phi_symbol=phi.nameset, phi=phi,
            slf=self)
        if phi not in self.formulae:
            self.formulae[phi.nameset] = phi

    def cross_reference_inference_rule(self, ir: InferenceRuleDeclaration) -> bool:
        """Cross-references an inference-rule in this universe-of-discourse.

        :param ir: an inference-rule.
        """
        verify(is_in_class(ir, classes.inference_rule), 'Parameter ⌜ir⌝ is not an inference-rule.',
            ir=ir, universe_of_discourse=self)
        verify(
            ir.nameset not in self.inference_rules.keys() or ir is self.inference_rules[ir.nameset],
            'The symbol of parameter ⌜ir⌝ is already referenced as a distinct inference-rule in '
            'this universe-of-discourse.', ir=ir, universe_of_discourse=self)
        if ir not in self.inference_rules:
            self.inference_rules[ir.nameset] = ir
            return True
        else:
            return False

    def cross_reference_relation(self, r: Relation):
        """Cross-references a relation in this universe-of-discourse.

        :param r: a relation.
        """
        verify(isinstance(r, Relation),
            'Cross-referencing a relation in a universe-of-discourse requires '
            'an object of type Relation.')
        verify(r.nameset not in self.relations.keys() or r is self.relations[r.nameset],
            'Cross-referencing a relation in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.', r_symbol=r.nameset, r=r, slf=self)
        if r not in self.relations:
            self.relations[r.nameset] = r

    def cross_reference_simple_objct(self, o: SimpleObjct):
        """Cross-references a simple-objct in this universe-of-discourse.

        :param o: a simple-objct.
        """
        verify(isinstance(o, SimpleObjct),
            'Cross-referencing a simple-objct in a universe-of-discourse requires '
            'an object of type SimpleObjct.')
        verify(o.nameset not in self.simple_objcts.keys() or o is self.simple_objcts[o.nameset],
            'Cross-referencing a simple-objct in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.', o_symbol=o.nameset, o=o, slf=self)
        if o not in self.simple_objcts:
            self.simple_objcts[o.nameset] = o

    def cross_reference_symbolic_objct(self, o: TheoreticalObject):
        """Cross-references a symbolic-objct in this universe-of-discourse.

        :param o: a symbolic-objct.
        """
        verify(is_in_class(o=o, c=classes.symbolic_objct),
            'Cross-referencing a symbolic-objct in a universe-of-discourse requires '
            'an object of type SymbolicObjct.', o=o, slf=self)
        duplicate = self.symbolic_objcts.get(o.nameset)
        verify(severity=verification_severities.warning, assertion=duplicate is None,
            msg='A symbolic-object already exists in the current universe-of-discourse with a '
                'duplicate (symbol, index) pair.', o=o, duplicate=duplicate, slf=self)
        self.symbolic_objcts[o.nameset] = o

    def cross_reference_theory(self, t: TheoryElaborationSequence):
        """Cross-references a theory in this universe-of-discourse.

        :param t: a formula.
        """
        verify(is_in_class(t, classes.theory_elaboration),
            'Cross-referencing a theory in a universe-of-discourse requires '
            'an object of type Theory.', t=t, slf=self)
        verify(t.nameset not in self.theories.keys() or t is self.theories[t.nameset],
            'Cross-referencing a theory in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.', t_symbol=t.nameset, t=t, slf=self)
        if t not in self.theories:
            self.theories[t.nameset] = t

    def declare_formula(self, relation: Relation, *parameters, nameset: (None, str, NameSet) = None,
            lock_variable_scope: (None, bool) = None, echo: (None, bool) = None):
        """Declare a new formula in this universe-of-discourse.

        This method is a shortcut for Formula(universe_of_discourse=self, . . d.).

        A formula is *declared* in a theory, and not *stated*, because it is not a statement,
        i.e. it is not necessarily true in this theory.
        """
        phi = Formula(relation=relation, parameters=parameters, universe_of_discourse=self,
            nameset=nameset, lock_variable_scope=lock_variable_scope, echo=echo)
        return phi

    def declare_free_variable(self, symbol: (None, str, StyledText) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, echo: (None, bool) = None):
        """Declare a free-variable in this universe-of-discourse.

        A shortcut function for FreeVariable(universe_of_discourse=u, ...)

        :param symbol:
        :return:
        """
        x = FreeVariable(universe_of_discourse=self, nameset=symbol,
            status=FreeVariable.scope_initialization_status, echo=echo)
        return x

    def declare_symbolic_objct(self, symbol: (None, str, StyledText) = None,
            index: (None, int, str) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None) -> SymbolicObject:
        return SymbolicObject(universe_of_discourse=self, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, echo=echo)

    def declare_theory(self, symbol: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, ref: (None, str) = None,
            subtitle: (None, str) = None, extended_theory: (None, TheoryElaborationSequence) = None,
            extended_theory_limit: (None, Statement) = None, stabilized: bool = False,
            echo: bool = None):
        """Declare a new theory in this universe-of-discourse.

        Shortcut for Theory(universe_of_discourse, ...).

        :param nameset:
        :param is_theory_foundation_system:
        :param extended_theory:
        :return:
        """
        return TheoryElaborationSequence(u=self, symbol=symbol, nameset=nameset, ref=ref,
            subtitle=subtitle, extended_theory=extended_theory,
            extended_theory_limit=extended_theory_limit, stabilized=stabilized, echo=echo)

    def declare_axiom(self, natural_language: str, symbol: (None, str, StyledText) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None) -> AxiomDeclaration:
        """:ref:`Declare<object_declaration_math_concept>` a new axiom in this universe-of-discourse.
        """
        return AxiomDeclaration(u=self, natural_language=natural_language, symbol=symbol,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle,
            paragraph_header=paragraph_header, nameset=nameset, echo=echo)

    def declare_definition(self, natural_language: str, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """Elaborate a new axiom 𝑎 in this universe-of-discourse.
        """
        return DefinitionDeclaration(u=self, natural_language=natural_language, symbol=symbol,
            index=index, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, nameset=nameset, echo=echo)

    def echo(self):
        return repm.prnt(self.rep_creation(cap=True))

    def f(self, relation: (Relation, FreeVariable), *parameters,
            nameset: (None, str, NameSet) = None, lock_variable_scope: (None, bool) = None,
            echo: (None, bool) = None):
        """Declare a new formula in this universe-of-discourse.

        Shortcut for self.elaborate_formula(. . .)."""
        return self.declare_formula(relation, *parameters, nameset=nameset,
            lock_variable_scope=lock_variable_scope, echo=echo)

    def get_symbol_max_index(self, symbol: ComposableText) -> int:
        """Return the highest index for that symbol-base in the universe-of-discourse."""
        # if symbol in self.symbol_indexes.keys():
        #    return self.symbol_indexes[symbol]
        # else:
        #    return 0
        same_symbols = tuple((nameset.index_as_int for nameset in self.symbolic_objcts.keys() if
            nameset.symbol == symbol and nameset.index_as_int is not None))
        return max(same_symbols, default=0)

    @property
    def i(self) -> InferenceRuleDeclarationCollection:
        """The (possibly empty) collection of :ref:`inference-rules<inference_rule_math_concept>` declared in this :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .

        Unabridged name: inference_rule
        """
        return self.inference_rules

    def index_symbol(self, symbol: StyledText) -> int:
        """Given a symbol-base S (i.e. an unindexed symbol), returns a unique integer n
        such that (S, n) is a unique identifier in this instance of UniverseOfDiscourse.

        :param symbol: The symbol-base.
        :return:
        """
        return self.get_symbol_max_index(symbol) + 1

    @property
    def inference_rules(self) -> InferenceRuleDeclarationCollection:
        """The (possibly empty) collection of :ref:`inference-rules<inference_rule_math_concept>` declared in this in this :ref:`universe-of-discourse<universe_of_discourse_math_concept>` .

        Abridged name: i
        """
        return self._inference_rules

    @property
    def o(self) -> SimpleObjctDict:
        """The (possibly empty) collection of simple-objects declared in this in this universe-of-discourse.

        Unabridged name: simple_objcts

        Well-known simple-objcts are exposed as python properties. In general, a well-known
        simple-objct is declared in the universe-of-discourse the first time its property is
        accessed.
        """
        return self.simple_objcts

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

    def t(self, symbol: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            ref: (None, str) = None, subtitle: (None, str) = None,
            extended_theory: (None, TheoryElaborationSequence) = None,
            extended_theory_limit: (None, Statement) = None, stabilized: bool = False,
            echo: bool = None):
        """Declare a new theory in this universe-of-discourse.

        Shortcut for self.declare_theory(...).

        :param nameset:
        :param is_theory_foundation_system:
        :param extended_theory:
        :return:
        """
        return self.declare_theory(symbol=symbol, nameset=nameset, ref=ref, subtitle=subtitle,
            extended_theory=extended_theory, extended_theory_limit=extended_theory_limit,
            stabilized=stabilized, echo=echo)

    def take_note(self, t: TheoryElaborationSequence, content: str,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """Take a note, make a comment, or remark."""
        verify(t.universe_of_discourse is self,
            'This universe-of-discourse 𝑢₁ (self) is distinct from the universe-of-discourse 𝑢₂ '
            'of the theory '
            'parameter 𝑡.')

        return NoteInclusion(t=t, content=content, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, nameset=nameset,
            echo=echo)

    # @FreeVariableContext()
    @contextlib.contextmanager
    def v(self, symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            echo: (None, bool) = None):
        """Declare a free-variable in this universe-of-discourse.

        This method is expected to be as in a with statement,
        it yields an instance of FreeVariable,
        and automatically lock the variable scope when the with left.

        Example: with u.v('x') as x, u.v('y') as y:
        some code...

        To manage variable scope extensions and locking expressly,
        use declare_free_variable() instead.
        """
        # return self.declare_free_variable(symbol=symbol)
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

    def __init__(self, i: InferenceRuleInclusion, premises: typing.NamedTuple,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None, echo_proof: (None, bool) = None):
        """Include (aka allow) an inference_rule in a theory-elaboration.
        """
        echo = prioritize_value(echo, configuration.echo_inferred_statement,
            configuration.echo_statement, configuration.echo_default, False)
        t: TheoryElaborationSequence = i.t
        self._inference_rule = i
        self._premises = premises
        # Check that the premises are valid.
        # If they are not, raise a Punctilious Exception and stop processing.
        # If they are, complete the inference process.
        self._inference_rule.check_premises_validity(**premises._asdict(), raise_exception=True)
        valid_proposition = self._inference_rule.construct_formula(**premises._asdict())
        super().__init__(theory=t, valid_proposition=valid_proposition, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name, ref=ref,
            subtitle=subtitle, nameset=nameset, paragraphe_header=paragraph_header, echo=False)
        super()._declare_class_membership(declarative_class_list.inferred_proposition)
        if self.valid_proposition.relation is self.t.u.r.inconsistency and is_in_class(
                self.valid_proposition.parameters[0], classes.theory_elaboration):
            # This inferred-statement proves the inconsistency of its argument,
            # its argument is a theory-elaboration-sequence (i.e. it is not a free-variable),
            # it follows that we must change the consistency attribute of that theory.
            inconsistent_theory: TheoryElaborationSequence
            inconsistent_theory = self.valid_proposition.parameters[0]
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
        output = yield from configuration.locale.compose_inferred_statement_report(o=self,
            proof=proof)
        return output

    def echo(self, proof: (None, bool) = None):
        proof = prioritize_value(proof, configuration.echo_proof, True)
        repm.prnt(self.rep_report(proof=proof))

    @property
    def parameters(self) -> tuple:
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

    def __init__(self, p, not_p, nameset=None, paragraphe_header=None, theory=None, title=None):
        if title is None:
            title = 'THEORY INCONSISTENCY'
        paragraphe_header = paragraph_headers.proposition if paragraphe_header is None else paragraphe_header
        self.p = p
        self.not_p = not_p
        valid_proposition = InconsistencyIntroductionInferenceRuleOBSOLETE.execute_algorithm(
            theory=theory, p=p, not_p=not_p)
        super().__init__(theory=theory, valid_proposition=valid_proposition,
            paragraphe_header=paragraphe_header, title=title, nameset=nameset)
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
    configuration.default_definition_declaration_symbol = ScriptNormal('D')
    configuration.default_definition_inclusion_symbol = SerifItalic('D')
    configuration.default_formula_symbol = SerifItalic(plaintext='phi', unicode='𝜑')
    configuration.default_free_variable_symbol = StyledText(plaintext='x',
        text_style=text_styles.serif_bold)
    configuration.default_parent_hypothesis_statement_symbol = SerifItalic('H')
    configuration.default_child_hypothesis_theory_symbol = ScriptNormal('H')
    configuration.default_inference_rule_declaration_symbol = SerifItalic('I')
    configuration.default_inference_rule_inclusion_symbol = SerifItalic('I')
    configuration.default_note_symbol = SerifItalic('note')
    configuration.default_relation_symbol = SerifItalic('r')
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
    configuration.echo_free_variable_declaration = False
    configuration.echo_hypothesis = None
    configuration.echo_inclusion = None
    configuration.echo_inference_rule_declaration = False
    configuration.echo_inference_rule_inclusion = True
    configuration.echo_inferred_statement = True
    configuration.echo_note = True
    configuration.echo_proof = True
    configuration.echo_relation = None
    configuration.echo_simple_objct_declaration = None
    configuration.echo_statement = True
    configuration.echo_symbolic_objct = None
    configuration.echo_theory_elaboration_sequence_declaration = None
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


class Package:
    def __init__(self):
        pass


class Article:
    """TODO: Article: for future development."""

    def __init__(self):
        self._elements = []

    def write_element(self, element: SymbolicObject):
        self._elements.append(element)


pass
