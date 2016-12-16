"""functions to build the server side of echo."""

from __future__ import unicode_literals
from sys import version_info
import socket
import os

PORT_NUMBER = 5024
ADDRESS = '127.0.0.1'
BUFFER_LENGTH = 8


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
            client_request = u''
            while client_request[-4:] != u"\r\n\r\n":
                part = conn.recv(BUFFER_LENGTH)
                client_request += part.decode('utf8')

            print('Recieved request: ', client_request)
            try:
                parse = parse_request(client_request)
                response_body = resolve_uri(parse)
                conn.sendall(response_ok(response_body))
            except IOError:
                conn.sendall(response_error('404'))
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


def response_ok(response_body):
    """Send a HTTP response to client."""
    message = 'HTTP/1.1 200 OK\n'
    message += 'Content-Type: ' + response_body[1] + '\r\n' + response_body[0]
    if version_info[0] == 2:
        message = message.decode('utf-8')
    message += u"\r\n\r\n"
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
    message += u"\r\n\r\n"
    return message.encode('utf8')


def parse_request(header):
    """Check header from client."""
    header = header.split(' ', 4)

    try:
        method, uri, protocol, address, port = header

    except ValueError:
        raise SyntaxError
    if method != 'GET':
        raise NameError
    elif protocol[:8] != 'HTTP/1.1':
        raise ValueError
    elif '127.0.0.1' not in address and str(PORT_NUMBER) not in port:
        raise TypeError
    return uri


def resolve_uri(parse_request):
    """Uri from parse_request, returns tuple of content, filetype."""
    file_type_dict = {
        "txt": "text/plain",
        "html": "text/html",
        "png": "image/png",
        "jpg": "image/jpg",
        "jpeg": "image/jpeg",
        "py": "text/py",
    }
    my_uri = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          parse_request)

    if os.path.isfile(my_uri):
        file_type = parse_request.split('.')
        f = open(my_uri, 'rb')
        content = f.read()
        file_type_tuple = (content, file_type_dict[file_type[-1]])
        f.close()
        return file_type_tuple
    elif os.path.isdir(my_uri):
        return html_directory(my_uri)
    else:
        raise IOError('raise IOError')


def html_directory(my_uri):
    """Take client request, if dir, returns html links to dir files within."""
    curr_directory = os.listdir(my_uri)
    directory_list = ["<a src={0}>{0}</a>".format(item)
                      for item in curr_directory]
    html_string = " ".join(directory_list)
    return (html_string, "text/html")


if __name__ == '__main__':
    server()
