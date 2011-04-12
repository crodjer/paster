#!/usr/bin/env python
##try:
##    from setuptools import setup, find_packages
##    have_setuptools = True
##except:
##    from distutils.core import setup
from distutils.core import setup
from sys import version
try:
    import markdown
    #from markdown import markdown
    markdown_available = True
except ImportError:
    markdown_available = False

if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

def long_description():
    DESC = open('README.md').read()
    if markdown_available:
        return markdown.markdown(DESC)
    else:
        return DESC

setup(name='paster',
      version='0.6',
      description='A generic pastebin posting tool',
      long_description=long_description(),
      author='Rohan Jain',
      author_email='crodjer@gmail.com',
      url='https://github.com/crodjer/paster',
      packages = ['paster'],
      data_files=[('/etc', ['paster.cfg']),],
      license="GPLv3",
      platforms=["all"],
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python',
          ],
      scripts=['pstr'],
     )
