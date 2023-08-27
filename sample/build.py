# with open('../sample/code/inconsistency_introduction_1.py') as f:
#    output = exec(f.read())
# pass

# import subprocess

# result = subprocess.run(['python', '../sample/code/inconsistency_introduction_1.py'],
#    capture_output=True, text=True)

# print(result.stdout)
import punctilious as pu

import contextlib

with open('../sample/code/inconsistency_introduction_1.py', mode='r',
        encoding='utf-8') as source_file:
    source_code = source_file.read()

path = '../sample/output/inconsistency_introduction_1_unicode.txt'
with open(path, 'w', encoding='utf-8') as f:
    with contextlib.redirect_stdout(f):
        pu.configuration.encoding = pu.encodings.unicode
        exec(source_code)

path = '../sample/output/inconsistency_introduction_1_plaintext.txt'
with open(path, 'w', encoding='utf-8') as f:
    with contextlib.redirect_stdout(f):
        pu.configuration.encoding = pu.encodings.plaintext
        exec(source_code)

pass
