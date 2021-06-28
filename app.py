# splitpdf.py
# 2021-06-28 david.montaner@gmail.com
# split pdf for Enevia APP

# https://www.tutorialspoint.com/python/tk_anchors.htm

import os
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk

import splitpdf

width = 2000
height = 1000
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

    msgs = splitpdf.create_batch_files(
        file=input_file_tkvar.get(),
        cuts=cuts,
        output_tag=output_tkvar.get())

    print(msgs)

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

input_file_tkvar = tk.StringVar(value='')
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

file_button_tkvar = tk.Button(frame_B, font=strong_font, text='Select File', command=open_pdf_file)
file_button_entry = tk.Entry(frame_B, font=normal_font, textvariable=input_file_tkvar, width=150)

submit_button_tkvar = tk.Button(frame_B, font=strong_font, text='Submit', command=process_pdf_file)

reset_button_tkvar = tk.Button(frame_B, font=normal_font, text='Reset form', command=reset_form)

msg_tkvar = tk.StringVar(value='')
msg_labeL = tk.Message(root, textvariable=msg_tkvar)


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
# quit()
