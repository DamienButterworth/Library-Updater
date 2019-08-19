#!/usr/bin/env python3

import os


def yes_no_question(question: str):
    if not os.environ.get("LIBRARY_UPGRADE_TEST"):
        user_input = input(question + " (Y/N) ")
        if user_input.lower() == "n":
            return False
        else:
            return True
    else:
        return False


def comma_str_to_list():
    if not os.environ.get("LIBRARY_UPGRADE_TEST"):
        entered_repos = input("Repository Names (Comma Separated): ")
        return entered_repos.replace(" ", "").split(",")
    else:
        return ["external-portal-stub", "one-time-password-admin-frontend"]


def extract_user_string(question: str):
    return input(question)
