"""Loop through theories natively included in the punctilious theory and build them for easy consultation. The idea is to progressively source an interesting library.

Status: Work in progress
"""

from src import punctilious as pu

t1 = theory.package.tao_2006_2_1_the_peano_axioms.Tao2006ThePeanoAxioms().develop()

for encoding in (pu.encodings.plaintext, pu.encodings.unicode, pu.encodings.latex):
    for proof in (False, True):
        proof_text = 'proof' if proof else 'noproof'
        t1.export_article_to_file(
            f'../build/tao_2006_2_1_the_peano_axioms_report_{proof_text}_enus_{str(encoding)}.txt',
            encoding=encoding, proof=proof)
