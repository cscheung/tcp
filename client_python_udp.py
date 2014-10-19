#!/usr/bin/env python 

""" 
UDP
""" 

#from socket import *
import socket
import sys, string

class Client:

	def __init__(self):
		pass

	############
	# client sends msg
	# keeps sending same msg until ACK is received
	# each msg has 0 or 1 at the end so server
	# can identify duplicate
	############
	def start(self, host, port):
		addr = (host, port)
		size = 1024 
		count = 0
		ack = ''
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print 'tried sock'
		#sys.exit(1)
		#s.connect((host,port)) 
		#s.sendto('Hello, world', addr)
		#data = s.recv(size) 
		#s.close() 
		#print 'Received:', data
		print 'after timeout'

		while 1:
			#print 'inside while'
			line = sys.stdin.readline()
			if line == 'help\n':
				print 'Valid commands are: ?key, key=value, list,' +\
				'listc num, listc num continuationkey, help, and exit.'
			elif line == 'exit\n':
				sys.exit(0)
			
			if self.check_valid(line) == 1:
				line = str(count) + ' ' + line
				s.sendto(line, addr)
					#print 'before timeout'
				time = 0
				# 500 ms
				# tri-try: tries 3 times to get ACK
				# if unsuccessful, then timeout
				s.settimeout(2)
				try:
					print 'try 1'
					ack = s.recv(size)
				except:
					try:
						print 'try 2'
						ack = s.recv(size)
					except:
						try:
							print 'try 3'
							ack = s.recv(size)
						except: socket.timeout
						print 'caught timeout'
				if ack == 'ACK':
					count = (count + 1)%2
						#msg = s.recv(size)
				#while (msg != 'Received'):
					#print 'waiting for receive'
				#print 'message received!'
			'''
			else:
				print 'ERROR: Invalid command.'
				continue
			#reply = s.recv(size)
			#print 'server response:'
			#print reply
			reply = s.recv(size)
			if (reply == 'list') | (reply == 'listc'):
				print 'printing reply', reply
				if reply == 'listc':
					contChecker = s.recv(size)
					print 'printing contChecker', contChecker
					if contChecker == 'ERROR':
						print 'ERROR: Invalid continuation key.'
				listString = s.recv(size)
				storeList = listString.split('\n')
				for item in storeList:
					print item
			else:
				print reply
			'''
		#s.close()


###################
# returns 1 if msg valid, else 0
###################

	def check_valid(self, msg):
		if (msg[0] == '?'):
			for letter in (msg[1:]):
				if (letter == '?') | (letter == '='):
					return 0
			return 1
		elif msg == 'list\n':
			#for pair in store:
				#print pair[0], '=', pair[1]
			return 1
		# check for listc
		elif msg[:6] == 'listc ':
			# check number after listc
			tail = msg[6:len(msg)-1]
			tailList = tail.split()
			limit = tailList[0]
			for digit in limit:
				if (ord(digit) <= 48 | ord(digit) >=57):
					return 0
			if len(tailList) ==1:
				return 1
			elif len(tailList) == 2:
				#cont = tailList[1]
				if (ord(digit) <= 48 | ord(digit) >= 57):
					return 0
			return 1
				#for i in range(int(msg[6:])+1):
					#print store[i][0], '=', store[i][1]
		# assignment case
		else:
			splitstr = self.split_string_at(msg, '=')
			if splitstr == None:
				return 0
			#for item in splitstr:
				#print item
			lhs = splitstr[0]
			rhs = splitstr[1]
			for char in lhs:
				if (char == '?') | (char == '='):
					return 0
			for char in rhs:
				if (char == '?') | (char == '='):
					return 0
			return 1

	def split_string_at(self, string, char):
		index = string.find(char)
		if index == -1:
			return None
		lhs = string[:index]
		rhs = string[index+1:]
		return [lhs, rhs]

############
# main
############
client = Client()
client.start('localhost', 8888)
