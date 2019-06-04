# Cradlepoint Log Parser

Cradlepoint Log Parser is a Python program that takes a Cradlepoint log and parses it for interesting/problematic lines.  It outputs a file containing the problem lines and their most likely meanings. 

scan_log.py is the main part of the project.  It pulls lines from the xlxs database, turns them into a regex, and searchs through log lines for matches. 

The current GUI for the project is log_analyzer_gui.py It displays your full log file on the left, and the search output on the right.
You can scroll through either textbox to examine and compare the output.
