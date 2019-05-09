"""
textbox gui that uses grids for a more complicated layout.
"""

import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.scrolledtext as ScrolledText
from search_log_01 import search_log

root = Tk()
root.geometry('1000x900')
root.title("Cradlepoint Log Analyzer")
root.iconbitmap('./Resources/Images/cradlepoint_icon.ico')


# create textpads & labels
log_text = Label(root, text="Cradlepoint Log")
log_textpad = ScrolledText.ScrolledText(root, font='Segoe 11')

scan_text = Label(root, text="Scan Results")
scan_textpad = ScrolledText.ScrolledText(root, font='Segoe 11')

# create a menu & define functions for each menu item
def open_command():
    file = filedialog.askopenfile(parent=root, mode='rb', title='Select a file', filetypes=(("Log Files",
                                                                                            ("*.txt", "*.log"),),
                                                                                            ("All Files", "*.*")))

    if file is not None:
        contents = file.read()
        # insert unscanned log into the log_textpad
        log_textpad.insert('1.0', contents)

        # insert scanned log into the scan_textpad
        search_log(file.name, 'scan_output.txt')
        with open('scan_output.txt', 'r') as scan_file:
            scan_contents = scan_file.read()
            scan_textpad.insert('1.0', scan_contents)

        file.close()

def save_command():
    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt", initialdir=os.getcwd())

    if file is not None:
        # slice off last character from end, because an extra return is added
        data = scan_textpad.get('1.0', END+'-1c')
        file.write(data)
        file.close()

def exit_command():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

def about_command():
    messagebox.showinfo("About", "Cradlepoint Log Analyzer\n\nThis program analyzes Cradlepoint logs "
                                         "to look for common messages and display their meanings."
                                         "\n\nMade by Harvey Breaux for Cradlepoint")

def dummy():
    print('dummy command, will be removed')

# instantiate root menu class
menu = Menu(root)
root.config(menu=menu)


# file menu
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open...", command=open_command)
filemenu.add_command(label="Save as...", command=save_command)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_command)

# help menu
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about_command)


# configure grid
Grid.columnconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 1, weight=1)
Grid.rowconfigure(root, 1, weight=1)

# place text labels
log_text.grid(column=0, row=0, sticky=W)
scan_text.grid(column=1, row=0, sticky=W)

# place scrollboxes
log_textpad.grid(column=0, row=1, sticky=N+S+E+W)
scan_textpad.grid(column=1, row=1, sticky=N+S+W+E)

root.mainloop()