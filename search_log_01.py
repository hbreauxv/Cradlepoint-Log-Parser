"""
This script takes a CP log and parses for problem lines. It outputs a file with the problem lines and their common meaning.

It operates by turning a xlsx of problem lines + their meanings into a regex of problem lines.  It uses that regex to
search the log file, and writes the problem line, the line number, and the common meaning of the problem line to an
output file.

Made by Harvey Breaux for use with Cradlepoint Logs
"""

import pandas as pd
import re
import os
import sys


def convert_xlsx():
    """
    Converts an XLSX file to a python dictionary with keys and values that equate to messages and their meanings.
    For each "message" line a regex group trailer and header get applied.  This is considered part of conversion. :)
    This function assumes that any unique identifiers in the log messages have been replaced with ".*"
    """

    # assemble path to xlsx
    dirname = os.path.dirname(__file__)
    xlsx = os.path.join(dirname, 'log_messages.xlsx')

    # Load a DataFrame from the connectivity+modem sheet and only look at the message + meaning columns
    cols = [2, 3]
    df1 = pd.read_excel(xlsx, sheet_name='Connectivity+Modem', usecols=cols, encoding='UTF-8')

    # make our search dictionary
    search_dictionary = {}

    # loop through rows and append them to the search_dictionary
    for index, row in df1.iterrows():
        # replace any characters that mess up regex with escaped versions
        escaped_row = str(row['Message'])
        escaped_row = escaped_row.replace('|', '\|')
        escaped_row = escaped_row.replace('(', '\(')
        escaped_row = escaped_row.replace(')', '\)')

        # write rows to our search dictionary and appened a greedy match to end of line
        search_dictionary['(' + escaped_row.rstrip() + '.*$)'] = row['Meaning']

    return search_dictionary

def search_log(input_file, output_file):
    """
    search_log a log file for search terms and then write matches + their meanings to an output file
    input_file: input log file
    output_file: name for your output file
    """

    # open input and output files
    input_file = open(input_file, "r")
    output_file = open(output_file, "w", encoding='UTF-8')


    # create a dictionary of messages and meanings from our xlsx
    dictionary = convert_xlsx()

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


if __name__ == "__main__":
    try:
        search_log(sys.argv[1], sys.argv[2])
        print('Searched logs for errors successfully')

    except Exception as e:
        print('Exception: %s' % e)
        print('\nUsage: search_log_01.py <input_file> <output_file>')