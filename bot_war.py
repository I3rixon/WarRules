#!/usr/bin/env python
import urllib2, re, time, hashlib, zlib
import simplejson as json


class GameBot():
	def __init__(self):
		self.wait = True
		self.buyed = False
		self.method = "TradingOffers.GetOffers"
		self.header = {
			"Connection": "close",
			"Content-Type": "text/html",
			"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.40 Safari/537.31",
			"Accept-Encoding": "deflate",
			"sign-code":"",
			"signin-authKey": "", # wireshark Luke
			"signin-userId":  "", # wireshark
			"server-method": self.method,
			"client-ver": 403
		}
		self.index = 0
		self.params = '{"x":0,"s":0,"n":0,"i":' + str(self.index) + ',"o":0,"c":6,"f":5,"d":null,"g":null}'
		self.url = 'http://173.244.186.146/GeoVk/Segment01/segment.ashx'
		self.counter = 1

	'''====== magic with sign-code here! ======='''
	def set_sing_code(self):
		self.header['sign-code'] = hashlib.md5('The Matrix has you...' + self.params + self.header['server-method'] + self.header['signin-userId'] + self.header['signin-authKey']).hexdigest()
		return self.header

	'''====== send request to game server ======='''
	def connect(self, buyed=False):
		# 'Skill maximum level reached'
		try:
			req = urllib2.Request(self.url, self.params, self.set_sing_code())
			response = urllib2.urlopen(req)
			if buyed == False:
				return zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
			else:
				try:
					return json.loads(response.read()[1:])["m"] # msg output
				except:
					return 'Buyed'
		except:
			None
	'''====== check progress of skill improvement ======='''
	# Todo: check number of skill (increment bruteforce?)
	def progress(self):
		#print self.index, self.header["server-method"]
		self.index += 6
		self.buyed = False
		data = json.loads(self.connect()[3:-33]) # get offers
		for items in data.get('o'):			#accept offers for money
			#print items
			if ( int(items["s"]["r"]["m"]) >= 3000 and (int(items["s"]["r"]["m"]) // int(items["o"]["r"]["u"]) <=4) and (int(items["s"]["r"]["m"]) // int(items["o"]["r"]["t"]) <=4)):
				print "BuyThis -> Money: %s\tTitanium: %s\tUranium: %s" % (items["o"]["r"]["m"], items["o"]["r"]["t"], items["o"]["r"]["u"]) # buy
				print "SoldThis -> Money: %s\tTitanium: %s\tUranium: %s" % (items["s"]["r"]["m"], items["s"]["r"]["t"], items["s"]["r"]["u"]) # sold
				self.header['server-method'] = "TradingOffers.AcceptOffer"
				pp = '{"t":1363981306465,"o":{"o":{"u":%s,"s":{"s":0,"d":null,"c":0,"r":{"u":%s,"m":%s,"c":0,"t":%s,"g":0}},"i":%s,"t":%s,"o":{"s":%s,"d":null,"c":%s,"r":{"u":%s,"m":%s,"c":0,"t":%s,"g":0}}}},"u":1363981012413,"q":[256,257,261],"g":294052,"r":40813}' % (items["u"], items["s"]["r"]["u"], items["s"]["r"]["m"], items["s"]["r"]["t"], items["i"], items["t"], items["o"]["s"], items["o"]["c"], items["o"]["r"]["u"], items["o"]["r"]["m"], items["o"]["r"]["t"])
				self.params = str(pp).replace("'", '"').replace(" ", "")
				self.buyed = True
				self.set_sing_code()
				print self.connect(self.buyed)
				if(self.index // 6 > 5 or self.buyed == True):
					self.index = 0
					self.params = '{"x":0,"s":0,"n":0,"i":' + str(self.index) + ',"o":0,"c":6,"f":5,"d":null,"g":null}'
					self.header['server-method'] = "TradingOffers.GetOffers"
					self.set_sing_code()

				print "===" * 20


bot = GameBot()
while True:
	bot.progress()
	if bot.index == 0:
		time.sleep(7)

