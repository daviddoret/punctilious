.. _proof_by_refutation_1_math_concept:
.. _proof-by-refutation-1:

proof-by-refutation-1
=========================

Definition
----------

*proof-by-refutation-1* is the :ref:`inference-rule`:

.. math::

    \left( \boldsymbol{\mathcal{H}} \: \textit{assume} \: \neg \boldsymbol{P}, \boldsymbol{P}, Inc\left( \boldsymbol{\mathcal{H}} \right)  \right) \vdash \boldsymbol{P}

Where:
 * :math:`\boldsymbol{\mathcal{H}}` is an :ref:`hypothesis`
 * :math:`\boldsymbol{P}` is a :ref:`formula-statement`

In plain language, it consists in posing the hypothesis that a proposition :math:`\boldsymbol{P}` is not true, refuting that hypothesis by proving :math:`\boldsymbol{P}`, inferring the inconsistency of that hypothesis from this contradiction, and finally inferring :math:`\boldsymbol{P}`.

Python implementation
---------------------

ProofByRefutation1Declaration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: core
    :noindex:
.. autoclass:: ProofByRefutation1Declaration
    :members:
    :special-members: __init__

ProofByRefutation1Inclusion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: ProofByRefutation1Inclusion
    :members:
    :special-members: __init__

Bibliography
------------

.. footbibliography::