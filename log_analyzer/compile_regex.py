"""
Creates and compiles regexs and message + meaning dictionaries that can be used by analyze_log
"""

import pandas as pd
import re
import os


class CreateRegex(object):
    def __init__(self, log_messages):
        self.log_messages = log_messages # input json file containing search info + meanings

    def convert_xlsx(self):
        """Converts xlsx log message files into a list of regex search phrases."""

        # assemble path to xlsx
        dirname = os.path.dirname(__file__)
        xlsx = os.path.join(dirname, self.log_messages)

        # Load a DataFrame from the connectivity+modem sheet and only look at the message + meaning columns
        cols = [2, 3]
        df1 = pd.read_excel(xlsx, sheet_name='Connectivity+Modem', usecols=cols, encoding='UTF-8')

        # make our search dictionary
        search_list = []

        # loop through rows and append them to the search_dictionary
        for index, row in df1.iterrows():
            # replace any characters that mess up regex with escaped versions
            escaped_row = str(row['Message'])
            escaped_row = escaped_row.replace('|', '\|')
            escaped_row = escaped_row.replace('(', '\(')
            escaped_row = escaped_row.replace(')', '\)')

            # write rows to our search dictionary and appened a greedy match to end of line
            search_list.append('(' + escaped_row.rstrip() + '.*$)')

        return search_list

    def convert_json(self):
        """converts json log message files into a list of regex search phrases"""

        return '{json: "empty json"}'

    def compile_regex(self):
        """Compiles a log_dictionary into regex and saves it for use by analyze_log.py"""
        if self.log_messages.endswith('.xlsx'):
            # Convert xlsx into a list
            log_list = self.convert_xlsx()

            # Convert list into regex
            regex = re.compile("".join(log_list))

            # Compile regex and save it

            print(str(regex) + '\n' + str(log_list))

        elif self.log_messages.endswith('.json'):
            # Convert json into a list
            log_dictionary = self.convert_xlsx()

            # Convert list into regex

            # Compile regex and save it

            print(log_dictionary)

        else:
            print('Unrecognized filetype.  log_messages must be a .xlsx or .json')


if __name__ == "__main__":
    try:
        CreateRegex('log_messages.xlsx').compile_regex()
    except Exception as e:
        print("Exception occurred! {}".format(e))