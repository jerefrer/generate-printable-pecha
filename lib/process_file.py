import subprocess
import re
import os
from .ordered_page_numbers.ordered_page_numbers import ordered_page_numbers

def process_file(
    input_file_path,
    output_file_name=None,
    paper_size="A4",
    pages_per_sheet=3,
    autoscale="pfdjam",
    sheet_margins=None,
    portrait=False,
    verbose=False
):
    directory, filename = os.path.split(input_file_path)
    filename, ext = os.path.splitext(filename)

    tempfile_path = os.path.join(directory, "tempfile.pdf")
    if output_file_name is None:
        output_file_name = f"{filename}_processed{ext}"
    output_file_path = os.path.join(directory, output_file_name)

    pdfInfo = subprocess.check_output(['pdfinfo', input_file_path])
    p = re.compile(rb'Pages:\s*(.*)')
    result = p.search(pdfInfo)

    number_of_one_sided_pecha_pages = int(result[1].decode())
    page_numbers_string = ordered_page_numbers(number_of_one_sided_pecha_pages)

    # print args
    if verbose:
        print(f"Processing {input_file_path}...")
        print(f"  Paper size: {paper_size}")
        print(f"  Pages per sheet: {pages_per_sheet}")
        print(f"  Autoscale: {autoscale}")
        print(f"  Portrait: {portrait}")
        print(f"  Verbose: {verbose}")
        if sheet_margins:
            print(f"  Sheet margins: left={sheet_margins[0]}mm, bottom={sheet_margins[1]}mm, right={sheet_margins[2]}mm, top={sheet_margins[3]}mm")

    options = [
        'pdfjam', input_file_path, page_numbers_string,
        '-o', tempfile_path,
        '--nup', f"1x{pages_per_sheet}",
        '--paper', 'a3paper' if paper_size == "A3" else 'a4paper'
    ]

    if autoscale in ["none", "podofo"]:
        options.extend(['--noautoscale', 'true'])

    if not portrait:
        options.append('--landscape')

    if not verbose:
        options.append('--quiet')

    if sheet_margins:
        border_string = f"{sheet_margins[0]}mm {sheet_margins[1]}mm {sheet_margins[2]}mm {sheet_margins[3]}mm"
        options.extend(['--trim', border_string, '--clip', 'true'])

    subprocess.call(options)

    if autoscale == "podofo":
        stdout_option = None if verbose else subprocess.DEVNULL
        subprocess.call(['podofocrop', tempfile_path, output_file_path], stdout=stdout_option)
        if verbose:
            print("  Removed tempfile.pdf.")
        subprocess.call(['rm', tempfile_path])
    else:
        if verbose:
            print(f"  Renamed tempfile.pdf to {output_file_name}.")
        subprocess.call(['mv', tempfile_path, output_file_path])