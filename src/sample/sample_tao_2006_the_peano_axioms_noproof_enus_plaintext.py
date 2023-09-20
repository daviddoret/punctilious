import punctilious as pu
import theory as pu_theory

the_peano_axioms = pu_theory.Tao2006ThePeanoAxioms()
the_peano_axioms.t.export_article_to_file(proof=False, encoding=pu.encodings.plaintext,
    file_path='../../data/report_tao_2006_the_peano_axioms_noproof_enus_plaintext.txt')
