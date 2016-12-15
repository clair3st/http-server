# encoding:utf-8
"""Test echo socket communication."""

import pytest
# import sys

HEADER = 'GET /src/server.py HTTP/1.1<CRLF> Host: 127.0.0.1:5017<CRLF><CRLF>'

ECHO_MESSAGES = [
    'Yo',
    'This is a longer message, longer than most other messages.',
    'This has sixteen',
]

CLIENT_MESSAGES = [
    ["GET /index.html HTTP/1.1<CRLF> Host: 127.0.0.1 5017<CRLF>", "HTTP/1.1 200 OK\n"],
    ['GET /src/server.py HTTP/1.1<CRLF> Host: 127.0.0.1:80<CRLF><CRLF>', "404 Not Found\n"],
    ['PUT /src/server.py HTTP/1.1<CRLF> Host: 127.0.0.1:5017<CRLF><CRLF>', "405 Method Not Allowed\n"],
    ['/src/server.py HTTP/1.1<CRLF> Host: 127.0.0.1:5017<CRLF><CRLF>', "400 Bad Request\n"],
    ['GET /src/server.py HTTP/1.0<CRLF> Host: 127.0.0.1:5017<CRLF><CRLF>', "505 HTTP Version Not Supported\n"],
]

ERROR_CODES = [
    ['405', b'405 Method Not Allowed\n\r\n'],
    ['400', b'400 Bad Request\n\r\n'],
    ['505', b'505 HTTP Version Not Supported\n\r\n'],
    ['500', b'500 Internal Server Error\n\r\n'],
    ['404', b'404 Not Found\n\r\n']
]

HEADER_ERRORS = [
    ['GET /src/server.py HTTP/1.1<CRLF> Host: 127.0.0.1:80<CRLF><CRLF>', TypeError],
    ['PUT /src/server.py HTTP/1.1<CRLF> Host: 127.0.0.1:5017<CRLF><CRLF>', NameError],
    ['/src/server.py HTTP/1.1<CRLF> Host: 127.0.0.1:5017<CRLF><CRLF>', SyntaxError],
    ['GET /src/server.py HTTP/1.0<CRLF> Host: 127.0.0.1:5017<CRLF><CRLF>', ValueError],
]

# @pytest.mark.parametrize("result", ECHO_MESSAGES)
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
    assert response_ok() == b'HTTP/1.1 200 OK\n\r\n'


@pytest.mark.parametrize("code, result", ERROR_CODES)
def test_response_error(code, result):
    """Test response error for correct error messages for a given code."""
    from server import response_error
    assert response_error(code) == result


@pytest.mark.parametrize("header, error", HEADER_ERRORS)
def test_parse_request_errors(header, error):
    """Test if correct errors get raised for different headers."""
    from server import parse_request
    with pytest.raises(error):
        parse_request(header)


def test_parse_request_correct():
    """Test for 200 response if correct header used."""
    from server import parse_request
    assert parse_request(HEADER) == '/src/server.py'


@pytest.mark.parametrize("message, result", CLIENT_MESSAGES)
def test_server_loop(message, result):
    """Test that server loop functions as expected."""
    from client import client
    assert client(message) == result

