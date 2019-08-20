#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from typing import Optional, List



class BColors:
    old = '\033[91m'
    new = '\033[92m'
    end = '\033[0m'


def get_files_in_dir(file_types: List[str], directory: str):
    files = []
    for file in os.listdir(directory):
        for t in file_types:
            if file.endswith(t):
                files.append(directory + "/" + file)
    return files


def get_files_in_dir_rec(file_name: str, directory: str):
    files = []
    for filename in Path(directory).glob("**/*"):
        if file_name.lower() in filename.name.lower():
            files.append(filename.as_posix())
    return files


def remove_tmp_folders(folders: List[str]):
    for folder in folders:
        print("Removing Folder " + folder)
        shutil.rmtree("/tmp/" + folder)


def find_lines(search_string: str, file, show_line_number: Optional[bool] = None):
    lines = []
    line_number = 0
    opened_file = open(file, "r")
    for line in opened_file:
        line_number += 1
        if search_string in line:
            if show_line_number:
                lines.append((line, line_number))
            else:
                lines.append(line)
    if lines:
        return lines


def replace_line(line, old_line, new_line):
    if str(old_line) != str(new_line):
        print(BColors.old + "Old Version: " + line + BColors.end)
        print(BColors.new + "New Version: " + line.replace(old_line, new_line) + BColors.end)
        return line.replace(old_line, new_line)
    else:
        return line
