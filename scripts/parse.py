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
    # (year, url, is_mass)
    ('', '201401/t20140116_501070.html', False),
    ('-2012', '201301/t20130118_38316.html', False),
    ('-2011', '201201/t20120105_38315.html', False),
    ('-2010', '201107/t20110726_38314.html', False),
    ('-2009', '201006/t20100623_38313.html', False),
    ('-2008', '200906/t20090626_38312.html', False),
    ('-2007', '200802/t20080215_38311.html', False),
    ('-2006', '200704/t20070411_38310.html', False),
    ('-2005', '200410/t20041022_38307.html', True),
    ('-200506', '200410/t20041022_38306.html', True),
    ('-2004', '200410/t20041022_38305.html', True),
    ('-200409', '200410/t20041022_38304.html', True),
    ('-200403', '200406/t20040607_38302.html', True),
    ('-2003', '200402/t20040211_38301.html', True),
    ('-200306', '200307/t20030722_38300.html', True),
    ('-2002', '200302/t20030219_38299.html', True),
]

XPATH_EXPRS = [
    './/div[@class="xilan_con"]//tbody/tr',
    './/div[@class="xilan_con"]//p[not(ancestor::tbody)]',
]
XPATH_MASS_EXPRS = [
    './/p[@class="MsoNormal"]//span//text()',
]


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

    for suffix, url, is_mass in URL_LIST:
        req = requests.get(URL_BASE + url)
        req.encoding = 'utf-8'
        el = fromstring(req.text)

        dirname = os.path.join(sys.argv[1], 'GB2260%s.txt' % suffix)
        print('--> %s' % dirname, file=sys.stderr)

        with open(dirname, 'w') as dest_file:
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
                    out = '%s\t%s' % (code, name)
                    print(out.encode('utf-8'), file=dest_file)


if __name__ == '__main__':
    main()
