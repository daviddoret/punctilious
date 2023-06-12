import punctilious as p
import foundation_system_1 as fs1
import tao_2006_the_peano_axioms

fs1.ft.export_to_text(
    'punctilious_2023_foundation_theory_with_proofs.txt', output_proofs=True)
fs1.ft.export_to_text(
    'punctilious_2023_foundation_theory_without_proofs.txt',
    output_proofs=False)
tao_2006_the_peano_axioms.t.export_to_text(
    'tao_2006_the_peano_axioms_with_proofs.txt', output_proofs=True)
tao_2006_the_peano_axioms.t.export_to_text(
    'tao_2006_the_peano_axioms_without_proofs.txt', output_proofs=False)
