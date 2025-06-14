"""A catalogue of well-known connectors.

"""

import connector

# logic
biconditional: connector.Connector = connector.Connector("if-and-only-if", uid="7db6be5a-3687-4ab3-aff6-b49ce06fd80a")
conjunction: connector.Connector = connector.Connector("and", uid="2d308177-5e30-4209-86ff-f844620416e6")
disjunction: connector.Connector = connector.Connector("or", uid="cdb13c92-0203-478f-93f3-d2a582aa0d42")
material_implication: connector.Connector = connector.Connector("implies", uid="b9b05d7b-97a7-4ebe-8e29-a1cbbcf98be6")
negation: connector.Connector = connector.Connector("not", uid="587a7008-ecae-4b20-ac8b-ceb49582db72")
if_and_only_if: connector.Connector = biconditional
implies: connector.Connector = material_implication
land: connector.Connector = conjunction
lnot: connector.Connector = negation
lor: connector.Connector = disjunction

# natural numbers
zero: connector.Connector = connector.Connector("0", uid="e98ed013-f538-4b1e-84e6-97aa54e51d00")
one: connector.Connector = connector.Connector("0", uid="cbf86ae3-1ada-43ee-a34e-d0abee0978fd")
two: connector.Connector = connector.Connector("0", uid="dd5d79e7-a3a7-4e36-a50a-9a1ccd0e9e60")
three: connector.Connector = connector.Connector("0", uid="028932f3-6179-4eb7-a788-20924999e5c8")

# arithmetic operators
addition: connector.Connector = connector.Connector("0", uid="3ed8a142-17a1-4799-b1e1-7061b07a1c36")
division: connector.Connector = connector.Connector("0", uid="167a8e01-8f9d-4f93-a004-bf1ae96fe335")
exponentiation: connector.Connector = connector.Connector("0", uid="c0ed8133-ea0e-4d23-939f-b308b6cc5cba")
multiplication: connector.Connector = connector.Connector("0", uid="2cd26a6f-15af-4529-b37c-71afab1699de")
substraction: connector.Connector = connector.Connector("0", uid="90c1ae38-5bc2-4917-ac66-5d03217055b6")
plus: connector.Connector = addition
minus: connector.Connector = substraction
power: connector.Connector = exponentiation
times: connector.Connector = multiplication
