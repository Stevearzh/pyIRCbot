#-*- encoding: utf-8 -*-

import urllib.request
import json

smURL = "http://xiaofengrobot.sinaapp.com/web.php?para="

def reply(string):
	try:
		response = urllib.request.urlopen(smURL + urllib.request.quote(string.encode("utf8")))
		data = response.read()
		finalResult = data[6:-2]
		return finalResult.decode("unicode-escape")
	except:
		return "玩坏掉了。"