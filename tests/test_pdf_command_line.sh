#!/bin/bash
# test_pdf_command_line.sh
# 2021-06-26 david@insightcapital.io
# test PDF scripts

# to be run from the project root directory

# este debe fallar
# python3.8 splitpdf.py tests/data/document.pdf

# estos deben funcionar
python3.8 splitpdf.py tests/data/document.pdf -e 2    -o tests/data/every2

python3.8 splitpdf.py tests/data/document.pdf -b 2    -o tests/data/batch2

python3.8 splitpdf.py tests/data/document.pdf -c 2,4, -o tests/data/cuts

python3.8 splitpdf.py tests/data/1a\ miccio-\ OAT\,\ Micotoxinas\,\ disruptores\ endocrinos-\ Candida.pdf 
