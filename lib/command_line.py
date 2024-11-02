import argparse
from .process_file import process_file

def parse_borders(value):
    values = [float(i) for i in value.split()]
    if len(values) == 1:
        return tuple(values[0] for _ in range(4))
    elif len(values) == 2:
        horizontal, vertical = values
        return (horizontal, vertical, horizontal, vertical)
    elif len(values) == 4:
        return tuple(values)
    else:
        raise argparse.ArgumentTypeError('Borders must be specified as either 1, 2 or 4 space-separated values')

parser = argparse.ArgumentParser(description='Generate a printable pecha PDF.')
parser.add_argument('input', help='Input PDF file path')
parser.add_argument('--output-file-name', help='Optional - Sets the name of the output file (in same directory as input)')
parser.add_argument('--paper-size', help='Optional - A4 or A3 (default: A4)', nargs="?", default='A4')
parser.add_argument('--pages-per-sheet', help='Optional - Number of pecha pages to fit on one sheet (default: 3)', nargs="?", type=int, default=3)
parser.add_argument('--autoscale', help='Optional - none, pfdjam, podofo (default: pdfjam)', nargs="?", default='pdfjam')
parser.add_argument('--portrait', help='Optional - Use portrait orientation instead of landscape', action='store_const', const=True, default=False)
parser.add_argument('--verbose', help='Optional - Shows process commentary', action='store_const', const=True, default=False)
parser.add_argument('--borders',
    help='''Optional - Specify border values in mm. Can be:
    - Single value for all borders: "5"
    - Two values for horizontal/vertical: "5 4.2"
    - Four values (left bottom right top): "5 4.2 5 4.2"
    Values can be negative for trimming.''',
    type=parse_borders,
    metavar='VALUES'
)
args = parser.parse_args()

pdf_file_path = args.input
del args.input

process_file(pdf_file_path, **vars(args))