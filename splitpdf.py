# splitpdf.py
# 2021-06-24 david.montaner@gmail.com
# split pdf by fix number of pages

import math
import argparse
import PyPDF2

parser = argparse.ArgumentParser(description='''
Split PDF tool:
''')
parser.add_argument('-v', '--version', action='version', version='0.0.0')
parser.add_argument('-c', '--cuts'   , type=str, help='Collection of comma separated page cuts where new batches should start. Ej: 1,5,12')
parser.add_argument('-b', '--batches', type=int, help='Number batches to be created.')
parser.add_argument('-e', '--every'  , type=int, help='Number of pages for each batch.')
parser.add_argument('-o', '--output' , type=str, help='output file tag')
parser.add_argument('file', help='PDF file you want to extract.', nargs=1)
args = parser.parse_args()

print(args)

input_file = args.file[0]
if input_file[-4:].lower() != '.pdf':
    print(f'\nFile `{input_file}` has not a proper PDF extension.\n')
    raise Exception

print(input_file)

# read input file
reader = PyPDF2.PdfFileReader(open(input_file, 'rb'))
n_pages = reader.numPages

if n_pages == 0:
    print(f'\nFile `{input_file}` seems to be empty.\n')
    raise Exception

if args.cuts:
    cuts = args.cuts.strip(',').split(',')
    cuts = [int(x) for x in cuts]
elif args.batches:
    step = math.ceil(n_pages / args.batches)
    cuts = list(range(0, n_pages, step))
elif args.every:
    cuts = list(range(0, n_pages, args.every))
else:
    print('\nOne of this parameters is required: `--cuts`, `--batches` or `--every`\nSee option -h for HELP`\n')
    raise Exception

if args.output:
    output_tag = args.output
    if '{}' not in output_tag:
        output_tag += '_{}.pdf'
else:
    output_tag = input_file[:-4] + '_{}.pdf'

# create batch files
batch = page = 0
writer = PyPDF2.PdfFileWriter()
writer.addPage(reader.getPage(page))
print(f'Processed page {page + 1} in batch {batch + 1}')

for page in range(1, n_pages):

    if page in cuts:
        writer.write(open(output_tag.format(batch + 1), 'wb'))
        writer = PyPDF2.PdfFileWriter()
        batch = page

    writer.addPage(reader.getPage(page))
    print(f'Processed page {page + 1} in batch {batch + 1}')

writer.write(open(output_tag.format(batch + 1), 'wb'))
