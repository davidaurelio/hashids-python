#!/usr/bin/env python
# coding=utf-8
from __future__ import with_statement
from distutils.core import setup


with open('README.rst') as file:
    long_description = file.read()

setup(name='hashids',
      version='0.8.0',
      description='Python implementation of hashids (http://www.hashids.org).'
                  'Compatible with python 2.5--3.',
      long_description=long_description,
      author='David Aurelio',
      author_email='dev@david-aurelio.com',
      url='https://github.com/davidaurelio/hashids-python',
      license='MIT License',
      py_modules=('hashids',))
