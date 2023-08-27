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


sample_file_name = 'inconsistency_introduction_1'
export_sample_output(sample_file_name='inconsistency_introduction_1')
