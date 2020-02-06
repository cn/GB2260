import os
import unittest

from parse.parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_by_content(self):
        destdir = '%s/tmp' % os.path.dirname(os.path.realpath(__file__))
        source = 'mca'
        revision = '201911'

        datadir = '%s/data' % os.path.dirname(os.path.realpath(__file__))
        with open('%s/201912251506.html' % datadir, 'r') as file:
            content = file.read()

        schema = 'mca'

        self.parser.parse_by_content(destdir, source, revision, content, schema)

if __name__ == '__main__':
    unittest.main()