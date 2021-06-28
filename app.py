# splitpdf.py
# 2021-06-28 david.montaner@gmail.com
# split pdf for Enevia APP

# https://www.tutorialspoint.com/python/tk_anchors.htm

import os
import tkinter as tk
import tkinter.filedialog

import splitpdf

title = 'Enevia PDF Extractor'
strong_font = ('calibre', 10, 'bold')
normal_font = ('calibre', 10, 'normal')


def open_pdf_file():
    input_file = tkinter.filedialog.askopenfilename(filetypes=[('PDF files', '.pdf .Pdf .pDf .pdF .PDf .PdF .pDF .PDF')])
    print('Pre-rocessing file:', input_file, sep='\n')

    input_file_tkvar.set(input_file)

    if not output_tkvar.get():
        output_tkvar.set(input_file[:-4])

    n_pages, is_teletest, _, tt_cuts = splitpdf.read_teletest_info(input_file)

    print('n_pages:', n_pages)
    print('is_teletest:', is_teletest)

    npages_tkvar.set(n_pages)
    teletest_tkvar.set(str(is_teletest))

    global teletest_cuts
    teletest_cuts = tt_cuts


def process_pdf_file():

    global teletest_cuts

    cuts = splitpdf.process_cuts(
        coma_cuts=cuts_tkvar.get(),
        batches=batches_tkvar.get(),
        every=every_tkvar.get(),
        n_pages=npages_tkvar.get(),
        is_teletest=teletest_tkvar.get() == 'True',
        teletest_cuts=teletest_cuts)

    splitpdf.create_batch_files(
        file=input_file_tkvar.get(),
        cuts=cuts,
        output_tag=output_tkvar.get())


root = tk.Tk()
root.title(title)
root.geometry("2000x1000")

input_file_tkvar = tk.StringVar(root, value='empezamos')
teletest_cuts = {}

# ELEMENTS
title_label = tk.Label(root, text=title, font=('calibre', 20, 'bold'))

cuts_tkvar = tk.StringVar(value='')
cuts_label = tk.Label(root, font=strong_font, text='Cuts')
cuts_notes = tk.Label(root, font=normal_font, text='Collection of comma separated page cuts where new batches should start. Ej: 1,5,12')
cuts_entry = tk.Entry(root, font=normal_font, textvariable=cuts_tkvar)

batches_tkvar = tk.StringVar(value='')
batches_label = tk.Label(root, font=strong_font, text='Batches')
batches_notes = tk.Label(root, font=normal_font, text='Number batches to be created.')
batches_entry = tk.Entry(root, font=normal_font, textvariable=batches_tkvar)

every_tkvar = tk.StringVar(value='')
every_label = tk.Label(root, font=strong_font, text='Every')
every_notes = tk.Label(root, font=normal_font, text='Number of pages for each batch.')
every_entry = tk.Entry(root, font=normal_font, textvariable=every_tkvar)

output_tkvar = tk.StringVar(value='')
output_label = tk.Label(root, font=strong_font, text='Output')
output_notes = tk.Label(root, font=normal_font, text='Output file tag.')
output_entry = tk.Entry(root, font=normal_font, textvariable=output_tkvar)
# hacer output dir aqui

file_button_tkvar = tk.Button(root, text='Select PDF File', command=open_pdf_file)
file_button_entry = tk.Entry(root, font=normal_font, textvariable=input_file_tkvar)

npages_tkvar = tk.IntVar(root, value=0)
npages_label = tk.Label(root, font=strong_font, text='N. pages')
npages_notes = tk.Label(root, font=normal_font, text='Number of pages in the selected file.')
npages_entrY = tk.Label(root, font=normal_font, textvariable=npages_tkvar)

teletest_tkvar = tk.StringVar(root, value='False')  # tk.BooleanVar(root, value=False)  # ToDo: see why boolean does not work below
teletest_label = tk.Label(root, font=strong_font, text='Is Teletest')
teletest_notes = tk.Label(root, font=normal_font, text='Indicates if the file is from Teletest')
teletest_entrY = tk.Label(root, font=normal_font, textvariable=teletest_tkvar)  # ToDo: see why boolean does not work well here

submit_button_tkvar = tk.Button(root, text='Submit', command=process_pdf_file)


# LAYOUT
r = 0
title_label.grid(row=r, column=1, columnspan=3, sticky='W')

r += 1
cuts_label.grid(row=r, column=0, sticky='E')
cuts_entry.grid(row=r, column=1)
cuts_notes.grid(row=r, column=2, sticky='W')

r += 1
batches_label.grid(row=r, column=0, sticky='E')
batches_entry.grid(row=r, column=1)
batches_notes.grid(row=r, column=2, sticky='W')

r += 1
every_label.grid(row=r, column=0, sticky='E')
every_entry.grid(row=r, column=1)
every_notes.grid(row=r, column=2, sticky='W')

r += 1
output_label.grid(row=r, column=0, sticky='E')
output_entry.grid(row=r, column=1)
output_notes.grid(row=r, column=2, sticky='W')

r += 1
file_button_tkvar.grid(row=r, column=0)
file_button_entry.grid(row=r, column=1, columnspan=3, sticky='W')

r += 1
npages_label.grid(row=r, column=0, sticky='E')
npages_entrY.grid(row=r, column=1)
npages_notes.grid(row=r, column=2, sticky='W')

r += 1
teletest_label.grid(row=r, column=0, sticky='E')
teletest_entrY.grid(row=r, column=1)
teletest_notes.grid(row=r, column=2, sticky='W')

r += 1
submit_button_tkvar.grid(row=r, column=1)

root.mainloop()
# quit()
