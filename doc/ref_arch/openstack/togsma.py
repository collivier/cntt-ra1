# pylint: disable=missing-module-docstring

import os

from pybtex.database import parse_file

bib_data = parse_file('refs.bib')

HEADER_REFERENCES = """References
----------

.. list-table:: References
   :widths: auto

   * - Ref
     - Doc Number
     - Title
"""

HEADER_BIBLIOGRAPHY = """Bibliography
------------

.. list-table:: Bibliography
   :widths: auto

   * - Ref
     - Document Title
     - Source
"""

with open("gsma/references.rst", "w", encoding='utf-8') as references, open(
        "gsma/bibliography.rst", "w", encoding='utf-8') as bibliography:
    references.write(HEADER_REFERENCES)
    bibliography.write(HEADER_BIBLIOGRAPHY)
    i = 0

    for key in bib_data.entries:
        if 'howpublished' in bib_data.entries[key].fields:
            references.write(f"   * - [{i}]\n")
            references.write(
                f"     - {bib_data.entries[key].fields['howpublished']}\n")
            references.write(
                f"     - {bib_data.entries[key].fields['title']}\n")
        else:
            bibliography.write(f"   * - [{i}]\n")
            bibliography.write(
                f"     - {bib_data.entries[key].fields['title']}\n")
            bibliography.write(
                f"     - {bib_data.entries[key].fields['url']}\n")
        i = i + 1

filenames = ['chapters/chapter01.rst',
             'gsma/references.rst', 'gsma/bibliography.rst',
             'chapters/chapter02.rst', 'chapters/chapter03.rst',
             'chapters/chapter04.rst', 'chapters/chapter05.rst',
             'chapters/chapter06.rst', 'chapters/chapter07.rst',
             'chapters/chapter08.rst', 'chapters/chapter09.rst']

with open('gsma/index.rst', 'w', encoding='utf-8') as outfile:
    for fname in filenames:
        with open(fname, encoding='utf-8') as infile:
            for line in infile:
                if (".. bibliography::" not in line.strip("\n") and 
                    ":cited:" not in line.strip("\n")):
                    outfile.write(line)
            outfile.write('\n')

with open('gsma/index.rst', 'r', encoding='utf-8') as infile:
    filedata = infile.read()
    i = 0
    for key in bib_data.entries:
        if 'howpublished' in bib_data.entries[key].fields:
            filedata = filedata.replace(
                f":cite:p:`{bib_data.entries[key].key}`",
                f"`[{i}] <#references>`_")
        else:
            filedata = filedata.replace(
                f":cite:p:`{bib_data.entries[key].key}`",
                f"`[{i}] <{bib_data.entries[key].fields['url']}>`__")
        i = i + 1

with open('gsma/index.rst', 'w', encoding='utf-8') as outfile:
    outfile.write(filedata)

os.remove("gsma/references.rst")
os.remove("gsma/bibliography.rst")
