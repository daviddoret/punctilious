"""The Representation Module (repm) is an independant module that provides IO and string manipulation utilities."""
import textwrap
import unidecode
import typing

_serif_bold_dict = {
    'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠',
    'h': '𝐡', 'i': '𝐢', 'j': '𝐣',
    'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩', 'q': '𝐪',
    'r': '𝐫', 's': '𝐬', 't': '𝐭',
    'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳', 'A': '𝐀',
    'B': '𝐁', 'C': '𝐂', 'D': '𝐃',
    'E': '𝐄', 'F': '𝐅', 'G': '𝐆', 'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊',
    'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
    'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
    'V': '𝐕', 'W': '𝐖', 'X': '𝐗',
    'Y': '𝐘', 'Z': '𝐙', '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
    '5': '𝟓', '6': '𝟔', '7': '𝟕',
    '8': '𝟖', '9': '𝟗'}

_monospace_dict = {
    'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶',
    'H': '𝙷', 'I': '𝙸', 'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽',
    'O': '𝙾', 'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄',
    'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉'}


def serif_bold(s=None):
    """Convert to serif bold characters the string s.
    """
    global _serif_bold_dict
    if isinstance(s, int):
        s = str(s)
    if s is None or s == '':
        return ''
    return ''.join([_serif_bold_dict.get(c, c) for c in s])


def monospace(s=None):
    """Convert to monospace characters the string s.
    """
    global _monospace_dict
    if isinstance(s, int):
        s = str(s)
    if s is None or s == '':
        return ''
    return ''.join([_monospace_dict.get(c, c) for c in s])


def wrap(text):
    """Wrap text for friendly rendering as text, e.g. in a console.

    :param text:
    :return:
    """
    return '\n'.join(
        textwrap.wrap(
            text=text, width=70,
            subsequent_indent=f'\t',
            break_on_hyphens=False,
            expand_tabs=True,
            tabsize=4))


class TextFormat:
    def __init__(self, text_format_name: str):
        self._text_format_name = text_format_name

    def __hash__(self):
        return hash((TextFormat, self._text_format_name))

    def __repr__(self):
        return self._text_format_name

    def __str__(self):
        return self._text_format_name


class TextFormats():
    def __init__(self):
        super().__init__('text-formats')
        self.html = TextFormat('html')
        self.latex = TextFormat('latex')
        self.plaintext = TextFormat('plaintext')
        self.markdown = TextFormat('markdown')
        self.unicode = TextFormat('unicode')


text_formats = TextFormats()


class FontWeight:
    def __init__(self, font_weight_name: str):
        self._font_weight_name = font_weight_name

    def __hash__(self):
        return hash((FontWeight, self._font_weight_name))

    def __repr__(self):
        return self._font_weight_name

    def __str__(self):
        return self._font_weight_name


class FontWeights:
    def __init__(self):
        self.plain = FontWeight('plain')
        self.bold = FontWeight('bold')


font_weights = FontWeights()


class FontStyle:
    def __init__(self, font_style_name: str):
        self._font_style_name = font_style_name

    def __hash__(self):
        return hash((FontStyle, self._font_style_name))

    def __repr__(self):
        return self._font_style_name

    def __str__(self):
        return self._font_style_name

    def repr(self, s: str, text_format: TextFormat = text_formats.plaintext):
        match text_format:
            case text_formats.latex:
                return self.repr_as_latex(s)
            case text_formats.plaintext:
                return self.repr_as_plaintext(s)
            case text_formats.unicode:
                return self.repr_as_unicode(s)
            case _:
                return self.repr_as_plaintext(s)

    def repr_as_plaintext(self, s: str):
        return s

    def repr_as_unicode(self, s: str):
        return s

    def repr_as_latex(self, s: str):
        return s


class ItalicFontStyle(FontStyle):
    def __init__(self):
        super().__init__('italic')

    def repr_as_plaintext(self, s: str):
        return s

    def repr_as_unicode(self, s: str):
        return s

    def repr_as_latex(self, s: str):
        return s


class FontStyles:
    def __init__(self):
        self.normal = FontStyle('normal')
        self.italic = FontStyle('italic')


font_styles = FontStyles()


class FontFamily:
    def __init__(self, font_family_name: str):
        self._font_family_name = font_family_name

    def __hash__(self):
        return hash((FontFamily, self._font_family_name))

    def __repr__(self):
        return self._font_family_name

    def __str__(self):
        return self._font_family_name


