"""Client side of server."""


# from __future__ import unicode_literals
import socket
from sys import argv, version_info


BUFFER_LENGTH = 8


ADDRESS = '127.0.0.1'
PORT = 5017


def client(message):
    """Setup client side."""
    infos = socket.getaddrinfo(ADDRESS, PORT)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]

    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    print("Connecting...")

    message += '\r\n'

    if version_info[0] == 2:
        message = message.decode("utf8")

    print("Sending: ", message.encode('utf8'))
    client.sendall(message.encode('utf8'))

    result = ""

    while result[-2:] != u"\r\n":

        part = client.recv(BUFFER_LENGTH)
        result += part.decode('utf8')

    client.close()
    print(result[:-2])
    return result[:-2]


def main():
    """Function initiates our echo server."""
    try:
        script, message = argv
        client(message)
    except ValueError:
        print('Oops, Something went wrong! Please add a message')

if __name__ == '__main__':
    main()
