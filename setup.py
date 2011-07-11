#!/usr/bin/env python
# Copyright (C) 2011  Rohan Jain
# Copyright (C) 2011  Alexis Le-Quoc
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from sys import version
from os.path import expanduser

if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(name='paster',
      version='0.7',
      description='A generic pastebin posting tool',
      long_description=open('README.md').read(),
      author='Rohan Jain',
      author_email='crodjer@gmail.com',
      url='https://github.com/crodjer/paster',
      packages = ['paster'],
      data_files=[(expanduser('~'), ['paster.cfg']),],
      license="GPLv3",
      platforms=["all"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Environment :: Plugins',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Topic :: Software Development',
          'Programming Language :: Python',
          ],
      scripts=['pstr'],
     )
