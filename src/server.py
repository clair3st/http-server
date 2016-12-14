"""functions to build the server side of echo."""


from __future__ import unicode_literals
from sys import version_info
import socket


def server():
    """Set up the server side to listen."""
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
    )
    address = ('127.0.0.1', 5017)
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
            conn.sendall(server_good_connection().encode('utf8'))
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


def server_good_connection():
    """Send a HTTP response to client."""
    message = 'HTTP/1.1 200 OK\n'
    if version_info[0] == 2:
        message = message.decode('utf-8')
    message += u"\r\n"
    return message


def server_bad_connection():
    """Send a HTTP response to client if bad request."""
    message = 'HTTP/1.1 500 Internal Server Error\n'
    if version_info[0] == 2:
        message = message.decode('utf-8')
    return message


if __name__ == '__main__':
    server()
