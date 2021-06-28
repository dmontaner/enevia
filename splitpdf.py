#!/usr/bin/env python3.8
# splitpdf.py
# 2021-06-26 david.montaner@gmail.com
# split pdf for Enevia

import os
import math
import argparse
import pdflib
import PyPDF2
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk

version = '0.0.1'


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


def create_batch_files(file, cuts, output_tag):
    msgs = []

    reader = PyPDF2.PdfFileReader(open(file, 'rb'))
    n_pages = reader.numPages

    batch = page = 0
    writer = PyPDF2.PdfFileWriter()
    writer.addPage(reader.getPage(page))
    msg = f'Processed page {page + 1} in batch {batch + 1}'
    msgs.append(msg)
    print(msg)

    for page in range(1, n_pages):
        if page in cuts:
            output_file = output_tag + '_' + '_'.join(cuts[batch]) + '.pdf'
            writer.write(open(output_file, 'wb'))
            writer = PyPDF2.PdfFileWriter()
            batch = page

        writer.addPage(reader.getPage(page))
        msg = f'Processed page {page + 1} in batch {batch + 1}'
        msgs.append(msg)
        print(msg)

    output_file = output_tag + '_' + '_'.join(cuts[batch]) + '.pdf'
    writer.write(open(output_file, 'wb'))

    return msgs


def cuts_from_comas(coma_cuts):
    '''
    cuts: string of coma separated page numbers (1 based).
    '''
    cuts = coma_cuts.strip(',').split(',')
    cuts = [int(x) - 1 for x in cuts]
    cuts.append(0)
    cuts = sorted(list(set(cuts)))
    cuts = {x: (str(x + 1),) for x in cuts}
    return cuts


def cuts_from_batches(batches, n_pages):
    '''
    batches: number of batches to be done.
    n_pages: number of pages in the document.
    '''
    batches = int(batches)
    n_pages = int(n_pages)

    step = math.ceil(n_pages / batches)
    cuts = list(range(0, n_pages, step))
    cuts = {x: (str(x + 1),) for x in cuts}
    return cuts


def cuts_from_every(every, n_pages):
    '''
    every  : number of pages in each batch document.
    n_pages: number of pages in the document.
    '''
    every = int(every)
    n_pages = int(n_pages)

    cuts = list(range(0, n_pages, every))
    cuts = {x: (str(x + 1),) for x in cuts}
    return cuts


def process_cuts(coma_cuts, batches, every, n_pages, is_teletest, teletest_cuts):
    if coma_cuts:
        cuts = cuts_from_comas(coma_cuts)
    elif batches:
        cuts = cuts_from_batches(batches, n_pages)
    elif every:
        cuts = cuts_from_every(every, n_pages)
    elif is_teletest and 0 < len(teletest_cuts):
        print('\nTeletest file detected.\n')
        cuts = teletest_cuts
    else:
        print('\nTeletest data not detected.\nOne of this parameters is then required: `--cuts`, `--batches` or `--every`\nSee option -h for HELP`\n')
        raise Exception
    return cuts


