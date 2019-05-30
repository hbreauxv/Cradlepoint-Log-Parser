"""
Performs various log analysis functions. Current vision is that class will handle requests to scan logs, make graphs,
etc...

This is very unfinished and im still not sure what to do with it.  May end up being removed.  Ignore for now and just
use scan_log.py or log_analyzer_gui :<
"""

import sys


class AnalyzeLog(object):

    def __init__(self, log, search_categories):
        self.log = log
        self.search_categories = search_categories

    def search_log(self):
        """Uses compiled regex to search log and export meaning file"""
        pass

    def _update_categories(self):
        """Update search_categories"""


if __name__ == "__main__":
    try:
        AnalyzeLog(sys.argv[1], search_categories='all').search_log()
        print('Searched logs for errors successfully')

    except Exception as e:
        print('Exception: %s' % e)
        print('\nUsage: search_log_01.py <input_file> <output_file>')