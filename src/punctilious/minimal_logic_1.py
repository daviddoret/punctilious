import typing
import axiomatic_system_1 as as1


class Connectives(typing.NamedTuple):
    implies: as1.BinaryConnective
    land: as1.SimpleObject
    lnot: as1.SimpleObject


connectives: Connectives = Connectives(
    implies=as1.let_x_be_a_binary_connective(rep='⊃'),
    land=as1.let_x_be_a_binary_connective(rep='∧'),
    lnot=as1.let_x_be_a_unary_connective(rep='¬')
)

implies = connectives.implies
land = connectives.land
lnot = connectives.lnot

a = as1.let_x_be_a_variable(rep='A')
b = as1.let_x_be_a_variable(rep='B')
c = as1.let_x_be_a_variable(rep='C')

pl01 = as1.ProofByPostulation(claim=a | implies | (a | land | a))
pl02 = as1.ProofByPostulation(claim=(a | land | b) | implies | (b | land | a))
pl03 = as1.ProofByPostulation(claim=(a | implies | b) | implies | ((a | land | c) | implies | (b | land | c)))
pl04 = a | implies | (a | land | a)
pl05 = a | implies | (a | land | a)
pl06 = a | implies | (a | land | a)
pl07 = a | implies | (a | land | a)
pl08 = a | implies | (a | land | a)
pl09 = a | implies | (a | land | a)
pl10 = a | implies | (a | land | a)

axioms = as1.Axiomatization(e=(pl01, pl02, pl03,))
print(axioms)

axioms = as1.Demonstration(e=(pl01, pl02, pl03,))
print(axioms)

pass
