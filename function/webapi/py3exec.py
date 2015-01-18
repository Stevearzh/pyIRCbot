#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import json

def reply(url, s):
	try:
		response = urllib2.urlopen(url + urllib.quote(s.encode("utf8")))
		data = response.read()
		result = json.loads(data)
		re = result['trace'][1]['stdout']
		if len(re) == 0:
			re = "<no output>"
		return re.decode("utf8")
	except:
		return "玩坏掉了。"
