.. role:: python(code)
    :language: py

object-declaration
===================

.. seealso::
   :doc:`object_creation` | :doc:`object_inclusion`

Definition
----------

An *object-declaration* is a statement* that an (existing) object is contained in a :doc:`universe_of_discourse`.

In straightforward language, an *object-declaration* extends a :doc:`universe_of_discourse` with that object, which makes it possible to speak about that object using other objects.

Formally, whenever an object is declared:

Let U be a newly created universe.
Let x be an object declared in U.
Let y be an object declared in U.

To be even more accurate, we should consider a universe as an "accreting" variable:

Let x be a newly created object.
Let U := U extended by x.
Let y be a newly created object.
Let U := U extended by y.

*. Here, statement is considered in its general meaning, distinct from :doc:`theory_statement`.

