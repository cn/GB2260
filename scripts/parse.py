# coding: utf-8

from __future__ import print_function

import os
import sys
import re

import requests
from lxml.html import fromstring


URL_BASE = 'http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/'
URL_LIST = [
    ('', URL_BASE + '201401/t20140116_501070.html'),  # latest: 2013
    ('-2012', URL_BASE + '201301/t20130118_38316.html'),
    ('-2011', URL_BASE + '201201/t20120105_38315.html'),
    ('-2010', URL_BASE + '201107/t20110726_38314.html'),
    ('-2009', URL_BASE + '201006/t20100623_38313.html'),
    ('-2008', URL_BASE + '200906/t20090626_38312.html'),
    ('-2007', URL_BASE + '200802/t20080215_38311.html'),
    ('-2006', URL_BASE + '200704/t20070411_38310.html'),
]

XPATH_EXPRS = [
    './/div[@class="xilan_con"]//tbody/tr',
    './/div[@class="xilan_con"]//p[not(ancestor::tbody)]',
]


def strip_spaces_in_chinese_words(line):
    cjk_chars = u'\u3007\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff'
    return re.sub(
        ur'(\d{6})(\s+)([%s]+)\s([%s]+)' % (cjk_chars, cjk_chars),
        ur'\1\2\3\4', line, flags=re.U)


def strip_comments(line):
    return line.strip('*() \n\t\r').strip()


def iter_lines(element):
    for xpath in XPATH_EXPRS:
        line_elements = element.xpath(xpath)
        for el in line_elements:
            fragments = el.xpath('.//text()')
            if any(child.tag == 'br' for child in el.getchildren()):
                for fragment in fragments:
                    yield fragment
            else:
                yield u' '.join(fragments)


def main():
    if len(sys.argv) != 2:
        print('Usage: %s [dir]' % sys.argv[0], file=sys.stderr)
        sys.exit(0)

    for suffix, url in URL_LIST:
        req = requests.get(url)
        req.encoding = 'utf-8'
        el = fromstring(req.text)

        dirname = os.path.join(sys.argv[1], 'GB2260%s.txt' % suffix)

        with open(dirname, 'w') as dest_file:
            for line in iter_lines(el):
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
