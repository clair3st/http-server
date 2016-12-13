"""Client side of server."""


import socket
from sys import argv

# def get_constants(prefix):
#    """mapping of socket module constants to their names"""
#     return {getattr(socket, n): n
#     for n in dir(socket)
#     if n.startswith(prefix)
# }


def client(message):
    """Setup client side."""
    from server import server
    server()
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(message.encode('utf8'))
    buffer_length = 8
    reply_complete = False
    while not reply_complete:
        part = client.recv(buffer_length)
        print(part.decode('utf8'))
        if len(part) < buffer_length:
            break


def main():
    """Function initiates our echo server."""
    try:
        script, message = argv
        client(message)
    except:
        print('Oops, Something went wrong!')


if __name__ == '__main__':
    main()
