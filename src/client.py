"""Client side of server."""

import socket
from sys import argv, version_info
from server import BUFFER_LENGTH, PORT, ADDRESS


def client(message):
    """Setup client side."""
    infos = socket.getaddrinfo(ADDRESS, PORT)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]

    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    print("Connecting...")

    message += '\r\n'

    if version_info[0] == 2:
        print('python 2')
        message = message.decode("utf8")

    print("Sending: ", message.encode('utf8'))
    client.sendall(message.encode('utf8'))

    result = []

    while b"\r\n" not in b''.join(result):

        result.append(client.recv(BUFFER_LENGTH))

    result = b''.join(result)

    client.close()
    print(result[:-2].decode('utf8'))
    return result[:-2].decode('utf8')


def main():
    """Function initiates our echo server."""
    try:
        script, message = argv
        client(message)
    except:
        print('Oops, Something went wrong!')


if __name__ == '__main__':
    main()
