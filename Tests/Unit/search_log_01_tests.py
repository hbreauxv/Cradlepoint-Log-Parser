"""
Basic test cases for search_log_01.py
"""

import unittest
import filecmp
from search_log_01 import search_log

class TestSearch(unittest.TestCase):

    def test_short_search(self):
        # Compare the output from searching a short log file
        search_log('short_test.txt','compare_short_test.txt')
        self.assertTrue(filecmp.cmp('correct_short_test.txt','compare_short_test.txt'),
                                    'Short search failed, output of search log didnt match correct_short_test.txt')


if __name__ == '__main__':
    unittest.main()