

import logging
import logging.handlers
import os
import stat
import collections
from io import StringIO


# http://docs.python.org/library/logging.html#logrecord-attributes
# RESERVED_ATTRS = (
#     'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
#     'funcName', 'levelname', 'levelno', 'lineno', 'module',
#     'msecs', 'message', 'msg', 'name', 'pathname', 'process',
#     'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName')

class Logger(logging.getLoggerClass()):
    """
    Core logger for all apps and scripts. This logger adds the following features
    to the default:

    - Colors!
    - Cooler line format
    - Function is included in the log format
    - File log
    - File rotation every 5M with 100 files kept


    """

    LOGDIR = "/var/log"
    """Log directory, it will be created if it does not exist"""

    MAXBYTES = 10000000
    """Default maximum file size allowed, after that rotation is taking place"""

    BACKUPCOUNT = 20
    """Default number of backup files to keep"""

    DATEFORMAT = '%d-%m-%Y %H:%M:%S'
    """Date output format"""

    LOGFORMAT = '%(asctime)s.%(msecs)03d %(process)s:%(thread)u %(levelname)-8s %(module)15.15s %(lineno)-4s: %(message)s'

    TERMSPECS = {
       "color": True,
       "splitLines": True,
       "level": logging.DEBUG,
       "pretty": True
    }

    @classmethod
    def _chkdir(cls):
        """
        Check that the loggin dir exists and create it if not
        """
        if not os.path.isdir(cls.LOGDIR):
            try:
                mkdir_p(cls.LOGDIR)
            except:
                # Do not log... logging here enables the
                # root logger...
                pass

    @classmethod
    def addFileLogger(cls, specs):
        """
        Add a file logger with the given specs. Specs:

        {
            "filename": Filename (under LOGDIR)
            "level": Logging level for this file
            "format": [ "json" | "console" | "default" ] # TODO: CSV
            "splitLines": Split new lines in when logging
            "backupCount": Number of files to keep
            "maxBytes": Maximum file size
        }
        """

        root = logging.getLogger()

        if "filename" not in specs:
            logging.error("'filename' missing from file specs... skipping!")
            return

        if "level" not in specs:
            specs["level"] = logging.INFO

        filePath = cls.LOGDIR + "/" + specs["filename"]

        # Test that we can access the file
        try:
            # Make sure the file is there
            fhandle = open(filePath, 'a')
            fhandle.close()
        except:
            logging.error("NOT Initializing File Logging: File-system permissions error: \n\t%s" % filePath)
            # No point doing anything else!
            return

        # If we just created it, set correct permissions so that is group accessible
        # This often crashes apps in multiuser environmnets
        try:
            # Correct permissions
            perms = (stat.S_IREAD | stat.S_IWRITE | stat.S_IWOTH |
                     stat.S_IROTH | stat.S_IWGRP | stat.S_IRGRP)
            os.chmod(filePath, perms)
        except Exception as e:
            # Error here can appear if another user owns the file...
            pass

        # Register the rotating file handler
        rotFileH = logging.handlers.RotatingFileHandler(
            filePath,
            backupCount=specs["backupCount"] if "backupCount" in specs else cls.BACKUPCOUNT,
            maxBytes=specs["maxBytes"] if "maxBytes" in specs else cls.MAXBYTES)

        formatter = logging.Formatter(cls.LOGFORMAT, datefmt=cls.DATEFORMAT)
        if "format" not in specs or specs["format"] == "default":
            pass
        elif specs["format"] == "console":
            formatter = ColorFormatter(cls.LOGFORMAT, datefmt=cls.DATEFORMAT, color=False)
        elif specs["format"] == "json":
            # formatter = JSONFormatter(cls.LOGFORMAT, datefmt=cls.DATEFORMAT)
            raise NotImplementedError("Hmmm... JSON not there yet")

        rotFileH.setFormatter(formatter)
        rotFileH.setLevel(specs["level"])
        rotFileH.propagate = False
        root.addHandler(rotFileH)

    @classmethod
    def init(cls,
             folder="/var/log/simplelog",
             termSpecs={},
             fileSpecs=None
        ):
        """
        Intialize logging based on the requested fileName. This
        will create one logger (global) that writes in both file
        and terminal

        :param str fileSpecs: A dict with "filename", "level", etc. See addFileLogger
                              for details
        :param int termSpecs: A dict with boolean values for "color" and "splitLines"
        """

        logging.setLoggerClass(cls)
        cls.LOGDIR = folder

        # Check folder
        cls._chkdir()

        # Merge with defaults...
        termSpecs = merge_dicts(termSpecs, cls.TERMSPECS.copy())

        # Disable default logger
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        root.handlers = []

        # Console logger
        console = logging.StreamHandler()
        console.setLevel(termSpecs["level"])

        formatter = ColorFormatter(
            cls.LOGFORMAT,
            datefmt=cls.DATEFORMAT,
            color=termSpecs["color"],
            splitLines=termSpecs["splitLines"],
            pretty=termSpecs["pretty"])

        console.setFormatter(formatter)
        console.propagate = False
        root.addHandler(console)

        # File logger
        if fileSpecs is not None:
            for specs in fileSpecs:
                cls.addFileLogger(specs)

    @staticmethod
    def logFun():
        """Print one message in each level to demo the colours"""
        logging.debug('All set in logger!')
        logging.info('This is how INFO lines are')
        logging.warning('Warnings here')
        logging.critical('Critical stuff appear like this')
        logging.error('Look out for ERRORs')

    @staticmethod
    def setConsoleLevel(level):
        logging.getLogger().handlers[0].setLevel(level)

    @staticmethod
    def setFileLevel(filenum, level):
        """
        Set a file logger log level. Filenum is 1,2,3,.. in the order the
        files have been added.
        """
        if len(logging.getLogger().handlers) < filenum + 1:
            return

        logging.getLogger().handlers[filenum].setLevel(level)

    @staticmethod
    def mockHandler(index):
        if len(logging.getLogger().handlers) < index + 1:
            return

        h = logging.getLogger().handlers[index]

        h.old_stream = h.stream
        h.stream = StringIO()
        return h.stream

    @staticmethod
    def restoreHandler(index):
        if len(logging.getLogger().handlers) < index + 1:
            return

        h = logging.getLogger().handlers[index]

        if not hasattr(h, "old_stream"):
            return

        h.stream = h.old_stream
        del h.old_stream


