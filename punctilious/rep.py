import unicode
import typing
import unidecode


class TextStyle:
    def __init__(self, font_style_name: str, unicode_table_index: int, latex_math_start_tag: str,
                 latex_math_end_tag: str):
        self.font_style_name = font_style_name
        self.unicode_table_index = unicode_table_index
        self.latex_math_start_tag = latex_math_start_tag
        self.latex_math_end_tag = latex_math_end_tag

    def __hash__(self):
        return hash((TextStyle, self.font_style_name))


class SerifBold(TextStyle):
    def __init__(self):
        super().__init__('serif-bold', unicode.unicode_serif_bold_index, '\\mathbf{', '}')


class SerifNormal(TextStyle):
    def __init__(self):
        super().__init__('serif-normal', unicode.unicode_serif_normal_index, '\\mathnormal{', '}')


class DoubleStruck(TextStyle):
    def __init__(self):
        super().__init__('double-strucj', unicode.unicode_double_struck, '\\mathbb{', '}')


class TextStyles:
    def __init__(self):
        self.double_struck = DoubleStruck()
        self.serif_bold = SerifBold()
        self.serif_normal = SerifNormal()


text_styles = TextStyles()


class TextFormat:
    def __init__(self, text_format_name: str):
        self._text_format_name = text_format_name

    def __hash__(self):
        return hash((TextFormat, self._text_format_name))


class LatexMath(TextFormat):
    def __init__(self):
        super().__init__('latex')


class Plaintext(TextFormat):
    def __init__(self):
        super().__init__('plaintext')


class Unicode(TextFormat):
    def __init__(self):
        super().__init__('unicode')


class TextFormats:
    def __init__(self):
        self.latex_math = LatexMath()
        self.plaintext = Plaintext()
        self.unicode = Unicode()


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


plaintext = 'hello world 123!'
x = StyledText(plaintext, text_styles.serif_bold)
print(x.repr(text_formats.plaintext))
print(x.repr(text_formats.unicode))
print(x.repr(text_formats.latex_math))
x = StyledText(plaintext, text_styles.serif_normal)
print(x.repr(text_formats.plaintext))
print(x.repr(text_formats.unicode))
print(x.repr(text_formats.latex_math))
x = StyledText(plaintext, text_styles.double_struck)
print(x.repr(text_formats.plaintext))
print(x.repr(text_formats.unicode))
print(x.repr(text_formats.latex_math))
