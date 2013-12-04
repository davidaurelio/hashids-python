#!/usr/bin/env python
from distutils.core import setup
from os.path import dirname, join

setup(name='hashids',
      version='0.8.3',
      description='Python implementation of hashids (http://www.hashids.org).'
                  'Compatible with python 2.5--3.',
      long_description=open(join(dirname(__file__), 'README.rst'), 'r', -1, 'utf-8').read(),
      author='David Aurelio',
      author_email='dev@david-aurelio.com',
      url='https://github.com/davidaurelio/hashids-python',
      license='MIT License',
      py_modules=('hashids',))
