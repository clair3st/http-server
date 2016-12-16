"""functions to build the server side of echo."""


from __future__ import unicode_literals
import socket
from client import BUFFER_LENGTH, ADDRESS, PORT


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
            response = b''
            while response[-2:] != b"\r\n":
                part = conn.recv(BUFFER_LENGTH)
                response += part
                print('Recieved: ', part)

            print("Message sent...")
            conn.sendall(response)
            conn, addr = server.accept()

        except KeyboardInterrupt:
            print('\nClosing echo server...')
            break

    conn.close()
    server.close()


if __name__ == '__main__':
    server()
