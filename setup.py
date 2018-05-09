from distutils.core import setup

# Get the version
vesrion = check_output(["git", "describe", "--always"]).strip().decode("ascii")

setup(
  name = 'simplelog',
  packages = ['simplelog'],
  version = version,
  description = 'Yet another python logger that implifies json file logging and prettifies console output',
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
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3'
  ],
)
