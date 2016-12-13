"""functions to build the server side of echo."""


import socket


def server():
    """Set up the server side to listen."""
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
    )
    address = ('127.0.0.1', 5003)
    server.bind(address)
    server.listen(1)
    print("Listening...")
    try:
        while True:
            conn, addr = server.accept()
            buffer_length = 8
            message_complete = False
            while not message_complete:
                part = conn.recv(buffer_length)
                print(part.decode('utf8'))
                if len(part) < buffer_length:
                    message_complete = True
            message = "I hear you, loud and clear!"
            print("Message sent...")
            conn.sendall(message.encode('utf8'))
            conn.close()
    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    server()
