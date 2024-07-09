"""

TODO: Implement strict connectives check in coerce_functions. To do this, we must better manage
    python-class inheritance (because this changes the connectives). Start systematically with
    python-classes that are not inherited.
        Map: OK


TODO: Replace the follows-from scheme?, e.g. inference-rule(blablabla), axiom(blablabla).
    Put more thought into this before changing anything, because we need to model Derivation.
    Distinguish clearly the predicate-function is-a-well-formed-axiom(a) from the
    derivation-function which implies that the axiom is in the current theory,
    i.e. a follows-from axiom.

TODO: Introduce canonical conversions (formula to enumeration, formula to tuple, etc.).

TODO: KEY QUALITY CHECK: In both the Theorem.__init__ or __new__ and in the is_well_formed_theorem function,
    check that newly declared objects are not present in any precedent formula in the theory!

TODO: IDEA: Develop a three-valued logic:
 - P is true
 - or P is false
 - or P is not decidable in this axiomatization

TODO: Implement Predicates.

TODO: Determine how to express predicates or classes over connectives,
    example: if blue is a predicate, to express formulas such as blue(sky),
    the truth that blue is a predicate should be expressible for example as predicate(blue).

TODO: Implement index constants on all formula classes, e.g. Inference. Then replace
    all hard-coded index positions.

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
    In the parent theory:
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


"""
