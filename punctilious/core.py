from __future__ import annotations
import collections.abc
import textwrap
import typing
import warnings
import repm
import contextlib
import abc
import collections
import pyvis
import networkx as nx
import unicode_utilities
import unidecode
from plaintext import Plaintext
from unicode_utilities import Unicode2


def prioritize_value(*args):
    """Return the first non-None object in ⌜*args⌝."""
    for a in args:
        if a is not None:
            return a
    return None


class PunctiliousException(Exception):
    def __init__(self, msg, **kwargs):
        pass


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
                                                                  encoding=encoding, cap=cap,
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
            else:
                raise TypeError(f'Type ⌜{str(type(item))}⌝ is not supported in compositions.')
        return representation


class Encoding:
    """A supported output text format."""

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
    """An object that is Composable is an object that may participate in a representation composition and may be represented."""

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

    def __init__(self, s: (None, str) = None,
                 plaintext: (None, str, Plaintext) = None, unicode: (None, str, Unicode2) = None,
                 latex: (None, str) = None
                 ):
        """

        :param s: A default undetermined string. Leave it to the constructor to infer its encoding (plaintext, unicode, ...).
        :param plaintext:
        :param unicode:
        :param latex:
        """
        self._plaintext = Plaintext(prioritize_value(plaintext, s, unicode))
        self._unicode = Unicode2(prioritize_value(unicode, s))
        self._latex = latex

    def __eq__(self, other: (None, object, ComposableText)) -> bool:
        """Two instances of TextStyle are equal if any of their formatted representation are equal and not None."""
        return type(self) is type(other) and \
            self.plaintext == other.plaintext and \
            self.unicode == other.unicode and \
            self.latex == other.latex

    def __hash__(self):
        """Two styled-texts are considered distinct if either their plaintext content or their style are distinct."""
        return hash(
            (ComposableText, self._plaintext, self._unicode, self._latex))

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
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
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


