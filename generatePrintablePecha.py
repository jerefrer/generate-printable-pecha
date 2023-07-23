#!/usr/bin/env python3

import sys

from tkinter import Tk, Button, Label, filedialog, Checkbutton, IntVar
import os
import subprocess
import re
import time
from tkinter import ttk

from generateOrderedPageNumbersForPrintingAsStacks import generateOrderedPageNumbersForPrintingAsStacks

def select_file():
    filepath = filedialog.askopenfilename(title="Select File")
    if filepath:
        process_file(filepath)

def process_file(inputFile):

    # Hide the checkbox and button during the process
    checkbox.pack_forget()
    select_button.pack_forget()

    # Create a progress label
    progress_label.config(text="Processing...")

    # Create a progress bar
    progress_bar.start()

    for _ in range(100):
      time.sleep(0.1)  # Simulating the process taking some time
      root.update_idletasks()  # Update the main event loop
      progress_bar.step(1)  # Move the progress bar

    directory, filename = os.path.split(inputFile)
    filename, ext = os.path.splitext(filename)

    tempfile = os.path.join(directory, "tempfile.pdf")
    outputFile = os.path.join(directory, filename + "_processed" + ext)

    autoscale = checkbox_var.get() == 1

    pdfInfo = subprocess.check_output(['pdfinfo', inputFile])
    p = re.compile(rb'Pages:\s*(.*)')
    result = p.search(pdfInfo)

    numberOfOneSidedPechaPages = int(result.group(1).decode())
    pageNumbersString = generateOrderedPageNumbersForPrintingAsStacks(numberOfOneSidedPechaPages)

    os.system(f"pdfjam '{inputFile}' '{pageNumbersString}' -o '{tempfile}' --nup 1x3 --paper a3paper --landscape")

    if autoscale:
      os.system(f"podofocrop '{tempfile}' '{outputFile}'")
      os.system(f"rm '{tempfile}'")
    else:
      os.system(f"mv '{tempfile}' '{outputFile}")

    progress_bar.stop()
    progress_label.config(text="Processing Complete")

    # Show the checkbox and button after the process is complete
    checkbox.pack()
    select_button.pack()

root = Tk()
root.title("File Processing Application")

# Add some padding and set the window size
root.geometry("400x150")
root.configure(padx=10, pady=10)

# Create a label for displaying progress and saving messages
progress_label = Label(root, text="")
progress_label.pack()

save_label = Label(root, text="")
save_label.pack()

# Create a button with custom styling
select_button = Button(root, text="Select File", command=select_file, padx=10, pady=5, width=20)
select_button.pack()

# Create a checkbox
checkbox_var = IntVar()
checkbox = Checkbutton(root, text="Autoscale", variable=checkbox_var)
checkbox.pack()

# Create a progress bar
progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.pack(pady=10)

root.mainloop()