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
termSpecs = {"level": logging.DEBUG, "splitLines": False, "pretty": False }
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=None)

logging.debug("You can remove all the fancy stuff:")
logging.info("... keeping\n each message\n in its own line")
logging.warning({"and": "flatten structures", "like": list("lists")})

logging.info("RECONFIGURING....")
termSpecs = {"level": logging.DEBUG, "splitLines": True, "pretty": False }
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=None)
logging.error("However,\nYou can choose to split\nlines")
logging.critical(["but", "not", "prettify\nstructs"])

logging.info("RECONFIGURING....")
termSpecs = {"level": logging.DEBUG, "splitLines": False, "pretty": False, "color": False }
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=None)
logging.info("Boooriiiing")
