#!/usr/bin/env python3
import os
import sys
import tempfile
import logging

# Set the paths
LOGDIR = tempfile.gettempdir()
ROOTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOTDIR)

from simplelog import Logger

# Console only logger
termSpecs = {"level": logging.DEBUG }
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=None)

logging.debug("This is an example log line")
logging.info("This logger handles\nNew\nLines")
logging.warning({"also": "handles basic structures", "like": list("lists"), "and": ("colors", "!")})
logging.error("Errors stick out")
logging.critical("but critical sticks out more...")
