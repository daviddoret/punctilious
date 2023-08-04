"""Loop through theories natively included in the punctilious package and export them for easy consultation. The idea is to progressively build an interesting library.

Status: Work in progress
"""

import punctilious as pu
import theory_packages.tao_2006_the_peano_axioms

t1 = theory_packages.tao_2006_the_peano_axioms.Tao2006ThePeanoAxioms().develop()

for encoding in (pu.encodings.plaintext, pu.encodings.unicode, pu.encodings.latex):
    for proof in (False, True):
        proof_text = 'proof' if proof else 'noproof'
        t1.export_report_to_file(
            f'../theory_exports/tao_2006_the_peano_axioms_report_{proof_text}_enus_{str(encoding)}.txt',
            encoding=encoding,
            proof=proof)
