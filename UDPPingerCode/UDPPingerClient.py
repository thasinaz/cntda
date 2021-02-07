#!/usr/bin/env python3

import sys, time
from socket import *

args = sys.argv

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
address = (sys.argv[1], int(sys.argv[2]))

minimum = float('inf')
maximum = 0
accTime = 0
recvCount = 0
averageRTT = float('inf')

for i in range(1, 11):
    sendTime = time.time()
    request = 'Ping ' + str(i) + ' ' + str(sendTime)
    clientSocket.sendto(request.encode(), address)
    try:
        respond = clientSocket.recv(2048)
        recvTime = time.time()
        rtt = recvTime - sendTime

        print(respond.decode())
        print(recvTime - sendTime)

        if rtt < minimum: minimum = rtt
        if rtt > maximum: maximum = rtt
        accTime += rtt
        recvCount += 1
    except timeout:
        print('Request timed out')

if not recvCount: maximum = float('inf')
else: averageRTT = accTime / recvCount
print("\nminimum: {}\nmaximum: {}\naverage: {}\nlost rate: {}%".format(
    minimum, maximum, averageRTT, 100 - recvCount * 10))

clientSocket.close()
sys.exit()
