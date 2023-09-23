import subprocess
import re
import os
from .ordered_page_numbers.ordered_page_numbers import ordered_page_numbers

def process_file(input_file_path, paper_size, autoscale, verbose):
    directory, filename = os.path.split(input_file_path)
    filename, ext = os.path.splitext(filename)

    tempfile_path = os.path.join(directory, "tempfile.pdf")
    output_file_name = f"{filename}_processed{ext}"
    output_file_path = os.path.join(directory, output_file_name)

    pdfInfo = subprocess.check_output(['pdfinfo', input_file_path])
    p = re.compile(rb'Pages:\s*(.*)')
    result = p.search(pdfInfo)

    number_of_one_sided_pecha_pages = int(result[1].decode())
    page_numbers_string = ordered_page_numbers(number_of_one_sided_pecha_pages)

    print(autoscale)

    options = [
        'pdfjam', input_file_path, page_numbers_string,
        '-o', tempfile_path,
        '--nup', '1x3',
        '--landscape',
        '--paper', 'a3paper' if paper_size == "A3" else 'a4paper',
        '--noautoscale', 'true' if not autoscale or autoscale == "podofo" else 'false'
    ] + (['--quiet'] if not verbose else [])

    subprocess.call(options)

    if autoscale == "podofo":
        stdout_option = None if verbose else subprocess.DEVNULL
        subprocess.call(['podofocrop', tempfile_path, output_file_path], stdout=stdout_option)
        if verbose:
            print(f"  Removed tempfile.pdf.")
        subprocess.call(['rm', tempfile_path])
    else:
        if verbose:
            print(f"  Renamed tempfile.pdf to {output_file_name}.")
        subprocess.call(['mv', tempfile_path, output_file_path])
