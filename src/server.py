"""functions to build the server side of echo."""


from __future__ import unicode_literals
import socket


def server():
    """Set up the server side to listen."""
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
    )
    address = ('127.0.0.1', 5016)
    server.bind(address)

    server.listen(1)
    print("Listening...")

    conn, addr = server.accept()

    while True:
        try:
            buffer_length = 8
            response = u''
            while response[-2:] != u"\r\n":
                part = conn.recv(buffer_length)
                response += part.decode('utf8')
                print('Recieved: ', part)

            print("Message sent...")
            conn.sendall(response.encode('utf8'))
            conn, addr = server.accept()

        except KeyboardInterrupt:
            print('\nClosing echo server...')
            break

    conn.close()
    server.close()


if __name__ == '__main__':
    server()
