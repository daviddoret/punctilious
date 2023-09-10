import punctilious as pu
import theory as pu_theory

t = pu_theory.Tao2006ThePeanoAxioms()
t.develop().export_article_to_file(proof=True, encoding=pu.encodings.plaintext,
    file_path='../../data/report_tao_2006_the_peano_axioms_proof_enus_plaintext.txt')
