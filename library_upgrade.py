#!/usr/bin/env python3
from typing import Pattern, Optional

import git_requests
import os
import re
import latest_hmrc_release
import shutil


class bcolors:
    OLD = '\033[91m'
    NEW = '\033[92m'
    ENDC = '\033[0m'


def extract_repo_names(value: str):
    return value.replace(" ", "").split(",")


def download_repository(repo_name):
    destination_path = "/tmp/" + repo_name

    if not os.path.isdir(destination_path):
        os.mkdir(destination_path)
    else:
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)

    git_requests.clone("git@github.com:/hmrc/" + repo_name, "--depth 1", destination_path)
    return destination_path


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


def get_libraries(files):
    libs = []

    for filename in files:
        if filename.endswith(".scala") or filename.endswith(".sbt"):
            opened_file = open(filename, "r")
            for line in opened_file:
                matched_library = library_dependency_regex.match(line)
                if matched_library:
                    libs.append(matched_library)

    return libs


def get_sbt_plugin_version():
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".scala") or filename.endswith(".sbt"):
            opened_file = open(filename, "r")
            for line in opened_file:
                if "\"" + "sbt-plugin" "\"" in line:
                    return line.split("%")[-1].replace(")", "").replace("\n", "").replace(" ", "").replace("\"", "")


def search_file(file_name, lib):
    opened_file = open(file_name, "r")
    new_lines = ""
    sbt_plugin_version = get_sbt_plugin_version()

    for line in opened_file:
        if lib.string in line:
            old_version = lib.group(3)
            library_name = lib.group(2)
            domain = lib.group(1)

            new_version = latest_hmrc_release.fetch_release(sbt_plugin_version, library_name, old_version, domain)
            if new_version:
                if str(old_version) != str(new_version):
                    print(bcolors.OLD + "Old Version: " + line + bcolors.ENDC)
                    print(bcolors.NEW + "New Version: " + line.replace(old_version, new_version) + bcolors.ENDC)
                    line = line.replace(old_version, new_version)
        new_lines += line
    opened_file.close()

    with open(file_name, 'w') as w:
        w.write(new_lines)


def get_files(lib):
    for file in os.listdir(os.getcwd()):
        if file.endswith(".scala") or file.endswith(".sbt"):
            search_file(file, lib)


def clean_cloned_repos(entered_repos: str, clean_project: str):
    print(os.getcwd())
    if clean_project.lower() == "y":
        print("Removing Cloned Repos")
        for repo_name in extract_repo_names(entered_repos):
            shutil.rmtree("/tmp/" + repo_name)


def upgrade_repos(entered_repos: str,
                  auto_push: str,
                  auto_raise_pr: str,
                  branch_name: Optional[str],
                  commit_message: Optional[str]):
    for repo_name in extract_repo_names(entered_repos):
        try:
            location = download_repository(repo_name)
            os.chdir(location)
            if os.path.isdir("project"):
                os.chdir("project")
                libraries = get_libraries(os.listdir(os.getcwd()))
                for library in libraries:
                    get_files(library)
                if auto_push.lower() == "y":
                    git_requests.push_changes(branch_name, commit_message)
                if auto_raise_pr.lower() == "y":
                    git_requests.raise_pull_request(branch_name)
            else:
                print("project folder not found in: " + repo_name)

        except TypeError:
            print("Something Went Wrong")


def run_main():
    git_requests.verify_hub_installed()
    project_dir = os.getcwd()
    # remove this once there's real tests
    test_run = os.environ.get("LIBRARY_UPGRADE_TEST") is not None  # type: bool
    auto_push = "n" if test_run else input("Do you want to automatically push to branch name? (Y/N) ")  # type: str
    auto_raise_pr = "n" if test_run else input("Do you want to automatically raise a pull request? (Y/N) ")  # type: str
    clean_project = "n" if test_run else input(
        "Do you want to remove the repository after changes? (Y/N) ")  # type: str
    entered_repos = input("Repository Names (Comma Separated): ")
    if auto_push.lower() == "y" or auto_raise_pr.lower() == "y":
        branch_name = input("Branch Name: ")
        commit_message = input("Commit Message: ")
    else:
        branch_name, commit_message = None, None
    upgrade_repos(entered_repos, auto_push, auto_raise_pr, branch_name, commit_message)
    clean_cloned_repos(entered_repos, clean_project)

    print("Finished Successfully")


if __name__ == '__main__':
    run_main()
