"""
A gui for scan_log.py.  It displays the log on the left, and the scan results on the right.

This is powered by tkinter and uses tkinters grid layout to place elements on the grid.
"""

import os
import codecs
import tkinter as tk
from tkinter import *
from tkinter import Grid
from tkinter import filedialog
from tkinter import messagebox
import tkinter.scrolledtext as ScrolledText
from scan_log import ScanLog


class TextLineNumbers(tk.Canvas):
    """Custom tkinter class that lets us make and display line numbers"""
    def __init__(self, textwidget, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = textwidget
        self.redraw()

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

        self.after(30, self.redraw)


class LogGui(tk.Frame):
    """Main screen of the GUI"""

    def __init__(self, master):
        # instantiate scan_log object with no input or output files selected
        tk.Frame.__init__(self)
        self.scanner = ScanLog(None, None, log_database='log_messages.json')

        self.master = master
        # set window settings
        master.title("Cradlepoint Log Analyzer")
        master.geometry('1000x900')
        # Assemble path to icon
        dirname = os.path.dirname(__file__)
        icon = os.path.join(dirname, './resources/cradlepoint_icon.ico')
        master.iconbitmap(icon)
        master.iconbitmap('./resources/cradlepoint_icon.ico')
        master.option_add('*tearOff', False)

        # configure grid
        Grid.columnconfigure(master, 0, weight=0, minsize=17)
        Grid.columnconfigure(master, 1, weight=1)
        Grid.columnconfigure(master, 2, weight=0, minsize=20)
        Grid.columnconfigure(master, 3, weight=1)
        Grid.rowconfigure(master, 1, weight=1)

        # create log scrollboxes & labels
        self.log_text = Label(master, text="Cradlepoint Log")
        self.log_text.grid(column=1, row=0, sticky=W)

        self.log_scrolledtext = ScrolledText.ScrolledText(master, font='Segoe 11', wrap='word')
        self.log_scrolledtext.grid(column=1, row=1, sticky=N + S + E + W)

        self.log_linenumbers = TextLineNumbers(self.log_scrolledtext, width=30)
        self.log_linenumbers.attach(self.log_scrolledtext)
        self.log_linenumbers.grid(column=0, row=1, sticky=N + W + S)

        # create scan results scrollboxes & labels
        self.scan_text = Label(master, text="Scan Results")
        self.scan_text.grid(column=3, row=0, sticky=W)

        self.scan_scrolledtext = ScrolledText.ScrolledText(master, font='Segoe 11', wrap='word')
        self.scan_scrolledtext.grid(column=3, row=1, sticky=N + S + W + E)

        self.scan_linenumbers = TextLineNumbers(self.scan_scrolledtext, width=30)
        self.scan_linenumbers.attach(self.scan_scrolledtext)
        self.scan_linenumbers.grid(column=2, row=1, sticky=N + W + S)

        # create menus for the window
        self.menu = Menu(master)
        master.config(menu=self.menu)

        # file menu
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open...", command=self.select_file_command)
        self.filemenu.add_command(label="Save scan output...", command=self.save_file_command)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Scan Log", command=self.scan_textbox_command)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit_command)

        # categories menu
        self.categories_menu = Menu(self.menu)
        self.menu.add_cascade(label="Categories", menu=self.categories_menu)

        self.connectivity_checkbox = BooleanVar()
        self.connectivity_checkbox.set(True)
        self.categories_menu.add_checkbutton(label="Connectivity+Modem", onvalue=True, offvalue=False,
                                             variable=self.connectivity_checkbox, command=self.update_scan)

        self.ipsec_checkbox = BooleanVar()
        self.ipsec_checkbox.set(True)
        self.categories_menu.add_checkbutton(label="IPSec", onvalue=True, offvalue=False,
                                             variable=self.ipsec_checkbox, command=self.update_scan)

        self.routing_protocols_checkbox = BooleanVar()
        self.routing_protocols_checkbox.set(True)
        self.categories_menu.add_checkbutton(label="Routing Protocols", onvalue=True, offvalue=False,
                                             variable=self.routing_protocols_checkbox, command=self.update_scan)

        self.ncp_checkbox = BooleanVar()
        self.ncp_checkbox.set(True)
        self.categories_menu.add_checkbutton(label="NCP", onvalue=True, offvalue=False,
                                             variable=self.ncp_checkbox, command=self.update_scan)

        self.ncm_checkbox = BooleanVar()
        self.ncm_checkbox.set(True)
        self.categories_menu.add_checkbutton(label="NCM", onvalue=True, offvalue=False,
                                             variable=self.ncm_checkbox, command=self.update_scan)

        # help menu
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.about_command)

        self.log_scrolledtext.bind('<f>', self.find_text)



    def select_file_command(self):
        """Used to open log files and scan them using scan_log.py. Displays results in scan_scrolledtext"""
        with codecs.open(filedialog.askopenfilename(parent=self.master,
                                    title='Select a log file',
                                    filetypes=(("Log Files", ("*.txt", "*.log"),),("All Files", "*.*"))
                                    ), encoding='UTF-8') as file:

        # with filedialog.askopenfile(parent=self.master,
        #                             mode='rb',
        #                             title='Select a log file',
        #                             filetypes=(("Log Files", ("*.txt", "*.log"),),("All Files", "*.*"))
        #                             ) as file:

            if file is not None:
                try:
                    contents = file.read()

                    # insert unscanned log into the log_textpad
                    self.log_scrolledtext.delete('1.0', END)
                    self.log_scrolledtext.insert('1.0', contents)

                    # Check the categories to search for
                    self.update_categories()

                    # insert scanned log into the scan_textpad
                    self.scanner.input_file = file.name
                    self.scanner.output_file = 'scan_output.txt'
                    self.scanner.search_log()

                    with open('scan_output.txt', 'r', encoding='UTF-8') as scan_file:
                        scan_contents = scan_file.read()
                        self.scan_scrolledtext.delete('1.0', END)
                        self.scan_scrolledtext.insert('1.0', scan_contents)

                except Exception as e:
                    print(e)
                    messagebox.showinfo('Error', 'Error occurred while opening file: {}'.format(e))

    def save_file_command(self):
        """Saves the contents of scan_scrolledtext to a file"""
        file = filedialog.asksaveasfile(mode='w', defaultextension=".txt", initialdir=os.getcwd())

        if file is not None:
            # slice off last character from end, because an extra return is added
            data = self.scan_scrolledtext.get('1.0', END+'-1c')
            file.write(data)
            file.close()

    def scan_textbox_command(self):
        """Scan the contents of the log_scrolledtext, so that users can have a way to scan pasted text"""
        with open('logtextbox.txt', 'w', encoding="UTF-8") as file:
            log_text = self.log_scrolledtext.get(1.0, END)
            file.write(log_text)

            # search the contents if there are any
            if file is not None:
                try:
                    # Check the categories to search for
                    self.update_categories()

                    # insert scanned log into the scan_textpad
                    self.scanner.input_file = file.name
                    self.scanner.output_file = 'scan_output.txt'
                    self.scanner.search_log()
                    with open('scan_output.txt', 'r', encoding='UTF-8') as scan_file:
                        scan_contents = scan_file.read()
                        self.scan_scrolledtext.delete('1.0', END)
                        self.scan_scrolledtext.insert('1.0', scan_contents)

                except Exception as e:
                    messagebox.showinfo('Error', 'Error occurred while opening file: {}'.format(e))


    def update_categories(self):
        """Checks which categories are enabled to be searched for and updates the scanners .search_categories"""

        # Updates Connectivity + Modem category
        if self.connectivity_checkbox.get():
            self.scanner.add_category('Connectivity+Modem')
        else:
            self.scanner.remove_category('Connectivity+Modem')

        # Updates IPSec category
        if self.ipsec_checkbox.get():
            self.scanner.add_category('IPSec')
        else:
            self.scanner.remove_category('IPSec')

        # Updates Routing Protocols category
        if self.routing_protocols_checkbox.get():
            self.scanner.add_category('Routing Protocols')
        else:
            self.scanner.remove_category('Routing Protocols')

        # Updates NCP category
        if self.ncp_checkbox.get():
            self.scanner.add_category('NCP')
        else:
            self.scanner.remove_category('NCP')

        # Updates NCM category
        if self.ncm_checkbox.get():
            self.scanner.add_category('NCM')
        else:
            self.scanner.remove_category('NCM')

    def update_scan(self):
        """Updates the scan results when a check box is checked/unchecked"""
        # checks to make sure a file has been opened, if not, doesn't update the search
        if self.scanner.input_file is not None:
            # Check the categories to search for
            self.update_categories()

            # Search the log with the updated categories
            self.scanner.search_log()
            with open('scan_output.txt', 'r', encoding='UTF-8') as scan_file:
                scan_contents = scan_file.read()
                self.scan_scrolledtext.delete('1.0', END)
                self.scan_scrolledtext.insert('1.0', scan_contents)

    def exit_command(self):
        """Quits the program"""
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.master.destroy()

    def about_command(self):
        """Displays information about the program"""
        messagebox.showinfo("About", "Cradlepoint Log Analyzer\n\nThis program analyzes Cradlepoint logs "
                                             "to look for common messages and display their meanings."
                                             "\n\nMade by Harvey Breaux for Cradlepoint")

    def find_text(self, event):
        """Searches current textbox for search text"""
        print("find_text triggered + {}".format(event))



root = Tk()
gui = LogGui(root)

root.mainloop()
