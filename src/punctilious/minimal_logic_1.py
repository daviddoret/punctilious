import typing
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

implies = connectives.implies
is_a = as1.connectives.is_a
land = connectives.land
lnot = connectives.lnot
proposition = connectives.proposition

# PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)
with as1.Variable(rep='a') as a:
    pl01_claim = as1.let_x_be_a_transformation(premises=(a,), conclusion=a | land | a, variables=(a,))
    pl01 = as1.let_x_be_an_axiom(claim=pl01_claim)
with as1.Variable(rep='a') as a, as1.Variable(rep='b') as b:
    pl02 = as1.let_x_be_an_axiom(claim=(a | land | b) | implies | (b | land | a))
with as1.Variable(rep='a') as a, as1.Variable(rep='b') as b, as1.Variable(rep='c') as c:
    pl03 = as1.let_x_be_an_axiom(claim=(a | implies | b) | implies | ((a | land | c) | implies | (b | land | c)))
with as1.Variable(rep='a') as a, as1.Variable(rep='b') as b, as1.Variable(rep='c') as c:
    pl04 = as1.let_x_be_an_axiom(claim=((a | implies | b) | land | (b | implies | c)) | implies | (a | implies | b))
# pl05 = as1.let_x_be_an_axiom(claim=𝐵 ⊃ (𝐴 ⊃ 𝐵))
# pl06 = (𝐴 ∧ (𝐴 ⊃ 𝐵)) ⊃ 𝐵
# pl07 = 𝐴 ⊃ (𝐴 ∨ 𝐵)
# pl08 = (𝐴 ∨ 𝐵) ⊃ (𝐵 ∨ 𝐴)
# pl09 = [(𝐴 ⊃ 𝐶) ∧ (𝐵 ⊃ 𝐶)] ⊃ [(𝐴 ∨ 𝐵) ⊃ 𝐶]
# pl10 = [(𝐴 ⊃ 𝐵) ∧ (𝐴 ⊃ ¬𝐵)] ⊃ ¬𝐴

axioms = as1.Axiomatization(e=(pl01, pl02, pl03, pl04,))
print(axioms)

axioms = as1.Demonstration(e=(pl01, pl02, pl03, pl04,))
print(axioms)

red = as1.let_x_be_a_simple_object(rep='red')
green = as1.let_x_be_a_simple_object(rep='green')
blue = as1.let_x_be_a_simple_object(rep='blue')
t1 = as1.let_x_be_an_axiom(claim=red)
test2 = red | implies | green
t2 = as1.let_x_be_an_axiom(claim=test2)
pbi = as1.TheoremByInference(claim=green, i=as1.Inference(p=(red, red | implies | green,), f=modus_ponens))
print(pbi)

red = as1.let_x_be_a_simple_object(rep='red')
green = as1.let_x_be_a_simple_object(rep='green')
blue = as1.let_x_be_a_simple_object(rep='blue')
t1 = as1.let_x_be_an_axiom(claim=red)
pbi = as1.TheoremByInference(claim=red | land | red, i=as1.Inference(p=(red,), f=pl01.claim))
print(pbi)

pass
