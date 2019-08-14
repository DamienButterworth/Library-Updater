#!/usr/bin/env python3

import os
import shutil
import git_requests


class bcolors:
    OLD = '\033[91m'
    NEW = '\033[92m'
    ENDC = '\033[0m'


def get_files(repo_name):
    for file in os.listdir(os.getcwd()):
        if file.endswith(repo_name + ".yaml"):
            search_file(file)


repos = [
    "bas-gateway",
    "bas-gateway-frontend",
    "bas-integration-tests",
    "bas-proxy",
    "bas-stub-frontend",
    "bas-stubs",
    "company-auth-frontend",
    "dashing-dashboards",
    "external-portal-stub",
    "gateway-demo-frontend",
    "government-gateway-authentication",
    "government-gateway-registration-frontend",
    "multi-factor-authentication",
    "multi-factor-authentication-frontend",
    "one-time-password",
    "one-time-password-admin-frontend",
    "poison-password",
    "reauthentication",
    "reauthentication-frontend",
    "security-console-frontend",
    "silent-login-admin",
    "silent-login-admin-frontend",
    "sms-gateway",
    "sms-gateway-admin-frontend",
    "sms-provider-stubs",
    "sso",
    "sso-frontend",
    "time-based-one-time-password",
    "two-step-verification-rule-engine"
]



check_list = [
    "public-mongo-1",
    "public-mongo-2",
    "public-mongo-3",
    "protected-mongo-1",
    "protected-mongo-2",
    "protected-mongo-3",
    "public-auth-mongo-1",
    "public-auth-mongo-2",
    "public-auth-mongo-3",
    "protected-auth-mongo-1",
    "protected-auth-mongo-2",
    "protected-auth-mongo-3",
    "public-rate-mongo-1",
    "public-rate-mongo-2",
    "public-rate-mongo-3",
    "protected-rate-mongo-1",
    "protected-rate-mongo-2",
    "protected-rate-mongo-3",
    "public-monolith-mongo-1",
    "public-monolith-mongo-2",
    "public-monolith-mongo-3"
]

change_list = [
    "public-mongo-eu-west-2a-1",
    "public-mongo-eu-west-2b-1",
    "public-mongo-eu-west-2c-1",
    "protected-mongo-eu-west-2a-1",
    "protected-mongo-eu-west-2b-1",
    "protected-mongo-eu-west-2c-1",
    "public-auth-mongo-eu-west-2a-1",
    "public-auth-mongo-eu-west-2b-1",
    "public-auth-mongo-eu-west-2c-1",
    "protected-auth-mongo-eu-west-2a-1",
    "protected-auth-mongo-eu-west-2b-1",
    "protected-auth-mongo-eu-west-2c-1",
    "public-rate-mongo-eu-west-2a-1",
    "public-rate-mongo-eu-west-2b-1",
    "public-rate-mongo-eu-west-2c-1",
    "protected-rate-mongo-eu-west-2a-1",
    "protected-rate-mongo-eu-west-2b-1",
    "protected-rate-mongo-eu-west-2c-1",
    "public-monolith-mongo-eu-west-2a-1",
    "public-monolith-mongo-eu-west-2b-1",
    "public-monolith-mongo-eu-west-2c-1"
]


def search_file(file_name):
    opened_file = open(file_name, "r")
    new_lines = ""

    for line in opened_file:
        for i in range(len(check_list)):
            old_string = check_list[i]
            new_string = change_list[i]

            if old_string in line:
                print(bcolors.OLD + "Old Version: " + line + bcolors.ENDC)
                print(bcolors.NEW + "New Version: " + line.replace(old_string,
                                                                   new_string) + bcolors.ENDC)
                line = line.replace(old_string, new_string)
        new_lines += line

    opened_file.close()

    with open(file_name, 'w') as w:
        w.write(new_lines)


auto_push = input("Do you want to automatically push to branch name? (Y/N) ")  # type: str
auto_raise_pr = input("Do you want to automatically raise a pull request? (Y/N) ")  # type: str
clean_project = input("Do you want to remove the repository after changes? (Y/N) ")  # type: str

entered_repos = input("Repository Names (Comma Separated): ")

if auto_push.lower() == "y" or auto_raise_pr.lower() == "y":
    branch_name = input("Branch Name: ")
    commit_message = input("Commit Message: ")


def download_repository():
    tmp = "app-config-production"

    destination_path = "/tmp/" + tmp

    if not os.path.isdir(destination_path):
        os.mkdir(destination_path)
    else:
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)

    git_requests.clone("git@github.com:/hmrc/" + tmp, "--depth 1", destination_path)
    return destination_path


def extract_repo_names(value):
    return value.replace(" ", "").split(",")


location = download_repository()

for repo_name in repos:
    try:
        os.chdir(location)
        get_files(repo_name)
    except TypeError:
        print("Something Went Wrong")

if auto_push.lower() == "y":
    git_requests.push_changes(branch_name, commit_message)
if auto_raise_pr.lower() == "y":
    git_requests.raise_pull_request(branch_name)
if clean_project.lower() == "y":
    shutil.rmtree(location)
