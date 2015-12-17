#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os
import re
import sys
import itertools

import requests
from lxml.html import fromstring


URL_BASE = 'http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/'
URL_LIST = [
    # (revision, url, is_mass)
    (201410, '201504/t20150415_712722.html', False),
    (201308, '201401/t20140116_501070.html', False),
    (201210, '201301/t20130118_38316.html', False),
    (201110, '201201/t20120105_38315.html', False),
    (201010, '201107/t20110726_38314.html', False),
    (200912, '201006/t20100623_38313.html', False),
    (200812, '200906/t20090626_38312.html', False),
    (200712, '200802/t20080215_38311.html', False),
    (200612, '200704/t20070411_38310.html', False),
    (200512, '200410/t20041022_38307.html', True),
    (200506, '200410/t20041022_38306.html', True),
    (200412, '200410/t20041022_38305.html', True),
    (200409, '200410/t20041022_38304.html', True),
    (200403, '200406/t20040607_38302.html', True),
    (200312, '200402/t20040211_38301.html', True),
    (200306, '200307/t20030722_38300.html', True),
    (200212, '200302/t20030219_38299.html', True),
]

XPATH_EXPRS = [
    './/div[@class="xilan_con"]//tbody/tr',
    './/div[@class="xilan_con"]//p[not(ancestor::tbody)]',
]
XPATH_MASS_EXPRS = [
    './/p[@class="MsoNormal"]//span//text()',
]

SAC = [200212, 200712]


def strip_spaces_in_chinese_words(line):
    cjk_chars = u'\u3007\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff'
    return re.sub(
        ur'(\d{6})(\s+)([%s]+)\s([%s]+)' % (cjk_chars, cjk_chars),
        ur'\1\2\3\4', line, flags=re.U)


def strip_comments(line):
    return line.strip('*() \n\t\r').strip()


def iter_lines(element, is_mass):
    if is_mass:
        for line in iter_lines_of_mass_document(element):
            yield line
        return

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
    if len(sys.argv) != 2:
        print('Usage: %s [dir]' % sys.argv[0], file=sys.stderr)
        sys.exit(0)

    for revision, url, is_mass in URL_LIST:
        req = requests.get(URL_BASE + url)
        req.encoding = 'utf-8'
        el = fromstring(req.text)

        dirname = os.path.join(sys.argv[1], '%s.tsv' % revision)
        print('--> %s' % dirname, file=sys.stderr)

        source = 'stats'
        if revision in SAC:
            source = 'sac'

        with open(dirname, 'w') as dest_file:
            print(b'Source\tRevision\tCode\tName', file=dest_file)
            for line in iter_lines(el, is_mass):
                text = strip_spaces_in_chinese_words(strip_comments(line))
                if not text:
                    continue

                try:
                    code, name = text.split()
                    code = int(code)
                except ValueError:
                    print('ignored: %s' % text, file=sys.stderr)
                else:
                    out = '%s\t%s\t%s\t%s' % (source, revision, code, name)
                    print(out.encode('utf-8'), file=dest_file)


if __name__ == '__main__':
    main()
