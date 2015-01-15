#!/usr/bin/env python
from setuptools import setup
from os.path import dirname, join
from codecs import open

setup(name='hashids',
      version='1.0.2',
      description='Python implementation of hashids (http://www.hashids.org).'
                  'Compatible with python 2.6, 2.7 and 3.3+.',
      long_description=open(join(dirname(__file__), 'README.rst'), encoding='utf-8').read(),
      author='David Aurelio',
      author_email='dev@david-aurelio.com',
      url='https://github.com/davidaurelio/hashids-python',
      license='MIT License',
      install_requires=['future >= 0.14.3'],
      py_modules=('hashids',))
