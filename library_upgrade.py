#!/usr/bin/env python3
from typing import Pattern, Optional, List

import user_input
import file_handler
import git_requests
import os
import re

from latest_hmrc_release import HmrcReleaseSearch

'''
matches sbt dependencies e.g. `"com.some-org" % "some-library" % "0.1.0"` 

^[^"]* - consume all characters before the first `"`
"([^"]+)" - captures the first quoted group (without the quotes) (i.e. the organisation)
[^%]*%+[^"]* - consumes all characters between the organisation and the library name, expecting at least one `%`
"([^"]+)" - captures the second quoted group (without the quotes) (i.e. the library name)
[^%]*%[^"]* - consumes all characters between the library name and the library version, expecting a single `%`
"([^"]+)" - captures the third quoted group (without the quotes) (i.e. the version)
.*$ - consumes the rest of the line
'''
library_dependency_regex = re.compile(
    r'^[^"]*"([^"]+)"[^%]*%+[^"]*"([^"]+)"[^%]*%[^"]*"([^"]+)".*$')  # type: Pattern[str]


def get_libraries():
    libs = []

    for filename in file_handler.get_files_in_dir([".scala", ".sbt"], os.getcwd()):
        opened_file = open(filename, "r")
        for line in opened_file:
            matched_library = library_dependency_regex.match(line)
            if matched_library:
                libs.append(matched_library)

    return libs


def get_sbt_plugin_version():
    for file in file_handler.get_files_in_dir([".scala", ".sbt"], os.getcwd()):
        lines = file_handler.find_lines("\"" + "sbt-plugin" "\"", file)
        if lines:
            return lines[0].split("%")[-1].replace(")", "").replace("\n", "").replace(" ", "").replace("\"", "")


def update_libraries(file_name, lib, sbt_plugin_version):
    opened_file = open(file_name, "r")
    new_lines = ""
    for line in opened_file:
        if lib.string in line:
            new_version = HmrcReleaseSearch().fetch_release(sbt_plugin_version, lib)
            if new_version:
                line = file_handler.replace_line(line, lib.group(3), new_version)
        new_lines += line
    opened_file.close()

    with open(file_name, 'w') as w:
        w.write(new_lines)


def upgrade_repos(entered_repos: List[str], auto_push: bool, auto_raise_pr: bool, branch_name: Optional[str],
                  commit_message: Optional[str]):
    for repo_name in entered_repos:
        try:
            location = git_requests.download_repository(repo_name, "/tmp/")
            os.chdir(location)
            if os.path.isdir("project"):
                os.chdir("project")
                sbt_plugin_version = get_sbt_plugin_version()
                for library in get_libraries():
                    files = file_handler.get_files_in_dir([".scala", ".sbt"], os.getcwd())
                    for file in files:
                        update_libraries(file, library, sbt_plugin_version)
                git_requests.git_auto(auto_push, auto_raise_pr, branch_name, commit_message)
            else:
                print("project folder not found in: " + repo_name)
        except TypeError:
            print("Something Went Wrong")


def run_main():
    git_requests.verify_hub_installed()

    auto_push = user_input.yes_no_question("Do you want to automatically push to branch name?")  # type: bool
    auto_raise_pr = user_input.yes_no_question("Do you want to automatically raise a pull request?")  # type: bool
    clean_project = user_input.yes_no_question("Do you want to remove the repository after changes?")  # type: bool

    entered_repos = user_input.comma_str_to_list()  # type: List[str]

    if auto_push:
        branch_name = user_input.extract_user_string("Branch Name: ")
        commit_message = user_input.extract_user_string("Commit Message:")
    else:
        branch_name, commit_message = None, None

    upgrade_repos(entered_repos, auto_push, auto_raise_pr, branch_name, commit_message)

    if clean_project:
        file_handler.remove_tmp_folders(entered_repos)

    print("Finished Successfully")


if __name__ == '__main__':
    run_main()
