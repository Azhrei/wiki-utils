#!/usr/bin/env python3

# Reads the wiki pages under `wiki.rptools.info/index.php/` and generates an
# index of each page name and its one-line summary.  This can be used to
# eyeball the result looking for anomalies.  The next script to be run reads
# this output file and processes the page in it instead of reading the
# `processed/` directory again because if there _is_ a glitch in the matrix,
# we want to be able to just remove that line from the output so it's
# ignored.

import glob
import os
import re
import sys

from lxml import etree
from lxml.etree import Element, ElementTree

_DIRECTORY = "processed/"
_FIRST_SENTENCE = re.compile(r"^(.*?[.])\s+[A-Z<]")


def fatal(msg: str, exit_code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(exit_code)


def convert_page_to_summary(filename: str):
    with open(filename, encoding='utf-8') as f:
        # Read the entire file into a single variable.
        text = f.read()

        # Cleanup text/elements we don't care about, such as links.
        text = re.sub(r"<a(\s+[^>]*)?>", "<a>", text)
        text = text.replace("\n", " ")

        tree = etree.fromstring(text)
        template_desc = tree.xpath("//div[@class='template_description']")[0]
        if not etree.tostring(template_desc):
            template_desc = tree.xpath("//div[@class='template_version']")[0]
        # text = etree.tounicode(template_desc)
        text = template_desc.text
        # Extract the first sentence.  That's any period followed by at least one
        # space and a capital letter.  Not very good, but good enough. :-/
        match = _FIRST_SENTENCE.match(text)
        if match:
            result = match.group(1)
        else:
            result = text
        return result


def main():
    # When dealing with the OS, non-zero indicates an error.
    if os.chdir(_DIRECTORY):
        fatal(f"Can't change directory to '{_DIRECTORY}'??")

    file_list = glob.glob("*.html")
    file_list.sort()
    for file in file_list:
        result = convert_page_to_summary(file)
        print(f"{file[:-5]}\t{result}")


if __name__ == "__main__":
    main()
