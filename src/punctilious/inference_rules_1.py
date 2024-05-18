import typing
import sys

import punctilious as pu

module_state = sys.modules[__name__]


# Propositional logic vocabulary

class Connectives(typing.NamedTuple):
    implies: pu.as1.BinaryConnective
    land: pu.as1.BinaryConnective
    lnot: pu.as1.BinaryConnective
    proposition: pu.as1.SimpleObject


# TODO: module_state: Extend this approach to all global variables
if hasattr(module_state, 'connectives'):
    connectives: Connectives = module_state.connectives
else:
    connectives: Connectives = Connectives(
        implies=pu.as1.let_x_be_a_binary_connective(rep='⊃'),
        land=pu.as1.let_x_be_a_binary_connective(rep='∧'),
        lnot=pu.as1.let_x_be_a_unary_connective(rep='¬'),
        proposition=pu.as1.let_x_be_a_simple_object(rep='proposition'),
    )

implies = connectives.implies
is_a = pu.as1.connectives.is_a
land = connectives.land
lnot = connectives.lnot

if hasattr(module_state, 'proposition'):
    proposition = module_state.event_types
else:
    proposition = connectives.proposition

# Basic inference rules

# Adjunction inference rule, aka conjunction introduction:
#   phi
#   psi
#   ________
#   phi ∧ psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with pu.as1.let_x_be_a_variable(rep='phi') as phi, pu.as1.let_x_be_a_variable(rep='psi') as psi:
    adjunction_rule: pu.as1.Transformation = pu.as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi,
            psi,),
        conclusion=phi | land | psi,
        variables=(phi, psi,))
adjunction_axiom: pu.as1.Axiom = pu.as1.let_x_be_an_axiom(claim=adjunction_rule)

# Simplification inference rule, aka conjunction elimination:
#   phi ∧ psi
#   ________
#   phi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with pu.as1.let_x_be_a_variable(rep='phi') as phi, pu.as1.let_x_be_a_variable(rep='psi') as psi:
    simplification_1_rule: pu.as1.Transformation = pu.as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | land | psi,),
        conclusion=phi,
        variables=(phi, psi,))
simplification_1_axiom: pu.as1.Axiom = pu.as1.let_x_be_an_axiom(claim=simplification_1_rule)

# Simplification inference rule, aka conjunction elimination:
#   phi ∧ psi
#   ________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with pu.as1.let_x_be_a_variable(rep='phi') as phi, pu.as1.let_x_be_a_variable(rep='psi') as psi:
    simplification_2_rule: pu.as1.Transformation = pu.as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | land | psi,),
        conclusion=psi,
        variables=(phi, psi,))
simplification_2_axiom: pu.as1.Axiom = pu.as1.let_x_be_an_axiom(claim=simplification_2_rule)

# Modus ponens inference rule:
#   phi --> psi
#   phi
#   ___________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with pu.as1.let_x_be_a_variable(rep='phi') as phi, pu.as1.let_x_be_a_variable(rep='psi') as psi:
    modus_ponens_rule: pu.as1.Transformation = pu.as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | land | psi,
            phi),
        conclusion=psi,
        variables=(phi, psi,))
modus_ponens_axiom: pu.as1.Axiom = pu.as1.let_x_be_an_axiom(claim=modus_ponens_rule)

inference_rules = pu.as1.Axiomatization(axioms=(
    adjunction_axiom,
    simplification_1_axiom,
    simplification_2_axiom,
    modus_ponens_axiom,))
