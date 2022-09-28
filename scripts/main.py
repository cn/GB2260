#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os
import csv
import sys

from parse.parser import Parser

PARSER = Parser()

def main():
    if len(sys.argv) != 3:
        print('Usage: %s [sources] [dir]' % sys.argv[0], file=sys.stderr)
        sys.exit(0)
    
    with open(sys.argv[1], 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        url_list = [
            (line['Source'], line['Revision'], line['URL'], line['Schema'])
            for line in reader
        ]

    for source, revision, url, schema in url_list:
        dirname = os.path.join(sys.argv[2], source)
        PARSER.parse_by_url(dirname, source, revision, url, schema)


if __name__ == '__main__':
    main()