# SimpleLog

Yet another python logger that aims to:

-   Simplify logging setup - down to config and a single line
-   Be minimal - single file, no dependencies
-   Support console and file logging with different log levels, different format
    and file rotation out of the box
-   Prettify an align console output to be more human readable
-   Allow for easy JSON logging (TODO)
-   "Fix some issues" of the default logging facility:
    -   Handles new-lines in messages by either re-adding the preamble or escaping
        the new-line characters
    -   Adds color to the console, based on the log level
    -   Prettifies basic structures (list, dicts and tuples)
    -   Handles logfile permissions for multi-user deployments
    -   Supports easy logger mocking (into StringIO)


## Usage

[You can find all the sources of this section in `examples` folder]

### Basics

In the simplest form, you can initialize `simplelog` with:

    # Import the Logger class
    from simplelog import Logger

    # Initialize with all defaults
    Logger.init()


This creates a console-only logger with all the values set to their defaults:

    {
       'color': True,
       'splitLines': True,
       'level': logging.DEBUG,
       'pretty': True
    }

-   `color`: Instructs `simplelog` to use different colors for different levels
-   `splitLines`: Enables handling new-lines by re-printing the preamble on every
    line
-   `level`: As usual, sets the logging level for the terminal
-   `pretty`: Enables prettifying dicts, lists and tuples to be more readable

Once initialized you can use the `logging` module as usual - nothing special:

    logging.debug("This is an example log line")
    logging.info("This logger handles\nNew\nLines")
    logging.warning({"also": "handles basic structures", "like": list("lists"), "and": ("colors", "!")})
    logging.error("Errors stick out")
    logging.critical("but critical sticks out more...")

The output should look like:

![console with default settings](https://gitlab.com/urban-1/simplelog/raw/master/examples/images/console-defaults.png "Default console settings")

### Customizing

You can customize `simplelog` and disable any of the features you don't like, so

```
# Init
termSpecs = {"level": logging.DEBUG, "splitLines": False, "pretty": False }
Logger.init(LOGDIR, termSpecs=termSpecs)

# Use ...
logging.debug("You can remove all the fancy stuff:")
logging.info("... keeping\n each message\n in its own line")
logging.warning({"and": "flatten structures", "like": list("lists")})
```

gives you:

![console color only settings](https://gitlab.com/urban-1/simplelog/raw/master/examples/images/console-color-only.png "Console colour only")

... while initializing with:

    termSpecs = {"level": logging.DEBUG, "splitLines": True, "pretty": False }

gives you:

![Console no prettifying structs settings](https://gitlab.com/urban-1/simplelog/raw/master/examples/images/console-no-pretty.png "Console no prettifying structs")

Of course you can disable everything, falling back to the default `logging`
behaviour with the only difference being the log format:

![Console boring settings](https://gitlab.com/urban-1/simplelog/raw/master/examples/images/console-boring.png "Boring...")

## Developing

Create a Virtual Environment and install dev-tools

    python3 -m venv venv
    . venv/bin/activate
    pip install coverage pipreqs Sphinx autopep8

The project is controlled from the `Makefile`:

```
Please use `make <target>' where <target> is one of

docs         to make standalone HTML files (in docs/build)
reqs         to generate the pip requirements file in etc/
autopep      to fix coding style in the project
tests        to run project's tests (actually parsers)
coverage     to run converage against the tests
help         to print this message...
```

To generate documentation you will need `pandoc` installed locally on your dev
box. The target `all` will run `autopep coverage docs` targets in order.
