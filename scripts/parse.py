# coding: utf-8

import requests
from lxml.html import fromstring


URL = 'http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201401/t20140116_501070.html'

req = requests.get(URL)
req.encoding = 'utf-8'
el = fromstring(req.text)

for line in el.find_class('MsoNormal'):
    text = line.text_content().strip()
    if text:
        code, name = text.split()
        out = '%s\t%s' % (code, name)
        print(out.encode('utf-8'))
