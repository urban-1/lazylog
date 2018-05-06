import os
import unittest
import traceback
import logging
from simplelog import Logger

LOGDIR = "/tmp"
log_file = "simplelogtests.log"

class TestSimpleLog(unittest.TestCase):
    """
    Test simplelog basic functionality
    """

    @classmethod
    def setUp(cls):
        fileSpecs = [{"filename": log_file, "level":logging.DEBUG}]
        termSpecs = {"color": True, "splitLines": True, "level": logging.DEBUG }

        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)


    def test_001_testmocking(self):
        """
        Get a new logger and ...
        """
        lg = logging.getLogger("simplelog")


        # Put in StringIO mode
        strio = lg.mockHandler(0)
        lg.debug("Hello\nWorld")
        # Make sure 2 lines printed...
        self.assertEqual(2, len(strio.getvalue().splitlines()))
        strio.close()

        # Now, put it back!
        lg.restoreHandler(0)

        # Finally, check we are back in stderr
        with self.assertLogs('simplelog', level='INFO') as cm:
            lg.info("Hello\nWorld")
        self.assertEqual(cm.output, ['INFO:simplelog:Hello\nWorld'])

    def test_002_pretty(self):
        """
        Get a new logger and ...
        """
        lg = logging.getLogger("simplelog")
        strio = lg.mockHandler(0)
        lg.debug({"hello": 1, "world": 2})
        lg.restoreHandler(0)

        # We expect 4 lines in pretty mode
        self.assertEqual(4, len(strio.getvalue().splitlines()))


    def test_003_pretty_false(self):
        """
        Get a new logger and ...
        """
        # Reset Logger
        termSpecs = {"color": True, "splitLines": True, "level": logging.DEBUG, "pretty": False }
        Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=None)

        lg = logging.getLogger("simplelog")
        strio = lg.mockHandler(0)
        lg.debug({"hello": 1, "world": 2})
        lg.restoreHandler(0)

        # We expect 1 line in default mode
        self.assertEqual(1, len(strio.getvalue().splitlines()))
