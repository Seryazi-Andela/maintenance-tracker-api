import re


def empty_string_catcher(value):
    value = ' '.join(value.split())
    if not value:
        return False
    return True


def isString(value):
    if isinstance(value, str):
        return True
    return False


def isInteger(value):
    if isinstance(value, int):
        return True
    return False


def isBool(value):
    if isinstance(value, bool):
        return True
    return False


def email_validator(value):
    if re.match(r"[a-zA-z0-9.]+@[a-z]+\.[a-z]+", value):
        return True
    return False
