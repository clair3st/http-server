"""Server to run concurrently with server.py."""

from __future__ import unicode_literals

from server import response_ok, resolve_uri, parse_request, response_error

from server import ADDRESS

from gevent.server import StreamServer
from gevent.monkey import patch_all

PORT_NUMBER = 5500
BUFFER_LENGTH = 1024


def server(socket, address):
    """Set up a concurrent socket server."""
    print("Listening...")

    while True:
        try:
            client_request = u''
            while client_request[-4:] != u"\r\n\r\n":
                part = socket.recv(BUFFER_LENGTH)
                # print(part)
                client_request += part.decode('utf8')

            print('Received request: ', client_request)
            try:
                parse = parse_request(client_request)
                response_body = resolve_uri(parse)
                print('this is concurrent', response_body)
                socket.sendall(response_ok(response_body))
            except IOError:
                socket.sendall(response_error('404'))
                print('IOError')
            except SyntaxError:
                socket.sendall(response_error('400'))
            except NameError:
                socket.sendall(response_error('405'))
            except ValueError:
                socket.sendall(response_error('505'))
            except TypeError:
                socket.sendall(response_error('404'))

        except KeyboardInterrupt:
            print('\nClosing echo server...')
            break

    socket.close()


if __name__ == '__main__':
    patch_all()
    server = StreamServer((ADDRESS, PORT_NUMBER), server)
    print("Starting concurrency server now... ")
    server.serve_forever()
