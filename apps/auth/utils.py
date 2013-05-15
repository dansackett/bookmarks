import re


def password_is_good(password):
    """
    Check that a password complies with the policy and return the result and
    corresponding message

    """
    min_length = 8
    if len(password) < min_length:
        return False, 'Passwords must be {} characters long.'.format(min_length)
    return True, None


def contains_special_characters(string):
    """Return True if sting contains special characters else return False"""
    for char in '!@#$%^&*?_~':
        if char in string:
            return True
    return False


def contains_letters(string):
    """Return True if string contains letters else return False"""
    return bool(re.search(r'[a-z]', string, re.IGNORECASE))


def contains_digits(string):
    """Return True if string contains numeric digits else return False"""
    return bool(re.search(r'[0-9]', string))


def is_mixed_case(string):
    """Return True if string contains upper and lower letters else return False"""
    return not (string.lower() == string or string.upper() == string)


def is_printable(string):
    """Return True if string is a printable entity else return False"""
    if re.search(r'[^ -~]', string):
        return False
    return True


def valid_username(string):
    return bool(re.match('^[\w.@+-]+$', string))