class FontFamilies:
    def __init__(self):
        self.monospace = FontFamily('monospace')
        self.sans_serif = FontFamily('sans-serif')
        self.serif = FontFamily('serif')


font_families = FontFamilies()


class StyledText:
    """

    """

    def __init__(self, content: str, font_weight: FontWeight = font_weights.plain,
                 font_style: FontStyle = font_styles.normal, font_family: FontFamily = font_families.sans_serif):
        self._content = unidecode.unidecode(content)
        self._font_weight = font_weight
        self._font_style = font_style
        self._font_family = font_family

    def __hash__(self):
        """WARNING: hash is only computed on the content???"""
        return hash(self._content)

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    @property
    def content(self) -> str:
        return self._content

    def repr(self, text_format: TextFormat = text_formats.plaintext):
        match text_format:
            case text_formats.plaintext:
                return self.repr_as_plaintext()
            case text_formats.unicode:
                return self.repr_as_unicode()
            case _:
                return self.repr_as_plaintext()

    def repr_as_latex(self):
        pass

    def repr_as_plaintext(self):
        return self.content

    def repr_as_unicode(self):
        return self.content


class ValueName(StyledText):
    """ValueName models arbitrary named values.

    The ValueName pythonic-class is used to expose feasible value-lists.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UseCase(ValueName):
    pass


class UseCases(ValueName):
    def __init__(self):
        super().__init__('use_cases')
        self.symbol = UseCase('symbol')
        self.dashed_name = UseCase('dashed_name')
        self.reference = UseCase('reference')
        self.natural_name = UseCase('natural_name')


use_cases = UseCases()


class Style(ValueName):
    pass


class Styles(ValueName):
    serif_normal = Style('serif_normal')
    serif_bold = Style('serif_bold')
    serif_italic = Style('serif_italic')
    serif_bold_italic = Style('serif_bold_italic')
    sans_serif_normal = Style('sans_serif_normal')
    sans_serif_bold = Style('sans_serif_bold')
    sans_serif_italic = Style('sans_serif_italic')
    sans_serif_bold_italic = Style('sans_serif_bold_italic')
    script_normal = Style('script_normal')
    script_bold = Style('script_bold')
    fraktur_normal = Style('fraktur_normal')
    fraktur_bold = Style('fraktur_bold')
    monospace_normal = Style('monospace_normal')
    double_struck_normal = Style('double_struck_normal')


styles = Style('styles')

utf8_subscript_dictionary = {
    '0': u'₀',
    '1': u'₁',
    '2': u'₂',
    '3': u'₃',
    '4': u'₄',
    '5': u'₅',
    '6': u'₆',
    '7': u'₇',
    '8': u'₈',
    '9': u'₉',
    'a': u'ₐ',
    'e': u'ₑ',
    'o': u'ₒ',
    'x': u'ₓ',
    # '???': u'ₔ',
    'h': u'ₕ',
    'k': u'ₖ',
    'l': u'ₗ',
    'm': u'ₘ',
    'n': u'ₙ',
    'p': u'ₚ',
    's': u'ₛ',
    't': u'ₜ',
    '+': u'₊',
    '-': u'₋',
    '=': u'₌',
    '(': u'₍',
    ')': u'₎',
    'j': u'ⱼ',
    'i': u'ᵢ',  # Alternative from the Unicode Phonetic Extensions block: ᵢ
    'r': u'ᵣ',  # Source: Unicode Phonetic Extensions block.
    'u': u'ᵤ',  # Source: Unicode Phonetic Extensions block.
    'v': u'ᵥ',  # Source: Unicode Phonetic Extensions block.
    'β': u'ᵦ',  # Source: Unicode Phonetic Extensions block.
    'γ': u'ᵧ',  # Source: Unicode Phonetic Extensions block.
    # '???': u'ᵨ', # Source: Unicode Phonetic Extensions block.
    'φ': u'ᵩ',  # Source: Unicode Phonetic Extensions block.
    'χ': u'ᵪ'  # Source: Unicode Phonetic Extensions block.
}


def subscriptify(s=None):
    """Converts to unicode-subscript the string s.

    References:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript
        * https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts
    """
    global utf8_subscript_dictionary
    if isinstance(s, int):
        s = str(s)
    if s is None or s == '':
        return ''
    return ''.join([utf8_subscript_dictionary.get(c, c) for c in s])


def prnt(s):
    print(s)
