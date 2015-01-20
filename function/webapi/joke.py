#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import json

jokeURL = "http://www.tuling123.com/openapi/api?key=b1833040534a6bfd761215154069ea58&info="

def reply(string):
	try:
		response = urllib2.urlopen(jokeURL + urllib.quote("笑话".encode("utf8")))
		data = response.read()
		result = json.loads(data.decode("utf8"))
		finalResult = result['text']
		return finalResult.decode("utf8")
	except:
		return "玩坏掉了。"