def yield_composition(*content, cap: (None, bool) = None,
                      pre: (None, str, Composable) = None,
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


def prioritize_composition(*content, cap: (None, bool) = None,
                           pre: (None, str, Composable) = None,
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

    def __init__(self, name: str,
                 start_tag: ComposableText,
                 end_tag: ComposableText, unicode_map: dict = None,
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
        self._no_style = TextStyle(
            name='no-style',
            unicode_table_index=unicode_utilities.unicode_sans_serif_normal_index,
            start_tag=ComposableText(plaintext=''),
            end_tag=ComposableText(plaintext=''))
        self.double_struck = TextStyle(
            name='double-struck',
            unicode_table_index=unicode_utilities.unicode_double_struck_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathbb{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.monospace = TextStyle(
            name='fraktur-normal',
            unicode_table_index=unicode_utilities.unicode_fraktur_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathfrak{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.monospace = TextStyle(
            name='monospace',
            unicode_table_index=unicode_utilities.unicode_monospace_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathtt{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.sans_serif_bold = TextStyle(
            name='sans-serif-bold',
            unicode_table_index=unicode_utilities.unicode_sans_serif_bold_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\boldsymbol\\mathsf{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}}'))
        self.sans_serif_italic = TextStyle(
            name='sans-serif-italic',
            unicode_table_index=unicode_utilities.unicode_sans_serif_italic_index,
            start_tag=ComposableText(plaintext='', unicode='',
                                     latex='\\text{\\sffamily{\\itshape{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}}}'))
        self.sans_serif_normal = TextStyle(
            name='sans-serif-normal',
            unicode_table_index=unicode_utilities.unicode_sans_serif_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathsf{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.script_normal = TextStyle(
            name='script-normal',
            unicode_table_index=unicode_utilities.unicode_script_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathcal{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.serif_bold = TextStyle(
            name='serif-bold',
            unicode_table_index=unicode_utilities.unicode_serif_bold_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathbf{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.serif_italic = TextStyle(
            name='serif-italic',
            unicode_table_index=unicode_utilities.unicode_serif_italic_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathit{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.serif_normal = TextStyle(
            name='serif-normal',
            unicode_table_index=unicode_utilities.unicode_serif_normal_index,
            start_tag=ComposableText(plaintext='', unicode='', latex='\\mathnormal{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))
        self.subscript = TextStyle(
            name='subscript',
            unicode_map=unicode_utilities.unicode_subscript_dictionary,
            start_tag=ComposableText(plaintext='_', unicode='', latex='_{'),
            end_tag=ComposableText(plaintext='', unicode='', latex='}'))

    @property
    def no_style(self):
        """The ⌜no_style⌝ text-style is a neutral style.
        Rendering defaults to sans-serif-normal.
        It is expected to be overriden by passing the text_style parameter to the rendering method."""
        return self._no_style


text_styles = TextStyles()


class TextDict:
    """Predefined texts are exposed in the TextDict. This should facilite internatiolization at a later stage.
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
        self.open_quasi_quote = ComposableText(plaintext='"', unicode='⌜',
                                               latex='\\left\\ulcorner')
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
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
        # Implement parameter wrap
        # wrap = get_config(wrap, configuration.wrap,
        #                  False)
        return ''.join(item.rep(encoding=encoding) for item in
                       self.outer_composition)

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
    """An instance of CompositionLeafBlock is a composition string that start with a start-element, that contains a single leaf-element, and that ends with an end-element.
    """

    def __init__(self, content: (None, ComposableText) = None,
                 start_tag: (None, ComposableText) = None,
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
                 plaintext: (None, str, Plaintext) = None, unicode: (None, str, Unicode2) = None,
                 latex: (None, str) = None, cap: (None, bool) = None
                 ):
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
        return type(self) is type(other) and \
            self._content == other.content and \
            self._text_style is other.text_style

    def __hash__(self):
        """Two styled-texts are considered distinct if either their plaintext content or their
        style are distinct."""
        return hash(
            (ComposableText, self._content, self._text_style))

    def __repr__(self):
        return f'⌜{self.rep(encoding=encodings.plaintext)}⌝ [{self._text_style}]'

    def compose(self, text_style: (None, TextStyle) = None, cap: (None, bool) = None, **kwargs) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        """

        :param text_style: Override the text_style property of the StyledText instance.
        :param cap: Override the cap property of the StyledText instance.
        :param kwargs:
        :return: A composition of the StyledText instance.
        """
        if (cap is not None and not self._cap) or \
                (text_style is not None and self._text_style is not text_style):
            # Return a close of ⌜self⌝ with the desired properties.
            latex = None if self.latex is None else self.latex.capitalize()
            plaintext = None if self.plaintext is None else self.plaintext.capitalize()
            unicode = None if self.unicode is None else self.unicode.capitalize()
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
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
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
                                                index=self.text_style._unicode_table_index,
                                                mapping=self.text_style.unicode_map)

    @property
    def text_content(self) -> ComposableText:
        return self._text_content

    @property
    def text_style(self) -> TextStyle:
        return self._text_style


class ComposableBlockSequence(ComposableBlock):
    """An instance of CompositionSequence is a composite string of representation that contains a sequence of composable elements.
    """

    def __init__(self, content: (None, list[ComposableBlock, ComposableText]) = None,
                 start_tag: (None, ComposableText) = None,
                 end_tag: (None, ComposableText) = None):
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
    """A parenthetical-expression is the representation of a formula or sub-formula where the content is included between an opening and closing parenthesis.

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
        """Force conversion of item to StyledText to assure the internal consistency of the TextComposition."""
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
                 unicode: (None, str, Unicode2) = None,
                 latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.sans_serif_bold, plaintext=plaintext,
                         unicode=unicode, latex=latex)


class Header(ComposableBlockSequence):
    def __init__(self, s: (str, None) = None, plaintext: (None, str, Plaintext) = None,
                 unicode: (None, str, Unicode2) = None,
                 latex: (None, str) = None, level: (None, int) = None) -> None:
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
            start_tag = ComposableText(plaintext='\n## ', unicode='\n## ',
                                       latex='\\subsection{')
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
                 unicode: (None, str, Unicode2) = None,
                 latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.sans_serif_normal, plaintext=plaintext,
                         unicode=unicode, latex=latex)


class SansSerifItalic(StyledText):
    def __init__(self, s: (str, None) = None, plaintext: (None, str, Plaintext) = None,
                 unicode: (None, str, Unicode2) = None,
                 latex: (None, str) = None) -> None:
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
        super().__init__(text_style=text_styles.script_normal, plaintext=plaintext,
                         unicode=unicode, latex=latex)


class SerifItalic(StyledText):
    def __init__(self, s: (None, str) = None, plaintext: (None, str) = None,
                 unicode: (None, str) = None,
                 latex: (None, str) = None) -> None:
        super().__init__(s=s, text_style=text_styles.serif_italic, plaintext=plaintext,
                         unicode=unicode, latex=latex)


class SerifNormal(StyledText):
    def __init__(self, plaintext: str, unicode: (None, str) = None,
                 latex: (None, str) = None) -> None:
        super().__init__(text_style=text_styles.serif_normal, plaintext=plaintext,
                         unicode=unicode, latex=latex)


class Subscript(StyledText):
    def __init__(self, plaintext: str, unicode: (None, str) = None,
                 latex: (None, str) = None) -> None:
        super().__init__(text_style=text_styles.subscript, plaintext=plaintext,
                         unicode=unicode, latex=latex)


def wrap_text(text):
    """Wrap text for friendly rendering as text, e.g. in a console.

    :param text:
    :return:
    """
    return '\n'.join(
        textwrap.wrap(
            text=text, width=configuration.text_output_total_width,
            subsequent_indent=f'\t',
            break_on_hyphens=False,
            expand_tabs=True,
            tabsize=4))


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


def subscriptify(text: (str, ComposableText) = '', encoding: Encoding = encodings.plaintext):
    encoding = prioritize_value(encoding, configuration.encoding,
                                encodings.plaintext)
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
        self.compose_axiom_interpretation_paragraph_proof = None

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


def verify(
        assertion, msg,
        severity: VerificationSeverity = verification_severities.error, **kwargs):
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
        self.default_axiom_declaration_symbol = None
        self.default_axiom_inclusion_symbol = None
        self.default_definition_declaration_symbol = None
        self.default_definition_inclusion_symbol = None
        self.default_formula_symbol = None
        self.default_free_variable_symbol = None
        self.default_hypothesis_symbol = None
        self.default_inference_rule_declaration_symbol = None
        self.default_inference_rule_inclusion_symbol = None
        self.default_note_symbol = None
        self.default_relation_symbol = None
        self.default_statement_symbol = None
        self.default_symbolic_object_symbol = None
        self.default_theory_symbol = None
        self.echo_axiom_declaration = None
        self.echo_axiom_inclusion = None
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
    """pyvis package is used to export graphs as interactive HTML pages.
    This class stores the corresponding configuration settings."""

    def __init__(self):
        self.axiom_inclusion_args = {'shape': 'box', 'color': '#81C784'}
        self.definition_inclusion_args = {'shape': 'box', 'color': '#90CAF9'}
        self.inferred_statement_args = {'shape': 'box', 'color': '#FFF59D'}
        self.label_wrap_size = 20
        self.title_wrap_size = 32


pyvis_configuration = PyvisConfiguration()


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
    verify(o is not None, 'o is None.', o=o, c=c)
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
    """The NoNameSolutionException is the exception that is raised when a NameSet cannot be represented because no representation was found for the required Encoding."""

    def __init__(self, nameset, encoding):
        self.nameset = nameset
        self.encoding = encoding

    def __str__(self):
        return f'The nameset ⌜{repr(self.nameset)}⌝ contains no representation for the ⌜{self.encoding}⌝ text-format.'


class NameSet(Composable):
    """A set of qualified names used to identify an object.

    TODO: Enhancement: for relations in particular, add a verb NameType (e.g. implies).
    """

    def __init__(self,
                 s: (None, str) = None,
                 symbol: (None, str, StyledText) = None,
                 index: (None, int, str, ComposableText) = None,
                 dashed_name: (None, str, StyledText) = None,
                 acronym: (None, str, StyledText) = None,
                 abridged_name: (None, str, StyledText) = None,
                 name: (None, str, StyledText) = None,
                 explicit_name: (None, str, StyledText) = None,
                 paragraph_header: (None, ParagraphHeader) = None,
                 ref: (None, str) = None,
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
        if isinstance(dashed_name, str):
            dashed_name = SerifItalic(s=dashed_name)
        self._dashed_name = dashed_name if isinstance(dashed_name,
                                                      StyledText) else \
            StyledText(s=dashed_name, text_style=text_styles.serif_italic) \
                if isinstance(dashed_name, str) else None
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
        self._paragraph_header = paragraph_headers.uncategorized if paragraph_header is None else paragraph_header
        self._subtitle = subtitle

    def __eq__(self, other):
        """Two NameSets n and m are equal if their (symbol, index) pairs are equal.
        """
        return type(self) is type(other) and \
            self.symbol == other.symbol and \
            self.index == other.index

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

    def compose(self, pre: (None, str, Composable) = None,
                post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        something = yield from self.compose_symbol(pre=pre, post=post)
        return something

    def compose_accurate_name(self, cap: (None, bool) = None, pre: (None, str, Composable) = None,
                              post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Composes the most least unambiguous natural-language name in the nameset.
        """
        something = yield from yield_composition(
            prioritize_value(self._explicit_name,
                             self._name,
                             self._abridged_name,
                             self._acronym),
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

    def compose_cat_unabridged(self, cap: (None, bool) = None, pre: (None, str, Composable) = None,
                               post: (None, str, Composable) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        if self._paragraph_header is None:
            return False
        else:
            something = yield from yield_composition(self._paragraph_header.natural_name, cap=cap,
                                                     pre=pre,
                                                     post=post)
            return something

    def compose_cat_abridged(self, cap: (None, bool) = None, pre: (None, str, Composable) = None,
                             post: (None, str, Composable) = None) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        if self._paragraph_header is None:
            return False
        else:
            something = yield from yield_composition(self._paragraph_header.abridged_name, cap=cap,
                                                     pre=pre,
                                                     post=post)
            return something

    def compose_compact_name(self, cap: (None, bool) = None,
                             pre: (None, str, Composable) = None,
                             post: (None, str, Composable) = None) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        """Composes the most compact / shortest name in the nameset.
        """
        something = yield from yield_composition(
            prioritize_value(self._abridged_name,
                             self._acronym,
                             self._name,
                             self._explicit_name),
            cap=cap, pre=pre, post=post)
        return something

    def compose_conventional_name(self, cap: (None, bool) = None,
                                  pre: (None, str, Composable) = None,
                                  post: (None, str, Composable) = None) -> \
            collections.abc.Generator[
                Composable, Composable, bool]:
        """Composes the most conventional / frequently-used name in the nameset.
        """
        something = yield from yield_composition(
            prioritize_value(self._name,
                             self._abridged_name,
                             self._acronym,
                             self._explicit_name),
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
        """Composes: ⌜[dashed-name] ([symbol])⌝, or ⌜[symbol]⌝ if dashed-name is None. The rationale is to enrich the symbol with a more meaningful dashed-name if it is available."""
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
        output1 = yield from self.compose_cat_abridged(cap=cap)
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
        output1 = yield from self.compose_cat_unabridged(cap=cap)
        pre = text_dict.space if output1 else None
        output2 = yield from self.compose_ref(pre=pre)
        pre = ' (' if output1 or output2 else None
        post = ')' if output1 or output2 else None
        output3 = yield from self.compose_symbol(pre=pre, post=post)
        pre = ' - ' if output1 or output2 or output3 else None
        yield from self.compose_subtitle(pre=pre)
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
        """Returns the most accurate (longest) possible name in the nameset for the required text-format.

        Order of priority:
        1) explicit-name
        2) name
        3) acronym
        4) symbol
        """
        return rep_composition(composition=self.compose_accurate_name(), encoding=encoding,
                               cap=cap)

    def rep_acronym(self, encoding: (None, Encoding) = None, compose: bool = False) -> (
            None, str):
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
        return rep_composition(composition=self.compose_compact_name(), encoding=encoding,
                               cap=cap)

    def rep_conventional_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None):
        """Returns the most conventional (default) possible name in the nameset for the required text-format.

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

    def rep_fully_qualified_name(self, encoding: (None, Encoding) = None,
                                 cap: (None, bool) = None, compose: bool = False):
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
        rep = rep + StyledText(s='(', text_style=text_styles.sans_serif_bold).rep(
            encoding=encoding)
        rep = rep + self.rep_symbol(encoding=encoding)
        rep = rep + StyledText(s=')', text_style=text_styles.sans_serif_bold).rep(
            encoding=encoding)
        rep = '' if self._paragraph_header is None else StyledText(
            s=self.paragraph_header.natural_name,
            text_style=text_styles.sans_serif_bold).rep(
            encoding=encoding, cap=cap)
        return rep

    def rep_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> (
            None, str):
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
        return {
            'symbol':        self._symbol,
            'acronym':       self._acronym,
            'name':          self._name,
            'explicit_name': self._explicit_name
        }


class TitleOBSOLETE:
    """A title to introduce some symbolic-objcts in reports.

    TODO: QUESTION: rename Title to Name, Category to Nature, Reference to Abridged and Unabridged Name.


    Features:
    - long-names have a short (reference) and long (long-name) version.
    - long-names do not have an index.
    - long-names comprise a category that must be consistent with
        the declarative class of the symbolic-objct.
    """

    def __init__(self, nameset: (None, NameSet) = None, ref: (None, str, ComposableText) = None,
                 paragrapha_header: (None, ParagraphHeader) = None,
                 subtitle: (None, str, ComposableText) = None,
                 abr: (None, str, ComposableText) = None):
        if isinstance(ref, str):
            ref = StyledText(s=ref, text_style=text_styles.sans_serif_bold)
        self._ref = ref
        if isinstance(abr, str):
            abr = StyledText(s=abr, text_style=text_styles.sans_serif_bold)
        self._abr = abr
        self._cat = paragraph_headers.uncategorized if paragrapha_header is None else paragrapha_header
        if isinstance(subtitle, str):
            subtitle = StyledText(s=subtitle, text_style=text_styles.sans_serif_normal)
        self._nameset = nameset
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
        return self.rep(encoding=encodings.plaintext)

    def __str__(self) -> str:
        return self.rep(encoding=encodings.plaintext)

    @property
    def cat(self) -> ParagraphHeader:
        """The category of this statement."""
        return self._cat

    @property
    def subtitle(self) -> ComposableText:
        """A conditional complement to the automatically structured title."""
        return self._subtitle

    @property
    def ref(self) -> ComposableText:
        """Unabridged name."""
        return self._ref

    @property
    def abr(self) -> ComposableText:
        """Abridged name."""
        return self._abr

    @property
    def nameset(self) -> NameSet:
        return self._nameset

    @nameset.setter
    def nameset(self, nameset: NameSet):
        self._nameset = nameset

    def rep(self, encoding: (None, Encoding) = None, cap: bool = False) -> str:
        """Return the default representation for this long-name.

        :param cap: Whether the representation must be capitalized (default: False).
        :return: str
        """
        return self.rep_ref(encoding=encoding, cap=cap)

    def rep_title(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        """

        :param cap:
        :return:
        """
        return f'{StyledText(s=self.cat.natural_name, text_style=text_styles.sans_serif_bold).rep(encoding=encoding, cap=cap)}' \
               f'{"" if self.ref is None else " " + self.ref.rep(encoding=encoding)}' \
               f'{"" if self.subtitle is None else " - " + self.subtitle.rep(encoding=encoding)}'

    def rep_ref(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        return StyledText(s=self._cat.abridged_name,
                          text_style=text_styles.sans_serif_bold).rep(
            encoding=encoding, cap=cap) + \
               '' if self._ref is None else str(' ' + self._ref.rep(encoding=encoding)) + \
                                            '' if self._nameset is None else str(
            ' (' + self._nameset.rep_symbol(
                encoding=encoding) + ')')

    def rep_mention(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        return f'{"" if self.ref is None else self.ref.rep(encoding=encoding) + " "}' \
               f'{StyledText(s=self.cat.natural_name, text_style=text_styles.sans_serif_normal).rep(encoding=encoding, cap=cap)}'


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

    def rep(self, encoding: (None, Encoding) = None) -> str:
        """Return the default representation.
        """
        return self.rep_dashed_name(encoding=encoding)

    def rep_dashed_name(self, encoding: (None, Encoding) = None) -> str:
        """Return a dashed-name representation.
        """
        # TODO: Implement encodings
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
            universe_of_discourse: UniverseOfDiscourse,
            is_theory_foundation_system: bool = False, is_universe_of_discourse: bool = False,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
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
            index = universe_of_discourse.index_symbol(
                symbol=symbol) if (index is None and auto_index) else index
            nameset = NameSet(symbol=symbol, index=index, dashed_name=dashed_name,
                              acronym=acronym, abridged_name=abridged_name, name=name,
                              explicit_name=explicit_name, paragraph_header=paragraph_header,
                              ref=ref, subtitle=subtitle)
        if isinstance(nameset, str):
            symbol = StyledText(plaintext=nameset, text_style=text_styles.serif_italic)
            index = universe_of_discourse.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index, dashed_name=dashed_name,
                              acronym=acronym, abridged_name=abridged_name, name=name,
                              explicit_name=explicit_name, paragraph_header=paragraph_header,
                              ref=ref, subtitle=subtitle)
        self._nameset = nameset
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

    # def __lt__(self, other):
    #    """WARNING: Only used for support with the sorted() function, no intention to transmit any mathematical meaning."""
    #    return str(self) < str(other)

    def __repr__(self):
        return self.rep_symbol(encoding=encodings.plaintext)

    def __str__(self):
        return self.rep_symbol(encoding=encodings.plaintext)

    def compose(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose()
        return True

    def compose_cat(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_cat()
        return True

    def compose_class(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield SerifItalic(plaintext='symbolic-object')
        return True

    def compose_dashed_name(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_dashed_name()
        return output

    def compose_declaration(self, close_punctuation: Composable = None, cap: bool = None) -> \
            collections.abc.Generator[Composable, Composable, bool]:
        """TODO: _declaration must be reserved to TheoreticalObjcts. SymbolObjcts should use a distinct verb to mean "report".
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

    def compose_ref(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from self.nameset.compose_ref()
        return output

    def compose_ref_link(self, cap: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from self.nameset.compose_ref_link(cap=cap)
        return output

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
         1. o₁ and o₂ have symbol-equivalent theory_packages.¹
         2. o₁ and o₂ have equal symbols.²

        ¹. Theories are symbolic-objects. This recursive condition
           yields a complete path between the objects and the universe-of-discourse.
        ². Remember that every symbolic-object has a unique symbol in its parent theory.

        Note:
        -----
        The symbol-equivalence relation allows to compare any pair of symbolic-objcts, including:
         * Both theoretical and atheoretical objects.
         * Symbolic-objcts linked to distinct theory_packages.
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

    def prnt(self, encoding: (None, Encoding) = None, expand=False):
        repm.prnt(self.nameset.rep(encoding=encoding, expand=expand))

    @property
    def ref(self) -> (None, str):
        return self.nameset.ref

    def rep(self, encoding: (None, Encoding) = None, **kwargs) -> str:
        return rep_composition(composition=self.compose(), encoding=encoding, **kwargs)

    def rep_dashed_name(self, encoding: (None, Encoding) = None) -> str:
        return self.nameset.rep_dashed_name(encoding=encoding)

    def rep_declaration(self, encoding: (None, Encoding) = None) -> str:
        """TODO: _declaration must be reserved to TheoreticalObjcts. SymbolObjcts should use a distinct verb to mean "report".
        """
        return f'Let {self.rep_fully_qualified_name(encoding=encoding)} be a symbolic-objct in {self.universe_of_discourse.rep_symbol(encoding=encoding)}.' + '\n'

    def rep_formula(self, encoding: (None, Encoding) = None,
                    expand: (None, bool) = None) -> str:
        """TODO: _formula must be reserved to TheoreticalObjcts. SymbolObjcts should use a distinct verb to mean "report".
        """
        """If supported, return a formula representation,
        a symbolic representation otherwise.

        The objective of the repr_as_formula() method is to
        represent formulae and formula-statements not as symbols
        (e.g.: 𝜑₅) but as expanded formulae (e.g.: (4 > 3)).
        Most symbolic-objcts do not have a formula representation,
        where we fall back on symbolic representation.
        """
        return self.rep_symbol(encoding=encoding)

    def rep_fully_qualified_name(self, encoding: (None, Encoding) = None,
                                 cap: (None, bool) = None, compose: bool = False) -> str:
        """"""
        return self.nameset.rep_fully_qualified_name(encoding=encoding, cap=cap,
                                                     compose=compose)

    def rep_mention(self, encoding: (None, Encoding) = None, cap: bool = False) -> str:
        return self.nameset.rep_mention(encoding=encoding, cap=cap)

    def rep_name(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        return self.nameset.rep_name(encoding=encoding, cap=cap)

    def rep_ref(self, encoding: (None, Encoding) = None, cap: bool = False) -> str:
        return self.nameset.rep_ref(encoding=encoding, cap=cap)

    def rep_symbol(self, encoding: (None, Encoding) = None) -> str:
        return self._nameset.rep_symbol(encoding=encoding)

    def rep_title(self, encoding: (None, Encoding) = None, cap: bool = False) -> str:
        return self._nameset.rep_title(encoding=encoding, cap=cap)

    @property
    def nameset(self) -> NameSet:
        """Every symbolic-object that is being referenced must be assigned a unique symbol in its universe-of-discourse."""
        return self._nameset

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
            self, universe_of_discourse: UniverseOfDiscourse,
            is_theory_foundation_system: bool = False, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        # pseudo-class properties. these must be overwritten by
        # the parent constructor after calling __init__().
        # the rationale is that checking python types fails
        # miserably (e.g. because of context managers),
        # thus, implementing explicit functional-types will prove
        # more robust and allow for duck typing.
        super().__init__(
            universe_of_discourse=universe_of_discourse,
            is_theory_foundation_system=is_theory_foundation_system,
            symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, nameset=nameset,
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
         3. o1 and o₂ are constitutive of symbolic-equivalent theory_packages.
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

    def compose_declaration(self) -> collections.abc.Generator[Composable, None, None]:
        pass

    def export_interactive_graph(self, output_path: str, pyvis_graph: (None, pyvis.network) = None,
                                 encoding: (None, Encoding) = None,
                                 label_wrap_size: (None, int) = None,
                                 title_wrap_size: (None, int) = None) -> None:
        """Export a theoretical-object as a statement dependency graph in an HTML page with visJS, thanks to the pyvis package."""
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
                node_label = f'{self.rep_symbol(encoding=encoding)} {ref}: {self.rep_natural_language(encoding=encoding)}'
                if label_wrap_size is not None:
                    node_label = '\n'.join(textwrap.wrap(text=node_label, width=label_wrap_size))
                pyvis_graph.add_node(node_id, label=node_label, **kwargs)
            elif is_in_class(self, classes.definition_inclusion):
                self: DefinitionInclusion
                kwargs = pyvis_configuration.definition_inclusion_args
                ref = '' if self.ref is None else f'({self.rep_ref(encoding=encoding)}) '
                bold = True if ref != '' else False
                node_label = f'{self.rep_symbol(encoding=encoding)} {ref}: {self.rep_natural_language(encoding=encoding)}'
                if label_wrap_size is not None:
                    node_label = '\n'.join(textwrap.wrap(text=node_label, width=label_wrap_size))
                pyvis_graph.add_node(node_id, label=node_label, **kwargs)
            elif is_in_class(self, classes.inferred_proposition):
                self: InferredStatement
                kwargs = pyvis_configuration.inferred_statement_args
                ref = '' if self.ref is None else f'({self.rep_ref(encoding=encoding)}) '
                bold = True if ref != '' else False
                node_label = f'{self.rep_symbol(encoding=encoding)} {ref}: {self.rep_formula(encoding=encoding)}'
                if label_wrap_size is not None:
                    node_label = '\n'.join(textwrap.wrap(text=node_label, width=label_wrap_size))
                node_title = self.rep_report(encoding=encoding, proof=True)
                if title_wrap_size is not None:
                    node_title = '\n'.join(textwrap.wrap(text=node_title, width=title_wrap_size))
                pyvis_graph.add_node(node_id, label=node_label, title=node_title,
                                     labelHighlightBold=bold, **kwargs)
                for parameter in self.parameters:
                    parameter.export_interactive_graph(output_path=None, pyvis_graph=pyvis_graph,
                                                       encoding=encoding,
                                                       label_wrap_size=label_wrap_size,
                                                       title_wrap_size=title_wrap_size)
                    parameter_node_id = parameter.rep_symbol(encoding=encodings.plaintext)
                    if parameter_node_id in pyvis_graph.get_nodes():
                        pyvis_graph.add_edge(source=parameter_node_id, to=node_id)
        if is_in_class(self, classes.theory_elaboration):
            self: TheoryElaborationSequence
            for statement in self.statements:
                # Bug fix: sections should not be TheoreticalObjects but DecorativeObjects!
                if not isinstance(statement, Section):
                    statement.export_interactive_graph(output_path=None,
                                                       pyvis_graph=pyvis_graph,
                                                       encoding=encoding,
                                                       label_wrap_size=label_wrap_size,
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

    def rep_declaration(self, encoding: (None, Encoding) = None) -> str:
        """TODO: _declaration must be reserved to TheoreticalObjcts. SymbolObjcts should use a distinct verb to mean "report".
        """
        return f'Let {self.rep_fully_qualified_name(encoding=encoding)} be a symbolic-objct in {self.universe_of_discourse.rep_symbol(encoding=encoding)}.' + '\n'

    def compose_formula(self) -> collections.abc.Generator[Composable, None, None]:
        yield from self.compose_symbol()

    def rep_formula(self, encoding: (None, Encoding) = None,
                    expand: (None, bool) = None) -> str:
        """Return a formula representation, which is equivalent to a symbolic representation for non-formula objects.
        """
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
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

    def __init__(
            self, nameset=None,
            universe_of_discourse=None, status=None, scope=None, echo=None):
        echo = prioritize_value(echo, configuration.echo_free_variable_declaration,
                                configuration.echo_default,
                                False)
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
            symbol = configuration.default_free_variable_symbol
            index = universe_of_discourse.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index)
        if isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            symbol = StyledText(plaintext=nameset, text_style=text_styles.serif_bold)
            index = universe_of_discourse.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index)
        super().__init__(
            nameset=nameset,
            universe_of_discourse=universe_of_discourse, echo=False)
        # self.universe_of_discourse.cross_reference_variable(x=self)
        super()._declare_class_membership(declarative_class_list.free_variable)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='free-variable')

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

    def rep_declaration(self, encoding: (None, Encoding) = None):
        return f'Let {self.rep_name(encoding=encoding)} be a free-variable in {self.universe_of_discourse.rep_name(encoding=encoding)}' + '\n'


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
            title: (None, str, TitleOBSOLETE) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """
        """
        echo = prioritize_value(echo, configuration.echo_formula_declaration,
                                configuration.echo_default,
                                False)
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
        forbid the instantiation of "duplicate" formulae in theory_packages.
        TODO: Consider the pros and cons of forbiding "duplicate" formulae in theory_packages
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
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
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

    def rep_infix_operator(self, encoding: (None, Encoding) = None,
                           expand=(None, bool), **kwargs) -> str:
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
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
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
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
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
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
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
        return rep_composition(composition=self.compose_formula(), encoding=encoding)

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='formula')

    def compose_declaration(self) -> collections.abc.Generator[Composable, None, None]:
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

    def rep_declaration(self, encoding: (None, Encoding) = None) -> str:
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
        return rep_composition(composition=self.compose_declaration(), encoding=encoding)


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
                symbol: (None, str, StyledText) = None,
                index: (None, int) = None, auto_index: (None, bool) = None,
                dashed_name: (None, str, StyledText) = None,
                acronym: (None, str, StyledText) = None,
                abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
                explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
                subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
                echo: (None, bool) = None) -> SimpleObjct:
        """Declare a new simple-objct in this universe-of-discourse.
        """
        return SimpleObjct(symbol=symbol, index=index, auto_index=auto_index,
                           dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name,
                           name=name, explicit_name=explicit_name,
                           ref=ref, subtitle=subtitle,
                           nameset=nameset,
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
                    symbol=StyledText(unicode='⊥', latex='\\bot',
                                      plaintext='false',
                                      text_style=text_styles.serif_normal),
                    name=ComposableText(plaintext='false'),
                    explicit_name=ComposableText(plaintext='falsehood'),
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
                symbol=StyledText(unicode='⊤', latex='\\top', plaintext='true',
                                  text_style=text_styles.serif_normal),
                name=ComposableText(plaintext='true'),
                explicit_name=ComposableText(plaintext='truth'),
                index=None))
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
    axiom_declaration = ParagraphHeader('axiom_declaration', 'a', SansSerifBold('axiom'),
                                        'axiom')
    axiom_inclusion = ParagraphHeader('axiom_inclusion', 's', SansSerifBold('axiom'), 'axiom')
    corollary = ParagraphHeader('corollary', 's', 'corollary', 'cor.')
    definition_declaration = ParagraphHeader('definition_declaration', 'd',
                                             SansSerifBold('definition'),
                                             'def.')
    definition_inclusion = ParagraphHeader('definition_inclusion', 's',
                                           SansSerifBold('definition'), 'def.')
    hypothesis = ParagraphHeader('hypothesis', 's', 'hypothesis', 'hyp.')
    inference_rule_declaration = ParagraphHeader('inference_rule', 's', 'inference rule',
                                                 'inference rule')
    inference_rule_inclusion = ParagraphHeader('inference_rule_inclusion', 's',
                                               'inference rule inclusion', 'i.-r.')
    inferred_proposition = ('inferred_proposition', 's', 'inferred-proposition')
    lemma = ParagraphHeader('lemma', 's', 'lemma', 'lem.')
    proposition = ParagraphHeader('proposition', 's', 'proposition', 'prop.')
    relation_declaration = ParagraphHeader('relation_declaration', 's', 'proposition',
                                           'prop.')
    theorem = ParagraphHeader('theorem', 's', 'theorem', 'thrm.')
    theory_elaboration_sequence = ParagraphHeader('theory_elaboration_sequence', 't',
                                                  'theory elaboration sequence',
                                                  'theo.')
    informal_definition = ParagraphHeader('informal definition',
                                          StyledText(plaintext='note', unicode='🗅'),
                                          'informal definition', 'inf. def.')
    comment = ParagraphHeader('comment',
                              StyledText(plaintext='note', unicode='🗅'),
                              'comment', 'cmt.')
    note = ParagraphHeader('note',
                           StyledText(plaintext='note', unicode='🗅'),
                           'note',
                           'note')
    remark = ParagraphHeader('remark',
                             StyledText(plaintext='note', unicode='🗅'),
                             'remark', 'rmrk.')
    warning = ParagraphHeader('warning',
                              StyledText(plaintext='warning', unicode='🗅'),
                              'warning', 'warning')
    # Special categories
    uncategorized = ParagraphHeader('uncategorized', 's', 'uncategorized', 'uncat.')


paragraph_headers = ParagraphHeaders('title_categories')


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
            symbol: (None, str, StyledText) = None,
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
        self._cat = paragraph_header
        super().__init__(
            universe_of_discourse=universe_of_discourse, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=paragraph_header, ref=ref, subtitle=subtitle, nameset=nameset,
            echo=echo)
        super()._declare_class_membership(declarative_class_list.statement)
        if echo:
            self.echo()

    @property
    def category(self) -> ParagraphHeader:
        """The statement-category assigned to this statement.

        :return:
        """
        return self._cat

    @abc.abstractmethod
    def compose_report(self, proof: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        raise NotImplementedError('This is an abstract method.')

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
        between theory_packages would lead to unstable theory_packages."""
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
            natural_language: (str, StyledText), u: UniverseOfDiscourse,
            symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """

        :param natural_language: The axiom's content in natural-language.
        :param u: The universe-of-discourse.
        :param nameset:
        :param echo:
        """
        echo = prioritize_value(echo, configuration.echo_axiom_declaration,
                                configuration.echo_default,
                                False)
        if isinstance(natural_language, str):
            natural_language = natural_language.strip()
            verify(natural_language != '',
                   'Parameter natural-language is an empty string (after trimming).')
            natural_language = SansSerifItalic(natural_language)
        self._natural_language = natural_language
        cat = paragraph_headers.axiom_declaration
        if nameset is None and symbol is None:
            symbol = configuration.default_axiom_declaration_symbol
        super().__init__(
            universe_of_discourse=u, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name,
            ref=ref, subtitle=subtitle,
            nameset=nameset, paragraph_header=cat,
            echo=False)
        super()._declare_class_membership(declarative_class_list.axiom)
        u.cross_reference_axiom(self)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='axiom')

    def compose_declaration(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_axiom_declaration(o=self)
        return output

    def compose_natural_language(self) -> collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        yield text_dict.open_quasi_quote
        yield self.natural_language
        yield text_dict.close_quasi_quote
        return True

    def echo(self):
        repm.prnt(self.rep_declaration())

    @property
    def natural_language(self) -> StyledText:
        return self._natural_language

    def rep_declaration(self, encoding: (None, Encoding) = None,
                        wrap: bool = None) -> str:
        return rep_composition(composition=self.compose_declaration(), encoding=encoding,
                               wrap=wrap)

    def rep_natural_language(self, encoding: (None, Encoding) = None,
                             wrap: bool = None) -> str:
        return rep_composition(composition=self.compose_natural_language(), encoding=encoding,
                               wrap=wrap)

    def rep_report(self, encoding: (None, Encoding) = None, proof: (None, bool) = None,
                   wrap: bool = True) -> str:
        """Return a representation that expresses and justifies the statement.

        :param declaration: (bool) Default: True. Whether the report will include the definition-declaration.
        :param proof:
        :return:
        """
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
        cap = True
        output = rep_composition(composition=self.compose_report(proof=proof), encoding=encoding,
                                 cap=cap)
        return output


class AxiomInclusion(Statement):
    """An axiom-inclusion (aka axiom-postulation) is defined as a pair (𝑡,𝑎),
    where 𝑡 is a theory-elaboration-sequence and 𝑎 is a contentual axiom.
    """

    def __init__(
            self,
            a: AxiomDeclaration,
            t: TheoryElaborationSequence,
            symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """Include (postulate) an axiom in a theory-elaboration-sequence.
        """
        echo = prioritize_value(echo, configuration.echo_axiom_inclusion,
                                configuration.echo_default,
                                False)
        self._axiom = a
        t.crossreference_definition_endorsement(self)
        cat = paragraph_headers.axiom_inclusion
        if nameset is None and symbol is None:
            symbol = configuration.default_axiom_inclusion_symbol
        super().__init__(
            theory=t, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=cat, ref=ref, subtitle=subtitle, nameset=nameset, echo=False)
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

    def compose_report(self, proof: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_axiom_inclusion_report(o=self, proof=proof)
        return output

    def rep_natural_language(self, encoding: (None, Encoding) = None,
                             wrap: bool = True) -> str:
        return self._axiom.rep_natural_language(encoding=encoding, wrap=wrap)

    def rep_report(self, encoding: (None, Encoding) = None, proof: (None, bool) = None) -> str:
        """Return a representation that expresses and justifies the statement.

        Sample with unicode encoding:
        𝗔𝘅𝗶𝗼𝗺 𝟮.𝟭.𝟭 (𝑝₁): ⌜0 is a natural number.⌝

        :param declaration: (bool) Default: True. Whether the report will include the definition-declaration.
        :param proof:
        :return:
        """
        return rep_composition(composition=self.compose_report(proof=proof), encoding=encoding)


class InferenceRuleInclusion(Statement):
    """An inference-rule inclusion (aka inference-rule allowance) in the current theory-elaboration.
    """

    def __init__(
            self,
            i: InferenceRuleDeclaration,
            t: TheoryElaborationSequence,
            symbol: (None, str, StyledText) = None,
            dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None,
            proof: (None, bool) = None):
        """Include (aka allow) an inference-rule in a theory-elaboration.
        """
        self._inference_rule = i
        if nameset is None:
            symbol = configuration.default_inference_rule_inclusion_symbol if symbol is None else symbol
            index = t.universe_of_discourse.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index, dashed_name=dashed_name, acronym=acronym,
                              abridged_name=abridged_name, name=name, explicit_name=explicit_name)
        super().__init__(
            theory=t,
            paragraph_header=paragraph_headers.inference_rule_inclusion,
            nameset=nameset,
            echo=False)
        t.crossreference_inference_rule_inclusion(self)
        super()._declare_class_membership(declarative_class_list.inference_rule_inclusion)
        if echo:
            proof = prioritize_value(proof, configuration.echo_proof, True)
            repm.prnt(self.rep_report(proof=proof))

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='inference-rule')

    def compose_report(self, proof: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_inference_rule_inclusion_report(
            i=self, proof=proof)
        return output

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
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """

        :param args:
        :param echo:
        :return:
        """
        return self.inference_rule.infer_statement(*args, t=self.theory, nameset=nameset,
                                                   ref=ref, paragraph_header=paragraph_header,
                                                   subtitle=subtitle,
                                                   echo=echo)

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

    def rep_report(self, proof=True) -> str:
        """Return a representation that expresses and justifies the statement."""
        text = f'Let allow the {repm.serif_bold(self.inference_rule.title.reference)} inference-rule in {self.theory.rep_ref()}.'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4)) + f'\n'


class DefinitionDeclaration(TheoreticalObject):
    """The Definition pythonic class models the elaboration of a _contentual_ _definition_ in a _universe-of-discourse_.

    """

    def __init__(
            self,
            natural_language: str, u: UniverseOfDiscourse, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """

        :param natural_language: The definition's content in natural-language.
        :param u: The universe-of-discourse.
        :param nameset:
        :param echo:
        """
        echo = prioritize_value(echo, configuration.echo_definition_declaration,
                                configuration.echo_default,
                                False)
        if isinstance(natural_language, str):
            natural_language = natural_language.strip()
            verify(natural_language != '',
                   'Parameter natural-language is an empty string (after trimming).')
            natural_language = SansSerifItalic(natural_language)
        self._natural_language = natural_language
        cat = paragraph_headers.definition_declaration
        if nameset is None and symbol is None:
            symbol = configuration.default_definition_declaration_symbol
        super().__init__(
            universe_of_discourse=u, symbol=symbol,
            index=index, auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=cat,
            ref=ref, subtitle=subtitle,
            nameset=nameset, echo=False)
        super()._declare_class_membership(declarative_class_list.definition)
        u.cross_reference_definition(self)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='definition')

    def compose_declaration(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_definition_declaration(o=self)
        return output

    def compose_natural_language(self) -> collections.abc.Generator[Composable, Composable, bool]:
        global text_dict
        yield text_dict.open_quasi_quote
        yield self.natural_language
        yield text_dict.close_quasi_quote
        return True

    def echo(self):
        repm.prnt(self.rep_declaration())

    @property
    def natural_language(self) -> (None, str):
        """The content of the axiom in natural-language."""
        return self._natural_language

    def rep_declaration(self, encoding: (None, Encoding) = None,
                        wrap: bool = None) -> str:
        return rep_composition(composition=self.compose_declaration(), encoding=encoding,
                               wrap=wrap)

    def rep_natural_language(self, encoding: (None, Encoding) = None,
                             wrap: bool = None) -> str:
        return rep_composition(composition=self.compose_natural_language(), encoding=encoding,
                               wrap=wrap)

    def rep_report(self, encoding: (None, Encoding) = None, proof: (None, bool) = None,
                   wrap: bool = True) -> str:
        """Return a representation that expresses and justifies the statement.

        :param declaration: (bool) Default: True. Whether the report will include the definition-declaration.
        :param proof:
        :return:
        """
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
        cap = True
        output = rep_composition(composition=self.compose_report(proof=proof), encoding=encoding,
                                 cap=cap)
        return output


class DefinitionInclusion(Statement):
    """A definition-endorsement in the current theory-elaboration.
    """

    def __init__(
            self,
            d: DefinitionDeclaration,
            t: TheoryElaborationSequence,
            symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """Endorsement (aka include, endorse) an definition in a theory-elaboration.
        """
        echo = prioritize_value(echo, configuration.echo_definition_inclusion,
                                configuration.echo_default,
                                False)
        self._definition = d
        t.crossreference_definition_endorsement(self)
        cat = paragraph_headers.definition_inclusion
        if nameset is None and symbol is None:
            symbol = configuration.default_definition_inclusion_symbol
        super().__init__(
            theory=t, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            paragraph_header=cat, ref=ref, subtitle=subtitle, nameset=nameset, echo=False)
        super()._declare_class_membership(declarative_class_list.definition_inclusion)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='definition-inclusion')

    def compose_report(self, proof: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_definition_inclusion_report(
            o=self, proof=proof)
        return output

    @property
    def definition(self):
        return self._definition

    def echo(self):
        repm.prnt(self.rep_report())

    def rep_natural_language(self, encoding: (None, Encoding) = None,
                             wrap: bool = True) -> str:
        return self._definition.rep_natural_language(encoding=encoding, wrap=wrap)

    def rep_report(self, encoding: (None, Encoding) = None, proof: (None, bool) = None) -> str:
        """Return a representation that expresses and justifies the statement.
        """
        return rep_composition(composition=self.compose_report(proof=proof), encoding=encoding)


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
            symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            paragraphe_header: (None, ParagraphHeader) = None,
            nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_statement, configuration.echo_default,
                                False)
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
        paragraphe_header = prioritize_value(paragraphe_header, paragraph_headers.proposition)
        # TODO: Check that cat is a valid statement cat (prop., lem., cor., theorem)
        if nameset is None and symbol is None:
            symbol = configuration.default_statement_symbol
        super().__init__(
            theory=theory,
            symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name,
            ref=ref, subtitle=subtitle,
            nameset=nameset, paragraph_header=paragraphe_header,
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
    A theoretical-morphism-statement, or morphism for short, aka syntactic-operation is a valid-proposition produced by a valid-morphism-formula.

    """

    def __init__(
            self, source_statement, nameset=None, theory=None,
            paragraphe_header=None):
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
            nameset=nameset, paragraphe_header=paragraphe_header)

    def rep_report(self, proof: (None, bool) = None):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{repm.serif_bold(self.rep_name())}: {self.valid_proposition.rep_formula(expand=True)}'
        if proof:
            output = output + self.rep_subreport()
        return output + f'\n'

    def rep_subreport(self):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'\n\t{repm.serif_bold("Derivation by theoretical-morphism / syntactic-operation")}'
        output = output + f'\n\t{self.source_statement.valid_proposition.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.source_statement.rep_symbol())}.'
        output = output + f'\n\t{self.valid_proposition.rep_formula(expand=True):<70} │ Output of {repm.serif_bold(self.source_statement.valid_proposition.relation.rep_symbol())} morphism.'
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
    where x is present, the same formula with the substitution of x by x' can be substituted in all theory_packages.
    TODO: QUESTION: Should we create a base "Alias" object that is distinct from simple-objct???
    XXXXXXX
    """

    def __init__(
            self,
            p: Formula,
            d: DefinitionInclusion,
            t: TheoryElaborationSequence,
            nameset: (None, str, NameSet) = None,
            title: (None, str, TitleOBSOLETE) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_definition_direct_inference,
                                configuration.echo_default,
                                False)
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
            nameset=nameset, paragraphe_header=paragraph_headers.formal_definition,
            title=title, dashed_name=dashed_name, echo=False)
        assert d.statement_index < self.statement_index
        super()._declare_class_membership(declarative_class_list.direct_definition_inference)
        if echo:
            repm.prnt(self.rep_report())

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='definition-interpretation')

    def rep_report(self, proof: (None, bool) = None):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.rep_title(cap=True)}: {self.valid_proposition.rep_formula(expand=True)}'
        if proof:
            output = output + f'\n\t{repm.serif_bold("Derivation from natural language definition")}'
            output = output + f'\n\t{self.valid_proposition.rep_formula(expand=True):<70} │ Follows from {self.definition.rep_ref()}.'
        return output + f'\n'


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
                 infer_formula: (None, collections.abc.Callable) = None,
                 verify_args: (None, collections.abc.Callable) = None,
                 rep_two_columns_proof_OBSOLETE: (None, collections.abc.Callable) = None,
                 compose_paragraph_proof_method: (None, collections.abc.Callable) = None,
                 symbol: (None, str, StyledText) = None,
                 index: (None, int) = None,
                 auto_index: (None, bool) = None,
                 dashed_name: (None, str, StyledText) = None,
                 acronym: (None, str, StyledText) = None,
                 abridged_name: (None, str, StyledText) = None,
                 name: (None, str, StyledText) = None,
                 explicit_name: (None, str, StyledText) = None,
                 ref: (None, str, StyledText) = None,
                 subtitle: (None, str, StyledText) = None,
                 nameset: (None, str, NameSet) = None,
                 echo: (None, bool) = None):
        self._infer_formula = infer_formula
        self._verify_args = verify_args
        self._rep_two_columns_proof = rep_two_columns_proof_OBSOLETE
        self._compose_paragraph_proof_method = compose_paragraph_proof_method
        if nameset is None and symbol is None:
            symbol = configuration.default_inference_rule_symbol
        cat = paragraph_headers.inference_rule_declaration
        super().__init__(universe_of_discourse=universe_of_discourse,
                         is_theory_foundation_system=False,
                         symbol=symbol, index=index, auto_index=auto_index,
                         dashed_name=dashed_name,
                         acronym=acronym, abridged_name=abridged_name, name=name,
                         explicit_name=explicit_name,
                         paragraph_header=cat, ref=ref, subtitle=subtitle,
                         nameset=nameset, echo=False)
        super()._declare_class_membership(declarative_class_list.inference_rule)
        universe_of_discourse.cross_reference_inference_rule(self)
        if echo:
            self.echo()

    def compose_declaration(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_inference_rule_declaration(i=self)
        return output

    @property
    def compose_paragraph_proof_method(self):
        return self._compose_paragraph_proof_method

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
            paragraph_header: (None, ParagraphHeader) = None,
            subtitle: (None, str) = None,
            echo: (None, bool) = None, **kwargs) -> InferredStatement:
        """Apply this inference-rules on input statements and return the resulting statement."""
        return InferredStatement(*args, i=self, t=t, nameset=nameset, ref=ref,
                                 paragraph_header=paragraph_header,
                                 subtitle=subtitle,
                                 echo=echo,
                                 **kwargs)

    def rep_two_columns_proof_OBSOLETE(self, s: InferredStatement,
                                       encoding: (None, Encoding) = None) -> str:
        """Given an inferred-statement 𝑠 based on this inference-rule,
        return a two-column proof

        :param inferred_statement:
        :return:
        """
        rep = \
            StyledText(s="Proof", text_style=text_styles.sans_serif_italic).rep(
                encoding=encoding) + \
            StyledText(s=" - By the ", text_style=text_styles.sans_serif_normal).rep(
                encoding=encoding) + \
            s.inference_rule.rep_fully_qualified_name(encoding=encoding) + \
            StyledText(s=" inference rule:\n",
                       text_style=text_styles.sans_serif_normal).rep(
                encoding=encoding)
        if self._rep_two_columns_proof is None:
            # There is no specific rep_two_columns_proof method
            # linked to this inference-rule,
            # make a best-effort to write a readable proof.
            for i in range(len(s.parameters)):
                parameter = s.parameters[i]
                rep = rep + rep_two_columns_proof_item(
                    left=parameter.rep_formula(encoding=encoding, expand=True),
                    right=StyledText(s='Follows from ',
                                     text_style=text_styles.sans_serif_normal).rep(
                        encoding=encoding) + parameter.rep_ref(
                        encoding=encoding))
        else:
            rep = rep + self._rep_two_columns_proof(*s.parameters, encoding=encoding)
        rep = rep + rep_two_columns_proof_end(
            left=s.valid_proposition.rep_formula(encoding=encoding))
        return rep

    def verify_args(self, *args, t: TheoryElaborationSequence):
        """Verify the syntactical-compatibility of input statements and return True
        if they are compatible, False otherwise."""
        return self._verify_args(*args, t=t)


class AbsorptionDeclaration(InferenceRuleDeclaration):
    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 echo: (None, bool) = None):
        symbol = 'absorption'
        abridged_name = 'absorp.'
        auto_index = False
        dashed_name = 'absorption'
        explicit_name = 'absorption inference rule'
        name = 'absorption'
        # Assure backward-compatibility with the parent class,
        # which received these methods as __init__ arguments.
        infer_formula = AxiomInterpretationDeclaration.infer_formula
        verify_args = AxiomInterpretationDeclaration.verify_args
        super().__init__(infer_formula=infer_formula, verify_args=verify_args,
                         universe_of_discourse=universe_of_discourse, symbol=symbol,
                         auto_index=auto_index, dashed_name=dashed_name,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo)

    def infer_formula(self, p_implies_q: FormulaStatement = None,
                      t: TheoryElaborationSequence = None,
                      echo: (None, bool) = None) -> Formula:
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

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_absorption_paragraph_proof(
            o=o)
        return output

    def verify_args(self, p_implies_q: FormulaStatement = None,
                    t: TheoryElaborationSequence = None) -> bool:
        verify(
            t.contains_theoretical_objct(p_implies_q),
            'Statement ⌜p_implies_q⌝ must be contained in theory ⌜t⌝.',
            phi=p_implies_q, t=t, slf=self)
        p_implies_q = unpack_formula(p_implies_q)
        verify(
            p_implies_q.relation is t.u.r.implication,
            'The relation of formula ⌜p_implies_q⌝ must be an implication.',
            phi_relation=p_implies_q.relation, phi=p_implies_q, t=t, slf=self)
        return True


class AxiomInterpretationDeclaration(InferenceRuleDeclaration):
    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 echo: (None, bool) = None):
        symbol = 'axiom-interpretation'
        acronym = 'ai'
        abridged_name = 'ax.-int.'
        auto_index = False
        dashed_name = 'axiom-interpretation'
        explicit_name = 'axiom interpretation inference rule'
        name = 'axiom interpretation'
        # Assure backward-compatibility with the parent class,
        # which received these methods as __init__ arguments.
        infer_formula = AxiomInterpretationDeclaration.infer_formula
        verify_args = AxiomInterpretationDeclaration.verify_args
        super().__init__(infer_formula=infer_formula, verify_args=verify_args,
                         universe_of_discourse=universe_of_discourse, symbol=symbol,
                         auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo)

    # def compose_inferred_statement_paragraph_proof(self, o: InferredStatement,
    #                                                proof: (None, bool) = None) -> \
    #         collections.abc.Generator[
    #             Composable, Composable, bool]:
    #     output = yield from configuration.locale.compose_axiom_interpretation_paragraph_proof(
    #         o=o)
    #     return output

    def infer_formula(self, a: AxiomInclusion, p: Formula, t: TheoryElaborationSequence,
                      echo: (None, bool) = None) -> Formula:
        """Compute the formula that results from applying this inference-rule with those arguments.

        :param a: An axiom-inclusion in the theory-elaboration-sequence under consideration: 𝒜.
        :param p: A propositional formula: P.
        :param t: The current theory-elaboration-sequence.
        :return: (Formula) The inferred formula: P.
        """
        p = unpack_formula(p)
        return p

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_axiom_interpretation_paragraph_proof(
            o=o)
        return output

    def verify_args(self, a: AxiomInclusion, p: Formula, t: TheoryElaborationSequence) -> bool:
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


class BiconditionalEliminationLeftDeclaration(InferenceRuleDeclaration):
    """The well-known biconditional elimination (left) inference rule: P ⟺ Q ⊢ P ⟹ Q.

    Acronym: bel.
    """

    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 echo: (None, bool) = None):
        symbol = 'biconditional-elimination-left'
        auto_index = False
        dashed_name = 'biconditional-elimination-left'
        acronym = 'bel'
        abridged_name = 'bicond. elim. (left)'
        explicit_name = 'biconditional elimination (left) inference rule'
        name = 'biconditional elimination (left)'
        # Assure backward-compatibility with the parent class,
        # which received these methods as __init__ arguments.
        infer_formula = BiconditionalEliminationLeftDeclaration.infer_formula
        verify_args = BiconditionalEliminationLeftDeclaration.verify_args
        super().__init__(infer_formula=infer_formula, verify_args=verify_args,
                         universe_of_discourse=universe_of_discourse, symbol=symbol,
                         auto_index=auto_index, dashed_name=dashed_name,
                         acronym=acronym, abridged_name=abridged_name, name=name,
                         explicit_name=explicit_name,
                         echo=echo)

    def infer_formula(self, p_iff_q: FormulaStatement = None,
                      t: TheoryElaborationSequence = None,
                      echo: (None, bool) = None) -> Formula:
        """

        :param p_implies_q: A formula-statement of the form: (P ⟹ Q).
        :param t: The current theory-elaboration-sequence.
        :return: The (proven) formula: (P ⟹ (P ∧ Q)).
        """
        p_iff_q = unpack_formula(p_iff_q)
        p: Formula
        q: Formula
        p = unpack_formula(p_iff_q.parameters[0])
        q = unpack_formula(p_iff_q.parameters[1])
        output = t.u.f(t.u.r.implication, p, q)
        return output

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_biconditional_elimination_left_paragraph_proof(
            o=o)
        return output

    def verify_args(self, p_iff_q: FormulaStatement = None,
                    t: TheoryElaborationSequence = None) -> bool:
        verify(
            t.contains_theoretical_objct(p_iff_q),
            'Formula-statement ⌜p_iff_q⌝ must be contained in theory ⌜t⌝.',
            phi=p_iff_q, t=t, slf=self)
        p_iff_q = unpack_formula(p_iff_q)
        verify(
            p_iff_q.relation is t.u.r.biconditional,
            'The relation of formula ⌜p_iff_q⌝ must be a biconditional.',
            phi_relation=p_iff_q.relation, phi=p_iff_q, t=t, slf=self)
        return True


class BiconditionalEliminationRightDeclaration(InferenceRuleDeclaration):
    """The well-known biconditional elimination (left) inference rule: P ⟺ Q ⊢ Q ⟹ P.

    Acronym: ber.
    """

    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 echo: (None, bool) = None):
        symbol = 'biconditional-elimination-right'
        auto_index = False
        dashed_name = 'biconditional-elimination-right'
        acronym = 'ber'
        abridged_name = 'bicond. elim. (right)'
        explicit_name = 'biconditional elimination (right) inference rule'
        name = 'biconditional elimination (right)'
        # Assure backward-compatibility with the parent class,
        # which received these methods as __init__ arguments.
        infer_formula = BiconditionalEliminationRightDeclaration.infer_formula
        verify_args = BiconditionalEliminationRightDeclaration.verify_args
        super().__init__(infer_formula=infer_formula, verify_args=verify_args,
                         universe_of_discourse=universe_of_discourse, symbol=symbol,
                         auto_index=auto_index, dashed_name=dashed_name,
                         acronym=acronym, abridged_name=abridged_name, name=name,
                         explicit_name=explicit_name,
                         echo=echo)

    def infer_formula(self, p_iff_q: FormulaStatement = None,
                      t: TheoryElaborationSequence = None,
                      echo: (None, bool) = None) -> Formula:
        """(P ⟺ Q ⊢ Q ⟹ P)

        :param p_iff_q: A formula-statement of the form: (P ⟺ Q).
        :param t: The current theory-elaboration-sequence.
        :return: The (proven) formula: (Q ⟹ P).
        """
        p_iff_q = unpack_formula(p_iff_q)
        p: Formula
        q: Formula
        p = unpack_formula(p_iff_q.parameters[0])
        q = unpack_formula(p_iff_q.parameters[1])
        output = t.u.f(t.u.r.implication, q, p)
        return output

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_biconditional_elimination_right_paragraph_proof(
            o=o)
        return output

    def verify_args(self, p_iff_q: FormulaStatement = None,
                    t: TheoryElaborationSequence = None) -> bool:
        verify(
            t.contains_theoretical_objct(p_iff_q),
            'Formula-statement ⌜p_iff_q⌝ must be contained in theory ⌜t⌝.',
            phi=p_iff_q, t=t, slf=self)
        p_iff_q = unpack_formula(p_iff_q)
        verify(
            p_iff_q.relation is t.u.r.biconditional,
            'The relation of formula ⌜p_iff_q⌝ must be a biconditional.',
            phi_relation=p_iff_q.relation, phi=p_iff_q, t=t, slf=self)
        return True


class BiconditionalIntroductionDeclaration(InferenceRuleDeclaration):
    """The well-known biconditional introduction inference rule: (P ⟹ Q), (Q ⟹ P) ⊢ (P ⟺ Q)

    Acronym: bi.
    """

    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 echo: (None, bool) = None):
        symbol = 'biconditional-introduction'
        auto_index = False
        dashed_name = 'biconditional-introduction'
        acronym = 'bi'
        abridged_name = 'bicond. intro.'
        explicit_name = 'biconditional introduction inference rule'
        name = 'biconditional introduction'
        # Assure backward-compatibility with the parent class,
        # which received these methods as __init__ arguments.
        infer_formula = BiconditionalIntroductionDeclaration.infer_formula
        verify_args = BiconditionalIntroductionDeclaration.verify_args
        super().__init__(infer_formula=infer_formula, verify_args=verify_args,
                         universe_of_discourse=universe_of_discourse, symbol=symbol,
                         auto_index=auto_index, dashed_name=dashed_name,
                         acronym=acronym, abridged_name=abridged_name, name=name,
                         explicit_name=explicit_name,
                         echo=echo)

    def infer_formula(self, p_implies_q: FormulaStatement = None,
                      q_implies_p: FormulaStatement = None,
                      t: TheoryElaborationSequence = None,
                      echo: (None, bool) = None) -> Formula:
        """Infer formula (P ⟺ Q) from formulae (P ⟹ Q), and (Q ⟹ P).
        """
        p_implies_q = unpack_formula(p_implies_q)
        p = p_implies_q.parameters[0]
        q = p_implies_q.parameters[1]
        return t.u.f(t.u.r.biconditional, p, q)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_biconditional_introduction_paragraph_proof(
            o=o)
        return output

    def verify_args(self, p_implies_q: FormulaStatement = None,
                    q_implies_p: FormulaStatement = None,
                    t: TheoryElaborationSequence = None) -> bool:
        verify(
            t.contains_theoretical_objct(p_implies_q),
            'Statement ⌜p_implies_q⌝ must be contained in theory ⌜t⌝''s hierarchy.',
            p_implies_q=p_implies_q, t=t, slf=self)
        verify(
            t.contains_theoretical_objct(q_implies_p),
            'Statement ⌜q_implies_p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
            q_implies_p=q_implies_p, t=t, slf=self)
        p_implies_q: Formula
        q_implies_p: Formula
        p_implies_q = unpack_formula(p_implies_q)
        q_implies_p = unpack_formula(q_implies_p)
        verify(
            p_implies_q.relation is t.u.r.implication,
            'The relation of formula ⌜p_implies_q⌝ must be an implication.',
            p_implies_q_relation=p_implies_q.relation, p_implies_q=p_implies_q, t=t, slf=self)
        verify(
            q_implies_p.relation is t.u.r.implication,
            'The relation of formula ⌜q_implies_p⌝ must be an implication.',
            q_implies_p_relation=p_implies_q.relation, q_implies_p=q_implies_p, t=t, slf=self)

        verify(
            p_implies_q.parameters[0].is_formula_equivalent_to(q_implies_p.parameters[1]),
            'The p of the ⌜p_implies_q⌝ formula must be formula-equivalent to the p of ⌜q_implies_p⌝ formula.',
            p_implies_q=p_implies_q, q_implies_p=q_implies_p, t=t, slf=self)
        verify(
            p_implies_q.parameters[1].is_formula_equivalent_to(q_implies_p.parameters[0]),
            'The q of the ⌜p_implies_q⌝ formula must be formula-equivalent to the q of ⌜q_implies_p⌝ formula.',
            p_implies_q=p_implies_q, q_implies_p=q_implies_p, t=t, slf=self)
        return True


class ConjunctionEliminationLeftDeclaration(InferenceRuleDeclaration):
    """The well-known conjunction elimination (left) inference rule: P ⟺ Q ⊢ P ⟹ Q.

    Acronym: cel.
    """

    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 echo: (None, bool) = None):
        symbol = 'conjunction-elimination-left'
        auto_index = False
        dashed_name = 'conjunction-elimination-left'
        acronym = 'bel'
        abridged_name = 'conj. elim. (left)'
        explicit_name = 'conjunction elimination (left) inference rule'
        name = 'conjunction elimination (left)'
        # Assure backward-compatibility with the parent class,
        # which received these methods as __init__ arguments.
        infer_formula = ConjunctionEliminationLeftDeclaration.infer_formula
        verify_args = ConjunctionEliminationLeftDeclaration.verify_args
        super().__init__(infer_formula=infer_formula, verify_args=verify_args,
                         universe_of_discourse=universe_of_discourse, symbol=symbol,
                         auto_index=auto_index, dashed_name=dashed_name,
                         acronym=acronym, abridged_name=abridged_name, name=name,
                         explicit_name=explicit_name,
                         echo=echo)

    def infer_formula(self, p_land_q: FormulaStatement = None,
                      t: TheoryElaborationSequence = None,
                      echo: (None, bool) = None) -> Formula:
        """

        :param p_land_q: A formula-statement of the form: (P ⋀ Q).
        :param t: The current theory-elaboration-sequence.
        :return: The (proven) formula: P.
        """
        p = unpack_formula(p_land_q).parameters[0]
        return p

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_conjunction_elimination_left_paragraph_proof(
            o=o)
        return output

    def verify_args(self, p_land_q: FormulaStatement = None,
                    t: TheoryElaborationSequence = None) -> bool:
        verify(
            t.contains_theoretical_objct(p_land_q),
            'Statement ⌜p_land_q⌝ must be contained in theory ⌜t⌝''s hierarchy.',
            p_land_q=p_land_q, t=t, slf=self)
        verify(
            p_land_q.relation is t.u.r.conjunction,
            'The relation of formula ⌜p_land_q⌝ must be a conjunction.',
            p_land_q_relation=p_land_q.relation, p_land_q=p_land_q, t=t, slf=self)
        return True


class ConjunctionEliminationRightDeclaration(InferenceRuleDeclaration):
    """The well-known conjunction elimination (left) inference rule: P ⟺ Q ⊢ Q ⟹ P.

    Acronym: cer.

    :param p_land_q: A formula-statement of the form: (P ⋀ Q).
    :param t: The current theory-elaboration-sequence.
    :return: The (proven) formula: Q.
    """

    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 echo: (None, bool) = None):
        symbol = 'conjunction-elimination-right'
        auto_index = False
        dashed_name = 'conjunction-elimination-right'
        acronym = 'ber'
        abridged_name = 'conj. elim. (right)'
        explicit_name = 'conjunction elimination (right) inference rule'
        name = 'conjunction elimination (right)'
        # Assure backward-compatibility with the parent class,
        # which received these methods as __init__ arguments.
        infer_formula = BiconditionalEliminationRightDeclaration.infer_formula
        verify_args = BiconditionalEliminationRightDeclaration.verify_args
        super().__init__(infer_formula=infer_formula, verify_args=verify_args,
                         universe_of_discourse=universe_of_discourse, symbol=symbol,
                         auto_index=auto_index, dashed_name=dashed_name,
                         acronym=acronym, abridged_name=abridged_name, name=name,
                         explicit_name=explicit_name,
                         echo=echo)

    def infer_formula(self, p_land_q: FormulaStatement = None,
                      t: TheoryElaborationSequence = None,
                      echo: (None, bool) = None) -> Formula:
        """

        :param p_land_q: A formula-statement of the form: (P ∧ Q).
        :param t: The current theory-elaboration-sequence.
        :return: The (proven) formula: Q.
        """
        q = unpack_formula(p_land_q).parameters[1]
        return q

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_conjunction_elimination_right_paragraph_proof(
            o=o)
        return output

    def verify_args(self, p_land_q: FormulaStatement = None,
                    t: TheoryElaborationSequence = None) -> bool:
        verify(
            t.contains_theoretical_objct(p_land_q),
            'Statement ⌜p_land_q⌝ must be contained in theory ⌜t⌝''s hierarchy.',
            p_land_q=p_land_q, t=t, slf=self)
        verify(
            p_land_q.relation is t.u.r.conjunction,
            'The relation of formula ⌜p_land_q⌝ must be a conjunction.',
            p_land_q_relation=p_land_q.relation, p_land_q=p_land_q, t=t, slf=self)
        return True


class ConjunctionIntroductionDeclaration(InferenceRuleDeclaration):
    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 echo: (None, bool) = None):
        symbol = 'conjunction-introduction'
        acronym = 'ci'
        abridged_name = 'conj.-intro.'
        auto_index = False
        dashed_name = 'conjunction-introduction'
        explicit_name = 'conjunction introduction inference rule'
        name = 'conjunction introduction'
        # Assure backward-compatibility with the parent class,
        # which received these methods as __init__ arguments.
        infer_formula = AxiomInterpretationDeclaration.infer_formula
        verify_args = AxiomInterpretationDeclaration.verify_args
        super().__init__(infer_formula=infer_formula, verify_args=verify_args,
                         universe_of_discourse=universe_of_discourse, symbol=symbol,
                         auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo)

    def infer_formula(self, p: FormulaStatement,
                      q: FormulaStatement,
                      t: TheoryElaborationSequence, echo: (None, bool) = None) -> Formula:
        p = unpack_formula(p)
        q = unpack_formula(q)
        return t.u.f(t.u.r.land, p, q)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_conjunction_introduction_paragraph_proof(
            o=o)
        return output

    def verify_args(self, p: FormulaStatement,
                    q: FormulaStatement, t: TheoryElaborationSequence) -> bool:
        verify(
            t.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
            p=p, t=t, slf=self)
        verify(
            t.contains_theoretical_objct(q),
            'Statement ⌜q⌝ must be contained in theory ⌜t⌝''s hierarchy.',
            q=q, t=t, slf=self)
        return True


class InconsistencyIntroductionDeclaration(InferenceRuleDeclaration):
    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 echo: (None, bool) = None):
        symbol = 'inconsistency-introduction'
        acronym = 'ii'
        abridged_name = 'inc.-intro.'
        auto_index = False
        dashed_name = 'inconsistency-introduction'
        explicit_name = 'inconsistency introduction inference rule'
        name = 'inconsistency introduction'
        # Assure backward-compatibility with the parent class,
        # which received these methods as __init__ arguments.
        infer_formula = AxiomInterpretationDeclaration.infer_formula
        verify_args = AxiomInterpretationDeclaration.verify_args
        super().__init__(infer_formula=infer_formula, verify_args=verify_args,
                         universe_of_discourse=universe_of_discourse, symbol=symbol,
                         auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo)

    def infer_formula(self, p: FormulaStatement = None,
                      not_p: FormulaStatement = None,
                      inconsistent_theory: TheoryElaborationSequence = None,
                      t: TheoryElaborationSequence = None,
                      echo: (None, bool) = None) -> Formula:
        p = unpack_formula(p)
        not_p = unpack_formula(not_p)
        return t.u.f(t.u.r.inconsistent, inconsistent_theory)

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_inconsistency_introduction_paragraph_proof(
            o=o)
        return output

    def verify_args(self, p: FormulaStatement = None,
                    not_p: FormulaStatement = None,
                    inconsistent_theory: TheoryElaborationSequence = None,
                    t: TheoryElaborationSequence = None) -> bool:
        verify(
            inconsistent_theory.contains_theoretical_objct(p),
            'Statement ⌜p⌝ must be contained in theory ⌜inconsistent_theory⌝''s hierarchy.',
            p=p, inconsistent_theory=inconsistent_theory, slf=self)
        verify(
            inconsistent_theory.contains_theoretical_objct(not_p),
            'Statement ⌜not_p⌝ must be contained in theory ⌜inconsistent_theory⌝''s hierarchy.',
            not_p=not_p, inconsistent_theory=inconsistent_theory, slf=self)
        verify(
            not_p.relation is not_p.theory.universe_of_discourse.relations.negation,
            'The relation of statement ⌜not_p⌝ must be ⌜negation⌝.',
            not_p=not_p, inconsistent_theory=inconsistent_theory, slf=self)
        not_p_formula = not_p.valid_proposition
        p_in_not_p = not_p_formula.parameters[0]
        verify(
            p_in_not_p.is_formula_equivalent_to(p),
            'The sub-formula (parameter) ⌜p⌝ in ⌜not_p⌝ must be formula-equivalent to ⌜p⌝.',
            not_p=not_p, p_in_not_p=p_in_not_p, p=p, slf=self)
        return True


class ModusPonensDeclaration(InferenceRuleDeclaration):
    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 echo: (None, bool) = None):
        symbol = 'modus-ponens'
        acronym = 'mp'
        abridged_name = 'mod.-pon.'
        auto_index = False
        dashed_name = 'modus-ponens'
        explicit_name = 'modus ponens inference rule'
        name = 'modus ponens'
        # Assure backward-compatibility with the parent class,
        # which received these methods as __init__ arguments.
        infer_formula = AxiomInterpretationDeclaration.infer_formula
        verify_args = AxiomInterpretationDeclaration.verify_args
        super().__init__(infer_formula=infer_formula, verify_args=verify_args,
                         universe_of_discourse=universe_of_discourse, symbol=symbol,
                         auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo)

    def infer_formula(self, p_implies_q: FormulaStatement,
                      p: FormulaStatement,
                      t: TheoryElaborationSequence, echo: (None, bool) = None) -> Formula:
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

    def compose_paragraph_proof(self, o: InferredStatement) -> collections.abc.Generator[
        Composable, Composable, bool]:
        output = yield from configuration.locale.compose_modus_ponens_paragraph_proof(
            o=o)
        return output

    def verify_args(self, p_implies_q: FormulaStatement,
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


class AtheoreticalStatement(SymbolicObject):
    """
    Definition
    ----------
    An atheoretical-statement is a statement that is contained in a theory report
    for commentary / explanatory purposes, but that is not mathematically constitutive
    of the theory. Atheoretical-statements may be added and/or removed from a
    theory without any impact to the theory sequence of proofs.

    """

    def __init__(
            self, theory: TheoryElaborationSequence, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        self.theory = theory
        super().__init__(universe_of_discourse=theory.universe_of_discourse, symbol=symbol,
                         index=index, auto_index=auto_index, dashed_name=dashed_name,
                         acronym=acronym, abridged_name=abridged_name, name=name,
                         explicit_name=explicit_name, paragraph_header=paragraph_header, ref=ref,
                         subtitle=subtitle,
                         nameset=nameset, echo=echo)
        super()._declare_class_membership(classes.atheoretical_statement)


class NoteInclusion(AtheoreticalStatement):
    """The Note pythonic-class models a note, comment, or remark in a theory.

    """

    def __init__(
            self, t: TheoryElaborationSequence, content: str,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):

        echo = prioritize_value(echo, configuration.echo_note, configuration.echo_default,
                                False)
        verify(is_in_class(t, classes.t),
               'theory is not a member of declarative-class theory.', t=t,
               slf=self)
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
        super().__init__(theory=t,
                         symbol=symbol, index=index, auto_index=auto_index,
                         dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name,
                         name=name, explicit_name=explicit_name, paragraph_header=paragraph_header,
                         ref=ref,
                         subtitle=subtitle,
                         nameset=nameset, echo=False)
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

    def compose_report(self, proof: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        yield from self.nameset.compose_title()
        yield text_dict.colon
        yield text_dict.space
        yield from self.compose_content()
        return True

    def echo(self):
        repm.prnt(self.rep_report())

    @property
    def natural_language(self) -> str:
        """Return the content of the note in natural-language."""
        return self._natural_language

    def rep_report(self, encoding: (None, Encoding) = None, proof: (None, bool) = None,
                   wrap: bool = True) -> str:
        """Return a representation that expresses and justifies the statement.

        :param declaration: (bool) Default: True. Whether the report will include the definition-declaration.
        :param proof:
        :return:
        """
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
        cap = True
        output = rep_composition(composition=self.compose_report(proof=proof), encoding=encoding,
                                 cap=cap)
        return output


section_category = ParagraphHeader(
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
        echo = prioritize_value(echo, configuration.echo_note, configuration.echo_default,
                                False)
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
        title = TitleOBSOLETE(ref=self._section_reference, paragrapha_header=section_category,
                              subtitle=section_title)
        super().__init__(
            nameset=symbol,
            theory=t,
            echo=False)
        super()._declare_class_membership(declarative_class_list.note)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, Composable, bool]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='section')

    def compose_report(self, proof: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        yield "#" * self.section_level
        yield text_dict.space
        yield from SansSerifBold(self.section_reference).compose()
        yield text_dict.space
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

    def rep_ref(self, cap=False) -> str:
        prefix = 'section' if self.section_level == 1 else 'sub-' * (
                self.section_level - 1) + 'section'
        text = f'{prefix}{repm.serif_bold(self.section_reference)}'
        return text

    def rep_report(self, encoding: (None, Encoding) = None) -> str:
        return rep_composition(composition=self.compose_report(), encoding=encoding)

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
            ref: (None, str) = None,
            subtitle: (None, str) = None,
            extended_theory: (None, TheoryElaborationSequence) = None,
            extended_theory_limit: (None, Statement) = None,
            stabilized: bool = False,
            echo: bool = None
    ):
        echo = prioritize_value(echo, configuration.echo_theory_elaboration_sequence_declaration,
                                configuration.echo_default,
                                False)
        self._max_subsection_number = 0
        self._consistency = consistency_values.undetermined
        self._stabilized = False
        self.axiom_inclusions = tuple()
        self.definition_inclusions = tuple()
        self._inference_rule_inclusions = InferenceRuleInclusionDict(t=self)
        self.statements = tuple()
        self._extended_theory = extended_theory
        self._extended_theory_limit = extended_theory_limit
        self._interpretation_disclaimer = False
        if nameset is None:
            symbol = configuration.default_theory_symbol
            index = u.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index)
        elif isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            symbol = StyledText(plaintext=nameset,
                                text_style=text_styles.script_normal)
            index = u.index_symbol(symbol=symbol)
            nameset = NameSet(s=symbol, index=index)
        nameset.paragraph_header = paragraph_headers.theory_elaboration_sequence
        nameset.ref = ref
        nameset.subtitle = subtitle
        super().__init__(
            nameset=nameset,
            paragraph_header=nameset.paragraph_header,
            is_theory_foundation_system=True if extended_theory is None else False,
            universe_of_discourse=u,
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
            self.echo()

    def assure_interpretation_disclaimer(self, echo: (None, bool) = None):
        """After the first usage of a contentual interpretation inference-rule,
        warns the user that no semantic verification is performed."""
        echo = prioritize_value(echo, configuration.echo_default, False)
        if not self._interpretation_disclaimer:
            self.take_note(
                'By design, punctilious assures the syntactical correctness of theory_packages, but does not perform any '
                'semantic verification. Therefore, the usage of inference-rules that interpret content (i.e. '
                'axiom-interpretation and definition-interpretation) is critically dependent on the correctness of '
                'the content translation performed by the theory author, from axiom or definition natural language, '
                'to formulae.',
                paragraph_header=paragraph_headers.warning,
                echo=echo)
            self._interpretation_disclaimer = True

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='theory-elaboration-sequence')

    def compose_declaration(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_theory_declaration(t=self)
        return output

    def compose_report(self, proof: (None, bool) = None) -> collections.abc.Generator[
        Composable, Composable, bool]:
        """Return a representation that expresses and justifies the theory."""
        output = yield from configuration.locale.compose_theory_report(t=self, proof=proof)
        return output

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
        repm.prnt(self.rep_declaration(cap=True))

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
            self, a: AxiomDeclaration,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None) -> AxiomInclusion:
        """Include an axiom in this theory-elaboration-sequence."""
        return AxiomInclusion(
            a=a, t=self, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            ref=ref, subtitle=subtitle, nameset=nameset, echo=echo)

    def include_definition(
            self, d: DefinitionDeclaration,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None) -> DefinitionInclusion:
        """Include a definition in this theory-elaboration-sequence."""
        return DefinitionInclusion(
            d=d, t=self, symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            ref=ref, subtitle=subtitle, nameset=nameset, echo=echo)

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
        The theory-chain informs of the parent theory_packages whose statements are considered valid in the current theory.
        Distinctively, theory_packages may be referenced by meta-theorizing, or in hypothesis, or possibly other use cases.
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
            hypothetical_proposition: Formula,
            symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None) -> Hypothesis:
        """Pose a new hypothesis in the current theory."""
        return Hypothesis(
            t=self, hypothetical_formula=hypothetical_proposition,
            symbol=symbol, index=index, auto_index=auto_index, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            ref=ref, subtitle=subtitle,
            nameset=nameset, echo=echo)

    def rep_report(self, encoding: (None, Encoding) = None,
                   proof: (None, bool) = None):
        output = rep_composition(composition=self.compose_report(proof=proof), encoding=encoding)
        return output

    def prnt(self, proof: (None, bool) = None):
        repm.prnt(self.rep_report(proof=proof))

    def prove_inconsistent(self, ii):
        verify(isinstance(ii, InconsistencyIntroductionStatement),
               'The ii statement is not of type InconsistencyIntroductionStatement.', ii=ii,
               theory=self)
        verify(ii in self.statements,
               'The ii statement is not a statement of this theory.', ii=ii, theory=self)
        self._consistency = consistency_values.proved_inconsistent

    def export_report_to_file(self, file_path, proof: (None, bool) = None,
                              encoding: (None, Encoding) = None):
        """Export this theory to a Unicode textfile."""
        text_file = open(file_path, 'w', encoding='utf-8')
        n = text_file.write(self.rep_report(encoding=encoding, proof=proof))
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

    def rep_declaration(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        return rep_composition(composition=self.compose_declaration(), encoding=encoding, cap=cap)

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

    def take_note(self, content: str,
                  symbol: (None, str, StyledText) = None,
                  index: (None, int) = None, auto_index: (None, bool) = None,
                  dashed_name: (None, str, StyledText) = None,
                  acronym: (None, str, StyledText) = None,
                  abridged_name: (None, str, StyledText) = None,
                  name: (None, str, StyledText) = None,
                  explicit_name: (None, str, StyledText) = None,
                  paragraph_header: (None, ParagraphHeader) = None,
                  ref: (None, str, StyledText) = None,
                  subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
                  echo: (None, bool) = None) -> NoteInclusion:
        """Take a note, make a comment, or remark in this theory.
        """
        return self.universe_of_discourse.take_note(t=self, content=content, symbol=symbol,
                                                    index=index, auto_index=auto_index,
                                                    dashed_name=dashed_name, acronym=acronym,
                                                    abridged_name=abridged_name,
                                                    name=name, explicit_name=explicit_name,
                                                    paragraph_header=paragraph_header,
                                                    ref=ref, subtitle=subtitle,
                                                    nameset=nameset, echo=echo)

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
            symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        category = paragraph_headers.hypothesis
        # TODO: Check that all components of the hypothetical-proposition
        #  are elements of the source theory-branch.
        verify(
            hypothetical_formula.is_proposition,
            'The hypothetical-formula is not a proposition.',
            hypothetical_formula=hypothetical_formula,
            slf=self)
        if nameset is None:
            symbol = prioritize_value(symbol, configuration.default_hypothesis_symbol)
            index = t.u.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index)
        if isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            symbol = StyledText(plaintext=nameset, text_style=text_styles.serif_italic)
            index = t.u.index_symbol(symbol=symbol)
            nameset = NameSet(symbol=symbol, index=index)
        super().__init__(
            theory=t, paragraph_header=category, nameset=nameset,
            subtitle=subtitle, dashed_name=dashed_name, echo=False)
        super()._declare_class_membership(declarative_class_list.hypothesis)
        self._hypothetical_formula = hypothetical_formula
        # When a hypothesis is posed in a theory 𝒯₁,
        # ...the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        self._hypothetical_axiom_declaration = self.universe_of_discourse.declare_axiom(
            f'By this hypothesis, assume {hypothetical_formula.rep_formula()} is true.')
        # ...a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        self._hypothetical_theory = t.universe_of_discourse.t(
            extended_theory=t,
            extended_theory_limit=self
        )
        # ...the axiom is included in 𝒯₂,
        self._hypothetical_axiom_inclusion = self.hypothetical_theory.include_axiom(
            self.hypothetical_axiom_declaration)
        # ...and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂.
        self._hypothetical_proposition = \
            self.hypothetical_theory.i.axiom_interpretation.infer_statement(
                self.hypothetical_axiom_inclusion,
                hypothetical_formula)

    def compose_class(self) -> collections.abc.Generator[Composable, Composable, True]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='hypothesis')
        return True

    @property
    def hypothetical_axiom_declaration(self) -> AxiomDeclaration:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothetical_axiom_declaration

    @property
    def hypothetical_axiom_inclusion(self) -> AxiomInclusion:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothetical_axiom_inclusion

    @property
    def hypothetical_formula(self) -> Formula:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothetical_formula

    @property
    def hypothetical_proposition(self) -> InferredStatement:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothetical_proposition

    @property
    def hypothetical_theory(self) -> TheoryElaborationSequence:
        """When a hypothesis is posed in a theory 𝒯₁,
        the hypothesis is declared (aka postulated) as an axiom in the universe-of-discourse,
        a hypothetical-theory 𝒯₂ is created to store the hypothesis elaboration,
        the axiom is included in 𝒯₂,
        and the hypothetical-proposition is posed as an interpretation of that axiom in 𝒯₂."""
        return self._hypothetical_theory


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
            self, universe_of_discourse: UniverseOfDiscourse, arity: int,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, formula_rep=None,
            signal_proposition=None, signal_theoretical_morphism=None, implementation=None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
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
        assert arity is not None and isinstance(arity, int) and arity > 0
        self.arity = arity
        if nameset is None:
            symbol = configuration.default_relation_symbol if symbol is None else symbol
            index = universe_of_discourse.index_symbol(symbol=symbol) if auto_index else index
            nameset = NameSet(symbol=symbol, index=index, dashed_name=dashed_name, acronym=acronym,
                              abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                              paragraph_header=cat, ref=ref, subtitle=subtitle)
        super().__init__(
            universe_of_discourse=universe_of_discourse, nameset=nameset, echo=False)
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

    def compose_declaration(self) -> collections.abc.Generator[
        Composable, Composable, bool]:
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
        repm.prnt(self.rep_declaration())

    # def rep_declaration(self):
    #    output = f'Let {self.rep_fully_qualified_name()} be a {rep_arity_as_text(self.arity)} relation in {self.u.rep_symbol()}'
    #    output = output + f' (default notation: {self.formula_rep}).'
    #    return output + '\n'
    def rep_declaration(self, encoding: (None, Encoding) = None, wrap: (None, bool) = None):
        return rep_composition(composition=self.compose_declaration(), encoding=encoding,
                               wrap=wrap)


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
            symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_simple_objct_declaration,
                                configuration.echo_default,
                                False)
        super().__init__(
            universe_of_discourse=universe_of_discourse,
            symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name,
            name=name, explicit_name=explicit_name,
            ref=ref, subtitle=subtitle,
            nameset=nameset,
            echo=False)
        self.universe_of_discourse.cross_reference_simple_objct(o=self)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='simple-object')

    def compose_declaration(self) -> collections.abc.Generator[Composable, Composable, bool]:
        output = yield from configuration.locale.compose_simple_objct_declaration(o=self)
        return output

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

    def rep_declaration(self, encoding: (None, Encoding) = None, wrap: (None, bool) = None):
        return rep_composition(composition=self.compose_declaration(), encoding=encoding,
                               wrap=wrap)


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
            paragraphe_header=None, theory=None, reference=None, title=None):
        paragraphe_header = paragraph_headers.proposition if paragraphe_header is None else paragraphe_header
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
            paragraphe_header=paragraphe_header,
            nameset=nameset)

    def rep_report(self, proof: (None, bool) = None):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.rep_title(cap=True)}: {self.valid_proposition.rep_formula()}'
        if proof:
            output = output + f'\n\t{repm.serif_bold("Substitution of equal terms")}'
            output = output + f'\n\t{self.original_expression.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.original_expression.rep_ref())}.'
            output = output + f'\n\t{self.equality_statement.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.equality_statement.rep_ref())}.'
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
        self._conjunction = None
        self._disjunction = None
        self._equality = None
        self._inconsistent = None
        self._inequality = None
        self._implication = None
        self._negation = None

    def declare(
            self, arity: int, symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, formula_rep=None,
            signal_proposition=None, signal_theoretical_morphism=None, implementation=None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """Declare a new relation in this universe-of-discourse.
        """
        return Relation(
            arity=arity,
            formula_rep=formula_rep,
            signal_proposition=signal_proposition,
            signal_theoretical_morphism=signal_theoretical_morphism,
            implementation=implementation,
            universe_of_discourse=self.u,
            symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle,
            nameset=nameset,
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
                arity=2,
                formula_rep=Formula.infix,
                signal_proposition=True,
                symbol=SerifItalic(plaintext='<==>', unicode='⟺', latex='\\iff'),
                auto_index=False,
                dashed_name='biconditional',
                name='biconditional')
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
                arity=2, formula_rep=Formula.infix, signal_proposition=True,
                symbol=SerifItalic(plaintext='and', unicode='∧', latex='\\land'),
                auto_index=False,
                name='and',
                explicit_name='conjunction')
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
                arity=2, formula_rep=Formula.infix,
                signal_proposition=True,
                auto_index=False,
                symbol=SerifItalic(unicode='∨', latex='\\lor', plaintext='or'),
                name='or',
                explicit_name='disjunction')
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
                arity=2,
                formula_rep=Formula.infix,
                signal_proposition=True,
                symbol='=', auto_index=False,
                dashed_name='equality')
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
                arity=2, formula_rep=Formula.infix,
                signal_proposition=True,
                symbol=SerifItalic(plaintext='==>', unicode='⟹', latex=r'\implies'),
                auto_index=False,
                name='implication',
                explicit_name='logical implication')
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
                arity=1, formula_rep=Formula.prefix, signal_proposition=True, symbol='Inc',
                auto_index=False, acronym='inc.', name='inconsistent')
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
                arity=2,
                formula_rep=Formula.infix,
                signal_proposition=True,
                symbol=SerifItalic(plaintext='neq', unicode='≠', latex='\\neq'),
                auto_index=False,
                acronym='neq',
                name='not equal')
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
                arity=1,
                formula_rep=Formula.prefix,
                signal_proposition=True,
                symbol=SerifItalic(plaintext='not', unicode='¬', latex='\\neg'),
                auto_index=False,
                abridged_name='not',
                name='negation')
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
    def absorb(self) -> AbsorptionDeclaration:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Unabridged property: u.i.absorption

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.absorption

    @property
    def absorption(self) -> AbsorptionDeclaration:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Abridged property: u.i.absorb

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        if self._absorption is None:
            self._absorption = AbsorptionDeclaration(
                universe_of_discourse=self.u)
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
        if self._axiom_interpretation is None:
            self._axiom_interpretation = AxiomInterpretationDeclaration(
                universe_of_discourse=self.u)
        return self._axiom_interpretation

    @property
    def bel(self) -> BiconditionalEliminationLeftDeclaration:
        """The well-known biconditional-elimination (left) inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Abridged property: u.i.bel

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_elimination_left

    @property
    def ber(self) -> BiconditionalEliminationRightDeclaration:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Abridged property: u.i.ber()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_elimination_right

    @property
    def bi(self) -> BiconditionalIntroductionDeclaration:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Unabridged property: u.i.biconditional_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_introduction

    @property
    def biconditional_elimination_left(self) -> BiconditionalEliminationLeftDeclaration:
        """The well-known biconditional-elimination (left) inference-rule: ((P ⟺ Q) ⊢ (P ⟹ Q)).

        The ⌜left⌝ suffix is non-standard and used to mean that among the two possible results of biconditional-elimination, i.e.: (P ⟹ Q) and (Q ⟹ P), we pick the first one, i.e.: (P ⟹ Q).

        Abridged property: u.i.bel

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        if self._biconditional_elimination_left is None:
            self._biconditional_elimination_left = BiconditionalEliminationLeftDeclaration(
                universe_of_discourse=self.u)
        return self._biconditional_elimination_left

    @property
    def biconditional_elimination_right(self) -> BiconditionalEliminationRightDeclaration:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        The ⌜right⌝ suffix is non-standard and used to mean that among the two possible results of biconditional-elimination, i.e.: (P ⟹ Q) and (Q ⟹ P), we pick the second one, i.e.: (Q ⟹ P).

        Abridged property: u.i.ber()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._biconditional_elimination_right is None:
            self._biconditional_elimination_right = BiconditionalEliminationRightDeclaration(
                universe_of_discourse=self.u)
        return self._biconditional_elimination_right

    @property
    def biconditional_introduction(self) -> BiconditionalIntroductionDeclaration:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Abridged property: u.i.bi

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        if self._biconditional_introduction is None:
            self._biconditional_introduction = BiconditionalIntroductionDeclaration(
                universe_of_discourse=self.u)
        return self._biconditional_introduction

    @property
    def cel(self) -> InferenceRuleDeclaration:
        """The well-known conjunction-elimination (left) inference-rule: ((P ∧ Q) ⊢ P).

        The ⌜left⌝ suffix is non-standard and used to mean that among the two possible results of conjunction-elimination, i.e.: P and Q, we pick the first one, i.e.: P.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_elimination_left

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.conjunction_elimination_left

    @property
    def cer(self) -> InferenceRuleDeclaration:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        The ⌜right⌝ suffix is non-standard and used to mean that among the two possible results of conjunction-elimination, i.e.: P and Q, we pick the second one, i.e.: Q.

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

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='inference-rule')

    @property
    def conjunction_elimination_left(self) -> ConjunctionEliminationLeftDeclaration:
        """The well-known conjunction-elimination (left) inference-rule: ((P ∧ Q) ⊢ P).

        The ⌜left⌝ suffix is non-standard and used to mean that among the two possible results of conjunction-elimination, i.e.: P and Q, we pick the first one, i.e.: P.

        Abridged property: u.i.cel()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        # TODO: inference-rule: conjunction_elimination_left: Migrate to specialized classes

        if self._conjunction_elimination_left is None:
            self._conjunction_elimination_left = ConjunctionEliminationLeftDeclaration(
                universe_of_discourse=self.u)
        return self._conjunction_elimination_left

    @property
    def conjunction_elimination_right(self) -> InferenceRuleDeclaration:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        The ⌜right⌝ suffix is non-standard and used to mean that among the two possible results of conjunction-elimination, i.e.: P and Q, we pick the second one, i.e.: Q.

        Abridged property: u.i.cer()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._conjunction_elimination_right is None:
            self._conjunction_elimination_right = ConjunctionEliminationRightDeclaration(
                universe_of_discourse=self.u)
        return self._conjunction_elimination_right

    @property
    def conjunction_introduction(self) -> ConjunctionIntroductionDeclaration:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ (P ∧ Q).

        Abridged property: u.i.ci

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._conjunction_introduction is None:
            self._conjunction_introduction = ConjunctionIntroductionDeclaration(
                universe_of_discourse=self.u)
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

        # TODO: inference-rule: definition_interpretation: Migrate to specialized classes

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

        def compose_paragraph_proof(o: InferredStatement):
            output = yield from configuration.locale.compose_definition_interpretation_paragraph_proof(
                o=o)
            return output

        if self._definition_interpretation is None:
            self._definition_interpretation = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                compose_paragraph_proof_method=compose_paragraph_proof,
                symbol='definition-interpretation', auto_index=False,
                dashed_name='definition-interpretation',
                name='definition interpretation',
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

        # TODO: inference-rule: disjunction_introduction: Migrate to specialized classes

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
                symbol='disjunction-introduction',
                index=None, auto_index=False,
                name='disjunction introduction',
                dashed_name='disjunction-introduction',
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

        # TODO: inference-rule: double_negation_elimination: Migrate to specialized classes

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
                symbol='double-negation-elimination',
                index=None, auto_index=False,
                dashed_name='double-negation-elimination',
                name='double negation elimination',
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

        # TODO: inference-rule: double_negation_introduction: Migrate to specialized classes

        def infer_formula(p: FormulaStatement, t: TheoryElaborationSequence) -> Formula:
            """

            :param p: A propositional formula, or formula-statement.
            :param t:
            :return:
            """
            p = unpack_formula(p)
            return t.u.f(t.u.r.lnot, t.u.f(t.u.r.lnot, p))

        def verify_args(p: FormulaStatement, t: TheoryElaborationSequence) -> bool:
            # verify(
            #    len(args) == 1,
            #    'Exactly 1 item is expected in ⌜*args⌝ .',
            #    args=args, t=t, slf=self)
            # p = args[0]
            verify(is_in_class(p, classes.formula_statement),
                   msg='⌜p⌝ is not an element of the formula-statement class.', p=p, t=t, slf=self)
            verify(is_in_class(t, classes.theory_elaboration),
                   msg='⌜t⌝ is not an element of the theory-elaboration-sequence class.', t=t, p=p,
                   slf=self)
            verify(
                t.contains_theoretical_objct(p),
                'formula-statement ⌜p⌝ is not contained in theory ⌜t⌝.', p=p, t=t, slf=self)
            return True

        if self._double_negation_introduction is None:
            self._double_negation_introduction = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                symbol='double-negation-introduction',
                index=None, auto_index=False,
                name='double negation introduction',
                dashed_name='double-negation-introduction',
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

        # TODO: inference-rule: equality_commutativity: Migrate to specialized classes

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

        def compose_paragraph_proof(o: InferredStatement):
            output = yield from configuration.locale.compose_equality_commutativity_paragraph_proof(
                o=o)
            return output

        if self._equality_commutativity is None:
            self._equality_commutativity = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                compose_paragraph_proof_method=compose_paragraph_proof,
                symbol='equality-commutativity', auto_index=False,
                name='equality commutativity',
                dashed_name='equality-commutativity',
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._equality_commutativity

    @property
    def inconsistency_introduction(self) -> InconsistencyIntroductionDeclaration:
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

        if self._inconsistency_introduction is None:
            self._inconsistency_introduction = InconsistencyIntroductionDeclaration(
                universe_of_discourse=self.u)
        return self._inconsistency_introduction

    @property
    def ii(self) -> InconsistencyIntroductionDeclaration:
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
    def modus_ponens(self) -> ModusPonensDeclaration:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P' ⊢ Q'.

        Abridged property: u.i.mp

        The implication (P ⟹ Q) may contain free-variables. If such is the
        case, the resulting Q' is computed by extracting variable-values
        from P' and applying variable-substitution.

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._modus_ponens is None:
            self._modus_ponens = ModusPonensDeclaration(
                universe_of_discourse=self.u)
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
         - P is a statement,
         - Q=R is an equality statement,
         - P' is a new statement identical to P except that all occurrences of Q in P
           are substituted with R.

        Abridged property: u.i.eqs

        The algorithm for formula substitution is:
        - canonical-order (top-down, depth-first, left-to-right)
        - replace all occurrences until end of formula is reached

        TODO: QUESTION: equal_terms_substitution: Should we forbid the presence of Q in R or R in Q?

        TODO: QUESTION: equal_terms_substitution: This version of the inference-rule replaces all occurences of Q in R. We may wish to enrich this inference-rule and make it possible to only replace a subset of occurences of Q in R. Let's keep this aside for future improvements.

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        # TODO: inference-rule: equal_terms_substitution: Migrate to specialized classes

        def infer_formula(p: FormulaStatement, q_equal_r: FormulaStatement,
                          t: TheoryElaborationSequence) -> Formula:
            """

            :param p: ⌜ P ⌝  a formula-statement.
            :param q_equal_r: a formula-statement of the form: (Q = R).
            :return: (FormulaStatement) A formula-statement P' where occurrences of Q are replaced with R.
            """
            p: Formula
            q_equal_r: Formula
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

        # def compose_paragraph_proof(o: InferredStatement):
        #     output = yield from configuration.locale.compose_equal_terms_substitution_paragraph_proof(
        #         o=o)
        #     return output

        if self._equal_terms_substitution is None:
            self._equal_terms_substitution = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                # compose_paragraph_proof_method=compose_paragraph_proof,
                symbol='equal-terms-substitution', auto_index=False,
                name='equal terms substitution',
                dashed_name='equal-terms-substitution',
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
        To avoid inconsistent theory_packages, one must be cautious
        with variable manipulations. In effect, the proposition:
            ((2n + 4) = 2(n + 2))
        may lead to inconsistencies following variable-substitution
        because the variable n is not typed. On the contrary:
            (n ∈ ℕ) ⟹ ((2n + 4) = 2(n + 2))
        where n is constrained leads to consistent results.

        If the inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """

        # TODO: inference-rule: variable_substitution: Migrate to specialized classes

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

        def compose_paragraph_proof(o: InferredStatement):
            output = yield from configuration.locale.compose_variable_substitution_paragraph_proof(
                o=o)
            return output

        if self._variable_substitution is None:
            self._variable_substitution = InferenceRuleDeclaration(
                universe_of_discourse=self.u,
                symbol='variable-substitution', index=None, auto_index=False,
                dashed_name='variable-substitution',
                name='variable substitution',
                compose_paragraph_proof_method=compose_paragraph_proof,
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
        To avoid inconsistent theory_packages, one must be cautious
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


class AbsorptionInclusion(InferenceRuleInclusion):
    """

    Note: designing a specialized inclusion class is superfluous because InferenceRuleInclusion
    is sufficient to do the job. But the advantage of specializing this class is to provide
    user-friendly type hints and method parameters documentation for that particular
    inference-rule. This may be justified for well-known inference-rules.
    """

    def __init__(self,
                 t: TheoryElaborationSequence,
                 echo: (None, bool) = None,
                 proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.absorption
        dashed_name = 'absorption'
        abridged_name = 'absorp.'
        name = 'absorption'
        explicit_name = 'absorption inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo, proof=proof)

    def infer_formula(self, p_implies_q: (None, FormulaStatement) = None,
                      echo: (None, bool) = None):
        """Apply the absorption inference-rule and return the inferred-formula.

        :param p_implies_q: (mandatory) The implication statement.
        :return: The inferred formula q.
        """
        return super().infer_formula(p_implies_q, echo=echo)

    def infer_statement(self, p_implies_q: (None, FormulaStatement) = None,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """Apply the absorption inference-rule and return the inferred-statement.

        :param p_implies_q: (mandatory) The implication statement.
        :return: An inferred-statement proving p implies p and q in the current theory.
        """
        return super().infer_statement(p_implies_q, nameset=nameset, ref=ref,
                                       paragraph_header=paragraph_header,
                                       subtitle=subtitle, echo=echo)


class AxiomInterpretationInclusion(InferenceRuleInclusion):
    """

    Note: designing a specialized inclusion class is superfluous because InferenceRuleInclusion
    is sufficient to do the job. But the advantage of specializing this class is to provide
    user-friendly type hints and method parameters documentation for that particular
    inference-rule. This may be justified for well-known inference-rules.
    """

    def __init__(self,
                 t: TheoryElaborationSequence,
                 echo: (None, bool) = None,
                 proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.axiom_interpretation
        dashed_name = 'axiom-interpretation'
        acronym = 'ai'
        abridged_name = 'ax.-inter.'
        name = 'axiom interpretation'
        explicit_name = 'axiom interpretation inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo, proof=proof)

    def infer_formula(self, axiom: (None, AxiomInclusion) = None, formula: (None, Formula) = None,
                      echo: (None, bool) = None):
        """Apply the axiom-interpretation inference-rule and return the inferred-formula.

        :param axiom: (mandatory) The axiom-inclusion statement. This proves that the axiom is part of the theory.
        :param formula: (mandatory) The interpretation of the axiom as a formula.
        :return: An inferred-statement proving the formula in the current theory.
        """
        return super().infer_formula(axiom, formula, echo=echo)

    def infer_statement(self, axiom: (None, AxiomInclusion) = None,
                        formula: (None, Formula) = None,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """Apply the axiom-interpretation inference-rule and return the inferred-statement.

        :param axiom: (mandatory) The axiom-inclusion statement. This proves that the axiom is part of the theory.
        :param formula: (mandatory) The interpretation of the axiom as a formula.
        :return: An inferred-statement proving the formula in the current theory.
        """
        return super().infer_statement(axiom, formula, nameset=nameset, ref=ref,
                                       paragraph_header=paragraph_header,
                                       subtitle=subtitle, echo=echo)


class BiconditionalEliminationLeftInclusion(InferenceRuleInclusion):
    """

    Note: designing a specialized inclusion class is superfluous because InferenceRuleInclusion
    is sufficient to do the job. But the advantage of specializing this class is to provide
    user-friendly type hints and method parameters documentation for that particular
    inference-rule. This may be justified for well-known inference-rules.
    """

    def __init__(self,
                 t: TheoryElaborationSequence,
                 echo: (None, bool) = None,
                 proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.biconditional_elimination_left
        dashed_name = 'biconditional-elimination-left'
        acronym = 'bel'
        abridged_name = 'bicond. elim. left'
        name = 'biconditional elimination (left)'
        explicit_name = 'biconditional elimination (left) inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo, proof=proof)

    def infer_formula(self, p_iff_q: (None, FormulaStatement) = None,
                      echo: (None, bool) = None):
        return super().infer_formula(p_iff_q, echo=echo)

    def infer_statement(self, p_iff_q: (None, FormulaStatement) = None,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """Apply the biconditional elimination (left) inference-rule and return the inferred-statement.

        :param p_iff_q: (mandatory) The biconditional statement.
        :return: The proven inferred-statement p implies q in the current theory.
        """
        return super().infer_statement(p_iff_q, nameset=nameset, ref=ref,
                                       paragraph_header=paragraph_header,
                                       subtitle=subtitle, echo=echo)


class BiconditionalEliminationRightInclusion(InferenceRuleInclusion):
    """

    Note: designing a specialized inclusion class is superfluous because InferenceRuleInclusion
    is sufficient to do the job. But the advantage of specializing this class is to provide
    user-friendly type hints and method parameters documentation for that particular
    inference-rule. This may be justified for well-known inference-rules.
    """

    def __init__(self,
                 t: TheoryElaborationSequence,
                 echo: (None, bool) = None,
                 proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.biconditional_elimination_right
        dashed_name = 'biconditional-elimination-right'
        acronym = 'bel'
        abridged_name = 'bicond. elim. right'
        name = 'biconditional elimination (right)'
        explicit_name = 'biconditional elimination (right) inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo, proof=proof)

    def infer_formula(self, p_iff_q: (None, FormulaStatement) = None,
                      echo: (None, bool) = None):
        return super().infer_formula(p_iff_q, echo=echo)

    def infer_statement(self, p_iff_q: (None, FormulaStatement) = None,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """Apply the biconditional elimination (right) inference-rule and return the inferred-statement.

        :param p_iff_q: (mandatory) The biconditional statement.
        :return: The proven inferred-statement p implies q in the current theory.
        """
        return super().infer_statement(p_iff_q, nameset=nameset, ref=ref,
                                       paragraph_header=paragraph_header,
                                       subtitle=subtitle, echo=echo)


class BiconditionalIntroductionInclusion(InferenceRuleInclusion):
    """

    Note: designing a specialized inclusion class is superfluous because InferenceRuleInclusion
    is sufficient to do the job. But the advantage of specializing this class is to provide
    user-friendly type hints and method parameters documentation for that particular
    inference-rule. This may be justified for well-known inference-rules.
    """

    def __init__(self,
                 t: TheoryElaborationSequence,
                 echo: (None, bool) = None,
                 proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.biconditional_introduction
        dashed_name = 'biconditional-introduction'
        acronym = 'bi'
        abridged_name = 'bicond. intro.'
        name = 'biconditional introduction'
        explicit_name = 'biconditional introduction inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo, proof=proof)

    def infer_formula(self, p_implies_q: FormulaStatement = None,
                      q_implies_p: FormulaStatement = None,
                      echo: (None, bool) = None):
        return super().infer_formula(p_iff_q, echo=echo)

    def infer_statement(self, p_implies_q: FormulaStatement = None,
                        q_implies_p: FormulaStatement = None,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """Apply the biconditional elimination (right) inference-rule and return the inferred-statement.

        :param p_iff_q: (mandatory) The biconditional statement.
        :return: The proven inferred-statement p implies q in the current theory.
        """
        return super().infer_statement(p_implies_q, q_implies_p, nameset=nameset, ref=ref,
                                       paragraph_header=paragraph_header,
                                       subtitle=subtitle, echo=echo)


class ConjunctionEliminationLeftInclusion(InferenceRuleInclusion):
    """

    Note: designing a specialized inclusion class is superfluous because InferenceRuleInclusion
    is sufficient to do the job. But the advantage of specializing this class is to provide
    user-friendly type hints and method parameters documentation for that particular
    inference-rule. This may be justified for well-known inference-rules.
    """

    def __init__(self,
                 t: TheoryElaborationSequence,
                 echo: (None, bool) = None,
                 proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_elimination_left
        dashed_name = 'conjunction-elimination-left'
        acronym = 'bel'
        abridged_name = 'conj. elim. left'
        name = 'conjunction elimination (left)'
        explicit_name = 'conjunction elimination (left) inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo, proof=proof)

    def infer_formula(self, p_land_q: (None, FormulaStatement) = None,
                      echo: (None, bool) = None):
        return super().infer_formula(p_land_q, echo=echo)

    def infer_statement(self, p_land_q: (None, FormulaStatement) = None,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """Apply the conjunction elimination (left) inference-rule and return the inferred-statement.

        :param p_iff_q: (mandatory) The conjunction statement.
        :return: The proven inferred-statement p implies q in the current theory.
        """
        return super().infer_statement(p_land_q, nameset=nameset, ref=ref,
                                       paragraph_header=paragraph_header,
                                       subtitle=subtitle, echo=echo)


class ConjunctionEliminationRightInclusion(InferenceRuleInclusion):
    """

    Note: designing a specialized inclusion class is superfluous because InferenceRuleInclusion
    is sufficient to do the job. But the advantage of specializing this class is to provide
    user-friendly type hints and method parameters documentation for that particular
    inference-rule. This may be justified for well-known inference-rules.
    """

    def __init__(self,
                 t: TheoryElaborationSequence,
                 echo: (None, bool) = None,
                 proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_elimination_right
        dashed_name = 'conjunction-elimination-right'
        acronym = 'bel'
        abridged_name = 'conj. elim. right'
        name = 'conjunction elimination (right)'
        explicit_name = 'conjunction elimination (right) inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo, proof=proof)

    def infer_formula(self, p_iff_q: (None, FormulaStatement) = None,
                      echo: (None, bool) = None):
        return super().infer_formula(p_iff_q, echo=echo)

    def infer_statement(self, p_iff_q: (None, FormulaStatement) = None,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """Apply the conjunction elimination (right) inference-rule and return the inferred-statement.

        :param p_iff_q: (mandatory) The conjunction statement.
        :return: The proven inferred-statement p implies q in the current theory.
        """
        return super().infer_statement(p_iff_q, nameset=nameset, ref=ref,
                                       paragraph_header=paragraph_header,
                                       subtitle=subtitle, echo=echo)


class ConjunctionIntroductionInclusion(InferenceRuleInclusion):
    """

    Note: designing a specialized inclusion class is superfluous because InferenceRuleInclusion
    is sufficient to do the job. But the advantage of specializing this class is to provide
    user-friendly type hints and method parameters documentation for that particular
    inference-rule. This may be justified for well-known inference-rules.
    """

    def __init__(self,
                 t: TheoryElaborationSequence,
                 echo: (None, bool) = None,
                 proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.conjunction_introduction
        dashed_name = 'conjunction-introduction'
        acronym = 'ci'
        abridged_name = 'conj.-intro.'
        name = 'conjunction introduction'
        explicit_name = 'conjunction introduction inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo, proof=proof)

    def infer_formula(self, p: (None, FormulaStatement) = None,
                      q: (None, FormulaStatement) = None,
                      echo: (None, bool) = None):
        """Apply the conjunction-introduction inference-rule and return the inferred-formula.
        """
        return super().infer_formula(p, q, echo=echo)

    def infer_statement(self, p: (None, FormulaStatement) = None,
                        q: (None, FormulaStatement) = None,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """Apply the conjunction-introduction inference-rule and return the inferred-statement.

        :param p_implies_q: (mandatory) The implication statement.
        :param p: (mandatory) The p statement, proving that p is true in the current theory.
        :return: An inferred-statement proving p in the current theory.
        """
        return super().infer_statement(p, q, nameset=nameset, ref=ref,
                                       paragraph_header=paragraph_header,
                                       subtitle=subtitle, echo=echo)


class InconsistencyIntroductionInclusion(InferenceRuleInclusion):
    """

    Note: designing a specialized inclusion class is superfluous because InferenceRuleInclusion
    is sufficient to do the job. But the advantage of specializing this class is to provide
    user-friendly type hints and method parameters documentation for that particular
    inference-rule. This may be justified for well-known inference-rules.
    """

    def __init__(self,
                 t: TheoryElaborationSequence,
                 echo: (None, bool) = None,
                 proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.inconsistency_introduction
        dashed_name = 'inconsistency-introduction'
        acronym = 'ii'
        abridged_name = 'inc.-intro.'
        name = 'inconsistency introduction'
        explicit_name = 'inconsistency introduction inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo, proof=proof)

    def infer_formula(self, p: (None, FormulaStatement) = None,
                      not_p: (None, FormulaStatement) = None,
                      inconsistent_theory: (None, TheoryElaborationSequence) = None,
                      t: (None, TheoryElaborationSequence) = None,
                      echo: (None, bool) = None):
        """Apply the inconsistency-introduction inference-rule and return the inferred-formula.
        """
        return super().infer_formula(p, not_p, inconsistent_theory, echo=echo)

    def infer_statement(self, p: (None, FormulaStatement) = None,
                        not_p: (None, FormulaStatement) = None,
                        inconsistent_theory: (None, TheoryElaborationSequence) = None,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """Apply the inconsistency-introduction inference-rule and return the inferred-statement.

        :param p: (mandatory) .
        :param not_p: (mandatory) .
        :param inconsistent_theory: (conditional) .
        :return: An inferred-statement proving p in the current theory.
        """
        if inconsistent_theory is None and p.t is not_p.t:
            # The inconsistent_theory can be unambiguously defaulted
            # when both p and not_p are contained in the same theory.
            inconsistent_theory = p.t
        return super().infer_statement(p, not_p, inconsistent_theory, nameset=nameset, ref=ref,
                                       paragraph_header=paragraph_header,
                                       subtitle=subtitle, echo=echo)


class ModusPonensInclusion(InferenceRuleInclusion):
    """

    Note: designing a specialized inclusion class is superfluous because InferenceRuleInclusion
    is sufficient to do the job. But the advantage of specializing this class is to provide
    user-friendly type hints and method parameters documentation for that particular
    inference-rule. This may be justified for well-known inference-rules.
    """

    def __init__(self,
                 t: TheoryElaborationSequence,
                 echo: (None, bool) = None,
                 proof: (None, bool) = None):
        i = t.universe_of_discourse.inference_rules.modus_ponens
        dashed_name = 'modus-ponens'
        acronym = 'mp'
        abridged_name = 'mod.-pon.'
        name = 'modus ponens'
        explicit_name = 'modus ponens inference rule'
        super().__init__(t=t, i=i, dashed_name=dashed_name, acronym=acronym,
                         abridged_name=abridged_name, name=name, explicit_name=explicit_name,
                         echo=echo, proof=proof)

    def infer_formula(self, p_implies_q: (None, FormulaStatement) = None,
                      p: (None, FormulaStatement) = None,
                      echo: (None, bool) = None):
        """Apply the modus-ponens inference-rule and return the inferred-formula.

        :param p_implies_q: (mandatory) The implication statement.
        :param p: (mandatory) The p statement, proving that p is true in the current theory.
        :return: The inferred formula q.
        """
        return super().infer_formula(p_implies_q, p, echo=echo)

    def infer_statement(self, p_implies_q: (None, FormulaStatement) = None,
                        p: (None, FormulaStatement) = None,
                        nameset: (None, str, NameSet) = None,
                        ref: (None, str) = None,
                        paragraph_header: (None, ParagraphHeader) = None,
                        subtitle: (None, str) = None,
                        echo: (None, bool) = None) -> InferredStatement:
        """Apply the modus-ponens inference-rule and return the inferred-statement.

        :param p_implies_q: (mandatory) The implication statement.
        :param p: (mandatory) The p statement, proving that p is true in the current theory.
        :return: An inferred-statement proving p in the current theory.
        """
        return super().infer_statement(p_implies_q, p, nameset=nameset, ref=ref,
                                       paragraph_header=paragraph_header,
                                       subtitle=subtitle, echo=echo)


class InferenceRuleInclusionDict(collections.UserDict):
    """The repository of inference-rules included in a theory. In complement, this object exposes
    well-known inference-rules as easily accessible python properties. Accessing these properties
    automatically include (aka recognizes as well-founded and valid) the corresponding
    inference-rule in the current theory.

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

               Warning
               -------
               Axiom-interpretation is especially dangerous because, contrary to most inference-rules,
               it allows the introduction of arbitrary truthes in the theory. For this reason,
               one must be very attentive when applying this inference-rule to assure the resulting
               formula-statement complies / interprets properly its related contentual-axiom.
               """
        if self._axiom_interpretation is None:
            self._axiom_interpretation = AxiomInterpretationInclusion(t=self.t)
        return self._axiom_interpretation

    @property
    def bel(self) -> BiconditionalEliminationLeftInclusion:
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
    def bi(self) -> BiconditionalIntroductionInclusion:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Unabridged property: u.i.biconditional_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        return self.biconditional_introduction

    @property
    def biconditional_elimination_left(self) -> BiconditionalEliminationLeftInclusion:
        """The well-known biconditional-elimination (left) inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Abridged property: u.i.bel

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._biconditional_elimination_left is None:
            self._biconditional_elimination_left = BiconditionalEliminationLeftInclusion(t=self.t)
        return self._biconditional_elimination_left

    @property
    def biconditional_elimination_right(self) -> BiconditionalEliminationRightInclusion:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Abridged property: u.i.ber()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._biconditional_elimination_left is None:
            self._biconditional_elimination_left = BiconditionalEliminationRightInclusion(t=self.t)
        return self._biconditional_elimination_left

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
    def conjunction_elimination_left(self) -> ConjunctionEliminationLeftDeclaration:
        """The well-known conjunction-elimination (left) inference-rule: P ∧ Q ⊢ P.

        Abridged property: t.i.cel()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._conjunction_elimination_left is None:
            self._conjunction_elimination_left = ConjunctionEliminationLeftInclusion(t=self.t)
        return self._conjunction_elimination_left

    @property
    def conjunction_elimination_right(self) -> InferenceRuleInclusion:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        Abridged property: t.i.cer

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically declared.
        """
        if self._conjunction_elimination_right is None:
            self._conjunction_elimination_right = ConjunctionEliminationRightInclusion(t=self.t)
        return self._conjunction_elimination_right

    @property
    def cel(self) -> InferenceRuleInclusion:
        """The well-known conjunction-elimination (left) inference-rule: (P ∧ Q) ⊢ P.

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
    def ci(self) -> ConjunctionIntroductionInclusion:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_introduction()

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
                name='definition interpretation')
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
                name='disjunction introduction')
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
                name='double negation elimination')
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
                name='double negation introduction')
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
                name='equality commutativity')
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
                name='equal terms substitution')
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
    def inconsistency_introduction(self) -> InconsistencyIntroductionInclusion:
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
            self._inconsistency_introduction = InconsistencyIntroductionInclusion(t=self.t)
        return self._inconsistency_introduction

    @property
    def ii(self) -> InconsistencyIntroductionInclusion:
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
        To avoid inconsistent theory_packages, one must be cautious
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
                name='variable substitution')
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
        To avoid inconsistent theory_packages, one must be cautious
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
                 symbol: (None, str, StyledText) = None,
                 dashed_name: (None, str, StyledText) = None,
                 name: (None, str, ComposableText) = None,
                 echo: (None, bool) = None):
        echo = prioritize_value(echo, configuration.echo_universe_of_discourse_declaration,
                                configuration.echo_default,
                                False)
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
        # self.symbol_indexes = dict()
        # self.titles = dict()

        if nameset is None:
            symbol = prioritize_value(symbol, StyledText(
                plaintext='U', text_style=text_styles.script_normal))
            dashed_name = prioritize_value(symbol, StyledText(
                plaintext='universe-of-discourse-', text_style=text_styles.serif_italic))
            index = index_universe_of_discourse_symbol(base=symbol)
            nameset = NameSet(symbol=symbol, dashed_name=dashed_name, index=index, name=name)
        elif isinstance(nameset, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            index = index_universe_of_discourse_symbol(base=nameset)
            nameset = NameSet(s=nameset, index=index, name=name)
        super().__init__(
            is_universe_of_discourse=True,
            is_theory_foundation_system=False,
            nameset=nameset,
            universe_of_discourse=None,
            echo=False)
        super()._declare_class_membership(classes.universe_of_discourse)
        if echo:
            self.echo()

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='universe-of-discourse')

    def compose_declaration(self) -> collections.abc.Generator[Composable, None, None]:
        global text_dict
        yield SansSerifNormal('Let ')
        yield text_dict.open_quasi_quote
        yield from self.nameset.compose_symbol()
        yield text_dict.close_quasi_quote
        yield SansSerifNormal(' be a ')
        yield from self.compose_class()
        yield text_dict.period

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
        duplicate = self.symbolic_objcts.get(o.nameset)
        verify(
            duplicate is None,
            'A symbolic-object already exists in the current universe-of-discourse with a duplicate (symbol, index) pair.',
            o=o,
            duplicate=duplicate,
            slf=self)
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
            self, symbol: (None, str, StyledText) = None, index: (None, int, str) = None,
            auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None) -> SymbolicObject:
        """"""
        return SymbolicObject(
            universe_of_discourse=self, symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name, ref=ref, subtitle=subtitle, echo=echo)

    def declare_theory(
            self,
            nameset: (None, str, NameSet) = None,
            ref: (None, str) = None,
            subtitle: (None, str) = None,
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
            ref=ref,
            subtitle=subtitle,
            extended_theory=extended_theory,
            extended_theory_limit=extended_theory_limit,
            stabilized=stabilized,
            echo=echo)

    def declare_axiom(
            self, natural_language: str,
            symbol: (None, str, StyledText) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None) -> AxiomDeclaration:
        """Elaborate a new axiom 𝑎 in this universe-of-discourse."""
        return AxiomDeclaration(
            u=self, natural_language=natural_language, symbol=symbol, dashed_name=dashed_name,
            acronym=acronym, abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            ref=ref, subtitle=subtitle,
            nameset=nameset, echo=echo)

    def declare_definition(
            self, natural_language: str, symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            nameset: (None, str, NameSet) = None, echo: (None, bool) = None):
        """Elaborate a new axiom 𝑎 in this universe-of-discourse."""
        return DefinitionDeclaration(
            u=self, natural_language=natural_language, symbol=symbol, index=index,
            auto_index=auto_index, dashed_name=dashed_name, acronym=acronym,
            abridged_name=abridged_name, name=name, explicit_name=explicit_name,
            ref=ref, subtitle=subtitle,
            nameset=nameset, echo=echo)

    def echo(self):
        return repm.prnt(self.rep_declaration(cap=True))

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
    def i(self):
        """A python dictionary of inference-rules contained in this universe-of-discourse,
        where well-known inference-rules are directly available as properties."""
        return self.inference_rules

    def index_symbol(self, symbol: StyledText) -> int:
        """Given a symbol-base S (i.e. an unindexed symbol), returns a unique integer n
        such that (S, n) is a unique identifier in this instance of UniverseOfDiscourse.

        :param symbol: The symbol-base.
        :return:
        """
        return self.get_symbol_max_index(symbol) + 1

    @property
    def inference_rules(self):
        """A python dictionary of inference-rules contained in this universe-of-discourse,
        where well-known inference-rules are directly available as properties."""
        return self._inference_rules

    @property
    def o(self) -> SimpleObjctDict:
        """The collection of simple-objcts in this universe-of-discourse.

        Unabridged version: universe_of_discourse.simple_objcts

        Well-known simple-objcts are exposed as python properties. In general, a well-known simple-objct is declared in the universe-of-discourse the first time its property is accessed.

        :return:
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

    def rep_declaration(self, encoding: (None, Encoding) = None, cap: (None, bool) = None) -> str:
        return rep_composition(composition=self.compose_declaration(), encoding=encoding, cap=cap)

    @property
    def simple_objcts(self) -> SimpleObjctDict:
        """The collection of simple-objcts in this universe-of-discourse.

        Abridged version: u.o

        Well-known simple-objcts are exposed as python properties. In general, a well-known simple-objct is declared in the universe-of-discourse the first time its property is accessed.

        :return:
        """
        return self._simple_objcts

    def so(self, symbol=None):
        return self.declare_symbolic_objct(
            symbol=symbol)

    def t(
            self,
            nameset: (None, str, NameSet) = None,
            ref: (None, str) = None,
            subtitle: (None, str) = None,
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
            ref=ref,
            subtitle=subtitle,
            extended_theory=extended_theory,
            extended_theory_limit=extended_theory_limit,
            stabilized=stabilized,
            echo=echo)

    def take_note(
            self, t: TheoryElaborationSequence, content: str,
            symbol: (None, str, StyledText) = None, index: (None, int) = None,
            auto_index: (None, bool) = None, dashed_name: (None, str, StyledText) = None,
            acronym: (None, str, StyledText) = None, abridged_name: (None, str, StyledText) = None,
            name: (None, str, StyledText) = None, explicit_name: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None, ref: (None, str, StyledText) = None,
            subtitle: (None, str, StyledText) = None, nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None):
        """Take a note, make a comment, or remark."""
        verify(
            t.universe_of_discourse is self,
            'This universe-of-discourse 𝑢₁ (self) is distinct from the universe-of-discourse 𝑢₂ of the theory '
            'parameter 𝑡.')

        return NoteInclusion(t=t, content=content, symbol=symbol, index=index,
                             auto_index=auto_index,
                             dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name,
                             name=name, explicit_name=explicit_name,
                             paragraph_header=paragraph_header, ref=ref,
                             subtitle=subtitle,
                             nameset=nameset, echo=echo)

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


