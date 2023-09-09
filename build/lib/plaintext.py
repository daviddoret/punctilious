import typing
import unidecode


def prioritize_value(*args) -> typing.Any:
    """Return the first non-None object in ⌜*args⌝."""
    for a in args:
        if a is not None:
            return a
    return None


def force_plaintext(s: (None, str), empty_if_none: (None, bool) = None) -> str:
    """In the context of the Punctilious package, plaintext is a subset
    of ASCII composed of well-known alphanumeric and punctuation characters.
    """
    if s is None:
        empty_if_none = prioritize_value(empty_if_none, False)
        return '' if empty_if_none else None
    # Using unidecode() is temporary solution,
    # it leads to some undesirable mappings (e.g. ¬ is mapped to !).
    # TODO: Consider implementing a custom mapper,
    #  optimized for mathematical usage.
    s = unidecode.unidecode(s)
    return s


class Plaintext(str):
    def __new__(cls, s: (None, str), empty_if_none: (None, bool) = None):
        empty_if_none = prioritize_value(empty_if_none, False)
        if s is None and not empty_if_none:
            return None
        s = force_plaintext(s=s, empty_if_none=empty_if_none)
        instance = super().__new__(cls, s)
        return instance
