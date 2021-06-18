#!/usr/bin/env python3

# Reads the wiki pages under `wiki.rptools.info/index.php/` and generates an
# index of each page name and its one-line summary.  This can be used to
# eyeball the result looking for anomalies.  The next script to be run reads
# this file and processes the page in it instead of reading the `processed/`
# directory again because if there _is_ a glitch in the matrix, we want to be
# able to just remove that line from the output so it's ignored.

import glob
import os
import re
import sys

from lxml import etree
from lxml.etree import Element, ElementTree

_DIRECTORY = "processed/"
_FIRST_SENTENCE = re.compile(r"^(.*?[.])\s+[A-Z<]")

if not os.chdir(_DIRECTORY):
    print(f"Can't change directory to '{_DIRECTORY}'??", file=sys.stderr)


def convert_page_to_summary(filename: str):
    tree = ElementTree().parse(filename)
    template_desc = tree.xpath("//div[@class='template_description']")
    if not template_desc:
        template_desc = tree.xpath("//div[@class='template_version']")
    result = template_desc.getnext()
    text = etree.tostring(result)
    # Extract the first sentence.  That's any period followed by at least one
    # space and a capital letter.  Not very good, but good enough. :-/
    match = _FIRST_SENTENCE.match(text)
    if match:
        return match.group(1)
    else:
        return text


for file in glob.glob(_DIRECTORY + "*.html"):
    result = convert_page_to_summary(file)
    print(f"{file[:-5]}\t{result}")

