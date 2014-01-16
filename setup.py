#!/usr/bin/env python
 
from setuptools import setup
 
setup(name='pawn',
      version='0.1.0',
      description='Concurrent Servers for Humans.',
      author='James Dennis',
      author_email='jdennis@gmail.com',
      url='http://github.com/j2labs/pawn',
      packages=['pawn'],
      install_requires=['gevent',])
