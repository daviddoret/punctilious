"""Loop through theories natively included in the punctilious theory and build them for easy consultation. The idea is to progressively source an interesting library.

Status: Work in progress
"""
import punctilious as pu
import theory

t1 = theory.Tao2006ThePeanoAxioms().develop()

for encoding in (pu.encodings.plaintext, pu.encodings.unicode, pu.encodings.latex):
    for proof in (False, True):
        proof_text = 'proof' if proof else 'noproof'
        output_file = f'..\\data\\theory_tao_2006_2_1_the_peano_axioms_report_{proof_text}_enus_{str(encoding)}.txt'
        print(output_file)
        t1.export_article_to_file(output_file, encoding=encoding, proof=proof)
