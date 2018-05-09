#!/usr/bin/env python
from distutils.core import setup
from subprocess import check_output, PIPE

# Get the version
version = check_output(["git", "describe", "--always"]).strip().decode("ascii")
version = '-'.join(version.split('-')[:2])

setup(
  name = 'simplelog',
  packages = ['simplelog'],
  version = version,
  description = 'Yet another python logger that implifies json file logging and prettifies console output',
  long_description=open("README.md").read(),
  long_description_content_type='text/markdown',
  author = 'Andreas Bontozoglou',
  author_email = 'bodozoglou@gmail.com',
  url = 'https://github.com/urban-1/simplelog',
  download_url = 'https://github.com/urban-1/simplelog/archive/master.tar.gz',
  keywords = ['logging', 'color', 'logfile', 'json'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Topic :: System :: Logging',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',,
    'Programming Language :: Python :: 2.6'
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
  ],
)
