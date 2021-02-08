import threading, time
from socket import *

class Heartbeater:
    serverSocket = {}
    address = {}

    sequenceNumber = 0

    def __init__(self, address):
        self.address = address
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)

    def __del__(self):
        self.serverSocket.close()
        print('close')

    def run(self):
        threading.Thread(target=self.recv).start()
        threading.Timer(1, function=self.send).start()

    def send(self):
        while True:
            timeStamp = time.time()
            request = str(self.sequenceNumber) + ' ' + str(timeStamp)
            self.serverSocket.sendto(request.encode(), self.address)
            self.sequenceNumber += 1
            time.sleep(1)

    def recv(self):
        while True:
            respond, address = self.serverSocket.recvfrom(2048)
            print(respond.decode())
