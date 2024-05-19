"""This module elaborates an axiomatization of minimal-logic.

Original axioms:
The following are the original axioms from Mancosu et al., 2021, p. 19:
 - PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)
 - PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴)
 - PL3. (𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]
 - PL4. [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)
 - PL5. 𝐵 ⊃ (𝐴 ⊃ 𝐵)
 - PL6. (𝐴 ∧ (𝐴 ⊃ 𝐵)) ⊃ 𝐵
 - PL7. 𝐴 ⊃ (𝐴 ∨ 𝐵)
 - PL8. (𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴)
 - PL9. [(𝐴 ⊃ 𝐶) ∧ (𝐵 ⊃ 𝐶)] ⊃ [(𝐴 ∨ 𝐵) ⊃ 𝐶]
 - PL10. [(𝐴 ⊃ 𝐵) ∧ (𝐴 ⊃ ¬𝐵)] ⊃ ¬𝐴

Implementation in axiomatic-system-1:
The axioms above are translated to equivalent axiomatic-system-1 transformations. This transformation is performed as
follows:
 - for all propositional variable X in the original axiom, a premise X is-a propositional-variable is elaborated,
   this prevents the usage of the transformation with inadequate variables (e.g.: natural numbers instead of
   propositional-variables),
 - the antecedent of the original axiom implication is appended as a premise of the transformation,
 - for all propositional variable X in the original axiom, a variable is appended in the transformation variables
   enumeration.

TODO: The translation of propositional implications such as the above axioms may be automated
  with a transformation. This would be interesting to facilitate the integration of other
  axiomatizations from different sources.

Bibliography:
 - Mancosu et al., 2021, p. 19.
"""

# python native modules
import typing
# punctilious modules
import axiomatic_system_1 as as1
import inference_rules_1 as ir1


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
    proposition=as1.let_x_be_a_binary_connective(rep='proposition'),
)

# retrieve vocabulary from axiomatic-system-1
is_a = as1.connectives.is_a

# retrieve vocabulary from inference-rules-1
implies = ir1.connectives.implies
land = ir1.connectives.land
lnot = ir1.connectives.lnot
proposition = ir1.connectives.proposition

with as1.let_x_be_a_variable(rep='a') as a:
    pl01_rule: as1.Transformation = as1.Transformation(premises=(
        a | is_a | proposition,
        a,
    ), conclusion=a | land | a,
        variables=(a,))
    """Original axiom: PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴). Source: (Mancosu et al., p. 19).
    """
    pl01_axiom: as1.Axiom = as1.let_x_be_an_axiom(claim=pl01_rule)
    """Original axiom: PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴). Source: (Mancosu et al., p. 19).
    """

with as1.let_x_be_a_variable(rep='a') as a, as1.let_x_be_a_variable(rep='b') as b:
    pl02_rule: as1.Transformation = as1.Transformation(premises=(
        a | is_a | proposition,
        b | is_a | proposition,
        a | land | b,
    ), conclusion=b | land | a,
        variables=(a, b,))
    """Original axiom: PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴). Source: (Mancosu et al., p. 19).
    """
    pl02_axiom: as1.Axiom = as1.let_x_be_an_axiom(claim=pl02_rule)
    """Original axiom: PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴). Source: (Mancosu et al., p. 19).
    """

with as1.let_x_be_a_variable(rep='a') as a, as1.let_x_be_a_variable(rep='b') as b, as1.let_x_be_a_variable(
        rep='c') as c:
    pl03 = as1.let_x_be_an_axiom(claim=(a | implies | b) | implies | ((a | land | c) | implies | (b | land | c)))
with as1.let_x_be_a_variable(rep='a') as a, as1.let_x_be_a_variable(rep='b') as b, as1.let_x_be_a_variable(
        rep='c') as c:
    pl04 = as1.let_x_be_an_axiom(claim=((a | implies | b) | land | (b | implies | c)) | implies | (a | implies | b))
# pl05 = as1.let_x_be_an_axiom(claim=𝐵 ⊃ (𝐴 ⊃ 𝐵))
# pl06 = (𝐴 ∧ (𝐴 ⊃ 𝐵)) ⊃ 𝐵
# pl07 = 𝐴 ⊃ (𝐴 ∨ 𝐵)
# pl08 = (𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴)
# pl09 = [(𝐴 ⊃ 𝐶) ∧ (𝐵 ⊃ 𝐶)] ⊃ [(𝐴 ∨ 𝐵) ⊃ 𝐶]
# pl10 = [(𝐴 ⊃ 𝐵) ∧ (𝐴 ⊃ ¬𝐵)] ⊃ ¬𝐴

axioms = as1.Axiomatization(axioms=(pl01_axiom, pl02_axiom, pl03, pl04,))

extended_theory = as1.Demonstration(theorems=(*axioms,))

pass
