import abstract_formula_library as afl


class AbstractTransformation(afl.AbstractFormula):
    """

    An abstract-formula 0(phi, psi)
    where phi is denoted as the input, and psi is denoted as the output.

    A tuple (input, output).

    """

    def __init__(self, i: afl.FlexibleAbstractFormula, o: afl.FlexibleAbstractFormula):
        super(AbstractTransformation, self).__init__(t=None, s=None)

    def __new__(cls, i: afl.FlexibleAbstractFormula, o: afl.FlexibleAbstractFormula):
        i: afl.AbstractFormula = afl.data_validate_abstract_formula(i)
        o: afl.AbstractFormula = afl.data_validate_abstract_formula(o)
        phi: afl.AbstractFormula = phi.canonical_abstract_formula  # Canonize the abstract-formula
        if s.length != phi.natural_number_sequence.image_cardinality:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the `ConnectiveSequence` `s`"
                f" is not equal to the `image_cardinality` of the `natural_number_sequence` of its"
                f" `abstract_formula`.",
                s_length=s.length, phi_tree_size=phi.tree_size, s=s, phi=phi)
        psi = super(Formula, cls).__new__(cls, (phi, s,))
        psi = retrieve_formula_from_cache(psi)
        return psi


class AbstractTransformationBySubstitution(AbstractTransformation):
    """

    A tuple (input, output)
    where the input is composed of a tuple: (input, variables, substitution_values)
    to which correspond a unique output

    input: the formula that must be transformed
    variables: the unique placeholders of the formulas to be replaced, of length n,
        by convention, we will use atomic (leaf) formulas, in ascending order
    substitution: the unique substitution_values for the variables, of length n
    output: the transformed

    """

    def __init__(self, i: afl.FlexibleAbstractFormula, o: afl.FlexibleAbstractFormula):
        super(AbstractTransformation, self).__init__(t=None, s=None)

    def __new__(cls, i: afl.FlexibleAbstractFormula, v: afl.FlexibleAbstractFormula, s: afl.FlexibleAbstractFormula,
                o: afl.FlexibleAbstractFormula):
        i: afl.AbstractFormula = afl.data_validate_abstract_formula(i)
        o: afl.AbstractFormula = afl.data_validate_abstract_formula(o)
        phi: afl.AbstractFormula = phi.canonical_abstract_formula  # Canonize the abstract-formula
        if s.length != phi.natural_number_sequence.image_cardinality:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the `ConnectiveSequence` `s`"
                f" is not equal to the `image_cardinality` of the `natural_number_sequence` of its"
                f" `abstract_formula`.",
                s_length=s.length, phi_tree_size=phi.tree_size, s=s, phi=phi)
        psi = super(Formula, cls).__new__(cls, (phi, s,))
        psi = retrieve_formula_from_cache(psi)
        return psi


class TransformationBySubstitution:
    def __init__(self, i: afl.FlexibleFormula, v: afl.FlexibleFormula, s: afl.FlexibleFormula,
                 o: afl.FlexibleFormula):
        super(Transformation, self).__init__(t=None, s=None)

    def __new__(cls, i: afl.FlexibleFormula, v: afl.FlexibleFormula, s: afl.FlexibleFormula,
                o: afl.FlexibleFormula):
        i: afl.AbstractFormula = afl.data_validate_abstract_formula(i)
        o: afl.AbstractFormula = afl.data_validate_abstract_formula(o)
        phi: afl.AbstractFormula = phi.canonical_abstract_formula  # Canonize the abstract-formula
        if s.length != phi.natural_number_sequence.image_cardinality:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the `ConnectiveSequence` `s`"
                f" is not equal to the `image_cardinality` of the `natural_number_sequence` of its"
                f" `abstract_formula`.",
                s_length=s.length, phi_tree_size=phi.tree_size, s=s, phi=phi)
        psi = super(Formula, cls).__new__(cls, (phi, s,))
        psi = retrieve_formula_from_cache(psi)
        return psi
