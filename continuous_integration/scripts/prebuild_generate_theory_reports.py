"""Loop through theories natively included in the punctilious theory and build them for easy consultation. The idea is to progressively source an interesting library.

Status: Work in progress
"""
import punctilious as pu
import theory

for package, filename in {
    'report_tao_2006_2_1_the_peano_axioms'=theory.Tao2006ThePeanoAxioms(), 'report_mgz_2021_minimal_logic_m0'=theory.MGZ2021MinimalLogicM0(), 'report_mgz_2021_intuitionistic_logic_j0'=theory.MGZ2021IntuitionisticLogicJ0(), 'report_mgz_2021_classical_logic_k0'=theory.MGZ2021ClassicalLogicK0()}:
    for encoding in (pu.encodings.plaintext, pu.encodings.unicode, pu.encodings.latex):
        for proof in (False, True):
            proof_text = 'proof' if proof else 'noproof'
            output_file = f'..\\..\\data\\theory_{filename}_report_{proof_text}_enus_{str(encoding)}.txt'
            print(output_file)
            package.declare_theory.export_article_to_file(output_file, encoding=encoding, proof=proof)
