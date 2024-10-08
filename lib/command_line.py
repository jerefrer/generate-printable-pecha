import argparse
from .process_file import process_file

parser = argparse.ArgumentParser(description='Generate a printable pecha PDF.')
parser.add_argument('input', help='Input PDF file path')
parser.add_argument('--paper-size', help='Optional - A4 or A3 (default: A4)')
parser.add_argument('--autoscale', help='Optional - pfdjam, podofo (default: pdfjam)',  nargs='?', const='pdfjam')
parser.add_argument('--output-name', help='Optional - Sets the name of the output file (in same directory as input)')
parser.add_argument('--verbose', help='Optional - Shows process commentary', action='store_const', const=True, default=False)
args = parser.parse_args()
process_file(args.input, args.paper_size, args.autoscale, args.verbose, args.output_name)
