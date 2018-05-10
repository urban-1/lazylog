#!/usr/bin/env python3
import os
import sys
import tempfile
import logging

# Set the paths
LOGDIR = tempfile.gettempdir()
LOGFILE = "simple-log-examples.log"
LOGFILE2 = "simple-log-examples-2.log"
LOGPATH = "%s/%s" % (LOGDIR, LOGFILE)
LOGPATH2 = "%s/%s" % (LOGDIR, LOGFILE2)
ROOTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOTDIR)

from lazylog import Logger

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
# 2. Customizing: Not splitting new lines
#
print("\n2. Reconfiguring...\n")
fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "splitLines":False}]
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

logging.info("Like console\nYou can avoid\nsplitting lines")

print("\n\nFile Contents:\n")
with open(LOGPATH) as f:
    print(f.read())

os.unlink(LOGPATH)

#
# 3. Customizing: Not prettyfying
#
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

#
# 6. Lets add another log-file
#
print("\n6. Reconfiguring...\n")
fileSpecs = [{"filename": LOGFILE, "level":logging.DEBUG, "format":"json"}]
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

fileSpecs2 = {"filename": LOGFILE2, "level":logging.INFO}
Logger.addFileLogger(fileSpecs2)

logging.info("2 Files!")

print("\n\nFile Contents 1:\n")
with open(LOGPATH) as f:
    print(f.read())

os.unlink(LOGPATH)

print("\n\nFile Contents 2:\n")
with open(LOGPATH2) as f:
    print(f.read())

os.unlink(LOGPATH2)

#
# 7. Both files from init!
#
print("\n7. Reconfiguring...\n")
fileSpecs = [
    {"filename": LOGFILE, "level":logging.DEBUG, "format":"json"},
    {"filename": LOGFILE2, "level":logging.INFO}
]
Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=fileSpecs)

logging.info("2 Files!")
logging.debug("JSON only...")

print("\n\nFile Contents 1:\n")
with open(LOGPATH) as f:
    print(f.read())

os.unlink(LOGPATH)

print("\n\nFile Contents 2:\n")
with open(LOGPATH2) as f:
    print(f.read())

os.unlink(LOGPATH2)
