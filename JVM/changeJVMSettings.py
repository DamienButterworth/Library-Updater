#!/usr/bin/env python3

import os
import shutil
import re
import repo_list

from typing import TextIO

import git_requests


class bcolors:
    OLD = '\033[91m'
    NEW = '\033[92m'
    ENDC = '\033[0m'


def get_file(file_name, file_type, parent_dir):
    for file in os.listdir(parent_dir):
        if file.endswith(file_name + file_type):
            return file


def download_repository(repo_name):
    destination_path = "/tmp/" + repo_name

    if not os.path.isdir(destination_path):
        os.mkdir(destination_path)
    else:
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)

    git_requests.clone("git@github.com:/hmrc/" + repo_name, "--depth 1", destination_path)
    return destination_path


def get_lines(file_name, containing, parent_dir):
    lines_found = []
    opened_file = open(parent_dir + "/" + file_name, "r")
    for line in opened_file:
        if containing in line:
            lines_found.append(line)
    return lines_found


def find_replace(file_name, search_str, replace_str, parent_dir):
    file_dir = parent_dir + "/" + file_name
    doc_lines = ""
    opened_file: TextIO = open(file_dir, "r")
    print(opened_file)
    for t in opened_file.readlines():
        if search_str in t:
            t = t.replace(search_str, replace_str)
        doc_lines += t
    opened_file.close()
    with open(file_dir, 'w') as w:
        w.write(doc_lines)


slotsRegEx = re.compile('(.*)([0-9])(.*)')

location = download_repository("app-config-production")
file = get_file("bas-gateway", ".yaml", location)
lines = get_lines(file, "slots:", location)
mem_line = get_lines(file, "mx:", location)

environments = ["development"]


for env in environments:
    for repo in repo_list.repos:
        if "512" in mem_line[0]:
            slots_line = get_lines(file, "slots:", location)
            groups = re.match(slotsRegEx, slots_line[0])

            print(groups.group(1))
            print(groups.group(2))
            print(groups.group(3))

            find_replace(file, slots_line[0], groups.group(1) + "9" + groups.group(3), location)
        elif "256" in mem_line[0]:
            slots_line = get_lines(file, "slots:", location)
            groups = re.match(slotsRegEx, slots_line[0])

            print(groups.group(1))
            print(groups.group(2))
            print(groups.group(3))

            find_replace(file, slots_line[0], groups.group(1) + "5" + groups.group(3), location)
        elif "384" in mem_line[0]:
            slots_line = get_lines(file, "slots:", location)
            groups = re.match(slotsRegEx, slots_line[0])

            print(groups.group(1))
            print(groups.group(2))
            print(groups.group(3))

            find_replace(file, slots_line[0], groups.group(1) + "7" + groups.group(3), location)
        else:
            print("check manually")

    git_requests.push_changes("GG-3997", "updated slots")
    git_requests.raise_pull_request("GG-3997")



