"""
Mockup of a gui for my search_log project
"""

import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from search_log_01 import search_log


window = Tk()
window.title("Cradlepoint Log Analyzer")
window.geometry('600x200')
window.grid_columnconfigure(0, weight=1)
window.iconbitmap('./Resources/Images/cradlepoint_icon.ico')


def open_log():
    """
    Open log lets the user choose the log file they want to analyze
    It stores the file in the "file" global variable.
    This and search_log() should probably be combined into one function. :)
    """

    # Open file select dialog and ask user to select their file
    file = filedialog.askopenfile(initialdir=os.getcwd(), filetypes=(("Log Files", ("*.txt", "*.log"),),
                                                                     ("All Files", "*.*")))
    # Insert the name of the file we selected into the text entry box
    log_text_box.insert(0, file.name)

    file.close()


# Analyze Log function
def analyze_function():
    """
    analyze_function() opens a save dialog to let the user choose where they want to save their file
    It's activated when the user clicks the "Analyze Log" button
    :return:
    """

    # Open save as dialog and ask user to save file
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", initialdir=os.getcwd())
    # Pass name of the output file to the search_log() function
    search_log(log_text_box.get(),output_file,'log_messages.xlsx')

    # update analyze_lbl to show results/name of output file
    analyze_result.configure(text='Saved result as: ' + output_file)


# Description of program
description_label = Label(window,
                          text="Cradlepoint Log Analyzer takes a log file and analyzes it for "
                               "common problem messages. "
                               "\nIt outputs a file with the problem messages and their meanings."
                               "\n\n"
                               "Select a log file and click Analyze Log to search it for issues."
                          )
description_label.grid(column=0, row=0, columnspan=2, rowspan=4,
                       padx=10, pady=10)


# Log file prompt text
log_file_prompt = Label(window, text="Log File:")
log_file_prompt.grid(column=0, row=4, sticky=W,
                     padx=5, pady=2)

# Log file text box
log_text_box = Entry(window)
log_text_box.grid(column=0, row=5, columnspan=2, sticky='nsew',
                  padx=5, pady=2)


# Log file browse button
log_browse_btn = Button(window, text="Browse...", command=open_log)
log_browse_btn.grid(column=1, row=5, sticky=W,
                    padx=5, pady=2)


# Analyze log file button
analyze_button = Button(window, text="Analyze Log", command=analyze_function)
analyze_button.grid(column=0, row=6, columnspan=2, sticky='nsew',
                    padx=5, pady=2)

# Analyze results label
analyze_result = Label(window, text='')
analyze_result.grid(column=0, row=7, columnspan=2, sticky='nsew',
                    padx=5, pady=2)


# Run window loop
window.mainloop()
