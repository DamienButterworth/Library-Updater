#!/usr/bin/env python3

from typing import Pattern, Optional, List


class ErrorColors:
    error = '\033[91m'
    warn = '\033[92m'
    end = '\033[0m'


def error(msg: str):
    print(ErrorColors.error + msg + ErrorColors.end)


def g_message(msg: str):
    print(ErrorColors.warn + msg + ErrorColors.end)


def r_message(msg: str):
    print(ErrorColors.error + msg + ErrorColors.end)
