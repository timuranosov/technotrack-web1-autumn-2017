# -*- coding: utf-8 -*-
import socket
import os


def http_header_parser(request):
    headers = {}

    lines = request.split('\n')[1:]
    for string in lines:
        first_pos = string.find(":")
        headers[string[:first_pos]] = string[first_pos + 2:]

    return headers


def create_response(http_code, http_code_status, content):
    return "HTTP/1.1 " + str(http_code) + " " + http_code_status + "\n" \
           "Content-Type: text/html\n" \
           "Content-Length: " + str(len(content)) + "\n" \
           + content + "\n"


def get_response(request):
    method, url, protocol = request.split(' ')[:3]
    headers = http_header_parser(request)

    if len(request[0].split(' ')) < 3:
        return create_response(400, "Bad Request", "Not enough arguments")
    if method != "GET":
        return create_response(405, "Method Not Allowed", "Sorry, this server supports only GET-method")
    if url == "/":
        return create_response(200, "OK", "Hello mister!\nYou are: " + headers["User-Agent"])
    elif url == "/test":
        return request
    elif url == "/media":
        return "\n" + str((os.listdir('../files')))
    elif url.startswith('/media/'):
        try:
            with open('../files/' + url[url.rindex('/'):]) as f:
                header = create_response(200, "OK", str(len(f.read())))
                return header + "\n\n" + f.read()
        except IOError:
            return create_response(404, "Not found", "File not found")
    else:
        return create_response(404, "Not Found", "Page not found")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # привязка к сокету названия хоста и порта
server_socket.listen(0)  # максимальное количество клиентов в очереди на подключение

print 'Started'

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  # вывод IP-адрес подключенного клиента
        request_string = client_socket.recv(2048)  # получение данных от сокета клиента(максимально - 2 КБ)
        client_socket.send(get_response(request_string))  # отправка ответа клиента серверу
        client_socket.close()
    except KeyboardInterrupt:  # прерывание работы сервера вручную
        print 'Stopped'
        server_socket.close()  # закрытие сокета
        exit()
