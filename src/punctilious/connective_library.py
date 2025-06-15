"""A catalogue of well-known connectives.

"""

import connective

# propositional logic
is_a_propositional_logic_variable: connective.Connective = connective.Connective("is-a-propositional-variable",
                                                                                 uid="1dde6cdb-8268-4586-bfdb-5531baee5b6f")
"""Connective used to formally declare variables of the propositional-logic axiomatic calculi.

References:
- Mancosu 2021, definition 2.1 (p. 13).
"""
is_a_propositional_logic_formula: connective.Connective = connective.Connective("is-a-propositional-variable",
                                                                                uid="1dde6cdb-8268-4586-bfdb-5531baee5b6f")
"""Connective used to formally declare formulas of the propositional-logic axiomatic calculi.

References:
- Mancosu 2021, definition 2.2 (p. 14).
"""

# general logic
biconditional: connective.Connective = connective.Connective("if-and-only-if",
                                                             uid="7db6be5a-3687-4ab3-aff6-b49ce06fd80a")
conjunction: connective.Connective = connective.Connective("and", uid="2d308177-5e30-4209-86ff-f844620416e6")
disjunction: connective.Connective = connective.Connective("or", uid="cdb13c92-0203-478f-93f3-d2a582aa0d42")
material_implication: connective.Connective = connective.Connective("implies",
                                                                    uid="b9b05d7b-97a7-4ebe-8e29-a1cbbcf98be6")
negation: connective.Connective = connective.Connective("not", uid="587a7008-ecae-4b20-ac8b-ceb49582db72")
if_and_only_if: connective.Connective = biconditional
implies: connective.Connective = material_implication
land: connective.Connective = conjunction
lnot: connective.Connective = negation
lor: connective.Connective = disjunction

# natural numbers
zero: connective.Connective = connective.Connective("0", uid="e98ed013-f538-4b1e-84e6-97aa54e51d00")
one: connective.Connective = connective.Connective("1", uid="cbf86ae3-1ada-43ee-a34e-d0abee0978fd")
two: connective.Connective = connective.Connective("2", uid="dd5d79e7-a3a7-4e36-a50a-9a1ccd0e9e60")
three: connective.Connective = connective.Connective("3", uid="028932f3-6179-4eb7-a788-20924999e5c8")
four: connective.Connective = connective.Connective("4", uid="fd58f749-7b6f-4de6-ba42-79c94cca9d8b")
five: connective.Connective = connective.Connective("5", uid="4844cf98-c65d-4f8c-9faa-d034d38aa9b5")
six: connective.Connective = connective.Connective("6", uid="6545a912-1fe3-493c-842c-601c423f9392")
seven: connective.Connective = connective.Connective("7", uid="b0bd6cfb-ae0e-4533-9024-32418288c0e1")
eight: connective.Connective = connective.Connective("8", uid="4311ae18-67d7-4d1f-aa8b-76638710aedb")
nine: connective.Connective = connective.Connective("9", uid="9f931933-649e-42d8-8a7b-8c19ba7fe89e")

# arithmetic operators
addition: connective.Connective = connective.Connective("0", uid="3ed8a142-17a1-4799-b1e1-7061b07a1c36")
division: connective.Connective = connective.Connective("0", uid="167a8e01-8f9d-4f93-a004-bf1ae96fe335")
exponentiation: connective.Connective = connective.Connective("0", uid="c0ed8133-ea0e-4d23-939f-b308b6cc5cba")
multiplication: connective.Connective = connective.Connective("0", uid="2cd26a6f-15af-4529-b37c-71afab1699de")
substraction: connective.Connective = connective.Connective("0", uid="90c1ae38-5bc2-4917-ac66-5d03217055b6")
plus: connective.Connective = addition
minus: connective.Connective = substraction
power: connective.Connective = exponentiation
times: connective.Connective = multiplication

# set theory
set_by_extension: connective.Connective = connective.Connective("set", uid="0f3d1ff1-e7e8-4b9f-9885-c6a9241dc1af")
