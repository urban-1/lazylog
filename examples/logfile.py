#!/usr/bin/env python3
import os
import sys
import tempfile
import logging

# Set the paths
LOGDIR = tempfile.gettempdir()
LOGFILE = "simple-log-examples.log"
LOGPATH = "%s/%s" % (LOGDIR, LOGFILE)
ROOTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOTDIR)

from simplelog import Logger

#
# 1. Default file log
#
termSpecs = {"level": logging.DEBUG}
fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG}]
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

logging.debug("^---same as console, this is an example log line")
logging.info("This logger handles\nNew\nLines")
logging.warning({"but": "Flattens structs by default"})
logging.error("Errors DONT stick out - color is not used")


print("\nFile Contents:\n")
with open(LOGPATH) as f:
    print(f.read())

os.unlink(LOGPATH)

#
# 2. Customizing
#
print("\n2. Reconfiguring...\n")
fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "splitLines":False}]
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

logging.info("Like console\nYou can avoid\nsplitting lines")

print("\n\nFile Contents:\n")
with open(LOGPATH) as f:
    print(f.read())

os.unlink(LOGPATH)


print("\n3. Reconfiguring...\n")
fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "pretty":True}]
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

logging.info({"or": "enable prettifying!"})

print("\n\nFile Contents:\n")
with open(LOGPATH) as f:
    print(f.read())

os.unlink(LOGPATH)

#
# 4. Default formatter
#
print("\n4. Reconfiguring...\n")
fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "format":"default"}]
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

logging.info("You\n can set the \n format to\n default")
logging.warning("But I don't like it...")

print("\n\nFile Contents:\n")
with open(LOGPATH) as f:
    print(f.read())

os.unlink(LOGPATH)


#
# 5. JSON formatter
#
print("\n5. Reconfiguring...\n")
fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "format":"json"}]
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

logging.info("Simple str message")
logging.warning("Message with metadata", extra={"user": "nwj12"})
logging.debug({"what": "dict-based logging"}, extra={"user": "asd32"})
logging.info(["anything", "json", "serializable", "see OBJECT"], extra={"foo":"bar"})

print("\n\nFile Contents:\n")
with open(LOGPATH) as f:
    print(f.read())

os.unlink(LOGPATH)
