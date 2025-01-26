import re

import punctilious.pu_03_representation as _rep


def convert_friendly_string_to_variable_name(variable_name: str, font: _rep.Font = None):
    """Receives a string of the form `abc123` where:
     - `abc` is a series of one or more alphabetic ASCII characters,
     - `123` is a series of ASCII digit characters,
    and returns an AbstractRepresentation of a variable name of the form `abc_{123}`.

    :param variable_name:
    :param font:
    :return:
    """
    # Regular expression pattern: ^([a-zA-Z])(\d*)$
    pattern = r'([a-zA-Z]+)(\d*)'
    match = re.fullmatch(pattern, variable_name)
    if match:
        alphabetic_part = match.group(1)  # The first capture group (alphabetic character)
        digit_part = match.group(2)  # The second capture group (digits, or an empty string if none)
        return alphabetic_part, digit_part
    else:
        raise ValueError("Input string does not match the expected format.")
