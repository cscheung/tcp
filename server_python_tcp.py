#!/usr/bin/env python
import socket               # Import socket module
import sys
import uuid


# code skeleton from 
# http://ilab.cs.byu.edu/python/socket/echoserver.html

host = ''
port = 5000
backlog = 5
size = 1024
idDict = {}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)

username = "user"

uuid = uuid.uuid4()
idDict[uuid] = username
while 1:
    client, address = s.accept()
    #takes size number of bytes message
    data = client.recv(size)
    if data:
    #sends data to client
       client.send(data)
    client.close()




# end byu code skeleton





