#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os
import re
import sys
import csv
import itertools

import requests
from lxml.html import fromstring


XPATH_EXPRS = [
    './/div[@class="xilan_con"]//tbody/tr',
    './/div[@class="xilan_con"]//p[not(ancestor::tbody)]',
]
XPATH_MASS_EXPRS = [
    './/p[@class="MsoNormal"]//span//text()',
]
XPATH_MCA_EXPRS = [
    './/tr',
]


def strip_spaces_in_chinese_words(line):
    cjk_chars = u'\u3007\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff'
    return re.sub(
        r'(\d{6})(\s+)([%s]+)\s([%s]+)' % (cjk_chars, cjk_chars),
        r'\1\2\3\4', line, flags=re.U)


def strip_comments(line):
    return line.strip('*() \n\t\r').strip()


def iter_lines(element, schema):
    handlers = {
        'stats': iter_lines_of_normal_document,
        'stats-mass': iter_lines_of_mass_document,
        'mca': iter_lines_of_mca_document,
    }
    assert schema in handlers, 'Schema not found'
    handler = handlers[schema]
    for line in handler(element):
        yield line


def iter_lines_of_mca_document(element):
    for xpath in XPATH_MCA_EXPRS:
        line_elements = element.xpath(xpath)
        for el in line_elements:
            fragments = el.xpath('.//text()')
            if any(child.tag == 'br' for child in el.getchildren()):
                for fragment in fragments:
                    yield fragment
            else:
                yield u' '.join(fragments)


def iter_lines_of_normal_document(element):
    for xpath in XPATH_EXPRS:
        line_elements = element.xpath(xpath)
        for el in line_elements:
            fragments = el.xpath('.//text()')
            if any(child.tag == 'br' for child in el.getchildren()):
                for fragment in fragments:
                    yield fragment
            else:
                yield u' '.join(fragments)


def iter_lines_of_mass_document(element):
    for xpath in XPATH_MASS_EXPRS:
        fragments = [e.strip() for e in element.xpath(xpath)]
        stashed_fragments = []
        for fragment, next_fragment in predict(fragments):
            stashed_fragments.append(fragment)
            if next_fragment and next_fragment.isdigit() and stashed_fragments:
                yield '\t'.join(f for f in stashed_fragments if f)
                stashed_fragments = []
        yield '\t'.join(stashed_fragments)


def predict(iterable):
    collection = list(iterable)
    return itertools.izip_longest(collection, collection[1:])


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
        user_agent = {'User-agent': 'Mozilla/5.0'}
        req = requests.get(url, headers=user_agent)
        if req.status_code != 200:
            # resource has been deleted.
            msg = 'error: %s/%s %s' % (source, revision, req.status_code)
            print(msg, file=sys.stderr)
            continue
        req.encoding = 'utf-8'
        el = fromstring(req.text)

        dirname = os.path.join(sys.argv[2], source)
        pathname = os.path.join(dirname, '%s.tsv' % revision)
        print('--> %s' % pathname, file=sys.stderr)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(pathname, 'w') as dest_file:
            print('Source\tRevision\tCode\tName', file=dest_file)
            for line in iter_lines(el, schema):
                text = strip_spaces_in_chinese_words(strip_comments(line))
                if not text:
                    continue

                try:
                    code, name = text.split()
                    if len(code) != 6:
                        raise ValueError()
                    code = int(code)
                except ValueError:
                    print('ignored: %s' % text, file=sys.stderr)
                else:
                    out = '%s\t%s\t%s\t%s' % (source, revision, code, name)
                    print(out, file=dest_file)


if __name__ == '__main__':
    main()
