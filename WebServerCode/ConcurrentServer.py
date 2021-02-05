#!/usr/bin/env python3

#import socket module
from socket import *
import sys # In order to terminate the program

from ServerWorker import ServerWorker

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverSocket.bind(('', 6789))
serverSocket.listen(1)
while True:
    #Establish the connection
    print('Ready to serve..')
    connectionSocket, addr = serverSocket.accept()
    ServerWorker(connectionSocket).run()
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
