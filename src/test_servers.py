# encoding:utf-8
"""Test echo socket communication."""

# import pytest
# import sys


PARAMS_TABLE = [
    'Yo',
    'This is a longer message, longer than most other messages.',
    'This has sixteen',
]


# @pytest.mark.parametrize("result", PARAMS_TABLE)
# def test_message_completion(result):
#     """Test table of potential messages for receipt and transmission."""
#     from client import client
#     assert client(result) == result


# def test_message_unicode():
#     """Test for unicode messages."""
#     from client import client
#     msg = 'CÅT'
#     if sys.version_info[0] == 2:
#         assert client(msg) == msg.decode('utf8')
#     else:
#         assert client(msg) == msg


def test_response_ok():
    """Test good connection message from server returns correct string."""
    from server import response_ok
    assert response_ok() == 'HTTP/1.1 200 OK\n\r\n'


def test_response_error():
    """Test 500 error message from server returns correct string."""
    from server import response_error
    assert response_error() == 'HTTP/1.1 500 Internal Server Error\n\r\n'
