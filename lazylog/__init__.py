import os
import stat
import json
import copy
import logging
import collections
import logging.handlers

try:
    from StringIO import StringIO
    str_types = basestring,
except BaseException:
    from io import StringIO
    str_types = str,


class Logger(logging.getLoggerClass()):
    '''
    Core logger for all apps and scripts. This logger adds the following features
    to the default:

    - Colors!
    - Cooler line format
    - Function is included in the log format
    - File log
    - File rotation every 5M with 100 files kept


    '''

    LOGDIR = '/var/log'
    '''Log directory, it will be created if it does not exist'''

    MAXBYTES = 10000000
    '''Default maximum file size allowed, after that rotation is taking place'''

    BACKUPCOUNT = 20
    '''Default number of backup files to keep'''

    DATEFORMAT = '%d-%m-%Y %H:%M:%S'
    '''Date output format'''

    LOGFORMAT = '%(asctime)s.%(msecs)03d %(process)s:%(thread)u %(levelname)-8s %(module)15.15s %(lineno)-4s: %(message)s'
    '''Default log format for all handlers. This can change in :py:meth:`init`'''

    @classmethod
    def _chkdir(cls):
        '''
        Check that the loggin dir exists and create it if not
        '''
        if not os.path.isdir(cls.LOGDIR):
            try:
                mkdir_p(cls.LOGDIR)
            except BaseException:
                # Do not log... logging here enables the
                # root logger...
                pass

    @classmethod
    def addFileLogger(cls, specs):
        '''
        Add a file logger with the given specs. Specs::

            {
                'filename': Filename (under LOGDIR)
                'level': Logging level for this file
                'format': [ 'json' | 'console' | 'default' ] # TODO: CSV
                'backupCount': Number of files to keep
                'maxBytes': Maximum file size
            }

        If format is set to "console", then ColorFormatter options are also
        supported.
        '''

        root = logging.getLogger()

        if 'filename' not in specs:
            raise RuntimeError('"filename" missing from file specs... skipping!')

        if 'level' not in specs:
            specs['level'] = logging.INFO

        filePath = cls.LOGDIR + '/' + specs['filename']

        # Test that we can access the file
        try:
            # Make sure the file is there
            fhandle = open(filePath, 'a')
            fhandle.close()
        except BaseException:
            logging.error('NOT Initializing File Logging: File-system permissions error: \n\t%s' % filePath)
            # No point doing anything else! BUT do not raise exception
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
            backupCount=specs['backupCount'] if 'backupCount' in specs else cls.BACKUPCOUNT,
            maxBytes=specs['maxBytes'] if 'maxBytes' in specs else cls.MAXBYTES)

        fmt = specs["fmt"] if "fmt" in specs else cls.USER_LOGFORMAT
        datefmt = specs["datefmt"] if "datefmt" in specs else cls.USER_DATEFORMAT

        formatter = logging.Formatter(fmt, datefmt=datefmt)
        if 'format' not in specs or specs['format'] == 'console':
            specs = ColorFormatter.parseSpecs(specs, ColorFormatter.FILEDEFAULTS)
            formatter = ColorFormatter(
                fmt,
                datefmt=datefmt,
                color=False,
                pretty=specs['pretty'],
                splitLines=specs['splitLines'])

        elif specs['format'] == 'default':
            pass
        elif specs['format'] == 'json':
            # Set to defaults
            if 'fields' not in specs:
                specs['fields'] = JSONFormatter.FIELDS

            formatter = JSONFormatter(specs['fields'])

        rotFileH.setFormatter(formatter)
        rotFileH.setLevel(specs['level'])
        rotFileH.propagate = False
        root.addHandler(rotFileH)

    @classmethod
    def init(cls,
             folder='/var/log/lazylog',
             termSpecs={},
             fileSpecs=None,
             fmt=None,
             datefmt=None
             ):
        '''
        Intialize logging based on the requested fileName. This
        will create one logger (global) that writes in both file
        and terminal

        :param str fileSpecs: A dict with 'filename', 'level', etc. See addFileLogger
                              for details
        :param int termSpecs: A dict with boolean values for 'color' and 'splitLines'
        '''

        logging.setLoggerClass(cls)

        cls.LOGDIR = folder

        if fmt is None:
            fmt = cls.LOGFORMAT

        if datefmt is None:
            datefmt = cls.DATEFORMAT

        # Store those statically as the last user supplied format. This will be
        # used from now on if format is not specified
        cls.USER_LOGFORMAT = fmt
        cls.USER_DATEFORMAT = datefmt

        # Check folder and create if needed
        cls._chkdir()

        # Merge with defaults...
        termSpecs = ColorFormatter.parseSpecs(termSpecs, ColorFormatter.TERMDEFAULTS)

        # Disable default logger
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        root.handlers = []

        # Console logger
        console = logging.StreamHandler()
        console.setLevel(termSpecs['level'])
        formatter = ColorFormatter(
            fmt,
            datefmt=datefmt,
            color=termSpecs['color'],
            splitLines=termSpecs['splitLines'],
            pretty=termSpecs['pretty'])

        console.setFormatter(formatter)
        console.propagate = False
        root.addHandler(console)

        # File logger
        if fileSpecs is not None:
            for specs in fileSpecs:
                cls.addFileLogger(specs)

    @staticmethod
    def logFun():
        '''Print one message in each level to demo the colours'''
        logging.debug('All set in logger!')
        logging.info('This is how INFO lines are')
        logging.warning('Warnings here')
        logging.critical('Critical stuff appear like this')
        logging.error('Look out for ERRORs')

    @staticmethod
    def setConsoleLevel(level):
        """
        In this logger, by convention, handler 0 is always the console halder.
        """
        logging.getLogger().handlers[0].setLevel(level)

    @staticmethod
    def setFileLevel(filenum, level):
        '''
        Set a file logger log level. Filenum is 1,2,3,.. in the order the
        files have been added.
        '''
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

        if not hasattr(h, 'old_stream'):
            return

        h.stream = h.old_stream
        del h.old_stream


