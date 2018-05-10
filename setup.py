#!/usr/bin/env python
from setuptools import setup
from subprocess import check_output, PIPE

# Get the version
version = (check_output(["git", "describe", "--always", "--match", "v[0-9]*"])
         .strip()
         .decode("ascii"))

version = '.'.join(version.split("-")[:2])
print("\n*** FOUND VERSION: %s ***\n" % version)

setup(
  name = 'lazylog',
  packages = ['lazylog'],
  version = version,
  description = 'Yet another python logger that simplifies json file logging and prettifies console output',
  long_description=open("README.md").read(),
  long_description_content_type='text/markdown',
  author = 'Andreas Bontozoglou',
  author_email = 'bodozoglou@gmail.com',
  url = 'http://lazylog.readthedocs.io/en/latest/',
  project_urls={
    'Documentation': 'http://lazylog.readthedocs.io/en/latest/',
    'Source': 'https://github.com/urban-1/lazylog',
    'Tracker': 'https://github.com/urban-1/lazylog/issues',
  },
  download_url = 'https://github.com/urban-1/lazylog/archive/master.tar.gz',
  keywords = ['logging', 'color', 'logfile', 'json'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Topic :: System :: Logging',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
  ],
)
