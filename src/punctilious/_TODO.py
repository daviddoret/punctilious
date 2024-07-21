"""

TODO: Change shape "(inference-rule) follows-from inference-rule" for derivations, to "is_axiomatic_rule(inference-rule)".

TODO: Change shape "(statement) follows-from axiom" for derivations, to "is_axiom(axiom)".

TODO: Change shape "(statement) follows-from (theorem-derivation)" for derivations, to "TBD???".

TODO: Consider meta connective "symbol(phi)" which returns the unique symbol of the root connective of phi.
    This can be leveraged to meta compare the connectives of two formulas, with symbol(phi)=symbol(psi).

TODO: Implement predicative-connectives. these are connectives that generate propositions.
    this will facilitate auto-derivation of is-a proposition.

TODO: When a transformation creates new objects, it is not deterministic.
    To verify the validity of derivations a posterio,
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

TODO: IDEA: Develop a three-valued logic:
 - P is true
 - or P is false
 - or P is not decidable in this axiomatization

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


TODO: AccretingTheory class ??? is this a good idea ???
    An accreting theory is a sequence of theories T0, T1, T2, ..., Tn, such that
    T0 is a theory, and Tn+1 is a theory that is Tn with one additional derivation.
    This would allow to keep a python-object as a reference object with an inner
    Theory instance.
    Would this structure be necessary to friendly manage meta- and sub-theories?


TODO: is-a-sub-theory-of (subset of axiomatization)

TODO: meta-theorem 1:
 if derivation d in t1 and t1 is-a-sub-theory-of t2, then d is valid in t1.

"""
