#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
from time import perf_counter
from random import choice

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

sock.listen(1)

while True:
    print('Ожидание соединения')
    connection, client_address = sock.accept()
    start_time = 0
    status = choice(['розетка неактивна', 'розетка активна'])
    try:
        if status == 'розетка активна':
            print('Подключено к:', client_address, ',', status)
            start_time = perf_counter()
        else:
            print('Подключено к:', client_address, ',', status)
        while True:
            data = connection.recv(1024)
            data_decode = data.decode("utf-8")
            print('Получено: {} '.format(data_decode))
            if data_decode == "on":
                if status == 'розетка активна':
                    msg = "Розетка уже включена".encode(encoding="utf-8")
                    connection.sendall(msg)
                else:
                    msg = "Розетка включена".encode(encoding="utf-8")
                    start_time = perf_counter()
                    status = "розетка активна"
                    connection.sendall(msg)
            elif data_decode == "off":
                if status == 'розетка неактивна':
                    msg = f"Розетка уже выключена".encode(encoding="utf-8")
                    connection.sendall(msg)
                else:
                    msg = f"Розетка выключена, время работы={perf_counter() - start_time:0.4f}"
                    msg_by = str(msg).encode(encoding="utf-8")
                    print(f"Розетка выключена, время работы={perf_counter() - start_time:0.4f}")
                    status = 'розетка неактивна'
                    connection.sendall(msg_by)
            elif data_decode == "info":
                msg = f"Розетка №1, состояние: {status}".encode(encoding="utf-8")
                connection.sendall(msg)
            elif data_decode == "exit":
                print("Завершение работы сервера")
                connection.close()
                sys.exit()

            else:
                print('Нет данных от:', client_address)
                break

    finally:
        connection.close()
