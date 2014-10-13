#!/usr/bin/env python
import socket
import sys
import getopt

# TCP client
# code skeleton from
# http://ilab.cs.byu.edu/python/socket/echoclient.html

def main():
	try:
		myopts, args = getopt.getopt(sys.argv[1:],"x:y:z")
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit()
	host = 'localhost'
	size = 1024

	hostname = sys.argv[1]
	print "host is ", hostname
	port = int(sys.argv[2])
	print "port is ", port
	#username = sys.argv[3]
	#print "username is ", username

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((host,port))
	s.connect((host, port))
	print "Welcome message: welcome to the server"

	while 1:
		cmd = raw_input("Enter a command: (send, print, or exit)\n")
		s.send(cmd)
		data = s.recv(size)

		if cmd == "exit":
			s.close()
			break
		elif cmd == "send":
			message = raw_input("Enter your message:")
			print 'Received:', data
		else:
			continue

# end code skeleton

if __name__ == "__main__":
	main()
        
