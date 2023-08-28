import punctilious as pu
import contextlib


def export_sample_output(sample_file_name: str):
    with open(f'../sample/code/{sample_file_name}.py', mode='r', encoding='utf-8') as source_file:
        source_code = source_file.read()

    path = f'../sample/output/{sample_file_name}_unicode.txt'
    with open(path, 'w', encoding='utf-8') as f:
        with contextlib.redirect_stdout(f):
            pu.configuration.encoding = pu.encodings.unicode
            exec(source_code)

    path = f'../sample/output/{sample_file_name}_plaintext.txt'
    with open(path, 'w', encoding='utf-8') as f:
        with contextlib.redirect_stdout(f):
            pu.configuration.encoding = pu.encodings.plaintext
            exec(source_code)


sample_filenames = (
    'biconditional_elimination_1', 'biconditional_elimination_2', 'inconsistency_introduction_1',
    'inconsistency_introduction_2', 'inconsistency_introduction_3')

for sample_filename in sample_filenames:
    export_sample_output(sample_file_name=sample_filename)
