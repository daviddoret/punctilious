"""The formal meta-language of the punctilious package.

The meta-language module requires 1) formal-language and 2) interpretation.

"""

# special features
from __future__ import annotations

# external modules
import collections.abc
import typing
import yaml

# punctilious modules
import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_04_formal_language as _formal_language
import punctilious.pu_05_interpretation as _interpretation

# hard-coded connectors
# the `tuple` connector is necessary to build complex formulas.
tuple2 = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='tuple2', uuid='c138b200-111a-4a40-ac3c-c8afa8e615fb'))


class Shape:
    """A

    Examples:

    c1(...)

    c1(c2(...))

    c1()[arity=0]
    c1(...)[arity=1]
    c1(...)[arity=2]
    c1(...)[arity=n]

    [shape.s1]:=specification
    c3([shape=s1])

    """

    pass