class ColorFormatter(logging.Formatter):
    """
    Color formatter. This class is working as expected atm but it can
    be tidied up to support blinking text and other useless features :)
    """

    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    """ Bash Colors """

    NORM, BOLD, UNK, ITAL, UNDER, BLINK, UNK2, INV, CON = range(9)
    """ Bash Styles """

    ESC = "\033["
    """Escape sequence for color"""
    COLOR_SEQ = "\033[1;%dm"
    """Escape seq. + color integer placeholder"""
    RESET_SEQ = "\033[0m"
    """Reset color sequence"""

    def __init__(self, fmt, datefmt=None, color=True, splitLines=True, pretty=False):
        """
        Init given the log line format, color and date format
        """
        logging.Formatter.__init__(self, fmt, datefmt)
        self.color = color
        self.splitLines = splitLines
        self.pretty = pretty

        ColorFormatter.COLORS = {
            'DEBUG': ColorFormatter.WHITE,
            'INFO': ColorFormatter.CYAN,
            'WARNING': ColorFormatter.YELLOW,
            'CRITICAL': ColorFormatter.YELLOW,
            'ERROR': ColorFormatter.RED
        }

        ColorFormatter.STYLES = {
            'DEBUG': ColorFormatter.NORM,
            'INFO': ColorFormatter.NORM,
            'WARNING': ColorFormatter.NORM,
            'CRITICAL': ColorFormatter.BOLD,
            'ERROR': ColorFormatter.BOLD
        }

    def format(self, record):
        """
        Override format function
        """
        levelname = record.levelname

        # NOTE: `message` is formatted, `msg` is raw
        if self.pretty and (
            isinstance(record.msg, dict) or
            isinstance(record.msg, tuple) or
            isinstance(record.msg, list)
            ):
            record.msg = pretty(record.msg)


        msg = logging.Formatter.format(self, record)


        if self.splitLines and record.message != "":
            parts = msg.split(record.message)
            msg = msg.replace('\n', '\n' + parts[0])

        # The background is set with 40 plus the number of the color,
        # and the foreground with 30
        if self.color and levelname in ColorFormatter.COLORS:
            msg = "%s%d;%dm%s%s" % (
                ColorFormatter.ESC,
                ColorFormatter.STYLES[levelname],
                30 + ColorFormatter.COLORS[levelname],
                msg,
                ColorFormatter.RESET_SEQ)
            return msg

        return msg


class JSONFormatter(logging.Formatter):
    """
    Format messages as JSON

    https://github.com/madzak/python-json-logger/blob/master/src/pythonjsonlogger/jsonlogger.py
    """

    def __init__(self, fields):
        self.fields = fields

    def format(self, record):
        """
        Override format function
        """
        return json.dumps({
            "FIXME": ""
        })

def pretty_recursive(value, htchar='\t', lfchar='\n', indent=0):
    """
    Pretty printing, full creadit to:

        http://stackoverflow.com/questions/3229419/pretty-printing-nested-dictionaries-in-python

    """
    nlch = lfchar + htchar * (indent + 1)

    if isinstance(value, dict) or isinstance(value, collections.MutableMapping):
        items = [
            nlch + repr(key) + ': ' + pretty_recursive(value[key], htchar, lfchar, indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + lfchar + htchar * indent)
    elif isinstance(value, list):
        items = [
            nlch + pretty_recursive(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + lfchar + htchar * indent)
    elif isinstance(value, tuple):
        items = [
            nlch + pretty_recursive(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + lfchar + htchar * indent)
    else:
        return repr(value)


def pretty(sth):
    """
    Format objects, tuples, lists and dicts for pretty printing
    """
    if sth is None:
        return sth

    prefix = ''
    if sth.__class__.__name__:
        prefix = "(%s) " % format(sth.__class__.__name__)

    return prefix + pretty_recursive(sth)


def mkdir_p(path):
    """
    Does the same as 'mkdir -p' in linux
    """
    if os.path.exists(path):
        return

    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise exc


def merge_dicts(source, destination):
    """
    run me with nosetests --with-doctest file.py - https://stackoverflow.com/a/20666342/3727050

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge_dicts(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination
