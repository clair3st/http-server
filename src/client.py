"""Client side of server."""

from __future__ import unicode_literals
import socket
from sys import argv, version_info
from server import PORT_NUMBER, ADDRESS, BUFFER_LENGTH


def client(message):
    """Setup client side."""
    infos = socket.getaddrinfo(ADDRESS, PORT_NUMBER)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]

    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    print("Connecting...")

    message += '\r\n\r\n'

    if version_info[0] == 2:
        print('python 2')
        message = message.decode("utf8")

    print("Sending: ", message.encode('utf8'))
    client.sendall(message.encode('utf8'))

    result = []

    while b"\r\n\r\n" not in b''.join(result):

        result.append(client.recv(BUFFER_LENGTH))

    result = b''.join(result)
    if b'text' in result:
        result = result.decode('utf8')
    client.close()
    print(result[:-4])
    return result[:-4]


def main():
    """Function initiates our echo server."""
    try:
        script, message = argv
        client(message)
    except ValueError:
        print('Oops, Something went wrong!')


if __name__ == '__main__':
    main()
