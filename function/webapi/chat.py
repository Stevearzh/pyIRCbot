#-*- encoding: utf-8 -*-

import urllib.request
import json

chatURL = "http://www.tuling123.com/openapi/api?key=b1833040534a6bfd761215154069ea58&info="

def reply(string):
	try:
		response = urllib.request.urlopen(chatURL + urllib.request.quote(string.encode("utf8")))
		data = response.read()
		result = json.loads(data.decode("utf8"))
		finalResult = result['text']
		return finalResult
	except:
		return "玩坏掉了。"
