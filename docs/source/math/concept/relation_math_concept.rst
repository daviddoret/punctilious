.. _connective_math_concept:

connective
==========

Definition
----------

A *connective* is a set of ordered pairs :cite:p:`downing_dictionary_2009` .
Equivalently, it is a property of sets such that, for any two members of sets :math:`a` and :math:`b`, :math:`aRb` is either true or false :cite:p:`mcadams_all_2014` .

Syntactically, a *connective* is represented with a
    A connective ◆ is a formula for formula.
    It assigns the following meaning to its composite formula 𝜑:
    𝜑 establishes a connective between its parameters.
    A connective ◆ has a fixed arity.

Key properties
-------------------
 - arity
 - :ref:`notation-form<notation_form_math_concept>`
 - signal-proposition (TODO: rename to propositional)
 - symbolic-representation

Punctilious data model
--------------------------

.. graphviz::

   digraph connective {
        rankdir = BT;
        "connective" -> "formula" [arrowhead=onormal];
   }


