proof-by-contradiction-1
=========================

Definition
-----------

*proof-by-contradiction-1* is the :doc:`inference_rule`:

.. math::

    \left( \mathcal{H} assume \not \mathbf{P}, Inc\left(\mathcal{H}\right)  \right) \vdash \mathbf{P}

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