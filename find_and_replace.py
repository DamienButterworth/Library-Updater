#!/usr/bin/env python3

import user_input
import file_handler

directory = user_input.extract_user_string("Directory to scan for files? ")
file_name = user_input.extract_user_string("Filename e.g. '.txt' or 'SsoConnector.scala: '")
search_string = user_input.extract_user_string("String to replace: ")
replace_string = user_input.extract_user_string("Replace String with: ")

for file in file_handler.get_files_in_dir_rec(file_name, directory):

    opened_file = open(file, "r")
    new_lines = ""
    for line in opened_file:
        line = file_handler.replace_line(line, search_string, replace_string)
        new_lines += line
    opened_file.close()

    with open(file, 'w') as w:
        w.write(new_lines)