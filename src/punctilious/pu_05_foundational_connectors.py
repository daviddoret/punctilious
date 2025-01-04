"""A catalog of fundamental connectors.

These connectors are hard-coded here as they are necessary to build the meta-language, etc."""

import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_04_formal_language as _formal_language

# hard-coded connectors
# the `tuple` connector is necessary to build complex formulas.
tuple2 = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='tuple2', uuid='c138b200-111a-4a40-ac3c-c8afa8e615fb'))

set_defined_by_extension = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='set_defined_by_extension', uuid='8fd36cc9-8845-4cdf-ac24-1faf95ee44fc'))

true2 = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='true', uuid='dde98ed2-b7e0-44b2-bd10-5f59d61fd93e'))

false2 = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='false2', uuid='ffa97ce6-e320-4e5c-86c7-d7470c2d7c94'))
