# Contributing

## Setup dev env

Create a Virtual Environment and install dev-tools

    python3 -m venv venv
    . venv/bin/activate
    pip install --upgrade coverage pipreqs Sphinx autopep8 twine wheel pip setuptools

The project is controlled from the `Makefile`:

```text
Please use `make <target>' where <target> is one of

  docs         to make standalone HTML files (in docs/build)
  reqs         to generate the pip requirements file in etc/
  autopep      to fix coding style in the project
  tests        to run project's tests (actually parsers)
  coverage     to run coverage against the tests
  dist         to push a new package to pypi (live)
  test_dist    to push a new package to test.pypi (test)
  distclean    to bring the folder in git-clone state
  help         to print this message...
```

To generate documentation you will need `pandoc` installed locally on your dev
box. The target `all` will run `autopep coverage docs` targets in order.

Coverage will be build and can be found in
[docs/build/html/_static/coverage/](http://simplelog.readthedocs.io/en/latest/_static/coverage/index.html).

## Versioning and releasing

This project uses `git describe` to generate version number and thus our format
is:

```text
 v0.2.32
  ^ ^  ^
  | |  |
  | |  number of commits since last tag (patch)
  | |
  | Minor version / release
  |
  Major version (along with minor form the tags `vX.Y`)
```

The project version is always in the format of `vX.Y` without the patch version,
however, releasing patches to pypi is also supported since pypi uses the full
version in `vX.Y.Z` format. To tag patch releases on Git (in order to track them)
we use `rX.Y.Z`.


### TODOs

Below is a list of features/ideas that have not been implemented either to keep
things simple, or because they were not needed by any of my projects. Feel free
to pick-em up or ask for them if you think are necessary.

- [ ] Maybe implement the `format` for termSpecs to allow JSON logging on the
  console.
- [ ] Log and date formats are currently class members of logging, modify to allow
  different handlers to have different formats
- [ ] Add support for Exception logging. At the moment this can be done "manually"
  with `traceback` module and `format_exc()`
- [ ] Same as formats, `LOGDIR` is considered to be one and is a static property.
  Change this to allow log-files in multiple locations
