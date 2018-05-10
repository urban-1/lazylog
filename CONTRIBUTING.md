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
The target `all` will run `autopep coverage docs` targets in order. Coverage will be build and can be found in
[docs/build/html/_static/coverage/](http://simplelog.readthedocs.io/en/latest/_static/coverage/index.html).


To generate documentation you will need `pandoc` installed locally on your dev
box:

    # Debian
    sudo apt-get install pandoc

    # RHEL (you might need epel-release repo enabled)
    sudo yum install pandoc

    # Mac
    brew install pandoc

## Branching

Basic rules only, use:

-   `fix_` for bug patching
-   `feature_` for new features: One feature in each branch (I know is tempting
    ... but adding more than one things in a branch causes a lot of trouble l
    ater!)


## Versioning

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
version in `-X.Y.Z` format. To tag patch releases on Git (in order to track them)
we use `rX.Y.Z` so `git describe` is not picking these tags up. Basic rules:

-   Patch releases should never change API or introduce new features
-   Minor version releases should be tagged and should not change API, but they
    can introduce new features
-   Major will be upped either because of API changes, or arbitrarily to lower
    the minor and patch numbers

## Releasing

The release process (WIP)

-   `git merge` to bring the master up to date with any feature branches
-   `make tests` to ensure everything is passing (or wait for Travis to finish).
    Up until here you can still make changes and run tests again.
-   `git tag` as required: `rX.Y.Z` for patches. `vX.Y` for major/minor releases
-   `make all` to run tests, generate coverage and docs
-   `make dist` will push to pypi
-   `git push` and `git push --tags` to trigger readthedocs and update the repo

All releases should be tested on test.pypi.org first to verify that it looks ok.
You can use `make test_dist` to do this.

## TODOs

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
