"""Loop through theories natively included in the punctilious package and build them for easy consultation. The idea is to progressively source an interesting library.

Status: Work in progress
"""

import punctilious as pu
import theory.package.tao_2006_the_peano_axioms

t1 = theory.package.tao_2006_the_peano_axioms.Tao2006ThePeanoAxioms().develop()

for encoding in (pu.encodings.plaintext, pu.encodings.unicode, pu.encodings.latex):
    for proof in (False, True):
        proof_text = 'proof' if proof else 'noproof'
        t1.export_report_to_file(
            f'../build/tao_2006_the_peano_axioms_report_{proof_text}_enus_{str(encoding)}.txt',
            encoding=encoding, proof=proof)
