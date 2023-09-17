.. _object_declaration_math_concept:

object-declaration
===================

.. seealso::
   :ref:`object-creation<object_creation_math_concept>` | :ref:`object-inclusion<object_inclusion_math_concept>`

Definition
----------

An *object-declaration* is a statement [footnote2]_ that an (existing) object is contained in a :ref:`universe-of-discourse<universe_of_discourse_math_concept>`.

In straightforward language, an *object-declaration* extends a :ref:`universe-of-discourse<universe_of_discourse_math_concept>` with that object, which makes it possible to speak about that object using other objects.

Formally, whenever an object is declared:

Let U be a newly created universe.
Let x be an object declared in U.
Let y be an object declared in U.

To be even more accurate, we should consider a universe as an "accreting" variable:

Let x be a newly created object.
Let U := U extended by x.
Let y be a newly created object.
Let U := U extended by y.

.. rubric:: Footnotes
.. [footnote2] Here, statement is considered in its general meaning, distinct from theory-statement.

