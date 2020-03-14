import socket
import logging

import templates

from tabulate import tabulate
logging.basicConfig(format="%(asctime)s|%(message)s")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5000))
server_socket.listen()
table =tabulate(tabular_data={('egor', 12), ("pavei", 16), ('ivan', 90)},
         headers= ['user', 'min'],
         tablefmt="HTML"
)

views = {'/main': b'HTTP/1.1 200 OK\n\n' + templates.main,
         "/shop": b'HTTP/1.1 200 OK\n\n ' + templates.shop,
         'user':('HTTP/1.1 200 OK\n\n' + table).encode("utf-8")}
def get_responce(request):
    if request:
        url = request[0].split()
        if len(url) > 1:
            url = url[1]
        else:
            logging.error("url is empty")
        if url == '/favicon.ico':
            logging.warning('yf')
        return views.get(url, b'HTTP/1.1 404 not found\n\n<h1>404)</h1>')

def sender(client, msg):
    if msg:
        client.sendall(msg)

while True:
    client, addr = server_socket.accept()
    logging.warning(f"accept client by addr {addr}")
    msg = client.recv(2048)
    request = (msg.decode('utf-8').split('\n'))
    response = get_responce(request)
    sender(client, response)