import os
import unittest
import traceback
import logging
from simplelog import Logger
import tempfile

LOGDIR = tempfile.gettempdir()
LOGFILE = "tmp-simple.log"
LOGPATH = "%s/%s" % (LOGDIR, LOGFILE)

def rmlog():
    try:
        os.unlink(LOGPATH)
    except:
        pass

class TestSimpleLog(unittest.TestCase):
    """
    Test simplelog basic functionality
    """

    @classmethod
    def setUp(cls):
        termSpecs = {"color": True, "splitLines": True, "level": logging.DEBUG }
        Logger.init(LOGDIR, termSpecs=termSpecs)


    def test_001_testmocking(self):
        """
        Get a new logger and ...
        """
        lg = logging.getLogger("simplelog")

        # Put in StringIO mode
        strio = logging.getLoggerClass().mockHandler(0)
        logging.debug("Hello\nWorld")
        # Now, put it back!
        logging.getLoggerClass().restoreHandler(0)

        # Make sure 2 lines printed...
        self.assertEqual(2, len(strio.getvalue().splitlines()))

        # Finally, check we are back in stderr
        with self.assertLogs('simplelog', level='INFO') as cm:
            lg.info("Hello\nWorld")
        self.assertEqual(cm.output, ['INFO:simplelog:Hello\nWorld'])

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
        termSpecs = {"color": True, "splitLines": True, "level": logging.DEBUG, "pretty": False }
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
        termSpecs = {"color": True, "splitLines": True, "level": logging.DEBUG, "pretty": False }
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
        termSpecs = {"color": True, "splitLines": False, "level": logging.DEBUG, "pretty": False }
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
        termSpecs = {"color": True, "splitLines": False, "level": logging.DEBUG, "pretty": True }
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
        fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING }
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
        fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "format": "console"}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING }
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
        fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "format": "console", "pretty": True}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING }
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
        fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "format": "default"}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING }
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
        fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "format": "console", "splitLines": False}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.WARNING }
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

        logging.debug("Hello\nWorld")

        with open(LOGPATH) as f:
            cont = f.read()

        self.assertEqual(1, len(cont.splitlines()), msg="Got: %s" % cont)
