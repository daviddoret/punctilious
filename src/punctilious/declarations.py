import string
import uuid as uuid_pkg
# punctilious modules
import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_03_representation as _representation
import punctilious.pu_04_formal_language as _formal_language
import punctilious.latin_alphabet_lowercase_serif_italic as _latin_alphabet_lowercase_serif_italic
import punctilious.pu_09_formula_notations as _formula_notations

_variable_counter = 0


def declare_variable(rep: _representation.AbstractRepresentation):
    """Declare a new variable.

    A variable is a connector that takes no arguments that is designated as a variable.

    :param rep:
    :return:
    """
    # Create a new connector.
    global _variable_counter
    _variable_counter = _variable_counter + 1
    c = _formal_language.Connector(
        uid=_identifiers.create_uid(slug=f'variable_{_variable_counter}'),
        connector_representation=rep)
    return _formal_language.Formula(c=c)


def declare_function(
        rep: _representation.AbstractRepresentation | str | None = None,
        slug: _identifiers.Slug | str | None = None) -> _formal_language.Connector:
    """Declares a new function.

    TODO: NICE_TO_HAVE: Automatically increment index and index new functions for unicity.

    :param slug:
    :param rep:
    :return:
    """
    if rep is None:
        rep = _latin_alphabet_lowercase_serif_italic.f
    if isinstance(rep, str) and rep in string.ascii_lowercase:
        rep = _latin_alphabet_lowercase_serif_italic.get_letter(rep)
    uuid: uuid_pkg.UUID = uuid_pkg.uuid4()
    slug: _identifiers.Slug = _identifiers.Slug('custom_connector')
    uid: _identifiers.UniqueIdentifier = _identifiers.UniqueIdentifier(uuid=uuid, slug=slug)
    connector: _formal_language.Connector = _formal_language.Connector(
        uid=uid,
        connector_representation=rep,
        formula_representation=_formula_notations.function_formula)
    return connector
