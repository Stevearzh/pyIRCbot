#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import json

def reply(url, s):
    try:
    	if len(s) < 9:
        	response = urllib2.urlopen(url + "笑话%20大基佬" + urllib.quote(s.encode("utf8")))
        else:
        	response = urllib2.urlopen(url + "笑话%20" + urllib.quote(s.encode("utf8")))
        data = response.read()
        result = json.loads(data.decode("utf8"))
        re = result['text']
        return re.decode("utf8")
    except:
        return "玩坏掉了。"