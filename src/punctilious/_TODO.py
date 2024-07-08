"""

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

TODO: IDEA: Algorithm class.
    General idea: an algorithm is an implementation in a programming language,
    here python, of a (determinist???) algorithm that acts like an inference-rule,
    i.e. given a number of arguments (that must be valid-statements in the theory),
    generates a new valid-statement in the theory.


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
