# SimpleLog

Yet another python logger that aims to:

-   Simplify logging setup - down to config and a single line
-   Be minimal - single file, no dependencies
-   Supports console and file logging with different log levels, different format
    and file rotation out of the box
-   Prettify console output to be more human readable
-   Allow for easy JSON logging (TODO)
-   "Fix some issues" of the default logging facility:
    -   Handles new-lines in messages by either re-adding the preamble or escaping
        the new-line characters
    -   Adds color to the console, based on the log level
    -   Prettifies basic structures (list, dicts and tuples)
    -   Handles logfile permissions for multi-user deployments
    -   Supports easy logger mocking (into StringIO)


## Usage



## Developing

Create a Virtual Environment and install coverage

    python3 -m venv venv
    . venv/bin/activate
    pip install coverage pipreqs Sphinx

### Coverage

    coverage run --include=simplelog/* test.py
    coverage html -d docs/coverage
