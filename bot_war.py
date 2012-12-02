#!/usr/bin/env python
import urllib2, re, time, hashlib


class GameBot():
	def __init__(self):
		self.wait = True
		self.header = {
			"Connection":"close",
			"Content-Type":"text/html",
			"sign-code":"",
			"signin-authKey":"",
			"signin-userId":"",
			"server-method":"ImproveSkill",
			"client-ver": 369
		}
		self.index = 1009		
		self.params = '{"n":{"n":1},"t":1354278702154,"o":{"i":' + str(self.index) + '},"u":1354278564016,"q":[195,208,209],"g":138138,"r":39185}'
		self.url = 'http://209.190.120.218/Geo/Segment01/segment.ashx'
		self.counter = 1

	'''====== magic with sign-code here! ======='''
	def set_sing_code(self):
		self.header['sign-code'] = hashlib.md5('The Matrix has you...' + self.params + self.header['server-method'] + self.header['signin-userId'] + self.header['signin-authKey']).hexdigest()
		return self.header

	'''====== send request to game server ======='''
	def connect(self):
		# 'Skill maximum level reached'
		req = urllib2.Request(self.url, self.params, self.set_sing_code())
		response = urllib2.urlopen(req)		
		return response.read()
	'''====== check progress of skill improvement ======='''
	# Todo: check number of skill (increment bruteforce?)
	def progress(self):
		data = self.connect()
		self.wait = True
		if(re.findall(r"Skill improvement already in progress", data)):
			print 'In progress'
			#return True
		elif(re.findall(r"Skill maximum level reached", data) or self.counter > 9):
			print 'All done'
			self.index += 1
			self.counter = 1			
			self.wait = False			
			#return False
		else:
			self.counter += 1
			print 'New cycle', self.counter			
			self.connect()			
			#return True



bot = GameBot()
while True:
	if(bot.progress() == False):
		break
	if bot.wait == True:
		time.sleep(300)