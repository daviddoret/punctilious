"""

TODO: Consider using a three-valued logic:
 - P is true
 - or P is false
 - or P is not decidable in this axiomatization

TODO: Question: How could we introduce a new symbol or connective in a theory?
    For this we need a special "instruction" or proto-derivation.
    Something like: Let S be a new symbol/connective or: (s is-a new-symbol).
    And we must be able to derive that two symbols introduced in a theory
    are necessarily unequal, or not symbol-equivalent.
    Should we use the target theory for that?
    Or a special-purpose meta-theory?
    Side note: this allows the development of a theory of connectives.
    Possibility:
        (x is-a new-connective ^ x is-a propositional-variable)
        or simply:
        (x is-a propositional-variable) with new-connective-variable x

TODO: Algorithm class.
    General idea: an algorithm is an implementation in a programming language,
    here python, of a (determinist???) algorithm that acts like an inference-rule,
    i.e. given a number of arguments (that must be valid-statements in the theory),
    generates a new valid-statement in the theory.

TODO: Implement sub-theory
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


TODO: AccretingTheory class
    An accreting theory is a sequence of theories T0, T1, T2, ..., Tn, such that
    T0 is a theory, and Tn+1 is a theory that is Tn with one additional derivation.
    This would allow to keep a python-object as a reference object with an inner
    Theory instance.
    Would this structure be necessary to friendly manage meta- and sub-theories?


"""
