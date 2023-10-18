import punctilious as pu
import theory as pu_theory

m0 = pu_theory.Mancosou2021MinimalLogicM0()
m0.t.export_article_to_file(proof=False, encoding=pu.encodings.plaintext,
    file_path='../../data/report_mancosou_2021_minimal_logic_noproof_enus_plaintext.txt')