class ColorFormatter(logging.Formatter):
    '''
    Color formatter. This class is working as expected atm but it can
    be tidied up to support blinking text and other useless features :)
    '''

    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    ''' Bash Colors '''

    NORM, BOLD, UNK, ITAL, UNDER, BLINK, UNK2, INV, CON = range(9)
    ''' Bash Styles '''

    ESC = '\033['
    '''Escape sequence for color'''
    COLOR_SEQ = '\033[1;%dm'
    '''Escape seq. + color integer placeholder'''
    RESET_SEQ = '\033[0m'
    '''Reset color sequence'''

    TERMDEFAULTS = {
        'color': True,
        'splitLines': True,
        'level': logging.DEBUG,
        'pretty': True
    }
    '''Terminal default settings'''

    FILEDEFAULTS = {
        'color': False,
        'splitLines': True,
        'level': logging.INFO,
        'pretty': False
    }
    '''File default settings'''

    STYLES = {
        'DEBUG': NORM,
        'INFO': NORM,
        'WARNING': NORM,
        'CRITICAL': BOLD,
        'ERROR': BOLD
    }
    """Each log-level's default character style"""

    COLORS = {
        'DEBUG': WHITE,
        'INFO': CYAN,
        'WARNING': YELLOW,
        'CRITICAL': YELLOW,
        'ERROR': RED
    }
    """Default color values for each log-level"""

    def __init__(self, fmt, datefmt=None, color=True, splitLines=True, pretty=False, colors=None, styles=None):
        '''
        Init given the log line format, color and date format
        '''
        logging.Formatter.__init__(self, fmt, datefmt)
        self.color = color
        self.splitLines = splitLines
        self.pretty = pretty

        self.colors = colors if colors is not None else ColorFormatter.COLORS
        self.styles = styles if styles is not None else ColorFormatter.STYLES

    def format(self, record):
        '''
        Override format function
        '''
        levelname = record.levelname

        # Keep reference and copy only if required
        tmp_record = record

        # NOTE: `message` is formatted, `msg` is raw
        if self.pretty and (
            isinstance(record.msg, dict) or
            isinstance(record.msg, tuple) or
            isinstance(record.msg, list)
        ):

            # Copy so we do not modify the original message
            tmp_record = copy.copy(record)
            tmp_record.msg = pretty(tmp_record.msg)

        msg = logging.Formatter.format(self, tmp_record)

        if self.splitLines and tmp_record.message != '':
            parts = msg.split(tmp_record.message)
            msg = msg.replace('\n', '\n' + parts[0])
        # Escape new lines so the full message is in a single line
        elif not self.splitLines and msg != '':
            msg = msg.replace('\n', '\\n')

        # The background is set with 40 plus the number of the color,
        # and the foreground with 30
        if self.color and levelname in self.colors:
            msg = '%s%d;%dm%s%s' % (
                ColorFormatter.ESC,
                self.styles[levelname],
                30 + self.colors[levelname],
                msg,
                ColorFormatter.RESET_SEQ)
            return msg

        return msg

    @staticmethod
    def parseSpecs(specs, defaults):
        '''
        Merge the user specs with the defaults given (terminal or file). Also
        ensure that if ``pretty`` is set, ``splitLines`` is also set (implied)
        '''
        specs = merge_dicts(specs, defaults.copy())

        # Pretty overrides split lines
        specs['pretty'] = specs['pretty'] if 'pretty' in specs else False
        specs['splitLines'] = specs['splitLines'] if 'splitLines' in specs else False
        if specs['pretty'] and not specs['splitLines']:
            specs['splitLines'] = True

        return specs


