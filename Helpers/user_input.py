#!/usr/bin/env python3

import os
from Helpers import logger as log


def yes_no_question(question: str):
    if not os.environ.get("LIBRARY_UPGRADE_TEST"):
        user_input = input(question + " (Y/N) ")
        if user_input.lower() == "n" or user_input.lower() == "no":
            return False
        elif user_input.lower() == "y" or user_input.lower() == "yes":
            return True
        else:
            log.error("Please Enter Valid Response ('Y' or 'N')")
            yes_no_question(question)
    else:
        return False


def comma_str_to_list():
    if not os.environ.get("LIBRARY_UPGRADE_TEST"):
        entered_repos = input("Repository Names (Comma Separated): ")
        user_response = entered_repos.replace(" ", "").split(",")
        if '' in user_response:
            log.error("Empty string detected please ensure services are seperated by comma e.g. bas-gateway, "
                    "bas-stubs")
            comma_str_to_list()
        else:
            return entered_repos.replace(" ", "").split(",")
    else:
        return ["external-portal-stub", "one-time-password-admin-frontend"]


def extract_user_string(question: str):
    return input(question)
