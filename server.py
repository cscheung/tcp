#!/usr/bin/env python 

""" 
Server
""" 

import socket 
import sys
import string
class Server:

###################
# returns 1 if msg valid, else 0
###################

	store = []
	def __init__(self):
		pass

	def start(self, port_num):

		host = '' 
		port = port_num
		backlog = 5 
		size = 2048
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.bind((host,port)) 
		s.listen(backlog) 
		print 'listening for client'
		client, address = s.accept() 
		print 'Connected.'
		while 1: 
			print 'inside while'
			msg = client.recv(size)
			# message is received
			print msg
			if msg:
				print 'received'
				result = self.check_valid(msg)
				print 'message:', msg
				#print result
				if result != None:
					print result[0]
					if result[0] == 'lookup':
						print 'lookup'
						key = result[1]
						#print key
						lookup = self.lookupKey(self.store, key)
						#print lookup
						if lookup == None:
							reply = key + '='
							print key + '='
						else:
							reply = key + '=' + lookup
							print key + '=' + lookup
						#client.send(reply)
					elif result[0] == 'list':
						storeLength = len(self.store)
						self.printList(storeLength)
						#print self.store
					elif result[0] == 'listc':
						limit = result[1]
						self.printList(limit)
					elif result[0] == 'assign':
						key = result[1]
						value = result[2]
						self.store.append((key, value))
						print 'OK'
					
		msg = None
			#if data == 'exit':
				#sys.exit(0)
		client.close()

#########what should happen if list is empty?
	def printList(self, count):
		if count == 0: return None
		for item in self.store:
			if count == 0:
				return None
			print item[0] + '=' + item[1]
			count = count-1
		return None

	def lookupKey(self, list, key):
		for item in list:
			#print 'item0 is:'
			#print item[0]
			if item[0] == key:
				return item[1]
		return None
############
# Output options are None, lookup, list, listc, and assign
############
	def check_valid(self, msg):
		# for key query, return list containing label and key
		if msg[0] == '?':
			print 'lookup in check_valid'
			for letter in msg[1:len(msg)-1]:
				if (letter == '?') | (letter == '='):
					return None
			print 'return lookup'
			return ['lookup', msg[1:len(msg)-1]]
		elif msg == 'list\n':
			print 'list returned'
			return ['list']
		# check for listc
		elif msg[:6] == 'listc ':
			# check number after listc
			num = msg[6:len(msg)-1]
			for digit in num:
				# digit is between 0 and 9
				if (ord(digit) <= 48 | ord(digit) >=57):
					return None
				return ['listc']
		# assignment case
		else:
			splitstr = self.split_string_at(msg, '=')
			if splitstr == None:
				return None
			#for item in splitstr:
				#print item
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
#User input
############
server = Server()
server.start(8888)

