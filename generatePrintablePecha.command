#!/usr/bin/env python3

import sys

from tkinter import Tk, Button, Label, filedialog, Checkbutton, IntVar
import os
import subprocess
import re
import time
from tkinter import ttk

from orderedPageNumbers.orderedPageNumbers import orderedPageNumbers

inputFilePath = ''

def select_file():
    if filepath := filedialog.askopenfilename(title="Select File"):
        global inputFilePath
        inputFilePath = filepath
        _, inputFileName = os.path.split(inputFilePath)
        file_selected_label.config(text=f"File selected: {inputFileName}")
        process_button.pack()

def process_file():
    progress_label.config(text="Processing...")
    root.update_idletasks()  # Update the main event loop

    directory, filename = os.path.split(inputFilePath)
    filename, ext = os.path.splitext(filename)

    tempfile = os.path.join(directory, "tempfile.pdf")
    outputFileName = f"{filename}_processed{ext}"
    outputFilePath = os.path.join(directory, outputFileName)

    autoscale = checkbox_var.get() == 1

    pdfInfo = subprocess.check_output(['pdfinfo', inputFilePath])
    p = re.compile(rb'Pages:\s*(.*)')
    result = p.search(pdfInfo)

    numberOfOneSidedPechaPages = int(result[1].decode())
    pageNumbersString = orderedPageNumbers(numberOfOneSidedPechaPages)

    subprocess.call([
        'pdfjam', inputFilePath, pageNumbersString,
        '-o', tempfile,
        '--nup', '1x3',
        '--paper', 'a3paper',
        '--landscape'
    ])

    if autoscale:
      subprocess.call(['podofocrop', tempfile, outputFilePath])
      subprocess.call(['rm', tempfile])
    else:
      subprocess.call(['mv', tempfile, outputFilePath])

    progress_label.config(text=f"Done! New file generated: {outputFileName}")

root = Tk()
root.title("File Processing Application")

root.geometry("540x260")
root.configure(padx=10, pady=10)

save_label = Label(root, text="")
save_label.pack()

# Create a button with custom styling
select_button = Button(root, text="Select File", command=select_file, padx=10, pady=5, width=20)
select_button.pack()

file_selected_label = Label(root, text="")
file_selected_label.pack()

# Create a checkbox
checkbox_var = IntVar()
checkbox = Checkbutton(root, text="Auto-magnify", variable=checkbox_var, pady=20)
checkbox.pack()

# Create a button with custom styling
process_button = Button(root, text="Go", command=process_file, padx=10, pady=20, width=20)
process_button.pack()

progress_label = Label(root, text="")
progress_label.pack()

root.mainloop()