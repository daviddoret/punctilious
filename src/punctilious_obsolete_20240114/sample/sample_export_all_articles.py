"""This sample script export all theory packages."""

import punctilious as pu
import theory as pu_theory

target_folder = '../../data/'

package_list = {'mgz_2021_minimal_logic_m0': pu_theory.MGZ2021MinimalLogicM0(),
    'mgz_2021_intuitionistic_logic_j0':      pu_theory.MGZ2021IntuitionisticLogicJ0(),
    'mgz_2021_classical_logic_k0':           pu_theory.MGZ2021ClassicalLogicK0(),
    'tao_2006_the_peano_axioms':             pu_theory.Tao2006ThePeanoAxioms()}

for underscored_name, package in package_list.items():
    package.t.export_article_to_file(proof=False, encoding=pu.encodings.plaintext,
        file_path=f'../../data/report_{underscored_name}_noproof_enus_plaintext.txt')
    package.t.export_article_to_file(proof=False, encoding=pu.encodings.unicode_extended,
        file_path=f'../../data/report_{underscored_name}_noproof_enus_unicode.txt')
    package.t.export_article_to_file(proof=True, encoding=pu.encodings.plaintext,
        file_path=f'../../data/report_{underscored_name}_proof_enus_plaintext.txt')
    package.t.export_article_to_file(proof=True, encoding=pu.encodings.unicode_extended,
        file_path=f'../../data/report_{underscored_name}_proof_enus_unicode.txt')
