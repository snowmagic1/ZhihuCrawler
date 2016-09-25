# tests/runner.py

import unittest
import sys
import os

sys.path.insert(0, os.getcwd())

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

all_suite = loader.discover(os.path.dirname(__file__), "tests_*.py")

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(all_suite)