def declare_universe_of_discourse(nameset: (None, str, NameSet) = None,
                                  name: (None, str, ComposableText) = None,
                                  echo: (None, bool) = None) -> UniverseOfDiscourse:
    return UniverseOfDiscourse(nameset=nameset, name=name, echo=echo)


class InferredStatement(FormulaStatement):
    """A statement inferred from an inference-rule in the current theory-elaboration.
    """

    def __init__(
            self,
            *parameters,
            i: InferenceRuleDeclaration,  # TODO: DESIGN-FLAW: PASS InferenceRuleInclusion instead
            t: TheoryElaborationSequence,
            symbol: (None, str, StyledText) = None,
            index: (None, int) = None, auto_index: (None, bool) = None,
            dashed_name: (None, str, StyledText) = None, acronym: (None, str, StyledText) = None,
            abridged_name: (None, str, StyledText) = None, name: (None, str, StyledText) = None,
            explicit_name: (None, str, StyledText) = None,
            ref: (None, str, StyledText) = None, subtitle: (None, str, StyledText) = None,
            paragraph_header: (None, ParagraphHeader) = None,
            nameset: (None, str, NameSet) = None,
            echo: (None, bool) = None,
            echo_proof: (None, bool) = None):
        """Include (aka allow) an inference_rule in a theory-elaboration.
        """
        echo = prioritize_value(echo, configuration.echo_inferred_statement,
                                configuration.echo_statement, configuration.echo_default,
                                False)
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
            symbol=symbol, index=index, auto_index=auto_index,
            dashed_name=dashed_name, acronym=acronym, abridged_name=abridged_name, name=name,
            explicit_name=explicit_name,
            ref=ref, subtitle=subtitle,
            nameset=nameset, paragraphe_header=paragraph_header,
            echo=False)
        super()._declare_class_membership(declarative_class_list.inferred_proposition)
        if self.inference_rule is self.t.u.i.inconsistency_introduction and \
                self.valid_proposition.relation is self.t.u.r.inconsistent and \
                self.valid_proposition.parameters[0] is self.t:
            # This inferred-statement proves the inconsistency
            # of the current theory-elaboration-sequence.
            t.report_inconsistency_proof(proof=self)
        if echo:
            self.echo(proof=echo_proof)
        if self.inference_rule is self.t.u.i.axiom_interpretation or \
                self.inference_rule is self.t.u.i.definition_interpretation:
            t.assure_interpretation_disclaimer(echo=echo)

    def compose_class(self) -> collections.abc.Generator[Composable, None, None]:
        # TODO: Instead of hard-coding the class name, use a meta-theory.
        yield SerifItalic(plaintext='inferred-statement')

    def compose_report(self, proof: (None, bool) = None):
        output = yield from configuration.locale.compose_inferred_statement_report(
            o=self, proof=proof)
        return output

    def echo(self, proof: (None, bool) = None):
        proof = prioritize_value(proof, configuration.echo_proof, True)
        repm.prnt(self.rep_report(proof=proof))

    @property
    def parameters(self) -> tuple:
        return self._parameters

    @property
    def inference_rule(self) -> InferenceRuleDeclaration:
        """Return the inference-rule upon which this inference-rule-inclusion is based.
        """
        return self._inference_rule

    def rep_report(self, encoding: (None, Encoding) = None, proof: (None, bool) = None) -> str:
        return rep_composition(composition=self.compose_report(proof=proof),
                               encoding=encoding)

    def rep_report_OBSOLETE(self, encoding: (None, Encoding) = None, proof=True) -> str:
        """Return a representation that expresses and justifies the statement."""
        encoding = prioritize_value(encoding, configuration.encoding,
                                    encodings.plaintext)
        rep = f'{self.rep_title(encoding=encoding, cap=True)}: {self.valid_proposition.rep_formula()}' + '\n\t'
        rep = wrap_text(rep) + '\n'
        if proof:
            rep = rep + self.rep_two_columns_proof_OBSOLETE(encoding=encoding)
        return rep

    def rep_two_columns_proof_OBSOLETE(self, encoding: (None, Encoding) = None):
        rep = self.inference_rule.rep_two_columns_proof_OBSOLETE(s=self, encoding=encoding)
        return rep


