#!/usr/bin/env python3

import os
import shutil
from typing import List


class BColors:
    old = '\033[91m'
    new = '\033[92m'
    end = '\033[0m'


def get_files_in_dir(file_types: List[str], directory: str):
    files = []
    for file in os.listdir(directory):
        for t in file_types:
            if file.endswith(t):
                files.append(file)
    return files


def remove_tmp_folders(folders: List[str]):
    for folder in folders:
        print("Removing Folder " + folder)
        shutil.rmtree("/tmp/" + folder)


def find_lines(search_string: str, file):
    lines = []
    opened_file = open(file, "r")
    for line in opened_file:
        if search_string in line:
            lines.append(line)
    if lines:
        return lines
    else:
        return []


def replace_line(line, old_line, new_line):
    if str(old_line) != str(new_line):
        print(BColors.old + "Old Version: " + line + BColors.end)
        print(BColors.new + "New Version: " + line.replace(old_line, new_line) + BColors.end)
        return line.replace(old_line, new_line)
    else:
        return line
