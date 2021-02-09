from socket import *
import threading

class ServerWorker:
    connectionSocket = {}

    def __init__(self, connectionSocket):
        self.connectionSocket = connectionSocket

    def run(self):
        threading.Thread(target=self.work).start()

    def work(self):
        try:
            message = self.connectionSocket.recv(1024).decode()
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()
            #Send one HTTP header line into socket
            self.connectionSocket.send(message.split()[2].encode())
            self.connectionSocket.send(' 200 OK\r\n\r\n'.encode())
            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                self.connectionSocket.send(outputdata[i].encode())
            self.connectionSocket.send("\r\n".encode())

            self.connectionSocket.close()
        except IOError:
            #Send response message for file not found
            self.connectionSocket.send(message.split()[2].encode())
            self.connectionSocket.send(' 404 Not Found\r\n\r\n'.encode())
            self.connectionSocket.send('404 Not Found\r\n'.encode())
            #Close client socket
            self.connectionSocket.close();
