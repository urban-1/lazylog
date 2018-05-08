SimpleLog
=========

Yet another python logger that aims to:

-  Simplify logging setup - down to config and a single line
-  Be minimal - single file, no dependencies
-  Supports console and file logging with different log levels,
   different format and file rotation out of the box
-  Prettify console output to be more human readable
-  Allow for easy JSON logging (TODO)
-  "Fix some issues" of the default logging facility:

   -  Handles new-lines in messages by either re-adding the preamble or
      escaping the new-line characters
   -  Adds color to the console, based on the log level
   -  Prettifies basic structures (list, dicts and tuples)
   -  Handles logfile permissions for multi-user deployments
   -  Supports easy logger mocking (into StringIO)

Usage
-----

Developing
----------

Create a Virtual Environment and install dev-tools

::

    python3 -m venv venv
    . venv/bin/activate
    pip install coverage pipreqs Sphinx autopep8

The project is controlled from the ``Makefile``:

::

    Please use `make <target>' where <target> is one of

    docs         to make standalone HTML files (in docs/build)
    reqs         to generate the pip requirements file in etc/
    autopep      to fix coding style in the project
    tests        to run project's tests (actually parsers)
    coverage     to run converage against the tests
    help         to print this message...

To generate documentation you will need ``pandoc`` installed locally on
your dev box. The target ``all`` will run ``autopep coverage reqs docs``
targets in order.
