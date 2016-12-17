# encoding:utf-8
"""Test echo socket communication."""

import pytest
from server import PORT_NUMBER, ADDRESS


HEADER = 'GET /src/server.py HTTP/1.1\r\n Host: {}:{}\r\n\r\n'.format(
    ADDRESS,
    PORT_NUMBER
)

ECHO_MESSAGES = [
    'Yo',
    'This is a longer message, longer than most other messages.',
    'This has sixteen',
]

CLIENT_MESSAGES = [
    ['GET /src/server.py HTTP/1.1\r\n {}:{}\r\n\r\n'.format(
        ADDRESS,
        PORT_NUMBER
    ),
        "404 Not Found\n"],
    ['PUT /src/server.py HTTP/1.1\r\n Host: {}:{}\r\n\r\n'.format(
        ADDRESS,
        PORT_NUMBER
    ),
        "405 Method Not Allowed\n"],
    ['/src/server.py HTTP/1.1\r\n Host: {}:{}\r\n\r\n'.format(
        ADDRESS,
        PORT_NUMBER
    ),
        "400 Bad Request\n"],
    ['GET /src/server.py HTTP/1.0\r\n Host: {}:{}\r\n\r\n'.format(
        ADDRESS,
        PORT_NUMBER
    ),
        "505 HTTP Version Not Supported\n"],
]

ERROR_CODES = [
    ['405', b'405 Method Not Allowed\n\r\n\r\n'],
    ['400', b'400 Bad Request\n\r\n\r\n'],
    ['505', b'505 HTTP Version Not Supported\n\r\n\r\n'],
    ['500', b'500 Internal Server Error\n\r\n\r\n'],
    ['404', b'404 Not Found\n\r\n\r\n']
]

HEADER_ERRORS = [
    ['GET /src/server.py HTTP/1.1\r\n Host: {}:80<\r\n><\r\n>'.format(ADDRESS),
     TypeError],
    ['PUT /src/server.py HTTP/1.1\r\n Host: {}:{}<\r\n><\r\n>'.format(
        ADDRESS,
        PORT_NUMBER
    ),
        NameError],
    ['/src/server.py HTTP/1.1<\r\n> Host: {}:{}<\r\n><\r\n>'.format(
        ADDRESS,
        PORT_NUMBER
    ),
        SyntaxError],
    ['GET /src/server.py HTTP/1.0<\r\n> Host: {}:{}<\r\n><\r\n>'.format(
        ADDRESS,
        PORT_NUMBER
    ),
        ValueError],
]

URI = [
    ['''This is a very simple text file.
Just to show that we can serve it up.
It is three lines long.
''', 'text/plain']
]


FILE_TABLE = [
    ['/webroot/sample.txt', b'''This is a very simple text file.
Just to show that we can serve it up.
It is three lines long.
''', 'text/plain'],
    ['/webroot/a_web_page.html', b"""<!DOCTYPE html>\n<html>\n<body>\n\n<h1>Code Fellows</h1>\n\n<p>A fine place to learn Python web programming!</p>\n\n</body>\n</html>\n\n""", 'text/html'],
    ['/webroot/make_time.py', b'''#!/usr/bin/env python\n\n"""\nmake_time.py\n\nsimple script that returns and HTML page with the current time\n"""\n\nimport datetime\n\ntime_str = datetime.datetime.now().isoformat()\n\nhtml = """\n<http>\n<body>\n<h2> The time is: </h2>\n<p> %s <p>\n</body>\n</http>\n""" % time_str\n\nprint(html)\n''', 'text/x-python'],
    ['/webroot/images', '''<a src=JPEG_example.jpg>JPEG_example.jpg</a> <a src=sample_1.png>sample_1.png</a> <a src=Sample_Scene_Balls.jpg>Sample_Scene_Balls.jpg</a>''', 'text/html'],
]


def test_response_ok():
    """Test good connection message from server returns correct string."""
    from server import response_ok
    assert response_ok(URI[0]) == b'HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 95\n\r\nThis is a very simple text file.\nJust to show that we can serve it up.\nIt is three lines long.\n\r\n\r\n'


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
    assert client(message).decode('utf8') == result


@pytest.mark.parametrize("fname, body, content_type", FILE_TABLE)
def test_resolve_uri_correct_files_returned(fname, body, content_type):
    """Check that resolve uri returns correct tuple of content and type."""
    from server import resolve_uri
    assert resolve_uri(fname) == (body, content_type)


def test_resolve_uri_raises_error():
    """Test if correct errors get raised for different headers."""
    from server import resolve_uri
    with pytest.raises(IOError):
        resolve_uri('webroot/javascript.js')
