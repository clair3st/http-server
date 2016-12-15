"""functions to build the server side of echo."""

from __future__ import unicode_literals
from sys import version_info
import socket

PORT_NUMBER = 5017


def server():
    """Set up the server side to listen."""
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
    )
    address = ('127.0.0.1', PORT_NUMBER)
    server.bind(address)

    server.listen(1)
    print("Listening...")

    conn, addr = server.accept()

    while True:
        try:
            buffer_length = 8
            client_request = u''
            while client_request[-2:] != u"\r\n":
                part = conn.recv(buffer_length)
                client_request += part.decode('utf8')

            print(client_request)
            conn.sendall(response_ok().encode('utf8'))
            conn.sendall(client_request.encode('utf8'))
            conn, addr = server.accept()

        except KeyboardInterrupt:
            print('\nClosing echo server...')
            break

        # except StandardError:
        #     conn.sendall(server_bad_connection().encode('utf8'))
        #     break
    conn.close()
    server.close()


def response_ok():
    """Send a HTTP response to client."""
    message = 'HTTP/1.1 200 OK\n'
    if version_info[0] == 2:
        message = message.decode('utf-8')
    message += u"\r\n"
    return message


def response_error(exception):
    """Send a HTTP response to client if bad request."""
    error_codes = {
        '405': 'Method Not Allowed\n',
        '400': 'Bad Request\n',
        '505': 'HTTP Version Not Supported\n',
        '500': 'Internal Server Error\n'
    }
    if exception in error_codes:
        message = exception + ' ' + error_codes[exception]
        if version_info[0] == 2:
            message = message.decode('utf-8')
    message += u"\r\n"
    return message


def parse_request(header):
    """Check header from client."""
    header = header.split(' ', 4)

    try:
        method, uri, protocol, host = header

    except ValueError:
        raise SyntaxError
    if method is not 'GET':
        raise NameError
    elif protocol[:9] is not 'HTTP/1.1':
        raise ValueError
    elif '127.0.0.1' not in host and str(PORT_NUMBER) not in host:
        raise TypeError
    return uri


if __name__ == '__main__':
    server()
