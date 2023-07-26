#!/usr/bin/env python

import re
import math

def stackSize(oneSidedPechaPages, stacks=3):
    """Determines how many one-sided pages will be in the thickest stack after cutting"""

    if oneSidedPechaPages == 1:
        return 1

    return math.ceil(oneSidedPechaPages / (stacks * 2)) * 2

def orderedPageNumbers(numberOfOneSidedPechaPages, numberOfStacks=3):
    """generates a string to be given to pdfjam to put pages in order for printing"""

    numberOfOneSidedPrintablePages = math.ceil(numberOfOneSidedPechaPages / numberOfStacks) if numberOfOneSidedPechaPages > numberOfStacks else 2
    numberOfDualSidedPrintablePages = math.ceil(numberOfOneSidedPechaPages / (numberOfStacks * 2))
    oneSidedPechaPagesPerStack = stackSize(numberOfOneSidedPechaPages, numberOfStacks)

    def appendIfExists(p):
      pageNumbers.append(p if p <= numberOfOneSidedPechaPages else '{}')

    def stackStart(stackNumber):
      return (stackNumber - 1) * oneSidedPechaPagesPerStack + 1

    pageNumbers = []

    for i in range(numberOfDualSidedPrintablePages):
      deltaRecto = i * 2
      deltaVerso = deltaRecto + 1
      appendIfExists(stackStart(1)+deltaRecto)
      appendIfExists(stackStart(2)+deltaRecto)
      appendIfExists(stackStart(3)+deltaRecto)
      appendIfExists(stackStart(3)+deltaVerso)
      appendIfExists(stackStart(2)+deltaVerso)
      appendIfExists(stackStart(1)+deltaVerso)

    return ','.join(map(str, pageNumbers))
