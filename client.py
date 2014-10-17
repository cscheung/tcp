#!/usr/bin/env python 

""" 
simple socket client
""" 

import socket 
import sys, re

class Client:

	def _init_(self):
		pass

	def start(self, host, port):
		size = 1024 
		exit = 0
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.connect((host,port)) 

		while 1:
			#print 'inside while'
			line = sys.stdin.readline()
			if self.check_valid(line) == 1:
				s.send(line)
				#msg = s.recv(size)
				#while (msg != 'Received'):
					#print 'waiting for receive'
				#print 'message received!'
			else:
				print 'ERROR: Invalid command.'
			reply = s.recv(size)
			print 'server response:'
			print reply
		s.close()

###################
# returns 1 if msg valid, else 0
###################
	def check_valid(self, msg):
		if msg[0] == '?':
			for letter in msg[1:]:
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
			num = msg[6:len(msg)-1]
			for digit in num:
				print digit
				# digit is between 0 and 9
				if (ord(digit) <= 48 | ord(digit) >=57):
					print 'did not pass digit test'
					return 0
				print 'number part is ok'
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
			
				
'''
		if re.match(valid_key_query, msg) != None:
			print 'valid'
			return 1
		elif (re.match( valid_key_set, msg ) != None):
			print 'valid2'
			return 1
		elif (re.match( valid_listc_num, msg ) != None):
			print 'valid listc'
			return 1
		elif (re.match( valid_list, msg ) != None):
			print 'list valid'
			return 1
		else:
			print 'not valid key query'
			return 0
		#else:
			#return 0
'''


###################
# Start client
###################
store = []
client = Client()
host = sys.argv[1]
port = int(sys.argv[2])
client.start(host, port)

