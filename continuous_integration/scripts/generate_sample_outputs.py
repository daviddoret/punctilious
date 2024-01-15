"""Pre-build script that iterates over all sample *punctilious_obsolete_20240114* python script files, executes them, and saves their outputs with in different formats (*punctilious_obsolete_20240114* encodings) in the data folder.
Like this, the output of sample *punctilious_obsolete_20240114* python script files can be included in the documentation.

"""

from pathlib import Path
import contextlib
import punctilious as pu

"""For every inference-rule in the punctilious_obsolete_20240114 package,
generate the restructured text documentation page.
"""

import jinja2
import os

file_loader = jinja2.FileSystemLoader('../jinja_templates')
env = jinja2.Environment(loader=file_loader)
script_path = os.getcwd()
script_name = os.path.basename(__file__)
ci_path = os.path.abspath(os.path.join(script_path, os.pardir))
project_path = os.path.abspath(os.path.join(ci_path, os.pardir))
src_path = os.path.abspath(os.path.join(project_path, 'src'))
sample_path = os.path.abspath(os.path.join(src_path, 'sample'))
data_path = os.path.abspath(os.path.join(project_path, 'data'))


def export_sample_output(sample_file: Path):
    print(sample_file)

    with open(sample_file, mode='r', encoding='utf-8') as source_file:
        source_code = source_file.read()

    output_file = str(sample_file).replace('.py', '_plaintext.txt')
    output_file = output_file.replace(sample_path, data_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        with contextlib.redirect_stdout(f):
            pu.configuration.encoding = pu.encodings.plaintext
            print(source_code)
            exec(source_code)

    output_file = str(sample_file).replace('.py', '_unicode.txt')
    output_file = output_file.replace(sample_path, data_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        with contextlib.redirect_stdout(f):
            pu.configuration.encoding = pu.encodings.unicode_extended
            exec(source_code)


def iterate_over_sample_files():
    for sample_file in Path(sample_path).glob('sample_*.py'):
        export_sample_output(sample_file)


iterate_over_sample_files()