class JSONFormatter(logging.Formatter):
    '''
    Format messages as JSON

    Lots of ideas from:

        https://github.com/madzak/python-json-logger/blob/master/src/pythonjsonlogger/jsonlogger.py


    '''

    # http://docs.python.org/library/logging.html#logrecord-attributes
    RESERVED_ATTRS = (
        'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
        'funcName', 'levelname', 'levelno', 'lineno', 'module',
        'msecs', 'message', 'msg', 'name', 'pathname', 'process',
        'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName')

    FIELDS = [
        'created',
        'process',
        'thread',
        'levelname',
        'module',
        'filename',
        'funcName'
        'lineno',
        'message',
    ]

    def __init__(self, fields, datefmt=None):
        self.fields = fields
        if "created" not in self.fields:
            self.fields.append("created")

    def format(self, record):
        '''
        Override format function
        '''
        result = {
            "message": ""
        }

        # Assign string to message
        if isinstance(record.msg, str_types):
            result["message"] = record.msg
        # Merge as dict
        elif isinstance(record.msg, dict):
            result = merge_dicts(record.msg, result)
        # Serialize as object
        else:
            result["object"] = record.msg

        # Now merge any extra
        for k, v in record.__dict__.items():
            # Required attrs
            if k in self.fields:
                if k == "created":
                    k = "timestamp"
                result[k] = v
            # Custom/extra
            elif k not in JSONFormatter.RESERVED_ATTRS:
                result[k] = v

        return json.dumps(result)

#
# Helpers and utilities
#


def pretty_recursive(value, htchar='\t', lfchar='\n', indent=0):
    '''
    Recursive pretty printing of dict, list and tuples - full creadit to:

    http://stackoverflow.com/questions/3229419/pretty-printing-nested-dictionaries-in-python

    '''
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
    '''
    Format objects, tuples, lists and dicts for pretty printing
    '''
    if sth is None:
        return sth

    prefix = ''
    if sth.__class__.__name__:
        prefix = '(%s) ' % format(sth.__class__.__name__)

    return prefix + pretty_recursive(sth)


def mkdir_p(path):
    '''
    Does the same as 'mkdir -p' in linux
    '''
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
    '''
    Full credit to: https://stackoverflow.com/a/20666342/3727050

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge_dicts(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    '''
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination
