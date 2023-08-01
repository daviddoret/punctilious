import punctilious as pu
import tao_2006_the_peano_axioms

t1 = tao_2006_the_peano_axioms.Tao2006ThePeanoAxioms().develop()

t1.export_report_to_file(
    'tao_2006_the_peano_axioms_with_proofs_en_us_unicode.txt', encoding=pu.encodings.unicode,
    output_proofs=True)
t1.export_report_to_file(
    'tao_2006_the_peano_axioms_without_proofs_en_us_unicode.txt', encoding=pu.encodings.unicode,
    output_proofs=False)
