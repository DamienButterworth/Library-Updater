#!/usr/bin/env python3

from typing import Pattern

import os
import shutil
import git_requests
import re


def download_repository(repo_name, organisation_name, destination):
    destination_path = destination + repo_name

    if not os.path.isdir(destination_path):
        os.mkdir(destination_path)
    else:
        # remove = input("Directed already exists, do you want to remove? Y | N ")
        remove = "y"
        if remove.lower() == "y":
            shutil.rmtree(destination_path)
            os.mkdir(destination_path)
    git_requests.clone("git@github.com:/" + organisation_name + "/" + repo_name, "--depth 1", destination_path)
    return destination_path


def check_line(search_values, line):
    for value in search_values:
        if value not in line:
            return False
    return True


def find_and_replace(search_values, folder_path, new_entry):

    for file in os.listdir(folder_path):
        new_lines = ""
        opened_file = open(folder_path + "/" + file, "r")
        for line in opened_file:
            if check_line(search_values, line):
                regex = re.compile(r'(\s+).*')  # type: Pattern[str]
                leading_whitespace = regex.match(line)
                if leading_whitespace.group(1):
                    line = line.replace(line, line + leading_whitespace.group(1) + new_entry + "\n")
                else:
                    line = line.replace(line, line + new_entry + "\n")
            new_lines += line
        opened_file.close()
        with open(folder_path + "/" + file, 'w') as w:
            w.write(new_lines)


services = [
            "bas-proxy",
            "bas-stub-frontend",
            "bas-stubs",
            "company-auth-frontend",
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

branch_name = input("Branch Name: ")
commit_message = input("Commit Message: ")

for service in services:
    download_repository(service, "hmrc", "/tmp/")
    find_and_replace(["majorVersion", ".settings"], "/tmp/" + service + "/project",
                    ".settings(excludeDependencies ++= Seq(SbtExclusionRule(\"uk.gov.hmrc\", \"play-authorised-frontend_2.11\"), SbtExclusionRule(\"uk.gov.hmrc\", \"play-authorisation_2.11\")))")
    os.chdir("/tmp/" + service + "/project")
    git_requests.push_changes(branch_name, commit_message)
    git_requests.raise_pull_request(branch_name)

