#!/usr/bin/env python

"""
A script to generate the data module.
"""

from __future__ import print_function, unicode_literals

import os
import sys
import pprint


def get_name_suffix(path):
    path, _ = os.path.splitext(path)
    splited = path.rsplit('-', 1)
    if len(splited) == 2:
        return splited[-1]
    return ''


def main():
    if len(sys.argv) < 3:
        print('Usage: {.argv[0]} [A] [B] ... [DESTINATION]'.format(sys),
              file=sys.stderr)
        sys.exit(1)
    source = sys.argv[1:-1]
    destination = sys.argv[-1]

    data = {}
    for current_source in source:
        suffix = get_name_suffix(current_source)
        current_dict = data.setdefault(int(suffix) if suffix else None, {})

        with open(current_source, 'r') as source_file:
            for line in source_file:
                code, name = line.strip().split()
                current_dict[int(code)] = name.decode('utf-8')

    result = 'data = {0}'.format(repr(data))
    with open(destination, 'w') as destination_file:
        print(result, file=destination_file)

    for current_dict in data.values():
        message = '{0} records has been generated.'.format(len(current_dict))
        print(message, file=sys.stderr)


if __name__ == '__main__':
    main()
