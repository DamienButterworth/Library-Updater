#!/usr/bin/env python3

import subprocess
from typing import Optional


def git(*args):
    return subprocess.check_call(['git'] + list(args))


def clone(repo_uri: str, args: Optional[str] = None, target: Optional[str] = None):
    exit_code = subprocess.check_call(["git", "clone"] + args.split(" ") + ["--", repo_uri, target])
    print("successfully cloned from " + repo_uri + (" into " + target) if target else "")
    return exit_code


def hub(*args):
    return subprocess.check_call(['hub'] + list(args))


def verify_hub_installed():
    try:
        subprocess.check_call(['hub'] + list(["--version"]))
        print("Hub installed, continuing")
    except FileNotFoundError:
        print("Please install the command-line tool 'hub' found at https://github.com/github/hub")
        exit(1)


def push_changes(branch_name, commit_message):
    git("checkout", "-b" + branch_name)
    git("add", ".")

    try:
        git("commit", "-am", commit_message)
    except subprocess.CalledProcessError:
        print("No Changes Detected")

    git("push", "--set-upstream", "origin", branch_name)


# Ensure Oauth token is defined in the hub config.
def raise_pull_request(message):
    try:
        hub("pull-request", "-m", message)
    except subprocess.CalledProcessError:
        print("No PR Raised")
