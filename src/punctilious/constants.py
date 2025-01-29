import enum

# formal-language constants

FORMULA_CONNECTOR_INDEX: int = 0
FORMULA_ARGUMENTS_INDEX: int = 1
FORMULA_FIXED_ARITY: int = 2

# meta-language formula structures

AXIOM_VALID_STATEMENT_INDEX: int = 0
AXIOM_FIXED_ARITY: int = 1

EXTENSION_MAP_DOMAIN_INDEX: int = 0  # The index-position of the `domain` element in the `arguments` tuple.
EXTENSION_MAP_CODOMAIN_INDEX: int = 1  # The index-position of the `codomain` element in the `arguments` tuple.
EXTENSION_MAP_FIXED_ARITY: int = 2  # A syntactic-rule.

NATURAL_INFERENCE_RULE_VARIABLES_INDEX: int = 0
NATURAL_INFERENCE_RULE_PREMISES_INDEX: int = 1
NATURAL_INFERENCE_RULE_CONCLUSION_INDEX: int = 2
NATURAL_INFERENCE_RULE_FIXED_ARITY: int = 3

THEOREM_STATEMENT_INDEX: int = 0
THEOREM_INPUTS_INDEX: int = 1
THEOREM_INFERENCE_RULE_INDEX: int = 2
THEOREM_FIXED_ARITY: int = 3


class ExtraneousElementOptions(enum.Enum):
    """Options when an extraneous element is present in a collection.
    
     Attributes:
        RAISE_ERROR: Raises a ValueError when a duplicate element is found.
        STRIP: Strips duplicate elements when they are found. Keeps only the first occurrence.
    """
    RAISE_ERROR = 'RAISE_ERROR'
    STRIP = 'STRIP'


class MissingElementOptions(enum.Enum):
    """Options when an element is missing from a collection.

     Attributes:
        RAISE_ERROR: Raises a ValueError when a duplicate element is found.
        STRIP: Strips duplicate elements when they are found. Keeps only the first occurrence.
        KEEP_ORIGINAL: Keep the original letter in the string.
    """
    RAISE_ERROR = 'RAISE_ERROR'
    STRIP = 'STRIP'
    KEEP_ORIGINAL = 'KEEP_ORIGINAL'
    RETURN_DEFAULT = 'RETURN_DEFAULT'


UNICODE_SUBSCRIPT_MAP: dict[str, str] = {
    '0': '₀',
    '1': '₁',
    '2': '₂',
    '3': '₃',
    '4': '₄',
    '5': '₅',
    '6': '₆',
    '7': '₇',
    '8': '₈',
    '9': '₉',
    'a': 'ₐ',
    'e': 'ₑ',
    'h': 'ₕ',
    'i': 'ᵢ',
    'j': 'ⱼ',
    'k': 'ₖ',
    'l': 'ₗ',
    'm': 'ₘ',
    'n': 'ₙ',
    'o': 'ₒ',
    'p': 'ₚ',
    'r': 'ᵣ',
    's': 'ₛ',
    't': 'ₜ',
    'u': 'ᵤ',
    'v': 'ᵥ',
    'x': 'ₓ'
}

UNICODE_SERIF_ITALIC_REGULAR_MAP = {
    # Latin lowercase
    'a': '𝑎', 'b': '𝑏', 'c': '𝑐', 'd': '𝑑', 'e': '𝑒',
    'f': '𝑓', 'g': '𝑔', 'h': 'ℎ', 'i': '𝑖', 'j': '𝑗',
    'k': '𝑘', 'l': '𝑙', 'm': '𝑚', 'n': '𝑛', 'o': '𝑜',
    'p': '𝑝', 'q': '𝑞', 'r': '𝑟', 's': '𝑠', 't': '𝑡',
    'u': '𝑢', 'v': '𝑣', 'w': '𝑤', 'x': '𝑥', 'y': '𝑦', 'z': '𝑧',

    # Latin uppercase
    'A': '𝐴', 'B': '𝐵', 'C': '𝐶', 'D': '𝐷', 'E': '𝐸',
    'F': '𝐹', 'G': '𝐺', 'H': '𝐻', 'I': '𝐼', 'J': '𝐽',
    'K': '𝐾', 'L': '𝐿', 'M': '𝑀', 'N': '𝑁', 'O': '𝑂',
    'P': '𝑃', 'Q': '𝑄', 'R': '𝑅', 'S': '𝑆', 'T': '𝑇',
    'U': '𝑈', 'V': '𝑉', 'W': '𝑊', 'X': '𝑋', 'Y': '𝑌', 'Z': '𝑍',

    # Greek lowercase
    'α': '𝛼', 'β': '𝛽', 'γ': '𝛾', 'δ': '𝛿', 'ε': '𝜀',
    'ζ': '𝜁', 'η': '𝜂', 'θ': '𝜃', 'ι': '𝜄', 'κ': '𝜅',
    'λ': '𝜆', 'μ': '𝜇', 'ν': '𝜈', 'ξ': '𝜉', 'ο': '𝜊',
    'π': '𝜋', 'ρ': '𝜌', 'σ': '𝜎', 'τ': '𝜏', 'υ': '𝜐',
    'φ': '𝜑', 'χ': '𝜒', 'ψ': '𝜓', 'ω': '𝜔',

    # Greek uppercase
    'Α': '𝛢', 'Β': '𝛣', 'Γ': '𝛤', 'Δ': '𝛥', 'Ε': '𝛦',
    'Ζ': '𝛧', 'Η': '𝛨', 'Θ': '𝛩', 'Ι': '𝛪', 'Κ': '𝛫',
    'Λ': '𝛬', 'Μ': '𝛭', 'Ν': '𝛮', 'Ξ': '𝛯', 'Ο': '𝛰',
    'Π': '𝛱', 'Ρ': '𝛲', 'Σ': '𝛴', 'Τ': '𝛵', 'Υ': '𝛶',
    'Φ': '𝛷', 'Χ': '𝛸', 'Ψ': '𝛹', 'Ω': '𝛺',

    # Digits
    '0': '𝟢', '1': '𝟣', '2': '𝟤', '3': '𝟥', '4': '𝟦',
    '5': '𝟧', '6': '𝟨', '7': '𝟩', '8': '𝟪', '9': '𝟫',
}

