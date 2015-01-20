#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import json

smURL = "http://xiaofengrobot.sinaapp.com/web.php?para="

def reply(string):
	try:
		response = urllib2.urlopen(smURL + urllib.quote(string.encode("utf8")))
		data = response.read()
		finalResult = data[6:-2]
		return finalResult.decode("unicode-escape")
	except:
		return "玩坏掉了。"