#!/usr/bin/env python3

import os
import shutil
import collections

from src.helpers import logger as l
from pathlib import Path
from typing import Optional, List


class ChangeColors:
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
        l.r_message("Old Version: " + line + "\n")
        l.g_message("New Version: " + line.replace(old_line, new_line) + "\n")
        return line.replace(old_line, new_line)
    else:
        return line


def count_duplicate_lines(file_path):
    with open(file_path) as file:
        counts = collections.Counter(l.strip() for l in file)
        for line, count in counts.most_common():
            print("Line: " + line.replace(",", "").replace("\"", "") + "\nCount: " + str(count) + "\n")

