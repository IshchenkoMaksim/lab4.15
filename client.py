#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print('Подключение к {} порт {}'.format(*server_address))
conn = sock.connect(server_address)

while True:
    command = input(">> ")
    command_line = bytes(command, "utf-8")
    sock.sendall(command_line)
    data = sock.recv(1024)
    if command == "exit":
        sys.exit()
    print("{}".format(data.decode("utf-8")))
