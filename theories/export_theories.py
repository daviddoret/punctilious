import punctilious as pu
import tao_2006_the_peano_axioms

t1 = tao_2006_the_peano_axioms.Tao2006ThePeanoAxioms().develop()

for encoding in (pu.encodings.plaintext, pu.encodings.unicode, pu.encodings.latex_math):
    for proof in (False, True):
        proof_text = 'with_proof' if proof else 'without_proof'

        t1.export_report_to_file(
            f'tao_2006_the_peano_axioms_{proof_text}_en_us_{str(encoding)}.txt',
            encoding=encoding,
            proof=proof)
