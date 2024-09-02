"""

TODO: Implement a new TransformationByExternalAlgorithm
    Input: a tuple of input values
    Output: a formula
    Align with the ABC class for transformations, some rework will be necessary

TODO: We need now some basic predicate logic:
    meta-theory algos such as is-well-formed-x(y) must be understood as well-formed propositions.


TODO: Use WellFormedProposition in WellFormedInferenceRule, i.e. premises must be propositions, and conclusion.

TODO: Develop is_axiomatic_base and get_axiomatic_base()

TODO: Develop is_a_component_of(T) from is_a_valid_proposition_in(T)

TODO: Check then remove argument `a` in inference. Should be useless now.

TODO: Develop native predicates. To keep things simple, start with the specialized
    unary predicate P(phi) where P is any connector. Then link the external resolution
    algorithm to the connector as a decoration. Every predicate should infer:
        (is-predicate(P(phi))
    ...and without any guarantee of success:
        (is-valid(P(phi)))
        "is-valid" or "is-true", not sure.

***************



TODO: Implement monotonicity, probably as an inference-rule until we prove it with the meta-theory once
    the meta-theory will be rich enough:
    If 𝛤 ⊢ 𝐴 and 𝛤 ⊆ 𝛤★, then 𝛤★ ⊢ 𝐴.15 In particular, if 𝛤 is empty, then 𝐴 can also be proved using any number
    of additional assumptions.
    (...)
    This property is called monotonicity. It holds for all the logics we will investigate in this book. There are
    logics in which this property does not hold (non-monotonic logics), however.
    (ref: Mancosu 2021, p. 25)


TODO: Change shape "Derivation(inference-rule, inference-rule)" for derivations,
    to something like "is_axiomatic_rule(inference-rule)" to make it a proposition as well.
    Like this, is_axiomatic_rule would be a proposition similarly to axioms and theorems,
    even though it is a bit of a meta-statement.

TODO: Consider meta connective "symbol(phi)" which returns the unique symbol of the root connective of phi.
    This can be leveraged to meta compare the connectives of two formulas, with symbol(phi)=symbol(psi).

TODO: Consider fundamental inference-rule: premises=(), conjecture=s is a (new) symbol, declarations={s}.
    This would allow the declaration of the connective symbols.
    We still don't have access to any real symbol or representation, but just of the concept
    of a symbol and that symbol being unique, i.e. distinct from all other inferred symbols.

TODO: When a transformation creates new objects, it is not deterministic.
    To verify the validity of derivations a posteriori,
    we must be able to re-map the new objects to the variables.
    i think this requires a single conclusion in algorithmic transformations.
    which would mean we need to double them all the time to have both P and not(P).

TODO: Replace the follows-from scheme?, e.g. inference-rule(blablabla), axiom(blablabla).
    Put more thought into this before changing anything, because we need to model Derivation.
    Distinguish clearly the predicate-function is-a-well-formed-axiom(a) from the
    derivation-function which implies that the axiom is in the current theory,
    i.e. a follows-from axiom.

TODO: KEY QUALITY CHECK: In both the Theorem.__init__ or __new__ and in the is_well_formed_theorem function,
    check that newly declared objects are not present in any precedent formula in the theory!


****** PREDICATES

TODO: Implement predicative-connectives or simply predicates. these are connectives that generate propositions.
    this will facilitate auto-derivation of is-a proposition.

TODO: Implement Predicates. These are n-ary connectives (we can start with unary connectives)
    that are linked to an inference-rule that returns true or false.

TODO: Determine how to express predicates or classes over connectives,
    example: if blue is a predicate, to express formulas such as blue(sky),
    the truth that blue is a predicate should be expressible for example as predicate(blue).

TODO: KEY FEATURE: Implement sub-theory
    In the parent theory:
        t1
            [1] ...
            [2] ...
            ...
            [n] Let t2 be-a sub-theory
            [n+1] h1.01 (d1) is a derivation of t2
            [n+2] h1.02 (d2) is a derivation of t2

TODO: Implement analysis of theory consistency
    In the parent theory:
        t1
            [1] ...
            [2] ...
            ...
            [n] Let t2 be-a sub-theory
            [n+1] h1.01 (d1) is a derivation of t2
            [n+2] h1.02 (d2) is a derivation of t2
    And then prove inconsistency of h1:
            [m+1] (p) is valid in h1
            [m+2] (not p) is valid in h1
            [m+3] h1 is inconsistent

TODO: Implement hypothesis
    In a theory:
        t1
            [1] ...
            [2] ...
            ...
            [n] Let h1 be-an hypothesis with assumption phi
            [n+1] h1.01 (d1) is a derivation of h1
            [n+2] h1.02 (d2) is a derivation of h1
    And then prove inconsistency of h1:
            [m] (p) is valid in h1
            [m+1] (not p) is valid in h1
            [m+2] h1 is inconsistent
    And then prove not phi:
            [q] not(phi)

TODO: is-a-sub-theory-of (subset of axiomatization)

TODO: meta-theorem 1:
 if derivation d in t1 and t1 is-a-sub-theory-of t2, then d is valid in t1.

NIVE-TO-HAVES

TODO: NICE-TO-HAVE: Consider a new class WFTupleExtensible which supports the extends(...) elements.
    From which WFEnumerationExtensible follows.
    And finally all theoretical contexts.


TODO: IDEA: Develop a three-valued logic:
 - P is true
 - or P is false
 - or P is not decidable in this axiomatization

TODO: When typesetting tuples or enumerations or theory contexts or ...
    when multiple is_a_predicate are listed consecutively, like:
    ⌜𝐴⌝ is a well-formed proposition, ⌜𝐵⌝ is a well-formed proposition
    group them together like this:
    ⌜𝐴⌝, ⌜𝐵⌝ are well-formed propositions



QUESTIONS

TODO: QUESTION: AccretingTheory class ??? is this a good idea ???
    An accreting theory is a sequence of theories T0, T1, T2, ..., Tn, such that
    T0 is a theory, and Tn+1 is a theory that is Tn with one additional derivation.
    This would allow to keep a python-object as a reference object with an inner
    Theory instance.
    Would this structure be necessary to friendly manage meta- and sub-theories?


"""
