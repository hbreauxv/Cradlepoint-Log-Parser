"""
Creates and compiles regexs and message + meaning dictionaries that can be used to search the log for problem
messages.
"""

import pandas as pd
import re
import os
import sys


class ScanLog(object):
    """
    The scan log object works with Cradlepoint log files and a xlsx or json database of log messages and their meanings.
    It uses regex to scan through logs to find problem messages from the database, and then it writes the messages and
    their meanings to an output file.
    """

    # initialized allowed search categories
    ALLOWED_CATEGORIES = ['Connectivity+Modem', 'IPSec', 'Routing Protocols', 'NCP', 'NCM']

    def __init__(self, input_file, output_file, log_database='log_messages.xlsx'):
        self.input_file = input_file
        self.output_file = output_file
        self.log_database = log_database
        self.search_categories = ['Connectivity+Modem','IPSec','Routing Protocols','NCP','NCM']

    def convert_xlsx(self):
        """
        Converts an XLSX file to a python dictionary with keys and values that equate to messages and their meanings.
        For each "message" line a regex group trailer and header get applied.  This is considered part of conversion. :)
        This function assumes that any unique identifiers in the log messages have been replaced with ".*"
        """

        # assemble path to xlsx
        dirname = os.path.dirname(__file__)
        xlsx = os.path.join(dirname, self.log_database)

        # make our search dictionary
        search_dictionary = {}

        # Loop through our search categories to open the correct sheets and load any messages in them into our df
        for category in self.search_categories:

            # Load a DataFrame from the specified categories sheet and only look at the message + meaning columns
            try:
                cols = [2, 3]
                df = pd.read_excel(xlsx, sheet_name=category, usecols=cols, encoding='UTF-8')

                # loop through rows and append them to the search_dictionary
                for index, row in df.iterrows():
                    # replace any characters that mess up regex with escaped versions
                    escaped_row = str(row['Message'])
                    escaped_row = escaped_row.replace('|', '\|')
                    escaped_row = escaped_row.replace('(', '\(')
                    escaped_row = escaped_row.replace(')', '\)')

                    # write rows to our search dictionary and appened a greedy match to end of line
                    search_dictionary['(' + escaped_row.rstrip() + '.*$)'] = row['Meaning']

            except Exception as e:
                print("Exception occured while loading %s: %s" % (category, e))
                continue

        return search_dictionary

    def convert_json(self):
        """converts json log message files into a dictionary"""

        return '{message: "this method hasnt been created yet :)"}'

    def search_log(self):
        """
        search_log a log file for search terms and then write matches + their meanings to an output file
        dictionary: dictionary from convert_xlsx() or convert_json()
        """

        dictionary = self._convert_db()

        # open input and output files
        input_file = open(self.input_file, "r")
        output_file = open(self.output_file, "w", encoding='UTF-8')

        # go through each line in the input file and search it for matches with our regex
        i = 0
        for line in input_file:
            # increment line counter
            i += 1

            # search line for a match
            for key in dictionary:
                # compile regex
                interesting_text = re.compile(key)

                # search line for a match
                match = re.search(interesting_text, line)

                # if there's a match, write the line, match, and the meaning to our output file
                if match:
                    output_file.write("Match on line %s, Keyword: %s \n" % (i, match.group()))
                    output_file.write('\n')
                    output_file.write("Common meaning: %s" % dictionary[key] + '\n')
                    output_file.write('\n\n\n')

        # close the input and output files
        input_file.close()
        output_file.close()

    def _convert_db(self):
        """Check log db type and return the correctly dictionary"""
        if self.log_database.endswith('.xlsx'):
            return self.convert_xlsx()

        elif self.log_database.endswith('.json'):
            return self.convert_json()

    def update_categories(self, category):
        """Add log categories to be searched for"""
        if category in self.ALLOWED_CATEGORIES:
            if category not in self.search_categories:
                self.search_categories.insert(0, category)
        else:
            raise Exception('The category %s does not exist. Allowed categories: %s' % (category, self.ALLOWED_CATEGORIES))

    def remove_category(self, category):
        """Remove a log category to be searched for"""
        if category in self.ALLOWED_CATEGORIES:
            self.search_categories.remove(category)
        else:
            raise Exception('The category %s does not exist. Allowed categories: %s' % (category, self.ALLOWED_CATEGORIES))




if __name__ == "__main__":
    try:
        ScanLog(sys.argv[1], sys.argv[2], 'log_messages.xlsx').search_log()
    except Exception as e:
        print("Exception occurred! {}".format(e))