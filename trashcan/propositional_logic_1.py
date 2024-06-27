import typing
import axiomatic_system_1 as as1


class Connectives(typing.NamedTuple):
    land: as1.BinaryConnective
    falsehood: as1.SimpleObject
    proposition: as1.SimpleObject
    equivalence: as1.BinaryConnective
    truth: as1.SimpleObject


connectives: Connectives = Connectives(
    land=as1.let_x_be_a_binary_connective(rep='∧'),
    equivalence=as1.let_x_be_a_binary_connective(rep='~propositional'),
    falsehood=as1.let_x_be_a_simple_object(formula_typesetter='falsehood'),
    proposition=as1.let_x_be_a_simple_object(formula_typesetter='proposition'),
    truth=as1.let_x_be_a_simple_object(formula_typesetter='truth'),
)

is_a = as1.connectives.is_a
equivalence = connectives.equivalence
proposition = connectives.proposition
truth = connectives.truth
land = connectives.land

p = as1.let_x_be_a_variable(formula_typesetter='p')
q = as1.let_x_be_a_variable(formula_typesetter='q')
premises = (p | is_a | proposition,
            q | is_a | proposition,
            p | equivalence | truth,
            q | equivalence | truth)
conclusion = p | land | q
t = as1.Transformation(premises=premises, conclusion=conclusion, variables=(p, q,))

r = as1.let_x_be_a_variable(formula_typesetter='r')
s = as1.let_x_be_a_variable(formula_typesetter='s')
psi1 = r | is_a | proposition
psi2 = s | is_a | proposition
psi3 = r | equivalence | truth
psi4 = s | equivalence | truth

omega = t.apply_transformation(arguments=(psi1, psi2, psi3, psi4,))
pass
