relation
==========

Definition
----------

A *relation* is a set of ordered pairs :footcite:p:`downing_dictionary_2009`.
Equivalently, it is a property of sets such that, for any two members of sets :math:`a` and :math:`b`, :math:`aRb` is either true or false :footcite:p:`mcadams_all_2014`.

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

Bibliography
------------
.. footbibliography::
