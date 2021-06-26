# splitpdf.py
# 2021-06-24 david.montaner@gmail.com
# split pdf by fix number of pages

import math
import argparse
import pdflib
import PyPDF2


def read_teletest_info(file):
    doc = pdflib.Document(file)
    n_pages = doc.no_of_pages
    is_teletest = doc.metadata.get('title') == 'Teletest'
    page_data = []
    if is_teletest:
        for page in doc:
            page_data.append({
                'page_no': page.page_no,
                'line_0' : page.lines[0],
                'line_3' : page.lines[3],
                'ref_lines': [x for x in page.lines if x.startswith('Ref:')]
            })

        cuts = {i: (
            str(x['page_no']),
            x['line_3'].replace(': ', '_'),
            x['line_0']
        ) for i, x in enumerate(page_data) if 0 < len(x['ref_lines'])}
    else:
        cuts = {}

    return n_pages, is_teletest, page_data, cuts


def create_batch_files(reader, cuts, output_tag):
    batch = page = 0
    writer = PyPDF2.PdfFileWriter()
    writer.addPage(reader.getPage(page))
    print(f'Processed page {page + 1} in batch {batch + 1}')

    for page in range(1, n_pages):
        if page in cuts:
            output_file = output_tag + '_' + '_'.join(cuts[batch]) + '.pdf'
            writer.write(open(output_file, 'wb'))
            writer = PyPDF2.PdfFileWriter()
            batch = page

        writer.addPage(reader.getPage(page))
        print(f'Processed page {page + 1} in batch {batch + 1}')

    output_file = output_tag + '_' + '_'.join(cuts[batch]) + '.pdf'
    writer.write(open(output_file, 'wb'))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''
    Split PDF tool:
    ''')
    parser.add_argument('-v', '--version', action='version', version='0.0.0')
    # parser.add_argument('-t', '--no-teletest', help='Do not attempt to parse Teletest data', action='store_true')
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
        cuts = [int(x) - 1 for x in cuts]
        cuts.append(0)
        cuts = sorted(list(set(cuts)))
        cuts = {x: (str(x + 1),) for x in cuts}
    elif args.batches:
        step = math.ceil(n_pages / args.batches)
        cuts = list(range(0, n_pages, step))
        cuts = {x: (str(x + 1),) for x in cuts}
    elif args.every:
        cuts = list(range(0, n_pages, args.every))
        cuts = {x: (str(x + 1),) for x in cuts}
    else:
        _, is_teletest, _, cuts = read_teletest_info(input_file)
        if is_teletest and 0 < len(cuts):
            print('\nTeletest data detected.\n')
        else:
            print('\nTeletest data not detected.\nOne of this parameters is then required: `--cuts`, `--batches` or `--every`\nSee option -h for HELP`\n')
            raise Exception

    if args.output:
        output_tag = args.output
    else:
        output_tag = input_file[:-4]

    create_batch_files(reader, cuts, output_tag)
