#!/usr/bin/env python3

from socket import *
import sys, os

if len(sys.argv) <= 1:
    print('Usage: "python ProxyServer.py server_ip"\n\
           [server_ip: It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(1)
while 1:
    # Start receiving data from the client
    print('Ready to server...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()
    print(message)
    # Extract the filepath from the given message
    print(message.split()[1])
    filepath = message.split()[1][1:]
    print(filepath)
    cachePath = "./cache/" + filepath + ".cache"
    print(cachePath)
    fileExist = "false"
    try:
        # Check wether the file exist in the cache
        f = open(cachePath, "rb")
        outputdata = f.read()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type: text/html\r\n".encode())
        tcpCliSock.send("Content-Length: {}\r\n\r\n".format(len(outputdata)).encode())
        tcpCliSock.send(outputdata)
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == 'false':
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filepath.partition("/")[0]
            print(hostn)
            url = "/" + filepath.partition("/")[2]
            print(url)
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))
                # Create a temporary file on this socket and ask port 80 for
                # the file requested by the client
                fileobj = c.makefile('rwb')
                fileobj.write(b"GET " + url.encode() + b" HTTP/1.0\r\n\r\n")
                fileobj.flush()
                # Read the response into buffer
                respondLine = fileobj.readline()
                buffer = respondLine
                if respondLine.split()[1] == b'200':
                    contentLength = 0
                    isHtml = False
                    while True:
                        line = fileobj.readline()
                        buffer += line
                        if line == b'\r\n': break
                        if line[:16] == b"Content-Length: ":
                            contentLength = int(line[16:])
                        if line[:14] == b"Content-Type: ":
                            if line[14:] == b"text/html\r\n":
                                isHtml = True
                    if isHtml:
                        tcpCliSock.send(buffer)
                        buffer = fileobj.read()
                        # Create a new file in the cache for the requested file.
                        # Also send the response in the buffer to client socket and the
                        os.makedirs(os.path.dirname(cachePath), exist_ok=True)
                        tmpFile = open(cachePath,"wb")
                        tmpFile.write(buffer)
                        tmpFile.close()
                    else:
                        buffer += fileobj.read()
                else:
                    buffer += fileobj.read()
                tcpCliSock.send(buffer)
                fileobj.close()
                c.close()
            except IOError:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.0 404 NOT FOUND\r\n\r\n".encode())
            tcpCliSock.send("404 NOT FOUND\r\n".encode())
    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()
sys.exit()
