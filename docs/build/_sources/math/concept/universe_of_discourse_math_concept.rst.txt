.. _universe_of_discourse_math_concept:

universe-of-discourse
======================

.. seealso::
   :ref:`object-creation<object_creation_math_concept>` | :ref:`theory-derivation<theory_derivation_math_concept>`

Definition
----------

A *universe-of-discourse* is a (possibly empty) collection of objects.

.. math::

    \left( o_1, o_2, \ldots, o_n \right)

Where:

* :math:`o_i` is an object

If we organize objects in (desirably mutually exclusive but necessarily exhaustive) categories [#category_footnote]_ , a *universe-of-discourse* is equivalently defined as a tuple:

.. math::

    \left( \mathcal{C}_1, \mathcal{C}_2, \ldots, \mathcal{C}_n \right)

Where:

* :math:`\mathcal{C}_i` is an object category.

Considering the set of mutually exclusive and exhaustive object categories implemented by punctilious, a *universe-of-discourse* is
equivalently defined as a tuple:

.. math::

    \left( \mathcal{I}, \mathcal{A}, \mathcal{D}, \mathcal{O}, \mathcal{R}, \mathcal{\Phi}, \mathcal{T} \right)

Where:

* :math:`\mathcal{I}` is a (possibly empty) collection of inference-rule declarations
* :math:`\mathcal{A}` is a (possibly empty) collection of axiom declarations
* :math:`\mathcal{D}` is a (possibly empty) collection of definition declarations
* :math:`\mathcal{O}` is a (possibly empty) collection of simple object declarations
* :math:`\mathcal{R}` is a (possibly empty) collection of relation declarations
* :math:`\mathcal{\Phi}` is a (possibly empty) collection of formulae declarations
* :math:`\mathcal{T}` is a (possibly empty) collection of theory declarations

.. note:: The lifecycle of objects

    For objects (including *universes-of-discourse*) to exist, they must be :ref:`created<object_creation_math_concept>` . For objects to be contained in *universes-of-discourse*, they must be :ref:`declared<object_declaration_math_concept>` . And finally, for objects to be contained in :ref:`theory-derivations<theory_derivation_math_concept>` , they must be :ref:`included<object_inclusion_math_concept>` (aka postulated).

.. rubric:: Footnotes

.. [#category_footnote] ⌜category⌝ is used in its ordinary sense, i.e. not its mathematical sense.
