#!/usr/bin/env python
# coding: utf-8
# @Time 05/31/2019
# @License MIT

from __future__ import print_function

import os
import sys
import csv
import time
import random

import requests
from lxml.html import fromstring
from urlparse import urljoin

BASE_URL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/'

XPATH_EXPRS = {
    'LEVEL1': '//tr[@class="provincetr"]/td/a',
    'LEVEL2': '//tr[@class="citytr"]/td/a',
    'LEVEL3': '//tr[@class="countytr"]/td'
}

def crawl_page(url, depth):
    url = urljoin(BASE_URL, url)
    user_agent = {'User-agent': 'Mozilla/5.0'}
    # to avoid 10054 case
    time.sleep(random.random() * 5)
    print('crawling %s...' % url)
    req = requests.get(url, headers=user_agent)
    if 200 != req.status_code:
        msg = 'failed crawling %s' % (url)
        print(msg, file=sys.stderr)

    req.encoding = 'gbk'
    text = req.text.replace('gb2312', 'utf-8')
    el = fromstring(text)
    return {
        'el': el,
        'depth': depth
    }

def do_next(url, depth, write_row_fn):
    res = crawl_page(url, depth)
    parse_res(res, write_row_fn)

def parse_res(res, write_row_fn):
    el = res['el']
    depth = res['depth']

    parser = [
        province_parser,
        city_parser,
        county_parser
    ]

    eles = el.xpath(
        XPATH_EXPRS['LEVEL%s' % (depth)]
    )
    parser[depth - 1](eles, write_row_fn)

def province_parser(els, write_row_fn):
    for el in els:
        name = el.text_content()
        attr_href = el.get('href')
        # for example, "11.html" => "110000"
        code = attr_href.replace('.html', '0000')
        write_row_fn(code, name)
        do_next(
            attr_href,
            2,
            write_row_fn
        )

def city_parser(els, write_row_fn):
    d = {}
    for i, el in enumerate(els):
        el_text = el.text_content()
        if not i % 2:
            d['code'] = six_digit(el_text)
        else:
            d['name'] = el_text
            attr_href = el.get('href')
            write_row_fn(d['code'], d['name'])
            do_next(
                attr_href,
                3,
                write_row_fn
            )

def county_parser(els, write_row_fn):
    d = {}
    for i, el in enumerate(els):
        el_text = el.text_content()
        if not i % 2:
            d['code'] = six_digit(el_text)
        else:
            d['name'] = el_text
            write_row_fn(d['code'], d['name'])

def fill_not_included_data(write_row_fn):
    data = [
        {'710000': u'台湾省'},
        {'810000': u'香港特别行政区'},
        {'820000': u'澳门特别行政区'}
    ]
    for item in data:
        for k, v in item.items():
            write_row_fn(k, v)


def read_meta():
    meta_path = os.path.join('sources.tsv')
    with open(meta_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if 'stats' == row['Schema']:
                return row

def six_digit(code_str):
    return code_str[0: 6]

def root_path():
    return os.path.abspath(
        os.path.join(
            os.path.dirname(sys.argv[0]),
            os.path.pardir
        )
    )

def write_row(source, revision, code, name, f):
    row = '%s\t%s\t%s\t%s' % (source, revision, code, name)
    print(row.encode('utf-8'), file=f)

def main():
    meta = read_meta()
    revision = meta['Revision']
    source = meta['Source']
    dirname = os.path.join(root_path(), source)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    global BASE_URL
    BASE_URL = urljoin(BASE_URL, '%s/' % revision[0: 4])

    dest_file_path = os.path.join(
        dirname,
        '%s.tsv' % revision
    )

    def write_row_fn(code, name):
        write_row(
            source,
            revision,
            code,
            name,
            dest_file
        )

    with open(dest_file_path, 'w') as dest_file:
        print(b'Source\tRevision\tCode\tName', file=dest_file)
        do_next(meta['URL'], 1, write_row_fn)
        fill_not_included_data(write_row_fn)
        dest_file.close()

if __name__ == '__main__':
    main()
