#!/usr/bin/env python3

"""
"""


import os
import re
import sys
import argparse
import unittest
import tempfile
import logging as lg

# Set the paths
ROOTDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOTDIR)

from simplelog import Logger

LOGDIR = tempfile.gettempdir()
log_file = "simplelogtests.log"
result = False

def main():
    global result
    parser = argparse.ArgumentParser(usage="%(prog)s [options]\n\n\tTest simplelog")
    parser.add_argument('-t', '--tests', nargs="*", required=False, help="Run specific tests (multiple can be specified)")
    parser.add_argument('-d', '--debug', required=False, help="Enable DEBUG Logging", action='store_true')
    parser.add_argument('-v', '--verbosity', type=int, required=False, help="Verbosity level (test suite), default 1", default=1)
    args = parser.parse_args()

    # Setup Logging
    #fileSpecs = [{"filename": log_file, "level":lg.DEBUG}]
    termSpecs = {"color": True, "splitLines": True, "level": lg.DEBUG }
    if not args.debug:
        termSpecs["level"] = lg.WARNING

    Logger.init(LOGDIR, termSpecs=termSpecs, fileSpecs=None)
    lg.getLogger("tests").setLevel(level=lg.DEBUG)


    if not args.tests:
        suite = unittest.TestLoader().discover(ROOTDIR + '/tests')
    else:
        lg.info(' * Running specific tests')

        suite = unittest.TestSuite()

        # Load standard tests
        for t in args.tests:
            # Remove folder name if there
            t = re.sub(r".*tests/", "", t)
            t = re.sub(r"\.py$", "", t)
            test = unittest.TestLoader().loadTestsFromName("tests." + t)
            suite.addTest(test)

    # Run
    lg.info("Single threaded tests")
    result = unittest.TextTestRunner(verbosity=args.verbosity).run(suite)
    result = result.wasSuccessful()

    if result is False:
        lg.info("Failing tests...")
        return 1

    lg.info("Success!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
