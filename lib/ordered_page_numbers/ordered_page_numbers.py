#!/usr/bin/env python

import re
import math

def stack_size(one_sided_pecha_pages, stacks=3):
    """Determines how many one-sided pages will be in the thickest stack after cutting"""

    if one_sided_pecha_pages == 1:
        return 1

    return math.ceil(one_sided_pecha_pages / (stacks * 2)) * 2

def ordered_page_numbers(number_of_one_sided_pecha_pages, number_of_stacks=3):
    """generates a string to be given to pdfjam to put pages in order for printing"""

    number_of_dual_sided_printable_pages = math.ceil(number_of_one_sided_pecha_pages / (number_of_stacks * 2))
    one_sided_pecha_pages_per_stack = stack_size(number_of_one_sided_pecha_pages, number_of_stacks)

    def appendIfExists(p):
      page_numbers.append(p if p <= number_of_one_sided_pecha_pages else '{}')

    def stackStart(stack_number):
      return (stack_number - 1) * one_sided_pecha_pages_per_stack + 1

    page_numbers = []

    for i in range(number_of_dual_sided_printable_pages):
      delta_recto = i * 2
      delta_verso = delta_recto + 1
      appendIfExists(stackStart(1)+delta_recto)
      appendIfExists(stackStart(2)+delta_recto)
      appendIfExists(stackStart(3)+delta_recto)
      appendIfExists(stackStart(3)+delta_verso)
      appendIfExists(stackStart(2)+delta_verso)
      appendIfExists(stackStart(1)+delta_verso)

    return ','.join(map(str, page_numbers))
