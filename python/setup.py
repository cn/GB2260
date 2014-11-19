#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup


def fread(filepath):
    with open(filepath, 'r') as f:
        return f.read()


def version():
    content = fread('gb2260/__init__.py')
    pattern = r"__version__ = '([0-9\.]*)'"
    m = re.findall(pattern, content)
    return m[0]


setup(
    name='GB2260',
    version=version(),
    author='Hsiaoming Yang',
    author_email='me@lepture.com',
    url='https://github.com/cn/GB2260',
    packages=['gb2260'],
    description='',
    long_description=fread('README.rst'),
    license='WTFPL',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Debuggers',
    ]
)
