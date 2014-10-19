#!/usr/bin/env python 
'''
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


import socket, sys, string


class Server:
	store = []

	def __init__self(self):
		pass

	def start(self, port_num):
		ACK = 'ACK'
		host = '' 
		port = port_num
		size = 1024 
		prevmsg = ''
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind((host,port)) 
		while 1: 
				#client, address = s.accept() 
				#data, addr = s.recvfrom(size) 
				#if data: 
						#s.sendto(data, addr) 
			currmsg, addr = s.recvfrom(size)
			# client did NOT receive ACK
			if currmsg == prevmsg:
				# send ACK again
				s.sendto(ACK, addr)
				continue
			# new message; send ACK
			s.sendto(ACK, addr)
			prevmsg = currmsg

			print currmsg
			#if currmsg:
				#print 'received'
				#result = self.check_valid(msg)
				#if result != None:
					#print result[0]
			currmsg = ''
		s.close()
			
'''
					if result[0] == 'lookup':
						#print 'lookup'
						key = result[1]
						#print key
						lookup = self.lookupKey(key)
						#print lookup
						if lookup == None:
							reply = key + '='
							#print key + '='
						else:
							reply = key + '=' + lookup
							#print key + '=' + lookup
						client.send(reply)
					elif result[0] == 'list':
						storeLength = len(self.store)
						#self.printList(storeLength)
						#print self.store
						client.send('list')
						sendList = ''
						for item in self.store:
							pair = item[0] + '=' + item[1]
							sendList = sendList + pair + '\n'
						sendList = sendList[:len(sendList)-1]
						client.send(sendList)
					elif result[0] == 'listc':
						client.send('listc')
						sendList = ''
						limit = int(result[1])
						cont = int(result[2])
						print 'cont is', cont
						# first time calling listc: set up nextCont
						if len(result) == 4:
							if result[3] == 'firstcont':
								self.nextCont = cont
						currPos = self.nextCont
						print 'stuck here?'
						if (self.nextCont != cont):
							client.send('ERROR')
							continue
						else:
							client.send('OK ?')
						print 'end error part'

						# prevents out of range in store
						if limit + self.nextCont > len(self.store):
							limit = len(self.store) - self.nextCont
						#print 'limit', limit

						#if self.nextCont + cont > len(self.store):
							#self.nextCont = len(self.store)
						#else:
							#self.nextCont = self.nextCont + cont
						# send list of items to be parsed in client
						for i in range(limit):
							pair = self.store[i+currPos][0] + '=' + self.store[i+currPos][1]
							sendList = sendList + pair + '\n'
							self.nextCont = i+currPos
						sendList = sendList + str(self.nextCont)
						client.send(sendList)

						#for i in range(limit):
							#print 'ok so far'
							#pair = self.store[i+currPos][0] + '=' + self.store[i+currPos][1]
							#sendList = sendList + pair
						#sendList = sendList + str(self.nextCont)
						#client.send(sendList)
						
						#self.printList(int(limit))
					elif result[0] == 'assign':
						#print 'assign!'
						key = result[1]
						value = result[2]
						index = self.findPartialTuple(key)
						# key has not been assigned
						if index != None:
							self.store[index] = (key, value)
						else:
							self.store.append((key, value))
						client.send('OK')
					
'''
		#msg = None
		#s.close()

'''
	def findPartialTuple(self, key):
		index = 0
		for item in self.store:
			if item[0] == key:
				return index
			index = index + 1
		return None
'''
'''
#########what should happen if list is empty?
	def printList(self, count):
		if count == 0: return None
		for item in self.store:
			if count == 0:
				return None
			print item[0] + '=' + item[1]
			count = count-1
		return None
'''
'''
	def lookupKey(self, key):
		for item in self.store:
			#print 'item0 is:'
			#print item[0]
			if item[0] == key:
				return item[1]
		return None
'''
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
'''
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
'''	

############
#main
############
port = int(sys.argv[1])
server = Server()
server.start(port)