def rep_two_columns_proof_item(left: str, right: str) -> str:
    """Format a two-columns proof row.
    TODO: Implement logic for plaintext, unicode and latex.
    """
    left_column_width = prioritize_value(configuration.two_columns_proof_left_column_width,
                                         67)
    right_column_width = prioritize_value(configuration.two_columns_proof_right_column_width,
                                          30)
    report = textwrap.wrap(text=left, width=left_column_width, break_on_hyphens=False)
    report = [line.ljust(left_column_width, ' ') + ' | ' for line in report]
    report[len(report) - 1] = report[len(report) - 1] + right
    report = '\n'.join(report)
    return report + '\n'


def rep_two_columns_proof_end(left: str) -> str:
    """Format the end of a two-columns proof
    TODO: Implement logic for plaintext, unicode and latex.
    """
    left_column_width = prioritize_value(configuration.two_columns_proof_left_column_width,
                                         67)
    right_column_width = prioritize_value(configuration.two_columns_proof_right_column_width,
                                          30)
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

    def __init__(
            self, p, not_p, nameset=None, paragraphe_header=None, theory=None,
            title=None):
        if title is None:
            title = 'THEORY INCONSISTENCY'
        paragraphe_header = paragraph_headers.proposition if paragraphe_header is None else paragraphe_header
        self.p = p
        self.not_p = not_p
        valid_proposition = InconsistencyIntroductionInferenceRuleOBSOLETE.execute_algorithm(
            theory=theory, p=p, not_p=not_p)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            paragraphe_header=paragraphe_header, title=title,
            nameset=nameset)
        # The theory is proved inconsistent!
        theory.prove_inconsistent(self)
        if configuration.warn_on_inconsistency:
            warnings.warn(f'{self.rep_report(proof=True)}', InconsistencyWarning)

    def rep_report(self, proof=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.rep_title(cap=True)}: {self.valid_proposition.rep_formula()}'
        if proof:
            output = output + f'\n\t{repm.serif_bold("Proof of inconsistency")}'
            output = output + f'\n\t{self.p.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.p.rep_ref())}.'
            output = output + f'\n\t{self.not_p.rep_formula(expand=True):<70} │ Follows from {repm.serif_bold(self.not_p.rep_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.rep_formula(expand=True):<70} │ ∎'
        return output + f'\n'


