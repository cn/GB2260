from __future__ import print_function

import os
import sys
import re
import itertools
import requests

from ttictoc import TicToc
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

class Parser:
    def parse_by_url(self, dirname, source, revision, url, schema):
        user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        
        print('===> load content of url %s' % url, file=sys.stderr)
        t = TicToc()
        t.tic()
        req = requests.get(url, headers=user_agent)
        t.toc()
        print('content of url %s is loaded in %ss' % (url, t.elapsed), file=sys.stderr)

        if req.status_code != 200:
            # resource has been deleted.
            msg = 'error: %s/%s %s' % (source, revision, req.status_code)
            print(msg, file=sys.stderr)
            return

        req.encoding = 'utf-8'
        content = req.text

        if "".__eq__(content):
            print('content of url %s is empty' % url, file=sys.stderr)
            return

        self.parse_by_content(dirname, source, revision, content, schema)

    def parse_by_content(self, dirname, source, revision, content, schema):
        if "".__eq__(content):
            raise ValueError('content should not be empty')
            
        el = fromstring(content)
        
        pathname = os.path.join(dirname, '%s.tsv' % revision)
        print('--> %s' % pathname, file=sys.stderr)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(pathname, 'w') as dest_file:
            print(b'Source\tRevision\tCode\tName', file=dest_file)
            for line in self.__iter_lines(el, schema):
                text = self.__strip_spaces_in_chinese_words(self.__strip_comments(line))
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
                    print(out.encode('utf-8'), file=dest_file)

    def __strip_spaces_in_chinese_words(self, line):
        cjk_chars = u'\u3007\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff'
        return re.sub(
            ur'(\d{6})(\s+)([%s]+)\s([%s]+)' % (cjk_chars, cjk_chars),
            ur'\1\2\3\4', line, flags=re.U)

    def __strip_comments(self, line):
        return line.strip('*() \n\t\r').strip()


    def __iter_lines(self, element, schema):
        handlers = {
            'stats': self.__iter_lines_of_normal_document,
            'stats-mass': self.__iter_lines_of_mass_document,
            'mca': self.__iter_lines_of_mca_document,
        }
        assert schema in handlers, 'Schema not found'
        handler = handlers[schema]
        for line in handler(element):
            yield line


    def __iter_lines_of_mca_document(self, element):
        for xpath in XPATH_MCA_EXPRS:
            line_elements = element.xpath(xpath)
            print('found %s lines by xpath %s' % (len(line_elements), xpath))
            for el in line_elements:
                fragments = el.xpath('.//text()')
                if any(child.tag == 'br' for child in el.getchildren()):
                    for fragment in fragments:
                        yield fragment
                else:
                    yield u' '.join(fragments)


    def __iter_lines_of_normal_document(self, element):
        for xpath in XPATH_EXPRS:
            line_elements = element.xpath(xpath)
            for el in line_elements:
                fragments = el.xpath('.//text()')
                if any(child.tag == 'br' for child in el.getchildren()):
                    for fragment in fragments:
                        yield fragment
                else:
                    yield u' '.join(fragments)


    def __iter_lines_of_mass_document(self, element):
        for xpath in XPATH_MASS_EXPRS:
            fragments = [e.strip() for e in element.xpath(xpath)]
            stashed_fragments = []
            for fragment, next_fragment in self._predict(fragments):
                stashed_fragments.append(fragment)
                if next_fragment and next_fragment.isdigit() and stashed_fragments:
                    yield '\t'.join(f for f in stashed_fragments if f)
                    stashed_fragments = []
            yield '\t'.join(stashed_fragments)
    
    def _predict(self, iterable):
        collection = list(iterable)
        return itertools.izip_longest(collection, collection[1:])