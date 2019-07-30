#!/usr/bin/env python3

import os
import subprocess

from graphqlclient import GraphQLClient


def git(*args):
    return subprocess.check_call(['git'] + list(args))


def hub(*args):
    return subprocess.check_call(['hub'] + list(args))


def verify_hub_installed():
    try:
        subprocess.check_call(['hub'] + list(["--version"]))
        print("Hub installed, continuing")
    except FileNotFoundError:
        print("Please ensure to install the command-line tool 'hub' found at https://github.com/github/hub")
        exit(0)


client = GraphQLClient('https://api.github.com/graphql')
client.inject_token(os.environ.get('GITOAUTH'))  # OauthToken 'bearer {token}'


def push_changes(branch_name, commit_message):
    try:
        git("checkout", "-b" + branch_name)
        git("add", ".")
        git("commit", "-am", commit_message)
        git("push", "--set-upstream", "origin", branch_name)
    except subprocess.CalledProcessError:
        print("No Changes Detected")


# Ensure Oauth token is defined in the hub config.
def raise_pull_request(message):
    try:
        hub("pull-request", "-m", message)
    except subprocess.CalledProcessError:
        print("No PR Raised")
