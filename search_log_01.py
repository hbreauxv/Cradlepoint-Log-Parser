"""
A log parser that compiles the regex for each individual line it searches
It takes an xlsx and turns it into a python dictionary.
Each key in the dictionary is a regex phrase that can be compiled and used to search a line.
Each value is the meaning of the log message the key searches for

It is probably bad practice to make a dictionary structured like that?  And there may be a more elegant way to
search through this data using panda.  But for now this works in my testing.

Things missing: exception handling. :|
Program can probably be restructured to keep each function more contained to the task its supposed to do.

Made by Harvey Breaux for use with Cradlepoint Logs
"""

import pandas as pd
import re


def convert_xlsx(xlsx):
    """
    Converts an XLSX file to a python dictionary with keys and values that equate to messages and their meanings.
    For each "message" line a regex group trailer and header get applied.  This is considered part of conversion. :)
    This function assumes that any unique identifiers in the log messages have been replaced with ".*"
    """
    # Assign spreadsheet filename to 'file'
    file = xlsx

    # Load a DataFrame from the connectivity+modem sheet and only look at the message + meaning columns
    cols = [2, 3]
    df1 = pd.read_excel(file, sheet_name='Connectivity+Modem', usecols=cols)

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


def search_log(input_file, output_file, xlsx):
    """
    search_log a log file for search terms and then write matches + their meanings to an output file
    input_file: input log file
    output_file: name for your output file
    xlsx: the xlsx with search terms you want to use.
    """
    # open input and output files
    input_file = open(input_file, "r")
    output_file = open(output_file, "w")
    # read through input file and separate each line
    text = input_file.read().splitlines()
    i = 0
    # create a dictionary of messages and meanings from our xlsx
    dictionary = convert_xlsx(xlsx)
    # print(dictionary)
    # go through each line in the input file and search it for matches with our regex
    for line in text:
        # increment line counter
        i += 1

        # print(line)
        # search line for a match
        for key in dictionary:
            interesting_text = re.compile(key)
            # print(interesting_text)
            # search line for a match
            match = re.search(interesting_text, line)
            # print(match)
            # if there's a regex search match, write the line, match, and the meaning to our output file
            if match:
                output_file.write("Match on line %s, Keyword: %s \n" % (i, match.group()))
                output_file.write("Line %s: " % i + line + '\n')
                output_file.write("Common meaning: %s" % dictionary[key] + '\n')
                output_file.write('\n\n\n')
    # close the input and output files
    input_file.close()
    output_file.close()


# usage example:
# search_log("test_search_me.txt", "test_output2.txt", 'log_messages.xlsx')