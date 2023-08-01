import punctilious as pu
import tao_2006_the_peano_axioms

t1 = tao_2006_the_peano_axioms.Tao2006ThePeanoAxioms().develop()

t1.export_report_to_file(
    'tao_2006_the_peano_axioms_with_proofs_en_us_unicode.txt', encoding=pu.encodings.unicode,
    proof=True)

# t1.export_report_to_file(
#    'tao_2006_the_peano_axioms_without_proofs_en_us_unicode.txt', encoding=pu.encodings.unicode,
#    proof=False)
# t1.export_report_to_file(
#    'tao_2006_the_peano_axioms_with_proofs_en_us_plaintext.txt', encoding=pu.encodings.plaintext,
#    proof=True)
# t1.export_report_to_file(
#    'tao_2006_the_peano_axioms_without_proofs_en_us_plaintext.txt', encoding=pu.encodings.plaintext,
#    proof=False)
# t1.export_report_to_file(
#    'tao_2006_the_peano_axioms_with_proofs_en_us_latex.tex', encoding=pu.encodings.latex_math,
#    proof=True)
# t1.export_report_to_file(
#    'tao_2006_the_peano_axioms_without_proofs_en_us_latex.tex', encoding=pu.encodings.latex_math,
#    proof=False)
