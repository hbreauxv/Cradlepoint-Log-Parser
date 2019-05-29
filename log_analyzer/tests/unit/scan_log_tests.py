"""
Basic test cases for search_log_01.py
"""

import unittest
import filecmp
import os
import sys

# import ScanLog class.  Inserting into our sys.path is very poor practice but for a basic test script it works
# ¯\_(ツ)_/¯
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from scan_log import ScanLog # this doesn't work atm :) :) :)

class TestSearch(unittest.TestCase):

    def test_short_search(self):
        # Compare the output from searching a short log file
        ScanLog('short_test.txt','compare_short_test.txt', '').search_log()
        self.assertTrue(filecmp.cmp('correct_short_test.txt','compare_short_test.txt'),
                                    'Short search failed, output of search log didnt match correct_short_test.txt')


if __name__ == '__main__':
    unittest.main()