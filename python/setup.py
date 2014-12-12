#!/usr/bin/env python

from setuptools import setup


def fread(filepath):
    with open(filepath, 'r') as f:
        return f.read()


setup(
    name='GB2260',
    version='0.2.0',
    author='Jiangge Zhang',
    author_email='tonyseek@gmail.com',
    url='https://github.com/cn/GB2260',
    packages=['gb2260'],
    description='The Python implementation for looking up the Chinese '
                'administrative divisions.',
    long_description=fread('README.rst'),
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