def enevia_gui(
        file='',
        title='Enevia PDF Extractor',
        width=2000,
        height=1000,
        strong_font=('calibre', 10, 'bold'),
        normal_font=('calibre', 10, 'normal'),
):

    def _open_pdf_file(input_file):
        print('Pre-rocessing file:', input_file, sep='\n')

        input_file_tkvar.set(input_file)

        if not output_tkvar.get():
            output_tkvar.set(input_file[:-4])

        n_pages, is_teletest, _, tt_cuts = read_teletest_info(input_file)

        print('n_pages:', n_pages)
        print('is_teletest:', is_teletest)

        npages_tkvar.set(n_pages)
        teletest_tkvar.set(str(is_teletest))

        global teletest_cuts
        teletest_cuts = tt_cuts

    def open_pdf_file():
        input_file = tkinter.filedialog.askopenfilename(filetypes=[('PDF files', '.pdf .Pdf .pDf .pdF .PDf .PdF .pDF .PDF')])
        _open_pdf_file(input_file)

    def process_pdf_file():

        global teletest_cuts

        cuts = process_cuts(
            coma_cuts=cuts_tkvar.get(),
            batches=batches_tkvar.get(),
            every=every_tkvar.get(),
            n_pages=npages_tkvar.get(),
            is_teletest=teletest_tkvar.get() == 'True',
            teletest_cuts=teletest_cuts)

        msgs = create_batch_files(
            file=input_file_tkvar.get(),
            cuts=cuts,
            output_tag=output_tkvar.get())

        msg_tkvar.set('\n'.join(msgs))

    def reset_form():
        global teletest_cuts
        teletest_cuts = {}

        input_file_tkvar.set('')
        cuts_tkvar.set('')
        batches_tkvar.set('')
        output_tkvar.set('')
        npages_tkvar.set(0)
        teletest_tkvar.set('False')
        msg_tkvar.set('')

    root = tk.Tk()
    root.title(title)
    root.geometry(f'{width}x{height}')

    frame_T = tk.Frame(root, width=width, height=height * 0.1, padx=10)
    frame_A = tk.Frame(root, width=width, height=height * 0.4, padx=100)
    frame_B = tk.Frame(root, width=width, height=height * 0.4, padx=100)

    teletest_cuts = {}

    # ELEMENTS
    title_label = tk.Label(frame_T, text=title, font=('calibre', 20, 'bold'))

    cuts_tkvar = tk.StringVar(value='')
    cuts_label = tk.Label(frame_A, font=strong_font, text='Cuts')
    cuts_notes = tk.Label(frame_A, font=normal_font, text='Collection of comma separated page cuts where new batches should start. Ej: 1,5,12')
    cuts_entry = tk.Entry(frame_A, font=normal_font, textvariable=cuts_tkvar)

    batches_tkvar = tk.StringVar(value='')
    batches_label = tk.Label(frame_A, font=strong_font, text='Batches')
    batches_notes = tk.Label(frame_A, font=normal_font, text='Number batches to be created.')
    batches_entry = tk.Entry(frame_A, font=normal_font, textvariable=batches_tkvar)

    every_tkvar = tk.StringVar(value='')
    every_label = tk.Label(frame_A, font=strong_font, text='Every')
    every_notes = tk.Label(frame_A, font=normal_font, text='Number of pages for each batch.')
    every_entry = tk.Entry(frame_A, font=normal_font, textvariable=every_tkvar)

    output_tkvar = tk.StringVar(value='')
    output_label = tk.Label(frame_A, font=strong_font, text='Output')
    output_notes = tk.Label(frame_A, font=normal_font, text='Output file tag.')
    output_entry = tk.Entry(frame_A, font=normal_font, textvariable=output_tkvar, width=150)  # allow for 100 characters in the box
    # hacer output dir aqui

    npages_tkvar = tk.IntVar(frame_A, value=0)
    npages_label = tk.Label(frame_A, font=strong_font, text='N. pages')
    npages_notes = tk.Label(frame_A, font=normal_font, text='Number of pages in the selected file.')
    npages_entrY = tk.Label(frame_A, font=normal_font, textvariable=npages_tkvar)

    teletest_tkvar = tk.StringVar(frame_A, value='False')  # tk.BooleanVar(root, value=False)  # ToDo: see why boolean does not work below
    teletest_label = tk.Label(frame_A, font=strong_font, text='Is Teletest')
    teletest_notes = tk.Label(frame_A, font=normal_font, text='Indicates if the file is from Teletest')
    teletest_entrY = tk.Label(frame_A, font=normal_font, textvariable=teletest_tkvar)  # ToDo: see why boolean does not work well here

    input_file_tkvar = tk.StringVar(value=file)
    file_button_tkvar = tk.Button(frame_B, font=strong_font, text='Select File', command=open_pdf_file)
    file_button_entry = tk.Entry(frame_B, font=normal_font, textvariable=input_file_tkvar, width=150)

    submit_button_tkvar = tk.Button(frame_B, font=strong_font, text='Submit', command=process_pdf_file)

    reset_button_tkvar = tk.Button(frame_B, font=normal_font, text='Reset form', command=reset_form)

    msg_tkvar = tk.StringVar(value='')
    msg_labeL = tk.Message(root, textvariable=msg_tkvar)

    if file:
        _open_pdf_file(file)

    # LAYOUT
    frame_T.pack()

    r = 0
    title_label.grid(row=r, column=1, columnspan=3, sticky='W')
    r += 1
    tkinter.ttk.Separator(frame_T, orient='horizontal').grid(row=r, column=0, rowspan=1, ipady=10)

    frame_A.pack()

    r = 0
    cuts_label.grid(row=r, column=0, sticky='E')
    cuts_entry.grid(row=r, column=1, sticky='W')
    cuts_notes.grid(row=r, column=2, sticky='W')

    r += 1
    batches_label.grid(row=r, column=0, sticky='E')
    batches_entry.grid(row=r, column=1, sticky='W')
    batches_notes.grid(row=r, column=2, sticky='W')

    r += 1
    every_label.grid(row=r, column=0, sticky='E')
    every_entry.grid(row=r, column=1, sticky='W')
    every_notes.grid(row=r, column=2, sticky='W')

    r += 1
    output_label.grid(row=r, column=0, sticky='E')
    output_entry.grid(row=r, column=1, columnspan=5)
    output_notes.grid(row=r, column=4, sticky='W')

    r += 1
    tkinter.ttk.Separator(frame_A, orient='horizontal').grid(row=r, column=0, rowspan=1, ipady=10)

    r += 1
    npages_label.grid(row=r, column=0, sticky='E')
    npages_entrY.grid(row=r, column=1)
    npages_notes.grid(row=r, column=2, sticky='W')

    r += 1
    teletest_label.grid(row=r, column=0, sticky='E')
    teletest_entrY.grid(row=r, column=1)
    teletest_notes.grid(row=r, column=2, sticky='W')

    r += 1
    tkinter.ttk.Separator(frame_A, orient='horizontal').grid(row=r, column=0, rowspan=1, ipady=10)

    frame_B.pack()

    r = 0
    file_button_tkvar.grid(row=r, column=0, sticky='W')
    file_button_entry.grid(row=r, column=1, columnspan=3, sticky='W')

    r += 1
    tkinter.ttk.Separator(frame_B, orient='horizontal').grid(row=r, column=0, rowspan=1, ipady=10)

    r += 1
    submit_button_tkvar.grid(row=r, column=1, sticky='W')
    reset_button_tkvar.grid(row=r, column=1, sticky='E')

    r += 1
    tkinter.ttk.Separator(frame_A, orient='horizontal').grid(row=r, column=0, rowspan=1, ipady=50)

    msg_labeL.pack()

    root.mainloop()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''
    Split PDF tool:
    ''')
    parser.add_argument('-v', '--version', action='version', version=version)
    parser.add_argument('-g', '--gui', action='store_true', help='Use graphical interface')
    parser.add_argument('-c', '--cuts'   , type=str, help='Collection of comma separated page cuts where new batches should start. Ej: 1,5,12')
    parser.add_argument('-b', '--batches', type=int, help='Number batches to be created.')
    parser.add_argument('-e', '--every'  , type=int, help='Number of pages for each batch.')
    parser.add_argument('-o', '--output' , type=str, help='Output file tag')
    parser.add_argument('file', help='PDF file you want to extract.', nargs='*')
    args = parser.parse_args()

    print(args)

    if args.gui:
        if args.file:
            enevia_gui(file=os.path.realpath(args.file[0]))
        else:
            enevia_gui()

    else:
        input_file = args.file[0]
        if input_file[-4:].lower() != '.pdf':
            print(f'\nFile `{input_file}` has not a proper PDF extension.\n')
            raise Exception

        print(input_file)

        # PREPROCESS FILE
        n_pages, is_teletest, _, teletest_cuts = read_teletest_info(input_file)

        if n_pages == 0:
            print(f'\nFile `{input_file}` seems to be empty.\n')
            raise Exception

        cuts = process_cuts(args.cuts, args.batches, args.every, n_pages, is_teletest, teletest_cuts)

        if args.output:
            output_tag = args.output
        else:
            output_tag = input_file[:-4]

        # PROCESS FILE
        create_batch_files(input_file, cuts, output_tag)
