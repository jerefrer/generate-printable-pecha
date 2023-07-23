#!/usr/bin/env python

import sys
import generateOrderedPageNumbersForPrintingAsStacks

if len(sys.argv) == 2 and sys.argv[1] == "test":
    import doctest
    doctest.testmod()

elif len(sys.argv) < 3:
    sys.exit("Usage: ./generatePrintablePDF.py input.pdf output.pdf [--autoscale]")

else:
  inputFile = sys.argv[1]
  outputFile = sys.argv[2]
  autoscale = len(sys.argv) == 4 and sys.argv[3] == "--autoscale"
  noautoscale = 'false' if autoscale else 'true'

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

  os.system(f"pdfjam '{inputFile}' '{pageNumbersString}' -o 'tempfile.pdf' --nup 1x3 --paper a3paper --landscape")

  if autoscale:
    os.system(f"podofocrop tempfile.pdf {outputFile}")
    os.system(f"rm tempfile.pdf")

  # os.system("gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dBATCH -dColorImageResolution=300 -sOutputFile=output2.pdf output.pdf")