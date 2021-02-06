#!/usr/bin/env python3

from socket import *
import sys

args = sys.argv

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((args[1], int(args[2])))

clientSocket.send('GET '.encode())
clientSocket.send(args[3].encode())
clientSocket.send(' HTTP/1.1\r\n'.encode())
clientSocket.send('HOST: '.encode())
clientSocket.send(args[1].encode())
clientSocket.send('\r\n\r\n'.encode())

while True:
    message = clientSocket.recv(1024)
    if not message: break
    print(message.decode(), end='')

clientSocket.close()
sys.exit()