UNICODE_SERIF_NORMAL_REGULAR_MAP = {
    # Latin lowercase
    'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎',
    'f': '𝚏', 'g': '𝚐', 'h': '𝚑', 'i': '𝚒', 'j': '𝚓',
    'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗', 'o': '𝚘',
    'p': '𝚙', 'q': '𝚚', 'r': '𝚛', 's': '𝚜', 't': '𝚝',
    'u': '𝚞', 'v': '𝚟', 'w': '𝚠', 'x': '𝚡', 'y': '𝚢', 'z': '𝚣',

    # Latin uppercase
    'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴',
    'F': '𝙵', 'G': '𝙶', 'H': '𝙷', 'I': '𝙸', 'J': '𝙹',
    'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽', 'O': '𝙾',
    'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃',
    'U': '𝚄', 'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉',

    # Greek lowercase
    'α': '𝛼', 'β': '𝛽', 'γ': '𝛾', 'δ': '𝛿', 'ε': '𝜀',
    'ζ': '𝜁', 'η': '𝜂', 'θ': '𝜃', 'ι': '𝜄', 'κ': '𝜅',
    'λ': '𝜆', 'μ': '𝜇', 'ν': '𝜈', 'ξ': '𝜉', 'ο': '𝜊',
    'π': '𝜋', 'ρ': '𝜌', 'σ': '𝜎', 'τ': '𝜏', 'υ': '𝜐',
    'φ': '𝜑', 'χ': '𝜒', 'ψ': '𝜓', 'ω': '𝜔',

    # Greek uppercase
    'Α': '𝚨', 'Β': '𝚩', 'Γ': '𝚪', 'Δ': '𝚫', 'Ε': '𝚬',
    'Ζ': '𝚭', 'Η': '𝚮', 'Θ': '𝚯', 'Ι': '𝚰', 'Κ': '𝚱',
    'Λ': '𝚲', 'Μ': '𝚳', 'Ν': '𝚴', 'Ξ': '𝚵', 'Ο': '𝚶',
    'Π': '𝚷', 'Ρ': '𝚸', 'Σ': '𝚺', 'Τ': '𝚻', 'Υ': '𝚼',
    'Φ': '𝚽', 'Χ': '𝚾', 'Ψ': '𝚿', 'Ω': '𝛀',

    # Digits
    '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
    '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗',
}

UNICODE_SERIF_NORMAL_BOLD_MAP = {
    # Latin lowercase
    'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞',
    'f': '𝐟', 'g': '𝐠', 'h': '𝐡', 'i': '𝐢', 'j': '𝐣',
    'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧', 'o': '𝐨',
    'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭',
    'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',

    # Latin uppercase
    'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄',
    'F': '𝐅', 'G': '𝐆', 'H': '𝐇', 'I': '𝐈', 'J': '𝐉',
    'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍', 'O': '𝐎',
    'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓',
    'U': '𝐔', 'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',

    # Greek lowercase
    'α': '𝛂', 'β': '𝛃', 'γ': '𝛄', 'δ': '𝛅', 'ε': '𝛆',
    'ζ': '𝛇', 'η': '𝛈', 'θ': '𝛉', 'ι': '𝛊', 'κ': '𝛋',
    'λ': '𝛌', 'μ': '𝛍', 'ν': '𝛎', 'ξ': '𝛏', 'ο': '𝛐',
    'π': '𝛑', 'ρ': '𝛒', 'σ': '𝛔', 'τ': '𝛕', 'υ': '𝛖',
    'φ': '𝛗', 'χ': '𝛘', 'ψ': '𝛙', 'ω': '𝛚',

    # Greek uppercase
    'Α': '𝚨', 'Β': '𝚩', 'Γ': '𝚪', 'Δ': '𝚫', 'Ε': '𝚬',
    'Ζ': '𝚭', 'Η': '𝚮', 'Θ': '𝚯', 'Ι': '𝚰', 'Κ': '𝚱',
    'Λ': '𝛬', 'Μ': '𝛭', 'Ν': '𝛮', 'Ξ': '𝛯', 'Ο': '𝛰',  # TODO: CORRECT THIS
    'Π': '𝛱', 'Ρ': '𝛲', 'Σ': '𝛴', 'Τ': '𝛵', 'Υ': '𝛶',  # TODO: CORRECT THIS
    'Φ': '𝛷', 'Χ': '𝛸', 'Ψ': '𝛹', 'Ω': '𝛺',  # TODO: CORRECT THIS

    # Digits
    '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',  # TODO: CORRECT THIS
    '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗',  # TODO: CORRECT THIS
}
