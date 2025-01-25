import punctilious.pu_03_representation as _rep


def ensure_variable_name(variable_name: object):
    """Receives a

    :param variable_name:
    :return:
    """
    # Regular expression pattern: ^([a-zA-Z])(\d*)$
    pattern = r'^([a-zA-Z])(\d*)$'
    match = re.fullmatch(pattern, s)
    if match:
        letter = match.group(1)  # The first capture group (alphabetic character)
        number = match.group(2)  # The second capture group (digits, or an empty string if none)
        return letter, number
    else:
        raise ValueError("Input string does not match the expected format.")
