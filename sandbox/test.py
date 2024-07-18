@staticmethod
def _data_validation(c: Connective, t: FlexibleTheory | None = None, d: FlexibleEnumeration = None) -> tuple[
    Connective, Enumeration]:
    """

    :param t:
    :param d:
    :return:
    """
    global _connectives
    c: Connective = _connectives.theory_formula
    if t is not None:
        t: Theory = coerce_theory(t=t, interpret_none_as_empty=False, canonical_conversion=True)
    d: Enumeration = coerce_enumeration(e=d, strip_duplicates=True, canonic_conversion=True,
                                        interpret_none_as_empty=True)
    is_valid, v, u = would_be_valid_derivations_in_theory(v=d, u=t, raise_error_if_false=True)
    d_old = union_enumeration(phi=v, psi=u, strip_duplicates=True)
    d = Enumeration(e=(*v, *u,))
    return c, d


def would_be_valid_derivations_in_theory(v: FlexibleTheory, u: FlexibleEnumeration,
                                         raise_error_if_false: bool = False) -> tuple[
    bool, Enumeration | None, Enumeration | None]:
    """Given an enumeration of presumably verified derivations "v" (e.g.: the derivation sequence of a theory "t"),
    and an enumeration of unverified derivations "u" (e.g.: whose elements are not (yet) effective
    theorems of "t"), returns True if a theory would be well-formed if it was composed of
    derivations "u" appended to derivations "v", or False if it would not.

    This function is useful to test whether some derivations will pass well-formedness validation before
    attempting to effectively derive it.

    :param v: An enumeration of presumably verified derivations.
    :param u: An enumeration of unverified derivations.
    :param raise_error_if_false:
    :return: A triple `(b, v′, u′)` where:
     `b` is `True` if all derivations in `u` would be valid, `False` otherwise,
     `v′` = `v` with duplicates stripped out if `b` is `True`, `None` otherwise,
     `u′` = `(u \ v)` with duplicates stripped out if `b` is `True`, `None` otherwise.
    """
    u: Enumeration = coerce_enumeration(e=u, strip_duplicates=True, interpret_none_as_empty=True,
                                        canonic_conversion=True)
    v: Enumeration = coerce_enumeration(e=v, strip_duplicates=True, interpret_none_as_empty=True,
                                        canonic_conversion=True)

    # Consider only derivations that are not elements of the verified enumeration.
    # In effect, a derivation sequence must contain unique derivations under enumeration-equivalence.
    u: Enumeration = difference_enumeration(phi=u, psi=v, strip_duplicates=True, interpret_none_as_empty=True,
                                            canonic_conversion=True)

    # Create a complete enumeration "c" composed of derivations "u" appended to derivations "v",
    # getting rid of duplicates if any in the process.
    c: Enumeration = union_enumeration(phi=v, psi=u, strip_duplicates=True)

    # Put aside the index from which the proofs of derivations have not been verified.
    verification_threshold: int = len(v)

    # Coerce all enumeration elements to axioms, inference-rules, and theorems.
    coerced_elements: list = [coerce_derivation(d=d) for d in iterate_enumeration_elements(e=c)]
    c: Enumeration = Enumeration(e=coerced_elements)

    # Iterate through all index positions of derivations for which the proofs must be verified.
    for index in range(verification_threshold, len(c)):

        # Retrieve the derivation whose proof must be verified.
        d: Derivation = c[index]

        # Retrieve the proposition or statement announced by the derivation.
        p: Formula = d.valid_statement

        if is_well_formed_axiom(a=d):
            # This is an axiom.
            # By definition, the presence of an axiom in a theory is valid.
            pass
        elif is_well_formed_inference_rule(i=d):
            # This is an inference-rule.
            # By definition, the presence of an inference-rule in a theory is valid.
            pass
        elif is_well_formed_theorem(t=d):
            # This is a well-formed theorem.
            # Check that this theorem is a valid derivation with regard to predecessor theorems.
            m: Theorem = coerce_theorem(t=d)
            i: Inference = m.inference
            ir: InferenceRule = m.inference.inference_rule
            # Check that the inference-rule is a valid predecessor in the derivation.
            if not any(is_formula_equivalent(phi=ir, psi=ir2) for ir2 in
                       iterate_theory_inference_rules(d=c, max_derivations=index + 1)):
                if raise_error_if_false:
                    raise u1.ApplicativeError(
                        code=c1.ERROR_CODE_AS1_068,
                        msg='Inference-rule "ir" is not a valid predecessor (with index strictly less than "index").'
                            ' This forbids the derivation of proposition "p" in step "d" in the derivation sequence.',
                        p=p, ir=ir, index=index, d=d, c=c)
                return False, None, None
            # Check that all premises are valid predecessor propositions in the derivation.
            for q in i.premises:
                # Check that this premise is a valid predecessor proposition in the derivation.
                if not is_valid_proposition_in_theory_1(p=q, t=None, d=c, max_derivations=index):
                    # not any(is_formula_equivalent(phi=q, psi=p2) for p2 in
                    # iterate_valid_statements_in_enumeration_of_derivations_OBSOLETE(e=c, max_index=index)):
                    if raise_error_if_false:
                        raise u1.ApplicativeError(
                            msg='Premise "q" is not a valid predecessor (with index strictly less than "index").'
                                ' This forbids the derivation of proposition "p" in step "d" in the derivation'
                                ' sequence.',
                            code=c1.ERROR_CODE_AS1_036,
                            p=p, q=q, index=index, d=d, c=c)
                    return False, None, None
            # Check that the transformation of the inference-rule effectively yields the announced proposition.
            t2: Transformation = i.inference_rule.transformation
            p_prime = t2.apply_transformation(p=i.premises, a=i.arguments)
            if not is_formula_equivalent(phi=p, psi=p_prime):
                if raise_error_if_false:
                    raise u1.ApplicativeError(
                        msg='Transformation "t2" of inference-rule "ir" does not yield the expected proposition "p",'
                            ' but yields "p_prime".'
                            ' This forbids the derivation of proposition "p" in step "d" in the derivation sequence.'
                            ' Inference "i" contains the arguments (premises and the complementary arguments).',
                        code=c1.ERROR_CODE_AS1_036,
                        p=p, p_prime=p_prime, index=index, t2=t2, ir=ir, i=i, d=d, c=c)
                return False, None, None
            # All tests have been successfully completed, we now have the assurance
            # that derivation "d" would be valid if appended to theory "t".
            pass
        else:
            # Incorrect form.
            if raise_error_if_false:
                raise u1.ApplicativeError(
                    msg='Expected derivation "d" is not of a proper form (e.g. axiom, inference-rule or theorem).'
                        ' This forbids the derivation of proposition "p" in step "d" in the derivation'
                        ' sequence.',
                    code=c1.ERROR_CODE_AS1_071,
                    p=p, d=d, index=index, c=c)
            return False, None, None
        # Derivation "d" is valid.
        pass
    # All unverified derivations have been verified.
    pass
    return True, v, u
