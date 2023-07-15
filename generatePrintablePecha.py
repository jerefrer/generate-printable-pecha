#!/usr/bin/env python

# var pages = input;
# var numberOfStacks = 3;
# var numberOfOneSidedPrintingPages =
#     Math.floor(pages/numberOfStacks) + pages%numberOfStacks
# if (input < 6)
#   numberOfOneSidedPrintingPages = 1;
# if (input == 2)
#   numberOfOneSidedPrintingPages = 1;
# if (input == 8)
#   numberOfOneSidedPrintingPages = 3;
# //var numberOfOneSidedPrintingPages =
# //  Math.ceil(pages/(numberOfStacks * 2)) + 1;
# var stacks = _.range(1, pages+1).
#     inGroupsOf(numberOfOneSidedPrintingPages);
# return _(numberOfOneSidedPrintingPages).
#   times((i) => stacks.map((stack) => stack[i])).
#     map((a, index) => index.isEven() ? a : a.reverse()).
#     flatten().
#     map((e) => e ? e : '{}').join(',')

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

from tkinter import Tk, Button, Label, filedialog
import os
import time
from tkinter import ttk

def generateOrderedPageNumbersForPrintingAsStacks(numberOfOneSidedPechaPages, numberOfStacks=3):
    """Return the square of x.

    >>> generateOrderedPageNumbersForPrintingAsStacks(1)
    '1,{},{},{},{},{}'
    >>> generateOrderedPageNumbersForPrintingAsStacks(2)
    '1,{},{},{},{},2'
    >>> generateOrderedPageNumbersForPrintingAsStacks(3)
    '1,3,{},{},{},2'
    >>> generateOrderedPageNumbersForPrintingAsStacks(4)
    '1,3,{},{},4,2'
    >>> generateOrderedPageNumbersForPrintingAsStacks(6)
    '1,3,5,6,4,2'
    >>> generateOrderedPageNumbersForPrintingAsStacks(7)
    '1,4,7,{},5,2,3,6,{}'
    >>> generateOrderedPageNumbersForPrintingAsStacks(8)
    '1,4,7,8,5,2,3,6,{}'
    >>> generateOrderedPageNumbersForPrintingAsStacks(9)
    '1,4,7,8,5,2,3,6,9'
    >>> generateOrderedPageNumbersForPrintingAsStacks(10)
    '1,4,7,8,5,2,3,6,9'
    >>> generateOrderedPageNumbersForPrintingAsStacks(14)
    '1,7,13,14,8,2,3,9,{},{},10,4,5,11,{},{},12,6'

    # >>> generateOrderedPageNumbersForPrintingAsStacks(4,1)
    # '1,2,3,4'

    """

    numberOfOneSidedPrintablePages = math.ceil(numberOfOneSidedPechaPages / numberOfStacks) if numberOfOneSidedPechaPages > numberOfStacks else 2
    numberOfDualSidedPrintablePages = math.ceil(numberOfOneSidedPechaPages / (numberOfStacks * 2))
    oneSidedPechaPagesPerStack = int(
      (
        numberOfStacks * math.floor(numberOfOneSidedPechaPages / numberOfStacks) + \
        numberOfStacks * (numberOfOneSidedPechaPages % numberOfStacks) \
      ) / numberOfStacks)

    def appendIfExists(p):
      pageNumbers.append(p if p <= numberOfOneSidedPechaPages else '{}')

    def stackStart(stackNumber):
      return (stackNumber - 1) * oneSidedPechaPagesPerStack + 1

    pageNumbers = []

    for i in range(0, numberOfDualSidedPrintablePages):
      deltaRecto = i * 2
      deltaVerso = deltaRecto + 1
      appendIfExists(stackStart(1)+deltaRecto)
      appendIfExists(stackStart(2)+deltaRecto)
      appendIfExists(stackStart(3)+deltaRecto)
      appendIfExists(stackStart(3)+deltaVerso)
      appendIfExists(stackStart(2)+deltaVerso)
      appendIfExists(stackStart(1)+deltaVerso)

    return ','.join(map(str, pageNumbers))

if len(sys.argv) == 2 and sys.argv[1] == "test":
    import doctest
    doctest.testmod()

elif len(sys.argv) < 3:
    sys.exit("Usage: ./generatePrintablePDF.py input.pdf output.pdf [--autoscale]")

else:
  inputFile = sys.argv[1]
  outputFile = sys.argv[2]
  noautoscale = 'false' if len(sys.argv) == 4 and sys.argv[3] == "--autoscale" else 'true'

  pdfInfo = subprocess.check_output(['pdfinfo', inputFile])
  p = re.compile(rb'Pages:\s*(.*)')
  result = p.search(pdfInfo)

  numberOfOneSidedPechaPages = int(result.group(1).decode())
  pageNumbersString = generateOrderedPageNumbersForPrintingAsStacks(numberOfOneSidedPechaPages)

  # pdfInfo = subprocess.check_output(['pdfinfo', inputFile])
  # p = re.compile(rb'(Page size:\s*(.*) x (.*)) pts')
  # result = p.search(pdfInfo)
  # width = result.group(2).decode()
  # height = result.group(3).decode()
  # os.system("pdfjam input.pdf '" + pageNumbersString + "' -o reordered.pdf --papersize '{" + width + "pt," + height + "pt}'")
  # os.system("pdfjam reordered.pdf -o output.pdf --nup 1x3 --paper a3paper --landscape")

  os.system(f"pdfjam '{inputFile}' '{pageNumbersString}' -o '{outputFile}' --nup 1x3 --noautoscale {noautoscale} --paper a3paper --landscape")

  # os.system("gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dBATCH -dColorImageResolution=300 -sOutputFile=output2.pdf output.pdf")