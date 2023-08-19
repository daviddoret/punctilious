relation
==========

Definition
----------

A *relation* is a set of ordered pairs :footcite:p:`downing_dictionary_2009`.
Equivalently, it is a property of sets such that, for any two members of sets :math:`a` and :math:`b`, :math:`aRb` is either true or false :footcite:p:`mcadams_all_2014`.

Syntactically, a *relation* is represented with a
    A relation ◆ is a theoretical-object for formula.
    It assigns the following meaning to its composite formula 𝜑:
    𝜑 establishes a relation between its parameters.
    A relation ◆ has a fixed arity.

Key properties
-------------------
 - arity
 - :doc:`notation_form`
 - signal-proposition (TODO: rename to propositional)
 - symbolic-representation

Punctilious data model
--------------------------

.. graphviz::

   digraph relation {
        rankdir = BT;
        "relation" -> "theoretical-object" [arrowhead=onormal];
   }

Python implementation
---------------------

In punctilious, *relations* are implemented by the core.Relation class.

A catalog of well-known *relations* is handily available in the RelationDict...

Relation
^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: Relation
    :members:
    :special-members: __init__

meta-object
^^^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: SimpleObjctDict
    :members: relation

Bibliography
------------

.. footbibliography::
