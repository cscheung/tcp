#!/usr/bin/env python 

'''
TCP Client in Python
@author Crystal Cheung
@date 10/19/14
CS176A
perm: 5228051
'''
'''
Citation:
Source: http://ilab.cs.byu.edu/python/socket/echoclient.html
Author: Daniel Zappala
-A simple echo client off of which I built my code
'''


import socket 
import sys

class Client:

	nextCont = 0

	def _init_(self):
		pass

	def start(self, host, port):
		size = 1024 
		exit = 0
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		except socket.error, (value, message):
			print 'Could not bind port. Terminating.'
			sys.exit(1)
		try:
			s.connect((host,port)) 
		except socket.error:
			print 'ERROR: Could not connect to server. Terminating.'
			sys.exit(1)

		while 1:
			#print 'inside while'
			line = sys.stdin.readline()
			if line == 'exit\n':
				sys.exit(0)
			elif line == 'help\n':
				print 'valid commands are: ?key, key=value, list,' + \
				' listc num, listc num continuationkey, exit, and help'
				continue

			if self.check_valid(line) == 1:
				#print 'checked valid'
				try:
					s.send(line)
				except socket.error:
					print 'ERROR: Failed to send message. Terminating.'
					sys.exit(1)
			else:
				print 'ERROR: Invalid command.'
				continue
			try:
				reply = s.recv(size)
			except socket.error:
				print 'ERROR: Failed to receive message. Terminating.'
				sys.exit(1)
			###Something weird is going on with this.
			# sometimes, this condition gets skipped when it shouldn't
			# and then next time, list will print as many times as it got skipped
			if (reply == 'list') | (reply == 'listc'):
				#print '2'
				if reply == 'listc':
					# check continuation key
					try:
						contChecker = s.recv(size)
					except socket.error:
						print 'ERROR: Failed to receive message. Terminating.'
						sys.exit(1)
					if contChecker == 'ERROR':
						print 'ERROR: Invalid continuation key.'
				try:
					listString = s.recv(size)
				except socket.error:
					print 'ERROR: Failed to receive message. Terminating.'
					sys.exit(1)
				storeList = listString.split('\n')
				#print '3'
				for item in storeList:
					print item
				#print '4'
			else:
				print reply
			#print '5'
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
if len(sys.argv) != 3:
	print 'ERROR: Invalid number of args. Terminating.'
	sys.exit(1)
client = Client()
host = sys.argv[1]
port = int(sys.argv[2])
if (port < 1024) | (port > 65535):
	print 'ERROR: Invalid port. Terminating.'
	sys.exit(1)
client.start(host, port)

