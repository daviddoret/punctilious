"""Text utilities."""

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

    def __hash__(self):
        return hash((TextStyle, self.font_style_name))


class TextStyles:
    """Expose a catalog of supported text-styles."""

    def __init__(self):
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
        self.serif_normal = TextStyle(
            font_style_name='serif-normal',
            unicode_table_index=unicode.unicode_serif_normal_index,
            latex_math_start_tag=r'\mathnormal{',
            latex_math_end_tag=r'}')


text_styles = TextStyles()


class TextFormat:
    """A supported output text format."""

    def __init__(self, text_format_name: str):
        self._text_format_name = text_format_name

    def __hash__(self):
        return hash((TextFormat, self._text_format_name))


class TextFormats:
    def __init__(self):
        self.latex_math = TextFormat('latex-math')
        self.plaintext = TextFormat('plaintext')
        self.unicode = TextFormat('unicode')


text_formats = TextFormats()


class StyledText:
    def __init__(self, plaintext: str, text_style: TextStyle = text_styles.serif_normal):
        self._plaintext = unidecode.unidecode(plaintext)
        self._text_style = text_style

    def __hash__(self):
        return hash((StyledText, self._plaintext, self._text_style))

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def repr(self, text_format: TextFormat = text_formats.plaintext):
        match text_format:
            case text_formats.plaintext:
                return self.repr_as_plaintext()
            case text_formats.latex_math:
                return self.repr_as_latex_math()
            case text_formats.unicode:
                return self.repr_as_unicode()

    def repr_as_latex_math(self):
        return f'{self._text_style.latex_math_start_tag}{self._plaintext}{self._text_style.latex_math_end_tag}'

    def repr_as_plaintext(self):
        return self._plaintext

    def repr_as_unicode(self):
        return unicode.unicode_format(self._plaintext, self._text_style.unicode_table_index)
