import punctilious as pu
from punctilious import pu_06_meta_language as mt

# declaration of the propositional-logic meta-theory

# connectors

# meta-theory predicates
is_a_well_formed_propositional_variable = object()
is_a_well_formed_propositional_logic_formula = object()

# theory connectors
negation = object()
conjunction = object()
disjunction = object()
implication = object()

# shortcuts
lnot = negation
land = conjunction
lor = disjunction
implies = implication

# inference-rules

"""
Definition 2.2. The formulas are defined as follows: 
3. Extremal clause: Nothing else is a formula. 

Remark. The letters “𝐴” and “𝐵” (and later “𝐶”, “𝐷”, . . . ) are not symbols of our propositional calculus. 
Rather, we use them in our discussion to stand in for arbitrary formulas. 
Such schematic letters are called metavariables, 
since they are variables we use in the metalanguage in which we talk about symbols, formulas, derivations, etc. 
Later on we will also use metavariables for other symbols and expressions.

Refefence:
"""

a = mt.declare_metavariable()
b = mt.declare_metavariable()

# 1. Basis clause: Each propositional variable is a formula (called an atomic formula)
ir_2_2_1a = mt.declare_natural_inference_rule(
    declarations=(a,),  # allows to make declarations of new objects in the theory
    variables=(),
    premises=(),
    conclusion=is_a_well_formed_propositional_variable(a)
)
ir_2_2_1b = mt.declare_natural_inference_rule(
    variables=(a,),
    premises=(is_a_well_formed_propositional_variable(a),),
    conclusion=is_a_well_formed_propositional_logic_formula()
)

# 2. Inductive clause: If 𝐴 and 𝐵 are formulas so are ¬𝐴, (𝐴 ∧ 𝐵), (𝐴 ∨ 𝐵), and (𝐴 ⊃ 𝐵).
ir_2_2_2a = mt.declare_natural_inference_rule(
    variables=(a, b,),
    premises=(is_a_well_formed_propositional_logic_formula(a),),
    conclusion=is_a_well_formed_propositional_logic_formula(lnot(a))
)
ir_2_2_2b = mt.declare_natural_inference_rule(
    variables=(a, b,),
    premises=(is_a_well_formed_propositional_logic_formula(a),
              is_a_well_formed_propositional_logic_formula(b)),
    conclusion=is_a_well_formed_propositional_logic_formula(a | land | b)
)
ir_2_2_2c = mt.declare_natural_inference_rule(
    variables=(a, b,),
    premises=(is_a_well_formed_propositional_logic_formula(a),
              is_a_well_formed_propositional_logic_formula(b)),
    conclusion=is_a_well_formed_propositional_logic_formula(a | lor | b)
)
ir_2_2_2d = mt.declare_natural_inference_rule(
    variables=(a, b,),
    premises=(is_a_well_formed_propositional_logic_formula(a),
              is_a_well_formed_propositional_logic_formula(b)),
    conclusion=is_a_well_formed_propositional_logic_formula(a | implies | b)
)
