import os
import sys
import json
import logging
import unittest
import tempfile
import traceback
import datetime
from lazylog import Logger

LOGDIR = tempfile.gettempdir()
LOGFILE = "tmp-simple.log"
LOGPATH = "%s/%s" % (LOGDIR, LOGFILE)


def rmlog():
    try:
        os.unlink(LOGPATH)
    except BaseException:
        pass


class Testlazylog(unittest.TestCase):
    """
    Test lazylog basic functionality
    """

    @classmethod
    def setUp(cls):
        termSpecs = {"color": True, "splitLines": True, "level": logging.DEBUG}
        Logger.init(LOGDIR, termSpecs=termSpecs)

    @classmethod
    def tearDown(cls):
        rmlog()

    def test_001_testmocking(self):
        """
        Get a new logger and ...
        """
        lg = logging.getLogger("lazylog")

        # Put in StringIO mode
        strio = logging.getLoggerClass().mockHandler(0)
        logging.debug("Hello\nWorld")
        # Now, put it back!
        logging.getLoggerClass().restoreHandler(0)

        # Make sure 2 lines printed...
        self.assertEqual(2, len(strio.getvalue().splitlines()))

        if sys.version_info[0] >= 3:
            # Finally, check we are back in stderr
            with self.assertLogs('lazylog', level='INFO') as cm:
                lg.info("Hello\nWorld")
            self.assertEqual(cm.output, ['INFO:lazylog:Hello\nWorld'])

    def test_002_pretty(self):
        """
        Get a new logger and ...
        """
        strio = logging.getLoggerClass().mockHandler(0)
        logging.debug({"hello": 1, "world": 2})
        logging.getLoggerClass().restoreHandler(0)

        # We expect 4 lines in pretty mode
        self.assertEqual(4, len(strio.getvalue().splitlines()))
        strio.close()

        strio = logging.getLoggerClass().mockHandler(0)
        logging.debug(["hello", "world"])
        logging.getLoggerClass().restoreHandler(0)

        # We expect 4 lines in pretty mode
        self.assertEqual(4, len(strio.getvalue().splitlines()))
        strio.close()

        strio = logging.getLoggerClass().mockHandler(0)
        logging.debug(("hello", "world"))
        logging.getLoggerClass().restoreHandler(0)

        # We expect 4 lines in pretty mode
        self.assertEqual(4, len(strio.getvalue().splitlines()))
        strio.close()

    def test_003_pretty_false_split_true(self):
        """
        Get a new logger and ...
        """
        # Reset Logger
        termSpecs = {"color": True, "splitLines": True, "level": logging.DEBUG, "pretty": False}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=None)

        strio = logging.getLoggerClass().mockHandler(0)
        logging.debug({"hello": 1, "world": 2})
        logging.getLoggerClass().restoreHandler(0)

        # We expect 1 line in default mode
        self.assertEqual(1, len(strio.getvalue().splitlines()))

    def test_004_pretty_false_split_true(self):
        """
        Get a new logger and ...
        """
        # Reset Logger
        termSpecs = {"color": True, "splitLines": True, "level": logging.DEBUG, "pretty": False}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=None)

        strio = logging.getLoggerClass().mockHandler(0)
        logging.debug("Hello\nWorld")
        logging.getLoggerClass().restoreHandler(0)

        self.assertEqual(2, len(strio.getvalue().splitlines()))

    def test_005_pretty_false_split_false(self):
        """
        Get a new logger and ...
        """
        # Reset Logger
        termSpecs = {"color": True, "splitLines": False, "level": logging.DEBUG, "pretty": False}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=None)

        strio = logging.getLoggerClass().mockHandler(0)
        logging.debug("Hello\nWorld")
        logging.getLoggerClass().restoreHandler(0)

        self.assertEqual(1, len(strio.getvalue().splitlines()))

    def test_006_pretty_true_split_false(self):
        """
        Get a new logger and ...
        """
        # Reset Logger
        termSpecs = {"color": True, "splitLines": False, "level": logging.DEBUG, "pretty": True}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=None)

        strio = logging.getLoggerClass().mockHandler(0)
        logging.debug("Hello\nWorld")
        logging.getLoggerClass().restoreHandler(0)

        self.assertEqual(2, len(strio.getvalue().splitlines()))

    def test_007_logFun(self):
        """
        Get a new logger and ...
        """
        # Put in StringIO mode
        strio = logging.getLoggerClass().mockHandler(0)
        logging.getLoggerClass().logFun()
        # Now, put it back!
        logging.getLoggerClass().restoreHandler(0)

        # Make sure 2 lines printed...
        self.assertEqual(5, len(strio.getvalue().splitlines()))

    #
    # File tests below here
    #

    def test_007_file_default_implied(self):
        """
        Remove log and test console-like formatting
        """
        rmlog()
        fileSpecs = [{"filename": LOGFILE, "level": logging.DEBUG}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

        logging.debug({"hello": 1, "world": 2})

        with open(LOGPATH) as f:
            cont = f.read()

        self.assertEqual(1, len(cont.splitlines()))

    def test_008_file_console(self):
        """
        Remove log and test console-like formatting
        """
        rmlog()
        fileSpecs = [{"filename": LOGFILE, "level": logging.DEBUG, "format": "console"}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

        logging.debug({"hello": 1, "world": 2})

        with open(LOGPATH) as f:
            cont = f.read()

        self.assertEqual(1, len(cont.splitlines()))

    def test_009_file_console_pretty(self):
        """
        Remove log and test console-like formatting
        """
        rmlog()
        fileSpecs = [{"filename": LOGFILE, "level": logging.DEBUG, "format": "console", "pretty": True}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

        logging.debug({"hello": 1, "world": 2})

        with open(LOGPATH) as f:
            cont = f.read()

        self.assertEqual(4, len(cont.splitlines()))

    def test_010_file_default(self):
        """
        Remove log and test default formatting
        """
        rmlog()
        fileSpecs = [{"filename": LOGFILE, "level": logging.DEBUG, "format": "default"}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

        logging.debug({"hello": 1, "world": 2})

        with open(LOGPATH) as f:
            cont = f.read()

        self.assertEqual(1, len(cont.splitlines()), msg="Got: %s" % cont)

    def test_011_file_console_split(self):
        """
        Remove log and test default formatting
        """
        rmlog()
        fileSpecs = [{"filename": LOGFILE, "level": logging.DEBUG, "format": "console", "splitLines": False}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

        logging.debug("Hello\nWorld")

        with open(LOGPATH) as f:
            cont = f.read()

        self.assertEqual(1, len(cont.splitlines()), msg="Got: %s" % cont)

    def test_012_file_json(self):
        """
        Remove log and test default formatting
        """
        rmlog()
        fileSpecs = [{"filename": LOGFILE, "level": logging.DEBUG, "format": "json"}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

        logging.debug("Hello\nWorld", extra={"when": "today"})

        with open(LOGPATH) as f:
            cont = json.loads(f.read())

        self.assertEqual(True, "message" in cont, msg="Got: %s" % str(cont))
        self.assertEqual("Hello\nWorld", cont["message"], msg="Got: %s" % str(cont))

        self.assertEqual(True, "when" in cont, msg="Got: %s" % str(cont))
        self.assertEqual("today", cont["when"], msg="Got: %s" % str(cont))

        self.assertEqual(True, "timestamp" in cont, msg="Got: %s" % str(cont))

    def test_013_file_json_dict(self):
        """
        Remove log and test default formatting
        """
        rmlog()
        fileSpecs = [{"filename": LOGFILE, "level": logging.DEBUG, "format": "json"}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

        logging.debug({"hello": "world"}, extra={"when": "today"})

        with open(LOGPATH) as f:
            cont = json.loads(f.read())

        self.assertEqual(True, "hello" in cont, msg="Got: %s" % str(cont))
        self.assertEqual("world", cont["hello"], msg="Got: %s" % str(cont))

    def test_014_file_json_object(self):
        """
        Remove log and test default formatting
        """
        rmlog()
        fileSpecs = [{"filename": LOGFILE, "level": logging.DEBUG, "format": "json"}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

        logging.debug(["hello", "world"], extra={"when": "today"})

        with open(LOGPATH) as f:
            cont = json.loads(f.read())

        self.assertEqual(True, "object" in cont, msg="Got: %s" % str(cont))
        self.assertEqual(["hello", "world"], cont["object"], msg="Got: %s" % str(cont))

    def test_015_file_misconfig(self):
        """
        Test misconfiguration
        """
        rmlog()
        with self.assertRaises(RuntimeError):
            Logger.addFileLogger({"filename_": LOGFILE, "level": logging.DEBUG, "format": "json"})

    def test_016_file_defaults(self):
        """
        Test default logging level for file
        """
        rmlog()
        Logger.addFileLogger({"filename": LOGFILE})
        self.assertEqual(logging.INFO, logging.getLogger().handlers[1].level)

    def test_017_console_fmt(self):
        """
        Test formats
        """
        termSpecs = {"color": False}
        Logger.init(
            LOGDIR,
            fmt='%(asctime)s %(levelname)-8s %(lineno)s: %(message)s',
            datefmt="%Y",
            termSpecs=termSpecs)

        strio = logging.getLoggerClass().mockHandler(0)
        logging.debug("hmmm")
        # Now, put it back!
        logging.getLoggerClass().restoreHandler(0)

        now = datetime.datetime.now()
        expect = "%s DEBUG" % now.year
        self.assertTrue(
            strio.getvalue().startswith(expect),
            msg="Got: %s, expected: %s" % (strio.getvalue(), expect))

    def test_018_set_levels(self):
        """
        Test default logging level for file
        """
        rmlog()
        fileSpecs = [{"filename": LOGFILE, "level": logging.DEBUG, "format": "json"}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING}
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

        Logger.setConsoleLevel(logging.DEBUG)
        Logger.setFileLevel(1, logging.WARNING)

        self.assertEqual(logging.DEBUG, logging.getLogger().handlers[0].level)
        self.assertEqual(logging.WARNING, logging.getLogger().handlers[1].level)
