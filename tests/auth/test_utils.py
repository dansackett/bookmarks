import pytest

from auth.utils import (
    contains_special_characters,
    contains_letters,
    contains_digits,
    is_mixed_case,
    is_printable,
    password_is_good,
    valid_username,
)


@pytest.mark.parametrize(('password', 'result'), [
    ('goodPassword23!', (True, None)),  # happy path
    ('ASdf', (False, 'Passwords must be 8 characters long.')),
])
def test_password_is_good(password, result):
    is_good, message = password_is_good(password)
    assert is_good is result[0]
    assert message == result[1]


@pytest.mark.parametrize(('string', 'result'), [
    ('asdf!1234', True),
    ('asdf@1234', True),
    ('asdf#1234', True),
    ('asdf$1234', True),
    ('asdf%1234', True),
    ('asdf^1234', True),
    ('asdf&1234', True),
    ('asdf*1234', True),
    ('asdf?1234', True),
    ('asdf_1234', True),
    ('asdf~1234', True),
    ('asdf', False),
    ('1234', False),
    ('asdf1234', False),
])
def test_contains_special_characters(string, result):
    assert contains_special_characters(string) is result


@pytest.mark.parametrize(('string', 'result'), [
   ('asdf', True),
   ('ASDF', True),
   ('asDF', True),
   ('1234', False),
   ('', False),
])
def test_contains_letters(string, result):
    assert contains_letters(string) is result


@pytest.mark.parametrize(('string', 'result'), [
   ('1234', True),
   ('asdf1', True),
   ('asdf', False),
   ('ASDF', False),
   ('asDF', False),
   ('', False),
])
def test_contains_digits(string, result):
    assert contains_digits(string) is result


@pytest.mark.parametrize(('string', 'result'), [
    ('ASdf', True),
    ('asdf', False),
    ('ASDF', False),
    ('1234', False),
    ('an34', False),
    ('AN34', False),
    ('an!?', False),
    ('AN!?', False),
    ('', False),
])
def test_is_mixed_case(string, result):
    assert is_mixed_case(string) is result


@pytest.mark.parametrize(('string', 'result'), [
    ('asdf1234', True),
    ('ASDF1234', True),
    ('asdfASDF', True),
    ('12345678', True),
    ('asdf!1234', True),
    ('asdf?1234', True),
    ('asdf%^&*(1234', True),
    ('asdf\x201234', True),  # make sure space chr(32) passes
    ('asdf\x7E1234', True),  # make sure tilde chr(126) passes
    ('asdf\x001234', False),  # nul chr(0)
    ('asdf\x1B1234', False),  # esc chr(27)
    ('asdf\x1F1234', False),  # us chr(31)
    ('asdf\x7F1234', False),  # del chr(127)
])
def test_is_printable(string, result):
    assert is_printable(string) is result


@pytest.mark.parametrize(('string', 'result'), [
    ('asdf@1234', True),
    ('asdf+1234', True),
    ('asdf-1234', True),
    ('asdf_1234', True),
    ('asdf!1234', False),
    ('asdf#1234', False),
    ('asdf$1234', False),
    ('asdf%1234', False),
    ('asdf^1234', False),
    ('asdf&1234', False),
    ('asdf*1234', False),
    ('asdf?1234', False),
    ('asdf~1234', False),
    ('1234', True),
    ('asdf1234', True),
])
def test_valid_username(string, result):
    assert valid_username(string) is result
