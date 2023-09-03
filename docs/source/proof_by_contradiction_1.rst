proof-by-contradiction-1
=========================

Definition
-----------

*proof-by-contradiction-1* is the :doc:`inference_rule`:

.. math::

    \left( \mathcal{H} \; \text{assume} \; \neg \mathbf{P}, \mathit{Inc}\left(\mathcal{H}\right)  \right) \vdash \mathbf{P}

Where:

* :math:`\mathcal{H}` is an :doc:`hypothesis`
* :math:`\mathbf{P}` is a propositional :doc:`formula`
* :math:`\mathit{Inc}` is the inconsistency function

Python implementation
----------------------

Sample usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude :: ../../sample/code/proof_by_contradiction_1.py
   :language: python

.. literalinclude :: ../../sample/output/proof_by_contradiction_1_unicode.txt
   :language: text

Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. module:: core
    :noindex:
.. autoclass:: InferenceRuleInclusionDict
    :members: proof_by_contradiction_1

Bibliography
------------

.. footbibliography::