#!/usr/bin/env python3

import ssl, sys
from socket import *
from base64 import b64encode

serverHost = ''
serverPort =

mailFrom = ''
rcptTo = ''

username = ''
password = ''

imagePath = "image.jpg"
f = open(imagePath, 'rb')
imageBase64 = b64encode(f.read())

msg = "\
MIME-Version: 1.0\r\n\
Content-Type: multipart/mixed; boundary=frontier\r\n\
\r\n\
This is a message with multiple parts in MIME format.\r\n\
--frontier\r\n\
Content-Type: text/plain\r\n\
\r\n\
I love computer networks!\r\n\
--frontier\r\n\
Content-Type: image/jpeg\r\n\
Content-Transfer-Encoding: base64\r\n\
\r\n".encode() + \
imageBase64 + "\r\n\
--frontier--".encode()
endmsg = b"\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = (serverHost, serverPort)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send EHLO command and print server response.
ehloCommand = 'EHLO Alice\r\n'
clientSocket.send(ehloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send STARTTLS command and print server response.
startTLSCommand = 'STARTTLS\r\n'
clientSocket.send(startTLSCommand.encode())
recv0 = clientSocket.recv(1024).decode()
print(recv0)
if recv0[:3] != '220':
    print('220 reply not received from server.')

context = ssl.create_default_context()
ssocket = context.wrap_socket(clientSocket, server_hostname=serverHost)

# Send EHLO command and print server response.
ehloCommand = 'EHLO Alice\r\n'
ssocket.send(ehloCommand.encode())
recv1 = ssocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send AUTH command and print server response.
authCommand = 'AUTH LOGIN\r\n'
ssocket.send(authCommand.encode())
recv0 = ssocket.recv(1024).decode()
print(recv0)
if recv0[:3] != '334':
    print('334 reply not received from server.')

username = b64encode(username.encode()) + b'\r\n'
ssocket.send(username)
recv0 = ssocket.recv(1024).decode()
print(recv0)
if recv0[:3] != '334':
    print('334 reply not received from server.')

password = b64encode(password.encode()) + b'\r\n'
ssocket.send(password)
recv0 = ssocket.recv(1024).decode()
print(recv0)
if recv0[:3] != '235':
    print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
fromCommand = 'MAIL FROM: <' + mailFrom + '> BODY=8BITMIME\r\n'
ssocket.send(fromCommand.encode())
recv2 = ssocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptToCommand = 'RCPT TO: <' + rcptTo + '>\r\n'
ssocket.send(rcptToCommand.encode())
recv3 = ssocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
ssocket.send(dataCommand.encode())
recv4 = ssocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
ssocket.send(msg)
# Message ends with a single period.
ssocket.send(endmsg)
recv5 = ssocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
ssocket.send(quitCommand.encode())
recv6 = ssocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '221':
    print('221 reply not received from server.')

ssocket.close()
sys.exit()
