"""Pre-build script that iterates over all sample *punctilious* python script files, executes them, and saves their outputs with in different formats (*punctilious* encodings) in the data folder.
Like this, the output of sample *punctilious* python script files can be included in the documentation.

"""

from pathlib import Path
import contextlib
import punctilious as pu

sample_files_folder = '..\\src\\sample'
output_folder = '..\\data'


def export_sample_output(sample_file: Path):
    print(sample_file)

    with open(sample_file, mode='r', encoding='utf-8') as source_file:
        source_code = source_file.read()

    output_file = str(sample_file).replace('.py', '_plaintext.txt')
    output_file = output_file.replace(sample_files_folder, output_folder)
    with open(output_file, 'w', encoding='utf-8') as f:
        with contextlib.redirect_stdout(f):
            pu.configuration.encoding = pu.encodings.plaintext
            exec(source_code)

    output_file = str(sample_file).replace('.py', '_unicode.txt')
    output_file = output_file.replace(sample_files_folder, output_folder)
    with open(output_file, 'w', encoding='utf-8') as f:
        with contextlib.redirect_stdout(f):
            pu.configuration.encoding = pu.encodings.unicode
            exec(source_code)


def iterate_over_sample_files():
    for sample_file in Path(sample_files_folder).glob('sample_*.py'):
        export_sample_output(sample_file)


iterate_over_sample_files()
