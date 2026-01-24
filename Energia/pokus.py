
import pprint
import os

os.popen('pdfko.pdf')


cmd = 'tasklist /fi "imagename eq {}"'.format('Notepad.exe')
output = subprocess.check_output(cmd, shell=False) 
pprint.pprint(output)

# ------------ pdfko -----------------
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


from fpdf import FPDF

import os

root = tk.Tk()
root.resizable(False, False)
root.geometry('300x150')

file = fd.asksaveasfilename(parent = root,
                            title = 'Zvoľte subor',
                            initialdir = '/pyfiles/energia/', # alebo sem das os.getcwd()
                            filetypes = (   ( 'textové súbory', '*.txt'), 
                                            ('pdf súbory', '*.pdf')
                                        )
                            )
pdf = FPDF(unit = 'mm', format = 'A4')
pdf.add_page()
pdf.add_font('DejaVu', '', 'fonty/DejaVuSansCondensed.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)

pdf.cell(0, 10, 'Ahoj Svet', ln = 1)

text = 'Len ťažko uveriť že toto nefunguje'
pdf.cell(0, 10, text, ln = 1)
pdf.set_x(15)
text = 'Tak ako by to malo fungovať'
pdf.cell(0, 10, text, ln = 1)
for _ in range(1, 50):
    pdf.write(10, 'Tento text je vyrobeny write-om')
    pdf.ln()

pdf.output(file, 'F')

os.system(file) # spusti pdf - ko jeho programom adobe acrobat

root.mainloop()
