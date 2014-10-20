#!/usr/bin/env python 
'''
TCP Server in Python
@author Crystal Cheung
@date 10/19/14
CS176A
perm: 5228051
'''

'''
Citation
Source: http://ilab.cs.byu.edu/python/socket/echoserver.html
Author: Daniel Zappala
-A simple echo server off of which I built my code
'''

import socket 
import sys
import string
class Server:

	store = []
	nextCont = 0
	def __init__(self):
		pass

	def start(self, port_num):

		host = '' 
		port = port_num
		backlog = 5 
		size = 2048
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		try:
			s.bind((host,port)) 
		except socket.error, (value, message):
			sys.exit(1)
		s.listen(backlog) 
		try:
			client, address = s.accept() 
		except socket.error:
			print 'ERROR: Could not connect to server. Terminating.'
			sys.exit(1)

		print 'Connected.'
		while 1: 
			try:
				msg = client.recv(size)
			except socket.error:
				print 'ERROR: Failed to receive message. Terminating.'
				sys.exit(1)

			print msg
			if msg:
				#print 'received'
				result = self.check_valid(msg)
				if result != None:
					#print result[0]
					if result[0] == 'lookup':
						key = result[1]
						lookup = self.lookupKey(key)
						if lookup == None:
							reply = key + '='
						else:
							reply = key + '=' + lookup
						try:
							client.send(reply)
						except socket.error:
							print 'ERROR: Failed to send message. Terminating.'
							sys.exit(1)
					########
					# Case: List.
					# Sends message that says 'list' so client knows it's about
					# to receive a list
					# then send string of list elements separatd by \n
					########
					elif result[0] == 'list':
						storeLength = len(self.store)
						try:
							client.send('list')
						except socket.error:
							print 'ERROR: Failed to send message. Terminating.'
							sys.exit(1)
						sendList = ''
						for item in self.store:
							pair = item[0] + '=' + item[1]
							sendList = sendList + pair + '\n'
						sendList = sendList[:len(sendList)-1]
						try:
							client.send(sendList)
						except socket.error:
							print 'ERROR: Failed to send message. Terminating.'
							sys.exit(1)
					########
					# Case: Listc.
					# Sends message that says 'listc' so client knows listc coming
					# then send string of list elements separated by \n
					########
					elif result[0] == 'listc':
						try:
							client.send('listc')
						except socket.error:
							print 'ERROR: Failed to send message. Terminating.'
							sys.exit(1)
						sendList = ''
						limit = int(result[1])
						cont = int(result[2])
						# first time calling listc: set up nextCont
						if len(result) == 4:
							if result[3] == 'firstcont':
								self.nextCont = cont
						currPos = self.nextCont
						if (self.nextCont != cont):
							try:
								client.send('ERROR')
								continue
							except socket.error:
								print 'ERROR: Failed to send message. Terminating.'
								sys.exit(1)
						else:
							try:
								client.send('OK ?')
							except socket.error:
								print 'ERROR: Failed to send message. Terminating.'
								sys.exit(1)

						# prevents out of range in store
						if limit + self.nextCont > len(self.store):
							limit = len(self.store) - self.nextCont
						# send list of items to be parsed in client
						for i in range(limit):
							pair = self.store[i+currPos][0] + '=' + self.store[i+currPos][1]
							sendList = sendList + pair + '\n'
							self.nextCont = i+currPos
						sendList = sendList + str(self.nextCont)
						try:
							client.send(sendList)
						except socket.error:
							print 'ERROR: Failed to send message. Terminating.'
							sys.exit(1)
					########
					# Case: Assign
					# Searches store for a key value equal to lhs
					# If found, replaces old value
					# else, appends new pair to list
					########
					elif result[0] == 'assign':
						key = result[1]
						value = result[2]
						index = self.findPartialTuple(key)
						# key has not been assigned
						if index != None:
							self.store[index] = (key, value)
						else:
							self.store.append((key, value))
						try:
							client.send('OK')
						except socket.error:
							print 'ERROR: Failed to send message. Terminating.'
							sys.exit(1)
		msg = None
		client.close()

	def findPartialTuple(self, key):
		index = 0
		for item in self.store:
			if item[0] == key:
				return index
			index = index + 1
		return None

	def lookupKey(self, key):
		for item in self.store:
			if item[0] == key:
				return item[1]
		return None

############
# Returns None if command is not valid
# Valid cases:
# -Lookup, returns list containing 'lookup' and the key
# -List, returns list containing 'list'
# -Listc, returns list containing 'listc',
#		the limit value, continuation key,
#		and 'firstcont' if it is the first time calling listc
# -Assignment, returns list containing 'assign', lhs, and rhs
#		of the input
############

	def check_valid(self, msg):
		# for key query, return list containing label and key
		if msg[0] == '?':
			for letter in msg[1:len(msg)-1]:
				if (letter == '?') | (letter == '='):
					return None
			return ['lookup', msg[1:len(msg)-1]]
		elif msg == 'list\n':
			#print 'list returned'
			return ['list']
		# check for listc
		elif msg[:6] == 'listc ':
			# check number after listc
			tail = msg[6:len(msg)-1]
			tailList = tail.split()
			limit = tailList[0]
			for digit in limit:
				# digit is between 0 and 9
				if (ord(digit) <= 48 | ord(digit) >=57):
					return None
				if len(tailList) == 1:
					cont = limit
					return ['listc', limit, cont, 'firstcont']
				elif len(tailList) == 2:
					cont = tailList[1]
					for digit in cont:
						if (ord(digit) <= 48 | ord(digit) >= 57):
							return None
						else:
							return ['listc', limit, cont]

		# assignment case
		else:
			splitstr = self.split_string_at(msg, '=')
			if splitstr == None:
				return None
			lhs = splitstr[0]
			rhs = splitstr[1]
			for char in lhs:
				if (char == '?') | (char == '='):
					return None
			for char in rhs:
				if (char == '?') | (char == '='):
					return None
			return ['assign', lhs, rhs]

	def split_string_at(self, string, char):
		index = string.find(char)
		if index == -1:
			return None
		lhs = string[:index]
		rhs = string[index+1:len(string)-1]
		return [lhs, rhs]
	

##############
#main
############

if len(sys.argv) != 2:
	print 'ERROR: Invalid number of args. Terminating.'
	sys.exit(1)
port = int(sys.argv[1])
if (port < 1024) | (port > 65536):
	print 'ERROR: Invalid port. Terminating.'
	sys.exit(1)
server = Server()
server.start(port)

