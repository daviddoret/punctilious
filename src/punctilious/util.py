import typing
import uuid


def deduplicate_integer_sequence(t: tuple[int, ...]) -> tuple[int, ...]:
    """Given a sequence S of integers, return a sequence T such that:
     - the order and values of elements are preserved with the exception that
     - only the first occurrence of every distinct value is copied to T.

    Samples:
    (1,5,0,3,5,1,1,2) --> (1,5,0,3,2)

    :param t:
    :return:
    """
    observed = set()
    result = []
    for item in t:
        if item not in observed:
            observed.add(item)
            result.append(item)
    return tuple(result)


def data_validate_unicity(elements: typing.Iterable, raise_error_on_duplicate: bool = True) -> tuple:
    """Given some `elements`, returns a tuple of unique elements.

    :param elements:
    :param raise_error_on_duplicate:
    :return:
    """
    unique_elements = []
    for element in elements:
        if element not in unique_elements:
            unique_elements.append(element)
        elif raise_error_on_duplicate:
            raise ValueError('Duplicate elements.')
    return tuple(unique_elements)


class PunctiliousException(Exception):
    def __init__(self, message: str, **kwargs):
        self.message: str = message
        self.variables: dict = kwargs
        super().__init__(message)

    def __str__(self):
        variables: str = ' | '.join(f'`{k}` {"is" if v is None else "="} `{v!r}`' for k, v in self.variables.items())
        return f'{self.message} | {variables}'


def data_validate_uid(o: uuid.UUID) -> uuid.UUID:
    """Ensures `o` is of type `uuid.UUID`, using implicit conversion if necessary.

    :param o:
    :return:
    """
    if isinstance(o, uuid.UUID):
        return o
    elif isinstance(o, str):
        try:
            return uuid.UUID(o)
        except ValueError:
            raise PunctiliousException('`uuid.UUID` ensurance failure. `o` is not a string in valid UUID format.',
                                       o=o)
    else:
        raise PunctiliousException('`uuid.UUID` ensurance failure. `o` is not of a supported type.', o=o)
