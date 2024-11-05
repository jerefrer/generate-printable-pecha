import argparse
from .process_file import process_file

def parse_margins(value):
    values = [float(i) for i in value.split()]
    if len(values) == 1:
        return tuple(values[0] for _ in range(4))
    elif len(values) == 2:
        horizontal, vertical = values
        return (horizontal, vertical, horizontal, vertical)
    elif len(values) == 4:
        return tuple(values)
    else:
        raise argparse.ArgumentTypeError('margins must be specified as either 1, 2 or 4 space-separated values')

parser = argparse.ArgumentParser(description='Generate a printable pecha PDF.')
parser.add_argument('input', help='Input PDF file path')
parser.add_argument('--output-file-name', help='Optional - Sets the name of the output file (in same directory as input)')
parser.add_argument('--paper-size', help='Optional - A4 or A3 (default: A4)', nargs="?", default='A4')
parser.add_argument('--pages-per-sheet', help='Optional - Number of pecha pages to fit on one sheet (default: 3)', nargs="?", type=int, default=3)
parser.add_argument('--autoscale', help='Optional - none, pfdjam, podofo (default: pdfjam)', nargs="?", default='pdfjam')
parser.add_argument('--portrait', help='Optional - Use portrait orientation instead of landscape', action='store_const', const=True, default=False)
parser.add_argument('--verbose', help='Optional - Shows process commentary', action='store_const', const=True, default=False)
parser.add_argument('--sheet-margins',
    help='''Optional - Specify margin values in mm applied to the pdf pages. They can be:
    - A single value for all margins: "5"
    - Two values for horizontal/vertical: "5 4.2"
    - Four values (left bottom right top): "5 4.2 5 4.2"
    Values can be negative for trimming.
    You can for example set it to "0 4.2" and print without adjustments if your printer has a 4.2mm margin where it cannot print.
    In that way all the stripes will have the same height including the first and last one.''',
    type=parse_margins,
    metavar='VALUES'
)
args = parser.parse_args()

pdf_file_path = args.input
del args.input

process_file(pdf_file_path, **vars(args))