class InconsistencyIntroductionInferenceRuleOBSOLETE(InferenceRuleOBSOLETE):
    """An implementation of the inconsistency-introduction inference-rule."""

    @staticmethod
    def infer(
            theory, p, not_p, symbol=None, paragraph_header=None,
            title=None):
        """"""
        return InconsistencyIntroductionStatement(
            p=p, not_p=not_p, nameset=symbol,
            paragraphe_header=paragraph_header, theory=theory, title=title)

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
    configuration.default_hypothesis_symbol = SerifNormal('H')
    configuration.default_inference_rule_declaration_symbol = SerifNormal('I')
    configuration.default_inference_rule_inclusion_symbol = SerifNormal('I')
    configuration.default_note_symbol = SerifItalic('note')
    configuration.default_relation_symbol = SerifItalic('r')
    configuration.default_statement_symbol = SerifNormal('P')
    configuration.default_symbolic_object_symbol = SerifItalic('o')
    configuration.default_theory_symbol = ScriptNormal('T')
    configuration.echo_axiom_declaration = None
    configuration.echo_axiom_inclusion = None
    configuration.echo_definition_declaration = None
    configuration.echo_definition_inclusion = None
    configuration.echo_definition_direct_inference = None
    configuration.echo_formula_declaration = False  # In general, this is too verbose.
    configuration.echo_hypothesis = None
    configuration.echo_inferred_statement = None
    configuration.echo_note = None
    configuration.echo_relation = None
    configuration.echo_simple_objct_declaration = None
    configuration.echo_statement = None
    configuration.echo_symbolic_objct = None
    configuration.echo_theory_elaboration_sequence_declaration = None
    configuration.echo_universe_of_discourse_declaration = None
    configuration.echo_free_variable_declaration = None
    configuration.echo_encoding = None
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
    def __init__(self):
        pass

    def develop(self) -> TheoryElaborationSequence:
        """Elaborate a new theory in a new universe with the content of the package.

        """
        u = declare_universe_of_discourse()
        t = u.declare_theory()
        self.develop_theory(t=t)
        return t

    @abc.abstractmethod
    def develop_theory(self, t: TheoryElaborationSequence) -> TheoryElaborationSequence:
        """Given a theory t, pursue the elaboration of that theory with the content of the package.

        This is the key method that must be implemented by the non-abstract package."""
        raise NotImplementedError()

    def develop_universe(self, u: UniverseOfDiscourse) -> TheoryElaborationSequence:
        """Given a universe u, elaborate a new theory with the content of the package in that universe.

        """
        t = u.declare_theory()
        t = self.develop_theory(t=t)
        return t


pass
