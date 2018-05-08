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

<pre style="color:white; font-weight:normal;background-color:black">
<code style="color:white; background-color:black"><span style="color:gray;">08-05-2018 21:40:16.943 13859:139943539918656 DEBUG            console 17  : This is an example log line</span>
<span style="color:teal;">08-05-2018 21:40:16.943 13859:139943539918656 INFO             console 18  : This logger handles
08-05-2018 21:40:16.943 13859:139943539918656 INFO             console 18  : New
08-05-2018 21:40:16.943 13859:139943539918656 INFO             console 18  : Lines</span>
<span style="color:#9E5C15;">08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  : (dict) {
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :    'and': (
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :            'colors',
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :            '!'
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :    ),
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :    'like': [
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :            'l',
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :            'i',
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :            's',
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :            't',
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :            's'
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :    ],
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  :    'also': 'handles basic structures'
08-05-2018 21:40:16.943 13859:139943539918656 WARNING          console 19  : }</span>
<span style="color:red;font-weight:bold;">08-05-2018 21:40:16.943 13859:139943539918656 ERROR            console 20  : Errors stick out</span>
<span style="color:yellow;font-weight:bold;">08-05-2018 21:40:16.943 13859:139943539918656 CRITICAL         console 21  : but critical sticks out more...</span>
</code></pre>


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

<pre style="color:white; background-color:black"><code><span style="color:gray; background-color:black">08-05-2018 21:19:40.688 11639:140599510849344 DEBUG    console_customi 18  : You can remove all the fancy stuff:</span>
<span style="color:teal; background-color:black">08-05-2018 21:19:40.689 11639:140599510849344 INFO     console_customi 19  : ... keeping\n each message\n in its own line</span>
<span style="color:#9E5C15; background-color:black">08-05-2018 21:19:40.689 11639:140599510849344 WARNING  console_customi 20  : {'like': ['l', 'i', 's', 't', 's'], 'and': 'flatten structures'}</span>
</code></pre>

... while initializing with:

    termSpecs = {"level": logging.DEBUG, "splitLines": True, "pretty": False }

gives you:

<pre style="color:white; background-color:black"><code><span style="color:red;font-weight:bold; background-color:black">08-05-2018 21:30:05.312 12648:140218785630016 ERROR    console_customi 25  : However,
08-05-2018 21:30:05.312 12648:140218785630016 ERROR    console_customi 25  : You can choose to split
08-05-2018 21:30:05.312 12648:140218785630016 ERROR    console_customi 25  : lines</span>
<span style="color:yellow;font-weight:bold; background-color:black">08-05-2018 21:30:05.312 12648:140218785630016 CRITICAL console_customi 26  : ['but', 'not', 'prettify\nstructs']</span>
</code></pre>

Of course you can disable everything, falling back to the default `logging`
behaviour with the only difference being the log format:

<pre style="color:white; background-color:black"><code style="color:white; background-color:black">08-05-2018 21:30:05.312 12648:140218785630016 INFO     console_customi 31  : Boooriiiing
</code></pre>

### Files

In case where you (the developer) are not the one running the code, you most
probably need a log-file! If you application is a CLI one, probably the end-user
should not be seeing all the debugging info, but warnings and errors only. Python
logging facility supports multiple handlers working simultaneously and `simplelog`
allows you to use this feature hassle-free. To define a file logger do:

    termSpecs = {"level": logging.DEBUG}
    fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG}]
    Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

The above creates a file in `LOGDIR/LOGFILE` with the default settings which are:

    {
        'format': 'console'
        'backupCount': 20
        'maxBytes': 10MB
        'color': False,
        'splitLines': True,
        'pretty': False
    }

-   `backupCount`: Is the number of files we keep
-   `maxBytes`: Is the maximum file size, after which rotation takes place
-   `format`: Controls which LogFormatter is being used. By default the
    ColorFormatter is used and thus the options `color`, `splitLines` and
    `pretty` are also supported. Other values include: `default` and `json`
    which we will see later on

The above settings produce the following output in the file:

```
08-05-2018 15:57:24.118 16142:140509479982912 DEBUG            logfile 23  : ^---same as console, this is an example log line
08-05-2018 15:57:24.118 16142:140509479982912 INFO             logfile 24  : This logger handles
08-05-2018 15:57:24.118 16142:140509479982912 INFO             logfile 24  : New
08-05-2018 15:57:24.118 16142:140509479982912 INFO             logfile 24  : Lines
08-05-2018 15:57:24.119 16142:140509479982912 WARNING          logfile 25  : {'but': 'Flattens structs by default'}
08-05-2018 15:57:24.119 16142:140509479982912 ERROR            logfile 26  : Errors DONT stick out - color is not used
```

with `splitLines: False` you get:

```
# Code:
# logging.info("Like console\nYou can avoid\nsplitting lines")

08-05-2018 15:57:24.119 16142:140509479982912 INFO             logfile 42  : Like console\nYou can avoid\nsplitting lines
```


while with `pretty: True` you get:

```
# Code:
# logging.info({"or": "enable prettifying!"})

08-05-2018 15:57:24.120 16142:140509479982912 INFO             logfile 55  : (dict) {
08-05-2018 15:57:24.120 16142:140509479982912 INFO             logfile 55  :    'or': 'enable prettifying!'
08-05-2018 15:57:24.120 16142:140509479982912 INFO             logfile 55  : }
```

#### JSON format

JSON logging is most useful when we need to index our logs to a database or
stream them and generally for machine-to-machine communication. At the moment,
`simplelog` does not support JSON logging on the terminal but does support it
for files. To enable it, initialize with:

```
fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "format":"json"}]
```

The following ways of logging are supported:

```
logging.info("Simple str message")
logging.warning("Message with metadata", extra={"user": "nwj12"})
logging.debug({"what": "dict-based logging"}, extra={"user": "asd32"})
logging.info(["anything", "json", "serializable", "see OBJECT"], extra={"foo":"bar"})
```

and the results will be:

```
{
    "filename": "logfile.py",
    "module": "logfile",
    "timestamp": 1525799704.8904743,
    "message": "Simple str message",
    "thread": 140193498228544,
    "levelname": "INFO",
    "process": 27529
}

{
    "filename": "logfile.py",
    "user": "nwj12",
    "module": "logfile",
    "timestamp": 1525799704.890644,
    "message": "Message with metadata",
    "thread": 140193498228544,
    "levelname": "WARNING",
    "process": 27529
}

{
    "filename": "logfile.py",
    "user": "asd32",
    "module": "logfile",
    "what": "dict-based logging",
    "timestamp": 1525799704.8907733,
    "message": "",
    "process": 27529,
    "levelname": "DEBUG",
    "thread": 140193498228544
}

{
    "filename": "logfile.py",
    "timestamp": 1525799704.8909438,
    "module": "logfile",
    "thread": 140193498228544,
    "foo": "bar",
    "message": "",
    "process": 27529,
    "levelname": "INFO",
    "object": [
        "anything",
        "json",
        "serializable",
        "see OBJECT"
    ]
}


```


#### Default format

I would really not suggest this... but you get

```
# Code:
# logging.info("You\n can set the \n format to\n default")
# logging.warning("But I don't like it...")

08-05-2018 15:57:24.120 16142:140509479982912 INFO             logfile 70  : You
 can set the
 format to
 default
08-05-2018 15:57:24.120 16142:140509479982912 WARNING          logfile 71  : But I don't like it...
```

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
