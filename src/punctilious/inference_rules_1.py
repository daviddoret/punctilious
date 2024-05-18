import typing
import axiomatic_system_1 as as1


# Propositional logic vocabulary

class Connectives(typing.NamedTuple):
    implies: as1.BinaryConnective
    land: as1.BinaryConnective
    lnot: as1.BinaryConnective
    proposition: as1.SimpleObject


connectives: Connectives = Connectives(
    implies=as1.let_x_be_a_binary_connective(rep='⊃'),
    land=as1.let_x_be_a_binary_connective(rep='∧'),
    lnot=as1.let_x_be_a_unary_connective(rep='¬'),
    proposition=as1.let_x_be_a_simple_object(rep='proposition'),
)

implies = connectives.implies
is_a = as1.connectives.is_a
land = connectives.land
lnot = connectives.lnot
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
with as1.let_x_be_a_variable(rep='phi') as phi, as1.let_x_be_a_variable(rep='psi') as psi:
    adjunction_rule: as1.Transformation = as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi,
            psi,),
        conclusion=phi | land | psi,
        variables=(phi, psi,))
adjunction_axiom: as1.Axiom = as1.let_x_be_an_axiom(claim=adjunction_rule)

# Simplification inference rule, aka conjunction elimination:
#   phi ∧ psi
#   ________
#   phi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(rep='phi') as phi, as1.let_x_be_a_variable(rep='psi') as psi:
    simplification_1_rule: as1.Transformation = as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | land | psi,),
        conclusion=phi,
        variables=(phi, psi,))
simplification_1_axiom: as1.Axiom = as1.let_x_be_an_axiom(claim=simplification_1_rule)

# Simplification inference rule, aka conjunction elimination:
#   phi ∧ psi
#   ________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(rep='phi') as phi, as1.let_x_be_a_variable(rep='psi') as psi:
    simplification_2_rule: as1.Transformation = as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | land | psi,),
        conclusion=psi,
        variables=(phi, psi,))
simplification_2_axiom: as1.Axiom = as1.let_x_be_an_axiom(claim=simplification_2_rule)

# Modus ponens inference rule:
#   phi --> psi
#   phi
#   ___________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(rep='phi') as phi, as1.let_x_be_a_variable(rep='psi') as psi:
    modus_ponens_rule: as1.Transformation = as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | land | psi,
            phi),
        conclusion=psi,
        variables=(phi, psi,))
modus_ponens_axiom: as1.Axiom = as1.let_x_be_an_axiom(claim=modus_ponens_rule)

inference_rules = as1.Axiomatization(axioms=(
    adjunction_axiom,
    simplification_1_axiom,
    simplification_2_axiom,
    modus_ponens_axiom,))
