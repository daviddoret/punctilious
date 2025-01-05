"""A catalog of fundamental connectors.

These connectors are hard-coded here as they are necessary to build the meta-language, etc."""

import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_04_formal_language as _formal_language

# hard-coded connectors
# the `tuple` connector is necessary to build complex formulas.
tuple1 = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='tuple_1', uuid='c138b200-111a-4a40-ac3c-c8afa8e615fb'))
"""The well-known connector of the `Tuple1` object.
"""

set_1 = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='set_1', uuid='8fd36cc9-8845-4cdf-ac24-1faf95ee44fc'))
"""The well-known connector of the `Set1` object.
"""

map_1 = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='map_1', uuid='2509dbf9-d636-431c-82d4-6d33b2de3bc4'))
"""The well-known connector of the `Map1` object.
"""

true2 = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='true', uuid='dde98ed2-b7e0-44b2-bd10-5f59d61fd93e'))

false2 = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='false2', uuid='ffa97ce6-e320-4e5c-86c7-d7470c2d7c94'))
