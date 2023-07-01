#!/usr/bin/env python

# ==============
#  Installation
# ==============
#
# > sudo apt-get install texlive-extra-utils poppler-utils
#
# ==============
#  Usage
# ==============
#
# > ./generatePrintablePDF.py input.pdf output.pdf [--autoscale]
#

import os
import re
import sys
import math
import subprocess

if len(sys.argv) < 3:
  sys.exit("Usage: ./generatePrintablePDF.py input.pdf output.pdf [--autoscale]")

inputFile = sys.argv[1]
outputFile = sys.argv[2]
noautoscale = 'false' if len(sys.argv) == 4 and sys.argv[3] == "--autoscale" else 'true'

pdfInfo = subprocess.check_output(['pdfinfo', inputFile])
p = re.compile(rb'Pages:\s*(.*)')
result = p.search(pdfInfo)

numberOfPdfPages = int(result.group(1).decode())
numberOfDualSidedPechaPages = math.ceil(numberOfPdfPages / 6)

pageNumbers = []

def appendIfExists(p):
  pageNumbers.append(p if p <= numberOfPdfPages else '{}')

for i in range(0, numberOfDualSidedPechaPages):
  p = i * 6 + 1
  appendIfExists(p)
  appendIfExists(p+2)
  appendIfExists(p+4)
  appendIfExists(p+5)
  appendIfExists(p+3)
  appendIfExists(p+1)

pageNumbersString = ','.join(map(str, pageNumbers))

# pdfInfo = subprocess.check_output(['pdfinfo', inputFile])
# p = re.compile(rb'(Page size:\s*(.*) x (.*)) pts')
# result = p.search(pdfInfo)
# width = result.group(2).decode()
# height = result.group(3).decode()
# os.system("pdfjam input.pdf '" + pageNumbersString + "' -o reordered.pdf --papersize '{" + width + "pt," + height + "pt}'")
# os.system("pdfjam reordered.pdf -o output.pdf --nup 1x3 --paper a3paper --landscape")

os.system(f"pdfjam '{inputFile}' '{pageNumbersString}' -o '{outputFile}' --nup 1x3 --noautoscale {noautoscale} --paper a3paper --landscape -q")

# os.system("gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dBATCH -dColorImageResolution=300 -sOutputFile=output2.pdf output.pdf")