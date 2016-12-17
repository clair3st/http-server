"""functions to build the server side of echo."""


from __future__ import unicode_literals
from sys import version_info
import socket
BUFFER_LENGTH = 8
ADDRESS, PORT = '127.0.0.1', 5004


def server():
    """Set up the server side to listen."""
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
    )
    address = (ADDRESS, PORT)
    server.bind(address)

    server.listen(1)
    print("Listening...")

    conn, addr = server.accept()

    while True:
        try:
            client_request = []
            while b"\r\n" not in b''.join(client_request):
                part = conn.recv(BUFFER_LENGTH)
                client_request.append(part)

            conn.sendall(response_ok())
            conn.sendall(b''.join(client_request))
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
    return message


def response_error():
    """Send a HTTP response to client if bad request."""
    message = 'HTTP/1.1 500 Internal Server Error\n'
    if version_info[0] == 2:
        message = message.decode('utf-8')
    message += u"\r\n"
    return message


if __name__ == '__main__':
    server()
