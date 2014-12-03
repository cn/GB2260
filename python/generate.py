#!/usr/bin/env python

"""
A script to generate the data module.
"""

from __future__ import print_function, unicode_literals

import sys
import pprint


def main():
    try:
        _, source, destination = sys.argv
    except ValueError:
        print('Usage: {.argv[0]} [SOURCE] [DESTINATION]'.format(sys),
              file=sys.stderr)
        sys.exit(1)

    data = {}

    with open(source, 'r') as source_file:
        for line in source_file:
            code, name = line.strip().split()
            data[int(code)] = name.decode('utf-8')

    items = pprint.pformat(data, indent=4).strip('{}')
    result = '\n'.join(['data = {', ' {0} '.format(items), '}'])

    with open(destination, 'w') as destination_file:
        print(result, file=destination_file)

    print('{0} records has been generated.'.format(len(data)), file=sys.stderr)


if __name__ == '__main__':
    main()
