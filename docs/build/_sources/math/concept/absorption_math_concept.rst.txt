.. _absorption_math_concept:
.. _absorption:

.. role:: python(code)
    :language: py

absorption (math concept)
==========================

.. seealso::
   :ref:`absorption_declaration_python_class` | :ref:`absorption_inclusion_python_class` | :ref:`absorption_python_sample`

Definition
----------

*absorption* is the well-known and valid :ref:`inference_rule_math_concept` in propositional-logic:

.. math::

    \left(P \implies Q\right) \vdash \left(P \implies P \land Q\right)

Where:

* :math:`P \implies Q` is a :ref:`formula_statement`
* :math:`P` is a propositional :ref:`formula`
* :math:`Q` is a propositional :ref:`formula`

In straightforward language, if P implies Q, it follows that P implies both P and Q.

Bibliography
--------------

* https://en.wikipedia.org/wiki/Absorption_(logic)
