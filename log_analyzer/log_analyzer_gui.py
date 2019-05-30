"""
A gui for scan_log.py.  It displays the log on the left, and the scan results on the right.

This is powered by tkinter and uses tkinters grid layout to place elements on the grid.
"""

import os
from tkinter import *
from tkinter import Grid
from tkinter import filedialog
from tkinter import messagebox
import tkinter.scrolledtext as ScrolledText
from scan_log import ScanLog


class LogGui:
    def __init__(self, master):
        self.master = master
        master.title("Cradlepoint Log Analyzer")
        master.geometry('1000x900')
        master.iconbitmap('./resources/cradlepoint_icon.ico')

        # configure grid
        Grid.columnconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 1, weight=1)
        Grid.rowconfigure(master, 1, weight=1)

        # create log scrollboxes & labels
        self.log_text = Label(master, text="Cradlepoint Log")
        self.log_text.grid(column=0, row=0, sticky=W)
        self.log_scrolledtext = ScrolledText.ScrolledText(master, font='Segoe 11', wrap='word')
        self.log_scrolledtext.grid(column=0, row=1, sticky=N + S + E + W)

        # create scan results scrollboxes & labels
        self.scan_text = Label(master, text="Scan Results")
        self.scan_text.grid(column=1, row=0, sticky=W)
        self.scan_scrolledtext = ScrolledText.ScrolledText(master, font='Segoe 11', wrap='word')
        self.scan_scrolledtext.grid(column=1, row=1, sticky=N + S + W + E)

        self.menu = Menu(master)
        master.config(menu=self.menu)

        # file menu
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open...", command=self.open_command)
        self.filemenu.add_command(label="Save as...", command=self.save_command)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit_command)

        # help menu
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.about_command)

    def open_command(self):
        file = filedialog.askopenfile(parent=self.master, mode='rb', title='Select a file', filetypes=(("Log Files",
                                                                                                ("*.txt", "*.log"),),
                                                                                                ("All Files", "*.*")))

        if file is not None:
            try:
                contents = file.read()
                # insert unscanned log into the log_textpad
                self.log_scrolledtext.delete('1.0', END)
                self.log_scrolledtext.insert('1.0', contents)

                # insert scanned log into the scan_textpad
                ScanLog(file.name, 'scan_output.txt').search_log()
                with open('scan_output.txt', 'r', encoding='UTF-8') as scan_file:
                    scan_contents = scan_file.read()
                    self.scan_scrolledtext.delete('1.0', END)
                    self.scan_scrolledtext.insert('1.0', scan_contents)

                file.close()

            except Exception as e:
                messagebox.showinfo('Error occurred: {}'.format(e))
                print('Exception occurred: {}'.format(e))
                file.close()

    def save_command(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".txt", initialdir=os.getcwd())

        if file is not None:
            # slice off last character from end, because an extra return is added
            data = self.scan_scrolledtext.get('1.0', END+'-1c')
            file.write(data)
            file.close()

    def exit_command(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.master.destroy()

    def about_command(self):
        messagebox.showinfo("About", "Cradlepoint Log Analyzer\n\nThis program analyzes Cradlepoint logs "
                                             "to look for common messages and display their meanings."
                                             "\n\nMade by Harvey Breaux for Cradlepoint")


root = Tk()
gui = LogGui(root)
root.mainloop()