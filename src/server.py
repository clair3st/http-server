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
            try:
                parse_request(client_request)
                conn.sendall(response_ok())
            except SyntaxError:
                conn.sendall(response_error('400'))
            except NameError:
                conn.sendall(response_error('405'))
            except ValueError:
                conn.sendall(response_error('505'))
            except TypeError:
                conn.sendall(response_error('404'))

            conn, addr = server.accept()

        except KeyboardInterrupt:
            print('\nClosing echo server...')
            break

    conn.close()
    server.close()


def response_ok():
    """Send a HTTP response to client."""
    message = 'HTTP/1.1 200 OK\n'
    if version_info[0] == 2:
        message = message.decode('utf-8')
    message += u"\r\n"
    return message.encode('utf8')


def response_error(exception):
    """Send a HTTP response to client if bad request."""
    error_codes = {
        '405': 'Method Not Allowed\n',
        '400': 'Bad Request\n',
        '505': 'HTTP Version Not Supported\n',
        '500': 'Internal Server Error\n',
        '404': 'Not Found\n'
    }
    if exception in error_codes:
        message = exception + ' ' + error_codes[exception]
        if version_info[0] == 2:
            message = message.decode('utf-8')
    message += u"\r\n"
    return message.encode('utf8')


def parse_request(header):
    """Check header from client."""
    """#TODO: What if there's a body after?"""
    header = header.split(' ', 4)
    print(header)

    try:
        method, uri, protocol, address, port = header
        # print("Method: " + method)
        # print(type(method))
        # print("uri: " + uri)
        # print("protocol: " + protocol)
        # print(protocol[:9])
        # print("address: " + address)
        # print("port: " + port)

    except ValueError:
        raise SyntaxError
    if method != 'GET':
        raise NameError
    elif protocol[:8] != 'HTTP/1.1':
        raise ValueError
    elif '127.0.0.1' not in address and str(PORT_NUMBER) not in port:
        raise TypeError
    return uri


if __name__ == '__main__':
    server()
