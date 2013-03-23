import re


def password_is_good(password):
    """
    Check that a password complies with the policy and return the result and
    corresponding message

    """
    min_length = 7
    if len(password) < min_length:
        return False, 'Password is not long enough.'
    if not contains_digits(password):
        return False, 'Password must contain digits.'
    if not contains_letters(password):
        return False, 'Password must contain letters.'
    if not is_mixed_case(password):
        return False, 'Password must contain both upper & lower case letters.'
    if not contains_special_characters(password):
        return False, 'Password does not contain a special character.'
    if not is_printable(password):
        return False, 'Password contains invalid characters.'
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
